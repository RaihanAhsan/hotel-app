# backend/routers/payment.py
from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from .. import models, schemas
from ..database import get_db
from ..services.xendit_service import xendit_service
from ..auth import get_current_user
import json
from datetime import datetime

router = APIRouter(prefix="/api/payment", tags=["Payment"])

@router.post("/create-invoice", response_model=schemas.XenditInvoiceResponse)
async def create_payment_invoice(
    data: schemas.XenditInvoiceCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """
    Membuat invoice pembayaran melalui Xendit berdasarkan booking yang sudah dibuat.
    """
    print("📥 Received data:", data.dict())

    # Validasi booking – pastikan booking milik user yang sedang login
    booking = db.query(models.Booking).filter(
        models.Booking.id == data.booking_id,
        models.Booking.email == current_user.email
    ).first()
    
    if not booking:
        print(f"❌ Booking not found: id={data.booking_id}, email={current_user.email}")
        raise HTTPException(status_code=404, detail="Booking not found")
    
    # Buat external_id unik
    external_id = f"BOOKING-{data.booking_id}-{int(datetime.now().timestamp())}"
    
    # Siapkan item detail untuk invoice
    items = [
        {"name": data.room_name, "quantity": 1, "price": data.amount, "category": "Hotel Room"},
        {"name": f"Check-in: {data.checkin}", "quantity": 1, "price": 0, "category": "Info"},
        {"name": f"Check-out: {data.checkout}", "quantity": 1, "price": 0, "category": "Info"},
        {"name": f"Guests: {data.guests}", "quantity": 1, "price": 0, "category": "Info"},
    ]
    
    # 🔁 Konversi USD ke IDR (jika diperlukan)
    usd_amount = data.amount
    try:
        import requests
        response = requests.get("https://api.exchangerate-api.com/v4/latest/USD")
        rates = response.json().get('rates', {})
        idr_rate = rates.get('IDR', 15000)
        idr_amount = int(usd_amount * idr_rate)
        print(f"💱 Kurs: 1 USD = {idr_rate} IDR, amount IDR: {idr_amount}")
    except Exception as e:
        print(f"❌ Gagal ambil kurs: {e}, pakai default 15000")
        idr_amount = int(usd_amount * 15000)

    # 🎯 Tentukan URL redirect setelah pembayaran
    # Ganti dengan URL halaman My Bookings di frontend Anda
    MY_BOOKINGS_URL = f"http://localhost:5173/my-bookings?payment=success&booking_id={data.booking_id}"
    FAILURE_URL = "http://localhost:5173/payment-failed"

    # Panggil service Xendit
    try:
        result = xendit_service.create_invoice(
            external_id=external_id,
            amount=idr_amount,                     # Kirim dalam IDR
            payer_email=data.payer_email,
            payer_name=data.payer_name,
            description=f"Hotel Booking - {data.room_name}",
            items=items,
            success_redirect_url=MY_BOOKINGS_URL,  # ⬅️ Arahkan ke My Bookings
            failure_redirect_url=FAILURE_URL       # ⬅️ Halaman gagal
        )
        print("📤 Xendit response:", result)
    except Exception as e:
        print(f"❌ Exception from xendit_service: {e}")
        raise HTTPException(status_code=500, detail=f"Xendit service error: {str(e)}")
    
    if result.get("success"):
        booking.xendit_invoice_id = result.get("invoice_id")
        db.commit()
        return result
    else:
        error_msg = result.get("error", "Unknown error from Xendit")
        print(f"❌ Xendit error: {error_msg}")
        raise HTTPException(status_code=400, detail=error_msg)


@router.get("/invoice-status/{invoice_id}")
async def get_invoice_status(invoice_id: str):
    result = xendit_service.get_invoice_status(invoice_id)
    return result


@router.post("/webhooks/xendit")
async def xendit_webhook(request: Request, db: Session = Depends(get_db)):
    try:
        body = await request.json()
        print(f"📩 Webhook received: {json.dumps(body, indent=2)}")
        
        # ===== PERBAIKAN: Langsung ambil dari body =====
        # Xendit invoice webhook mengirimkan data langsung, bukan dalam "data" wrapper
        status = body.get("status")
        external_id = body.get("external_id")
        invoice_id = body.get("id")
        
        print(f"🔍 Status: {status}, external_id: {external_id}, invoice_id: {invoice_id}")
        
        # Proses jika status PAID
        if status and status.upper() == "PAID":
            print("✅ Payment confirmed, updating booking...")
            
            parts = external_id.split("-")
            if len(parts) >= 2:
                booking_id_str = parts[1]
                try:
                    booking_id = int(booking_id_str)
                except ValueError:
                    print(f"❌ Invalid booking_id in external_id: {external_id}")
                    return {"status": "error", "message": "Invalid external_id format"}
                
                booking = db.query(models.Booking).filter(
                    models.Booking.id == booking_id
                ).first()
                
                if booking:
                    print(f"✅ Booking found: id={booking.id}, ref={booking.ref}, current status={booking.status}")
                    booking.status = "Paid"
                    booking.special = (booking.special or "") + f" | Paid via Xendit (ID: {invoice_id})"
                    db.commit()
                    print(f"✅ Booking {booking.ref} updated to Paid")
                else:
                    print(f"❌ Booking not found for id: {booking_id}")
            else:
                print(f"❌ Unexpected external_id format: {external_id}")
        else:
            print(f"ℹ️ Status bukan PAID atau tidak ada status: {status}")
            
        return {"status": "ok"}
    except Exception as e:
        print(f"❌ Webhook error: {e}")
        import traceback
        traceback.print_exc()
        return {"status": "error", "message": str(e)}
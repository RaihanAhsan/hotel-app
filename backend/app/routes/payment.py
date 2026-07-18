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
    current_user=Depends(get_current_user),
):
    """
    Membuat invoice Xendit untuk booking
    """
    # Validasi booking
    booking = db.query(models.Booking).filter(
        models.Booking.id == data.booking_id,
        models.Booking.email == current_user.email
    ).first()
    
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    
    # External ID unik untuk tracking
    external_id = f"BOOKING-{data.booking_id}-{int(datetime.now().timestamp())}"
    
    # Siapkan item invoice
    items = [
        {"name": data.room_name, "quantity": 1, "price": data.amount, "category": "Hotel Room"},
        {"name": f"Check-in: {data.checkin}", "quantity": 1, "price": 0, "category": "Info"},
        {"name": f"Check-out: {data.checkout}", "quantity": 1, "price": 0, "category": "Info"},
        {"name": f"Guests: {data.guests}", "quantity": 1, "price": 0, "category": "Info"},
    ]
    
    # Buat invoice di Xendit
    result = xendit_service.create_invoice(
        external_id=external_id,
        amount=data.amount,
        payer_email=data.payer_email,
        payer_name=data.payer_name,
        description=f"Hotel Booking - {data.room_name}",
        items=items,
    )
    
    if result["success"]:
        # ✅ SIMPAN ID INVOICE KE DATABASE
        booking.xendit_invoice_id = result["invoice_id"]
        db.commit()
        return result
    else:
        raise HTTPException(status_code=400, detail=result.get("error", "Failed to create invoice"))

@router.get("/invoice-status/{invoice_id}")
async def get_invoice_status(invoice_id: str):
    """
    Cek status invoice dari Xendit
    """
    result = xendit_service.get_invoice_status(invoice_id)
    return result

@router.post("/webhooks/xendit")
async def xendit_webhook(request: Request, db: Session = Depends(get_db)):
    """
    Endpoint untuk menerima webhook dari Xendit.
    Update status booking berdasarkan invoice yang dibayar.
    """
    try:
        body = await request.json()
        print(f"📩 Webhook received: {json.dumps(body, indent=2)}")
        
        event_type = body.get("type", "")
        data = body.get("data", {})
        
        if event_type == "invoice.paid":
            invoice_id = data.get("id")
            external_id = data.get("external_id")
            
            # ✅ UPDATE STATUS BOOKING
            # external_id format: BOOKING-{booking_id}-{timestamp}
            parts = external_id.split("-")
            if len(parts) >= 2:
                booking_id = parts[1]
                booking = db.query(models.Booking).filter(
                    models.Booking.id == int(booking_id)
                ).first()
                
                if booking:
                    booking.status = "Paid"
                    booking.special = f"{booking.special or ''} | Paid via Xendit (ID: {invoice_id})"
                    db.commit()
                    print(f"✅ Booking {booking.ref} updated to Paid")
                else:
                    print(f"⚠️ Booking with ID {booking_id} not found")
            
            print(f"✅ Payment confirmed for invoice: {invoice_id}")
            
        elif event_type == "invoice.expired":
            print(f"⏰ Invoice expired: {data.get('id')}")
            
        elif event_type == "invoice.failed":
            print(f"❌ Payment failed: {data.get('id')}")
            
        return {"status": "ok"}
        
    except Exception as e:
        print(f"❌ Webhook error: {e}")
        return {"status": "error", "message": str(e)}
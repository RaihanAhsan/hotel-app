# backend/routers/bookings.py
from fastapi import APIRouter, Depends, HTTPException, Request, status, Query
from sqlalchemy.orm import Session
from typing import Optional
from .. import models, schemas, auth
from ..database import get_db
import time

router = APIRouter(prefix="/api/bookings", tags=["bookings"])

# Endpoint OPTIONS untuk CORS (tetap dipertahankan)
@router.options("/")
@router.options("/{booking_id}")
async def options_bookings():
    return {"status": "ok"}

# GET daftar booking dengan filter email (tanpa trailing slash)
@router.get("", response_model=list[schemas.BookingOut])  # <-- tanpa slash
def get_bookings(
    email: Optional[str] = Query(None, description="Filter bookings by customer email"),
    db: Session = Depends(get_db),
    current_user = Depends(auth.get_current_user)
):
    """
    Mendapatkan semua booking milik pengguna saat ini.
    Jika parameter 'email' diberikan, filter berdasarkan email.
    """
    query = db.query(models.Booking)
    if email:
        # Asumsi kolom di model Booking adalah 'email' (sesuai dengan model Anda)
        query = query.filter(models.Booking.email == email)
    # Jika tidak ada filter email, tampilkan semua booking (atau bisa dibatasi untuk admin)
    bookings = query.all()
    return bookings

# GET booking by ID (harus diletakkan setelah get_all agar tidak tertimpa)
@router.get("/{booking_id}", response_model=schemas.BookingOut)
def get_booking_by_id(
    booking_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(auth.get_current_user)
):
    booking = db.query(models.Booking).filter(models.Booking.id == booking_id).first()
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    return booking

# POST create booking (sudah ada)
@router.post("/", response_model=schemas.BookingOut)
def create_booking(
    booking: schemas.BookingCreate, 
    db: Session = Depends(get_db),
    current_user = Depends(auth.get_current_user)
):
    # Generate unique ref
    ref = booking.ref or f"GRAND-{int(time.time())}"
    existing = db.query(models.Booking).filter(models.Booking.ref == ref).first()
    
    while existing:
        ref = f"GRAND-{int(time.time())}-{booking.guest[:4].upper()}"
        existing = db.query(models.Booking).filter(models.Booking.ref == ref).first()

    db_booking = models.Booking(
        ref=ref,
        guest=booking.guest,
        email=booking.email,
        room=booking.room,
        room_id=booking.room_id,
        checkin=booking.checkin,
        checkout=booking.checkout,
        guests=booking.guests,
        nights=booking.nights,
        total=booking.total,
        special=booking.special,
        card_last4=booking.card_last4 or "DUMMY",
        status="Pending"
    )
    db.add(db_booking)
    db.commit()
    db.refresh(db_booking)
    return db_booking
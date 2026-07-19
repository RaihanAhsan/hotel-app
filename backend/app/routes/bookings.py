# backend/routers/bookings.py
from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy.orm import Session
from .. import models, schemas, auth
from ..database import get_db
import time

router = APIRouter(prefix="/api/bookings", tags=["bookings"])

@router.options("/")
@router.options("/{booking_id}")
async def options_bookings():
    return {"status": "ok"}

@router.post("/", response_model=schemas.BookingOut)
def create_booking(
    booking: schemas.BookingCreate, 
    db: Session = Depends(get_db),
    current_user=Depends(auth.get_current_user)
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
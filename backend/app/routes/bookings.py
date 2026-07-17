import time
from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session
from .. import models, schemas, auth
from ..database import get_db

router = APIRouter(prefix="/api/bookings", tags=["bookings"])

@router.options("/")
@router.options("")
async def options_bookings_root():
    return Response(status_code=200)

@router.options("/{booking_id}")
async def options_booking_detail():
    return Response(status_code=200)

@router.post("/", response_model=schemas.BookingOut)
@router.post("", response_model=schemas.BookingOut)
def create_booking(booking: schemas.BookingCreate, db: Session = Depends(get_db)):
    # Cek apakah ref sudah ada (duplicate), jika ya generate ulang
    existing = db.query(models.Booking).filter(models.Booking.ref == booking.ref).first()
    if existing:
        # generate new ref with timestamp + random
        booking.ref = f"GRAND-{int(time.time())}-{booking.guest[:4].upper()}"
        # Pastikan tidak duplicate lagi (loop sederhana)
        while db.query(models.Booking).filter(models.Booking.ref == booking.ref).first():
            booking.ref = f"GRAND-{int(time.time())}-{booking.guest[:4].upper()}{int(time.time()*1000)%1000}"

    db_booking = models.Booking(
        ref=booking.ref,
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
        status=booking.status
    )
    db.add(db_booking)
    db.commit()
    db.refresh(db_booking)
    return db_booking

@router.get("/", response_model=list[schemas.BookingOut])
@router.get("", response_model=list[schemas.BookingOut])
def get_bookings(
    email: str,
    db: Session = Depends(get_db),
    current_user = Depends(auth.get_current_user)
):
    if current_user.email != email:
        raise HTTPException(status_code=403, detail="Not authorized")
    bookings = db.query(models.Booking).filter(models.Booking.email == email).all()
    return bookings
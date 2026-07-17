from pydantic import BaseModel, EmailStr
from typing import List, Optional
from datetime import datetime  # ← tambahkan import ini

# Auth
class UserRegister(BaseModel):
    name: str
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserOut(BaseModel):
    name: str
    email: str

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserOut

# Rooms
class RoomBase(BaseModel):
    id: str
    name: str
    price: float
    image: str
    description: str
    features: List[str]

class RoomOut(RoomBase):
    pass

# Bookings
class BookingCreate(BaseModel):
    ref: str
    guest: str
    email: EmailStr
    room: str
    room_id: str
    checkin: str
    checkout: str
    guests: int
    nights: int
    total: float
    special: Optional[str] = None
    card_last4: str
    status: str = "Confirmed"

class BookingOut(BaseModel):
    id: int
    ref: str
    guest: str
    email: str
    room: str
    room_id: str
    checkin: str
    checkout: str
    guests: int
    nights: int
    total: float
    special: Optional[str]
    card_last4: str
    status: str
    created_at: datetime  # ← ubah dari str menjadi datetime
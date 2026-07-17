import json
from sqlalchemy.orm import Session
from . import models
from .database import engine, SessionLocal

ROOMS_DATA = [
    {
        "id": "deluxe",
        "name": "Deluxe Skyline",
        "price": 220,
        "image": "https://images.pexels.com/photos/258154/pexels-photo-258154.jpeg?auto=compress&cs=tinysrgb&w=600",
        "description": "Floor-to-ceiling windows, king bed, marble bathroom, and a private balcony.",
        "features": ["King Bed", "City View", "Marble Bath", "Balcony"]
    },
    {
        "id": "executive",
        "name": "Executive Suite",
        "price": 380,
        "image": "https://images.pexels.com/photos/271618/pexels-photo-271618.jpeg?auto=compress&cs=tinysrgb&w=600",
        "description": "Spacious living area, separate bedroom, and a private terrace with skyline views.",
        "features": ["King Bed", "Living Area", "Terrace", "Skyline View"]
    },
    {
        "id": "penthouse",
        "name": "Penthouse Collection",
        "price": 590,
        "image": "https://images.pexels.com/photos/279746/pexels-photo-279746.jpeg?auto=compress&cs=tinysrgb&w=600",
        "description": "Top-floor luxury with panoramic views, private terrace, and dedicated butler service.",
        "features": ["Panoramic View", "Private Terrace", "Butler Service", "King Bed"]
    }
]

def seed_rooms(db: Session):
    for room_data in ROOMS_DATA:
        existing = db.query(models.Room).filter(models.Room.id == room_data["id"]).first()
        if not existing:
            room = models.Room(
                id=room_data["id"],
                name=room_data["name"],
                price=room_data["price"],
                image=room_data["image"],
                description=room_data["description"],
                features=json.dumps(room_data["features"])
            )
            db.add(room)
    db.commit()
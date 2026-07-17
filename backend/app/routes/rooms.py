import json
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from .. import models, schemas
from ..database import get_db

router = APIRouter(prefix="/api/rooms", tags=["rooms"])

@router.get("/", response_model=list[schemas.RoomOut])
def get_rooms(db: Session = Depends(get_db)):
    rooms = db.query(models.Room).all()
    result = []
    for r in rooms:
        result.append({
            "id": r.id,
            "name": r.name,
            "price": r.price,
            "image": r.image,
            "description": r.description,
            "features": json.loads(r.features) if r.features else []
        })
    return result

@router.get("/{room_id}", response_model=schemas.RoomOut)
def get_room(room_id: str, db: Session = Depends(get_db)):
    r = db.query(models.Room).filter(models.Room.id == room_id).first()
    if not r:
        return None
    return {
        "id": r.id,
        "name": r.name,
        "price": r.price,
        "image": r.image,
        "description": r.description,
        "features": json.loads(r.features) if r.features else []
    }
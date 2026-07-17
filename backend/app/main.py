from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import engine, Base, SessionLocal
from .seed import seed_rooms
from .routes import auth, rooms, bookings

app = FastAPI(title="The Grand Jakarta API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create tables
Base.metadata.create_all(bind=engine)

# Seed rooms
with SessionLocal() as db:
    seed_rooms(db)

# Routes
app.include_router(auth.router)
app.include_router(rooms.router)
app.include_router(bookings.router)

@app.get("/")
def root():
    return {"message": "The Grand Jakarta API", "status": "running"}

@app.get("/health")
def health():
    return {"status": "ok"}
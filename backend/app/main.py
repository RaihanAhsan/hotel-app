from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import engine, Base, SessionLocal
from .seed import seed_rooms
from .routes import auth, rooms, bookings
from fastapi import FastAPI
from app.routes import bookings, webhooks

app = FastAPI(title="The Grand Jakarta API", version="1.0.0")

# CORS - izinkan semua method dan header
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:5174",
        "http://127.0.0.1:5174",
    ],
    allow_credentials=True,
    allow_methods=["*"],          # Izinkan semua method (GET, POST, OPTIONS, dll)
    allow_headers=["*"],
)

# Buat tabel database
Base.metadata.create_all(bind=engine)

# Seed data kamar (jika belum ada)
with SessionLocal() as db:
    seed_rooms(db)

# Daftarkan router
app.include_router(auth.router)
app.include_router(rooms.router)
app.include_router(bookings.router)

@app.get("/")
def root():
    return {"message": "The Grand Jakarta API", "status": "running"}

@app.get("/health")
def health():
    return {"status": "ok"}

app = FastAPI(title="Book Hotel API")

# Daftarkan Router yang sudah dibuat
app.include_router(bookings.router, prefix="/api/bookings", tags=["Bookings"])
app.include_router(webhooks.router, prefix="/webhooks", tags=["Webhooks"])

@app.get("/")
def root():
    return {"message": "Backend FastAPI Hotel berjalan dengan baik!"}
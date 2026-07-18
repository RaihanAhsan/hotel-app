import os
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 1440))
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./grand_jakarta.db")

# Xendit Configuration
XENDIT_API_KEY = os.getenv("XENDIT_API_KEY", "")
XENDIT_WEBHOOK_URL = os.getenv("XENDIT_WEBHOOK_URL", "")
XENDIT_WEBHOOK_TOKEN = os.getenv("XENDIT_WEBHOOK_TOKEN", "")
XENDIT_API_URL = "https://api.xendit.co"  # Sandbox/Test menggunakan URL yang sama[reference:8]
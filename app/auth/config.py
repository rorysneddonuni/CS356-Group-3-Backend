import os

from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv("BACKEND_API_SECRET", "super-secret-key")  # fallback for dev
ALGORITHM = os.getenv("ALGORITHM", "HS256")
RESET_PASSWORD_SECRET_KEY = os.getenv("BACKEND_API_RESET_SECRET", "super-secret-key")
RESET_TOKEN_EXPIRE_MINUTES = os.getenv("TOKEN_RESET_EXPIRY", 15)


ROLE_HIERARCHY = {
    "user": 1,
    "admin": 2,
    "super_admin": 3
}
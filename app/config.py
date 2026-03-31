import os
from datetime import timedelta
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()
BASE_DIR = Path(__file__).resolve().parent.parent


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "hms-secret-key-change-in-production")

    MYSQL_HOST = os.getenv("MYSQL_HOST", "localhost")
    MYSQL_PORT = int(os.getenv("MYSQL_PORT", "3306"))
    MYSQL_DB = os.getenv("MYSQL_DB", "hotel_db")
    MYSQL_USER = os.getenv("MYSQL_USER", "root")
    MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD", "")

    SQLALCHEMY_DATABASE_URI = (
        f"mysql+mysqlconnector://{MYSQL_USER}:{MYSQL_PASSWORD}"
        f"@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DB}?charset=utf8mb4"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        "pool_pre_ping": True,
        "pool_size": 10,
        "max_overflow": 20,
    }

    UPLOAD_FOLDER = BASE_DIR / "app" / "static" / "images"
    AVATARS_FOLDER = UPLOAD_FOLDER / "avatars"
    ROOMS_FOLDER = UPLOAD_FOLDER / "rooms"
    ROOM_TYPES_FOLDER = UPLOAD_FOLDER / "room_types"
    DEFAULT_FOLDER = UPLOAD_FOLDER / "default"
    MAX_CONTENT_LENGTH = 5 * 1024 * 1024
    ALLOWED_EXTENSIONS = {"jpg", "jpeg", "png", "webp"}
    MAX_ROOM_IMAGES = 5

    PER_PAGE = 20

    DEFAULT_TAX_RATE = float(os.getenv("DEFAULT_TAX_RATE", "10.0"))

    REMEMBER_COOKIE_DURATION = timedelta(days=7)
    REMEMBER_COOKIE_REFRESH_EACH_REQUEST = True
    SESSION_COOKIE_SAMESITE = "Lax"

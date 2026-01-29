"""
TeamTrack – Development settings.
"""
from .base import *

DEBUG = True
ALLOWED_HOSTS = ["localhost", "127.0.0.1", "*"]

# Optional: SQLite for local dev if DB_* not set
import os
if os.getenv("DB_ENGINE", "").lower() not in ("django.db.backends.mysql", "mysql"):
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }

CORS_ALLOW_ALL_ORIGINS = True

"""
TeamTrack – Production settings.
Do not enable DEBUG or allow * in ALLOWED_HOSTS.
"""
import os
from .base import *

DEBUG = False
ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "").split(",")
if not any(ALLOWED_HOSTS):
    ALLOWED_HOSTS = ["localhost"]

# Security
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = "DENY"
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True

# CORS: use explicit origins from env
CORS_ALLOW_ALL_ORIGINS = False

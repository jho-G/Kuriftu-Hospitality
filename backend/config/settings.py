"""Django settings for hospitality API — environment-driven for local dev and Render."""

from __future__ import annotations

import os
from pathlib import Path

import dj_database_url
from django.core.exceptions import ImproperlyConfigured

BASE_DIR = Path(__file__).resolve().parent.parent

# Render sets RENDER=true; do not load .env files on the platform (secrets come from the dashboard).
_ON_RENDER = os.environ.get("RENDER", "").strip().lower() == "true"

if not _ON_RENDER:
    try:
        from dotenv import load_dotenv

        load_dotenv(BASE_DIR.parent / ".env")
        load_dotenv(BASE_DIR / ".env", override=True)
    except ImportError:
        pass

# Blank DATABASE_URL in .env would make dj-database-url parse an empty string — treat as unset.
if "DATABASE_URL" in os.environ and not (os.environ.get("DATABASE_URL") or "").strip():
    del os.environ["DATABASE_URL"]

# --- Core (requirement: DEBUG False by default; dev-only secret fallback) ---
DEBUG = os.environ.get("DEBUG", "False") == "True"

SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY", "unsafe-dev-key")

if _ON_RENDER:
    if not (os.environ.get("DJANGO_SECRET_KEY") or "").strip():
        raise ImproperlyConfigured(
            "DJANGO_SECRET_KEY must be set in the Render environment (Dashboard → Environment)."
        )
    if SECRET_KEY == "unsafe-dev-key":
        raise ImproperlyConfigured("DJANGO_SECRET_KEY must not be left as the development default on Render.")
    if not (os.environ.get("DATABASE_URL") or "").strip():
        raise ImproperlyConfigured(
            "DATABASE_URL must be set on Render (link your PostgreSQL service’s internal URL)."
        )

ALLOWED_HOSTS = [
    h.strip()
    for h in os.environ.get("ALLOWED_HOSTS", "*").split(",")
    if h.strip()
] or ["*"]

_csrf_default = "http://127.0.0.1:8000,http://localhost:8000"
CSRF_TRUSTED_ORIGINS = [
    x.strip()
    for x in os.environ.get("CSRF_TRUSTED_ORIGINS", _csrf_default).split(",")
    if x.strip()
]

_sqlite_fallback = f"sqlite:///{(BASE_DIR / 'db.sqlite3').as_posix()}"
DATABASES = {
    "default": dj_database_url.config(
        default=_sqlite_fallback,
        conn_max_age=600,
    ),
}

# Sensitive / optional integrations (read from environment only; no hardcoded secrets)
OPENROUTER_API_KEY = (os.environ.get("OPENROUTER_API_KEY") or "").strip() or None
OPENAI_API_KEY = (os.environ.get("OPENAI_API_KEY") or "").strip() or None
GEMINI_API_KEY = (os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY") or "").strip() or None

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "corsheaders",
    "users",
    "rooms",
    "bookings",
    "chat",
    "feedback",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

STATIC_URL = "static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"

MEDIA_URL = "media/"
MEDIA_ROOT = BASE_DIR / "media"

VIRTUAL_ROOM_FALLBACK_MODEL_URL = (os.environ.get("VIRTUAL_ROOM_FALLBACK_MODEL_URL") or "").strip()

STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedStaticFilesStorage",
    },
}

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

AUTH_USER_MODEL = "users.User"

LOGIN_URL = "login"
LOGIN_REDIRECT_URL = "/accounts/dashboard/"
LOGOUT_REDIRECT_URL = "/"

REST_FRAMEWORK = {
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticatedOrReadOnly",
    ],
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.SessionAuthentication",
        "rest_framework.authentication.BasicAuthentication",
    ],
}

_cors = os.environ.get(
    "CORS_ALLOWED_ORIGINS",
    "http://localhost:5173,http://127.0.0.1:5173",
)
CORS_ALLOWED_ORIGINS = [x.strip() for x in _cors.split(",") if x.strip()]

if not DEBUG and _ON_RENDER:
    SECURE_SSL_REDIRECT = os.environ.get("SECURE_SSL_REDIRECT", "True").strip().lower() in (
        "1",
        "true",
        "yes",
        "on",
    )
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    X_FRAME_OPTIONS = "DENY"


import os
from django.contrib.auth import get_user_model

User = get_user_model()

def create_admin():
    username = os.environ.get("ADMIN_USERNAME")
    email = os.environ.get("ADMIN_EMAIL")
    password = os.environ.get("ADMIN_PASSWORD")

    if username and password:
        if not User.objects.filter(username=username).exists():
            User.objects.create_superuser(username, email, password)

try:
    create_admin()
except Exception as e:
    print("Admin creation skipped:", e)
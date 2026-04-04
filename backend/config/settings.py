"""Django settings for hospitality API (local + Render)."""

import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

try:
    from dotenv import load_dotenv

    load_dotenv(BASE_DIR.parent / ".env")
    load_dotenv(BASE_DIR / ".env", override=True)
except ImportError:
    pass


def _env_bool(key: str, default: str = "False") -> bool:
    return os.environ.get(key, default).strip().lower() in ("1", "true", "yes", "on")


def _env_list(key: str, default: str) -> list[str]:
    return [x.strip() for x in os.environ.get(key, default).split(",") if x.strip()]


# Django requires SECRET_KEY non-empty. Empty DJANGO_SECRET_KEY= in .env would otherwise win over defaults.
_secret = (os.environ.get("DJANGO_SECRET_KEY") or os.environ.get("SECRET_KEY") or "").strip()
SECRET_KEY = _secret or "django-insecure-dev-only-set-django-secret-key-in-env-for-production"

DEBUG = _env_bool("DEBUG", "True")

_default_hosts = "localhost,127.0.0.1,[::1],testserver,.onrender.com"
ALLOWED_HOSTS: list[str] = _env_list("ALLOWED_HOSTS", _default_hosts)

_csrf_default = "http://127.0.0.1:8000,http://localhost:8000"
CSRF_TRUSTED_ORIGINS: list[str] = _env_list("CSRF_TRUSTED_ORIGINS", _csrf_default)

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

# PostgreSQL on Render via DATABASE_URL; SQLite when unset or empty
_database_url = os.environ.get("DATABASE_URL", "").strip()
try:
    import dj_database_url

    if _database_url:
        DATABASES = {
            "default": dj_database_url.parse(_database_url, conn_max_age=600),
        }
    else:
        DATABASES = {
            "default": {
                "ENGINE": "django.db.backends.sqlite3",
                "NAME": BASE_DIR / "db.sqlite3",
            }
        }
except ImportError:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }

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

# Optional HTTPS GLB/GLTF URL when a RoomVirtualTwin has no valid model_url (dev/demo only).
# Per-room URLs are always read from RoomVirtualTwin.model_url in the database.
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

# Production hardening on Render (they set RENDER=true)
if not DEBUG and os.environ.get("RENDER", "").lower() == "true":
    SECURE_SSL_REDIRECT = _env_bool("SECURE_SSL_REDIRECT", "True")
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    X_FRAME_OPTIONS = "DENY"

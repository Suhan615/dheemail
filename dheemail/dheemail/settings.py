import os
import shutil
import tempfile
from importlib.util import find_spec
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
IS_VERCEL = bool(os.environ.get("VERCEL") or os.environ.get("VERCEL_ENV"))
RUNTIME_DIR = Path(tempfile.gettempdir())
HAS_WHITENOISE = find_spec("whitenoise") is not None

SECRET_KEY = "django-insecure-change-this-key-before-production"
DEBUG = True
ALLOWED_HOSTS = ["*"]

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "mailapp",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

if HAS_WHITENOISE:
    MIDDLEWARE.insert(1, "whitenoise.middleware.WhiteNoiseMiddleware")

ROOT_URLCONF = "dheemail.urls"

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
                "mailapp.context_processors.mail_sidebar",
            ],
        },
    },
]

WSGI_APPLICATION = "dheemail.wsgi.application"

if IS_VERCEL:
    SQLITE_DB_PATH = RUNTIME_DIR / "db.sqlite3"
    bundled_db_path = BASE_DIR / "db.sqlite3"
    if not SQLITE_DB_PATH.exists() and bundled_db_path.exists():
        shutil.copyfile(bundled_db_path, SQLITE_DB_PATH)
else:
    SQLITE_DB_PATH = BASE_DIR / "db.sqlite3"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": SQLITE_DB_PATH,
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

LANGUAGE_CODE = "en-us"
TIME_ZONE = "Asia/Kolkata"
USE_I18N = True
USE_TZ = True

STATIC_URL = "/static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"
STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": (
            "whitenoise.storage.CompressedStaticFilesStorage"
            if HAS_WHITENOISE
            else "django.contrib.staticfiles.storage.StaticFilesStorage"
        ),
    },
}
if HAS_WHITENOISE:
    WHITENOISE_USE_FINDERS = True
MEDIA_URL = "/media/"
MEDIA_ROOT = RUNTIME_DIR / "media" if IS_VERCEL else BASE_DIR / "media"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
AUTH_USER_MODEL = "mailapp.User"

LOGIN_URL = "login"
LOGIN_REDIRECT_URL = "dashboard"
LOGOUT_REDIRECT_URL = "login"

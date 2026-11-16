"""
Django settings for mystery_quest_project.

Local development uses SQLite by default. Set TURSO_DB_URL and
TURSO_AUTH_TOKEN to use the remote Turso/libSQL database in deployment.
"""

from pathlib import Path
import os
from django.core.exceptions import ImproperlyConfigured

BASE_DIR = Path(__file__).resolve().parent.parent


def env_list(name, default=""):
    return [item.strip() for item in os.getenv(name, default).split(",") if item.strip()]


IS_VERCEL = bool(os.getenv("VERCEL"))
DEBUG = os.getenv("DJANGO_DEBUG", "false" if IS_VERCEL else "true").lower() in {
    "1", "true", "yes"
}
SECRET_KEY = os.getenv("DJANGO_SECRET_KEY")
if not SECRET_KEY:
    if not DEBUG:
        raise ImproperlyConfigured(
            "DJANGO_SECRET_KEY must be set when DEBUG is disabled."
        )
    SECRET_KEY = "django-insecure-local-development-only-change-before-deploying"

ALLOWED_HOSTS = env_list(
    "DJANGO_ALLOWED_HOSTS",
    ".vercel.app" if IS_VERCEL else "localhost,127.0.0.1",
)
if os.getenv("VERCEL_URL"):
    ALLOWED_HOSTS.append(os.environ["VERCEL_URL"].split(":")[0])

CSRF_TRUSTED_ORIGINS = env_list("DJANGO_CSRF_TRUSTED_ORIGINS")
if IS_VERCEL:
    CSRF_TRUSTED_ORIGINS.append("https://*.vercel.app")

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "accounts.apps.AccountsConfig",
    "investigation.apps.InvestigationConfig",
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

ROOT_URLCONF = "mystery_quest_project.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "django.template.context_processors.media",
            ],
        },
    },
]

WSGI_APPLICATION = "mystery_quest_project.wsgi.application"

TURSO_DB_URL = os.getenv("TURSO_DB_URL")
TURSO_AUTH_TOKEN = os.getenv("TURSO_AUTH_TOKEN")

if TURSO_DB_URL and TURSO_AUTH_TOKEN:
    DATABASES = {
        "default": {
            "ENGINE": "django_libsql",
            "NAME": TURSO_DB_URL,
            "AUTH_TOKEN": TURSO_AUTH_TOKEN,
            "OPTIONS": {"timeout": 30},
        }
    }
elif TURSO_DB_URL or TURSO_AUTH_TOKEN:
    raise ImproperlyConfigured(
        "Set both TURSO_DB_URL and TURSO_AUTH_TOKEN, or neither for local SQLite."
    )
elif IS_VERCEL:
    raise ImproperlyConfigured(
        "TURSO_DB_URL and TURSO_AUTH_TOKEN are required for Vercel deployment."
    )
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
        "OPTIONS": {"min_length": 8},
    },
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
]

LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

STATIC_URL = "/static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"

# Vercel's filesystem is ephemeral. Configure durable object storage before
# enabling user-uploaded case/suspect/clue images in production.
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

LOGIN_URL = "login"
LOGIN_REDIRECT_URL = "home"
LOGOUT_REDIRECT_URL = "home"

from django.contrib.messages import constants as messages

MESSAGE_TAGS = {
    messages.DEBUG: "secondary",
    messages.INFO: "info",
    messages.SUCCESS: "success",
    messages.WARNING: "warning",
    messages.ERROR: "danger",
}

SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
SESSION_COOKIE_SECURE = not DEBUG
CSRF_COOKIE_SECURE = not DEBUG
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = "DENY"

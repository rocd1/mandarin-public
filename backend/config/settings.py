"""
============================================================
CORE
============================================================
"""

from pathlib import Path

import environ
from corsheaders.defaults import default_headers


# -------------------------------------------------
# BASE DIRECTORY
# -------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent


# -------------------------------------------------
# LOAD .ENV
# -------------------------------------------------

env = environ.Env(
    DEBUG=(bool, False),
)

environ.Env.read_env(BASE_DIR / ".env")


# -------------------------------------------------
# CORE SETTINGS
# -------------------------------------------------


SECRET_KEY = env("SECRET_KEY")

DEBUG = env.bool("DEBUG", default=False)

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

LANGUAGE_CODE = "en-us"


TIME_ZONE = env(
    "TIME_ZONE",
    default="Asia/Singapore",
)


USE_I18N = True

USE_TZ = True




"""
============================================================
APPLICATIONS
============================================================
"""

INSTALLED_APPS = [

    # Django
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    # Third Party
    "rest_framework",
    "corsheaders",
    "csp",

    # Local Apps
    "learning.apps.LearningConfig",

]


"""
============================================================
MIDDLEWARE
============================================================
"""

MIDDLEWARE = [
    #Security
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",

    #CORS
    "corsheaders.middleware.CorsMiddleware",

    #Django
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    #csrf
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",

    #Content Security Policy
    "csp.middleware.CSPMiddleware",

]


ROOT_URLCONF = "config.urls"

WSGI_APPLICATION = "config.wsgi.application"


TEMPLATES = [

    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",

        "DIRS": [],

        "APP_DIRS": True,

        "OPTIONS": {

            "context_processors": [

                "django.template.context_processors.request",

                "django.contrib.auth.context_processors.auth",

                "django.contrib.messages.context_processors.messages",

            ],
        },
    },

]



"""
============================================================
DATABASE
============================================================
"""

DATABASE_URL = env(
    "DATABASE_URL",
    default=f"sqlite:///{BASE_DIR / 'db.sqlite3'}",
)

DATABASES = {
    "default": env.db(
        "DATABASE_URL",
    )
}

DATABASES["default"]["CONN_MAX_AGE"] = 60

if not DEBUG and DATABASES["default"]["ENGINE"] == "django.db.backends.postgresql":

    DATABASES["default"]["OPTIONS"] = {
        "sslmode": "require",
    }




"""
============================================================
AUTHENTICATION
============================================================
"""

AUTHENTICATION_BACKENDS = [

    "django.contrib.auth.backends.ModelBackend",

]


AUTH_PASSWORD_VALIDATORS = [

    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },

    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },

    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },

    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",

        "OPTIONS": {

            "min_length": 12,

        },

    },

]


"""
============================================================
REST FRAMEWORK
============================================================
"""

REST_FRAMEWORK = {

    # Learning endpoints are public by default. Add explicit permissions
    # to individual views if a future feature needs access control.
    "DEFAULT_AUTHENTICATION_CLASSES": (),

    "DEFAULT_PERMISSION_CLASSES": (
        "rest_framework.permissions.AllowAny",
    ),

    "DEFAULT_THROTTLE_CLASSES": [
        "rest_framework.throttling.AnonRateThrottle",
    ],

    "DEFAULT_THROTTLE_RATES": {

        "anon": "100/day",

    },

}

if not DEBUG:

    REST_FRAMEWORK["DEFAULT_RENDERER_CLASSES"] = [

        "rest_framework.renderers.JSONRenderer",

    ]


"""
============================================================
SECURITY
============================================================
"""

ALLOWED_HOSTS = env.list(
    "ALLOWED_HOSTS",
    default=[
        "127.0.0.1",
        "localhost",
    ],
)

CORS_ALLOWED_ORIGINS = env.list(
    "CORS_ALLOWED_ORIGINS",
    default=[
        
        "http://localhost:4200",
    ],
    
)

CORS_ALLOW_CREDENTIALS = False

CSRF_TRUSTED_ORIGINS = CORS_ALLOWED_ORIGINS

CORS_ALLOW_HEADERS = list(default_headers) + [

    "x-csrftoken",

]

SECURE_SSL_REDIRECT = not DEBUG

SECURE_PROXY_SSL_HEADER = (

    "HTTP_X_FORWARDED_PROTO",

    "https",

)

SECURE_HSTS_SECONDS = 31536000 if not DEBUG else 0

SECURE_HSTS_INCLUDE_SUBDOMAINS = not DEBUG

SECURE_HSTS_PRELOAD = not DEBUG

SECURE_CONTENT_TYPE_NOSNIFF = True

SECURE_REFERRER_POLICY = "strict-origin-when-cross-origin"

SECURE_CROSS_ORIGIN_OPENER_POLICY = "same-origin"

X_FRAME_OPTIONS = "DENY"

SESSION_COOKIE_HTTPONLY = True

SESSION_COOKIE_SECURE = not DEBUG

SESSION_COOKIE_SAMESITE = "None" if not DEBUG else "Lax"

SESSION_COOKIE_AGE = 60 * 60 * 24

CSRF_COOKIE_HTTPONLY = True

CSRF_COOKIE_SECURE = not DEBUG

CSRF_COOKIE_SAMESITE = "None" if not DEBUG else "Lax"

CSRF_COOKIE_NAME = "csrftoken"


"""
============================================================
STATIC / MEDIA
============================================================
"""

STATIC_URL = "/static/"

STATIC_ROOT = BASE_DIR / "staticfiles"

STORAGES = {

    "staticfiles": {

        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",

    }

}

MEDIA_URL = "/media/"

MEDIA_ROOT = BASE_DIR / "media"


"""
============================================================
EMAIL
============================================================
"""


EMAIL_BACKEND = env(
    "EMAIL_BACKEND",
    default="django.core.mail.backends.console.EmailBackend",
)

EMAIL_HOST = env(
    "EMAIL_HOST",
    default="smtp.gmail.com",
)

EMAIL_PORT = env.int(
    "EMAIL_PORT",
    default=587,
)

EMAIL_USE_TLS = env.bool(
    "EMAIL_USE_TLS",
    default=True,
)

EMAIL_HOST_USER = env(
    "EMAIL_HOST_USER",
    default="",
)

EMAIL_HOST_PASSWORD = env(
    "EMAIL_HOST_PASSWORD",
    default="",
)

DEFAULT_FROM_EMAIL = env(
    "DEFAULT_FROM_EMAIL",
    default="noreply@example.com",
)





"""
============================================================
LOGGING
============================================================
"""

LOG_DIR = BASE_DIR / "logs"

LOG_DIR.mkdir(
    parents=True,
    exist_ok=True,
)


LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,

    "formatters": {
        "verbose": {
            "format": "[{levelname}] {asctime} {name} {message}",
            "style": "{",
        },
        "simple": {
            "format": "[{levelname}] {message}",
            "style": "{",
        },
    },

    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "simple",
        },

        "security_file": {
            "class": "logging.handlers.RotatingFileHandler",
            "filename": LOG_DIR / "security.log",
            "maxBytes": 10 * 1024 * 1024,
            "backupCount": 5,
            "formatter": "verbose",
            "encoding": "utf-8",
        },

        "django_file": {
            "class": "logging.handlers.RotatingFileHandler",
            "filename": LOG_DIR / "django.log",
            "maxBytes": 10 * 1024 * 1024,
            "backupCount": 5,
            "formatter": "verbose",
            "encoding": "utf-8",
        },
    },


    #root logger helps catch logs from third-party packages
    "root": {
        "handlers": [
            "console",
            "django_file",
        ],
        "level": "DEBUG" if DEBUG else "INFO",
    },

}


# (Keep your existing LOGGING dictionary here unchanged)


"""
============================================================
CONTENT SECURITY POLICY (CSP)
============================================================
"""

if DEBUG:

    connect_src = (

        "'self'",

        "http://localhost:4200",
        

    )

else:

    connect_src = (

        "'self'",

    )

CONTENT_SECURITY_POLICY = {

    "DIRECTIVES": {

        "default-src": ("'self'",),

        "script-src": ("'self'",),

        "style-src": ("'self'",),

        "img-src": ("'self'", "data:", "blob:"),

        "font-src": ("'self'", "data:"),

        "connect-src": connect_src,

        "object-src": ("'none'",),

        "base-uri": ("'self'",),

        "form-action": ("'self'",),

        "frame-ancestors": ("'none'",),

        "media-src": ("'self'",),

        "manifest-src": ("'self'",),

        "worker-src": ("'self'",),

        "frame-src": ("'none'",),

    }

}


"""
============================================================
OPTIONAL SETTINGS
============================================================
"""

LOGIN_URL = "/login/"

LOGIN_REDIRECT_URL = "/"

LOGOUT_REDIRECT_URL = "/"



# ============================================================
# PRODUCTION ENVIRONMENT VALIDATION
# ============================================================

if not DEBUG:

    REQUIRED_ENV_VARS = [

        "SECRET_KEY",

        "DATABASE_URL",

    ]

    missing = [

        var

        for var in REQUIRED_ENV_VARS

        if not env(var, default=None)

    ]

    if missing:

        raise RuntimeError(
            f"Missing required environment variables: {', '.join(missing)}"
        )




#future for use of websockets
ASGI_APPLICATION = "config.asgi.application"








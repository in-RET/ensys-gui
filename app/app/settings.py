"""
Django settings for EPA project.

Generated by 'django-admin startproject' using Django 3.0.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import ast
import os

from django.contrib.messages import constants as messages

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = ast.literal_eval(os.getenv("DJANGO_DEBUG", "False"))

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
]

# Static files (CSS, JavaScript, Images)
STATICFILES_DIRS = (os.path.join(BASE_DIR, "static"),)
STATIC_URL = "static/"
STATIC_ROOT = os.path.join(BASE_DIR, "cdn_static_root")
print("STATIC ROOT:", STATIC_ROOT)

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv(
    "EPA_SECRET_KEY", "v@p9^=@lc3#1u_xtx*^xhrv0l3li1(+8ik^k@g-_bzmexb0$7n"
)

ALLOWED_HOSTS = ["*"]

CSRF_TRUSTED_ORIGINS = [
    "http://localhost:9004",
    "http://127.0.0.1:9004",
    "http://surak.hs-nordhausen.de:9004",
    "https://ensys.hs-nordhausen.de",
    "http://iae.hs-nordhausen.de",
]

# Application definition
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.forms",
    "users.apps.UsersConfig",
    "projects.apps.ProjectsConfig",
    "dashboard.apps.DashboardConfig",
    # 3rd Party
    "crispy_forms",
    "crispy_bootstrap4",
    "django_q",
    "django_plotly_dash.apps.DjangoPlotlyDashConfig",
    "bootstrap_datepicker_plus",
]

if DEBUG is True:
    INSTALLED_APPS.append("sass_processor")
    STATICFILES_FINDERS.append("sass_processor.finders.CssFinder")
    SASS_PROCESSOR_ROOT = STATIC_ROOT
    SASS_PRECISION = 8

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django_plotly_dash.middleware.BaseMiddleware",
]

FILE_UPLOAD_HANDLERS = [
    "django.core.files.uploadhandler.MemoryFileUploadHandler",
    "django.core.files.uploadhandler.TemporaryFileUploadHandler",
]

ROOT_URLCONF = "app.urls"

FORM_RENDERER = "django.forms.renderers.TemplatesSetting"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "app.context_processors.debug",
            ]
        },
    }
]

WSGI_APPLICATION = "app.wsgi.application"

STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
    },
}

# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases
# By default the database is postgres, if you want to use mysql make sure you pip install the mysql requirement file

DATABASES = {
    "default": {
        "ENGINE": os.environ.get("SQL_ENGINE", "django.db.backends.sqlite3"),
        "NAME": os.environ.get("SQL_DATABASE", os.path.join(BASE_DIR, "db.sqlite3")),
        "USER": os.environ.get("SQL_USER"),
        "PASSWORD": os.environ.get("SQL_PASSWORD"),
        "HOST": os.environ.get("SQL_HOST"),
        "PORT": os.environ.get("SQL_PORT"),
    }
}

DEFAULT_AUTO_FIELD = "django.db.models.AutoField"

# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = "en"
LOCALE_PATHS = (os.path.join(BASE_DIR, "locale"),)
LANGUAGES = [("en", "English")]  # ("de", "German"),
TIME_ZONE = "Europe/Copenhagen"
USE_I18N = True
USE_L10N = True
USE_TZ = False

BOOTSTRAP_DATEPICKER_PLUS = {
    "options": {
        "locale": "de",
        "showClose": True,
        "showTodayButton": True,
    },
    "variant_options": {
        "date": {
            "format": "DD-MM",
        },
    },
}

# Other configs

AUTH_USER_MODEL = "users.CustomUser"

LOGIN_URL = "login"
LOGIN_REDIRECT_URL = "project_search"
LOGOUT_REDIRECT_URL = "home"

CRISPY_TEMPLATE_PACK = "bootstrap4"

# Email Backend Service
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = os.getenv("EMAIL_HOST_IP")
EMAIL_PORT = 587
EMAIL_USE_TLS = True

# Use environment variables for sensitive information
EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD")
DEFAULT_FROM_EMAIL = os.getenv("EMAIL_SENDER")

# Email addresses to which feedback emails will be sent
RECIPIENTS = os.getenv("RECIPIENTS", "ensys@hs-nordhausen.de,andreas.lubojanski@hs-nordhausen.de").split(",")
EMAIL_SUBJECT_PREFIX = os.getenv("EMAIL_SUBJECT_PREFIX", "[EnSys] ")

MESSAGE_TAGS = {
    messages.DEBUG: "alert-info",
    messages.INFO: "alert-info",
    messages.SUCCESS: "alert-success",
    messages.WARNING: "alert-warning",
    messages.ERROR: "alert-danger",
}

USE_PROXY = ast.literal_eval(os.getenv("USE_PROXY", "True"))
PROXY_ADDRESS_LINK = os.getenv("PROXY_ADDRESS", "http://proxy:port")
PROXY_CONFIG = (
    ({"http://": PROXY_ADDRESS_LINK, "https://": PROXY_ADDRESS_LINK})
    if USE_PROXY
    else ({})
)

INRETENSYS_API_HOST = "http://api:8001"
INRETENSYS_POST_URL = f"{INRETENSYS_API_HOST}/uploadJson"
INRETENSYS_CHECK_URL = f"{INRETENSYS_API_HOST}/check/"
INRETENSYS_LP_FILE_URL = f"{INRETENSYS_API_HOST}/getLpFile/"

OEP_URL = "https://openenergy-platform.org/api/v0/schema/model_draft/tables/"

# Allow iframes to show in page
X_FRAME_OPTIONS = "SAMEORIGIN"

# DJANGO-Q CONFIGURATION
# source: https://django-q.readthedocs.io/en/latest/configure.html
Q_CLUSTER = {
    "name": "django_q_orm",
    "workers": 4,
    "timeout": 90,
    "retry": 120,
    "queue_limit": 50,
    "orm": "default",
}

import sys

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "dtlnm": {
            "format": "%(asctime)s - %(levelname)8s - %(name)s - %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S",
        }
    },
    "handlers": {
        "info_file": {
            "level": "INFO",
            "class": "logging.FileHandler",
            "filename": "django_epa_info.log",
            "formatter": "dtlnm",
        },
        "warnings_file": {
            "level": "WARNING",
            "class": "logging.FileHandler",
            "filename": "django_epa_warning.log",
            "formatter": "dtlnm",
        },
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "stream": sys.stdout,
        },
    },
    "loggers": {
        "": {
            "handlers": ["info_file", "warnings_file", "console"],
            "level": "DEBUG",
            "propagate": True,
        },
        "asyncio": {"level": "WARNING"},
    },
}

"""
Django settings for config project.

Generated by 'django-admin startproject' using Django 5.1.1.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""

import os
from pathlib import Path

from django.core.management.commands.runserver import Command as runserver
from dotenv import load_dotenv
import sys
from datetime import datetime
from pathlib import Path
from loguru import logger
import logging  # Add this import

runserver.default_port = "5000"

# Load environment variables from .env file
load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Remove the default handler
logger.remove()

# Configure Loguru logger
logger_format = (
    "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
    "<level>{level: <8}</level> | "
    "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - "
    "<level>{message}</level>"
)

# SECURITY WARNING: don't run with debug turned on in production!
ENVIRONMENT = os.getenv('DJANGO_ENVIRONMENT', 'Development').capitalize()
DEBUG = ENVIRONMENT != 'Production'

LOGGING_LEVEL = os.getenv("DJANGO_LOGGING", "INFO")

# Loguru configuration
logger.remove()  # Remove default handler

log_dir = BASE_DIR / "logs"
log_dir.mkdir(exist_ok=True)

now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

logger.configure(
    handlers=[
        {
            "sink": sys.stderr,
            "format": "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
            "level": "DEBUG" if DEBUG else "INFO",
            "colorize": True,
        },
        {
            "sink": log_dir / f"Django-{now}.log",
            "format": "{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
            "rotation": "10 MB",
            "compression": "zip",
            "level": "DEBUG" if DEBUG else "INFO",
            "enqueue": True,
        },
    ]
)


# Intercept Django logging
class InterceptHandler(logging.Handler):
    def emit(self, record):
        # Get corresponding Loguru level if it exists
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        # Find caller from where originated the logged message
        frame, depth = sys._getframe(6), 6
        while frame and frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back
            depth += 1

        logger.opt(depth=depth, exception=record.exc_info).log(level, record.getMessage())


# Django logging configuration
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "loguru": {
            "class": "config.settings.InterceptHandler",
        },
    },
    "root": {
        "handlers": ["loguru"],
        "level": "INFO",
    },
    "loggers": {
        "django": {
            "handlers": ["loguru"],
            "level": "INFO",
            "propagate": False,
        },
        "django.server": {
            "handlers": ["loguru"],
            "level": "INFO",
            "propagate": False,
        },
        "django_q": {
            "handlers": ["loguru"],
            "level": "INFO",
            "propagate": False,
        },
    },
}

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv(
    'DJANGO_SECRET_KEY',
    'django-insecure-h)o$-2c^l)rh_)p#d-7w+rqi2a#$2+zhvwkra@21!mzr4!%97e')


# Check if running in Docker
IN_DOCKER = os.environ.get('DOCKER_CONTAINER', False)


ALLOWED_HOSTS = os.getenv('DJANGO_ALLOWED_HOSTS', '').split(',')

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'core',
    'rest_framework',
    'drf_yasg',
    'django_q',
    'corsheaders',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware'
]

CORS_ALLOWED_ORIGINS = os.getenv('CORS_ALLOWED_ORIGINS', '').split(',')

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
}

AUTH_USER_MODEL = 'auth.User'

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

if ENVIRONMENT == 'Production':
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': os.getenv('DB_NAME'),
            'USER': os.getenv('DB_USER'),
            'PASSWORD': os.getenv('DB_PASSWORD'),
            'HOST': os.getenv('DB_HOST'),
            'PORT': os.getenv('DB_PORT'),
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / f'{ENVIRONMENT}_db.sqlite3',
        }
    }
    

# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME':
        'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME':
        'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME':
        'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME':
        'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Configure Django Q in settings.py
Q_CLUSTER = {
    'name': os.getenv('Q_CLUSTER_NAME', 'myproject'),
    'workers': int(os.getenv('Q_CLUSTER_WORKERS', 4)),
    'recycle': int(os.getenv('Q_CLUSTER_RECYCLE', 500)),
    'timeout': int(os.getenv('Q_CLUSTER_TIMEOUT', 60)),
    'compress': os.getenv('Q_CLUSTER_COMPRESS', 'True') == 'True',
    'save_limit': int(os.getenv('Q_CLUSTER_SAVE_LIMIT', 250)),
    'queue_limit': int(os.getenv('Q_CLUSTER_QUEUE_LIMIT', 500)),
    'cpu_affinity': int(os.getenv('Q_CLUSTER_CPU_AFFINITY', 1)),
    'label': os.getenv('Q_CLUSTER_LABEL', 'Django Q2'),
    'redis': {
        'host': 'redis' if IN_DOCKER else 'localhost',
        'port': int(os.getenv('Q_CLUSTER_REDIS_PORT', 6379)),
        'db': int(os.getenv('Q_CLUSTER_REDIS_DB', 0)),
    }
}

"""
Django settings for electronicSignature project.

Generated by 'django-admin startproject' using Django 3.1.13.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""

import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
from django.contrib import messages
from decouple import config

BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG', cast=bool)

ALLOWED_HOSTS = ['*']

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'cirrushieldapi',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'main',
    'widget_tweaks',
    'signature',
    'django.contrib.sites',
    'corsheaders',
    'pdfDossier',
]
SITE_ID = config('SITE_ID')
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'csp.middleware.CSPMiddleware',

]

ROOT_URLCONF = 'electronicSignature.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / "templates"],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'main.context_processors.group_processor',
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',

            ],
        },
    },
]

WSGI_APPLICATION = 'electronicSignature.wsgi.application'

# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

STATIC_ROOT = os.path.join(BASE_DIR, 'static')

STATIC_URL = "/static/"

# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

LOGIN_URL = "login"
LOGIN_REDIRECT_URL = "main:home"
DEFAULT_FROM_EMAIL = 'millforma.signature@gmail.com'

MESSAGE_TAGS = {
    messages.DEBUG: 'alert-info',
    messages.INFO: 'alert-info',
    messages.SUCCESS: 'alert-success',
    messages.WARNING: 'alert-warning',
    messages.ERROR: 'alert-danger',
}
API_USER = config('API_USER')
API_PSSWD = config('API_PSSWD')
UPLOAD_FOLDER_DOCUMENTS = os.path.join(BASE_DIR, 'static/assets/emargements')
UPLOAD_FOLDER_CHATS_DOCUMENT = "static"
UPLOAD_FOLDER_IMAGES = "static"
THUMBNAIL_DIMENSIONS = (250, 250)
THUMBNAIL_SUBDIRECTORY = "static/thumbnail"
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
PHONE_ACCEPTED_FORMAT = "FR"
PHONENUMBER_DEFAULT_REGION = "US"
LANGUAGES = (
    ('en', 'English'),
    ('fr', 'French'),
)

LOCALE_PATHS = (
    os.path.join(BASE_DIR, 'locale/'),
)
EMAIL_SENDER = config('EMAIL_SENDER')
EMAIL_USE_TLS = config('EMAIL_USE_TLS')
EMAIL_HOST = config('EMAIL_HOST')
EMAIL_HOST_USER = config('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')
EMAIL_PORT = config('EMAIL_PORT')

CORS_ALLOWED_ORIGINS = [
    "http://millforma-admin.fr/",
    "https://millforma-admin.fr/",
    "http://localhost:8080",
]
CSP_DEFAULT_SRC = ("'none'",)
CSP_STYLE_SRC = ("'self'", 'unsafe-inline', 'fonts.googleapis.com', 'cdn.datatables.net', 'stackpath.bootstrapcdn.com',)
CSP_SCRIPT_SRC = (
    "'self'", 'unsafe-inline', 'unsafe-eval',)
CSP_FONT_SRC = ("'self'", 'fonts.gstatic.com', 'fonts.googleapis.com',)
CSP_IMG_SRC = ("'self'",)
CSP_CONNECT_SRC = ("'self'", 'millforma-admin.fr',)
CSP_FRAME_SRC = ("'self'", 'documentcloud.adobe.com', 'unsafe-inline',)
CSP_INCLUDE_NONCE_IN = ("script-src", "font-src", "style-src", "connect-src", "frame-src")

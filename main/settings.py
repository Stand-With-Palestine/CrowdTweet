"""
Django settings for main project.

Generated by 'django-admin startproject' using Django 4.2.6.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

import os
import sys
from pathlib import Path
import tweepy
from dotenv import load_dotenv

from apps.my_apps import MY_APPS

load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
TEMPLATE_DIR = os.path.join(BASE_DIR, 'apps/templates')

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('SECRET_KEY', 'Al@A!!')
ENVIRONMENT = os.getenv('ENVIRONMENT', '')
# SECURITY WARNING: don't run with debug turned on in production!
if os.getenv('ENVIRONMENT') != "prod":
    DEBUG=True

ALLOWED_HOSTS = ['3.249.31.235', 'palmycause.info', 'localhost', 'standwithpalestine.info',
                 'ECS-LB-1114824834.eu-west-1.elb.amazonaws.com', '34.245.60.84']
CSRF_TRUSTED_ORIGINS = ['https://standwithpalestine.info']

TWITTER_API_KEY = os.getenv('TWITTER_API_KEY', 'p8itN5RqnLoMa37ttJ5ap0HV6')
TWITTER_API_SECRET_KEY = os.getenv('TWITTER_API_SECRET_KEY', 'IyyOLUz4y9wFwtUD8jcnnIjMeRG3CZo9IAppMp9NmFsIf2xGrv')
BEARER_TOKEN = os.getenv('BEARER_TOKEN',
                         "AAAAAAAAAAAAAAAAAAAAAL712AAAAAAAgWN3mJssDsSMVob43hNCoR87RgU%3DHrcabAXd6D3lSCkt98ZJ5vg6D3RfohPnSLfyLJ7XsGe8ka7JL9")

AUTH = tweepy.OAuth1UserHandler(consumer_key=TWITTER_API_KEY, consumer_secret=TWITTER_API_SECRET_KEY)

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # 3rd parties
    'crispy_forms',
    'crispy_bootstrap5',
    'bootstrap5',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
]

# django apps
INSTALLED_APPS += MY_APPS

AUTHENTICATION_BACKENDS = (
    'allauth.account.auth_backends.AuthenticationBackend',
)
AUTHENTICATION_CLASSES = (
    'allauth.account.auth_backends.AuthenticationBackend',
)
# Allauth settings
AUTHENTICATION_METHOD = 'email'  # Change as per your requirements
ACCOUNT_EMAIL_VERIFICATION = 'none'  # Change for email verification

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'allauth.account.middleware.AccountMiddleware',
]

ROOT_URLCONF = 'main.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [TEMPLATE_DIR, ],
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

WSGI_APPLICATION = 'main.wsgi.application'

# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

if os.getenv('ENVIRONMENT'):
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': os.getenv('DB_NAME', ''),
            'USER': os.getenv('DB_USER', ''),
            'PASSWORD': os.getenv('DB_PASS', ''),
            'HOST': os.getenv('DB_HOST', 'localhost'),
            'PORT': os.getenv('DB_PORT', '3306'),
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': 'db.sql',
        }
}


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
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
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'ar'

TIME_ZONE = os.getenv('TIME_ZONE', 'UTC')

USE_I18N = True

USE_TZ = True

LOCALE_PATHS = (
    os.path.join(BASE_DIR, 'apps/locale'),
)

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_ROOT = os.path.join(BASE_DIR, 'apps/static')
STATIC_URL = '/static/'

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'apps/../static'),
)

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"
LOGIN_REDIRECT_URL = os.getenv('LOGIN_REDIRECT_URL', '/')
LOGIN_URL = os.getenv('LOGIN_URL', '/accounts/login/')

# celery settings
BROKER_URL = 'amqp://guest:@localhost/'
BROKER_BACKEND = 'amqp://guest:@localhost/'
if "celeryd" in sys.argv:
    DEBUG = False

"""
Django settings for config project.
"""

from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-@#(5cy2!_c0bu8^jr$c9hx$oq7rtq3j878n7au3_d92%mmn0z$'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# Updated to include your Elastic Beanstalk domain
# settings.py

ALLOWED_HOSTS = [
    'incidentmanagement-env-1.eba-rbgtyr6y.us-east-1.elasticbeanstalk.com'
]

# Updated to include your Elastic Beanstalk origin
CSRF_TRUSTED_ORIGINS = [
    "https://c7d82075a40f4e8ea40538297677bbcf.vfs.cloud9.us-east-1.amazonaws.com",
    "http://incidentmanagement-env.eba-43v235sh.us-east-1.elasticbeanstalk.com"
]

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'accounts',
    'incidents',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Password validation
# FIXED: Added the missing closing brackets and names here
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Static files
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static')
]

# Authentication Settin
AUTH_USER_MODEL = 'accounts.CustomUser'
LOGIN_URL = 'login'
LOGOUT_REDIRECT_URL = 'login'
LOGIN_REDIRECT_URL = 'incidents:incident_list'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
"""
Django settings for django_server project.

Generated by 'django-admin startproject' using Django 3.1.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""

from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve(strict=True).parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '@zl(2zb4ke9#@_38$%gf^wgb%z!6ok*2wb$7x$x5_qm0)pa9*c'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['deal.dirox.dev', 'api.deal.dirox.dev', '127.0.0.1', 'localhost']

# Security setting
SECURE_REFERRER_POLICY = 'origin'
SECURE_CONTENT_TYPE_NOSNIFF = True
CORS_ALLOW_ALL_ORIGINS = False
CORS_ALLOWED_ORIGINS = ['https://deal.dirox.dev', 'https://api.deal.dirox.dev','http://127.0.0.1:8000', 'http://localhost:8080']
SESSION_COOKIE_SAMESITE = None
SESSION_COOKIE_SECURE = False # Should be True when deploy
CORS_ALLOW_CREDENTIALS = True
SESSION_COOKIE_AGE = 60 # cookie timeout in seconds

# Setting Oauth2 clients
AUTHLIB_OAUTH_CLIENTS = {
    'google': {
	    'client_id': '719320147131-pke60fglsm657ghd5ak304o375qh1iol.apps.googleusercontent.com',
	    'client_secret': 'i-6rIsOZiZXEsM4_O1v9OzhC',
        'authorize_url': 'https://accounts.google.com/o/oauth2/v2/auth',
        'access_token_url': 'https://oauth2.googleapis.com/token',
        'authorize_params': {'access_type':'offline'},
        'client_kwargs': {
            'scope': 'https://www.googleapis.com/auth/gmail.metadata \
                      https://www.googleapis.com/auth/drive \
                      https://www.googleapis.com/auth/drive.file \
                      https://www.googleapis.com/auth/spreadsheets \
                      https://www.googleapis.com/auth/presentations',
        }
    },
    'hubspot': {
	    'client_id': 'dcd83b26-1f89-4922-8f2d-69382eb671e2',
	    'client_secret': '233f8a31-de8e-4c2b-af44-b97416f319f1',
        'authorize_url': 'https://app.hubspot.com/oauth/authorize',
        'access_token_url': 'https://api.hubapi.com/oauth/v1/token',
        'client_kwargs': {
            'scope': 'contacts'
        }
    }
}

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'corsheaders',
    'server.deals'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'server.urls'

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

WSGI_APPLICATION = 'server.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'server' / 'database' / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = 'server/static/'

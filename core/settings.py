
from pathlib import Path
import os
from dotenv import load_dotenv
import os
import cloudinary
import cloudinary.uploader
import cloudinary.api
from cloudinary_storage.storage import MediaCloudinaryStorage
from cloudinary_storage.storage import VideoMediaCloudinaryStorage

BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = 'django-insecure-8(#@uu1-h_8nsp&h7n=m#dw8s8-x^+ou8ieg(*=v_=qtvlv^fh'
AUTH_USER_MODEL = 'jobed.UserModel'
DEBUG = True
load_dotenv()
ALLOWED_HOSTS = ["*"]
INSTALLED_APPS = [
    'jazzmin',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'jobed',
    'cloudinary',
    'cloudinary_storage',
    'django.contrib.sites',  
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',    'allauth.socialaccount.providers.github',
    'rest_framework_simplejwt',
    'sslserver',
    'corsheaders',
    'rest_framework_simplejwt.token_blacklist'


]
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SECURE = False  
SITE_ID = 1

# Authentication backends
AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',  # Default auth backend
    'allauth.account.auth_backends.AuthenticationBackend',  # Required for allauth
)

# Define login redirect URLs
LOGIN_REDIRECT_URL = 'https://jobed-theta.vercel.app/'
LOGOUT_REDIRECT_URL = 'https://jobed-theta.vercel.app/'


EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST ="smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = "jobedinwebsite@gmail.com"
EMAIL_HOST_PASSWORD = "Aditya@2004"

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware', 
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',  
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    "allauth.account.middleware.AccountMiddleware",
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
ACCOUNT_EMAIL_VERIFICATION = 'none'
APPEND_SLASH=False
CORS_ALLOWED_ORIGINS = [
    "https://jobedinwebsite-production.up.railway.app", 
    "https://jobed-theta.vercel.app",  
    "http://localhost:5173",
    "https://127.1.1.0:8000",
    "http://127.1.1.0:8000",

]
CORS_ALLOW_CREDENTIALS = True  
ROOT_URLCONF = 'core.urls'
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_SSL_REDIRECT = True
CSRF_COOKIE_SECURE =False 
SESSION_COOKIE_SECURE = True
SESSION_COOKIE_SAMESITE = None 
CSRF_USE_SESSIONS = False 

from decouple import config
SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'SCOPE': ['profile', 'email'],
        'AUTH_PARAMS': {'access_type': 'online'},
        'CLIENT_ID': os.getenv('GOOGLE_CLIENT_ID'),
        'SECRET': os.getenv('GOOGLE_SECRET'),
    },
    'github': {
        'APP': {
            'client_id':os.getenv('GITHUB_CLIENT_ID'),
            'secret': os.getenv('GITHUB_SECRET'),
            'key': ''
        }
    }
}

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

WSGI_APPLICATION = 'core.wsgi.application'

import dj_database_url

DATABASES = {
        'default': dj_database_url.config(default="postgresql://postgres:MbEEkAztKyrsvnYqPxRxnIfPesHDypcT@autorack.proxy.rlwy.net:20109/railway")
}
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
LANGUAGE_CODE = 'en-us'

CSRF_TRUSTED_ORIGINS = [
    "https://jobedinwebsite-production.up.railway.app",  
    "https://jobed-theta.vercel.app", 
    "https://127.0.0.1:8000",

]
TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles') 
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
# Claudinary

# Load environment variables


# Cloudinary configuration
cloudinary.config( 
  cloud_name=os.getenv('CLOUDINARY_CLOUD_NAME'), 
  api_key=os.getenv('CLOUDINARY_API_KEY'), 
  api_secret=os.getenv('CLOUDINARY_API_SECRET') 
)

# Django Cloudinary storage setup
DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'

# jwt 
from datetime import timedelta

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.SessionAuthentication'
    ),
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=1000),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
    'ALGORITHM': 'HS256',
    'SIGNING_KEY': 'django-insecure-8(#@uu1-h_8nsp&h7n=m#dw8s8-x^+ou8ieg(*=v_=qtvlv^fh',
    'AUTH_HEADER_TYPES': ('Bearer',),
}

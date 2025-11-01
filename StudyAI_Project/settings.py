# StudyAI_Project/settings.py

import os
from pathlib import Path
from dotenv import load_dotenv
from django.urls import reverse_lazy # <-- CRITICAL FIX: ADD THIS IMPORT FOR LOGOUT

# CRITICAL: Load environment variables from .env file immediately
load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

# --- CORE DJANGO SETTINGS ---

SECRET_KEY = os.environ.get('SECRET_KEY', 'default-insecure-key-for-local-use-only')
DEBUG = os.environ.get('DEBUG', 'False') == 'True' 

# 🚨 CRITICAL FIX: ALLOWED_HOSTS is now a manually defined list to include Ngrok.
ALLOWED_HOSTS = [
    '127.0.0.1', 
    'localhost',
    # Ngrok hosts needed for public access (add your specific Ngrok URL if needed)
    '.ngrok-free.dev', 
    '172.20.10.2', # Your local Wi-Fi IP for mobile testing
    '0.0.0.0' # Wildcard for listening
]
CSRF_TRUSTED_ORIGINS = [
    # Trust the Ngrok tunnel domain for form submission
    'https://unmundified-dominica-autecologically.ngrok-free.dev', 
    'https://*.ngrok-free.dev', 
    'https://*.ngrok.dev',
]


# Application definition

INSTALLED_APPS = [
    # Django Defaults
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_browser_reload',
    # Third-Party Apps
    'tailwind',
    
    # Your Project Apps
    'theme', 
    'core',  
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django_browser_reload.middleware.BrowserReloadMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'StudyAI_Project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'], 
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

WSGI_APPLICATION = 'StudyAI_Project.wsgi.application'

# --- DATABASE CONFIGURATION (MySQL) ---

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.environ.get('DB_NAME', 'studyai_db'),
        'USER': os.environ.get('DB_USER', 'root'),
        'PASSWORD': os.environ.get('DB_PASSWORD', 'admin_password_placeholder'),
        'HOST': os.environ.get('DB_HOST', 'localhost'),
        'PORT': os.environ.get('DB_PORT', '3306'),
    }
}


# --- AUTHENTICATION, STATIC, MEDIA ---

LOGIN_REDIRECT_URL = '/' 
# 🚨 CRITICAL FIX: Use reverse_lazy('home') to resolve the URL at startup
LOGOUT_REDIRECT_URL = reverse_lazy('home') 
LOGIN_URL = '/accounts/login/' 

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [
    BASE_DIR / 'static',
]

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# --- THIRD-PARTY APP SETTINGS ---

TAILWIND_APP_NAME = 'theme'
NPM_BIN_PATH = r'C:\Program Files\nodejs\npm.cmd' 
GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY') 
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
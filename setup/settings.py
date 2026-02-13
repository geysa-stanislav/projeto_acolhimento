from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-+d!zub260ee^x@id!qwsvsn&5@9h9hkz1wvn&i31wz+e!!#xg3'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# --- IMPORTANTE: LIBERA O ACESSO NA NUVEM ---
ALLOWED_HOSTS = ['*']

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Seus apps
    'aulas',
    'guia',
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

ROOT_URLCONF = 'setup.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'setup.wsgi.application'

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {
            'min_length': 4,
        }
    },
]

# Internationalization
LANGUAGE_CODE = 'pt-br'
TIME_ZONE = 'America/Campo_Grande' # Deixei o correto
USE_I18N = True
USE_TZ = True

# --- CONFIGURAÇÃO DAS ROUPAS (CSS/STATIC) ---
STATIC_URL = 'static/'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]

# A PASTA ONDE AS ROUPAS FICAM NA NUVEM (Importante!)
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# --- CONFIGURAÇÃO DE MÍDIA (FOTOS) ---
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
MEDIA_URL = 'media/'
MEDIA_ROOT = BASE_DIR / 'media'

# --- CONFIGURAÇÃO DE LOGIN (O que corrige o erro 404) ---
# ONDE ESTÁ A TELA DE LOGIN?
LOGIN_URL = '/login/'

# PRA ONDE VOU DEPOIS DE LOGAR? (Para a Home)
LOGIN_REDIRECT_URL = '/'

# PRA ONDE VOU DEPOIS DE SAIR? (De volta pro Login)
LOGOUT_REDIRECT_URL = '/login/'
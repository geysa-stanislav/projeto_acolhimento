import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# Credenciais via variáveis de ambiente. Não expor secrets
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', 'chave-insegura-apenas-para-desenvolvimento-local')

# Nunca deixar DEBUG True em produção
DEBUG = True

# Restringindo hosts (Substitua pelo seu endereço real do PythonAnywhere)
ALLOWED_HOSTS = ['localhost', '127.0.0.1', 'projetoacolhimento.pythonanywhere.com']

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
    # CKEditor
    'ckeditor',
    'ckeditor_uploader',
    'axes', # NOVO: Sistema de bloqueio de invasões
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'axes.middleware.AxesMiddleware', # NOVO: Monitoramento de tentativas de login
]

ROOT_URLCONF = 'setup.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Implementar política de senha forte nativa do Django
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator', 'OPTIONS': {'min_length': 8}},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Configurações Regionais (UFMS/Campo Grande)
LANGUAGE_CODE = 'pt-br'
TIME_ZONE = 'America/Campo_Grande'
USE_I18N = True
USE_TZ = True

# Arquivos Estáticos e Mídia
STATIC_URL = 'static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
# Adicione esta linha para o Django achar suas imagens:
STATICFILES_DIRS = [BASE_DIR / 'static']

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Configuração do CKEditor
CKEDITOR_UPLOAD_PATH = "uploads/"

# URLs de Autenticação
LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/login/'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# --- PROTEÇÃO CONTRA FORÇA BRUTA (DJANGO-AXES) ---
AUTHENTICATION_BACKENDS = [
    'axes.backends.AxesStandaloneBackend', # Motor de bloqueio do Axes
    'django.contrib.auth.backends.ModelBackend', # Motor padrão do Django
]

AXES_FAILURE_LIMIT = 5  # Bloqueia o IP/Usuário após 5 tentativas de senha errada
AXES_COOLOFF_TIME = 1   # Tempo de bloqueio: 1 hora de geladeira para o hacker
AXES_RESET_ON_SUCCESS = True # Se o usuário verdadeiro lembrar a senha antes da 5ª tentativa, zera o contador
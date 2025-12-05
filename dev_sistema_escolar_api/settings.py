import os
from pathlib import Path
import dj_database_url # <--- Importante para la base de datos de Render

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# ============================================
# SEGURIDAD
# ============================================
# En producción (Render), toma la clave de las variables de entorno.
# En local, usa la clave insegura por defecto para desarrollo.
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-default-key-para-desarrollo-local')

# DEBUG debe ser True solo si la variable no está definida o es 'True'
# En Render, asegúrate de poner la variable de entorno DEBUG = False
DEBUG = os.environ.get('DEBUG', 'True') == 'True'

# ALLOWED_HOSTS: Acepta localhost y tu dominio de Render (o cualquier host en producción con '*')
ALLOWED_HOSTS = ['*'] 

# ============================================
# APLICACIONES
# ============================================
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Third party apps
    'corsheaders',
    'rest_framework',
    'rest_framework.authtoken',
    'django_filters',
    # Local apps
    'dev_sistema_escolar_api',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware', # <--- AÑADIDO: Para servir archivos estáticos en Render
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware', # CORS antes de Common
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# ============================================
# CORS (Permisos de acceso desde Frontend)
# ============================================
CORS_ALLOW_ALL_ORIGINS = True # Útil para desarrollo. En producción, considera restringirlo a tu dominio de frontend.
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_HEADERS = [
    'accept',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
]

ROOT_URLCONF = 'dev_sistema_escolar_api.urls'

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

WSGI_APPLICATION = 'dev_sistema_escolar_api.wsgi.application'

# ============================================
# BASE DE DATOS (La magia para que funcione en ambos lados)
# ============================================
# Por defecto usa SQLite (local). 
# Si Render inyecta la variable DATABASE_URL, dj_database_url la usará automáticamente (PostgreSQL).
DATABASES = {
    'default': dj_database_url.config(
        default='sqlite:///' + os.path.join(BASE_DIR, 'db.sqlite3'),
        conn_max_age=600
    )
}

# ============================================
# VALIDACIÓN DE PASSWORD
# ============================================
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# ============================================
# INTERNACIONALIZACIÓN
# ============================================
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# ============================================
# ARCHIVOS ESTÁTICOS (CSS, JS, Imágenes)
# ============================================
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles') # Carpeta donde Render reunirá los archivos

# Configuración de WhiteNoise para almacenamiento comprimido
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# ============================================
# REST FRAMEWORK
# ============================================
REST_FRAMEWORK = {
    'COERCE_DECIMAL_TO_STRING': False,
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.SessionAuthentication',
        'dev_sistema_escolar_api.models.BearerTokenAuthentication',
    ),
    'DEFAULT_FILTER_BACKENDS': (
        'django_filters.rest_framework.DjangoFilterBackend',
    ),
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    ),
}

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
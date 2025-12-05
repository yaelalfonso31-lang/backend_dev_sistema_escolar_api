import os
from pathlib import Path
from dotenv import load_dotenv
import dj_database_url

# Cargar variables de entorno si existe el archivo .env
load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# --- SEGURIDAD ---
# En producción (PythonAnywhere), asegúrate de establecer esta variable de entorno.
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-clave-por-defecto-cambiar-en-prod')

# Poner en False si estás en producción
DEBUG = os.environ.get('DEBUG', 'False') == 'True'

# ALLOWED_HOSTS: Aquí debes poner tu dominio de PythonAnywhere
# Ejemplo: ['tuusuario.pythonanywhere.com', 'localhost', '127.0.0.1']
ALLOWED_HOSTS_STR = os.environ.get('ALLOWED_HOSTS', 'localhost,127.0.0.1')
ALLOWED_HOSTS = ALLOWED_HOSTS_STR.split(',')


# --- APLICACIONES ---
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Librerías de terceros
    'rest_framework',
    'rest_framework.authtoken',
    'django_filters',
    'corsheaders',
    
    # Tus apps (Asegúrate de que el nombre sea correcto)
    'dev_sistema_escolar_api',
]

# --- MIDDLEWARE (Orden Correcto y Sin Duplicados) ---
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware', # Manejo de estáticos
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',      # CORS debe ir antes de Common
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
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


# --- BASE DE DATOS ---
# Configuración híbrida:
# 1. Intenta buscar una variable DATABASE_URL (para Postgre/MySQL externos si tienes cuenta pagada).
# 2. Si no la encuentra, usa SQLite (archivo local), ideal para PythonAnywhere Gratuito.

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Si defines DATABASE_URL en tus variables de entorno, usará esa DB externa.
# NOTA: En PythonAnywhere GRATIS, esto fallará si es una DB externa (como Render).
if os.environ.get('DATABASE_URL'):
    DATABASES['default'] = dj_database_url.config(conn_max_age=600, ssl_require=True)


# --- VALIDACIÓN DE CONTRASEÑAS ---
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]


# --- INTERNACIONALIZACIÓN ---
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True


# --- ARCHIVOS ESTÁTICOS (CSS, JS, Images) ---
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Configuración WhiteNoise para servir estáticos (útil, aunque PA tiene su propio método)
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'


# --- REST FRAMEWORK ---
REST_FRAMEWORK = {
    'COERCE_DECIMAL_TO_STRING': False,
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,
    'DEFAULT_AUTHENTICATION_CLASSES': (
        # Asegúrate de que esta ruta sea correcta a tu clase personalizada
        'dev_sistema_escolar_api.models.BearerTokenAuthentication',
        'rest_framework.authentication.TokenAuthentication', 
    ),
    'DEFAULT_FILTER_BACKENDS': (
        'django_filters.rest_framework.DjangoFilterBackend',
    ),
}


# --- CORS (Comunicación con Angular) ---
CORS_ALLOW_CREDENTIALS = True

# Define aquí tus orígenes permitidos.
# En producción, agrega tu dominio de Vercel a esta lista.
CORS_ALLOWED_ORIGINS = [
    "http://localhost:4200",
    "http://127.0.0.1:4200",
    # "https://mi-frontend-angular.vercel.app",  <-- Descomenta y pon tu URL real de Vercel aquí
]

# Si tienes problemas, puedes descomentar esto temporalmente para probar, 
# pero NO lo dejes en True en producción permanentemente:
# CORS_ALLOW_ALL_ORIGINS = True
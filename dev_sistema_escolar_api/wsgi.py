"""
WSGI config for dev_sistema_escolar_api project.
"""
"""
WSGI config for dev_sistema_escolar_api project.
"""

import os
from django.core.wsgi import get_wsgi_application

# Configura el módulo de settings por defecto
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dev_sistema_escolar_api.settings')

application = get_wsgi_application()
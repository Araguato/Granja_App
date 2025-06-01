import os
import sys
import django

# Configurar manualmente el path del proyecto
project_root = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(0, project_root)

# Configurar la variable de entorno para los settings
os.environ['DJANGO_SETTINGS_MODULE'] = 'granja.settings'

# Inicializar Django
django.setup()

# Imprimir información básica
from django.conf import settings

print("Django Environment Setup")
print("=" * 30)
print(f"Django Version: {django.get_version()}")
print("\nInstalled Apps:")
for app in settings.INSTALLED_APPS:
    print(f"  - {app}")

print("\nDatabase Configuration:")
print(settings.DATABASES)

print("\nCACHES Configuration:")
print(settings.CACHES)

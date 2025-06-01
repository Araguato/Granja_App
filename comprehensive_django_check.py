import os
import sys
import django
from django.conf import settings
from django.apps import apps
from django.db import connections
from django.core.management import call_command

# Configurar manualmente el path del proyecto
project_root = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(0, project_root)

# Configurar la variable de entorno para los settings
os.environ['DJANGO_SETTINGS_MODULE'] = 'granja.settings'

# Inicializar Django
django.setup()

def comprehensive_django_check():
    print("Comprehensive Django Diagnostic Tool")
    print("=" * 40)
    
    # Información básica de Django
    print(f"\nDjango Version: {django.get_version()}")
    print(f"Python Version: {sys.version}")
    print(f"Project Root: {project_root}")
    
    # Verificar configuraciones
    print("\n--- Settings ---")
    print(f"DEBUG: {settings.DEBUG}")
    print(f"ALLOWED_HOSTS: {settings.ALLOWED_HOSTS}")
    
    # Verificar base de datos
    print("\n--- Database Connections ---")
    for alias, db_settings in settings.DATABASES.items():
        print(f"\nDatabase Alias: {alias}")
        for key, value in db_settings.items():
            if key != 'PASSWORD':  # No mostrar contraseñas
                print(f"  {key}: {value}")
        
        try:
            connection = connections[alias]
            print(f"  Connection Test: {'✅ Successful' if connection.is_usable() else '❌ Failed'}")
        except Exception as e:
            print(f"  Connection Error: {e}")
    
    # Verificar aplicaciones instaladas
    print("\n--- Installed Apps ---")
    for app_config in apps.get_app_configs():
        print(f"\n{app_config.name}")
        print(f"  Path: {app_config.path}")
        
        # Verificar modelos en cada aplicación
        try:
            models = list(app_config.get_models())
            print(f"  Models: {len(models)}")
            for model in models:
                print(f"    - {model.__name__}")
        except Exception as e:
            print(f"  Error getting models: {e}")
    
    # Intentar ejecutar verificaciones de Django
    print("\n--- Django System Checks ---")
    try:
        from django.core.management.commands.check import Command as CheckCommand
        check_command = CheckCommand()
        issues = check_command.handle(deploy=True)
        if not issues:
            print("✅ No deployment issues found")
        else:
            print("❌ Deployment issues detected")
    except Exception as e:
        print(f"Error running system checks: {e}")

if __name__ == "__main__":
    comprehensive_django_check()

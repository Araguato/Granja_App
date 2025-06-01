import os
import sys
import traceback

def setup_django_environment():
    """Configurar manualmente el entorno de Django"""
    # Configurar path del proyecto
    project_root = os.path.abspath(os.path.dirname(__file__))
    sys.path.insert(0, project_root)

    # Configurar variables de entorno
    os.environ['DJANGO_SETTINGS_MODULE'] = 'granja.settings'
    
    # Importar Django
    import django
    django.setup()

def diagnose_django_configuration():
    """Diagnóstico detallado de la configuración de Django"""
    print("Comprehensive Django Configuration Diagnostic")
    print("=" * 50)
    
    try:
        # Importar configuraciones de Django
        from django.conf import settings
        
        # Información básica
        print("\n1. Basic Configuration:")
        print(f"   Django Version: {__import__('django').get_version()}")
        print(f"   Python Version: {sys.version}")
        print(f"   Project Root: {os.getcwd()}")
        
        # Verificar configuraciones críticas
        print("\n2. Critical Settings:")
        critical_settings = [
            'SECRET_KEY', 
            'DEBUG', 
            'ALLOWED_HOSTS', 
            'INSTALLED_APPS', 
            'DATABASES', 
            'CACHES'
        ]
        
        for setting in critical_settings:
            try:
                value = getattr(settings, setting)
                print(f"   {setting}: {value}")
            except Exception as e:
                print(f"   {setting}: ERROR - {e}")
        
        # Verificar aplicaciones
        print("\n3. Installed Apps:")
        from django.apps import apps
        for app_config in apps.get_app_configs():
            print(f"   {app_config.name}")
            try:
                models = list(app_config.get_models())
                print(f"     Models: {len(models)}")
            except Exception as e:
                print(f"     Error getting models: {e}")
        
        # Verificar conexión de base de datos
        print("\n4. Database Connection:")
        from django.db import connections
        for alias, connection in connections.databases.items():
            try:
                with connection.cursor() as cursor:
                    cursor.execute("SELECT 1")
                    print(f"   {alias}: Connection ✅")
            except Exception as e:
                print(f"   {alias}: Connection ❌ - {e}")
    
    except Exception as e:
        print("\nFatal Error during Django configuration diagnosis:")
        traceback.print_exc()

def main():
    try:
        setup_django_environment()
        diagnose_django_configuration()
    except Exception as e:
        print(f"Unhandled error: {e}")
        traceback.print_exc()

if __name__ == "__main__":
    main()

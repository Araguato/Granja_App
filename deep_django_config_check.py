import os
import sys
import traceback

def deep_django_config_check():
    print("Deep Django Configuration Diagnostic")
    print("=" * 40)
    
    # Información del entorno
    print("\nEnvironment Information:")
    print(f"Current Working Directory: {os.getcwd()}")
    print(f"Python Executable: {sys.executable}")
    print(f"PYTHONPATH: {sys.path}")
    
    # Variables de entorno
    print("\nEnvironment Variables:")
    print(f"DJANGO_SETTINGS_MODULE: {os.environ.get('DJANGO_SETTINGS_MODULE', 'NOT SET')}")
    
    # Intentar configurar manualmente
    try:
        # Agregar el directorio del proyecto al path de Python
        project_root = os.path.abspath(os.path.dirname(__file__))
        if project_root not in sys.path:
            sys.path.insert(0, project_root)
        
        # Configurar manualmente el módulo de settings
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'granja.settings')
        
        # Importar Django y configurarlo
        import django
        django.setup()
        
        # Importar configuraciones
        from django.conf import settings
        
        # Imprimir configuraciones detalladas
        print("\nDjango Configuration:")
        print(f"Django Version: {django.get_version()}")
        
        print("\nInstalled Apps:")
        for app in settings.INSTALLED_APPS:
            print(f"  - {app}")
        
        print("\nDatabase Configuration:")
        print(f"  DEFAULT DATABASE: {settings.DATABASES.get('default', 'NOT CONFIGURED')}")
        
        print("\nCACHES Configuration:")
        print(f"  CACHES: {settings.CACHES}")
        
        # Intentar importar apps
        from django.apps import apps
        print("\nApp Configurations:")
        for app_config in apps.get_app_configs():
            print(f"  {app_config.name}: {app_config.path}")
    
    except Exception as e:
        print("\nError during Django setup:")
        print(f"  {type(e).__name__}: {e}")
        print("\nDetailed Traceback:")
        traceback.print_exc()

if __name__ == "__main__":
    deep_django_config_check()

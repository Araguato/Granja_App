import os
import sys
import traceback

def minimal_migration_check():
    print("Minimal Migration Check")
    print("=" * 30)
    
    # Configurar path del proyecto
    project_root = os.path.abspath(os.path.dirname(__file__))
    sys.path.insert(0, project_root)
    
    # Configurar variables de entorno
    os.environ['DJANGO_SETTINGS_MODULE'] = 'granja.settings'
    
    try:
        import django
        django.setup()
        
        # Importar herramientas de migración
        from django.core.management import call_command
        from django.apps import apps
        
        print("\nInstalled Apps:")
        for app_config in apps.get_app_configs():
            print(f"  - {app_config.name}")
            try:
                models = list(app_config.get_models())
                print(f"    Models: {len(models)}")
                for model in models:
                    print(f"      * {model.__name__}")
            except Exception as e:
                print(f"    Error getting models: {e}")
        
        print("\nAttempting to create migrations...")
        call_command('makemigrations', verbosity=2)
        
    except Exception as e:
        print("\n❌ Error during migration check:")
        print(f"Type: {type(e).__name__}")
        print(f"Error: {e}")
        print("\nDetailed Traceback:")
        traceback.print_exc()

if __name__ == "__main__":
    minimal_migration_check()

import os
import sys
import django
from django.conf import settings
from django.apps import apps

# Configurar manualmente el path del proyecto
project_root = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(0, project_root)

# Configurar la variable de entorno para los settings
os.environ['DJANGO_SETTINGS_MODULE'] = 'granja.settings'

# Inicializar Django
django.setup()

def diagnose_migrations():
    print("Migration Diagnostic Tool")
    print("=" * 30)
    
    # Listar todas las aplicaciones
    print("\nInstalled Apps:")
    for app_config in apps.get_app_configs():
        print(f"  - {app_config.name}")
        
        # Verificar si la aplicación tiene modelos
        try:
            models = list(app_config.get_models())
            print(f"    Models: {len(models)}")
            for model in models:
                print(f"      - {model.__name__}")
        except Exception as e:
            print(f"    Error getting models: {e}")
        
        # Verificar migraciones
        try:
            from django.db.migrations.loader import MigrationLoader
            loader = MigrationLoader(None, ignore_no_migrations=True)
            
            # Buscar migraciones para esta aplicación
            app_migrations = [m for m in loader.graph.nodes.keys() if m[0] == app_config.label]
            
            print(f"    Migrations: {len(app_migrations)}")
            for migration in app_migrations:
                print(f"      - {migration[1]}")
        except Exception as e:
            print(f"    Error checking migrations: {e}")

if __name__ == "__main__":
    diagnose_migrations()

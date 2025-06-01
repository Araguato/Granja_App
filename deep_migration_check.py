import os
import sys
import traceback

def deep_migration_check():
    print("Deep Migration Diagnostic")
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
        from django.db.migrations.loader import MigrationLoader
        from django.db import connections
        
        print("\nMigration Diagnostic Details:")
        
        # Obtener loader de migraciones
        loader = MigrationLoader(connections['default'], ignore_no_migrations=True)
        
        print("\nMigration Graph:")
        for key, migration in loader.graph.nodes.items():
            print(f"  App: {key[0]}, Migration: {key[1]}")
        
        print("\nDetailed App Migration Status:")
        for app_config in apps.get_app_configs():
            print(f"\n{app_config.name}:")
            
            # Verificar modelos
            try:
                models = list(app_config.get_models())
                print(f"  Models: {len(models)}")
                for model in models:
                    print(f"    * {model.__name__}")
            except Exception as e:
                print(f"  Error getting models: {e}")
            
            # Verificar migraciones
            try:
                app_migrations = [m for m in loader.graph.nodes.keys() if m[0] == app_config.label]
                print(f"  Migrations: {len(app_migrations)}")
                for migration in app_migrations:
                    print(f"    - {migration[1]}")
            except Exception as e:
                print(f"  Error checking migrations: {e}")
        
        print("\nAttempting to create migrations...")
        call_command('makemigrations', verbosity=2)
        
    except Exception as e:
        print("\n❌ Error during migration check:")
        print(f"Type: {type(e).__name__}")
        print(f"Error: {e}")
        print("\nDetailed Traceback:")
        traceback.print_exc()

if __name__ == "__main__":
    deep_migration_check()

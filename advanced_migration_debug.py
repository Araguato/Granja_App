import os
import sys
import traceback

def advanced_migration_debug():
    print("Advanced Django Migration Debugging")
    print("=" * 40)
    
    # Configurar path del proyecto
    project_root = os.path.abspath(os.path.dirname(__file__))
    sys.path.insert(0, project_root)
    
    # Configurar variables de entorno
    os.environ['DJANGO_SETTINGS_MODULE'] = 'granja.settings'
    
    try:
        import django
        from django.core.management import call_command
        from django.apps import apps
        from django.db import connections
        from django.db.migrations.loader import MigrationLoader
        from django.db.migrations.recorder import MigrationRecorder
        
        # Forzar configuración de Django
        django.setup()
        
        # Información detallada de migración
        print("\n1. Aplicaciones Instaladas:")
        for app_config in apps.get_app_configs():
            print(f"  - {app_config.name}")
            try:
                models = list(app_config.get_models())
                print(f"    Modelos: {len(models)}")
                for model in models:
                    print(f"      * {model.__name__}")
            except Exception as e:
                print(f"    Error obteniendo modelos: {e}")
        
        # Verificar estado de migraciones
        print("\n2. Estado de Migraciones:")
        connection = connections['default']
        loader = MigrationLoader(connection)
        recorder = MigrationRecorder(connection)
        
        # Migraciones aplicadas
        print("\n  Migraciones Aplicadas:")
        applied_migrations = recorder.applied_migrations()
        for migration in applied_migrations:
            print(f"    - {migration[0]}: {migration[1]}")
        
        # Migraciones pendientes
        print("\n  Migraciones Pendientes:")
        for app_label, migration_dict in loader.graph.nodes.items():
            if app_label not in ['contenttypes', 'admin', 'auth', 'sessions']:
                print(f"    {app_label}:")
                print(f"      Migrations: {migration_dict}")
        
        # Intentar crear migraciones
        print("\n3. Creando Migraciones...")
        call_command('makemigrations', verbosity=2)
        
    except Exception as e:
        print("\n❌ Error durante diagnóstico de migraciones:")
        print(f"Tipo: {type(e).__name__}")
        print(f"Error: {e}")
        print("\nTraza detallada:")
        traceback.print_exc()

if __name__ == "__main__":
    advanced_migration_debug()

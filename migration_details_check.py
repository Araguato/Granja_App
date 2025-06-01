import os
import sys
import django
from django.conf import settings
from django.db import connections
from django.db.migrations.recorder import MigrationRecorder
from django.db.migrations.loader import MigrationLoader

def detailed_migration_check():
    # Configurar entorno de Django
    os.environ['DJANGO_SETTINGS_MODULE'] = 'granja.settings'
    django.setup()

    print("Detailed Migration Status Check")
    print("=" * 35)

    # Obtener conexión por defecto
    connection = connections['default']

    # Crear recorder y loader de migraciones
    recorder = MigrationRecorder(connection)
    loader = MigrationLoader(connection)

    # Obtener migraciones aplicadas
    applied_migrations = recorder.applied_migrations()
    
    print("\n1. Applied Migrations:")
    for migration in applied_migrations:
        print(f"  - {migration[0]}: {migration[1]}")

    print("\n2. Migration Graph Details:")
    for key, migration in loader.graph.nodes.items():
        print(f"  App: {key[0]}, Migration: {key[1]}")

    print("\n3. Detailed Migration Status:")
    for app_config in django.apps.apps.get_app_configs():
        app_label = app_config.label
        if app_label.startswith('django.'):
            continue
        
        print(f"\nApp: {app_label}")
        try:
            # Obtener modelos de la aplicación
            models = list(app_config.get_models())
            print(f"  Models: {len(models)}")
            for model in models:
                print(f"    * {model.__name__}")
            
            # Obtener todas las migraciones para esta app
            app_migrations = [m for m in loader.graph.nodes.keys() if m[0] == app_label]
            
            print("\n  Migrations:")
            if not app_migrations:
                print("    No migrations found")
            for migration in app_migrations:
                # Verificar si está aplicada
                is_applied = (migration[0], migration[1]) in applied_migrations
                status = "✅ Applied" if is_applied else "❌ Not Applied"
                print(f"    - {migration[1]}: {status}")
        
        except Exception as e:
            print(f"  Error checking app {app_label}: {e}")

if __name__ == "__main__":
    detailed_migration_check()

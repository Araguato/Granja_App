import os
import sys
import psycopg2
import django
from django.db import connection

# Configurar el entorno Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'granja.settings')
django.setup()

def test_postgres_connection():
    """Prueba la conexión directa a PostgreSQL usando psycopg2"""
    print("=== DIAGNÓSTICO DE CONEXIÓN A POSTGRESQL ===")
    
    # Obtener parámetros de conexión desde settings
    from django.conf import settings
    db_settings = settings.DATABASES['default']
    
    db_name = db_settings['NAME']
    db_user = db_settings['USER']
    db_password = db_settings['PASSWORD']
    db_host = db_settings['HOST']
    db_port = db_settings['PORT']
    
    print(f"Intentando conectar a PostgreSQL con los siguientes parámetros:")
    print(f"- Base de datos: {db_name}")
    print(f"- Usuario: {db_user}")
    print(f"- Host: {db_host}")
    print(f"- Puerto: {db_port}")
    
    try:
        # Intentar conexión directa con psycopg2
        conn = psycopg2.connect(
            dbname=db_name,
            user=db_user,
            password=db_password,
            host=db_host,
            port=db_port
        )
        
        print("\n✅ Conexión exitosa a PostgreSQL!")
        
        # Verificar tablas en la base de datos
        cursor = conn.cursor()
        cursor.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public'
            ORDER BY table_name;
        """)
        
        tables = cursor.fetchall()
        
        print(f"\nTablas encontradas en la base de datos ({len(tables)}):")
        for i, table in enumerate(tables, 1):
            print(f"{i}. {table[0]}")
        
        # Verificar si existen las tablas principales
        main_tables = [
            'avicola_userprofile', 
            'avicola_empresa',
            'produccion_granja',
            'produccion_galpon',
            'produccion_lote',
            'inventario_proveedor',
            'inventario_raza',
            'ventas_cliente'
        ]
        
        print("\nVerificando tablas principales:")
        for table in main_tables:
            found = any(table == t[0] for t in tables)
            status = "✅ Encontrada" if found else "❌ No encontrada"
            print(f"- {table}: {status}")
        
        # Verificar registros en tablas principales
        print("\nConteo de registros en tablas principales:")
        for table in main_tables:
            if any(table == t[0] for t in tables):
                cursor.execute(f"SELECT COUNT(*) FROM {table}")
                count = cursor.fetchone()[0]
                print(f"- {table}: {count} registros")
        
        cursor.close()
        conn.close()
        
    except psycopg2.OperationalError as e:
        print(f"\n❌ Error de conexión a PostgreSQL: {e}")
        print("\nPosibles soluciones:")
        print("1. Verifica que el servidor PostgreSQL esté en ejecución")
        print("2. Comprueba que las credenciales sean correctas")
        print("3. Asegúrate de que la base de datos exista")
        print("4. Verifica que el puerto sea el correcto")
        print("5. Comprueba que el firewall no esté bloqueando la conexión")
        
    except Exception as e:
        print(f"\n❌ Error inesperado: {e}")

def test_django_models():
    """Prueba el acceso a los modelos de Django"""
    print("\n=== DIAGNÓSTICO DE MODELOS DJANGO ===")
    
    try:
        # Importar modelos principales
        from avicola.models import UserProfile, Empresa
        from produccion.models import Granja, Galpon, Lote
        from inventario.models import Proveedor, Raza
        
        # Verificar cantidad de registros
        print("\nConteo de registros en modelos principales:")
        print(f"- UserProfile: {UserProfile.objects.count()} registros")
        print(f"- Empresa: {Empresa.objects.count()} registros")
        print(f"- Granja: {Granja.objects.count()} registros")
        print(f"- Galpon: {Galpon.objects.count()} registros")
        print(f"- Lote: {Lote.objects.count()} registros")
        print(f"- Proveedor: {Proveedor.objects.count()} registros")
        print(f"- Raza: {Raza.objects.count()} registros")
        
        # Verificar usuarios
        print("\nUsuarios registrados:")
        users = UserProfile.objects.all()
        for i, user in enumerate(users, 1):
            print(f"{i}. {user.username} ({user.get_user_type_display()})")
        
    except Exception as e:
        print(f"\n❌ Error al acceder a los modelos de Django: {e}")

def test_migrations():
    """Verifica el estado de las migraciones"""
    print("\n=== DIAGNÓSTICO DE MIGRACIONES ===")
    
    try:
        from django.db.migrations.recorder import MigrationRecorder
        
        migrations = MigrationRecorder.Migration.objects.all()
        
        print(f"Total de migraciones aplicadas: {migrations.count()}")
        
        # Agrupar migraciones por aplicación
        app_migrations = {}
        for migration in migrations:
            app = migration.app
            if app not in app_migrations:
                app_migrations[app] = []
            app_migrations[app].append(migration.name)
        
        print("\nMigraciones por aplicación:")
        for app, migs in app_migrations.items():
            print(f"- {app}: {len(migs)} migraciones")
            
    except Exception as e:
        print(f"\n❌ Error al verificar migraciones: {e}")

if __name__ == "__main__":
    try:
        test_postgres_connection()
        test_django_models()
        test_migrations()
        
        print("\n=== RECOMENDACIONES ===")
        print("Si no hay errores pero no ves datos en la aplicación:")
        print("1. Verifica que las migraciones estén aplicadas correctamente")
        print("2. Comprueba que los datos de ejemplo no estén siendo mostrados por alguna lógica en las vistas")
        print("3. Asegúrate de que los permisos de usuario estén configurados correctamente")
        print("4. Revisa los logs de Django para ver si hay errores específicos")
        
    except Exception as e:
        print(f"Error general en el diagnóstico: {e}")

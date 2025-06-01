import os
import sys
import subprocess
import psycopg2
from psycopg2 import sql
from django.core.management import execute_from_command_line

# Configurar el entorno de Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'granja.settings')
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def verificar_instalacion_postgres():
    print("Verificando si psycopg2 está instalado...")
    try:
        import psycopg2
        print("[OK] psycopg2 está instalado.")
        return True
    except ImportError:
        print("[ERROR] psycopg2 no está instalado.")
        print("Instalando psycopg2...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "psycopg2-binary"])
            print("[OK] psycopg2-binary instalado correctamente.")
            import psycopg2
            return True
        except Exception as e:
            print(f"[ERROR] No se pudo instalar psycopg2-binary: {e}")
            return False

def verificar_conexion_postgres():
    print("\nVerificando conexión a PostgreSQL...")
    
    # Obtener configuración de settings.py
    try:
        from django.conf import settings
        db_settings = settings.DATABASES['default']
        db_name = db_settings.get('NAME', 'DB_Avicola')
        db_user = db_settings.get('USER', 'usuario_avicola')
        db_password = db_settings.get('PASSWORD', 'Aves2025')
        db_host = db_settings.get('HOST', 'localhost')
        db_port = db_settings.get('PORT', '5432')
        
        print(f"Configuración de base de datos:")
        print(f"  Nombre: {db_name}")
        print(f"  Usuario: {db_user}")
        print(f"  Host: {db_host}")
        print(f"  Puerto: {db_port}")
    except Exception as e:
        print(f"[ERROR] No se pudo obtener la configuración de Django: {e}")
        db_name = 'DB_Avicola'
        db_user = 'usuario_avicola'
        db_password = 'Aves2025'
        db_host = 'localhost'
        db_port = '5432'
    
    # Intentar conectar a PostgreSQL
    try:
        print("\nIntentando conectar a PostgreSQL...")
        conn = psycopg2.connect(
            dbname='postgres',  # Primero conectamos a la base de datos por defecto
            user=db_user,
            password=db_password,
            host=db_host,
            port=db_port
        )
        conn.autocommit = True
        cursor = conn.cursor()
        print("[OK] Conexión a PostgreSQL establecida correctamente.")
        
        # Verificar si la base de datos existe
        cursor.execute("SELECT 1 FROM pg_database WHERE datname = %s", (db_name,))
        if cursor.fetchone():
            print(f"[OK] La base de datos '{db_name}' existe.")
        else:
            print(f"[ERROR] La base de datos '{db_name}' no existe.")
            crear_db = input(f"¿Deseas crear la base de datos '{db_name}'? (S/N): ")
            if crear_db.upper() == 'S':
                try:
                    # Cerrar la conexión actual
                    cursor.close()
                    conn.close()
                    
                    # Conectar como superusuario postgres
                    print("Intentando conectar como usuario postgres...")
                    conn = psycopg2.connect(
                        dbname='postgres',
                        user='postgres',
                        password=input("Ingresa la contraseña del usuario postgres: "),
                        host=db_host,
                        port=db_port
                    )
                    conn.autocommit = True
                    cursor = conn.cursor()
                    
                    # Crear usuario si no existe
                    cursor.execute("SELECT 1 FROM pg_roles WHERE rolname = %s", (db_user,))
                    if not cursor.fetchone():
                        print(f"Creando usuario '{db_user}'...")
                        cursor.execute(
                            sql.SQL("CREATE USER {} WITH PASSWORD {}").format(
                                sql.Identifier(db_user),
                                sql.Literal(db_password)
                            )
                        )
                        print(f"[OK] Usuario '{db_user}' creado.")
                    
                    # Crear base de datos
                    print(f"Creando base de datos '{db_name}'...")
                    cursor.execute(
                        sql.SQL("CREATE DATABASE {} WITH OWNER = {}").format(
                            sql.Identifier(db_name),
                            sql.Identifier(db_user)
                        )
                    )
                    print(f"[OK] Base de datos '{db_name}' creada.")
                    
                    # Asignar permisos
                    cursor.execute(
                        sql.SQL("GRANT ALL PRIVILEGES ON DATABASE {} TO {}").format(
                            sql.Identifier(db_name),
                            sql.Identifier(db_user)
                        )
                    )
                    print(f"[OK] Permisos asignados a '{db_user}' sobre '{db_name}'.")
                    
                    # Reconectar con el usuario normal a la nueva base de datos
                    cursor.close()
                    conn.close()
                    
                    conn = psycopg2.connect(
                        dbname=db_name,
                        user=db_user,
                        password=db_password,
                        host=db_host,
                        port=db_port
                    )
                    conn.autocommit = True
                    cursor = conn.cursor()
                    print(f"[OK] Conexión a '{db_name}' establecida correctamente.")
                    
                except Exception as e:
                    print(f"[ERROR] No se pudo crear la base de datos: {e}")
                    return False
        
        # Verificar si podemos conectar a la base de datos del proyecto
        try:
            cursor.close()
            conn.close()
            
            conn = psycopg2.connect(
                dbname=db_name,
                user=db_user,
                password=db_password,
                host=db_host,
                port=db_port
            )
            cursor = conn.cursor()
            print(f"[OK] Conexión a la base de datos '{db_name}' establecida correctamente.")
            
            # Verificar si hay tablas en la base de datos
            cursor.execute("""
                SELECT COUNT(*) 
                FROM information_schema.tables 
                WHERE table_schema = 'public'
            """)
            table_count = cursor.fetchone()[0]
            
            if table_count > 0:
                print(f"[OK] La base de datos '{db_name}' contiene {table_count} tablas.")
                
                # Listar algunas tablas
                cursor.execute("""
                    SELECT table_name 
                    FROM information_schema.tables 
                    WHERE table_schema = 'public'
                    LIMIT 10
                """)
                tables = cursor.fetchall()
                print("Tablas encontradas:")
                for table in tables:
                    print(f"  - {table[0]}")
            else:
                print(f"[ADVERTENCIA] La base de datos '{db_name}' no contiene tablas.")
                aplicar_migraciones = input("¿Deseas aplicar las migraciones de Django? (S/N): ")
                if aplicar_migraciones.upper() == 'S':
                    print("Aplicando migraciones...")
                    try:
                        execute_from_command_line(['manage.py', 'migrate'])
                        print("[OK] Migraciones aplicadas correctamente.")
                    except Exception as e:
                        print(f"[ERROR] No se pudieron aplicar las migraciones: {e}")
            
            cursor.close()
            conn.close()
            return True
            
        except Exception as e:
            print(f"[ERROR] No se pudo conectar a la base de datos '{db_name}': {e}")
            return False
        
    except Exception as e:
        print(f"[ERROR] No se pudo conectar a PostgreSQL: {e}")
        print("\nPosibles causas:")
        print("1. PostgreSQL no está instalado")
        print("2. El servicio de PostgreSQL no está en ejecución")
        print("3. Las credenciales son incorrectas")
        print("4. El puerto está bloqueado o es incorrecto")
        
        instalar_postgres = input("\n¿Deseas cambiar a SQLite para desarrollo? (S/N): ")
        if instalar_postgres.upper() == 'S':
            cambiar_a_sqlite()
        
        return False

def cambiar_a_sqlite():
    print("\nCambiando a SQLite para desarrollo...")
    
    # Leer el archivo settings.py
    settings_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'granja', 'settings.py')
    
    with open(settings_path, 'r', encoding='utf-8') as f:
        settings_content = f.read()
    
    # Buscar la configuración de DATABASES
    if 'django.db.backends.postgresql' in settings_content:
        # Reemplazar la configuración de PostgreSQL por SQLite
        sqlite_config = """# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Configuración original de PostgreSQL (comentada)
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': os.getenv('DB_NAME', 'DB_Avicola'),
#         'USER': os.getenv('DB_USER', 'usuario_avicola'),
#         'PASSWORD': os.getenv('DB_PASSWORD', 'Aves2025'),
#         'HOST': os.getenv('DB_HOST', 'localhost'),
#         'PORT': os.getenv('DB_PORT', '5432'),
#     }
# }"""
        
        # Reemplazar la configuración
        import re
        new_settings = re.sub(
            r'# Database.*?DATABASES\s*=\s*\{.*?\'default\':\s*\{.*?\'ENGINE\':\s*\'django\.db\.backends\.postgresql\'.*?\}\s*\}',
            sqlite_config,
            settings_content,
            flags=re.DOTALL
        )
        
        # Guardar el archivo
        with open(settings_path, 'w', encoding='utf-8') as f:
            f.write(new_settings)
        
        print("[OK] Configuración cambiada a SQLite.")
        
        # Aplicar migraciones
        aplicar_migraciones = input("¿Deseas aplicar las migraciones a SQLite? (S/N): ")
        if aplicar_migraciones.upper() == 'S':
            print("Aplicando migraciones a SQLite...")
            try:
                execute_from_command_line(['manage.py', 'migrate'])
                print("[OK] Migraciones aplicadas correctamente a SQLite.")
            except Exception as e:
                print(f"[ERROR] No se pudieron aplicar las migraciones: {e}")
    else:
        print("[INFO] La configuración ya está usando SQLite.")

def main():
    print("===================================================")
    print("    DIAGNÓSTICO DE CONEXIÓN A POSTGRESQL")
    print("===================================================")
    
    if verificar_instalacion_postgres():
        verificar_conexion_postgres()
    
    print("\nDiagnóstico completado.")
    input("Presiona Enter para salir...")

if __name__ == "__main__":
    main()

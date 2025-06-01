import sys
import os
from sqlalchemy import create_engine, inspect, text
from dotenv import load_dotenv
import psycopg2
from psycopg2 import OperationalError

def test_connection():
    try:
        # Load environment variables
        load_dotenv()
        
        # Get database configuration
        db_config = {
            'dbname': os.getenv('DB_NAME', 'DB_Avicola'),
            'user': os.getenv('DB_USER', 'usuario_avicola'),
            'password': os.getenv('DB_PASSWORD', 'Aves2025'),
            'host': os.getenv('DB_HOST', 'localhost'),
            'port': os.getenv('DB_PORT', '5432')
        }
        
        # Print connection details (without password)
        print("ℹ️  Intentando conectar a la base de datos con los siguientes parámetros:")
        print(f"   Host: {db_config['host']}")
        print(f"   Puerto: {db_config['port']}")
        print(f"   Base de datos: {db_config['dbname']}")
        print(f"   Usuario: {db_config['user']}")
        
        # Test direct connection with psycopg2
        print("\n🔍 Probando conexión directa con psycopg2...")
        try:
            conn = psycopg2.connect(**db_config)
            cur = conn.cursor()
            cur.execute("SELECT version();")
            db_version = cur.fetchone()
            print(f"✅ Conexión exitosa a PostgreSQL: {db_version[0]}")
            cur.close()
            conn.close()
        except OperationalError as e:
            print(f"❌ Error de conexión con psycopg2: {e}")
            print("\nPor favor verifica que:")
            print("1. PostgreSQL esté en ejecución")
            print("2. Las credenciales en el archivo .env sean correctas")
            print("3. La base de datos exista y sea accesible")
            return False
        
        # Test SQLAlchemy connection
        print("\n🔍 Probando conexión con SQLAlchemy...")
        try:
            conn_string = f"postgresql://{db_config['user']}:{db_config['password']}@{db_config['host']}:{db_config['port']}/{db_config['dbname']}"
            engine = create_engine(conn_string)
            
            with engine.connect() as conn:
                # Test raw SQL execution
                result = conn.execute(text("SELECT version()"))
                print(f"✅ SQLAlchemy versión de PostgreSQL: {result.scalar()}")
                
                # Get table names
                inspector = inspect(engine)
                tables = inspector.get_table_names()
                print(f"\n📊 Tablas encontradas: {len(tables)}")
                if tables:
                    print("Primeras 5 tablas:")
                    for table in tables[:5]:
                        print(f"  - {table}")
            
            return True
            
        except Exception as e:
            print(f"❌ Error con SQLAlchemy: {e}")
            return False
            
    except Exception as e:
        print(f"\n❌ Error inesperado: {str(e)}")
        return False
    finally:
        print("\nPrueba finalizada.")

if __name__ == "__main__":
    test_connection()
    input("\nPresiona Enter para salir...")
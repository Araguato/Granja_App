import os
import psycopg2
from dotenv import load_dotenv

def test_postgres_connection():
    # Cargar variables de entorno
    load_dotenv()
    
    # Parámetros de conexión
    conn_params = {
        'dbname': os.getenv('DB_NAME', 'DB_Avicola'),
        'user': os.getenv('DB_USER', 'usuario_avicola'),
        'password': os.getenv('DB_PASSWORD', 'Aves2025'),
        'host': os.getenv('DB_HOST', 'localhost'),
        'port': os.getenv('DB_PORT', '5432')
    }
    
    print("PostgreSQL Connection Test")
    print("=" * 30)
    
    print("\nConnection Parameters:")
    for key, value in conn_params.items():
        # Ocultar contraseña
        display_value = '****' if key == 'password' else value
        print(f"  {key}: {display_value}")
    
    try:
        # Intentar conectar
        conn = psycopg2.connect(**conn_params)
        
        # Crear cursor
        cur = conn.cursor()
        
        # Ejecutar consulta de prueba
        cur.execute("SELECT version();")
        version = cur.fetchone()
        
        print("\n✅ Connection Successful!")
        print(f"PostgreSQL Version: {version[0]}")
        
        # Verificar si la base de datos existe
        cur.execute("SELECT 1 FROM pg_database WHERE datname = %s", (conn_params['dbname'],))
        db_exists = cur.fetchone()
        
        if db_exists:
            print(f"✅ Database '{conn_params['dbname']}' exists")
        else:
            print(f"❌ Database '{conn_params['dbname']}' does not exist")
        
        # Cerrar cursor y conexión
        cur.close()
        conn.close()
        
    except Exception as e:
        print(f"\n❌ Connection Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_postgres_connection()

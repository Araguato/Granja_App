import os
import psycopg2
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

def test_postgres_connection():
    try:
        # Obtener parámetros de conexión
        conn_params = {
            'dbname': os.getenv('DB_NAME', 'DB_Avicola'),
            'user': os.getenv('DB_USER', 'usuario_avicola'),
            'password': os.getenv('DB_PASSWORD', 'Aves2025'),
            'host': os.getenv('DB_HOST', 'localhost'),
            'port': os.getenv('DB_PORT', '5432')
        }
        
        print("Intentando conectar a PostgreSQL...")
        print("Parámetros de conexión:")
        for key, value in conn_params.items():
            print(f"  {key}: {value}")
        
        # Intentar establecer conexión
        conn = psycopg2.connect(**conn_params)
        
        # Crear un cursor
        cur = conn.cursor()
        
        # Ejecutar consulta de prueba
        cur.execute("SELECT version();")
        version = cur.fetchone()
        
        print("\n✅ Conexión exitosa!")
        print(f"Versión de PostgreSQL: {version[0]}")
        
        # Cerrar cursor y conexión
        cur.close()
        conn.close()
        
    except Exception as e:
        print(f"\n❌ Error de conexión: {e}")

if __name__ == "__main__":
    test_postgres_connection()

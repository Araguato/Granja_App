import psycopg2
from psycopg2 import OperationalError

def test_postgres_connection(dbname, user, password, host, port):
    print("PostgreSQL Connection Debugging")
    print("=" * 35)
    
    connection_params = {
        'dbname': dbname,
        'user': user,
        'password': password,
        'host': host,
        'port': port
    }
    
    print("\nConnection Parameters:")
    for key, value in connection_params.items():
        # Ocultar contraseña
        display_value = '****' if key == 'password' else value
        print(f"  {key}: {display_value}")
    
    try:
        # Intentar conectar
        conn = psycopg2.connect(**connection_params)
        
        # Crear cursor
        cur = conn.cursor()
        
        # Ejecutar consulta de prueba
        cur.execute("SELECT version();")
        version = cur.fetchone()
        
        print("\n✅ Connection Successful!")
        print(f"PostgreSQL Version: {version[0]}")
        
        # Verificar bases de datos existentes
        cur.execute("SELECT datname FROM pg_database;")
        databases = cur.fetchall()
        
        print("\nExisting Databases:")
        for db in databases:
            print(f"  - {db[0]}")
        
        # Cerrar cursor y conexión
        cur.close()
        conn.close()
        
    except OperationalError as e:
        print("\n❌ Connection Error:")
        print(f"Error Type: {type(e).__name__}")
        print(f"Error Details: {e}")
        
        # Intentar diagnosticar el error
        error_message = str(e).lower()
        if "password" in error_message:
            print("\n🔒 Possible Password Issue:")
            print("  - Verify the password is correct")
            print("  - Check for any special characters that might need escaping")
        elif "connection refused" in error_message:
            print("\n🚫 Connection Refused:")
            print("  - Verify PostgreSQL is running")
            print("  - Check host and port settings")
        elif "authentication" in error_message:
            print("\n🔐 Authentication Failed:")
            print("  - Check username")
            print("  - Verify user permissions")

if __name__ == "__main__":
    # Parámetros de conexión desde el .env
    test_postgres_connection(
        dbname='DB_Avicola',
        user='usuario_avicola',
        password='Aves2025',
        host='localhost',
        port='5432'
    )

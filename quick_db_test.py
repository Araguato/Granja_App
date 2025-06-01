import os
import sys

def quick_test():
    print("Quick Database Configuration Test")
    print("=" * 40)
    
    # Imprimir variables de entorno
    print("\nEnvironment Variables:")
    env_vars = ['DB_NAME', 'DB_USER', 'DB_HOST', 'DB_PORT']
    for var in env_vars:
        print(f"  {var}: {os.environ.get(var, 'NOT SET')}")
    
    # Intentar importar psycopg2
    try:
        import psycopg2
        print("\npsycopg2 imported successfully")
    except ImportError as e:
        print(f"\nError importing psycopg2: {e}")
        return
    
    # Intentar conexión básica
    try:
        conn = psycopg2.connect(
            dbname=os.environ.get('DB_NAME', 'DB_Avicola'),
            user=os.environ.get('DB_USER', 'usuario_avicola'),
            password=os.environ.get('DB_PASSWORD', 'Aves2025'),
            host=os.environ.get('DB_HOST', 'localhost'),
            port=os.environ.get('DB_PORT', '5432')
        )
        print("\n✅ Database connection successful")
        conn.close()
    except Exception as e:
        print(f"\n❌ Database connection error: {e}")

if __name__ == "__main__":
    quick_test()

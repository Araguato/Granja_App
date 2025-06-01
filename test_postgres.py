import psycopg2

try:
    # Intenta conectar a PostgreSQL con los parámetros de conexión
    conn = psycopg2.connect(
        dbname="DB_Avicola",
        user="usuario_avicola",
        password="Aves2025",
        host="localhost",
        port="5432"
    )
    
    print("✅ Conexión exitosa a PostgreSQL!")
    
    # Verificar que la conexión esté activa
    cursor = conn.cursor()
    cursor.execute("SELECT version();")
    version = cursor.fetchone()
    print(f"Versión de PostgreSQL: {version[0]}")
    
    cursor.close()
    conn.close()
    
except psycopg2.OperationalError as e:
    print(f"❌ Error de conexión a PostgreSQL: {e}")
    print("\nPosibles soluciones:")
    print("1. Verifica que el servidor PostgreSQL esté en ejecución")
    print("2. Comprueba que las credenciales sean correctas")
    print("3. Asegúrate de que la base de datos 'DB_Avicola' exista")
    print("4. Verifica que el puerto 5432 esté abierto")
    
except Exception as e:
    print(f"❌ Error inesperado: {e}")

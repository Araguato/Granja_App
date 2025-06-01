import sys
import os
from sqlalchemy import create_engine, inspect
from dotenv import load_dotenv

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
        
        # Create connection string
        conn_string = f"postgresql://{db_config['user']}:{db_config['password']}@{db_config['host']}:{db_config['port']}/{db_config['dbname']}"
        
        # Create engine
        engine = create_engine(conn_string)
        
        # Test connection
        with engine.connect() as conn:
            inspector = inspect(engine)
            tables = inspector.get_table_names()
            
            if tables:
                first_table = tables[0]
                from sqlalchemy import text
                result = conn.execute(text(f"SELECT COUNT(*) FROM {first_table}"))
                row_count = result.scalar()
                
                print("✅ Conexión exitosa a la base de datos!")
                print(f"\n📊 Tablas encontradas: {len(tables)}")
                print(f"📋 Primera tabla: {first_table}")
                print(f"📈 Filas en {first_table}: {row_count}")
                return True
            else:
                print("⚠️  La base de datos no contiene tablas.")
                return False
                
    except Exception as e:
        print("\n❌ Error al conectar a la base de datos")
        print(f"Error: {str(e)}")
        print("\nPor favor verifica que:")
        print("1. PostgreSQL esté en ejecución")
        print("2. Las credenciales en el archivo .env sean correctas")
        print("3. La base de datos exista y sea accesible")
        return False

if __name__ == "__main__":
    test_connection()
    input("\nPresiona Enter para salir...")

from sqlalchemy import create_engine, inspect, text
from database import Database

def check_tables():
    db = Database()
    inspector = inspect(db.engine)
    
    # Method 1: Using SQLAlchemy inspector
    print("Method 1 - Using SQLAlchemy inspector:")
    for table_name in inspector.get_table_names(schema='public'):
        print(f"Table: {table_name}")
    
    # Method 2: Using raw SQL
    print("\nMethod 2 - Using raw SQL query:")
    with db.engine.connect() as conn:
        result = conn.execute(text("""
            SELECT table_schema, table_name 
            FROM information_schema.tables 
            WHERE table_type = 'BASE TABLE'
            ORDER BY table_schema, table_name
        """))
        for row in result:
            print(f"Schema: {row[0]}, Table: {row[1]}")
    
    # Method 3: Check specific table
    print("\nMethod 3 - Check specific table:")
    with db.engine.connect() as conn:
        try:
            conn.execute(text("SELECT 1 FROM public.produccion_galpon LIMIT 1"))
            print("Table public.produccion_galpon exists")
        except Exception as e:
            print(f"Error accessing public.produccion_galpon: {e}")

if __name__ == "__main__":
    check_tables()
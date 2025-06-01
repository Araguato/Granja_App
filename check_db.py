import os
import django
import psycopg2
from django.conf import settings

def check_database():
    # Set up Django environment
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'granja.settings')
    django.setup()
    
    # Get database settings
    db_settings = settings.DATABASES['default']
    
    try:
        # Connect to PostgreSQL
        conn = psycopg2.connect(
            dbname=db_settings['NAME'],
            user=db_settings['USER'],
            password=db_settings['PASSWORD'],
            host=db_settings['HOST'],
            port=db_settings['PORT']
        )
        
        # Create a cursor
        cur = conn.cursor()
        
        # List all tables in the database
        cur.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public'
        """)
        
        tables = cur.fetchall()
        print("\nTables in the database:")
        for table in tables:
            print(f"- {table[0]}")
        
        # Check if produccion_consumoenergia exists
        cur.execute("""
            SELECT EXISTS (
                SELECT FROM information_schema.tables 
                WHERE table_schema = 'public' 
                AND table_name = 'produccion_consumoenergia'
            );
        """)
        
        exists = cur.fetchone()[0]
        print(f"\nDoes produccion_consumoenergia table exist? {'Yes' if exists else 'No'}")
        
        # Close communication with the database
        cur.close()
        conn.close()
        
        return True
        
    except Exception as e:
        print(f"Error connecting to the database: {str(e)}")
        return False

if __name__ == "__main__":
    check_database()

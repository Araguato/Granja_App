import os
import sys
import psycopg2
from psycopg2 import OperationalError, sql
from dotenv import load_dotenv

def test_postgres_connection():
    load_dotenv()

    conn_params = {
        'dbname': os.getenv('DB_NAME', 'DB_Avicola'),
        'user': os.getenv('DB_USER', 'usuario_avicola'),
        'password': os.getenv('DB_PASSWORD', 'Aves2025'),
        'host': os.getenv('DB_HOST', 'localhost'),
        'port': os.getenv('DB_PORT', '5432')
    }

    print("PostgreSQL Connection Diagnostics")
    print("=" * 35)

    print("\nConnection Parameters:")
    for key, value in conn_params.items():
        display_value = '****' if key == 'password' else value
        print(f"  {key}: {display_value}")

    try:
        conn = psycopg2.connect(**conn_params)
        cur = conn.cursor()

        print("\n1. Server Version:")
        cur.execute("SELECT version();")
        version = cur.fetchone()
        print(f"   {version[0]}")

        print("\n2. Existing Databases:")
        cur.execute("SELECT datname FROM pg_database;")
        databases = cur.fetchall()
        for db in databases:
            print(f"   - {db[0]}")

        print(f"\n3. Checking Database '{conn_params['dbname']}'")
        cur.execute(
            sql.SQL("SELECT 1 FROM pg_catalog.pg_database WHERE datname = %s"),
            [conn_params['dbname']]
        )
        db_exists = cur.fetchone()

        if db_exists:
            print(f"   ✅ Database '{conn_params['dbname']}' exists")
            conn.set_isolation_level(0)
            cur.execute("SET search_path TO public")

            print("\n4. Tables in Database:")
            cur.execute("""
                SELECT table_schema, table_name 
                FROM information_schema.tables 
                WHERE table_schema = 'public' 
                ORDER BY table_schema, table_name
            """)
            tables = cur.fetchall()

            if tables:
                for table in tables:
                    print(f"   - {table[1]}")
            else:
                print("   No tables found in the database")
        else:
            print(f"   ❌ Database '{conn_params['dbname']}' does not exist")

        cur.close()
        conn.close()

    except OperationalError as e:
        print("\n❌ Connection Error:")
        print(f"Error Type: {type(e).__name__}")
        print(f"Error Details: {e}")

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
    test_postgres_connection()

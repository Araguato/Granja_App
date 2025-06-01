import psycopg2
import sys

print(f"Python executable: {sys.executable}")
print(f"Python version: {sys.version}")
print(f"Psycopg2 version: {psycopg2.__version__}")

try:
    # Usamos las credenciales hardcodeadas que también están en settings.py
    conn_string = "host='localhost' port='5432' dbname='DB_Avicola' user='usuario_avicola' password='testpassword123'"
    print(f"Intentando conectar con DSN: {conn_string}")
    conn = psycopg2.connect(conn_string)
    print("¡Conexión psycopg2 directa exitosa!")
    
    # Pequeña prueba para obtener la codificación del cliente
    cur = conn.cursor()
    cur.execute("SHOW client_encoding;")
    client_encoding = cur.fetchone()
    print(f"Codificación del cliente reportada por PostgreSQL: {client_encoding}")
    cur.close()
    
    conn.close()
except UnicodeDecodeError as ude:
    print(f"Error de UnicodeDecodeError en psycopg2 directo: {ude}")
    print(f"  Encoding: {ude.encoding}")
    print(f"  Reason: {ude.reason}")
    print(f"  Object: {ude.object}")
    print(f"  Start: {ude.start}")
    print(f"  End: {ude.end}")
except Exception as e:
    print(f"Otro error en psycopg2 directo: {type(e).__name__} - {e}")

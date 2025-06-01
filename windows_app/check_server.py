"""
Script para verificar si el servidor está en funcionamiento
Este script NO usa la biblioteca requests para evitar bloqueos
"""
import socket
import time

def check_server_connection():
    """Verifica si el servidor está respondiendo usando sockets básicos"""
    print("=== Verificando conexión básica al servidor ===")
    
    host = "127.0.0.1"
    port = 8000
    
    print(f"Intentando conectar a {host}:{port}...")
    
    try:
        # Crear socket
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Establecer timeout para evitar bloqueos
        s.settimeout(5)
        # Intentar conectar
        result = s.connect_ex((host, port))
        
        if result == 0:
            print(f"✓ Conexión exitosa a {host}:{port}")
            print("El servidor Django está en funcionamiento")
        else:
            print(f"✗ No se pudo conectar a {host}:{port}")
            print("El servidor Django NO está en funcionamiento")
            print("Por favor, asegúrese de que el servidor Django esté iniciado")
            print("Ejecute 'python manage.py runserver' en el directorio del proyecto Django")
    except Exception as e:
        print(f"✗ Error al verificar conexión: {str(e)}")
    finally:
        # Cerrar socket
        s.close()
    
    print("\n=== Fin de la verificación ===")

if __name__ == "__main__":
    check_server_connection()
    print("\nEste script se cerrará en 5 segundos...")
    time.sleep(5)

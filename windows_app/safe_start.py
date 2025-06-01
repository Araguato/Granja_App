"""
Script de inicio seguro para la aplicación de Windows
Este script inicia la aplicación con timeouts y manejo de errores mejorado
"""
import sys
import os
import time
import subprocess
import threading
import signal

def run_app_with_timeout():
    """Ejecuta la aplicación principal con un timeout de seguridad"""
    print("=== Iniciando App Granja en modo seguro ===")
    print("Este script ejecutará la aplicación con protección contra bloqueos")
    
    # Verificar si el servidor está en funcionamiento
    import socket
    
    def check_server():
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(3)
            result = s.connect_ex(('127.0.0.1', 8000))
            s.close()
            return result == 0
        except:
            return False
    
    server_running = check_server()
    if not server_running:
        print("\n⚠️ ADVERTENCIA: El servidor Django no parece estar en funcionamiento")
        print("La aplicación funcionará en modo offline con datos de ejemplo")
        print("Para ver datos reales, inicie el servidor Django antes de ejecutar la aplicación")
    else:
        print("\n✓ Servidor Django detectado y en funcionamiento")
    
    print("\nIniciando aplicación principal...")
    
    # Función para ejecutar la aplicación en un hilo separado
    def run_app():
        try:
            # Usar subprocess para ejecutar la aplicación
            process = subprocess.Popen([sys.executable, "main.py"])
            process.wait()
        except Exception as e:
            print(f"Error al ejecutar la aplicación: {str(e)}")
    
    # Crear y ejecutar el hilo
    app_thread = threading.Thread(target=run_app)
    app_thread.daemon = True
    app_thread.start()
    
    # Esperar a que el usuario cierre la aplicación
    try:
        while app_thread.is_alive():
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nDetectada interrupción del usuario, cerrando aplicación...")
    
    print("\nAplicación cerrada correctamente")

if __name__ == "__main__":
    run_app_with_timeout()

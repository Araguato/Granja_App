"""
Script simple para diagnosticar problemas básicos
"""
import sys
import os
import json
import time

def check_environment():
    """Verifica el entorno básico sin hacer llamadas a la API"""
    print("=== Diagnóstico básico del entorno ===")
    
    # Verificar Python
    print(f"\nVersión de Python: {sys.version}")
    
    # Verificar directorio actual
    print(f"\nDirectorio actual: {os.getcwd()}")
    
    # Verificar archivos de configuración
    config_file = 'config.json'
    print(f"\nBuscando archivo de configuración: {config_file}")
    if os.path.exists(config_file):
        print(f"✓ Archivo de configuración encontrado")
        try:
            with open(config_file, 'r', encoding='utf-8') as f:
                config = json.load(f)
            print(f"Contenido de configuración: {json.dumps(config, indent=2, ensure_ascii=False)}")
        except Exception as e:
            print(f"✗ Error al leer configuración: {str(e)}")
    else:
        print(f"✗ Archivo de configuración no encontrado")
    
    # Verificar módulos instalados
    print("\nVerificando módulos críticos:")
    modules_to_check = ['PyQt5', 'requests', 'json', 'datetime']
    for module in modules_to_check:
        try:
            __import__(module)
            print(f"✓ Módulo {module} disponible")
        except ImportError:
            print(f"✗ Módulo {module} no disponible")
    
    print("\n=== Fin del diagnóstico básico ===")

if __name__ == "__main__":
    check_environment()
    print("\nEste script se cerrará en 10 segundos...")
    time.sleep(10)

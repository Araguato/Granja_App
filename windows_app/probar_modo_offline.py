"""
Script para probar el modo offline de la aplicación
Este script fuerza el modo offline y verifica que los datos de ejemplo se carguen correctamente
"""
import sys
import os
from api_client import ApiClient

def print_header(title):
    """Imprime un encabezado formateado"""
    print("\n" + "=" * 80)
    print(f" {title} ".center(80, "="))
    print("=" * 80)

def print_section(title):
    """Imprime un título de sección"""
    print("\n" + "-" * 80)
    print(f" {title} ".center(80, "-"))
    print("-" * 80)

def probar_modo_offline():
    """Prueba el modo offline de la aplicación"""
    print_header("PRUEBA DE MODO OFFLINE")
    
    # Crear instancia de ApiClient
    api_client = ApiClient()
    
    # Forzar modo offline
    api_client.is_offline = True
    print("Modo offline forzado: True")
    
    # Probar inicio de sesión offline
    print_section("Prueba de inicio de sesión offline")
    success, user_info = api_client.offline_login("admin", "admin123")
    
    if success:
        print("✓ Inicio de sesión offline exitoso")
        print(f"Información de usuario: {user_info}")
    else:
        print(f"✗ Error en inicio de sesión offline: {user_info}")
    
    # Probar obtención de datos de ejemplo
    endpoints = [
        "galpones", "lotes", "razas", "alimentos", "vacunas", 
        "usuarios", "grupos", "granjas", "empresas", "seguimientos"
    ]
    
    print_section("Prueba de obtención de datos de ejemplo")
    
    for endpoint in endpoints:
        print(f"\nProbando endpoint: {endpoint}")
        success, data = api_client.make_request("get", f"{api_client.base_url}/{endpoint}/")
        
        if isinstance(data, list):
            print(f"✓ Datos obtenidos: {len(data)} elementos")
            if data and len(data) > 0:
                print(f"Primer elemento: {data[0]}")
        else:
            print(f"✗ Error: Los datos no son una lista")
    
    print_header("FIN DE LA PRUEBA")

if __name__ == "__main__":
    probar_modo_offline()

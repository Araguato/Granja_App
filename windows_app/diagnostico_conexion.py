#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Script de diagnóstico para verificar la conectividad con el servidor Django
"""

import requests
import socket
import json
import os
import sys
from urllib.parse import urlparse

def check_server_running(url):
    """Verifica si el servidor está en ejecución"""
    parsed_url = urlparse(url)
    host = parsed_url.hostname
    port = parsed_url.port or (443 if parsed_url.scheme == 'https' else 80)
    
    print(f"Verificando si el servidor está en ejecución en {host}:{port}...")
    
    try:
        # Verificar si el puerto está abierto
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(3)
        result = sock.connect_ex((host, port))
        sock.close()
        
        if result == 0:
            print(f"✓ El puerto {port} está abierto en {host}")
            return True
        else:
            print(f"✗ El puerto {port} está cerrado en {host}")
            return False
    except Exception as e:
        print(f"✗ Error al verificar el puerto: {str(e)}")
        return False

def check_api_endpoints(base_url):
    """Verifica los endpoints de la API"""
    endpoints = [
        "/",
        "/galpones/",
        "/lotes/",
        "/razas/",
        "/alimentos/",
        "/vacunas/",
        "/usuarios/",
        "/grupos/",
        "/granjas/",
        "/empresas/",
        "/seguimientos/",
        "/token/"
    ]
    
    print("\nVerificando endpoints de la API:")
    print("----------------------------------------")
    
    results = {}
    for endpoint in endpoints:
        url = f"{base_url}{endpoint}"
        print(f"Probando: {endpoint}")
        
        try:
            if endpoint == "/token/":
                # Para el endpoint de token, enviar credenciales
                response = requests.post(
                    url,
                    json={"username": "admin", "password": "admin123"},
                    headers={"Content-Type": "application/json"},
                    timeout=10
                )
            else:
                # Para otros endpoints, hacer una solicitud GET
                response = requests.get(url, timeout=10)
            
            status_code = response.status_code
            results[endpoint] = status_code
            
            if status_code in [200, 201, 204]:
                print(f"✓ Endpoint {endpoint} disponible (código {status_code})")
                if status_code != 204 and response.content:
                    try:
                        data = response.json()
                        if isinstance(data, dict) and "results" in data:
                            print(f"  - Contiene {len(data['results'])} resultados")
                        elif isinstance(data, list):
                            print(f"  - Contiene {len(data)} elementos")
                    except:
                        pass
            elif status_code in [401, 403]:
                print(f"! Endpoint {endpoint} requiere autenticación (código {status_code})")
            elif status_code == 404:
                print(f"✗ Endpoint {endpoint} no existe (código {status_code})")
            else:
                print(f"? Endpoint {endpoint} devolvió código {status_code}")
        except requests.exceptions.Timeout:
            results[endpoint] = "Timeout"
            print(f"✗ Timeout al conectar con {endpoint}")
        except requests.exceptions.ConnectionError:
            results[endpoint] = "ConnectionError"
            print(f"✗ Error de conexión al intentar acceder a {endpoint}")
        except Exception as e:
            results[endpoint] = f"Error: {str(e)}"
            print(f"✗ Error al probar endpoint {endpoint}: {str(e)}")
    
    return results

def suggest_solutions(api_url, server_running, endpoint_results):
    """Sugiere soluciones basadas en los resultados del diagnóstico"""
    print("\n=== DIAGNÓSTICO Y SOLUCIONES SUGERIDAS ===")
    
    if not server_running:
        print("\n1. PROBLEMA: El servidor Django no está en ejecución o no es accesible.")
        print("   SOLUCIONES:")
        print("   - Verificar que el servidor Django esté iniciado")
        print("   - Si el servidor está en otra máquina, verificar la conectividad de red")
        print("   - Comprobar si hay un firewall bloqueando la conexión")
        print("   - Si el servidor está en otra dirección, modificar la URL en config.json")
        
        # Sugerir URL alternativa si estamos usando localhost
        parsed_url = urlparse(api_url)
        if parsed_url.hostname in ["localhost", "127.0.0.1"]:
            print("\n   URL alternativas para probar:")
            print(f"   - {api_url.replace('127.0.0.1', 'localhost')}")
            print(f"   - {api_url.replace('127.0.0.1', socket.gethostname())}")
            print(f"   - http://[IP_DEL_SERVIDOR]:8000/api")
    else:
        # Verificar problemas específicos con endpoints
        missing_endpoints = [ep for ep, status in endpoint_results.items() 
                           if status == 404 or status == "ConnectionError"]
        auth_endpoints = [ep for ep, status in endpoint_results.items() 
                        if status in [401, 403]]
        
        if missing_endpoints:
            print("\n2. PROBLEMA: Algunos endpoints no existen en el servidor.")
            print("   ENDPOINTS FALTANTES:", ", ".join(missing_endpoints))
            print("   SOLUCIONES:")
            print("   - Verificar que la versión del servidor Django sea compatible con la aplicación")
            print("   - Revisar la configuración de URLs en el servidor Django")
            
        if auth_endpoints:
            print("\n3. PROBLEMA: Algunos endpoints requieren autenticación.")
            print("   ENDPOINTS CON AUTENTICACIÓN:", ", ".join(auth_endpoints))
            print("   SOLUCIONES:")
            print("   - Verificar que las credenciales en config.json sean correctas")
            print("   - Intentar obtener un token de autenticación manualmente")
    
    # Sugerir configuración alternativa
    print("\n4. CONFIGURACIÓN ALTERNATIVA:")
    print("   Si el servidor está en otra dirección, modifica el archivo config.json:")
    print('   {"is_offline": false, "api_url": "http://[DIRECCIÓN_CORRECTA]/api", "username": "admin", "password": "admin123"}')

def main():
    """Función principal"""
    print("=== DIAGNÓSTICO DE CONEXIÓN CON SERVIDOR DJANGO ===\n")
    
    # Cargar configuración actual
    config_file = "config.json"
    if os.path.exists(config_file):
        try:
            with open(config_file, "r") as f:
                config = json.load(f)
                api_url = config.get("api_url", "http://127.0.0.1:8000/api")
                print(f"URL de la API configurada: {api_url}")
        except Exception as e:
            print(f"Error al leer config.json: {str(e)}")
            api_url = "http://127.0.0.1:8000/api"
            print(f"Usando URL predeterminada: {api_url}")
    else:
        api_url = "http://127.0.0.1:8000/api"
        print(f"Archivo config.json no encontrado. Usando URL predeterminada: {api_url}")
    
    # Verificar si el servidor está en ejecución
    server_running = check_server_running(api_url)
    
    # Si el servidor está en ejecución, verificar endpoints
    endpoint_results = {}
    if server_running:
        endpoint_results = check_api_endpoints(api_url)
    
    # Sugerir soluciones
    suggest_solutions(api_url, server_running, endpoint_results)
    
    print("\n=== DIAGNÓSTICO COMPLETADO ===")

if __name__ == "__main__":
    main()

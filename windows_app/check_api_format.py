"""
Script para verificar el formato de respuesta de la API
"""
import requests
import json
import sys

def check_api_format():
    # Configuración básica
    base_url = "http://127.0.0.1:8000/api"
    
    # Intentar obtener token (sin usar ApiClient para evitar bloqueos)
    print("Intentando obtener token...")
    try:
        login_data = {
            "username": "admin",
            "password": "admin123"
        }
        response = requests.post(f"{base_url}/token/", json=login_data)
        if response.status_code == 200:
            token_data = response.json()
            token = token_data.get('access')
            print(f"✓ Token obtenido: {token[:20]}...")
        else:
            print(f"✗ Error al obtener token: {response.status_code}")
            print(response.text)
            token = None
    except Exception as e:
        print(f"✗ Error de conexión: {str(e)}")
        token = None
    
    if not token:
        print("No se pudo obtener token, usando endpoint sin autenticación...")
    
    # Probar endpoint de galpones
    print("\nProbando endpoint de galpones...")
    headers = {"Authorization": f"Bearer {token}"} if token else {}
    try:
        response = requests.get(f"{base_url}/galpones/", headers=headers)
        print(f"Código de respuesta: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"Tipo de datos recibidos: {type(data)}")
            
            if isinstance(data, dict):
                print("La respuesta es un diccionario")
                print(f"Claves: {list(data.keys())}")
                if 'results' in data:
                    print(f"Número de resultados: {len(data['results'])}")
                    print(f"Primer resultado: {json.dumps(data['results'][0] if data['results'] else {}, indent=2)}")
            elif isinstance(data, list):
                print("La respuesta es una lista")
                print(f"Número de elementos: {len(data)}")
                print(f"Primer elemento: {json.dumps(data[0] if data else {}, indent=2)}")
            else:
                print(f"Tipo de respuesta inesperado: {type(data)}")
        else:
            print(f"Error en la respuesta: {response.text}")
    except Exception as e:
        print(f"Error al acceder al endpoint: {str(e)}")

if __name__ == "__main__":
    print("=== Verificando formato de respuesta de la API ===")
    check_api_format()
    print("\n=== Fin de la verificación ===")
    print("Este script se cerrará en 3 segundos...")
    import time
    time.sleep(3)

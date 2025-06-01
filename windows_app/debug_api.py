"""
Script para diagnosticar problemas de conexión con la API
"""
import sys
import requests
import json
from api_client import ApiClient

def test_api_connection():
    """Prueba la conexión con la API y muestra información detallada"""
    print("=== Diagnóstico de conexión a la API ===")
    
    # Crear cliente API
    api_client = ApiClient()
    
    # Verificar configuración
    print(f"\nConfiguración:")
    print(f"URL base: {api_client.base_url}")
    print(f"Token: {'Configurado' if api_client.token else 'No configurado'}")
    
    # Probar conexión básica
    print("\nProbando conexión básica...")
    try:
        response = requests.get(api_client.base_url)
        print(f"Respuesta: {response.status_code}")
        if response.status_code == 200:
            print("✓ Conexión básica exitosa")
        else:
            print(f"✗ Error de conexión: {response.text}")
    except Exception as e:
        print(f"✗ Error de conexión: {str(e)}")
    
    # Probar autenticación
    print("\nProbando autenticación...")
    success, result = api_client.test_connection()
    if success:
        print("✓ Autenticación exitosa")
    else:
        print(f"✗ Error de autenticación: {result}")
    
    # Probar obtención de galpones
    print("\nProbando obtención de galpones...")
    try:
        success, data = api_client.get_galpones()
        print(f"Éxito: {success}")
        print(f"Tipo de datos: {type(data)}")
        print(f"Contenido: {json.dumps(data, indent=2, ensure_ascii=False)[:500]}...")
    except Exception as e:
        print(f"✗ Error al obtener galpones: {str(e)}")
    
    # Probar obtención de lotes
    print("\nProbando obtención de lotes...")
    try:
        success, data = api_client.get_lotes()
        print(f"Éxito: {success}")
        print(f"Tipo de datos: {type(data)}")
        print(f"Contenido: {json.dumps(data, indent=2, ensure_ascii=False)[:500]}...")
    except Exception as e:
        print(f"✗ Error al obtener lotes: {str(e)}")
    
    print("\n=== Fin del diagnóstico ===")

if __name__ == "__main__":
    test_api_connection()

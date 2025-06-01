"""
Script de diagnóstico avanzado para la API de App_Granja
Este script prueba la comunicación con la API y muestra información detallada
sobre los formatos de respuesta y posibles problemas.
"""
import sys
import os
import json
import requests
import time
from datetime import datetime

# Configuración
API_URL = "http://127.0.0.1:8000/api"
TIMEOUT = 5  # segundos - reducido para evitar bloqueos
CREDENTIALS = {
    "username": "admin",
    "password": "admin123"
}

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

def print_result(success, message):
    """Imprime un resultado formateado"""
    if success:
        print(f"✓ {message}")
    else:
        print(f"✗ {message}")

def test_server_connection():
    """Prueba la conexión básica al servidor"""
    print_section("Prueba de conexión básica al servidor")
    
    try:
        response = requests.get(API_URL, timeout=TIMEOUT)
        print(f"Código de respuesta: {response.status_code}")
        
        if response.status_code == 200:
            print_result(True, "Conexión básica exitosa")
            try:
                data = response.json()
                print(f"Respuesta: {json.dumps(data, indent=2, ensure_ascii=False)}")
            except:
                print(f"Respuesta (texto): {response.text[:500]}")
        else:
            print_result(False, f"Error de conexión: {response.status_code}")
            print(f"Respuesta: {response.text[:500]}")
    except requests.exceptions.Timeout:
        print_result(False, f"Timeout al conectar con {API_URL}")
    except requests.exceptions.ConnectionError:
        print_result(False, f"Error de conexión al intentar acceder a {API_URL}")
    except Exception as e:
        print_result(False, f"Error inesperado: {str(e)}")

def get_auth_token():
    """Obtiene un token de autenticación"""
    print_section("Obtención de token de autenticación")
    
    try:
        response = requests.post(
            f"{API_URL}/token/",
            json=CREDENTIALS,
            timeout=TIMEOUT
        )
        
        print(f"Código de respuesta: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            token = data.get('access')
            refresh = data.get('refresh')
            
            if token:
                print_result(True, "Token obtenido correctamente")
                print(f"Token: {token[:20]}...{token[-20:] if len(token) > 40 else ''}")
                print(f"Refresh Token: {refresh[:20]}...{refresh[-20:] if len(refresh) > 40 else ''}")
                return token
            else:
                print_result(False, "No se pudo extraer el token de la respuesta")
                print(f"Respuesta: {json.dumps(data, indent=2, ensure_ascii=False)}")
                return None
        else:
            print_result(False, f"Error al obtener token: {response.status_code}")
            print(f"Respuesta: {response.text[:500]}")
            return None
    except Exception as e:
        print_result(False, f"Error al obtener token: {str(e)}")
        return None

def test_endpoint(endpoint, token=None):
    """Prueba un endpoint específico de la API"""
    print_section(f"Prueba del endpoint: {endpoint}")
    
    headers = {"Content-Type": "application/json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    
    try:
        print(f"Realizando solicitud GET a {API_URL}/{endpoint}/")
        print(f"Headers: {json.dumps(headers, indent=2)}")
        
        response = requests.get(
            f"{API_URL}/{endpoint}/",
            headers=headers,
            timeout=TIMEOUT
        )
        
        print(f"Código de respuesta: {response.status_code}")
        
        if response.status_code == 200:
            print_result(True, f"Solicitud a {endpoint} exitosa")
            
            try:
                data = response.json()
                print(f"Tipo de respuesta: {type(data).__name__}")
                
                if isinstance(data, dict):
                    print(f"Claves en la respuesta: {list(data.keys())}")
                    
                    if 'results' in data:
                        results = data['results']
                        print(f"'results' es de tipo: {type(results).__name__}")
                        print(f"Número de elementos en 'results': {len(results)}")
                        if results and len(results) > 0:
                            print(f"Primer elemento en 'results': {json.dumps(results[0], indent=2, ensure_ascii=False)}")
                    
                    elif 'data' in data:
                        results = data['data']
                        print(f"'data' es de tipo: {type(results).__name__}")
                        print(f"Número de elementos en 'data': {len(results)}")
                        if results and len(results) > 0:
                            print(f"Primer elemento en 'data': {json.dumps(results[0], indent=2, ensure_ascii=False)}")
                    
                    elif 'id' in data:
                        print("La respuesta parece ser un solo objeto")
                        print(f"Objeto: {json.dumps(data, indent=2, ensure_ascii=False)}")
                    
                    else:
                        print(f"Contenido de la respuesta: {json.dumps(data, indent=2, ensure_ascii=False)[:500]}...")
                
                elif isinstance(data, list):
                    print(f"Número de elementos en la lista: {len(data)}")
                    if data and len(data) > 0:
                        print(f"Primer elemento: {json.dumps(data[0], indent=2, ensure_ascii=False)}")
                
                else:
                    print(f"Contenido de la respuesta: {json.dumps(data, indent=2, ensure_ascii=False)[:500]}...")
            
            except ValueError:
                print("La respuesta no es JSON válido")
                print(f"Respuesta (texto): {response.text[:500]}")
        
        else:
            print_result(False, f"Error en la solicitud a {endpoint}: {response.status_code}")
            print(f"Respuesta: {response.text[:500]}")
    
    except requests.exceptions.Timeout:
        print_result(False, f"Timeout al conectar con {API_URL}/{endpoint}/")
    except requests.exceptions.ConnectionError:
        print_result(False, f"Error de conexión al intentar acceder a {API_URL}/{endpoint}/")
    except Exception as e:
        print_result(False, f"Error inesperado: {str(e)}")

def run_diagnostics():
    """Ejecuta todas las pruebas de diagnóstico"""
    print_header("DIAGNÓSTICO DE LA API DE APP_GRANJA")
    print(f"Fecha y hora: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"URL de la API: {API_URL}")
    
    # Prueba de conexión básica
    test_server_connection()
    
    # Obtener token
    token = get_auth_token()
    
    # Probar endpoints principales
    endpoints = ["galpones", "lotes", "razas", "alimentos", "vacunas"]
    
    for endpoint in endpoints:
        test_endpoint(endpoint, token)
    
    print_header("FIN DEL DIAGNÓSTICO")
    print("Este reporte puede ayudar a identificar problemas de comunicación con la API.")
    print("Revise los resultados para entender mejor qué está fallando.")

if __name__ == "__main__":
    try:
        # Crear archivo de registro
        log_dir = "logs"
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
            
        # Ejecutar diagnóstico con un timeout global
        run_diagnostics()
        
        print("\nDiagnóstico completado. Revise los resultados para identificar problemas.")
    except Exception as e:
        print(f"\nError durante el diagnóstico: {str(e)}")
    # No esperar entrada del usuario para evitar bloqueos
    
    log_file = os.path.join(log_dir, f"api_diagnostico_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log")
    
    # Redirigir salida a archivo y consola
    class Tee:
        def __init__(self, *files):
            self.files = files
        def write(self, obj):
            for f in self.files:
                f.write(obj)
                f.flush()
        def flush(self):
            for f in self.files:
                f.flush()
    
    with open(log_file, 'w', encoding='utf-8') as log:
        original_stdout = sys.stdout
        sys.stdout = Tee(sys.stdout, log)
        
        try:
            run_diagnostics()
            print(f"\nLog guardado en: {log_file}")
        except Exception as e:
            print(f"\nError durante el diagnóstico: {str(e)}")
        finally:
            sys.stdout = original_stdout
    
    print(f"\nDiagnóstico completado. Log guardado en: {log_file}")
    print("Presione Enter para salir...")
    input()

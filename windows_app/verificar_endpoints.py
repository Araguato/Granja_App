"""
Script para verificar qué endpoints están disponibles en la API de Django
"""
import requests
import json

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

def verificar_endpoints():
    """Verifica qué endpoints están disponibles en la API"""
    print_header("VERIFICACIÓN DE ENDPOINTS DISPONIBLES")
    
    # URL base de la API
    base_url = "http://127.0.0.1:8000/api"
    
    # Intentar obtener la lista de endpoints disponibles
    try:
        print(f"Consultando {base_url}...")
        response = requests.get(base_url, timeout=5)
        
        if response.status_code == 200:
            print("✓ Conexión exitosa a la API")
            
            try:
                # Intentar parsear la respuesta como JSON
                data = response.json()
                print("\nEndpoints disponibles:")
                for key, value in data.items():
                    print(f"- {key}: {value}")
            except:
                print("La respuesta no es JSON. Contenido:")
                print(response.text[:500])
        else:
            print(f"✗ Error al conectar a la API: {response.status_code}")
            print(response.text[:500])
    except Exception as e:
        print(f"✗ Error: {str(e)}")
    
    # Lista de endpoints comunes para probar
    endpoints = [
        "usuarios", "granjas", "galpones", "lotes", "razas", 
        "alimentos", "vacunas", "seguimientos", "empresas"
    ]
    
    print_section("VERIFICACIÓN DE ENDPOINTS ESPECÍFICOS")
    
    for endpoint in endpoints:
        url = f"{base_url}/{endpoint}/"
        try:
            print(f"Consultando {url}...")
            response = requests.get(url, timeout=5)
            
            if response.status_code == 200:
                print(f"✓ {endpoint}: Disponible")
                try:
                    data = response.json()
                    if isinstance(data, dict) and 'results' in data:
                        print(f"  - Formato: Diccionario con 'results' ({len(data['results'])} elementos)")
                    elif isinstance(data, list):
                        print(f"  - Formato: Lista ({len(data)} elementos)")
                    else:
                        print(f"  - Formato: {type(data).__name__}")
                except:
                    print("  - No es JSON válido")
            else:
                print(f"✗ {endpoint}: No disponible ({response.status_code})")
        except Exception as e:
            print(f"✗ {endpoint}: Error - {str(e)}")
    
    print_header("FIN DE LA VERIFICACIÓN")

if __name__ == "__main__":
    verificar_endpoints()

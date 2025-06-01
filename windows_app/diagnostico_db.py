"""
Script de diagnóstico para la conexión a la base de datos de App_Granja
Este script prueba la conexión directa a la base de datos y muestra información detallada
sobre posibles problemas.
"""
import os
import sys
import json
import time
from datetime import datetime

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

def test_django_db_connection():
    """Prueba la conexión a la base de datos Django"""
    print_section("Prueba de conexión a la base de datos Django")
    
    try:
        # Intentar importar Django y configurar el entorno
        print("Intentando importar Django...")
        
        # Agregar el directorio del proyecto Django al path
        django_project_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
        if django_project_dir not in sys.path:
            sys.path.append(django_project_dir)
        
        # Configurar el entorno Django
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'granja.settings')
        
        try:
            import django
            django.setup()
            print_result(True, "Django importado correctamente")
        except Exception as e:
            print_result(False, f"Error al importar Django: {str(e)}")
            return
        
        # Intentar conectar a la base de datos
        try:
            from django.db import connections
            from django.db.utils import OperationalError
            
            print("Intentando conectar a la base de datos...")
            
            # Obtener la conexión default
            conn = connections['default']
            
            try:
                # Intentar ejecutar una consulta simple
                cursor = conn.cursor()
                cursor.execute("SELECT 1")
                result = cursor.fetchone()
                
                if result and result[0] == 1:
                    print_result(True, "Conexión a la base de datos exitosa")
                    
                    # Mostrar información de la base de datos
                    from django.conf import settings
                    db_settings = settings.DATABASES['default']
                    
                    print("\nInformación de la base de datos:")
                    print(f"Engine: {db_settings['ENGINE']}")
                    print(f"Name: {db_settings['NAME']}")
                    
                    if 'postgresql' in db_settings['ENGINE']:
                        print(f"Host: {db_settings.get('HOST', 'localhost')}")
                        print(f"Port: {db_settings.get('PORT', '5432')}")
                        print(f"User: {db_settings.get('USER', '')}")
                    
                    # Listar tablas
                    print("\nListando tablas en la base de datos:")
                    if 'sqlite' in db_settings['ENGINE']:
                        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
                    elif 'postgresql' in db_settings['ENGINE']:
                        cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public';")
                    else:
                        print("No se puede listar tablas para este motor de base de datos")
                        return
                    
                    tables = cursor.fetchall()
                    for table in tables:
                        print(f"- {table[0]}")
                else:
                    print_result(False, "Error al ejecutar consulta de prueba")
            except OperationalError as e:
                print_result(False, f"Error operacional al conectar a la base de datos: {str(e)}")
            except Exception as e:
                print_result(False, f"Error al ejecutar consulta: {str(e)}")
        except Exception as e:
            print_result(False, f"Error al configurar conexión a la base de datos: {str(e)}")
    except Exception as e:
        print_result(False, f"Error general: {str(e)}")

def test_api_db_connection():
    """Prueba la conexión a la base de datos a través de la API"""
    print_section("Prueba de conexión a la base de datos a través de la API")
    
    try:
        import requests
        
        # Configuración
        api_url = "http://127.0.0.1:8000/api"
        timeout = 5  # segundos
        
        # Probar conexión básica a la API
        print("Probando conexión básica a la API...")
        try:
            response = requests.get(api_url, timeout=timeout)
            print(f"Código de respuesta: {response.status_code}")
            
            if response.status_code == 200:
                print_result(True, "Conexión a la API exitosa")
                
                # Probar endpoint de estado de la base de datos
                # Este endpoint debe ser implementado en el backend de Django
                print("\nProbando endpoint de estado de la base de datos...")
                try:
                    response = requests.get(f"{api_url}/status/", timeout=timeout)
                    print(f"Código de respuesta: {response.status_code}")
                    
                    if response.status_code == 200:
                        try:
                            data = response.json()
                            print(f"Respuesta: {json.dumps(data, indent=2, ensure_ascii=False)}")
                            
                            if data.get('database_status') == 'connected':
                                print_result(True, "Base de datos conectada según la API")
                            else:
                                print_result(False, f"Estado de la base de datos: {data.get('database_status', 'desconocido')}")
                        except:
                            print(f"Respuesta (texto): {response.text[:500]}")
                    else:
                        print_result(False, f"Error al consultar estado de la base de datos: {response.status_code}")
                        print(f"Respuesta: {response.text[:500]}")
                except Exception as e:
                    print_result(False, f"Error al consultar endpoint de estado: {str(e)}")
                
                # Probar endpoint que requiere acceso a la base de datos
                print("\nProbando endpoint que requiere acceso a la base de datos...")
                try:
                    response = requests.get(f"{api_url}/galpones/", timeout=timeout)
                    print(f"Código de respuesta: {response.status_code}")
                    
                    if response.status_code == 200:
                        try:
                            data = response.json()
                            print_result(True, "Endpoint de galpones responde correctamente")
                            print(f"Tipo de respuesta: {type(data).__name__}")
                            
                            if isinstance(data, dict) and 'results' in data:
                                print(f"Número de galpones: {len(data['results'])}")
                            elif isinstance(data, list):
                                print(f"Número de galpones: {len(data)}")
                        except:
                            print(f"Respuesta (texto): {response.text[:500]}")
                    else:
                        print_result(False, f"Error al consultar galpones: {response.status_code}")
                        print(f"Respuesta: {response.text[:500]}")
                except Exception as e:
                    print_result(False, f"Error al consultar endpoint de galpones: {str(e)}")
            else:
                print_result(False, f"Error de conexión a la API: {response.status_code}")
                print(f"Respuesta: {response.text[:500]}")
        except requests.exceptions.Timeout:
            print_result(False, f"Timeout al conectar con {api_url}")
        except requests.exceptions.ConnectionError:
            print_result(False, f"Error de conexión al intentar acceder a {api_url}")
        except Exception as e:
            print_result(False, f"Error inesperado: {str(e)}")
    except Exception as e:
        print_result(False, f"Error general: {str(e)}")

def run_diagnostics():
    """Ejecuta todas las pruebas de diagnóstico"""
    print_header("DIAGNÓSTICO DE CONEXIÓN A LA BASE DE DATOS DE APP_GRANJA")
    print(f"Fecha y hora: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Prueba de conexión directa a la base de datos
    test_django_db_connection()
    
    # Prueba de conexión a través de la API
    test_api_db_connection()
    
    print_header("FIN DEL DIAGNÓSTICO")
    print("Este reporte puede ayudar a identificar problemas de conexión con la base de datos.")
    print("Revise los resultados para entender mejor qué está fallando.")

if __name__ == "__main__":
    try:
        # Ejecutar diagnóstico
        run_diagnostics()
        
        print("\nDiagnóstico completado. Revise los resultados para identificar problemas.")
    except Exception as e:
        print(f"\nError durante el diagnóstico: {str(e)}")

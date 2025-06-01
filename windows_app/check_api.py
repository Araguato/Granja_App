#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import json
import os
import sys

def load_config():
    """Carga la configuración desde el archivo config.json"""
    config_path = os.path.join(os.path.dirname(__file__), 'config.json')
    try:
        if os.path.exists(config_path):
            with open(config_path, 'r') as f:
                return json.load(f)
        else:
            # Configuración por defecto
            config = {
                'api_url': 'http://127.0.0.1:8000/api',
                'token': '',
                'username': 'admin',
                'password': 'admin123'
            }
            # Guardar configuración por defecto
            with open(config_path, 'w') as f:
                json.dump(config, f, indent=4)
            return config
    except Exception as e:
        print(f"Error al cargar configuración: {str(e)}")
        return {
            'api_url': 'http://127.0.0.1:8000/api',
            'token': '',
            'username': 'admin',
            'password': 'admin123'
        }

def test_connection(config):
    """Prueba la conexión básica con el servidor Django"""
    try:
        # Obtener la URL base sin /api
        base_url = config['api_url'].split('/api')[0]
        print(f"Intentando conectar a: {base_url}")
        
        # Intentar obtener la página principal de Django
        response = requests.get(
            base_url,
            timeout=10
        )
        
        print(f"Respuesta del servidor: {response.status_code}")
        
        if response.status_code == 200:
            print(f"✅ Conexión exitosa al servidor Django en {base_url}")
            return True
        else:
            print(f"❌ No se pudo conectar al servidor Django. Código: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error al conectar con el servidor: {str(e)}")
        return False

def test_api(config):
    """Prueba la conexión con la API de Django"""
    try:
        api_url = config['api_url']
        print(f"Intentando conectar a la API: {api_url}")
        
        # Intentar obtener la raíz de la API
        response = requests.get(
            api_url,
            timeout=10
        )
        
        print(f"Respuesta de la API: {response.status_code}")
        
        if response.status_code == 200:
            try:
                data = response.json()
                print(f"✅ Conexión exitosa a la API. Endpoints disponibles:")
                for key, value in data.items():
                    print(f"  - {key}: {value}")
                return True
            except Exception as e:
                print(f"⚠️ Se pudo acceder a la API pero hubo un error al procesar la respuesta: {str(e)}")
                return False
        else:
            print(f"❌ No se pudo acceder a la API. Código: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error al conectar con la API: {str(e)}")
        return False

def test_auth(config):
    """Prueba la autenticación con la API de Django"""
    try:
        api_url = config['api_url']
        username = config['username']
        password = config['password']
        
        print(f"Intentando autenticar en: {api_url}/token/")
        
        # Intentar obtener un token JWT
        response = requests.post(
            f"{api_url}/token/",
            json={'username': username, 'password': password},
            headers={'Content-Type': 'application/json'},
            timeout=10
        )
        
        print(f"Respuesta de autenticación: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            token = data.get('access', '')
            refresh = data.get('refresh', '')
            
            # Guardar el token en la configuración
            config['token'] = token
            config['refresh_token'] = refresh
            with open(os.path.join(os.path.dirname(__file__), 'config.json'), 'w') as f:
                json.dump(config, f, indent=4)
            
            print(f"✅ Autenticación exitosa con el usuario {username}")
            
            # Probar el token obtenido
            return test_token(config, token)
        else:
            print(f"❌ No se pudo autenticar. Código: {response.status_code}")
            print(f"Respuesta: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Error al intentar autenticar: {str(e)}")
        return False

def test_token(config, token):
    """Prueba el token obtenido haciendo una petición a un endpoint protegido"""
    try:
        api_url = config['api_url']
        
        # Intentar obtener la lista de usuarios (endpoint protegido)
        print(f"Probando token en: {api_url}/usuarios/")
        response = requests.get(
            f"{api_url}/usuarios/",
            headers={'Authorization': f'Bearer {token}'},
            timeout=10
        )
        
        print(f"Respuesta con token: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ El token es válido y se pudo acceder a un endpoint protegido.")
            print(f"Usuarios: {json.dumps(data, indent=2)}")
            return True
        else:
            print(f"❌ El token no es válido o no tiene permisos. Código: {response.status_code}")
            print(f"Respuesta: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Error al probar el token: {str(e)}")
        return False

def test_endpoints(config):
    """Prueba los endpoints específicos de la API"""
    token = config.get('token', '')
    if not token:
        print("⚠️ No hay token disponible. Ejecute primero la prueba de autenticación.")
        return False
    
    api_url = config['api_url']
    headers = {'Authorization': f'Bearer {token}'}
    
    # Lista de endpoints a probar
    endpoints = [
        '/granjas/',
        '/galpones/',
        '/lotes/',
        '/razas/',
        '/alimentos/',
        '/vacunas/',
        '/seguimientos/',
        '/tareas/'
    ]
    
    print("\n=== Probando endpoints específicos ===")
    
    for endpoint in endpoints:
        try:
            full_url = f"{api_url}{endpoint}"
            print(f"Probando endpoint: {full_url}")
            
            response = requests.get(
                full_url,
                headers=headers,
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                count = len(data) if isinstance(data, list) else "N/A"
                print(f"✅ Endpoint {endpoint}: OK (Código: {response.status_code}, Items: {count})")
            else:
                print(f"❌ Endpoint {endpoint}: Error (Código: {response.status_code})")
                print(f"   Respuesta: {response.text}")
        except Exception as e:
            print(f"❌ Error al probar endpoint {endpoint}: {str(e)}")
    
    return True

if __name__ == "__main__":
    print("=== Test de Conexión a Django API ===")
    config = load_config()
    
    print("\n1. Probando conexión básica...")
    conn_ok = test_connection(config)
    
    print("\n2. Probando API...")
    api_ok = test_api(config)
    
    print("\n3. Probando autenticación...")
    auth_ok = test_auth(config)
    
    if auth_ok:
        print("\n4. Probando endpoints específicos...")
        test_endpoints(config)
    
    print("\n=== Resumen ===")
    print(f"Conexión básica: {'✅ OK' if conn_ok else '❌ Error'}")
    print(f"API: {'✅ OK' if api_ok else '❌ Error'}")
    print(f"Autenticación: {'✅ OK' if auth_ok else '❌ Error'}")
    
    if conn_ok and api_ok and auth_ok:
        print("\n✅ Todas las pruebas pasaron correctamente.")
    else:
        print("\n⚠️ Algunas pruebas fallaron. Revise los mensajes anteriores para más detalles.")

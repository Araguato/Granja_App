#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Script de diagnóstico para verificar la funcionalidad de obtención de usuarios
en modo offline en la aplicación App_Granja.
"""

import sys
import json
import os
from api_client import ApiClient

def main():
    """Función principal del script de diagnóstico"""
    print("=== DIAGNÓSTICO DE USUARIOS EN MODO OFFLINE ===")
    
    # Crear una instancia de ApiClient
    api_client = ApiClient()
    
    # Activar modo offline manualmente
    api_client.is_offline = True
    print("Modo offline activado manualmente en el cliente")
    
    # Verificar si el archivo config.json existe
    if os.path.exists('config.json'):
        print("\n[✓] Archivo config.json encontrado")
        try:
            with open('config.json', 'r') as f:
                config = json.load(f)
                print(f"Configuración: {json.dumps(config, indent=2)}")
                
            # Verificar si el modo offline está activado en la configuración
            if config.get('is_offline'):
                print("[✓] Modo offline activado en config.json")
            else:
                print("[!] Modo offline NO está activado en config.json")
                # Actualizar config.json para activar modo offline
                config['is_offline'] = True
                with open('config.json', 'w') as f:
                    json.dump(config, f, indent=2)
                print("    Activado modo offline en config.json")
        except Exception as e:
            print(f"[!] Error al leer config.json: {str(e)}")
    else:
        print("\n[!] Archivo config.json no encontrado")
        print("    Creando archivo config.json con modo offline activado")
        with open('config.json', 'w') as f:
            json.dump({"is_offline": True, "api_url": "http://127.0.0.1:8000/api"}, f, indent=2)
    
    # Verificar datos de ejemplo disponibles
    print("\n=== VERIFICANDO DATOS DE EJEMPLO ===")
    example_data_types = [
        'empresas', 'granjas', 'galpones', 'lotes', 'razas', 
        'alimentos', 'vacunas', 'usuarios', 'grupos', 'seguimientos'
    ]
    
    for data_type in example_data_types:
        example_data = api_client.get_example_data(data_type)
        if example_data:
            print(f"[✓] Datos de ejemplo para '{data_type}' disponibles: {len(example_data)} elementos")
        else:
            print(f"[!] No hay datos de ejemplo para '{data_type}'")
    
    # Probar obtención de usuarios en modo offline
    print("\n=== PROBANDO OBTENCIÓN DE USUARIOS ===")
    success, usuarios = api_client.get_usuarios()
    
    if success:
        print(f"[✓] Obtención de usuarios exitosa: {len(usuarios)} usuarios")
        print("\nPrimeros 3 usuarios:")
        for i, usuario in enumerate(usuarios[:3]):
            print(f"\nUsuario {i+1}:")
            for key, value in usuario.items():
                print(f"  {key}: {value}")
    else:
        print(f"[!] Error al obtener usuarios: {usuarios}")
        
        # Verificar método make_request directamente
        print("\n=== VERIFICANDO MÉTODO MAKE_REQUEST ===")
        success, data = api_client.make_request('get', f"{api_client.base_url}/usuarios/")
        print(f"Resultado de make_request: success={success}, data_length={len(data) if isinstance(data, list) else 'no es lista'}")
        
        # Verificar datos de ejemplo de usuarios directamente
        print("\n=== VERIFICANDO DATOS DE EJEMPLO DE USUARIOS DIRECTAMENTE ===")
        usuarios_ejemplo = api_client.get_example_data('usuarios')
        print(f"Datos de ejemplo de usuarios: {len(usuarios_ejemplo) if isinstance(usuarios_ejemplo, list) else 'no es lista'}")
        if isinstance(usuarios_ejemplo, list) and len(usuarios_ejemplo) > 0:
            print("Primer usuario de ejemplo:")
            for key, value in usuarios_ejemplo[0].items():
                print(f"  {key}: {value}")
    
    print("\n=== DIAGNÓSTICO COMPLETADO ===")

if __name__ == "__main__":
    main()

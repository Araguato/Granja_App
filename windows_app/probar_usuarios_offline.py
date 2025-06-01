#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Script para probar específicamente la funcionalidad de usuarios en modo offline
"""

import json
import os
from api_client import ApiClient

def main():
    print("=== PRUEBA DE USUARIOS EN MODO OFFLINE ===\n")
    
    # Crear instancia de ApiClient
    api = ApiClient()
    
    # Forzar modo offline
    api.is_offline = True
    print("Modo offline activado")
    
    # Guardar configuración con modo offline activado
    config = {
        "is_offline": True,
        "api_url": "http://127.0.0.1:8000/api",
        "username": "admin",
        "password": "admin123"
    }
    
    with open('config.json', 'w') as f:
        json.dump(config, f, indent=2)
    print("Archivo config.json actualizado con modo offline\n")
    
    # Probar get_example_data directamente
    print("Obteniendo datos de ejemplo para usuarios directamente:")
    usuarios_ejemplo = api.get_example_data('usuarios')
    print(f"Número de usuarios de ejemplo: {len(usuarios_ejemplo)}")
    
    if usuarios_ejemplo:
        print("\nPrimer usuario de ejemplo:")
        for key, value in usuarios_ejemplo[0].items():
            print(f"  {key}: {value}")
    else:
        print("No se encontraron datos de ejemplo para usuarios")
    
    # Probar get_usuarios
    print("\nProbando método get_usuarios:")
    success, usuarios = api.get_usuarios()
    
    print(f"Resultado: success={success}, usuarios={len(usuarios) if isinstance(usuarios, list) else 'no es lista'}")
    
    if success and isinstance(usuarios, list) and usuarios:
        print("\nPrimer usuario obtenido:")
        for key, value in usuarios[0].items():
            print(f"  {key}: {value}")
    
    print("\n=== PRUEBA COMPLETADA ===")

if __name__ == "__main__":
    main()

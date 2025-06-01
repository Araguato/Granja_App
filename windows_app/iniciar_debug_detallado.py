#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Script de inicio con depuración detallada para App_Granja
"""

import sys
import os
import json
import traceback
import importlib.util

# Configurar para mostrar todos los errores
sys.tracebacklimit = None

def print_header(text):
    print("\n" + "=" * 60)
    print(" " + text)
    print("=" * 60 + "\n")

def crear_config():
    """Crea un archivo de configuración limpio"""
    print_header("CREANDO ARCHIVO DE CONFIGURACIÓN")
    
    config = {
        "is_offline": True,
        "api_url": "http://127.0.0.1:8000/api",
        "username": "admin",
        "password": "admin123"
    }
    
    try:
        with open("config.json", "w") as f:
            json.dump(config, f, indent=2)
        print("✓ Archivo config.json creado correctamente")
    except Exception as e:
        print(f"✗ Error al crear config.json: {str(e)}")
        traceback.print_exc()

def cargar_modulo_seguro(nombre_modulo, ruta_archivo):
    """Carga un módulo de forma segura, mostrando errores detallados"""
    print(f"Intentando cargar {nombre_modulo} desde {ruta_archivo}...")
    
    try:
        spec = importlib.util.spec_from_file_location(nombre_modulo, ruta_archivo)
        modulo = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(modulo)
        print(f"✓ Módulo {nombre_modulo} cargado correctamente")
        return modulo
    except Exception as e:
        print(f"✗ Error al cargar {nombre_modulo}: {str(e)}")
        traceback.print_exc()
        return None

def iniciar_aplicacion_segura():
    """Intenta iniciar la aplicación de forma segura, capturando y mostrando todos los errores"""
    print_header("INICIANDO APLICACIÓN DE FORMA SEGURA")
    
    # Modificar sys.argv para forzar modo offline
    sys.argv = [sys.argv[0], "--offline", "--debug"]
    
    try:
        # Primero, intentar importar los módulos principales uno por uno
        print("Importando módulos principales...")
        
        # Importar api_client.py
        api_client_path = os.path.join(os.path.dirname(__file__), "api_client.py")
        api_client_module = cargar_modulo_seguro("api_client", api_client_path)
        
        if api_client_module is None:
            print("No se pudo cargar api_client.py, no se puede continuar")
            return
        
        # Importar sync_manager.py
        sync_manager_path = os.path.join(os.path.dirname(__file__), "sync_manager.py")
        sync_manager_module = cargar_modulo_seguro("sync_manager", sync_manager_path)
        
        # Importar main.py
        main_path = os.path.join(os.path.dirname(__file__), "main.py")
        main_module = cargar_modulo_seguro("main", main_path)
        
        if main_module is None:
            print("No se pudo cargar main.py, no se puede continuar")
            return
        
        # Intentar ejecutar la función main
        print("\nEjecutando función main...")
        try:
            main_module.main()
            print("✓ Aplicación cerrada correctamente")
        except Exception as e:
            print(f"✗ Error al ejecutar main(): {str(e)}")
            traceback.print_exc()
    
    except Exception as e:
        print(f"✗ Error general: {str(e)}")
        traceback.print_exc()

def main():
    print_header("INICIO DE APP_GRANJA CON DEPURACIÓN DETALLADA")
    
    # Crear archivo de configuración limpio
    crear_config()
    
    # Iniciar aplicación de forma segura
    iniciar_aplicacion_segura()
    
    print_header("DEPURACIÓN COMPLETADA")
    input("Presione Enter para salir...")

if __name__ == "__main__":
    main()

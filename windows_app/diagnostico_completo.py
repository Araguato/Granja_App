#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Script de diagnóstico completo para la aplicación App_Granja
"""

import os
import sys
import json
import subprocess
import traceback
from pathlib import Path

# Colores para la consola
class Colors:
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BLUE = '\033[94m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

def print_header(text):
    print(f"\n{Colors.BLUE}{Colors.BOLD}{'=' * 60}{Colors.ENDC}")
    print(f"{Colors.BLUE}{Colors.BOLD} {text}{Colors.ENDC}")
    print(f"{Colors.BLUE}{Colors.BOLD}{'=' * 60}{Colors.ENDC}\n")

def print_success(text):
    print(f"{Colors.GREEN}✓ {text}{Colors.ENDC}")

def print_warning(text):
    print(f"{Colors.YELLOW}⚠ {text}{Colors.ENDC}")

def print_error(text):
    print(f"{Colors.RED}✗ {text}{Colors.ENDC}")

def print_info(text):
    print(f"{Colors.BLUE}ℹ {text}{Colors.ENDC}")

def check_python():
    print_header("VERIFICANDO PYTHON")
    try:
        version = sys.version.split()[0]
        print_success(f"Python {version} instalado correctamente")
        return True
    except Exception as e:
        print_error(f"Error al verificar Python: {str(e)}")
        return False

def check_dependencies():
    print_header("VERIFICANDO DEPENDENCIAS")
    required_packages = [
        "PyQt5", "PyQtChart", "pandas", "matplotlib", 
        "requests", "qrcode", "pillow"
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
            print_success(f"Paquete {package} instalado correctamente")
        except ImportError:
            print_error(f"Paquete {package} no encontrado")
            missing_packages.append(package)
    
    if missing_packages:
        print_warning(f"Faltan los siguientes paquetes: {', '.join(missing_packages)}")
        
        install = input("¿Desea instalar los paquetes faltantes? (s/n): ")
        if install.lower() == 's':
            try:
                for package in missing_packages:
                    print_info(f"Instalando {package}...")
                    subprocess.check_call([sys.executable, "-m", "pip", "install", package])
                    print_success(f"Paquete {package} instalado correctamente")
                return True
            except Exception as e:
                print_error(f"Error al instalar paquetes: {str(e)}")
                return False
        else:
            return False
    
    return True

def check_main_files():
    print_header("VERIFICANDO ARCHIVOS PRINCIPALES")
    
    # Verificar que estamos en el directorio correcto
    current_dir = os.path.abspath(os.path.dirname(__file__))
    print_info(f"Directorio actual: {current_dir}")
    
    # Archivos principales que deben existir
    main_files = ["main.py", "api_client.py", "sync_manager.py", "config.json"]
    
    all_files_exist = True
    
    for file in main_files:
        file_path = os.path.join(current_dir, file)
        if os.path.isfile(file_path):
            print_success(f"Archivo {file} encontrado")
        else:
            print_error(f"Archivo {file} no encontrado")
            all_files_exist = False
    
    return all_files_exist

def check_config_file():
    print_header("VERIFICANDO ARCHIVO DE CONFIGURACIÓN")
    
    config_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), "config.json")
    
    if not os.path.isfile(config_path):
        print_error(f"Archivo config.json no encontrado")
        create_config = input("¿Desea crear un archivo de configuración nuevo? (s/n): ")
        if create_config.lower() == 's':
            create_new_config(config_path)
            return True
        else:
            return False
    
    try:
        with open(config_path, "r") as f:
            config = json.load(f)
            print_success(f"Archivo config.json válido")
            print_info(f"Configuración actual: {json.dumps(config, indent=2)}")
            
            # Verificar si la configuración tiene los campos necesarios
            required_fields = ["is_offline", "api_url"]
            missing_fields = [field for field in required_fields if field not in config]
            
            if missing_fields:
                print_warning(f"Faltan los siguientes campos en la configuración: {', '.join(missing_fields)}")
                update_config = input("¿Desea actualizar el archivo de configuración? (s/n): ")
                if update_config.lower() == 's':
                    create_new_config(config_path)
                    return True
                else:
                    return False
            
            return True
    except json.JSONDecodeError:
        print_error(f"Archivo config.json inválido (JSON malformado)")
        fix_config = input("¿Desea reparar el archivo de configuración? (s/n): ")
        if fix_config.lower() == 's':
            create_new_config(config_path)
            return True
        else:
            return False
    except Exception as e:
        print_error(f"Error al leer config.json: {str(e)}")
        return False

def create_new_config(config_path):
    print_info("Creando nuevo archivo de configuración...")
    
    # Preguntar por el modo offline
    offline_mode = input("¿Desea iniciar en modo offline? (s/n): ").lower() == 's'
    
    # Preguntar por la URL de la API
    api_url = input("Ingrese la URL de la API (por defecto: http://127.0.0.1:8000/api): ")
    if not api_url:
        api_url = "http://127.0.0.1:8000/api"
    
    # Crear configuración
    config = {
        "is_offline": offline_mode,
        "api_url": api_url,
        "username": "",
        "password": ""
    }
    
    try:
        with open(config_path, "w") as f:
            json.dump(config, f, indent=2)
        print_success(f"Archivo config.json creado correctamente")
        return True
    except Exception as e:
        print_error(f"Error al crear config.json: {str(e)}")
        return False

def check_django_server():
    print_header("VERIFICANDO SERVIDOR DJANGO")
    
    # Obtener la URL de la API del archivo de configuración
    config_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), "config.json")
    
    try:
        with open(config_path, "r") as f:
            config = json.load(f)
            api_url = config.get("api_url", "http://127.0.0.1:8000/api")
    except:
        api_url = "http://127.0.0.1:8000/api"
    
    # Extraer la base URL (sin /api)
    base_url = api_url.rsplit("/api", 1)[0]
    
    print_info(f"Verificando conexión con el servidor Django en {base_url}...")
    
    try:
        import requests
        response = requests.get(base_url, timeout=5)
        
        if response.status_code == 200:
            print_success(f"Servidor Django accesible en {base_url}")
            return True
        else:
            print_warning(f"Servidor Django responde con código {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print_error(f"No se pudo conectar con el servidor Django en {base_url}")
        
        start_server = input("¿Desea iniciar el servidor Django? (s/n): ")
        if start_server.lower() == 's':
            try:
                # Buscar el archivo manage.py
                manage_py = None
                
                # Buscar en el directorio actual y en el directorio padre
                current_dir = os.path.abspath(os.path.dirname(__file__))
                parent_dir = os.path.dirname(current_dir)
                
                if os.path.isfile(os.path.join(current_dir, "manage.py")):
                    manage_py = os.path.join(current_dir, "manage.py")
                elif os.path.isfile(os.path.join(parent_dir, "manage.py")):
                    manage_py = os.path.join(parent_dir, "manage.py")
                
                if manage_py:
                    print_info(f"Iniciando servidor Django desde {manage_py}...")
                    
                    # Iniciar el servidor Django en un proceso separado
                    django_process = subprocess.Popen(
                        [sys.executable, manage_py, "runserver", "0.0.0.0:8000"],
                        cwd=os.path.dirname(manage_py)
                    )
                    
                    print_success(f"Servidor Django iniciado en proceso {django_process.pid}")
                    print_warning(f"El servidor Django se detendrá cuando cierre este script")
                    
                    return True
                else:
                    print_error(f"No se encontró el archivo manage.py")
                    return False
            except Exception as e:
                print_error(f"Error al iniciar el servidor Django: {str(e)}")
                return False
        else:
            print_info("Continuando en modo offline...")
            
            # Actualizar config.json para modo offline
            try:
                with open(config_path, "r") as f:
                    config = json.load(f)
                
                config["is_offline"] = True
                
                with open(config_path, "w") as f:
                    json.dump(config, f, indent=2)
                
                print_success("Modo offline activado en config.json")
            except:
                print_error("No se pudo actualizar config.json para modo offline")
            
            return False
    except Exception as e:
        print_error(f"Error al verificar el servidor Django: {str(e)}")
        return False

def start_application():
    print_header("INICIANDO APLICACIÓN")
    
    try:
        print_info("Iniciando aplicación...")
        
        # Obtener el directorio actual
        current_dir = os.path.abspath(os.path.dirname(__file__))
        
        # Iniciar la aplicación
        subprocess.call([sys.executable, os.path.join(current_dir, "main.py")])
        
        print_success("Aplicación cerrada correctamente")
        return True
    except Exception as e:
        print_error(f"Error al iniciar la aplicación: {str(e)}")
        traceback.print_exc()
        return False

def main():
    print_header("DIAGNÓSTICO COMPLETO DE APP_GRANJA")
    
    # Verificar Python
    if not check_python():
        print_error("Se requiere Python para ejecutar la aplicación")
        return
    
    # Verificar dependencias
    if not check_dependencies():
        print_warning("Faltan dependencias necesarias para la aplicación")
    
    # Verificar archivos principales
    if not check_main_files():
        print_error("Faltan archivos principales de la aplicación")
        return
    
    # Verificar archivo de configuración
    if not check_config_file():
        print_warning("Problemas con el archivo de configuración")
    
    # Verificar servidor Django
    django_running = check_django_server()
    
    # Iniciar la aplicación
    start_application()

if __name__ == "__main__":
    main()

#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Script de diagnóstico básico para identificar problemas con la aplicación
"""

import sys
import os
import importlib
import traceback

def check_python_version():
    """Verifica la versión de Python"""
    print(f"Versión de Python: {sys.version}")
    if sys.version_info.major != 3:
        print("⚠️ ADVERTENCIA: La aplicación requiere Python 3")
    elif sys.version_info.minor < 6:
        print("⚠️ ADVERTENCIA: Se recomienda Python 3.6 o superior")
    else:
        print("✓ Versión de Python compatible")

def check_dependencies():
    """Verifica las dependencias requeridas"""
    dependencies = [
        "PyQt5", "PyQtChart", "requests", "qrcode", "pandas", "matplotlib"
    ]
    
    print("\nVerificando dependencias:")
    missing = []
    
    for dep in dependencies:
        try:
            importlib.import_module(dep)
            print(f"✓ {dep} está instalado")
        except ImportError:
            print(f"✗ {dep} NO está instalado")
            missing.append(dep)
    
    return missing

def check_main_files():
    """Verifica la existencia de archivos principales"""
    required_files = [
        "main.py", 
        "api_client.py", 
        "config.json",
        "sync_manager.py",
        "sync_tab.py",
        "admin_tab.py",
        "mobile_tab.py"
    ]
    
    print("\nVerificando archivos principales:")
    missing = []
    
    for file in required_files:
        if os.path.exists(file):
            print(f"✓ {file} existe")
        else:
            print(f"✗ {file} NO existe")
            missing.append(file)
    
    return missing

def try_import_main():
    """Intenta importar el módulo main para verificar errores de sintaxis"""
    print("\nVerificando errores de sintaxis en main.py:")
    try:
        import main
        print("✓ main.py se importó correctamente")
        return True
    except Exception as e:
        print(f"✗ Error al importar main.py: {str(e)}")
        print("\nDetalles del error:")
        traceback.print_exc()
        return False

def try_import_api_client():
    """Intenta importar el módulo api_client para verificar errores de sintaxis"""
    print("\nVerificando errores de sintaxis en api_client.py:")
    try:
        import api_client
        print("✓ api_client.py se importó correctamente")
        return True
    except Exception as e:
        print(f"✗ Error al importar api_client.py: {str(e)}")
        print("\nDetalles del error:")
        traceback.print_exc()
        return False

def check_config_file():
    """Verifica el contenido del archivo config.json"""
    import json
    
    print("\nVerificando config.json:")
    try:
        with open("config.json", "r") as f:
            config = json.load(f)
            print(f"Contenido: {json.dumps(config, indent=2)}")
            
            # Verificar campos requeridos
            required_fields = ["is_offline", "api_url"]
            missing_fields = [field for field in required_fields if field not in config]
            
            if missing_fields:
                print(f"⚠️ ADVERTENCIA: Faltan campos requeridos: {', '.join(missing_fields)}")
            else:
                print("✓ config.json contiene los campos requeridos")
                
            return config
    except FileNotFoundError:
        print("✗ config.json NO existe")
        return None
    except json.JSONDecodeError:
        print("✗ config.json contiene JSON inválido")
        return None
    except Exception as e:
        print(f"✗ Error al leer config.json: {str(e)}")
        return None

def suggest_solutions(missing_deps, missing_files, main_ok, api_client_ok, config):
    """Sugiere soluciones basadas en los resultados del diagnóstico"""
    print("\n=== DIAGNÓSTICO Y SOLUCIONES SUGERIDAS ===")
    
    if missing_deps:
        print("\n1. PROBLEMA: Faltan dependencias requeridas.")
        print("   SOLUCIÓN: Instalar las dependencias faltantes con pip:")
        print(f"   pip install {' '.join(missing_deps)}")
    
    if missing_files:
        print("\n2. PROBLEMA: Faltan archivos principales.")
        print("   SOLUCIÓN: Verificar que todos los archivos de la aplicación estén presentes.")
        print("   Si falta algún archivo, es posible que necesites reinstalar la aplicación.")
    
    if not main_ok:
        print("\n3. PROBLEMA: Hay errores de sintaxis en main.py.")
        print("   SOLUCIÓN: Revisar y corregir los errores de sintaxis en main.py.")
    
    if not api_client_ok:
        print("\n4. PROBLEMA: Hay errores de sintaxis en api_client.py.")
        print("   SOLUCIÓN: Revisar y corregir los errores de sintaxis en api_client.py.")
    
    if config is None:
        print("\n5. PROBLEMA: El archivo config.json no existe o contiene errores.")
        print("   SOLUCIÓN: Crear un archivo config.json válido con el siguiente contenido:")
        print('   {"is_offline": true, "api_url": "http://127.0.0.1:8000/api", "username": "admin", "password": "admin123"}')
    
    print("\nPara iniciar la aplicación en modo simple, ejecuta:")
    print("python main.py --offline")

def main():
    """Función principal"""
    print("=== DIAGNÓSTICO BÁSICO DE LA APLICACIÓN ===\n")
    
    # Verificar versión de Python
    check_python_version()
    
    # Verificar dependencias
    missing_deps = check_dependencies()
    
    # Verificar archivos principales
    missing_files = check_main_files()
    
    # Verificar config.json
    config = check_config_file()
    
    # Intentar importar main.py
    main_ok = try_import_main()
    
    # Intentar importar api_client.py
    api_client_ok = try_import_api_client()
    
    # Sugerir soluciones
    suggest_solutions(missing_deps, missing_files, main_ok, api_client_ok, config)
    
    print("\n=== DIAGNÓSTICO COMPLETADO ===")

if __name__ == "__main__":
    main()

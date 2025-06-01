#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Script de diagnóstico mínimo para identificar problemas con la aplicación
"""

import os
import sys
import traceback

def print_separator():
    print("-" * 60)

def check_python_version():
    print(f"Versión de Python: {sys.version}")
    print_separator()

def check_main_file():
    main_path = os.path.join(os.path.dirname(__file__), "main.py")
    if os.path.exists(main_path):
        print(f"Archivo main.py encontrado: {main_path}")
        try:
            with open(main_path, "r", encoding="utf-8") as f:
                first_lines = [next(f) for _ in range(10)]
                print("Primeras 10 líneas de main.py:")
                for line in first_lines:
                    print(f"  {line.rstrip()}")
        except Exception as e:
            print(f"Error al leer main.py: {str(e)}")
    else:
        print(f"Archivo main.py NO encontrado")
    print_separator()

def check_imports():
    print("Verificando importaciones básicas...")
    modules = ["PyQt5", "requests", "json", "os", "sys"]
    for module in modules:
        try:
            __import__(module)
            print(f"✓ Módulo {module} importado correctamente")
        except ImportError:
            print(f"✗ Error al importar {module}")
    print_separator()

def check_config():
    config_path = os.path.join(os.path.dirname(__file__), "config.json")
    if os.path.exists(config_path):
        print(f"Archivo config.json encontrado: {config_path}")
        try:
            import json
            with open(config_path, "r", encoding="utf-8") as f:
                config = json.load(f)
                print(f"Contenido de config.json: {json.dumps(config, indent=2)}")
        except Exception as e:
            print(f"Error al leer config.json: {str(e)}")
    else:
        print(f"Archivo config.json NO encontrado")
    print_separator()

def try_minimal_app():
    print("Intentando crear una aplicación PyQt5 mínima...")
    try:
        from PyQt5.QtWidgets import QApplication, QLabel
        app = QApplication([])
        label = QLabel("Prueba de PyQt5")
        label.show()
        print("✓ Aplicación PyQt5 mínima creada correctamente")
        print("  Cierre la ventana para continuar")
        app.exec_()
    except Exception as e:
        print(f"✗ Error al crear aplicación PyQt5 mínima: {str(e)}")
        traceback.print_exc()
    print_separator()

def main():
    print("DIAGNÓSTICO MÍNIMO DE APP_GRANJA")
    print_separator()
    
    check_python_version()
    check_main_file()
    check_imports()
    check_config()
    try_minimal_app()
    
    print("Diagnóstico completado")

if __name__ == "__main__":
    main()

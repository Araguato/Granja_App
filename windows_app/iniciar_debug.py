#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Script de inicio con modo debug para mostrar todos los errores
"""

import sys
import os
import json
import traceback

# Configurar para mostrar todos los errores
sys.tracebacklimit = None

# Crear un archivo de configuración limpio
config = {
    "is_offline": True,
    "api_url": "http://127.0.0.1:8000/api",
    "username": "admin",
    "password": "admin123"
}

print("=== INICIANDO APP GRANJA EN MODO DEBUG ===")

# Guardar configuración
try:
    with open("config.json", "w") as f:
        json.dump(config, f, indent=2)
    print("✓ Archivo config.json creado correctamente")
except Exception as e:
    print(f"✗ Error al crear config.json: {str(e)}")
    traceback.print_exc()

# Intentar importar los módulos principales
try:
    print("\nImportando módulos principales...")
    import main
    print("✓ Módulo main importado correctamente")
except Exception as e:
    print(f"✗ Error al importar main: {str(e)}")
    traceback.print_exc()
    sys.exit(1)

# Intentar iniciar la aplicación
try:
    print("\nIniciando aplicación en modo offline...")
    sys.argv = [sys.argv[0], "--offline"]  # Forzar modo offline
    main.main()
    print("✓ Aplicación iniciada correctamente")
except Exception as e:
    print(f"✗ Error al iniciar la aplicación: {str(e)}")
    traceback.print_exc()
    sys.exit(1)

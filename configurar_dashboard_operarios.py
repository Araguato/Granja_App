#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Script para configurar el dashboard de operarios con todos los enlaces necesarios
"""

import os
import sys
import django
import shutil
from pathlib import Path

# Configurar entorno Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'granja.settings')
django.setup()

from django.urls import path, include
from django.contrib.auth.models import Group, Permission, User
from django.contrib.contenttypes.models import ContentType
from django.db.models import Q

def crear_directorios_templates():
    """
    Crea los directorios de templates necesarios si no existen
    """
    print("Creando directorios de templates...")
    
    directorios = [
        'produccion/templates/produccion',
        'inventario/templates/inventario',
        'wiki/templates/wiki',
        'faq/templates/faq',
        'bot/templates/bot'
    ]
    
    for directorio in directorios:
        path = Path(f'C:/App_Granja/{directorio}')
        if not path.exists():
            path.mkdir(parents=True, exist_ok=True)
            print(f"  Creado directorio: {directorio}")
        else:
            print(f"  El directorio ya existe: {directorio}")

def actualizar_dashboard_operarios():
    """
    Actualiza la plantilla del dashboard de operarios para incluir todos los enlaces necesarios
    """
    print("\nActualizando plantilla del dashboard de operarios...")
    
    # Ruta a la plantilla del dashboard de operarios
    dashboard_path = Path('C:/App_Granja/avicola/templates/dashboard_operario.html')
    
    if not dashboard_path.exists():
        print("  Error: No se encontró la plantilla del dashboard de operarios")
        return False
    
    # Leer la plantilla actual
    with open(dashboard_path, 'r', encoding='utf-8') as file:
        content = file.read()
    
    # Verificar si ya tiene los enlaces a Wiki, FAQ y BOT
    if 'href="/wiki/"' in content and 'href="/faq/"' in content and 'href="/bot/"' in content:
        print("  La plantilla ya tiene los enlaces necesarios")
        return True
    
    # Buscar la sección de acceso rápido
    quick_access_section = '<!-- Menú de navegación para operarios -->'
    
    if quick_access_section not in content:
        print("  Error: No se encontró la sección de acceso rápido en la plantilla")
        return False
    
    # Hacer una copia de seguridad de la plantilla original
    backup_path = dashboard_path.with_suffix('.html.bak')
    shutil.copy2(dashboard_path, backup_path)
    print(f"  Copia de seguridad creada: {backup_path}")
    
    # Actualizar la sección de acceso rápido para incluir enlaces a Wiki, FAQ y BOT
    updated_section = '''<!-- Menú de navegación para operarios -->
    <div class="row mb-4">
        <div class="col-12">
            <div class="card shadow-sm">
                <div class="card-header bg-dark text-white">
                    <h5 class="mb-0">
                        <i class="fas fa-th-large me-2"></i>
                        {% if LANGUAGE_CODE == 'en' %}Quick Access{% else %}Acceso Rápido{% endif %}
                    </h5>
                </div>
                <div class="card-body">
                    <div class="row g-3">
                        <div class="col-md-3 col-sm-6">
                            <a href="/produccion/lotes/" class="btn btn-outline-primary w-100 py-3">
                                <i class="fas fa-layer-group mb-2 d-block" style="font-size: 24px;"></i>
                                {% if LANGUAGE_CODE == 'en' %}Lots{% else %}Lotes{% endif %}
                            </a>
                        </div>
                        <div class="col-md-3 col-sm-6">
                            <a href="/produccion/galpones/" class="btn btn-outline-success w-100 py-3">
                                <i class="fas fa-warehouse mb-2 d-block" style="font-size: 24px;"></i>
                                {% if LANGUAGE_CODE == 'en' %}Sheds{% else %}Galpones{% endif %}
                            </a>
                        </div>
                        <div class="col-md-3 col-sm-6">
                            <a href="/inventario/alimentos/" class="btn btn-outline-warning w-100 py-3">
                                <i class="fas fa-drumstick-bite mb-2 d-block" style="font-size: 24px;"></i>
                                {% if LANGUAGE_CODE == 'en' %}Feed{% else %}Alimentos{% endif %}
                            </a>
                        </div>
                        <div class="col-md-3 col-sm-6">
                            <a href="/produccion/tareas/" class="btn btn-outline-danger w-100 py-3">
                                <i class="fas fa-tasks mb-2 d-block" style="font-size: 24px;"></i>
                                {% if LANGUAGE_CODE == 'en' %}Tasks{% else %}Tareas{% endif %}
                            </a>
                        </div>
                    </div>
                    <div class="row g-3 mt-2">
                        <div class="col-md-3 col-sm-6">
                            <a href="/inventario/seguimiento/" class="btn btn-outline-info w-100 py-3">
                                <i class="fas fa-clipboard-check mb-2 d-block" style="font-size: 24px;"></i>
                                {% if LANGUAGE_CODE == 'en' %}Tracking{% else %}Seguimiento{% endif %}
                            </a>
                        </div>
                        <div class="col-md-3 col-sm-6">
                            <a href="/wiki/" class="btn btn-outline-secondary w-100 py-3">
                                <i class="fas fa-book mb-2 d-block" style="font-size: 24px;"></i>
                                {% if LANGUAGE_CODE == 'en' %}Wiki{% else %}Wiki{% endif %}
                            </a>
                        </div>
                        <div class="col-md-3 col-sm-6">
                            <a href="/faq/" class="btn btn-outline-primary w-100 py-3">
                                <i class="fas fa-question-circle mb-2 d-block" style="font-size: 24px;"></i>
                                {% if LANGUAGE_CODE == 'en' %}FAQ{% else %}FAQ{% endif %}
                            </a>
                        </div>
                        <div class="col-md-3 col-sm-6">
                            <a href="/bot/" class="btn btn-outline-dark w-100 py-3">
                                <i class="fas fa-robot mb-2 d-block" style="font-size: 24px;"></i>
                                {% if LANGUAGE_CODE == 'en' %}Bot{% else %}Bot{% endif %}
                            </a>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>'''
    
    # Reemplazar la sección de acceso rápido
    updated_content = content.replace(
        content[content.find(quick_access_section):content.find('<div class="row mb-4">', content.find(quick_access_section) + 1)],
        updated_section
    )
    
    # Guardar la plantilla actualizada
    with open(dashboard_path, 'w', encoding='utf-8') as file:
        file.write(updated_content)
    
    print("  Plantilla del dashboard de operarios actualizada correctamente")
    return True

def actualizar_urls_granja():
    """
    Actualiza el archivo urls.py del proyecto para incluir todas las aplicaciones necesarias
    """
    print("\nActualizando URLs del proyecto...")
    
    # Ruta al archivo urls.py del proyecto
    urls_path = Path('C:/App_Granja/granja/urls.py')
    
    if not urls_path.exists():
        print("  Error: No se encontró el archivo urls.py del proyecto")
        return False
    
    # Leer el archivo actual
    with open(urls_path, 'r', encoding='utf-8') as file:
        content = file.read()
    
    # Verificar si ya tiene todas las URLs necesarias
    required_urls = [
        "path('produccion/', include('produccion.urls'))",
        "path('inventario/', include('inventario.urls'))",
        "path('wiki/', include('wiki.urls'))",
        "path('faq/', include('faq.urls'))",
        "path('bot/', include('bot.urls'))"
    ]
    
    missing_urls = [url for url in required_urls if url not in content]
    
    if not missing_urls:
        print("  El archivo urls.py ya tiene todas las URLs necesarias")
        return True
    
    # Hacer una copia de seguridad del archivo original
    backup_path = urls_path.with_suffix('.py.bak')
    shutil.copy2(urls_path, backup_path)
    print(f"  Copia de seguridad creada: {backup_path}")
    
    # Buscar la sección de urlpatterns
    urlpatterns_start = content.find('urlpatterns = [')
    if urlpatterns_start == -1:
        print("  Error: No se encontró la sección urlpatterns en el archivo")
        return False
    
    # Encontrar la primera URL después de urlpatterns
    first_url_start = content.find('path(', urlpatterns_start)
    if first_url_start == -1:
        print("  Error: No se encontraron URLs en el archivo")
        return False
    
    # Insertar las URLs faltantes
    urls_to_add = '\n    '.join(missing_urls) + '\n    '
    updated_content = content[:first_url_start] + urls_to_add + content[first_url_start:]
    
    # Guardar el archivo actualizado
    with open(urls_path, 'w', encoding='utf-8') as file:
        file.write(updated_content)
    
    print("  URLs del proyecto actualizadas correctamente")
    print("  URLs añadidas:")
    for url in missing_urls:
        print(f"    {url}")
    
    return True

def main():
    """
    Función principal
    """
    print("=" * 60)
    print("CONFIGURACIÓN DEL DASHBOARD DE OPERARIOS")
    print("=" * 60)
    
    # Crear directorios de templates
    crear_directorios_templates()
    
    # Actualizar dashboard de operarios
    actualizar_dashboard_operarios()
    
    # Actualizar URLs del proyecto
    actualizar_urls_granja()
    
    print("\nConfiguración completada")
    print("=" * 60)
    print("\nPara aplicar los cambios, reinicie el servidor Django:")
    print("  1. Ejecute: taskkill /F /IM python.exe")
    print("  2. Ejecute: .\\iniciar_servidor_django.bat")
    print("=" * 60)

if __name__ == "__main__":
    main()

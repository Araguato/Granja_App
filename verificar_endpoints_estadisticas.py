#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Script para verificar y corregir los endpoints de estadísticas en el servidor Django
"""

import os
import sys
import requests
import json
from pathlib import Path

def print_header(text):
    print("\n" + "=" * 60)
    print(" " + text)
    print("=" * 60 + "\n")

def verificar_endpoints():
    """Verifica los endpoints de estadísticas en el servidor Django"""
    print_header("VERIFICANDO ENDPOINTS DE ESTADÍSTICAS")
    
    # URL base del servidor Django
    base_url = "http://127.0.0.1:8000"
    api_url = f"{base_url}/api"
    
    # Endpoints a verificar
    endpoints = [
        "/api/estadisticas/dashboard/",
        "/api/estadisticas/lotes/",
        "/api/estadisticas/produccion/",
        "/api/estadisticas/mortalidad/",
        "/api/estadisticas/comparacion-razas/"
    ]
    
    # Verificar cada endpoint
    endpoints_disponibles = []
    endpoints_no_disponibles = []
    
    for endpoint in endpoints:
        url = f"{base_url}{endpoint}"
        try:
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                print(f"✓ Endpoint {endpoint} disponible")
                endpoints_disponibles.append(endpoint)
            else:
                print(f"✗ Endpoint {endpoint} no disponible (código {response.status_code})")
                endpoints_no_disponibles.append(endpoint)
        except requests.exceptions.RequestException:
            print(f"✗ Endpoint {endpoint} no disponible (error de conexión)")
            endpoints_no_disponibles.append(endpoint)
    
    return endpoints_disponibles, endpoints_no_disponibles

def main():
    print_header("VERIFICACIÓN DE ENDPOINTS DE ESTADÍSTICAS")
    
    # Verificar endpoints
    endpoints_disponibles, endpoints_no_disponibles = verificar_endpoints()
    
    if not endpoints_no_disponibles:
        print("\n✓ Todos los endpoints de estadísticas están disponibles")
        return
    
    print("\n✗ Algunos endpoints de estadísticas no están disponibles")
    
    # Sugerir soluciones
    print_header("SOLUCIONES SUGERIDAS")
    
    print("1. Asegúrese de que el servidor Django esté en ejecución")
    print("   Ejecute: python manage.py runserver 0.0.0.0:8000")
    print("\n2. Verifique que las URLs de estadísticas estén definidas en urls.py")
    print("   Ejemplo:")
    print("   path('api/estadisticas/dashboard/', views.dashboard_stats, name='dashboard_stats'),")
    print("   path('api/estadisticas/comparacion-razas/', views.comparacion_razas, name='comparacion_razas'),")
    print("\n3. Implemente las vistas necesarias en views.py")
    print("   Ejemplo:")
    print("   @api_view(['GET'])")
    print("   def dashboard_stats(request):")
    print("       # Código para obtener estadísticas")
    print("       return Response(data)")
    print("\n4. Para la comparación de razas, asegúrese de que la vista devuelva:")
    print("   {")
    print("     'raza_nominal': {")
    print("       'nombre': 'Nombre de la raza',")
    print("       'produccion_esperada': 280,")
    print("       'peso_esperado': 1.8,")
    print("       'mortalidad_esperada': 2")
    print("     },")
    print("     'raza_actual': {")
    print("       'nombre': 'Nombre de la raza',")
    print("       'lote_id': 1,")
    print("       'produccion_actual': 265,")
    print("       'peso_actual': 1.7,")
    print("       'mortalidad_actual': 3")
    print("     }")
    print("   }")

if __name__ == "__main__":
    main()

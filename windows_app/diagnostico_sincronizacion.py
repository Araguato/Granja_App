#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Script de diagnóstico para verificar la funcionalidad de sincronización
en la aplicación App_Granja.
"""

import sys
import json
import os
import time
from api_client import ApiClient
from sync_manager import SyncManager

def main():
    """Función principal del script de diagnóstico"""
    print("=== DIAGNÓSTICO DE SINCRONIZACIÓN ===")
    
    # Crear instancia de ApiClient
    api_client = ApiClient()
    print(f"Modo offline: {api_client.is_offline}")
    
    # Verificar conexión con el servidor
    print("\n=== VERIFICANDO CONEXIÓN CON EL SERVIDOR ===")
    success, message = api_client.test_connection()
    print(f"Resultado: success={success}, message='{message}'")
    
    # Crear instancia de SyncManager
    print("\n=== INICIALIZANDO SYNC MANAGER ===")
    sync_manager = SyncManager(api_client)
    
    # Registrar callbacks para eventos de sincronización
    def on_sync_started():
        print("\n>>> Sincronización iniciada")
    
    def on_sync_completed(success, message):
        print(f"\n>>> Sincronización completada: success={success}, message='{message}'")
    
    def on_sync_progress(progress, message):
        print(f">>> Progreso: {progress}% - {message}")
    
    def on_data_updated(entity):
        print(f">>> Datos actualizados: {entity}")
    
    # Conectar señales
    sync_manager.sync_started.connect(on_sync_started)
    sync_manager.sync_completed.connect(on_sync_completed)
    sync_manager.sync_progress.connect(on_sync_progress)
    sync_manager.data_updated.connect(on_data_updated)
    
    # Probar sincronización
    print("\n=== PROBANDO SINCRONIZACIÓN ===")
    success, message = sync_manager.sync_now()
    print(f"Resultado de sync_now(): success={success}, message='{message}'")
    
    # Esperar a que termine la sincronización
    print("\nEsperando a que termine la sincronización...")
    wait_time = 0
    while sync_manager.is_syncing and wait_time < 30:
        time.sleep(1)
        wait_time += 1
        print(".", end="", flush=True)
    print("\n")
    
    if sync_manager.is_syncing:
        print("¡Advertencia! La sincronización está tardando demasiado tiempo.")
    else:
        print("Sincronización finalizada.")
    
    # Verificar datos sincronizados
    print("\n=== DATOS SINCRONIZADOS ===")
    for entity in sync_manager.entities:
        data = sync_manager.offline_data.get(entity, [])
        print(f"{entity}: {len(data) if isinstance(data, list) else 'no es lista'} elementos")
    
    print("\n=== DIAGNÓSTICO COMPLETADO ===")

if __name__ == "__main__":
    main()

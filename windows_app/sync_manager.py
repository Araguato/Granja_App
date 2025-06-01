#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import json
import os
import time
import threading
from datetime import datetime
from PyQt5.QtCore import QObject, pyqtSignal, QTimer

class SyncManager(QObject):
    """
    Gestor de sincronización entre la aplicación de Windows, 
    el banco de datos y la aplicación móvil.
    """
    
    # Señales para notificar eventos de sincronización
    sync_started = pyqtSignal()
    sync_completed = pyqtSignal(bool, str)  # Éxito, mensaje
    sync_progress = pyqtSignal(int, str)  # Porcentaje, entidad actual
    data_updated = pyqtSignal(str)  # Entidad actualizada
    
    def __init__(self, api_client):
        super().__init__()
        self.api_client = api_client
        self.is_syncing = False
        self.last_sync = None
        self.sync_interval = 15 * 60  # 15 minutos en segundos
        self.entities = [
            'lotes', 'galpones', 'alimentos', 'vacunas', 'razas', 
            'seguimientos', 'tareas', 'usuarios', 'empresas', 'granjas'
        ]
        self.pending_changes = {}
        self.offline_data = {}
        
        # Cargar cambios pendientes
        self.load_pending_changes()
        
        # Configurar temporizador para sincronización automática
        self.sync_timer = QTimer()
        self.sync_timer.timeout.connect(self.auto_sync)
        self.sync_timer.start(self.sync_interval * 1000)  # Convertir a milisegundos
    
    def load_pending_changes(self):
        """Carga los cambios pendientes desde el archivo de cambios pendientes"""
        pending_changes_path = os.path.join(os.path.dirname(__file__), 'pending_changes.json')
        try:
            if os.path.exists(pending_changes_path):
                with open(pending_changes_path, 'r') as f:
                    self.pending_changes = json.load(f)
            else:
                self.pending_changes = {entity: [] for entity in self.entities}
                self.save_pending_changes()
        except Exception as e:
            print(f"Error al cargar cambios pendientes: {str(e)}")
            self.pending_changes = {entity: [] for entity in self.entities}
    
    def save_pending_changes(self):
        """Guarda los cambios pendientes en el archivo de cambios pendientes"""
        pending_changes_path = os.path.join(os.path.dirname(__file__), 'pending_changes.json')
        try:
            with open(pending_changes_path, 'w') as f:
                json.dump(self.pending_changes, f, indent=4)
            return True
        except Exception as e:
            print(f"Error al guardar cambios pendientes: {str(e)}")
            return False
    
    def add_pending_change(self, entity, operation, data):
        """Agrega un cambio pendiente para sincronizar más tarde"""
        if entity not in self.pending_changes:
            self.pending_changes[entity] = []
        
        # Agregar cambio con timestamp
        change = {
            'operation': operation,  # 'create', 'update', 'delete'
            'data': data,
            'timestamp': datetime.now().isoformat()
        }
        
        self.pending_changes[entity].append(change)
        self.save_pending_changes()
        
        # Notificar que hay datos actualizados
        self.data_updated.emit(entity)
    
    def sync_now(self):
        """Inicia la sincronización de datos inmediatamente"""
        if self.is_syncing:
            return False, "Ya hay una sincronización en curso"
        
        # Iniciar sincronización en un hilo separado
        self.is_syncing = True
        self.sync_started.emit()
        
        sync_thread = threading.Thread(target=self._sync_process)
        sync_thread.daemon = True
        sync_thread.start()
        
        return True, "Sincronización iniciada"
    
    def _sync_process(self):
        """Proceso de sincronización (ejecutado en un hilo separado)"""
        try:
            # Verificar conexión
            success, _ = self.api_client.test_connection()
            if not success:
                self.is_syncing = False
                self.sync_completed.emit(False, "No hay conexión con el servidor")
                return
            
            # Sincronizar entidades
            total_entities = len(self.entities)
            for i, entity in enumerate(self.entities):
                # Actualizar progreso
                progress = int((i / total_entities) * 100)
                self.sync_progress.emit(progress, f"Sincronizando {entity}")
                
                # Enviar cambios pendientes
                self._sync_entity_changes(entity)
                
                # Obtener datos actualizados
                self._sync_entity_data(entity)
                
                # Breve pausa para no sobrecargar la API
                time.sleep(0.5)
            
            # Actualizar timestamp de última sincronización
            self.last_sync = datetime.now()
            
            # Notificar finalización exitosa
            self.is_syncing = False
            self.sync_completed.emit(True, f"Sincronización completada: {self.last_sync.strftime('%Y-%m-%d %H:%M:%S')}")
        
        except Exception as e:
            error_msg = f"Error durante la sincronización: {str(e)}"
            print(error_msg)
            self.is_syncing = False
            self.sync_completed.emit(False, error_msg)
    
    def _sync_entity_changes(self, entity):
        """Sincroniza los cambios pendientes de una entidad específica"""
        if entity not in self.pending_changes or not self.pending_changes[entity]:
            return
        
        changes_to_remove = []
        
        for i, change in enumerate(self.pending_changes[entity]):
            operation = change['operation']
            data = change['data']
            
            success = False
            
            if operation == 'create':
                # Llamar al método correspondiente según la entidad
                if entity == 'lotes':
                    success, _ = self.api_client.create_lote(data)
                elif entity == 'galpones':
                    success, _ = self.api_client.create_galpon(data)
                elif entity == 'seguimientos':
                    success, _ = self.api_client.create_seguimiento(data.get('lote_id'), data)
                elif entity == 'tareas':
                    success, _ = self.api_client.crear_tarea(data)
                # Agregar más entidades según sea necesario
            
            elif operation == 'update':
                # Llamar al método correspondiente según la entidad
                if entity == 'lotes':
                    success, _ = self.api_client.update_lote(data.get('id'), data)
                elif entity == 'galpones':
                    success, _ = self.api_client.update_galpon(data.get('id'), data)
                elif entity == 'seguimientos':
                    success, _ = self.api_client.update_seguimiento(data.get('id'), data)
                elif entity == 'tareas':
                    success, _ = self.api_client.actualizar_tarea(data)
                # Agregar más entidades según sea necesario
            
            elif operation == 'delete':
                # Llamar al método correspondiente según la entidad
                if entity == 'lotes':
                    success, _ = self.api_client.delete_lote(data.get('id'))
                elif entity == 'galpones':
                    success, _ = self.api_client.delete_galpon(data.get('id'))
                elif entity == 'tareas':
                    success, _ = self.api_client.eliminar_tarea(data.get('id'))
                # Agregar más entidades según sea necesario
            
            # Si el cambio se aplicó correctamente, marcarlo para eliminación
            if success:
                changes_to_remove.append(i)
        
        # Eliminar cambios aplicados (de atrás hacia adelante para no afectar los índices)
        for i in sorted(changes_to_remove, reverse=True):
            del self.pending_changes[entity][i]
        
        # Guardar cambios pendientes actualizados
        self.save_pending_changes()
    
    def _save_local_data(self, entity, data):
        """
        Guarda los datos de una entidad en el almacenamiento local.
        
        Args:
            entity (str): Nombre de la entidad a guardar (ej: 'lotes', 'galpones')
            data: Datos a guardar (debe ser serializable a JSON)
            
        Returns:
            bool: True si los datos se guardaron correctamente, False en caso contrario
        """
        if data is None:
            print(f"[SYNC] Advertencia: No hay datos para guardar de {entity}")
            return False
            
        try:
            # Verificar si los datos son serializables
            try:
                json.dumps(data)
            except (TypeError, OverflowError, ValueError) as e:
                print(f"[SYNC] Error: Los datos de {entity} no son serializables: {str(e)}")
                return False
                
            # Crear directorio de datos si no existe
            data_dir = os.path.join(os.path.dirname(__file__), 'data')
            try:
                os.makedirs(data_dir, exist_ok=True)
            except OSError as e:
                print(f"[SYNC] Error al crear directorio de datos: {str(e)}")
                return False
            
            # Crear ruta de archivo temporal
            temp_path = os.path.join(data_dir, f"{entity}.json.tmp")
            file_path = os.path.join(data_dir, f"{entity}.json")
            
            # Escribir primero en un archivo temporal
            try:
                with open(temp_path, 'w', encoding='utf-8') as f:
                    json.dump(data, f, ensure_ascii=False, indent=2, default=str)
                
                # Renombrar el archivo temporal al archivo final (operación atómica)
                if os.path.exists(file_path):
                    os.remove(file_path)
                os.rename(temp_path, file_path)
                
                # Verificar que el archivo se haya guardado correctamente
                if os.path.exists(file_path) and os.path.getsize(file_path) > 0:
                    print(f"[SYNC] Datos de {entity} guardados correctamente en {file_path}")
                    # Actualizar la caché en memoria
                    self.offline_data[entity] = data
                    return True
                else:
                    print(f"[SYNC] Error: No se pudo verificar el archivo guardado para {entity}")
                    return False
                    
            except (IOError, OSError, json.JSONEncodeError) as e:
                print(f"[SYNC] Error al escribir datos locales de {entity}: {str(e)}")
                # Intentar eliminar el archivo temporal si existe
                if os.path.exists(temp_path):
                    try:
                        os.remove(temp_path)
                    except OSError:
                        pass
                return False
                
        except Exception as e:
            import traceback
            print(f"[SYNC] Error inesperado al guardar datos de {entity}: {str(e)}")
            print(f"[SYNC] Traceback: {traceback.format_exc()}")
            return False

    def _load_local_data(self, entity):
        """
        Carga los datos de una entidad desde el almacenamiento local.
        
        Args:
            entity (str): Nombre de la entidad a cargar (ej: 'lotes', 'galpones')
            
        Returns:
            list or dict or None: Los datos cargados, o None si hay un error o el archivo no existe
        """
        # Verificar si los datos están en caché
        if entity in self.offline_data and self.offline_data[entity] is not None:
            print(f"[SYNC] Usando datos en caché para {entity}")
            return self.offline_data[entity]
            
        file_path = os.path.join(os.path.dirname(__file__), 'data', f"{entity}.json")
        
        # Verificar si el archivo existe
        if not os.path.exists(file_path):
            print(f"[SYNC] No se encontró archivo local para {entity}")
            return None
            
        # Verificar si el archivo está vacío o es muy pequeño
        try:
            if os.path.getsize(file_path) < 2:  # Un JSON válido debe tener al menos 2 caracteres: [] o {}
                print(f"[SYNC] Advertencia: El archivo {entity}.json está vacío o es muy pequeño")
                return None
        except OSError as e:
            print(f"[SYNC] Error al verificar el tamaño del archivo {entity}.json: {str(e)}")
            return None
        
        # Intentar cargar el archivo
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                
            # Validar que los datos tengan un formato esperado
            if not isinstance(data, (list, dict)):
                print(f"[SYNC] Advertencia: Formato de datos inesperado en {entity}.json")
                return None
                
            # Actualizar la caché
            self.offline_data[entity] = data
            print(f"[SYNC] Datos de {entity} cargados correctamente desde {file_path}")
            return data
            
        except json.JSONDecodeError as e:
            print(f"[SYNC] Error de sintaxis JSON en {entity}.json: {str(e)}")
            return None
            
        except UnicodeDecodeError as e:
            print(f"[SYNC] Error de codificación en {entity}.json: {str(e)}")
            return None
            
        except Exception as e:
            import traceback
            print(f"[SYNC] Error inesperado al cargar {entity}.json: {str(e)}")
            print(f"[SYNC] Traceback: {traceback.format_exc()}")
            return None

    def _sync_entity_data(self, entity):
        """
        Sincroniza los datos de una entidad específica con el servidor.
        
        Args:
            entity (str): Nombre de la entidad a sincronizar
            
        Returns:
            bool: True si la sincronización fue exitosa, False en caso contrario
        """
        print(f"[SYNC] Iniciando sincronización de {entity}...")
        
        # Cargar datos locales como respaldo
        local_data = self._load_local_data(entity)
        
        # Mapeo de entidades a métodos de la API y sus parámetros
        entity_map = {
            'lotes': (self.api_client.get_lotes, {}),
            'galpones': (self.api_client.get_galpones, {}),
            'alimentos': (self.api_client.get_alimentos, {}),
            'vacunas': (self.api_client.get_vacunas, {}),
            'razas': (self.api_client.get_razas, {}),
            'seguimientos': (self.api_client.get_seguimientos, {}),
            'tareas': (self.api_client.get_tareas, {}),
            'usuarios': (self.api_client.get_usuarios, {}),
            'empresas': (self.api_client.get_empresas, {}),
            'granjas': (self.api_client.get_granjas, {}),
        }
        
        # Verificar si la entidad es soportada
        if entity not in entity_map:
            error_msg = f"[SYNC] Error: No se encontró método para la entidad {entity}"
            print(error_msg)
            self.sync_completed.emit(False, error_msg)
            self.data_updated.emit(entity)  # Notificar actualización para usar datos locales
            return False
            
        api_method, params = entity_map[entity]
        
        # Verificar modo offline
        if hasattr(self.api_client, 'is_offline') and self.api_client.is_offline:
            print(f"[SYNC] Modo offline. Usando datos locales para {entity}")
            if local_data:
                print(f"[SYNC] Se encontraron {len(local_data) if isinstance(local_data, list) else 1} registros locales para {entity}")
                self.data_updated.emit(entity)
            else:
                print(f"[SYNC] No hay datos locales disponibles para {entity}")
            return bool(local_data)
        
        # Intentar obtener datos del servidor
        try:
            print(f"[SYNC] Solicitando datos de {entity} al servidor...")
            success, data = api_method(**params) if params else api_method()
            
            # Verificar si la petición fue exitosa
            if not success:
                error_msg = f"[SYNC] Error en la respuesta del servidor para {entity}"
                if isinstance(data, str):
                    error_msg += f": {data}"
                print(error_msg)
                
                # Usar datos locales como respaldo si están disponibles
                if local_data:
                    print(f"[SYNC] Usando {len(local_data) if isinstance(local_data, list) else 1} registros locales como respaldo")
                    self.data_updated.emit(entity)
                return bool(local_data)
                
            # Verificar si hay datos
            if data is None:
                print(f"[SYNC] No se recibieron datos para {entity}")
                # Guardar lista vacía para evitar reintentos constantes
                self._save_local_data(entity, [])
                self.data_updated.emit(entity)
                return False
                
            # Normalizar los datos recibidos
            print(f"[SYNC] Normalizando datos de {entity}...")
            normalized_data = self._normalize_api_data(data, entity)
            
            if normalized_data is None:
                error_msg = f"[SYNC] No se pudieron normalizar los datos de {entity}"
                print(error_msg)
                
                # Usar datos locales si están disponibles
                if local_data:
                    print(f"[SYNC] Usando {len(local_data) if isinstance(local_data, list) else 1} registros locales")
                    self.data_updated.emit(entity)
                return bool(local_data)
                
            # Verificar si hay datos después de la normalización
            if not normalized_data:
                print(f"[SYNC] No hay datos después de normalizar para {entity}")
                # Guardar lista vacía
                self._save_local_data(entity, [])
                self.data_updated.emit(entity)
                return True
                
            # Guardar datos localmente
            print(f"[SYNC] Guardando {len(normalized_data)} registros de {entity} localmente...")
            if self._save_local_data(entity, normalized_data):
                print(f"[SYNC] Datos de {entity} sincronizados correctamente")
                self.data_updated.emit(entity)
                return True
            else:
                print(f"[SYNC] Error al guardar datos locales de {entity}")
                return bool(local_data)
            
        except Exception as e:
            import traceback
            error_details = traceback.format_exc()
            print(f"[SYNC] Error al sincronizar {entity}: {str(e)}")
            print(f"[SYNC] Detalles del error: {error_details}")
            
            # En caso de error, usar datos locales si están disponibles
            if local_data:
                print("[SYNC] Usando datos locales debido a un error de sincronización")
                self.data_updated.emit(entity)
                return True
                
            return False
    
    def _normalize_api_data(self, data, entity):
        """
        Normaliza los datos recibidos de la API a un formato consistente.
        
        Args:
            data: Datos recibidos de la API
            entity (str): Nombre de la entidad que se está normalizando
            
        Returns:
            list: Lista de elementos normalizados, o None en caso de error
        """
        if data is None:
            print(f"[SYNC] Advertencia: No hay datos para normalizar para {entity}")
            return None
            
        try:
            # Si es una lista, ya está en el formato esperado
            if isinstance(data, list):
                print(f"[SYNC] Datos de {entity} recibidos como lista de {len(data)} elementos")
                return data
                
            # Si es un diccionario, verificar formatos comunes
            if isinstance(data, dict):
                # Formato con 'results' (DRF pagination estándar)
                if 'results' in data and isinstance(data['results'], list):
                    print(f"[SYNC] Datos de {entity} recibidos con paginación estándar, {len(data['results'])} elementos")
                    return data['results']
                    
                # Formato con 'data' (alternativo)
                if 'data' in data and isinstance(data['data'], list):
                    print(f"[SYNC] Datos de {entity} recibidos en campo 'data', {len(data['data'])} elementos")
                    return data['data']
                    
                # Formato con 'items' (algunas APIs usan esto)
                if 'items' in data and isinstance(data['items'], list):
                    print(f"[SYNC] Datos de {entity} recibidos en campo 'items', {len(data['items'])} elementos")
                    return data['items']
                    
                # Si es un solo objeto, convertirlo a lista
                if 'id' in data:
                    print(f"[SYNC] Datos de {entity} recibidos como objeto único, convirtiendo a lista")
                    return [data]
                    
                # Si el diccionario está vacío, devolver lista vacía
                if not data:
                    print(f"[SYNC] Diccionario vacío recibido para {entity}, devolviendo lista vacía")
                    return []
                    
            # Si llegamos aquí, el formato no es el esperado
            print(f"[SYNC] Formato de datos no soportado para {entity}: {type(data)}")
            print(f"[SYNC] Contenido: {str(data)[:200]}...")  # Mostrar parte del contenido para depuración
            return None
            
        except Exception as e:
            import traceback
            print(f"[SYNC] Error al normalizar datos de {entity}: {str(e)}")
            print(f"[SYNC] Traceback: {traceback.format_exc()}")
            return None
    
    def _save_offline_data(self, entity, data):
        """Guarda los datos de una entidad para uso offline"""
        offline_dir = os.path.join(os.path.dirname(__file__), 'offline_data')
        
        # Crear directorio si no existe
        if not os.path.exists(offline_dir):
            os.makedirs(offline_dir)
        
        # Guardar datos
        offline_path = os.path.join(offline_dir, f"{entity}.json")
        try:
            with open(offline_path, 'w') as f:
                json.dump(data, f, indent=4)
            return True
        except Exception as e:
            print(f"Error al guardar datos offline de {entity}: {str(e)}")
            return False
    
    def load_offline_data(self, entity):
        """Carga los datos offline de una entidad"""
        offline_path = os.path.join(os.path.dirname(__file__), 'offline_data', f"{entity}.json")
        try:
            if os.path.exists(offline_path):
                with open(offline_path, 'r') as f:
                    return json.load(f)
            return []
        except Exception as e:
            print(f"Error al cargar datos offline de {entity}: {str(e)}")
            return []
    
    def auto_sync(self):
        """Realiza una sincronización automática si es necesario"""
        # Verificar si hay una sincronización en curso
        if self.is_syncing:
            return
        
        # Verificar si hay cambios pendientes
        has_pending_changes = any(len(changes) > 0 for changes in self.pending_changes.values())
        
        # Verificar si ha pasado suficiente tiempo desde la última sincronización
        if self.last_sync:
            time_since_last_sync = (datetime.now() - self.last_sync).total_seconds()
            if time_since_last_sync < self.sync_interval and not has_pending_changes:
                return
        
        # Iniciar sincronización
        self.sync_now()
    
    def set_sync_interval(self, minutes):
        """Establece el intervalo de sincronización automática en minutos"""
        if minutes < 1:
            minutes = 1
        
        self.sync_interval = minutes * 60
        
        # Reiniciar temporizador
        self.sync_timer.stop()
        self.sync_timer.start(self.sync_interval * 1000)
    
    def get_entity_data(self, entity, force_refresh=False):
        """
        Obtiene los datos de una entidad, ya sea desde la caché local o del servidor.
        
        Args:
            entity (str): Nombre de la entidad a obtener (ej: 'galpones', 'lotes')
            force_refresh (bool): Si es True, fuerza una actualización desde el servidor
            
        Returns:
            tuple: (success, data) donde success es un booleano que indica si la operación
                  fue exitosa, y data es la lista de datos o None en caso de error.
        """
        print(f"[SYNC] Solicitando datos de {entity}, forzar actualización: {force_refresh}")
        
        # Verificar si la entidad es válida
        if entity not in self.entities:
            print(f"[SYNC] Error: Entidad '{entity}' no es válida")
            return False, []
        
        # Si no se fuerza la actualización, verificar si hay datos en caché
        if not force_refresh:
            # Verificar caché en memoria primero
            if entity in self.offline_data and self.offline_data[entity] is not None:
                print(f"[SYNC] Usando datos en caché para {entity}")
                return True, self.offline_data[entity]
                
            # Si no hay en caché, intentar cargar desde archivo local
            local_data = self._load_local_data(entity)
            if local_data is not None:
                print(f"[SYNC] Datos de {entity} cargados desde almacenamiento local")
                self.offline_data[entity] = local_data
                return True, local_data
        
        # Si se fuerza la actualización o no hay datos locales, sincronizar
        print(f"[SYNC] Sincronizando datos de {entity} desde el servidor...")
        success = self._sync_entity_data(entity)
        
        # Si la sincronización falló, intentar usar datos locales si están disponibles
        if not success:
            print(f"[SYNC] No se pudieron obtener datos actualizados de {entity}")
            
            # Intentar cargar datos locales como último recurso
            local_data = self._load_local_data(entity)
            if local_data is not None:
                print(f"[SYNC] Usando datos locales como respaldo para {entity}")
                self.offline_data[entity] = local_data
                return True, local_data
                
            print(f"[SYNC] No hay datos locales disponibles para {entity}")
            return False, []
        
        # Si la sincronización fue exitosa, devolver los datos actualizados
        if entity in self.offline_data and self.offline_data[entity] is not None:
            return True, self.offline_data[entity]
            
        # Si todo falla, devolver lista vacía
        print(f"[SYNC] No se encontraron datos para {entity} después de la sincronización")
        return False, []

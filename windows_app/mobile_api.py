#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import os
import time
import threading
from datetime import datetime
from http.server import HTTPServer, BaseHTTPRequestHandler
import socketserver
import urllib.parse
import ssl

class MobileAPIHandler(BaseHTTPRequestHandler):
    """Manejador de peticiones para la API móvil"""
    
    def __init__(self, *args, api_client=None, sync_manager=None, **kwargs):
        self.api_client = api_client
        self.sync_manager = sync_manager
        super().__init__(*args, **kwargs)
    
    def _set_headers(self, status_code=200, content_type='application/json'):
        """Establece las cabeceras de respuesta"""
        self.send_response(status_code)
        self.send_header('Content-type', content_type)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        self.end_headers()
    
    def do_OPTIONS(self):
        """Maneja las peticiones OPTIONS (CORS)"""
        self._set_headers()
    
    def do_GET(self):
        """Maneja las peticiones GET"""
        # Parsear la ruta
        parsed_path = urllib.parse.urlparse(self.path)
        path = parsed_path.path
        
        # Obtener parámetros de consulta
        query = urllib.parse.parse_qs(parsed_path.query)
        
        # Verificar autenticación
        if not self._check_auth():
            self._set_headers(401)
            self.wfile.write(json.dumps({'error': 'No autorizado'}).encode())
            return
        
        # Rutas de la API
        if path == '/api/status':
            # Estado de la API
            response = {
                'status': 'online',
                'version': '1.0',
                'timestamp': datetime.now().isoformat()
            }
            self._set_headers()
            self.wfile.write(json.dumps(response).encode())
        
        elif path.startswith('/api/sync/status'):
            # Estado de sincronización
            response = {
                'is_syncing': self.sync_manager.is_syncing,
                'last_sync': self.sync_manager.last_sync.isoformat() if self.sync_manager.last_sync else None,
                'pending_changes': {k: len(v) for k, v in self.sync_manager.pending_changes.items()}
            }
            self._set_headers()
            self.wfile.write(json.dumps(response).encode())
        
        elif path.startswith('/api/data/'):
            # Obtener datos de una entidad
            entity = path.split('/')[-1]
            if entity in self.sync_manager.entities:
                success, data = self.sync_manager.get_entity_data(entity, force_refresh='refresh' in query)
                if success:
                    self._set_headers()
                    self.wfile.write(json.dumps(data).encode())
                else:
                    self._set_headers(404)
                    self.wfile.write(json.dumps({'error': f'No se encontraron datos para {entity}'}).encode())
            else:
                self._set_headers(404)
                self.wfile.write(json.dumps({'error': f'Entidad no válida: {entity}'}).encode())
        
        else:
            # Ruta no encontrada
            self._set_headers(404)
            self.wfile.write(json.dumps({'error': 'Ruta no encontrada'}).encode())
    
    def do_POST(self):
        """Maneja las peticiones POST"""
        # Parsear la ruta
        parsed_path = urllib.parse.urlparse(self.path)
        path = parsed_path.path
        
        # Verificar autenticación
        if not self._check_auth():
            self._set_headers(401)
            self.wfile.write(json.dumps({'error': 'No autorizado'}).encode())
            return
        
        # Obtener datos del cuerpo
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        
        try:
            data = json.loads(post_data.decode())
        except json.JSONDecodeError:
            self._set_headers(400)
            self.wfile.write(json.dumps({'error': 'JSON inválido'}).encode())
            return
        
        # Rutas de la API
        if path == '/api/sync/start':
            # Iniciar sincronización
            success, message = self.sync_manager.sync_now()
            if success:
                self._set_headers()
                self.wfile.write(json.dumps({'message': message}).encode())
            else:
                self._set_headers(500)
                self.wfile.write(json.dumps({'error': message}).encode())
        
        elif path.startswith('/api/data/'):
            # Crear o actualizar datos de una entidad
            parts = path.split('/')
            if len(parts) < 4:
                self._set_headers(400)
                self.wfile.write(json.dumps({'error': 'Ruta inválida'}).encode())
                return
            
            entity = parts[3]
            operation = 'create'
            
            if len(parts) > 4:
                # Si hay un ID, es una actualización
                operation = 'update'
                data['id'] = parts[4]
            
            if entity in self.sync_manager.entities:
                # Agregar cambio pendiente
                self.sync_manager.add_pending_change(entity, operation, data)
                self._set_headers()
                self.wfile.write(json.dumps({'message': f'{operation.capitalize()} pendiente para {entity}'}).encode())
            else:
                self._set_headers(404)
                self.wfile.write(json.dumps({'error': f'Entidad no válida: {entity}'}).encode())
        
        elif path == '/api/auth/login':
            # Iniciar sesión
            username = data.get('username', '')
            password = data.get('password', '')
            
            if not username or not password:
                self._set_headers(400)
                self.wfile.write(json.dumps({'error': 'Se requiere nombre de usuario y contraseña'}).encode())
                return
            
            success, result = self.api_client.login(username, password)
            if success:
                self._set_headers()
                self.wfile.write(json.dumps({
                    'token': self.api_client.token,
                    'refresh_token': self.api_client.refresh_token,
                    'user_info': self.api_client.current_user_info
                }).encode())
            else:
                self._set_headers(401)
                self.wfile.write(json.dumps({'error': 'Credenciales inválidas'}).encode())
        
        else:
            # Ruta no encontrada
            self._set_headers(404)
            self.wfile.write(json.dumps({'error': 'Ruta no encontrada'}).encode())
    
    def do_PUT(self):
        """Maneja las peticiones PUT"""
        # Parsear la ruta
        parsed_path = urllib.parse.urlparse(self.path)
        path = parsed_path.path
        
        # Verificar autenticación
        if not self._check_auth():
            self._set_headers(401)
            self.wfile.write(json.dumps({'error': 'No autorizado'}).encode())
            return
        
        # Obtener datos del cuerpo
        content_length = int(self.headers['Content-Length'])
        put_data = self.rfile.read(content_length)
        
        try:
            data = json.loads(put_data.decode())
        except json.JSONDecodeError:
            self._set_headers(400)
            self.wfile.write(json.dumps({'error': 'JSON inválido'}).encode())
            return
        
        # Rutas de la API
        if path.startswith('/api/data/'):
            # Actualizar datos de una entidad
            parts = path.split('/')
            if len(parts) < 5:  # /api/data/{entity}/{id}
                self._set_headers(400)
                self.wfile.write(json.dumps({'error': 'Ruta inválida'}).encode())
                return
            
            entity = parts[3]
            entity_id = parts[4]
            data['id'] = entity_id
            
            if entity in self.sync_manager.entities:
                # Agregar cambio pendiente
                self.sync_manager.add_pending_change(entity, 'update', data)
                self._set_headers()
                self.wfile.write(json.dumps({'message': f'Actualización pendiente para {entity} {entity_id}'}).encode())
            else:
                self._set_headers(404)
                self.wfile.write(json.dumps({'error': f'Entidad no válida: {entity}'}).encode())
        
        else:
            # Ruta no encontrada
            self._set_headers(404)
            self.wfile.write(json.dumps({'error': 'Ruta no encontrada'}).encode())
    
    def do_DELETE(self):
        """Maneja las peticiones DELETE"""
        # Parsear la ruta
        parsed_path = urllib.parse.urlparse(self.path)
        path = parsed_path.path
        
        # Verificar autenticación
        if not self._check_auth():
            self._set_headers(401)
            self.wfile.write(json.dumps({'error': 'No autorizado'}).encode())
            return
        
        # Rutas de la API
        if path.startswith('/api/data/'):
            # Eliminar datos de una entidad
            parts = path.split('/')
            if len(parts) < 5:  # /api/data/{entity}/{id}
                self._set_headers(400)
                self.wfile.write(json.dumps({'error': 'Ruta inválida'}).encode())
                return
            
            entity = parts[3]
            entity_id = parts[4]
            
            if entity in self.sync_manager.entities:
                # Agregar cambio pendiente
                self.sync_manager.add_pending_change(entity, 'delete', {'id': entity_id})
                self._set_headers()
                self.wfile.write(json.dumps({'message': f'Eliminación pendiente para {entity} {entity_id}'}).encode())
            else:
                self._set_headers(404)
                self.wfile.write(json.dumps({'error': f'Entidad no válida: {entity}'}).encode())
        
        else:
            # Ruta no encontrada
            self._set_headers(404)
            self.wfile.write(json.dumps({'error': 'Ruta no encontrada'}).encode())
    
    def _check_auth(self):
        """Verifica la autenticación del cliente"""
        # Obtener token de autorización
        auth_header = self.headers.get('Authorization', '')
        
        # Si no hay token, verificar si es una ruta pública
        if not auth_header:
            public_paths = ['/api/status', '/api/auth/login']
            return any(self.path.startswith(path) for path in public_paths)
        
        # Verificar token
        try:
            # Formato: "Bearer {token}"
            token_type, token = auth_header.split(' ', 1)
            if token_type.lower() != 'bearer':
                return False
            
            # Verificar que el token coincida con el token actual
            return token == self.api_client.token
        except:
            return False


class MobileAPIServer:
    """Servidor para la API móvil"""
    
    def __init__(self, api_client, sync_manager, host='localhost', port=8080, use_ssl=False):
        self.api_client = api_client
        self.sync_manager = sync_manager
        self.host = host
        self.port = port
        self.use_ssl = use_ssl
        self.server = None
        self.server_thread = None
        self.is_running = False
    
    def start(self):
        """Inicia el servidor"""
        if self.is_running:
            return False, "El servidor ya está en ejecución"
        
        try:
            # Crear manejador personalizado con acceso a api_client y sync_manager
            handler = lambda *args, **kwargs: MobileAPIHandler(*args, api_client=self.api_client, sync_manager=self.sync_manager, **kwargs)
            
            # Crear servidor
            self.server = socketserver.ThreadingTCPServer((self.host, self.port), handler)
            
            # Configurar SSL si es necesario
            if self.use_ssl:
                cert_path = os.path.join(os.path.dirname(__file__), 'ssl', 'cert.pem')
                key_path = os.path.join(os.path.dirname(__file__), 'ssl', 'key.pem')
                
                if not os.path.exists(cert_path) or not os.path.exists(key_path):
                    return False, "No se encontraron los certificados SSL"
                
                self.server.socket = ssl.wrap_socket(
                    self.server.socket,
                    keyfile=key_path,
                    certfile=cert_path,
                    server_side=True
                )
            
            # Iniciar servidor en un hilo separado
            self.server_thread = threading.Thread(target=self.server.serve_forever)
            self.server_thread.daemon = True
            self.server_thread.start()
            
            self.is_running = True
            return True, f"Servidor iniciado en {self.host}:{self.port}"
        
        except Exception as e:
            error_msg = f"Error al iniciar el servidor: {str(e)}"
            print(error_msg)
            return False, error_msg
    
    def stop(self):
        """Detiene el servidor"""
        if not self.is_running:
            return False, "El servidor no está en ejecución"
        
        try:
            self.server.shutdown()
            self.server.server_close()
            self.is_running = False
            return True, "Servidor detenido"
        except Exception as e:
            error_msg = f"Error al detener el servidor: {str(e)}"
            print(error_msg)
            return False, error_msg
    
    def get_status(self):
        """Obtiene el estado del servidor"""
        return {
            'is_running': self.is_running,
            'host': self.host,
            'port': self.port,
            'use_ssl': self.use_ssl
        }

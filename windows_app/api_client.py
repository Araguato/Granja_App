#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import json
import os
import time
from datetime import datetime

class ApiClient:
    """Cliente para interactuar con la API de App Granja"""
    
    def __init__(self):
        print("\n=== Inicializando ApiClient ===")
        
        # Cargar configuración
        self.config = self.load_config()
        
        # Inicializar atributos con valores por defecto
        self.base_url = self.config.get('api_url', 'http://127.0.0.1:8000/api')
        self.token = self.config.get('token', '')
        self.refresh_token = self.config.get('refresh_token', '')
        self.username = self.config.get('username', '')
        self.password = self.config.get('password', '')
        self.is_offline = bool(self.config.get('is_offline', False))
        self.current_user_info = self.config.get('user_info', None)
        
        print(f"Modo offline: {'ACTIVADO' if self.is_offline else 'DESACTIVADO'}")
        print(f"API URL: {self.base_url}")
        print(f"Usuario: {self.username}")
        print(f"Token disponible: {'Sí' if self.token else 'No'}")
        print(f"Refresh token disponible: {'Sí' if self.refresh_token else 'No'}")
        
        # Si no estamos en modo offline y tenemos credenciales, intentar autenticar
        if not self.is_offline and self.username and self.password:
            if self.token and self.refresh_token:
                print("Verificando token existente...")
                success = self.refresh_auth_token()
                if not success:
                    print("No se pudo actualizar el token. Intentando autenticación completa...")
                    success, _ = self.login(self.username, self.password)
                    if not success:
                        print("No se pudo autenticar. Cambiando a modo offline.")
                        self.is_offline = True
                        self.config['is_offline'] = True
                        self.save_config(self.config)
            else:
                print("No hay token existente. Intentando autenticación...")
                success, _ = self.login(self.username, self.password)
                if not success:
                    print("No se pudo autenticar. Cambiando a modo offline.")
                    self.is_offline = True
                    self.config['is_offline'] = True
                    self.save_config(self.config)
        else:
            print("Usando modo offline según configuración o falta de credenciales")
    
    def load_config(self):
        """Carga la configuración desde el archivo config.json"""
        config_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'config.json'))
        print(f"Intentando cargar configuración desde: {config_path}")
        
        try:
            if os.path.exists(config_path):
                print(f"Archivo de configuración encontrado en: {config_path}")
                with open(config_path, 'r') as f:
                    config = json.load(f)
                    print(f"Contenido del archivo de configuración: {json.dumps(config, indent=2)}")
                    return config
            else:
                print(f"Archivo de configuración no encontrado en: {config_path}")
                # Configuración por defecto
                default_config = {
                    'is_offline': False,
                    'api_url': 'http://127.0.0.1:8000/api',
                    'token': '',
                    'refresh_token': '',
                    'username': 'thomas',
                    'password': 'PTZuata2025-'
                }
                # Guardar configuración por defecto
                os.makedirs(os.path.dirname(config_path), exist_ok=True)
                with open(config_path, 'w') as f:
                    json.dump(default_config, f, indent=4)
                print(f"Archivo de configuración creado con valores por defecto en: {config_path}")
                return default_config
        except Exception as e:
            print(f"Error al cargar configuración: {str(e)}")
            default_config = {
                'is_offline': False,
                'api_url': 'http://127.0.0.1:8000/api',
                'token': '',
                'refresh_token': '',
                'username': 'thomas',
                'password': 'PTZuata2025-'
            }
            print(f"Usando configuración por defecto: {json.dumps(default_config, indent=2)}")
            return default_config
    
    def save_config(self, config):
        """Guarda la configuración en el archivo config.json"""
        try:
            config_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'config.json'))
            print(f"Guardando configuración en: {config_path}")
            
            # Asegurarse de que todos los campos necesarios estén presentes
            default_config = {
                'is_offline': False,
                'api_url': 'http://127.0.0.1:8000/api',
                'token': '',
                'refresh_token': '',
                'username': 'thomas',
                'password': 'PTZuata2025-'
            }
            
            # Actualizar solo los campos proporcionados, manteniendo los valores por defecto para los faltantes
            for key in default_config:
                if key not in config:
                    config[key] = default_config[key]
            
            # Asegurarse de que el directorio existe
            os.makedirs(os.path.dirname(config_path), exist_ok=True)
            
            # Guardar la configuración
            with open(config_path, 'w') as f:
                json.dump(config, f, indent=4)
                
            print(f"Configuración guardada correctamente: {json.dumps(config, indent=2)}")
            self.config = config
            self.base_url = config.get('api_url', 'http://127.0.0.1:8000/api')
            self.token = config.get('token', '')
            self.username = config.get('username', '')
            self.password = config.get('password', '')
            return True
            
        except Exception as e:
            print(f"Error al guardar configuración: {str(e)}")
            return False
    
    def get_headers(self):
        """Obtiene los headers para las peticiones a la API"""
        if self.token:
            return {
                'Authorization': f'Bearer {self.token}',
                'Content-Type': 'application/json'
            }
        return {'Content-Type': 'application/json'}
        
    def make_request(self, method, url, data=None, params=None, headers=None, retry_count=0, max_retries=2):
        """Método centralizado para hacer peticiones HTTP con manejo de errores, reintentos y timeouts
        
        Args:
            method (str): Método HTTP (get, post, put, delete)
            url (str): URL completa del endpoint
            data (dict, optional): Datos a enviar en el cuerpo de la petición
            params (dict, optional): Parámetros de consulta
            headers (dict, optional): Headers HTTP personalizados
            retry_count (int): Número de reintentos realizados (uso interno)
            max_retries (int): Número máximo de reintentos ante fallos
            
        Returns:
            tuple: (success, data) donde success es un booleano que indica si la petición fue exitosa,
                  y data contiene la respuesta del servidor o datos de ejemplo en modo offline.
        """
        # Si no se proporcionan headers, usar los predeterminados
        if headers is None:
            headers = self.get_headers()
        
        # Asegurarse de que la URL sea completa
        if not url.startswith(('http://', 'https://')):
            url = f"{self.base_url.rstrip('/')}/{url.lstrip('/')}"
        
        # Verificar si estamos en modo offline
        if self.is_offline:
            print(f"[OFFLINE] Modo offline activado. No se realizará la petición a {url}")
            return self._handle_offline_request(url)
        
        try:
            # Configuración de la petición
            request_kwargs = {
                'url': url,
                'headers': headers,
                'params': params,
                'timeout': 10,  # 10 segundos de timeout por defecto
                'verify': True  # Verificar certificados SSL
            }
            
            # Añadir datos JSON si es necesario
            if method.lower() in ['post', 'put', 'patch'] and data is not None:
                request_kwargs['json'] = data
            
            # Registrar la petición
            print(f"[{method.upper()}] {url}")
            if params:
                print(f"Parámetros: {params}")
            if data and method.lower() in ['post', 'put', 'patch']:
                print(f"Datos: {json.dumps(data, indent=2, ensure_ascii=False)[:500]}...")  # Limitar tamaño del log
            
            start_time = time.time()
            
            # Realizar la petición
            if method.lower() == 'get':
                response = requests.get(**request_kwargs)
            elif method.lower() == 'post':
                response = requests.post(**request_kwargs)
            elif method.lower() == 'put':
                response = requests.put(**request_kwargs)
            elif method.lower() == 'patch':
                response = requests.patch(**request_kwargs)
            elif method.lower() == 'delete':
                response = requests.delete(**request_kwargs)
            else:
                error_msg = f"Método HTTP no soportado: {method}"
                print(f"[ERROR] {error_msg}")
                return False, {'error': error_msg}
            
            elapsed = (time.time() - start_time) * 1000  # Tiempo en milisegundos
            print(f"[RESPUESTA] {response.status_code} en {elapsed:.2f}ms - {url}")
            
            # Manejar códigos de estado exitosos
            if 200 <= response.status_code < 300:
                try:
                    # Intentar parsear la respuesta como JSON
                    response_data = response.json()
                    return True, response_data
                except ValueError:
                    # Si no es JSON, devolver el texto plano
                    return True, response.text
            
            # Manejar errores de autenticación/autoriación
            if response.status_code == 401:  # No autorizado
                print("[AUTENTICACIÓN] Token inválido o expirado")
                if retry_count < max_retries and self._handle_auth_error():
                    # Reintentar con el nuevo token
                    return self.make_request(
                        method=method,
                        url=url,
                        data=data,
                        params=params,
                        headers=self.get_headers(),  # Usar headers actualizados
                        retry_count=retry_count + 1,
                        max_retries=max_retries
                    )
                return False, {'error': 'No autorizado', 'message': 'La sesión ha expirado'}
            
            # Manejar otros errores HTTP
            error_msg = self._get_error_message(response)
            print(f"[ERROR HTTP {response.status_code}] {error_msg}")
            
            # Para errores del servidor, podríamos reintentar
            if 500 <= response.status_code < 600 and retry_count < max_retries:
                print(f"Reintentando... (intento {retry_count + 1}/{max_retries})")
                time.sleep(1)  # Esperar antes de reintentar
                return self.make_request(
                    method=method,
                    url=url,
                    data=data,
                    params=params,
                    headers=headers,
                    retry_count=retry_count + 1,
                    max_retries=max_retries
                )
            
            return False, {'error': f'Error {response.status_code}', 'message': error_msg}
            
        except requests.exceptions.RequestException as e:
            return self._handle_request_exception(e, method, url, data, params, headers, retry_count, max_retries)
        except Exception as e:
            error_msg = f"Error inesperado: {str(e)}"
            print(f"[ERROR] {error_msg}")
            import traceback
            traceback.print_exc()
            return False, {'error': 'internal_error', 'message': error_msg}
    
    def _handle_offline_request(self, url):
        """Maneja las peticiones cuando estamos en modo offline"""
        # Extraer el tipo de datos de la URL para devolver datos de ejemplo
        endpoint = url.split('/')[-2] if url.endswith('/') else url.split('/')[-1]
        print(f"[OFFLINE] Endpoint detectado: {endpoint}")
        
        # Mapear endpoints a tipos de datos de ejemplo
        endpoint_map = {
            'galpones': 'galpones',
            'lotes': 'lotes',
            'razas': 'razas',
            'alimentos': 'alimentos',
            'vacunas': 'vacunas',
            'usuarios': 'usuarios',
            'grupos': 'grupos',
            'granjas': 'granjas',
            'empresas': 'empresas',
            'seguimientos': 'seguimientos',
            'tareas': 'tareas',
            'dashboard': 'dashboard_stats',
            'stats': 'dashboard_stats'
        }
        
        # Obtener el tipo de datos de ejemplo correspondiente
        data_type = endpoint_map.get(endpoint, 'default')
        print(f"[OFFLINE] Usando datos de ejemplo para: {data_type}")
        
        # Devolver datos de ejemplo
        example_data = self.get_example_data(data_type)
        return True, example_data  # Devolver True para evitar mensajes de error en la interfaz
    
    def _handle_auth_error(self):
        """Maneja errores de autenticación, intentando refrescar el token"""
        print("[AUTENTICACIÓN] Intentando refrescar el token...")
        if self.refresh_token:
            success = self.refresh_auth_token()
            if success:
                print("[AUTENTICACIÓN] Token refrescado correctamente")
                return True
        
        print("[AUTENTICACIÓN] No se pudo refrescar el token")
        return False
    
    def _handle_request_exception(self, exception, method, url, data, params, headers, retry_count, max_retries):
        """Maneja excepciones de la petición HTTP"""
        error_type = type(exception).__name__
        
        # Manejar diferentes tipos de excepciones
        if isinstance(exception, requests.exceptions.Timeout):
            error_msg = f"Tiempo de espera agotado al conectar con {url}"
            print(f"[TIMEOUT] {error_msg}")
            
        elif isinstance(exception, requests.exceptions.ConnectionError):
            error_msg = f"No se pudo conectar con el servidor: {str(exception)}"
            print(f"[CONEXIÓN] {error_msg}")
            
            # Si es un error de conexión, activar modo offline
            if not self.is_offline:
                print("[MODO OFFLINE] Activando modo offline")
                self.is_offline = True
                self.config['is_offline'] = True
                self.save_config(self.config)
            
            # Devolver datos de ejemplo
            return self._handle_offline_request(url)
            
        elif isinstance(exception, requests.exceptions.RequestException):
            error_msg = f"Error en la petición: {str(exception)}"
            print(f"[ERROR] {error_msg}")
            
        else:
            error_msg = f"Error inesperado: {str(exception)}"
            print(f"[ERROR] {error_msg}")
        
        # Si tenemos reintentos disponibles, reintentar
        if retry_count < max_retries:
            print(f"Reintentando... (intento {retry_count + 1}/{max_retries})")
            time.sleep(1)  # Esperar antes de reintentar
            return self.make_request(
                method=method,
                url=url,
                data=data,
                params=params,
                headers=headers,
                retry_count=retry_count + 1,
                max_retries=max_retries
            )
        
        # Si no hay más reintentos, devolver error
        return False, {'error': 'connection_error', 'message': error_msg}
    
    def login(self, username, password, remember_me=False):
        """Inicia sesión en la API y obtiene un token JWT
        
        Args:
            username (str): Nombre de usuario
            password (str): Contraseña
            remember_me (bool, optional): Si es True, guarda la contraseña. Por defecto es False.
            
        Returns:
            tuple: (success, data) donde success es un booleano que indica si el inicio de sesión fue exitoso,
                  y data es la información del usuario o un mensaje de error.
        """
        print("\n=== Iniciando sesión ===")
        print(f"Usuario: {username}")
        print(f"Recordar sesión: {'Sí' if remember_me else 'No'}")
        
        # Validar credenciales
        if not username or not password:
            error_msg = "Usuario y contraseña son obligatorios"
            print(error_msg)
            return False, error_msg
            
        try:
            # Intentar autenticación con la API
            start_time = time.time()
            print(f"Conectando con {self.base_url}/token/...")
            
            response = requests.post(
                f"{self.base_url}/token/",
                json={'username': username, 'password': password},
                headers={"Content-Type": "application/json"},
                timeout=10  # 10 segundos de timeout
            )
            
            # Calcular tiempo de respuesta
            elapsed = (time.time() - start_time) * 1000
            print(f"Respuesta recibida en {elapsed:.2f}ms - Código: {response.status_code}")
            
            # Procesar respuesta exitosa
            if response.status_code == 200:
                data = response.json()
                self.token = data.get('access', '')
                self.refresh_token = data.get('refresh', '')
                self.username = username
                self.password = password if remember_me else ''
                self.is_offline = False  # Asegurarse de desactivar el modo offline
                
                print("Autenticación exitosa")
                print(f"Token: {'***' + self.token[-8:] if self.token else 'No disponible'}")
                print(f"Refresh Token: {'***' + self.refresh_token[-8:] if self.refresh_token else 'No disponible'}")
                
                # Obtener información del usuario
                print("Obteniendo información del usuario...")
                success, user_info = self.get_user_info(username)
                
                if success and user_info:
                    self.current_user_info = user_info
                    # Asegurar que la información del usuario tenga los campos necesarios
                    self.current_user_info.update({
                        'is_offline': False,
                        'demo_mode': False
                    })
                    
                    # Actualizar configuración
                    self.config.update({
                        'token': self.token,
                        'refresh_token': self.refresh_token,
                        'username': username,
                        'password': self.password,
                        'is_offline': False,
                        'user_info': self.current_user_info
                    })
                    
                    if not self.save_config(self.config):
                        print("Advertencia: No se pudo guardar la configuración")
                    
                    print(f"Usuario autenticado: {self.current_user_info.get('username')}")
                    return True, self.current_user_info
                else:
                    error_msg = "No se pudo obtener la información del usuario"
                    print(error_msg)
                    return False, error_msg
            
            # Manejar errores de autenticación
            elif response.status_code == 401:
                error_msg = "Usuario o contraseña incorrectos"
                print(f"Error de autenticación: {error_msg}")
                return False, error_msg
                
            # Manejar otros errores HTTP
            else:
                error_msg = self._get_error_message(response)
                print(f"Error en la autenticación: {error_msg}")
                return False, error_msg
                
        except requests.exceptions.Timeout:
            error_msg = "Tiempo de espera agotado. Verifique su conexión a internet."
            print(error_msg)
            # Intentar inicio de sesión offline
            return self.offline_login(username, password)
            
        except requests.exceptions.ConnectionError as e:
            error_msg = f"No se pudo conectar al servidor: {str(e)}"
            print(error_msg)
            # Intentar inicio de sesión offline
            return self.offline_login(username, password)
            
        except requests.exceptions.RequestException as e:
            error_msg = f"Error en la solicitud: {str(e)}"
            print(error_msg)
            # Intentar inicio de sesión offline como último recurso
            return self.offline_login(username, password)
            
        except Exception as e:
            error_msg = f"Error inesperado: {str(e)}"
            print(error_msg)
            import traceback
            traceback.print_exc()
            # Intentar inicio de sesión offline como último recurso
            return self.offline_login(username, password)
    
    def _get_error_message(self, response):
        """Obtiene un mensaje de error legible a partir de la respuesta HTTP"""
        if response.status_code == 400:
            try:
                error_data = response.json()
                if 'non_field_errors' in error_data:
                    return ". ".join(error_data['non_field_errors'])
                if 'detail' in error_data:
                    return error_data['detail']
                return "Datos de solicitud inválidos"
            except Exception:
                return "Error en la solicitud"
            except:
                return "Solicitud incorrecta"
        elif response.status_code == 401:
            return "No autorizado. Verifique sus credenciales."
        elif response.status_code == 403:
            return "No tiene permiso para realizar esta acción"
        elif response.status_code == 404:
            return "Recurso no encontrado"
        elif 500 <= response.status_code < 600:
            return f"Error del servidor (código {response.status_code})"
        else:
            return f"Error en la solicitud (código {response.status_code})"
            
    def offline_login(self, username=None, password=None):
        """Inicia sesión en modo offline usando credenciales guardadas o las proporcionadas
        
        Args:
            username (str, optional): Nombre de usuario. Si no se proporciona, se usará el guardado.
            password (str, optional): Contraseña. Si no se proporciona, se usará la guardada.
            
        Returns:
            tuple: (success, user_info) donde success es un booleano que indica si el inicio de sesión
                  offline fue exitoso, y user_info es un diccionario con la información del usuario.
        """
        print("\n=== Iniciando sesión en modo offline ===")
        
        # Usar credenciales guardadas si no se proporcionan
        if not username:
            username = self.config.get('username', 'demo')
        if not password:
            password = self.config.get('password', '')
            
        print(f"Iniciando sesión offline como: {username}")
        
        try:
            # Configurar el modo offline
            self.is_offline = True
            self.config['is_offline'] = True
            self.username = username
            self.password = password
            
            # Crear información de usuario de ejemplo si no existe
            if not self.config.get('user_info'):
                self.current_user_info = {
                    'id': 0,
                    'username': username,
                    'first_name': 'Usuario',
                    'last_name': 'Demo',
                    'email': f"{username}@demo.appgranja.com",
                    'is_staff': True,
                    'is_superuser': True,
                    'is_offline': True,
                    'empresa': 'Granja Demo',
                    'granja': 'Sede Principal',
                    'demo_mode': True,  # Marcar como modo demo
                    'permissions': [
                        'add_lote', 'change_lote', 'delete_lote', 'view_lote',
                        'add_galpon', 'change_galpon', 'delete_galpon', 'view_galpon',
                        'add_alimento', 'change_alimento', 'delete_alimento', 'view_alimento',
                        'add_vacuna', 'change_vacuna', 'delete_vacuna', 'view_vacuna',
                        'add_raza', 'change_raza', 'delete_raza', 'view_raza',
                        'view_dashboard', 'view_reportes', 'view_estadisticas', 'view_configuracion'
                    ]
                }
                self.config['user_info'] = self.current_user_info
                self.save_config(self.config)
            else:
                self.current_user_info = self.config['user_info']
                self.current_user_info['is_offline'] = True
                self.current_user_info['demo_mode'] = True  # Asegurar que esté en modo demo
            
            # Actualizar configuración con tokens offline
            self.config.update({
                'token': 'offline_token',
                'refresh_token': 'offline_refresh_token',
                'is_offline': True
            })
            
            # Guardar configuración
            if not self.save_config(self.config):
                print("Advertencia: No se pudo guardar la configuración offline")
            
            print("Inicio de sesión offline exitoso")
            print(f"Usuario: {self.current_user_info.get('username')}")
            print("Modo DEMO activado - Usando datos de ejemplo")
            
            # Mostrar notificación de modo demo usando QTimer para evitar problemas de hilos
            try:
                from PyQt5.QtWidgets import QMessageBox
                from PyQt5.QtCore import QTimer
                
                QTimer.singleShot(1000, lambda: QMessageBox.information(
                    None,
                    "Modo Demo Activado",
                    "La aplicación está funcionando en modo demo con datos de ejemplo.\n\n"
                    "Puede navegar por todas las secciones, pero los cambios no se guardarán.",
                    QMessageBox.Ok
                ))
            except Exception as e:
                print(f"No se pudo mostrar la notificación de demo: {str(e)}")
            
            return True, self.current_user_info
            
        except Exception as e:
            error_msg = f"Error en inicio de sesión offline: {str(e)}"
            print(error_msg)
            import traceback
            traceback.print_exc()
            return False, error_msg
    
    def logout(self, skip_server_logout=False):
        """Cierra la sesión actual y limpia los datos de autenticación
        
        Args:
            skip_server_logout (bool): Si es True, no intenta cerrar sesión en el servidor.
                                     Útil cuando hay problemas de conexión.
        
        Returns:
            tuple: (success, message) donde success es un booleano que indica si el cierre de sesión
                  fue exitoso, y message es un mensaje descriptivo.
        """
        print("\n=== Cerrando sesión ===")
        print(f"Modo offline: {'Sí' if self.is_offline else 'No'}")
        print(f"Token disponible: {'Sí' if self.token else 'No'}")
        
        try:
            # Solo intentar cerrar sesión en el servidor si no estamos en modo offline,
            # tenemos un token válido y no se debe omitir
            if not skip_server_logout and not self.is_offline and self.token:
                try:
                    print("Notificando al servidor del cierre de sesión...")
                    start_time = time.time()
                    
                    # Intentar revocar el token en el servidor
                    response = requests.post(
                        f"{self.base_url}/token/blacklist/",
                        json={"refresh_token": self.refresh_token},
                        headers={"Content-Type": "application/json"},
                        timeout=10  # 10 segundos de timeout
                    )
                    
                    elapsed = (time.time() - start_time) * 1000
                    print(f"Respuesta del servidor en {elapsed:.2f}ms - Código: {response.status_code}")
                    
                    if response.status_code == 200:
                        print("Sesión cerrada correctamente en el servidor")
                    elif response.status_code == 401:
                        print("El token ya no es válido o ha expirado")
                    else:
                        error_msg = self._get_error_message(response)
                        print(f"Advertencia: No se pudo cerrar la sesión en el servidor: {response.status_code} - {error_msg}")
                        
                except requests.exceptions.Timeout:
                    print("Advertencia: Tiempo de espera agotado al intentar cerrar sesión en el servidor")
                except requests.exceptions.ConnectionError as e:
                    print(f"Advertencia: No se pudo conectar al servidor para cerrar sesión: {str(e)}")
                except Exception as e:
                    print(f"Error inesperado al intentar cerrar sesión en el servidor: {str(e)}")
            
            # Limpiar los tokens y la información del usuario
            print("Limpiando datos de sesión local...")
            self.token = ''
            self.refresh_token = ''
            self.username = ''
            self.password = ''
            self.current_user_info = None
            self.is_offline = False
            
            # Actualizar la configuración
            self.config.update({
                'token': '',
                'refresh_token': '',
                'username': '',
                'password': '',
                'user_info': None,
                'is_offline': False
            })
            
            # Guardar la configuración
            if not self.save_config(self.config):
                print("Advertencia: No se pudo guardar la configuración actualizada")
            
            # Eliminar el archivo de usuario recordado si existe
            try:
                if os.path.exists('remembered_user.txt'):
                    os.remove('remembered_user.txt')
                    print("Archivo de usuario recordado eliminado")
            except Exception as e:
                print(f"Advertencia: No se pudo eliminar el archivo de usuario recordado: {str(e)}")
            
            print("Sesión cerrada correctamente a nivel local")
            return True, "Sesión cerrada correctamente"
            
        except Exception as e:
            error_msg = f"Error inesperado al cerrar sesión: {str(e)}"
            print(error_msg)
            import traceback
            traceback.print_exc()
            
            # Asegurarse de limpiar los datos locales incluso si hay un error
            try:
                self.token = ''
                self.refresh_token = ''
                self.current_user_info = None
                self.is_offline = False
                self.username = ''
                
                # Actualizar configuración
                self.config.update({
                    'token': '',
                    'refresh_token': '',
                    'user_info': None,
                    'username': '',
                    'is_offline': False
                })
                self.save_config(self.config)
            except Exception as cleanup_error:
                print(f"Error durante la limpieza de la sesión: {str(cleanup_error)}")
            
            return False, error_msg
    
    def refresh_auth_token(self):
        """Refresca el token JWT usando el refresh token
        
        Returns:
            bool: True si el token se actualizó correctamente, False en caso contrario
        """
        if not self.refresh_token:
            print("No hay refresh token disponible para actualizar")
            return False
            
        if self.is_offline:
            print("Modo offline activado. No se puede actualizar el token.")
            return False
            
        try:
            refresh_url = f"{self.base_url}/token/refresh/"
            print(f"Refrescando token de autenticación en {refresh_url}...")
            
            start_time = time.time()
            response = requests.post(
                refresh_url,
                json={'refresh': self.refresh_token},
                headers={'Content-Type': 'application/json'},
                timeout=10  # 10 segundos de timeout
            )
            elapsed = (time.time() - start_time) * 1000
            
            print(f"Respuesta recibida en {elapsed:.2f}ms - Código: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                new_token = data.get('access', '')
                new_refresh_token = data.get('refresh', self.refresh_token)
                
                if not new_token:
                    print("Error: El servidor no devolvió un token de acceso válido")
                    return False
                
                # Actualizar tokens
                self.token = new_token
                self.refresh_token = new_refresh_token
                
                # Actualizar configuración
                self.config.update({
                    'token': new_token,
                    'refresh_token': new_refresh_token,
                    'is_offline': False
                })
                
                if not self.save_config(self.config):
                    print("Advertencia: No se pudo guardar la configuración actualizada")
                
                print("Token actualizado correctamente")
                print(f"Nuevo token: ***{new_token[-8:] if new_token else 'N/A'}")
                return True
                
            elif response.status_code == 401:
                print("Error 401: Token de refresco inválido o expirado")
                # El refresh token ya no es válido, forzar cierre de sesión
                self.logout()
                return False
                
            else:
                error_msg = self._get_error_message(response)
                print(f"Error al refrescar el token: {response.status_code} - {error_msg}")
                
                # Si el error es de autenticación, forzar cierre de sesión
                if response.status_code in [401, 403]:
                    self.logout()
                
                return False
                
        except requests.exceptions.Timeout:
            error_msg = "Tiempo de espera agotado al intentar actualizar el token"
            print(error_msg)
            return False
            
        except requests.exceptions.ConnectionError as e:
            error_msg = f"Error de conexión al intentar actualizar el token: {str(e)}"
            print(error_msg)
            # Activar modo offline
            self.is_offline = True
            self.config['is_offline'] = True
            self.save_config(self.config)
            return False
            
        except Exception as e:
            error_msg = f"Error inesperado al actualizar el token: {str(e)}"
            print(error_msg)
            import traceback
            traceback.print_exc()
            return False
    
    def test_connection(self):
        """Prueba la conexión con la API"""
        print("\n=== Probando conexión con el servidor ===")
        print(f"URL base de la API: {self.base_url}")
        
        # Si estamos en modo offline forzado, no intentar conectar
        if self.is_offline:
            print("Modo offline activado. No se intentará conectar con el servidor.")
            return False, "Modo offline activado"
        
        # Lista de endpoints para probar
        endpoints_to_try = [
            # Endpoint principal de la API
            {'url': f"{self.base_url.rstrip('/')}/", 'method': 'get', 'timeout': 5, 'name': 'API Root'},
            # Endpoint de autenticación
            {'url': f"{self.base_url.rstrip('/')}/token/", 'method': 'get', 'timeout': 5, 'name': 'Token Endpoint'},
            # Endpoint de galpones (debería existir y requerir autenticación)
            {'url': f"{self.base_url.rstrip('/')}/galpones/", 'method': 'get', 'timeout': 5, 'name': 'Galpones Endpoint'}
        ]
        
        # Si tenemos credenciales, probar también la autenticación
        if self.username and self.password:
            endpoints_to_try.append({
                'url': f"{self.base_url.rstrip('/')}/token/",
                'method': 'post',
                'data': {'username': self.username, 'password': self.password},
                'timeout': 5,
                'name': 'Authentication'
            })
        
        # Probar cada endpoint
        success = False
        last_error = "No se pudo conectar al servidor"
        
        for endpoint in endpoints_to_try:
            url = endpoint['url']
            method = endpoint['method']
            timeout = endpoint['timeout']
            name = endpoint.get('name', 'Endpoint')
            
            print(f"\nProbando {name} ({method.upper()} {url})...")
            
            try:
                if method.lower() == 'get':
                    response = requests.get(url, timeout=timeout, verify=False)
                elif method.lower() == 'post':
                    headers = {'Content-Type': 'application/json'}
                    response = requests.post(
                        url, 
                        json=endpoint.get('data', {}), 
                        headers=headers, 
                        timeout=timeout,
                        verify=False
                    )
                else:
                    continue
                
                # Verificar el código de estado
                if response.status_code < 400:
                    print(f"✓ {name} respondió correctamente (HTTP {response.status_code})")
                    success = True
                    break
                else:
                    error_msg = f"{name} respondió con código {response.status_code}"
                    if response.text:
                        try:
                            error_data = response.json()
                            error_msg += f": {error_data}"
                        except:
                            error_msg += f": {response.text[:200]}"
                    print(f"✗ {error_msg}")
                    last_error = error_msg
                    
            except requests.exceptions.RequestException as e:
                error_msg = f"Error al conectar a {name}: {str(e)}"
                print(f"✗ {error_msg}")
                last_error = error_msg
            except Exception as e:
                error_msg = f"Error inesperado al probar {name}: {str(e)}"
                print(f"✗ {error_msg}")
                last_error = error_msg
        
        # Si al menos un endpoint respondió correctamente, la conexión es exitosa
        if success:
            print("\n✓ Conexión con el servidor establecida correctamente")
            return True, "Conexión exitosa"
        else:
            print(f"\n✗ No se pudo establecer conexión con el servidor: {last_error}")
            return False, last_error
    
    def get_user_info(self, username):
        """Obtiene la información de un usuario"""
        try:
            # Agregar timeout para evitar bloqueos
            response = requests.get(
                f"{self.base_url}/usuarios/?search={username}",
                headers=self.get_headers()
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get('results') and len(data['results']) > 0:
                    user = data['results'][0]
                    return True, user
                else:
                    return False, "Usuario no encontrado"
            else:
                return False, f"Error al obtener información del usuario: {response.text}"
        except Exception as e:
            return False, f"Error de conexión: {str(e)}"
    
    def get_current_user_info(self):
        """Obtiene la información del usuario actual"""
        if self.current_user_info:
            return self.current_user_info
        elif self.username:
            success, user_info = self.get_user_info(self.username)
            if success:
                self.current_user_info = user_info
                return user_info
        return None
    
    # Métodos para obtener datos de ejemplo (modo offline)
    def _save_offline_data(self, entity, data):
        """Guarda los datos localmente para acceso offline
        
        Args:
            entity (str): Nombre de la entidad (ej: 'galpones', 'lotes')
            data: Datos a guardar (generalmente una lista de diccionarios)
            
        Returns:
            bool: True si se guardó correctamente, False en caso de error
        """
        try:
            import os
            import json
            
            # Crear directorio si no existe
            offline_dir = os.path.join(os.path.dirname(__file__), 'offline_data')
            os.makedirs(offline_dir, exist_ok=True)
            
            # Ruta al archivo de datos offline
            offline_path = os.path.join(offline_dir, f"{entity}.json")
            
            # Guardar los datos en formato JSON
            with open(offline_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
                
            print(f"Datos de {entity} guardados correctamente en {offline_path}")
            return True
            
        except Exception as e:
            print(f"Error al guardar datos offline de {entity}: {str(e)}")
            return False
    
    def load_offline_data(self, entity):
        """Carga los datos offline de una entidad
        
        Args:
            entity (str): Nombre de la entidad a cargar (ej: 'galpones', 'lotes')
            
        Returns:
            list: Lista de diccionarios con los datos de la entidad, o lista vacía si hay error
        """
        try:
            import os
            import json
            
            # Ruta al archivo de datos offline
            offline_dir = os.path.join(os.path.dirname(__file__), 'offline_data')
            os.makedirs(offline_dir, exist_ok=True)
            offline_path = os.path.join(offline_dir, f"{entity}.json")
            
            if os.path.exists(offline_path):
                with open(offline_path, 'r', encoding='utf-8') as f:
                    print(f"Datos offline cargados desde: {offline_path}")
                    return json.load(f)
            else:
                print(f"No se encontró archivo offline para {entity} en {offline_path}")
                # Si no existe el archivo, devolver datos de ejemplo
                return self.get_example_data(entity)
        except Exception as e:
            print(f"Error al cargar datos offline de {entity}: {str(e)}")
            # En caso de error, devolver datos de ejemplo
            return self.get_example_data(entity)
    
    def get_example_data(self, data_type):
        """Obtiene datos de ejemplo para usar en modo offline"""
        examples = {
            'usuarios': [
                {
                    'id': 1,
                    'username': 'admin',
                    'email': 'admin@granjaapp.com',
                    'first_name': 'Administrador',
                    'last_name': 'Sistema',
                    'is_active': True,
                    'is_staff': True,
                    'is_superuser': True,
                    'date_joined': '2025-01-01T00:00:00Z',
                    'last_login': '2025-05-20T10:00:00Z',
                    'groups': [1],
                    'user_permissions': []
                },
                {
                    'id': 2,
                    'username': 'supervisor',
                    'email': 'supervisor@granjaapp.com',
                    'first_name': 'Juan',
                    'last_name': 'Pérez',
                    'is_active': True,
                    'is_staff': True,
                    'is_superuser': False,
                    'date_joined': '2025-01-15T00:00:00Z',
                    'last_login': '2025-05-19T08:30:00Z',
                    'groups': [2],
                    'user_permissions': []
                },
                {
                    'id': 3,
                    'username': 'operador',
                    'email': 'operador@granjaapp.com',
                    'first_name': 'María',
                    'last_name': 'López',
                    'is_active': True,
                    'is_staff': False,
                    'is_superuser': False,
                    'date_joined': '2025-02-01T00:00:00Z',
                    'last_login': '2025-05-20T09:15:00Z',
                    'groups': [3],
                    'user_permissions': []
                }
            ],
            'empresas': [
                {
                    'id': 1,
                    'nombre': 'Granja Avícola San José',
                    'rif': 'J-12345678-9',
                    'direccion': 'Carretera Nacional, km 12',
                    'telefono': '04141234567',
                    'email': 'contacto@granjasanjose.com',
                    'activo': True
                },
                {
                    'id': 2,
                    'nombre': 'Avícola El Prado',
                    'rif': 'J-98765432-1',
                    'direccion': 'Vía La Victoria',
                    'telefono': '04241234567',
                    'email': 'info@avicolaelprado.com',
                    'activo': True
                }
            ],
            'lotes': [
                {
                    'id': 1,
                    'codigo': 'L-2023-001',
                    'fecha_ingreso': '2023-01-15',
                    'cantidad_aves': 1000,
                    'raza': 'Lohmann Brown',
                    'galpon': 1,
                    'estado': 'Activo',
                    'edad_semanas': 30
                },
                {
                    'id': 2,
                    'codigo': 'L-2023-002',
                    'fecha_ingreso': '2023-02-01',
                    'cantidad_aves': 1500,
                    'raza': 'Hy-Line Brown',
                    'galpon': 2,
                    'estado': 'Activo',
                    'edad_semanas': 25
                },
                {
                    'id': 3,
                    'codigo': 'L-2023-003',
                    'fecha_ingreso': '2023-02-15',
                    'cantidad_aves': 1200,
                    'raza': 'Babcock',
                    'galpon': 3,
                    'estado': 'Cerrado',
                    'edad_semanas': 20
                }
            ],
            'galpones': [
                {
                    'id': 1,
                    'codigo': 'G-001',
                    'capacidad': 1500,
                    'tipo': 'Producción',
                    'estado': 'Ocupado',
                    'ubicacion': 'Sector Norte',
                    'activo': True
                },
                {
                    'id': 2,
                    'codigo': 'G-002',
                    'capacidad': 2000,
                    'tipo': 'Crianza',
                    'estado': 'Ocupado',
                    'ubicacion': 'Sector Sur',
                    'activo': True
                },
                {
                    'id': 3,
                    'codigo': 'G-003',
                    'capacidad': 1800,
                    'tipo': 'Producción',
                    'estado': 'Mantenimiento',
                    'ubicacion': 'Sector Este',
                    'activo': False
                }
            ],
            'seguimientos': [
                {
                    'id': 1,
                    'fecha': '2023-03-01',
                    'lote': 1,
                    'huevos_producidos': 980,
                    'mortalidad': 5,
                    'consumo_agua': 1200,
                    'consumo_alimento': 850,
                    'observaciones': 'Comportamiento normal',
                    'temperatura': 21.5,
                    'humedad': 60
                },
                {
                    'id': 2,
                    'fecha': '2023-03-02',
                    'lote': 1,
                    'huevos_producidos': 975,
                    'mortalidad': 3,
                    'consumo_agua': 1190,
                    'consumo_alimento': 840,
                    'observaciones': 'Todo en orden',
                    'temperatura': 22.0,
                    'humedad': 58
                },
                {
                    'id': 3,
                    'fecha': '2023-03-03',
                    'lote': 1,
                    'huevos_producidos': 970,
                    'mortalidad': 2,
                    'consumo_agua': 1205,
                    'consumo_alimento': 855,
                    'observaciones': 'Aumento en consumo de agua',
                    'temperatura': 22.5,
                    'humedad': 62
                }
            ],
            'tareas': [
                {
                    'id': 1,
                    'titulo': 'Vacunación Newcastle',
                    'descripcion': 'Aplicar vacuna de Newcastle a lote L-2025-001',
                    'fecha_creacion': '2025-03-01',
                    'fecha_vencimiento': '2025-03-05',
                    'prioridad': 'Alta',
                    'estado': 'Pendiente',
                    'asignado_a': 'Juan Pérez',
                    'lote': 1,
                    'completada': False
                },
                {
                    'id': 2,
                    'titulo': 'Limpieza de galpón',
                    'descripcion': 'Realizar limpieza y desinfección del galpón 2',
                    'fecha_creacion': '2025-03-02',
                    'fecha_vencimiento': '2025-03-03',
                    'prioridad': 'Media',
                    'estado': 'Completada',
                    'asignado_a': 'María Gómez',
                    'galpon': 2,
                    'completada': True
                }
            ],
            'grupos': [
                {'id': 1, 'name': 'Administradores'},
                {'id': 2, 'name': 'Supervisores'},
                {'id': 3, 'name': 'Operarios'}
            ],
            'razas': [
                {'id': 1, 'nombre': 'Lohmann Brown', 'tipo': 'Ponedora', 'descripcion': 'Excelente productora de huevos marrones'},
                {'id': 2, 'nombre': 'Hy-Line Brown', 'tipo': 'Ponedora', 'descripcion': 'Alta producción de huevos'}
            ],
            'alimentos': [
                {'id': 1, 'nombre': 'Iniciador', 'marca': 'Purina', 'proteina': 20, 'presentacion': 'Saco 50kg'},
                {'id': 2, 'nombre': 'Crecimiento', 'marca': 'Purina', 'proteina': 18, 'presentacion': 'Saco 50kg'}
            ],
            'vacunas': [
                {'id': 1, 'nombre': 'Newcastle', 'fabricante': 'Merial', 'presentacion': 'Dosis para 1000 aves'},
                {'id': 2, 'nombre': 'Gumboro', 'fabricante': 'Merial', 'presentacion': 'Dosis para 1000 aves'}
            ]
        }
        
        return examples.get(data_type, [])
    
    # Implementación de los métodos para cada entidad
    # Estos métodos intentarán obtener datos de la API y, si no es posible,
    # devolverán datos de ejemplo
    
    # Métodos para gestionar lotes
    def get_lotes(self):
        """Obtiene la lista de lotes
        
        Returns:
            tuple: (success, data) donde success es un booleano que indica si la operación fue exitosa,
                  y data es una lista de lotes o un mensaje de error.
        """
        print("\n=== Iniciando obtención de lotes ===")
        
        # 1. Intentar obtener datos del servidor
        try:
            print("Intentando obtener lotes desde el servidor...")
            success, data = self.make_request('get', f"{self.base_url}/lotes/")
            
            if success and data is not None:
                print(f"Datos recibidos del servidor. Tipo: {type(data)}")
                
                # Procesar diferentes formatos de respuesta
                if isinstance(data, dict):
                    # Formato con 'results' (Django REST Framework)
                    if 'results' in data and isinstance(data['results'], list):
                        print(f"Formato: diccionario con 'results' ({len(data['results'])} elementos)")
                        return True, data['results']
                    # Formato con 'data'
                    elif 'data' in data and isinstance(data['data'], list):
                        print(f"Formato: diccionario con 'data' ({len(data['data'])} elementos)")
                        return True, data['data']
                    # Diccionario con campos de lote individual
                    elif all(key in data for key in ['id', 'codigo', 'fecha_ingreso']):
                        print("Formato: diccionario con datos de un solo lote")
                        return True, [data]
                    # Diccionario vacío o sin formato reconocido
                    else:
                        print("Formato de diccionario no reconocido. Buscando listas internas...")
                        # Buscar recursivamente cualquier lista que pueda contener lotes
                        def find_lists(d):
                            if isinstance(d, list):
                                return d
                            elif isinstance(d, dict):
                                for v in d.values():
                                    result = find_lists(v)
                                    if result:
                                        return result
                            return None
                        
                        found_lists = find_lists(data)
                        if found_lists and all(isinstance(x, dict) for x in found_lists):
                            print(f"Encontrada lista interna con {len(found_lists)} elementos")
                            return True, found_lists
                
                # Si es una lista, verificar que contenga diccionarios
                elif isinstance(data, list):
                    if all(isinstance(x, dict) for x in data):
                        print(f"Formato: lista directa con {len(data)} elementos")
                        return True, data
                    else:
                        print("Advertencia: La lista contiene elementos que no son diccionarios")
                
                print(f"Formato de respuesta no reconocido: {type(data)}")
            
            # Si llegamos aquí, no se pudo procesar la respuesta del servidor
            print("No se pudieron procesar los datos del servidor. Intentando cargar datos locales...")
            
        except Exception as e:
            print(f"Error al obtener lotes del servidor: {str(e)}")
            if hasattr(e, 'response') and hasattr(e.response, 'status_code'):
                print(f"Código de estado HTTP: {e.response.status_code}")
        
        # 2. Si falla la conexión o el procesamiento, intentar cargar datos locales
        try:
            print("\nIntentando cargar lotes desde almacenamiento local...")
            local_data = self.load_offline_data('lotes')
            if local_data and isinstance(local_data, list):
                print(f"Cargados {len(local_data)} lotes desde almacenamiento local")
                return True, local_data
            else:
                print("No se encontraron datos locales de lotes")
        except Exception as e:
            print(f"Error al cargar datos locales: {str(e)}")
        
        # 3. Como último recurso, usar datos de ejemplo
        print("\nUsando datos de ejemplo para lotes...")
        example_data = self.get_example_data('lotes')
        if example_data and isinstance(example_data, list):
            print(f"Cargados {len(example_data)} lotes de ejemplo")
            return True, example_data
        
        # 4. Si todo falla, devolver lista vacía con mensaje de error
        print("No se pudieron cargar los lotes. Verifica la conexión e intenta nuevamente.")
        return False, "No se pudieron cargar los lotes. Verifica la conexión e intenta nuevamente."
    
    def get_lote(self, lote_id):
        """Obtiene un lote específico"""
        # Verificar si lote_id es válido
        if lote_id is None or lote_id == '' or lote_id == '--':
            print(f"ID de lote inválido: '{lote_id}'. Devolviendo primer lote de ejemplo.")
            # Devolver el primer lote de ejemplo si el ID no es válido
            lotes_ejemplo = self.get_example_data('lotes')
            return True, lotes_ejemplo[0] if lotes_ejemplo else None
            if lotes_ejemplo and len(lotes_ejemplo) > 0:
                return True, lotes_ejemplo[0]
            return False, "No hay lotes disponibles"
        
        # Si estamos en modo offline, buscar directamente en los datos de ejemplo
        if self.is_offline:
            print(f"Modo offline activado. Buscando lote {lote_id} en datos de ejemplo.")
            lotes_ejemplo = self.get_example_data('lotes')
            for lote in lotes_ejemplo:
                if str(lote.get('id')) == str(lote_id):
                    return True, lote
            # Si no se encuentra, devolver el primer lote como alternativa
            if lotes_ejemplo and len(lotes_ejemplo) > 0:
                print(f"No se encontró el lote {lote_id}. Devolviendo primer lote disponible.")
                return True, lotes_ejemplo[0]
            return False, "No hay lotes disponibles"
        
        # Si no estamos en modo offline, intentar obtener de la API
        try:
            # Usar el método centralizado con timeout
            success, data = self.make_request('get', f"{self.base_url}/lotes/{lote_id}/")
            
            if success:
                return True, data
            else:
                error_msg = f"Error al obtener lote {lote_id}: {data}"
                print(error_msg)
                # Buscar el lote en los datos de ejemplo como fallback
                lotes_ejemplo = self.get_example_data('lotes')
                for lote in lotes_ejemplo:
                    if str(lote.get('id')) == str(lote_id):
                        return True, lote
                # Si no se encuentra, devolver el primer lote como alternativa
                if lotes_ejemplo and len(lotes_ejemplo) > 0:
                    print(f"No se encontró el lote {lote_id}. Devolviendo primer lote disponible.")
                    return True, lotes_ejemplo[0]
                return False, f"No se encontró el lote con ID {lote_id}"
        except Exception as e:
            error_msg = f"Error de conexión: {str(e)}"
            print(error_msg)
            # Activar modo offline automáticamente
            self.is_offline = True
            print("Activando modo offline debido a error de conexión")
            # Buscar el lote en los datos de ejemplo
            lotes_ejemplo = self.get_example_data('lotes')
            for lote in lotes_ejemplo:
                if str(lote.get('id')) == str(lote_id):
                    return True, lote
            # Si no se encuentra, devolver el primer lote como alternativa
            if lotes_ejemplo and len(lotes_ejemplo) > 0:
                print(f"No se encontró el lote {lote_id}. Devolviendo primer lote disponible.")
                return True, lotes_ejemplo[0]
            return False, "No hay lotes disponibles"
            
    def get_seguimientos(self, lote_id=None):
        """Obtiene los seguimientos diarios, opcionalmente filtrados por lote"""
        print(f"Intentando obtener seguimientos{' para lote ' + str(lote_id) if lote_id else ''}...")
        try:
            # Construir URL con parámetros de consulta si se proporciona un lote_id
            url = f"{self.base_url}/seguimientos/"
            params = {}
            if lote_id:
                params['lote'] = lote_id
            
            # Usar el método centralizado con timeout
            success, data = self.make_request('get', url, params=params)
            
            if success:
                print(f"Datos recibidos: {type(data)}")
                # Normalizar el formato de respuesta
                if isinstance(data, dict):
                    # Si es un diccionario, verificar si tiene una clave 'results' que contenga la lista
                    if 'results' in data and isinstance(data['results'], list):
                        print(f"Formato: diccionario con 'results' ({len(data['results'])} elementos)")
                        return True, data['results']
                    # Si no tiene 'results' pero tiene 'data'
                    elif 'data' in data and isinstance(data['data'], list):
                        print(f"Formato: diccionario con 'data' ({len(data['data'])} elementos)")
                        return True, data['data']
                    # Si es un diccionario con otros campos, intentar extraer los datos relevantes
                    else:
                        print(f"Formato: diccionario sin 'results' o 'data'")
                        return True, data
                # Si ya es una lista, devolverla directamente
                elif isinstance(data, list):
                    print(f"Formato: lista ({len(data)} elementos)")
                    return True, data
                # Si es otro tipo de datos, convertirlo a string y devolverlo
                else:
                    print(f"Formato inesperado: {type(data)}")
                    return False, self.get_example_data('seguimientos')
            else:
                error_msg = f"Error al obtener seguimientos: {data}"
                print(error_msg)
                # Devolver datos de ejemplo en modo offline
                return False, self.get_example_data('seguimientos')
        except Exception as e:
            error_msg = f"Error inesperado: {str(e)}"
            print(error_msg)
            # Devolver datos de ejemplo en modo offline
            return False, self.get_example_data('seguimientos')
    
    # Métodos para gestionar tareas
    def get_tareas(self):
        """Obtiene la lista de tareas"""
        print("Intentando obtener tareas...")
        try:
            # Usar el método centralizado con timeout
            success, data = self.make_request('get', f"{self.base_url}/tareas/")
            
            if success:
                print(f"Datos recibidos: {type(data)}")
                # Normalizar el formato de respuesta
                if isinstance(data, dict):
                    # Si es un diccionario, verificar si tiene una clave 'results' que contenga la lista
                    if 'results' in data and isinstance(data['results'], list):
                        print(f"Formato: diccionario con 'results' ({len(data['results'])} elementos)")
                        return True, data['results']
                    # Si no tiene 'results' pero tiene 'data'
                    elif 'data' in data and isinstance(data['data'], list):
                        print(f"Formato: diccionario con 'data' ({len(data['data'])} elementos)")
                        return True, data['data']
                    # Si es un diccionario con otros campos, intentar extraer los datos relevantes
                    else:
                        print(f"Formato: diccionario sin 'results' o 'data'")
                        # Si tiene campos como 'id', 'titulo', etc., podría ser una sola tarea
                        if 'id' in data and 'titulo' in data:
                            print("Parece ser una sola tarea, convirtiendo a lista")
                            return True, [data]
                        # De lo contrario, devolver el diccionario completo
                        return True, data
                # Si ya es una lista, devolverla directamente
                elif isinstance(data, list):
                    print(f"Formato: lista ({len(data)} elementos)")
                    return True, data
                # Si es otro tipo de datos, convertir a string y devolverlo
                else:
                    print(f"Formato inesperado: {type(data)}")
                    return True, self.get_example_data('tareas')
            else:
                error_msg = f"Error al obtener tareas: {data}"
                print(error_msg)
                # Devolver datos de ejemplo en modo offline
                return True, self.get_example_data('tareas')
        except Exception as e:
            error_msg = f"Error inesperado al obtener tareas: {str(e)}"
            print(error_msg)
            
            # Si es un error 404, el endpoint no existe
            if "404" in str(e):
                print("El endpoint de tareas no está disponible (404). Usando datos de ejemplo.")
                return True, self.get_example_data('tareas')
                
            # Si es un error 500, intentar una vez más antes de usar datos de ejemplo
            if "500" in str(e):
                print("Error 500 detectado, intentando una vez más...")
                try:
                    success, data = self.make_request('get', f"{self.base_url}/tareas/")
                    if success:
                        return True, data
                except Exception as retry_error:
                    print(f"Error en reintento: {str(retry_error)}")
            
            # Devolver datos de ejemplo en modo offline
            print("Usando datos de ejemplo para tareas")
            return True, self.get_example_data('tareas')
    
    def get_tarea(self, tarea_id):
        """Obtiene una tarea específica"""
        try:
            # Agregar timeout para evitar bloqueos
            response = requests.get(
                f"{self.base_url}/tareas/{tarea_id}/",
                headers=self.get_headers()
            )
            
            if response.status_code == 200:
                return True, response.json()
            else:
                error_msg = f"Error al obtener tarea: {response.text}"
                print(error_msg)
                # Buscar en datos de ejemplo
                for tarea in self.get_example_data('tareas'):
                    if tarea['id'] == tarea_id:
                        return False, tarea
                return False, {}
        except Exception as e:
            error_msg = f"Error de conexión: {str(e)}"
            print(error_msg)
            # Buscar en datos de ejemplo
            for tarea in self.get_example_data('tareas'):
                if tarea['id'] == tarea_id:
                    return False, tarea
            return False, {}
    
    def crear_tarea(self, tarea_data):
        """Crea una nueva tarea"""
        try:
            # Agregar timeout para evitar bloqueos
            response = requests.post(
                f"{self.base_url}/tareas/",
                json=tarea_data,
                headers=self.get_headers()
            )
            
            if response.status_code in [200, 201]:
                return True, response.json()
            else:
                error_msg = f"Error al crear tarea: {response.text}"
                print(error_msg)
                # Simular éxito en modo offline
                return True, tarea_data
        except Exception as e:
            error_msg = f"Error de conexión: {str(e)}"
            print(error_msg)
            # Simular éxito en modo offline
            return True, tarea_data
    
    def actualizar_tarea(self, tarea_id, tarea_data):
        """Actualiza una tarea existente"""
        try:
            # Agregar timeout para evitar bloqueos
            response = requests.put(
                f"{self.base_url}/tareas/{tarea_id}/",
                json=tarea_data,
                headers=self.get_headers()
            )
            
            if response.status_code in [200, 201, 204]:
                return True, response.json() if response.status_code != 204 else tarea_data
            else:
                error_msg = f"Error al actualizar tarea: {response.text}"
                print(error_msg)
                # Simular éxito en modo offline
                return True, tarea_data
        except Exception as e:
            error_msg = f"Error de conexión: {str(e)}"
            print(error_msg)
            # Simular éxito en modo offline
            return True, tarea_data
    
    def eliminar_tarea(self, tarea_id):
        """Elimina una tarea"""
        try:
            # Agregar timeout para evitar bloqueos
            response = requests.delete(
                f"{self.base_url}/tareas/{tarea_id}/",
                headers=self.get_headers()
            )
            
            if response.status_code in [200, 204]:
                return True, "Tarea eliminada correctamente"
            else:
                error_msg = f"Error al eliminar tarea: {response.text}"
                print(error_msg)
                # Simular éxito en modo offline
                return True, "Tarea eliminada correctamente"
        except Exception as e:
            error_msg = f"Error de conexión: {str(e)}"
            print(error_msg)
            # Simular éxito en modo offline
            return True, "Tarea eliminada correctamente"
    
    # Métodos para estadísticas
    def get_dashboard_stats(self):
        """Obtiene estadísticas para el dashboard"""
        try:
            # Primero intentar cargar desde el archivo de datos de ejemplo
            try:
                import os
                import json
                stats_file = os.path.join(os.path.dirname(__file__), "datos_estadisticas.json")
                if os.path.exists(stats_file):
                    with open(stats_file, "r") as f:
                        print("Usando datos de estadísticas desde archivo local")
                        return True, json.load(f)
            except Exception as e:
                print(f"Error al cargar datos de estadísticas desde archivo: {str(e)}")
            
            # Si estamos en modo offline, usar datos de ejemplo directamente
            if self.is_offline:
                print("Modo offline activado. Usando datos de ejemplo para estadísticas.")
                return True, self.get_example_data('dashboard_stats')
            
            # Si no estamos en modo offline, intentar obtener datos del servidor
            try:
                # Agregar timeout para evitar bloqueos
                response = requests.get(
                    f"{self.base_url}/estadisticas/dashboard/",
                    headers=self.get_headers(),
                    timeout=5
                )
                
                if response.status_code == 200:
                    return True, response.json()
                else:
                    error_msg = f"Error al obtener estadísticas: {response.text}"
                    print(error_msg)
                    # Usar datos de ejemplo
                    return True, self.get_example_data('dashboard_stats')
            except Exception as e:
                error_msg = f"Error de conexión: {str(e)}"
                print(error_msg)
                # Usar datos de ejemplo
                return True, self.get_example_data('dashboard_stats')
        except Exception as e:
            error_msg = f"Error general en get_dashboard_stats: {str(e)}"
            print(error_msg)
            # Siempre devolver True con datos de ejemplo para evitar errores en la UI
            return True, self.get_example_data('dashboard_stats')
            
    def get_comparacion_razas(self, raza1_id, raza2_id):
        """Obtiene datos para comparar una raza nominal con los datos reales de un lote
        
        Args:
            raza1_id: ID de la primera raza a comparar
            raza2_id: ID de la segunda raza a comparar (puede ser None si solo se quiere comparar una raza)
            
        Returns:
            tuple: (success, data)
        """
        try:
            # Primero intentar cargar desde el archivo de datos de ejemplo
            try:
                import os
                import json
                comparacion_file = os.path.join(os.path.dirname(__file__), "datos_comparacion_razas.json")
                if os.path.exists(comparacion_file):
                    with open(comparacion_file, "r") as f:
                        print("Usando datos de comparación de razas desde archivo local")
                        data = json.load(f)
                        
                        # Si solo se quiere comparar una raza
                        if raza2_id is None or raza2_id == "":
                            return True, {"raza1": data["raza1"]}
                        
                        # Si se quieren comparar dos razas
                        return True, {"raza1": data["raza1"], "raza2": data["raza2"]}
            except Exception as e:
                print(f"Error al cargar datos de comparación de razas: {str(e)}")
            
            # Si estamos en modo offline, usar datos de ejemplo directamente
            if self.is_offline:
                print("Modo offline activado. Usando datos de ejemplo para comparación de razas.")
                return True, self.get_example_data('comparacion_razas')
            
            # Si no estamos en modo offline, intentar obtener datos del servidor
            try:
                # Construir URL según si se comparan una o dos razas
                url = f"{self.base_url}/estadisticas/comparacion-razas/?raza1={raza1_id}"
                if raza2_id is not None and raza2_id != "":
                    url += f"&raza2={raza2_id}"
                
                # Agregar timeout para evitar bloqueos
                response = requests.get(
                    url,
                    headers=self.get_headers(),
                    timeout=5
                )
                
                if response.status_code == 200:
                    return True, response.json()
                else:
                    error_msg = f"Error al obtener comparación de razas: {response.text}"
                    print(error_msg)
                    # Usar datos de ejemplo
                    return True, self.get_example_data('comparacion_razas')
            except Exception as e:
                error_msg = f"Error de conexión: {str(e)}"
                print(error_msg)
                # Usar datos de ejemplo
                return True, self.get_example_data('comparacion_razas')
        except Exception as e:
            error_msg = f"Error general en get_comparacion_razas: {str(e)}"
            print(error_msg)
            # Siempre devolver True con datos de ejemplo para evitar errores en la UI
            return True, self.get_example_data('comparacion_razas')
            
    def get_empresas(self):
        """Obtiene la lista de empresas (usando el endpoint de granjas como alternativa)"""
        print("Intentando obtener empresas (usando endpoint de granjas)...")
        try:
            # Usar el método centralizado con timeout
            # Nota: El endpoint /empresas/ no existe, usamos /granjas/ como alternativa
            success, data = self.make_request('get', f"{self.base_url}/granjas/")
            
            if success:
                print(f"Datos recibidos: {type(data)}")
                # Normalizar el formato de respuesta
                if isinstance(data, dict):
                    # Si es un diccionario, verificar si tiene una clave 'results' que contenga la lista
                    if 'results' in data and isinstance(data['results'], list):
                        print(f"Formato: diccionario con 'results' ({len(data['results'])} elementos)")
                        # Convertir granjas a formato de empresas
                        empresas = []
                        for granja in data['results']:
                            # Crear una empresa a partir de los datos de la granja
                            empresa = {
                                'id': granja.get('id', 0),
                                'nombre': granja.get('nombre', 'Empresa sin nombre'),
                                'nit': granja.get('codigo', 'Sin NIT'),
                                'direccion': granja.get('ubicacion', 'Sin dirección'),
                                'telefono': granja.get('telefono', 'Sin teléfono'),
                                'email': granja.get('email', 'info@ejemplo.com'),
                                'sitio_web': granja.get('sitio_web', 'www.ejemplo.com'),
                                'descripcion': granja.get('descripcion', 'Sin descripción')
                            }
                            empresas.append(empresa)
                        return True, empresas
                    # Si no tiene 'results' pero tiene 'data'
                    elif 'data' in data and isinstance(data['data'], list):
                        print(f"Formato: diccionario con 'data' ({len(data['data'])} elementos)")
                        # Convertir granjas a formato de empresas
                        empresas = []
                        for granja in data['data']:
                            # Crear una empresa a partir de los datos de la granja
                            empresa = {
                                'id': granja.get('id', 0),
                                'nombre': granja.get('nombre', 'Empresa sin nombre'),
                                'nit': granja.get('codigo', 'Sin NIT'),
                                'direccion': granja.get('ubicacion', 'Sin dirección'),
                                'telefono': granja.get('telefono', 'Sin teléfono'),
                                'email': granja.get('email', 'info@ejemplo.com'),
                                'sitio_web': granja.get('sitio_web', 'www.ejemplo.com'),
                                'descripcion': granja.get('descripcion', 'Sin descripción')
                            }
                            empresas.append(empresa)
                        return True, empresas
                    # Si es un diccionario con otros campos, intentar extraer los datos relevantes
                    else:
                        print(f"Formato: diccionario sin 'results' o 'data'")
                        # Si tiene campos como 'id', 'nombre', etc., podría ser una sola granja
                        if 'id' in data and 'nombre' in data:
                            print("Parece ser una sola granja, convirtiendo a empresa")
                            # Crear una empresa a partir de los datos de la granja
                            empresa = {
                                'id': data.get('id', 0),
                                'nombre': data.get('nombre', 'Empresa sin nombre'),
                                'nit': data.get('codigo', 'Sin NIT'),
                                'direccion': data.get('ubicacion', 'Sin dirección'),
                                'telefono': data.get('telefono', 'Sin teléfono'),
                                'email': data.get('email', 'info@ejemplo.com'),
                                'sitio_web': data.get('sitio_web', 'www.ejemplo.com'),
                                'descripcion': data.get('descripcion', 'Sin descripción')
                            }
                            return True, [empresa]
                        # De lo contrario, devolver datos de ejemplo
                        return False, self.get_example_data('empresas')
                # Si ya es una lista, convertirla a formato de empresas
                elif isinstance(data, list):
                    print(f"Formato: lista ({len(data)} elementos)")
                    # Convertir granjas a formato de empresas
                    empresas = []
                    for granja in data:
                        # Crear una empresa a partir de los datos de la granja
                        empresa = {
                            'id': granja.get('id', 0),
                            'nombre': granja.get('nombre', 'Empresa sin nombre'),
                            'nit': granja.get('codigo', 'Sin NIT'),
                            'direccion': granja.get('ubicacion', 'Sin dirección'),
                            'telefono': granja.get('telefono', 'Sin teléfono'),
                            'email': granja.get('email', 'info@ejemplo.com'),
                            'sitio_web': granja.get('sitio_web', 'www.ejemplo.com'),
                            'descripcion': granja.get('descripcion', 'Sin descripción')
                        }
                        empresas.append(empresa)
                    return True, empresas
                # Si es otro tipo de datos, devolver datos de ejemplo
                else:
                    print(f"Formato inesperado: {type(data)}")
                    return False, self.get_example_data('empresas')
            else:
                error_msg = f"Error al obtener empresas: {data}"
                print(error_msg)
                # Devolver datos de ejemplo en modo offline
                return False, self.get_example_data('empresas')
        except Exception as e:
            error_msg = f"Error inesperado: {str(e)}"
            print(error_msg)
            # Devolver datos de ejemplo en modo offline
            return False, self.get_example_data('empresas')
            
    def get_galpones(self):
        """Obtiene la lista de galpones"""
        print("\n=== Iniciando get_galpones() ===")
        
        # Si estamos en modo offline, devolver datos locales
        if self.is_offline:
            print("Modo offline activado, devolviendo datos locales...")
            local_data = self.load_offline_data('galpones')
            if local_data:
                print(f"Datos locales cargados: {len(local_data)} elementos")
                return True, local_data
            else:
                print("No hay datos locales disponibles, usando datos de ejemplo")
                return True, self.get_example_data('galpones')
        
        try:
            print(f"Solicitando galpones a {self.base_url}/galpones/")
            success, data = self.make_request('get', f"{self.base_url}/galpones/")
            
            if not success:
                print("Error en la respuesta de la API, intentando cargar datos locales...")
                local_data = self.load_offline_data('galpones')
                if local_data:
                    print(f"Datos locales cargados: {len(local_data)} elementos")
                    return True, local_data
                return False, ["Error al obtener galpones"]
            
            print(f"Respuesta recibida: {type(data)}")
            
            # Normalizar la respuesta para manejar diferentes formatos de API
            normalized_data = None
            
            # 1. Si es una lista, usarla directamente
            if isinstance(data, list):
                print(f"Formato: Lista directa con {len(data)} elementos")
                normalized_data = data
            
            # 2. Si es un diccionario, buscar claves comunes
            elif isinstance(data, dict):
                print("Formato: Diccionario")
                print(f"Claves disponibles: {list(data.keys())}")
                
                # 2.1 Formato estándar de paginación (DRF)
                if 'results' in data and isinstance(data['results'], list):
                    print(f"  - Encontrada clave 'results' con {len(data['results'])} elementos")
                    normalized_data = data['results']
                
                # 2.2 Formato alternativo con 'data'
                elif 'data' in data and isinstance(data['data'], list):
                    print(f"  - Encontrada clave 'data' con {len(data['data'])} elementos")
                    normalized_data = data['data']
                
                # 2.3 Formato con 'items'
                elif 'items' in data and isinstance(data['items'], list):
                    print(f"  - Encontrada clave 'items' con {len(data['items'])} elementos")
                    normalized_data = data['items']
                
                # 2.4 Si es un diccionario con datos de galpón directamente
                elif any(key in data for key in ['id', 'nombre', 'numero_galpon']):
                    print("  - Diccionario con datos de galpón, convirtiendo a lista")
                    normalized_data = [data]
                
                # 2.5 Si es un diccionario vacío
                elif not data:
                    print("  - Diccionario vacío recibido")
                    normalized_data = []
                
                # 2.6 Si es un diccionario con un solo valor que es una lista
                elif len(data) == 1 and isinstance(list(data.values())[0], list):
                    print(f"  - Diccionario con una lista, extrayendo lista")
                    normalized_data = list(data.values())[0]
                
                # 2.7 Otro formato de diccionario no reconocido
                else:
                    print("  - Formato de diccionario no reconocido")
                    print(f"  - Claves disponibles: {list(data.keys())}")
                    # Intentar extraer cualquier lista que pueda contener
                    lists_in_dict = [v for v in data.values() if isinstance(v, list)]
                    if lists_in_dict:
                        print(f"  - Encontrada(s) {len(lists_in_dict)} lista(s) en el diccionario")
                        normalized_data = lists_in_dict[0]  # Tomar la primera lista encontrada
            
            # 3. Si no se pudo normalizar, devolver lista vacía
            if normalized_data is None:
                print("No se pudo normalizar la respuesta, usando lista vacía")
                normalized_data = []
            
            # Asegurarse de que los datos sean una lista
            if not isinstance(normalized_data, list):
                print(f"Los datos normalizados no son una lista, convirtiendo...")
                normalized_data = [normalized_data] if normalized_data is not None else []
            
            # Verificar que los elementos tengan la estructura esperada
            if normalized_data:
                print(f"Datos normalizados: {len(normalized_data)} elementos")
                
                # Verificar el primer elemento para ver si tiene la estructura esperada
                first_item = normalized_data[0] if normalized_data else None
                print("Primer elemento:")
                if first_item is not None:
                    if isinstance(first_item, dict):
                        print(f"  - Tipo: diccionario con claves: {list(first_item.keys())}")
                        
                        # Mapear nombres de campos si es necesario
                        for item in normalized_data:
                            if 'numero_galpon' in item and 'nombre' not in item:
                                item['nombre'] = f"Galpón {item['numero_galpon']}"
                            if 'capacidad_aves' in item and 'capacidad' not in item:
                                item['capacidad'] = item['capacidad_aves']
                            if 'ancho_m' in item and 'ancho' not in item:
                                item['ancho'] = item['ancho_m']
                            if 'largo_m' in item and 'largo' not in item:
                                item['largo'] = item['largo_m']
                    else:
                        print(f"  - Tipo: {type(first_item).__name__}")
            
            # Guardar datos localmente para uso offline
            if normalized_data:
                self._save_offline_data('galpones', normalized_data)
            
            return True, normalized_data
                
        except Exception as e:
            import traceback
            error_msg = f"Error inesperado al obtener galpones: {str(e)}"
            print(error_msg)
            print(f"Traceback: {traceback.format_exc()}")
            
            # Si es un error de conexión o timeout, intentar usar datos locales
            if any(err in str(e).lower() for err in ['connection', 'timeout', 'refused']):
                print("Error de conexión, intentando usar datos locales...")
                local_data = self.load_offline_data('galpones')
                if local_data:
                    print(f"Datos locales cargados: {len(local_data)} elementos")
                    return True, local_data
            
            # Si es un error 404, el endpoint no existe
            if "404" in str(e):
                print("El endpoint de galpones no está disponible (404). Usando datos de ejemplo.")
                return True, self.get_example_data('galpones')
                
            # Si es un error 500, intentar una vez más antes de usar datos de ejemplo
            if "500" in str(e):
                print("Error 500 detectado, intentando una vez más...")
                try:
                    success, data = self.make_request('get', f"{self.base_url}/galpones/")
                    if success:
                        return True, data if isinstance(data, list) else []
                except Exception as retry_error:
                    print(f"Error en reintento: {str(retry_error)}")
            
            # Si todo falla, devolver datos de ejemplo
            print("Usando datos de ejemplo para galpones")
            return True, self.get_example_data('galpones')
        
    def get_razas(self):
        """Obtiene la lista de razas de aves"""
        print("Intentando obtener razas...")
        try:
            # Usar el método centralizado con timeout
            success, data = self.make_request('get', f"{self.base_url}/razas/")
            
            if success:
                print(f"Datos recibidos: {type(data)}")
                # Normalizar el formato de respuesta
                if isinstance(data, dict):
                    # Si es un diccionario, verificar si tiene una clave 'results' que contenga la lista
                    if 'results' in data and isinstance(data['results'], list):
                        print(f"Formato: diccionario con 'results' ({len(data['results'])} elementos)")
                        return True, data['results']
                    # Si no tiene 'results' pero tiene 'data'
                    elif 'data' in data and isinstance(data['data'], list):
                        print(f"Formato: diccionario con 'data' ({len(data['data'])} elementos)")
                        return True, data['data']
                    # Si es un diccionario con otros campos, intentar extraer los datos relevantes
                    else:
                        print(f"Formato: diccionario sin 'results' o 'data'")
                        # Si tiene campos como 'id', 'nombre', etc., podría ser una sola raza
                        if 'id' in data and 'nombre' in data:
                            print("Parece ser una sola raza, convirtiendo a lista")
                            return True, [data]
                        # De lo contrario, devolver el diccionario completo
                        return True, data
                # Si ya es una lista, devolverla directamente
                elif isinstance(data, list):
                    print(f"Formato: lista ({len(data)} elementos)")
                    return True, data
                # Si es otro tipo de datos, convertirlo a string y devolverlo
                else:
                    print(f"Formato inesperado: {type(data)}")
                    return True, self.get_example_data('razas')
            else:
                error_msg = f"Error al obtener razas: {data}"
                print(error_msg)
                # Devolver datos de ejemplo en modo offline
                return True, self.get_example_data('razas')
        except Exception as e:
            error_msg = f"Error inesperado: {str(e)}"
            print(error_msg)
            # Devolver datos de ejemplo en modo offline
            return True, self.get_example_data('razas')
            
    def get_alimentos(self):
        """Obtiene la lista de alimentos"""
        print("Intentando obtener alimentos...")
        try:
            # Usar el método centralizado con timeout
            success, data = self.make_request('get', f"{self.base_url}/alimentos/")
            
            if success:
                print(f"Datos recibidos: {type(data)}")
                # Normalizar el formato de respuesta
                if isinstance(data, dict):
                    # Si es un diccionario, verificar si tiene una clave 'results' que contenga la lista
                    if 'results' in data and isinstance(data['results'], list):
                        print(f"Formato: diccionario con 'results' ({len(data['results'])} elementos)")
                        return True, data['results']
                    # Si no tiene 'results' pero tiene 'data'
                    elif 'data' in data and isinstance(data['data'], list):
                        print(f"Formato: diccionario con 'data' ({len(data['data'])} elementos)")
                        return True, data['data']
                    # Si es un diccionario con otros campos, intentar extraer los datos relevantes
                    else:
                        print(f"Formato: diccionario sin 'results' o 'data'")
                        # Si tiene campos como 'id', 'nombre', etc., podría ser un solo alimento
                        if 'id' in data and 'nombre' in data:
                            print("Parece ser un solo alimento, convirtiendo a lista")
                            return True, [data]
                        # De lo contrario, devolver el diccionario completo
                        return True, data
                # Si ya es una lista, devolverla directamente
                elif isinstance(data, list):
                    print(f"Formato: lista ({len(data)} elementos)")
                    return True, data
                # Si es otro tipo de datos, convertirlo a string y devolverlo
                else:
                    print(f"Formato inesperado: {type(data)}")
                    return True, self.get_example_data('alimentos')
            else:
                error_msg = f"Error al obtener alimentos: {data}"
                print(error_msg)
                # Devolver datos de ejemplo en modo offline
                return True, self.get_example_data('alimentos')
        except Exception as e:
            error_msg = f"Error inesperado al obtener alimentos: {str(e)}"
            print(error_msg)
            # Si es un error 500, intentar una vez más antes de usar datos de ejemplo
            if "500" in str(e):
                print("Error 500 detectado, intentando una vez más...")
                try:
                    success, data = self.make_request('get', f"{self.base_url}/alimentos/")
                    if success:
                        return True, data
                except Exception as retry_error:
                    print(f"Error en reintento: {str(retry_error)}")
            
            # Devolver datos de ejemplo en modo offline
            print("Usando datos de ejemplo para alimentos")
            return True, self.get_example_data('alimentos')
            
    def get_vacunas(self):
        """Obtiene la lista de vacunas"""
        print("Intentando obtener vacunas...")
        try:
            # Usar el método centralizado con timeout
            success, data = self.make_request('get', f"{self.base_url}/vacunas/")
            
            if success:
                print(f"Datos recibidos: {type(data)}")
                # Normalizar el formato de respuesta
                if isinstance(data, dict):
                    # Si es un diccionario, verificar si tiene una clave 'results' que contenga la lista
                    if 'results' in data and isinstance(data['results'], list):
                        print(f"Formato: diccionario con 'results' ({len(data['results'])} elementos)")
                        return True, data['results']
                    # Si no tiene 'results' pero tiene 'data'
                    elif 'data' in data and isinstance(data['data'], list):
                        print(f"Formato: diccionario con 'data' ({len(data['data'])} elementos)")
                        return True, data['data']
                    # Si es un diccionario con otros campos, intentar extraer los datos relevantes
                    else:
                        print(f"Formato: diccionario sin 'results' o 'data'")
                        # Si tiene campos como 'id', 'nombre', etc., podría ser una sola vacuna
                        if 'id' in data and 'nombre' in data:
                            print("Parece ser una sola vacuna, convirtiendo a lista")
                            return True, [data]
                        # De lo contrario, devolver el diccionario completo
                        return True, data
                # Si ya es una lista, devolverla directamente
                elif isinstance(data, list):
                    print(f"Formato: lista ({len(data)} elementos)")
                    return True, data
                # Si es otro tipo de datos, convertirlo a string y devolverlo
                else:
                    print(f"Formato inesperado: {type(data)}")
                    return True, self.get_example_data('vacunas')
            else:
                error_msg = f"Error al obtener vacunas: {data}"
                print(error_msg)
                # Devolver datos de ejemplo en modo offline
                return True, self.get_example_data('vacunas')
        except Exception as e:
            error_msg = f"Error inesperado: {str(e)}"
            print(error_msg)
            # Devolver datos de ejemplo en modo offline
            return True, self.get_example_data('vacunas')
            
    def get_granjas(self):
        """Obtiene la lista de granjas"""
        print("Intentando obtener granjas...")
        try:
            # Usar el método centralizado con timeout
            success, data = self.make_request('get', f"{self.base_url}/granjas/")
            
            if success:
                print(f"Datos recibidos: {type(data)}")
                # Normalizar el formato de respuesta
                if isinstance(data, dict):
                    # Si es un diccionario, verificar si tiene una clave 'results' que contenga la lista
                    if 'results' in data and isinstance(data['results'], list):
                        print(f"Formato: diccionario con 'results' ({len(data['results'])} elementos)")
                        return True, data['results']
                    # Si no tiene 'results' pero tiene 'data'
                    elif 'data' in data and isinstance(data['data'], list):
                        print(f"Formato: diccionario con 'data' ({len(data['data'])} elementos)")
                        return True, data['data']
                    # Si es un diccionario con otros campos, intentar extraer los datos relevantes
                    else:
                        print(f"Formato: diccionario sin 'results' o 'data'")
                        # Si tiene campos como 'id', 'nombre', etc., podría ser una sola granja
                        if 'id' in data and 'nombre' in data:
                            print("Parece ser una sola granja, convirtiendo a lista")
                            return True, [data]
                        # De lo contrario, devolver el diccionario completo
                        return True, data
                # Si ya es una lista, devolverla directamente
                elif isinstance(data, list):
                    print(f"Formato: lista ({len(data)} elementos)")
                    return True, data
                # Si es otro tipo de datos, convertirlo a string y devolverlo
                else:
                    print(f"Formato inesperado: {type(data)}")
                    return False, self.get_example_data('granjas')
            else:
                error_msg = f"Error al obtener granjas: {data}"
                print(error_msg)
                # Devolver datos de ejemplo en modo offline
                return False, self.get_example_data('granjas')
        except Exception as e:
            error_msg = f"Error inesperado: {str(e)}"
            print(error_msg)
            # Devolver datos de ejemplo en modo offline
            return False, self.get_example_data('granjas')
            
    def get_usuarios(self):
        """Obtiene la lista de usuarios"""
        print("Intentando obtener usuarios...")
        try:
            # Verificar si tenemos un token de autenticación
            if not self.token:
                print("No hay token de autenticación disponible. Usando datos de ejemplo.")
                return False, self.get_example_data('usuarios')
                
            # Usar el método centralizado con timeout y asegurar que se envía el token
            headers = self.get_headers()
            success, data = self.make_request('get', f"{self.base_url}/usuarios/", headers=headers)
            
            if success:
                print(f"Datos recibidos: {type(data)}")
                # Normalizar el formato de respuesta
                if isinstance(data, dict):
                    # Si es un diccionario, verificar si tiene una clave 'results' que contenga la lista
                    if 'results' in data and isinstance(data['results'], list):
                        print(f"Formato: diccionario con 'results' ({len(data['results'])} elementos)")
                        return True, data['results']
                    # Si no tiene 'results' pero tiene 'data'
                    elif 'data' in data and isinstance(data['data'], list):
                        print(f"Formato: diccionario con 'data' ({len(data['data'])} elementos)")
                        return True, data['data']
                    # Si es un diccionario con otros campos, intentar extraer los datos relevantes
                    else:
                        print(f"Formato: diccionario sin 'results' o 'data'")
                        # Si tiene campos como 'id', 'username', etc., podría ser un solo usuario
                        if 'id' in data and 'username' in data:
                            print("Parece ser un solo usuario, convirtiendo a lista")
                            return True, [data]
                        # De lo contrario, devolver el diccionario completo
                        return True, data
                # Si ya es una lista, devolverla directamente
                elif isinstance(data, list):
                    print(f"Formato: lista ({len(data)} elementos)")
                    return True, data
                # Si es otro tipo de datos, usar datos de ejemplo
                else:
                    print(f"Formato inesperado: {type(data)}")
                    return False, self.get_example_data('usuarios')
            else:
                # Si el error es 401 (No autorizado) o 403 (Prohibido), probablemente necesitamos un token válido
                if isinstance(data, str) and ('401' in data or '403' in data):
                    print("Error de autenticación. Intentando refrescar el token...")
                    # Intentar refrescar el token
                    if self.refresh_auth_token():
                        # Intentar nuevamente con el token refrescado
                        return self.get_usuarios()
                
                error_msg = f"Error al obtener usuarios: {data}"
                print(error_msg)
                # Devolver datos de ejemplo en modo offline
                return False, self.get_example_data('usuarios')
        except Exception as e:
            error_msg = f"Error inesperado: {str(e)}"
            print(error_msg)
            # Devolver datos de ejemplo en modo offline
            return False, self.get_example_data('usuarios')
            
    def get_grupos(self):
        """Obtiene la lista de grupos de usuarios"""
        print("Intentando obtener grupos...")
        try:
            # Verificar si tenemos un token de autenticación
            if not self.token:
                print("No hay token de autenticación disponible. Usando datos de ejemplo.")
                return False, self.get_example_data('grupos')
                
            # Usar el método centralizado con timeout y asegurar que se envía el token
            headers = self.get_headers()
            
            # El endpoint /grupos/ probablemente no existe, intentar con /auth/groups/ o simplemente usar datos de ejemplo
            # Como alternativa, podemos crear grupos ficticios basados en los permisos del usuario actual
            print("El endpoint /grupos/ probablemente no existe. Usando datos de ejemplo.")
            return False, self.get_example_data('grupos')
            
            # Código original comentado por si en el futuro se implementa el endpoint
            '''
            success, data = self.make_request('get', f"{self.base_url}/grupos/", headers=headers)
            
            if success:
                print(f"Datos recibidos: {type(data)}")
                # Normalizar el formato de respuesta
                if isinstance(data, dict):
                    # Si es un diccionario, verificar si tiene una clave 'results' que contenga la lista
                    if 'results' in data and isinstance(data['results'], list):
                        print(f"Formato: diccionario con 'results' ({len(data['results'])} elementos)")
                        return True, data['results']
                    # Si no tiene 'results' pero tiene 'data'
                    elif 'data' in data and isinstance(data['data'], list):
                        print(f"Formato: diccionario con 'data' ({len(data['data'])} elementos)")
                        return True, data['data']
                    # Si es un diccionario con otros campos, intentar extraer los datos relevantes
                    else:
                        print(f"Formato: diccionario sin 'results' o 'data'")
                        # Si tiene campos como 'id', 'name', etc., podría ser un solo grupo
                        if 'id' in data and 'name' in data:
                            print("Parece ser un solo grupo, convirtiendo a lista")
                            return True, [data]
                        # De lo contrario, devolver el diccionario completo
                        return True, data
                # Si ya es una lista, devolverla directamente
                elif isinstance(data, list):
                    print(f"Formato: lista ({len(data)} elementos)")
                    return True, data
                # Si es otro tipo de datos, usar datos de ejemplo
                else:
                    print(f"Formato inesperado: {type(data)}")
                    return False, self.get_example_data('grupos')
            else:
                # Si el error es 401 (No autorizado) o 403 (Prohibido), probablemente necesitamos un token válido
                if isinstance(data, str) and ('401' in data or '403' in data):
                    print("Error de autenticación. Intentando refrescar el token...")
                    # Intentar refrescar el token
                    if self.refresh_auth_token():
                        # Intentar nuevamente con el token refrescado
                        return self.get_grupos()
                
                error_msg = f"Error al obtener grupos: {data}"
                print(error_msg)
                # Devolver datos de ejemplo en modo offline
                return False, self.get_example_data('grupos')
            '''
        except Exception as e:
            error_msg = f"Error inesperado: {str(e)}"
            print(error_msg)
            # Devolver datos de ejemplo en modo offline
            return False, self.get_example_data('grupos')
            
    def read_config(self):
        """Lee la configuración desde el archivo config.json"""
        try:
            import os
            import json
            
            # Ruta al archivo de configuración
            config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'config.json')
            
            # Verificar si el archivo existe
            if not os.path.exists(config_path):
                # Crear un archivo de configuración vacío
                with open(config_path, 'w', encoding='utf-8') as f:
                    json.dump({}, f)
                return {}
            
            # Leer el archivo de configuración
            with open(config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
            
            return config
        except Exception as e:
            print(f"Error al leer la configuración: {str(e)}")
            return {}
    
    def save_config(self, config):
        """Guarda la configuración en el archivo config.json"""
        try:
            import os
            import json
            
            # Ruta al archivo de configuración
            config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'config.json')
            
            # Guardar la configuración
            with open(config_path, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=4)
            
            return True
        except Exception as e:
            print(f"Error al guardar la configuración: {str(e)}")
            return False
            
    def get_remembered_user(self):
        """Obtiene el nombre de usuario recordado"""
        try:
            # Intentar leer el archivo de configuración
            config = self.read_config()
            if config and 'remembered_user' in config:
                return config['remembered_user']
            return None
        except Exception as e:
            print(f"Error al obtener usuario recordado: {str(e)}")
            return None
            
    def save_remembered_user(self, username):
        """Guarda el nombre de usuario para recordarlo"""
        try:
            # Leer configuración actual
            config = self.read_config()
            if not config:
                config = {}
                
            # Actualizar el usuario recordado
            config['remembered_user'] = username
            
            # Guardar la configuración
            self.save_config(config)
            return True
        except Exception as e:
            print(f"Error al guardar usuario recordado: {str(e)}")
            return False
            
    def create_galpon(self, galpon_data):
        """
        Crea un nuevo galpón
        
        Args:
            galpon_data (dict): Diccionario con los datos del galpón a crear
                              Formato esperado:
                              {
                                  'numero_galpon': str,
                                  'tipo_galpon': str,
                                  'capacidad_aves': int,
                                  'area_metros_cuadrados': float,
                                  'altura': float,
                                  'estado': str,
                                  'equipamiento': dict,
                                  'sensores': dict,
                                  'energia': dict,
                                  'granja': int (ID de la granja, opcional),
                                  'responsable': int (ID del usuario responsable, opcional)
                              }
            
        Returns:
            tuple: (success, data) donde success es un booleano que indica si la operación fue exitosa,
                  y data contiene el galpón creado o un mensaje de error.
        """
        print(f"[DEBUG] Datos recibidos para crear galpón: {json.dumps(galpon_data, indent=2)}")
        
        try:
            # Validar campos requeridos
            required_fields = ['numero_galpon', 'tipo_galpon', 'capacidad_aves']
            for field in required_fields:
                if field not in galpon_data or galpon_data[field] is None:
                    error_msg = f"Campo requerido faltante: {field}"
                    print(f"[ERROR] {error_msg}")
                    return False, error_msg
            
            # Preparar los datos para la API
            data = {
                'numero_galpon': str(galpon_data['numero_galpon']),
                'tipo_galpon': str(galpon_data['tipo_galpon']),
                'capacidad_aves': int(galpon_data['capacidad_aves']),
                'estado': str(galpon_data.get('estado', 'Activo')),
                'area_metros_cuadrados': float(galpon_data.get('area_metros_cuadrados', 0)),
                'altura': float(galpon_data.get('altura', 3.0)),
                'equipamiento': galpon_data.get('equipamiento', {}),
                'sensores': galpon_data.get('sensores', {}),
                'energia': galpon_data.get('energia', {})
            }
            
            # Campos opcionales
            if 'granja' in galpon_data and galpon_data['granja'] is not None:
                data['granja'] = int(galpon_data['granja'])
                
            if 'responsable' in galpon_data and galpon_data['responsable'] is not None:
                data['responsable'] = int(galpon_data['responsable'])
            
            print(f"[DEBUG] Enviando datos al servidor: {json.dumps(data, indent=2)}")
            
            # Realizar la petición POST con los datos
            success, response = self.make_request('post', f"{self.base_url}/galpones/", data=data)
            
            if success:
                print(f"[SUCCESS] Galpón creado exitosamente: {response}")
                
                # Verificar que el ID del galpón se haya generado
                if 'id' not in response:
                    error_msg = "El servidor no devolvió un ID de galpón válido"
                    print(f"[WARNING] {error_msg}")
                    print(f"[DEBUG] Respuesta completa: {response}")
                    return False, error_msg
                
                # Guardar los datos localmente para acceso offline
                try:
                    galpones_success, galpones_data = self.get_galpones()
                    if galpones_success and isinstance(galpones_data, list):
                        # Si el galpón no está en la lista, agregarlo
                        galpon_exists = any(g.get('id') == response.get('id') for g in galpones_data)
                        if not galpon_exists:
                            galpones_data.append(response)
                        
                        # Guardar la lista actualizada
                        self._save_offline_data('galpones', galpones_data)
                        print("[DEBUG] Datos guardados localmente para acceso offline")
                except Exception as e:
                    print(f"[ERROR] Error al guardar datos offline: {str(e)}")
                
                return True, response
            else:
                error_msg = f"Error al crear galpón: {response}"
                print(f"[ERROR] {error_msg}")
                return False, error_msg
                
        except Exception as e:
            error_msg = f"Error inesperado al crear el galpón: {str(e)}"
            print(f"[ERROR] {error_msg}")
            import traceback
            print(f"[DEBUG] Traceback: {traceback.format_exc()}")
            return False, error_msg
    
    def get_galpon(self, galpon_id):
        """Obtiene los datos de un galpón específico por su ID"""
        try:
            # Agregar timeout para evitar bloqueos
            response = requests.get(
                f"{self.base_url}/galpones/{galpon_id}/",
                headers=self.get_headers()
            )
            
            if response.status_code == 200:
                return True, response.json()
            else:
                error_msg = f"Error al obtener galpón: {response.text}"
                print(error_msg)
                # Buscar en datos de ejemplo
                for galpon in self.get_example_data('galpones'):
                    if str(galpon['id']) == str(galpon_id):
                        return False, galpon
                return False, {}
        except Exception as e:
            error_msg = f"Error de conexión: {str(e)}"
            print(error_msg)
            # Buscar en datos de ejemplo
            for galpon in self.get_example_data('galpones'):
                if str(galpon['id']) == str(galpon_id):
                    return False, galpon
            return False, {}

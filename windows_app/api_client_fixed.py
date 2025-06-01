#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import json
import os
from datetime import datetime

class ApiClient:
    """Cliente para interactuar con la API de App Granja"""
    
    def __init__(self):
        # Cargar configuración
        self.config = self.load_config()
        self.base_url = self.config.get('api_url', 'http://127.0.0.1:8000/api')
        self.token = self.config.get('token', '')
        self.refresh_token = self.config.get('refresh_token', '')
        self.username = self.config.get('username', '')
        self.password = self.config.get('password', '')
        
        # Información del usuario actual
        self.current_user_info = self.config.get('user_info', None)
        self.is_offline = False
        
        # Verificar si necesitamos refrescar el token
        if self.token and self.refresh_token:
            self.refresh_auth_token()
    
    def load_config(self):
        """Carga la configuración desde el archivo config.json"""
        config_path = os.path.join(os.path.dirname(__file__), 'config.json')
        try:
            if os.path.exists(config_path):
                with open(config_path, 'r') as f:
                    return json.load(f)
            else:
                # Configuración por defecto
                default_config = {
                    'api_url': 'http://127.0.0.1:8000/api',
                    'token': '',
                    'username': '',
                    'password': ''
                }
                # Guardar configuración por defecto
                with open(config_path, 'w') as f:
                    json.dump(default_config, f, indent=4)
                return default_config
        except Exception as e:
            print(f"Error al cargar configuración: {str(e)}")
            return {
                'api_url': 'http://127.0.0.1:8000/api',
                'token': '',
                'username': '',
                'password': ''
            }
    
    def save_config(self, config):
        """Guarda la configuración en el archivo config.json"""
        config_path = os.path.join(os.path.dirname(__file__), 'config.json')
        try:
            with open(config_path, 'w') as f:
                json.dump(config, f, indent=4)
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
        headers = {
            'Content-Type': 'application/json'
        }
        if self.token:
            # JWT usa Bearer en lugar de Token
            headers['Authorization'] = f'Bearer {self.token}'
        return headers
    
    def login(self, username, password):
        """Inicia sesión en la API y obtiene un token JWT"""
        try:
            # Usar el endpoint JWT correcto
            response = requests.post(
                f"{self.base_url}/token/",
                json={'username': username, 'password': password}
            )
            
            if response.status_code == 200:
                data = response.json()
                # JWT devuelve access y refresh tokens
                self.token = data.get('access', '')
                self.refresh_token = data.get('refresh', '')
                self.username = username
                self.password = password
                self.is_offline = False
                
                # Obtener información del usuario
                success, user_info = self.get_user_info(username)
                if success:
                    self.current_user_info = user_info
                    # Incluir información adicional
                    self.current_user_info['username'] = username
                    self.current_user_info['is_offline'] = False
                else:
                    # Si no se puede obtener la información, crear un objeto básico
                    self.current_user_info = {
                        'username': username,
                        'is_offline': False,
                        'empresa': 'No disponible',
                        'granja': 'No disponible'
                    }
                
                # Actualizar configuración
                self.config['token'] = self.token
                self.config['refresh_token'] = self.refresh_token
                self.config['username'] = username
                self.config['password'] = password
                self.config['user_info'] = self.current_user_info
                self.save_config(self.config)
                
                return True, self.current_user_info
            else:
                return False, f"Error de inicio de sesión: {response.text}"
        except Exception as e:
            return False, f"Error de conexión: {str(e)}"
    
    def logout(self):
        """Cierra la sesión en la API"""
        try:
            # Si estamos usando JWT, no hay endpoint de logout en el servidor
            # Solo eliminamos el token localmente
            self.token = ''
            self.refresh_token = ''
            self.current_user_info = None
            self.is_offline = False
            self.username = ''
            
            # Actualizar configuración
            self.config['token'] = ''
            self.config['refresh_token'] = ''
            self.config['user_info'] = None
            self.config['username'] = ''
            self.save_config(self.config)
            
            # Eliminar el archivo de usuario recordado si existe
            try:
                if os.path.exists('remembered_user.txt'):
                    os.remove('remembered_user.txt')
            except Exception as e:
                print(f"Error al eliminar archivo de usuario recordado: {str(e)}")
            
            print("Cierre de sesión exitoso")
            return True, "Cierre de sesión exitoso"
        except Exception as e:
            error_msg = f"Error al cerrar sesión: {str(e)}"
            print(error_msg)
            
            # Incluso si hay un error, limpiar tokens localmente
            self.token = ''
            self.refresh_token = ''
            self.current_user_info = None
            self.is_offline = False
            self.username = ''
            
            # Actualizar configuración
            self.config['token'] = ''
            self.config['refresh_token'] = ''
            self.config['user_info'] = None
            self.config['username'] = ''
            self.save_config(self.config)
            
            return False, error_msg
    
    def refresh_auth_token(self):
        """Refresca el token JWT usando el refresh token"""
        try:
            if not self.refresh_token:
                return False, "No hay refresh token disponible"
                
            response = requests.post(
                f"{self.base_url}/token/refresh/",
                json={'refresh': self.refresh_token}
            )
            
            if response.status_code == 200:
                data = response.json()
                self.token = data.get('access', '')
                
                # Actualizar configuración
                self.config['token'] = self.token
                self.save_config(self.config)
                
                return True, "Token refrescado exitosamente"
            else:
                # Si no se puede refrescar, limpiar tokens
                self.token = ''
                self.refresh_token = ''
                self.config['token'] = ''
                self.config['refresh_token'] = ''
                self.save_config(self.config)
                
                return False, f"Error al refrescar token: {response.text}"
        except Exception as e:
            return False, f"Error al refrescar token: {str(e)}"
    
    def test_connection(self):
        """Prueba la conexión con la API"""
        try:
            print(f"Intentando conectar a: {self.base_url}/")
            # Intentar obtener la raíz de la API
            response = requests.get(
                f"{self.base_url}/",
                headers=self.get_headers(),
                timeout=10  # Aumentado a 10 segundos
            )
            
            print(f"Respuesta del servidor: {response.status_code}")
            
            # Verificar si la respuesta es exitosa (código 200)
            if response.status_code == 200:
                print("Conexión exitosa con la API")
                return True
            else:
                # Si la respuesta no es exitosa, intentar con otro endpoint común
                try:
                    print(f"Intentando endpoint alternativo: {self.base_url}/token/")
                    # Intentar con el endpoint de token
                    response = requests.post(
                        f"{self.base_url}/token/",
                        json={'username': 'admin', 'password': 'admin123'},
                        headers={'Content-Type': 'application/json'},
                        timeout=10  # Aumentado a 10 segundos
                    )
                    
                    print(f"Respuesta del servidor (token): {response.status_code}")
                    
                    if response.status_code in [200, 400, 401]:  # Estos códigos indican que el endpoint existe
                        print("Conexión exitosa con la API (endpoint de token)")
                        return True
                    else:
                        error_msg = f"Error al conectar con la API: {response.status_code}"
                        print(error_msg)
                        print("Funcionando en modo offline con datos de ejemplo")
                        return False
                except Exception as e:
                    error_msg = f"Error al conectar con la API: {str(e)}"
                    print(error_msg)
                    print("Funcionando en modo offline con datos de ejemplo")
                    return False
        except Exception as e:
            error_msg = f"Error de conexión: {str(e)}"
            print(error_msg)
            print(f"URL intentada: {self.base_url}/")
            print("Funcionando en modo offline con datos de ejemplo")
            return False
    
    def get_user_info(self, username):
        """Obtiene la información de un usuario"""
        try:
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
    def get_example_data(self, data_type):
        """Obtiene datos de ejemplo para cuando la API no está disponible"""
        examples = {
            'empresas': [
                {
                    'id': 1,
                    'nombre': 'Avicola El Dorado',
                    'nit': '900.123.456-7',
                    'direccion': 'Calle 123 #45-67, Bogotá',
                    'telefono': '(601) 123-4567',
                    'email': 'contacto@eldorado.com',
                    'sitio_web': 'www.eldorado.com',
                    'descripcion': 'Empresa líder en producción avícola'
                },
                {
                    'id': 2,
                    'nombre': 'Granjas del Valle',
                    'nit': '800.987.654-3',
                    'direccion': 'Km 5 Vía Cali-Palmira',
                    'telefono': '(602) 987-6543',
                    'email': 'info@granjasdelvalle.com',
                    'sitio_web': 'www.granjasdelvalle.com',
                    'descripcion': 'Producción y distribución de huevos y pollos'
                }
            ],
            'granjas': [
                {
                    'id': 1,
                    'nombre': 'Granja El Porvenir',
                    'ubicacion': 'Vereda La Esperanza',
                    'capacidad': 50000,
                    'estado': 'Activa'
                },
                {
                    'id': 2,
                    'nombre': 'Granja San José',
                    'ubicacion': 'Km 3 Vía al Mar',
                    'capacidad': 30000,
                    'estado': 'Activa'
                }
            ],
            'galpones': [
                {
                    'id': 1,
                    'nombre': 'Galpón 1',
                    'tipo': 'Producción',
                    'capacidad': 5000,
                    'granja': 1
                },
                {
                    'id': 2,
                    'nombre': 'Galpón 2',
                    'tipo': 'Cría',
                    'capacidad': 3000,
                    'granja': 1
                }
            ],
            'lotes': [
                {
                    'id': 1,
                    'codigo': 'L-2025-001',
                    'fecha_ingreso': '2025-01-15',
                    'cantidad_inicial': 4500,
                    'raza': 'Hy-Line Brown',
                    'galpon': 1
                },
                {
                    'id': 2,
                    'codigo': 'L-2025-002',
                    'fecha_ingreso': '2025-02-10',
                    'cantidad_inicial': 2800,
                    'raza': 'Lohmann LSL',
                    'galpon': 2
                }
            ],
            'razas': [
                {
                    'id': 1,
                    'nombre': 'Hy-Line Brown',
                    'tipo': 'Ponedora',
                    'descripcion': 'Excelente producción de huevos marrones'
                },
                {
                    'id': 2,
                    'nombre': 'Lohmann LSL',
                    'tipo': 'Ponedora',
                    'descripcion': 'Alta producción de huevos blancos'
                }
            ],
            'alimentos': [
                {
                    'id': 1,
                    'nombre': 'Concentrado Iniciación',
                    'tipo': 'Iniciación',
                    'proteina': 21.5,
                    'precio_kg': 1800
                },
                {
                    'id': 2,
                    'nombre': 'Concentrado Postura',
                    'tipo': 'Postura',
                    'proteina': 18.0,
                    'precio_kg': 1650
                }
            ],
            'vacunas': [
                {
                    'id': 1,
                    'nombre': 'Newcastle',
                    'tipo': 'Viral',
                    'via': 'Ocular',
                    'edad_aplicacion': 7
                },
                {
                    'id': 2,
                    'nombre': 'Gumboro',
                    'tipo': 'Viral',
                    'via': 'Agua',
                    'edad_aplicacion': 14
                }
            ],
            'seguimientos': [
                {
                    'id': 1,
                    'fecha': '2025-03-01',
                    'cantidad_actual': 4480,
                    'mortalidad': 20,
                    'produccion_huevos': 4100,
                    'peso_promedio': 1.8,
                    'lote': 1
                },
                {
                    'id': 2,
                    'fecha': '2025-03-02',
                    'cantidad_actual': 4475,
                    'mortalidad': 5,
                    'produccion_huevos': 4150,
                    'peso_promedio': 1.82,
                    'lote': 1
                }
            ],
            'dashboard_stats': {
                'lotes_activos': 2,
                'aves_totales': 7275,
                'produccion_semanal': 28500,
                'mortalidad_semanal': 42,
                'graficos': {
                    'produccion': [4100, 4150, 4200, 4180, 4220, 4250, 4400],
                    'mortalidad': [20, 5, 8, 4, 3, 2, 0],
                    'ventas': [3800, 3900, 4000, 4100, 4150, 4200, 4300]
                }
            },
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
                    'lote': 1
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
                    'galpon': 2
                }
            ]
        }
        
        return examples.get(data_type, [])
    
    # Implementación de los métodos para cada entidad
    # Estos métodos intentarán obtener datos de la API y, si no es posible,
    # devolverán datos de ejemplo
    
    # Métodos para gestionar lotes
    def get_lotes(self):
        """Obtiene la lista de lotes"""
        try:
            response = requests.get(
                f"{self.base_url}/lotes/",
                headers=self.get_headers()
            )
            
            if response.status_code == 200:
                return True, response.json()
            else:
                error_msg = f"Error al obtener lotes: {response.text}"
                print(error_msg)
                # Usar datos de ejemplo
                return False, self.get_example_data('lotes')
        except Exception as e:
            error_msg = f"Error de conexión: {str(e)}"
            print(error_msg)
            # Usar datos de ejemplo
            return False, self.get_example_data('lotes')
    
    def get_lote(self, lote_id):
        """Obtiene un lote específico"""
        try:
            response = requests.get(
                f"{self.base_url}/lotes/{lote_id}/",
                headers=self.get_headers()
            )
            
            if response.status_code == 200:
                return True, response.json()
            else:
                error_msg = f"Error al obtener lote: {response.text}"
                print(error_msg)
                # Buscar en datos de ejemplo
                for lote in self.get_example_data('lotes'):
                    if lote['id'] == lote_id:
                        return False, lote
                return False, {}
        except Exception as e:
            error_msg = f"Error de conexión: {str(e)}"
            print(error_msg)
            # Buscar en datos de ejemplo
            for lote in self.get_example_data('lotes'):
                if lote['id'] == lote_id:
                    return False, lote
            return False, {}
    
    # Métodos para gestionar tareas
    def get_tareas(self):
        """Obtiene la lista de tareas"""
        try:
            response = requests.get(
                f"{self.base_url}/tareas/",
                headers=self.get_headers()
            )
            
            if response.status_code == 200:
                return True, response.json()
            else:
                error_msg = f"Error al obtener tareas: {response.text}"
                print(error_msg)
                # Usar datos de ejemplo
                return False, self.get_example_data('tareas')
        except Exception as e:
            error_msg = f"Error de conexión: {str(e)}"
            print(error_msg)
            # Usar datos de ejemplo
            return False, self.get_example_data('tareas')
    
    def get_tarea(self, tarea_id):
        """Obtiene una tarea específica"""
        try:
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
            response = requests.get(
                f"{self.base_url}/estadisticas/dashboard/",
                headers=self.get_headers()
            )
            
            if response.status_code == 200:
                return True, response.json()
            else:
                error_msg = f"Error al obtener estadísticas: {response.text}"
                print(error_msg)
                # Usar datos de ejemplo
                return False, self.get_example_data('dashboard_stats')
        except Exception as e:
            error_msg = f"Error de conexión: {str(e)}"
            print(error_msg)
            # Usar datos de ejemplo
            return False, self.get_example_data('dashboard_stats')

#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import json
import os
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QVBoxLayout, QWidget, QMessageBox

class TestConnectionWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Test de Conexión a Django")
        self.setGeometry(100, 100, 400, 300)
        
        # Widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Layout
        layout = QVBoxLayout(central_widget)
        
        # Etiqueta de estado
        self.status_label = QLabel("Estado: No probado")
        layout.addWidget(self.status_label)
        
        # Botón para probar conexión
        test_button = QPushButton("Probar Conexión")
        test_button.clicked.connect(self.test_connection)
        layout.addWidget(test_button)
        
        # Botón para probar API
        api_button = QPushButton("Probar API")
        api_button.clicked.connect(self.test_api)
        layout.addWidget(api_button)
        
        # Botón para probar autenticación
        auth_button = QPushButton("Probar Autenticación")
        auth_button.clicked.connect(self.test_auth)
        layout.addWidget(auth_button)
        
        # Cargar configuración
        self.load_config()
    
    def load_config(self):
        """Carga la configuración desde el archivo config.json"""
        config_path = os.path.join(os.path.dirname(__file__), 'config.json')
        try:
            if os.path.exists(config_path):
                with open(config_path, 'r') as f:
                    self.config = json.load(f)
            else:
                # Configuración por defecto
                self.config = {
                    'api_url': 'http://127.0.0.1:8000/api',
                    'token': '',
                    'username': 'admin',
                    'password': 'admin123'
                }
                # Guardar configuración por defecto
                with open(config_path, 'w') as f:
                    json.dump(self.config, f, indent=4)
        except Exception as e:
            print(f"Error al cargar configuración: {str(e)}")
            self.config = {
                'api_url': 'http://127.0.0.1:8000/api',
                'token': '',
                'username': 'admin',
                'password': 'admin123'
            }
    
    def test_connection(self):
        """Prueba la conexión básica con el servidor Django"""
        try:
            # Obtener la URL base sin /api
            base_url = self.config['api_url'].split('/api')[0]
            print(f"Intentando conectar a: {base_url}")
            
            # Intentar obtener la página principal de Django
            response = requests.get(
                base_url,
                timeout=10
            )
            
            print(f"Respuesta del servidor: {response.status_code}")
            
            if response.status_code == 200:
                self.status_label.setText(f"Estado: Conexión exitosa - {response.status_code}")
                QMessageBox.information(self, "Conexión Exitosa", f"Se pudo conectar al servidor Django en {base_url}")
            else:
                self.status_label.setText(f"Estado: Error de conexión - {response.status_code}")
                QMessageBox.warning(self, "Error de Conexión", f"No se pudo conectar al servidor Django. Código: {response.status_code}")
        except Exception as e:
            self.status_label.setText(f"Estado: Error - {str(e)}")
            QMessageBox.critical(self, "Error", f"Error al conectar con el servidor: {str(e)}")
    
    def test_api(self):
        """Prueba la conexión con la API de Django"""
        try:
            api_url = self.config['api_url']
            print(f"Intentando conectar a la API: {api_url}")
            
            # Intentar obtener la raíz de la API
            response = requests.get(
                api_url,
                timeout=10
            )
            
            print(f"Respuesta de la API: {response.status_code}")
            
            if response.status_code == 200:
                try:
                    data = response.json()
                    endpoints = json.dumps(data, indent=2)
                    self.status_label.setText(f"Estado: API accesible - {response.status_code}")
                    QMessageBox.information(self, "API Accesible", f"Se pudo acceder a la API en {api_url}\n\nEndpoints disponibles:\n{endpoints}")
                except Exception as e:
                    self.status_label.setText(f"Estado: Error al procesar respuesta - {str(e)}")
                    QMessageBox.warning(self, "Error de Procesamiento", f"Se pudo acceder a la API pero hubo un error al procesar la respuesta: {str(e)}")
            else:
                self.status_label.setText(f"Estado: Error de API - {response.status_code}")
                QMessageBox.warning(self, "Error de API", f"No se pudo acceder a la API. Código: {response.status_code}")
        except Exception as e:
            self.status_label.setText(f"Estado: Error - {str(e)}")
            QMessageBox.critical(self, "Error", f"Error al conectar con la API: {str(e)}")
    
    def test_auth(self):
        """Prueba la autenticación con la API de Django"""
        try:
            api_url = self.config['api_url']
            username = self.config['username']
            password = self.config['password']
            
            print(f"Intentando autenticar en: {api_url}/token/")
            
            # Intentar obtener un token JWT
            response = requests.post(
                f"{api_url}/token/",
                json={'username': username, 'password': password},
                headers={'Content-Type': 'application/json'},
                timeout=10
            )
            
            print(f"Respuesta de autenticación: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                token = data.get('access', '')
                refresh = data.get('refresh', '')
                
                # Guardar el token en la configuración
                self.config['token'] = token
                self.config['refresh_token'] = refresh
                with open(os.path.join(os.path.dirname(__file__), 'config.json'), 'w') as f:
                    json.dump(self.config, f, indent=4)
                
                self.status_label.setText(f"Estado: Autenticación exitosa")
                QMessageBox.information(self, "Autenticación Exitosa", f"Se pudo autenticar con el usuario {username}")
                
                # Probar el token obtenido
                self.test_token(token)
            else:
                self.status_label.setText(f"Estado: Error de autenticación - {response.status_code}")
                QMessageBox.warning(self, "Error de Autenticación", f"No se pudo autenticar. Código: {response.status_code}\nRespuesta: {response.text}")
        except Exception as e:
            self.status_label.setText(f"Estado: Error - {str(e)}")
            QMessageBox.critical(self, "Error", f"Error al intentar autenticar: {str(e)}")
    
    def test_token(self, token):
        """Prueba el token obtenido haciendo una petición a un endpoint protegido"""
        try:
            api_url = self.config['api_url']
            
            # Intentar obtener la lista de usuarios (endpoint protegido)
            response = requests.get(
                f"{api_url}/usuarios/",
                headers={'Authorization': f'Bearer {token}'},
                timeout=10
            )
            
            print(f"Respuesta con token: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                users = json.dumps(data, indent=2)
                QMessageBox.information(self, "Token Válido", f"El token es válido y se pudo acceder a un endpoint protegido.\n\nUsuarios:\n{users}")
            else:
                QMessageBox.warning(self, "Token Inválido", f"El token no es válido o no tiene permisos. Código: {response.status_code}\nRespuesta: {response.text}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al probar el token: {str(e)}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TestConnectionWindow()
    window.show()
    sys.exit(app.exec_())

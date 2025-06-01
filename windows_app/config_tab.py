from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                            QPushButton, QFormLayout, QLineEdit, QGroupBox,
                            QMessageBox, QCheckBox)
from PyQt5.QtCore import Qt

class ConfigTab(QWidget):
    """Pestaña para configurar la aplicación"""
    
    def __init__(self, api_client):
        super().__init__()
        self.api_client = api_client
        
        # Crear layout principal
        layout = QVBoxLayout(self)
        
        # Título
        title_label = QLabel("Configuración")
        title_label.setStyleSheet("font-size: 24px; font-weight: bold; color: #5a5c69;")
        layout.addWidget(title_label)
        
        # Descripción
        desc_label = QLabel("Configura la conexión con el servidor y otras opciones")
        desc_label.setStyleSheet("font-size: 14px; color: #858796; margin-bottom: 20px;")
        layout.addWidget(desc_label)
        
        # Grupo de configuración de API
        api_group = QGroupBox("Configuración de API")
        api_layout = QFormLayout()
        
        # URL de la API
        self.api_url_input = QLineEdit()
        self.api_url_input.setText(self.api_client.base_url)
        api_layout.addRow("URL de la API:", self.api_url_input)
        
        # Usuario
        self.username_input = QLineEdit()
        self.username_input.setText(self.api_client.username)
        api_layout.addRow("Usuario:", self.username_input)
        
        # Contraseña
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setText(self.api_client.password)
        api_layout.addRow("Contraseña:", self.password_input)
        
        # Botón de prueba de conexión
        self.test_button = QPushButton("Probar Conexión")
        self.test_button.setStyleSheet("""
            QPushButton {
                background-color: #4e73df;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #2e59d9;
            }
        """)
        self.test_button.clicked.connect(self.test_connection)
        api_layout.addRow("", self.test_button)
        
        api_group.setLayout(api_layout)
        layout.addWidget(api_group)
        
        # Grupo de opciones de la aplicación
        app_group = QGroupBox("Opciones de la Aplicación")
        app_layout = QFormLayout()
        
        # Iniciar sesión automáticamente
        self.auto_login_check = QCheckBox("Iniciar sesión automáticamente al abrir la aplicación")
        app_layout.addRow("", self.auto_login_check)
        
        # Actualizar datos automáticamente
        self.auto_refresh_check = QCheckBox("Actualizar datos automáticamente cada 5 minutos")
        app_layout.addRow("", self.auto_refresh_check)
        
        app_group.setLayout(app_layout)
        layout.addWidget(app_group)
        
        # Botones de acción
        button_layout = QHBoxLayout()
        
        self.save_button = QPushButton("Guardar Configuración")
        self.save_button.setStyleSheet("""
            QPushButton {
                background-color: #1cc88a;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #169b6b;
            }
        """)
        self.save_button.clicked.connect(self.save_config)
        
        button_layout.addStretch()
        button_layout.addWidget(self.save_button)
        
        layout.addLayout(button_layout)
        
        # Espacio adicional
        layout.addStretch()
    
    def test_connection(self):
        """Prueba la conexión con la API"""
        # Obtener URL de la API
        api_url = self.api_url_input.text()
        
        # Crear configuración temporal
        temp_config = {
            'api_url': api_url,
            'username': self.username_input.text(),
            'password': self.password_input.text(),
            'token': self.api_client.token
        }
        
        # Guardar configuración actual
        old_config = self.api_client.config.copy()
        
        # Aplicar configuración temporal
        self.api_client.config = temp_config
        self.api_client.base_url = api_url
        
        # Probar conexión
        if self.api_client.test_connection():
            QMessageBox.information(self, "Conexión Exitosa", 
                                   "La conexión con el servidor fue exitosa.")
        else:
            QMessageBox.warning(self, "Error de Conexión", 
                               "No se pudo conectar al servidor. Verifique la URL y la conexión a Internet.")
        
        # Restaurar configuración anterior
        self.api_client.config = old_config
        self.api_client.base_url = old_config['api_url']
    
    def save_config(self):
        """Guarda la configuración"""
        # Obtener datos de configuración
        config = {
            'api_url': self.api_url_input.text(),
            'username': self.username_input.text(),
            'password': self.password_input.text(),
            'token': self.api_client.token,
            'auto_login': self.auto_login_check.isChecked(),
            'auto_refresh': self.auto_refresh_check.isChecked()
        }
        
        # Guardar configuración
        if self.api_client.save_config(config):
            QMessageBox.information(self, "Configuración Guardada", 
                                   "La configuración se ha guardado correctamente.")
        else:
            QMessageBox.warning(self, "Error", 
                               "No se pudo guardar la configuración.")

from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                            QPushButton, QLineEdit, QFormLayout, QMessageBox,
                            QCheckBox, QFrame)
from PyQt5.QtGui import QIcon, QPixmap, QFont
from PyQt5.QtCore import Qt, pyqtSignal

class LoginDialog(QDialog):
    """Diálogo de inicio de sesión"""
    
    # Señal que se emite cuando el login es exitoso
    login_successful = pyqtSignal(dict)
    
    def __init__(self, api_client, parent=None):
        super().__init__(parent)
        self.api_client = api_client
        self.setWindowTitle("Iniciar Sesión - App Granja")
        self.setMinimumWidth(400)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        
        # Crear layout principal
        layout = QVBoxLayout(self)
        
        # Logo y título
        header_layout = QHBoxLayout()
        
        # Logo (si existe)
        logo_label = QLabel()
        try:
            pixmap = QPixmap("icons/logo.png")
            logo_label.setPixmap(pixmap.scaled(64, 64, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        except:
            # Si no hay logo, mostrar un texto
            logo_label.setText("🐔")
            logo_label.setStyleSheet("font-size: 48px;")
        
        header_layout.addWidget(logo_label)
        
        # Título
        title_layout = QVBoxLayout()
        title_label = QLabel("App Granja")
        title_label.setStyleSheet("font-size: 24px; font-weight: bold; color: #5a5c69;")
        subtitle_label = QLabel("Sistema de Gestión Avícola")
        subtitle_label.setStyleSheet("font-size: 14px; color: #858796;")
        
        title_layout.addWidget(title_label)
        title_layout.addWidget(subtitle_label)
        
        header_layout.addLayout(title_layout)
        layout.addLayout(header_layout)
        
        # Separador
        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setFrameShadow(QFrame.Sunken)
        layout.addWidget(separator)
        
        # Formulario de login
        form_layout = QFormLayout()
        
        # Usuario
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Ingrese su nombre de usuario")
        form_layout.addRow("Usuario:", self.username_input)
        
        # Contraseña
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setPlaceholderText("Ingrese su contraseña")
        form_layout.addRow("Contraseña:", self.password_input)
        
        # Recordar usuario
        self.remember_check = QCheckBox("Recordar usuario")
        form_layout.addRow("", self.remember_check)
        
        layout.addLayout(form_layout)
        
        # Botones
        buttons_layout = QHBoxLayout()
        
        # Botón de iniciar sesión
        self.login_button = QPushButton("Iniciar Sesión")
        self.login_button.setStyleSheet("""
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
        self.login_button.clicked.connect(self.login)
        
        # Botón de modo sin conexión
        self.offline_button = QPushButton("Modo Sin Conexión")
        self.offline_button.setStyleSheet("""
            QPushButton {
                background-color: #858796;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #717384;
            }
        """)
        self.offline_button.clicked.connect(self.offline_mode)
        
        buttons_layout.addWidget(self.offline_button)
        buttons_layout.addWidget(self.login_button)
        
        layout.addLayout(buttons_layout)
        
        # Mensaje de error (inicialmente oculto)
        self.error_label = QLabel()
        self.error_label.setStyleSheet("color: #e74a3b; margin-top: 10px;")
        self.error_label.setVisible(False)
        layout.addWidget(self.error_label)
        
        # Cargar usuario recordado si existe
        self.load_remembered_user()
    
    def login(self):
        """Intenta iniciar sesión con las credenciales proporcionadas"""
        username = self.username_input.text().strip()
        password = self.password_input.text()
        
        if not username or not password:
            self.show_error("Por favor ingrese usuario y contraseña")
            return
        
        # Intentar login
        success, result = self.api_client.login(username, password)
        
        if success:
            # Guardar usuario si se seleccionó "recordar"
            if self.remember_check.isChecked():
                self.save_remembered_user(username)
            
            # Emitir señal de login exitoso
            self.login_successful.emit(result)
            
            # Cerrar diálogo
            self.accept()
        else:
            # Mostrar error
            self.show_error(f"Error de inicio de sesión: {result}")
    
    def offline_mode(self):
        """Inicia la aplicación en modo sin conexión"""
        # Emitir señal con datos de ejemplo
        self.login_successful.emit({
            "username": "offline_user",
            "is_offline": True,
            "empresa": "Empresa de Ejemplo",
            "granja": "Granja de Ejemplo"
        })
        
        # Cerrar diálogo
        self.accept()
    
    def show_error(self, message):
        """Muestra un mensaje de error en el formulario"""
        self.error_label.setText(message)
        self.error_label.setVisible(True)
    
    def load_remembered_user(self):
        """Carga el usuario recordado si existe"""
        remembered_user = self.api_client.get_remembered_user()
        if remembered_user:
            self.username_input.setText(remembered_user)
            self.remember_check.setChecked(True)
    
    def save_remembered_user(self, username):
        """Guarda el usuario para recordarlo"""
        self.api_client.save_remembered_user(username)

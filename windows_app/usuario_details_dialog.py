from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QFormLayout, 
    QLabel, QPushButton, QListWidget
)
from PyQt5.QtCore import Qt

class UsuarioDetailsDialog(QDialog):
    """Diálogo para mostrar los detalles de un usuario"""
    
    def __init__(self, parent=None, api_client=None, usuario_id=None):
        super().__init__(parent)
        self.api_client = api_client
        self.usuario_id = usuario_id
        
        # Configurar diálogo
        self.setWindowTitle("Detalles de Usuario")
        self.setMinimumWidth(500)
        self.setMinimumHeight(400)
        
        # Crear layout principal
        self.layout = QVBoxLayout(self)
        
        # Crear formulario
        self.create_form()
        
        # Crear botones
        self.create_buttons()
        
        # Cargar datos del usuario
        self.load_usuario_data()
    
    def create_form(self):
        """Crea el formulario para mostrar los datos del usuario"""
        form_layout = QFormLayout()
        
        # Campos de usuario
        self.username_label = QLabel()
        self.username_label.setTextInteractionFlags(Qt.TextSelectableByMouse)
        form_layout.addRow("Nombre de usuario:", self.username_label)
        
        self.name_label = QLabel()
        self.name_label.setTextInteractionFlags(Qt.TextSelectableByMouse)
        form_layout.addRow("Nombre completo:", self.name_label)
        
        self.email_label = QLabel()
        self.email_label.setTextInteractionFlags(Qt.TextSelectableByMouse)
        form_layout.addRow("Email:", self.email_label)
        
        self.status_label = QLabel()
        form_layout.addRow("Estado:", self.status_label)
        
        self.staff_label = QLabel()
        form_layout.addRow("Acceso al admin:", self.staff_label)
        
        self.superuser_label = QLabel()
        form_layout.addRow("Superusuario:", self.superuser_label)
        
        self.date_joined_label = QLabel()
        form_layout.addRow("Fecha de registro:", self.date_joined_label)
        
        self.last_login_label = QLabel()
        form_layout.addRow("Último acceso:", self.last_login_label)
        
        # Lista de grupos
        form_layout.addRow(QLabel("Grupos:"))
        self.grupos_list = QListWidget()
        self.grupos_list.setMaximumHeight(100)
        form_layout.addRow(self.grupos_list)
        
        self.layout.addLayout(form_layout)
    
    def create_buttons(self):
        """Crea los botones de acción"""
        button_layout = QHBoxLayout()
        
        self.close_button = QPushButton("Cerrar")
        self.close_button.clicked.connect(self.accept)
        button_layout.addWidget(self.close_button)
        
        self.edit_button = QPushButton("Editar")
        self.edit_button.clicked.connect(self.edit_usuario)
        button_layout.addWidget(self.edit_button)
        
        self.layout.addLayout(button_layout)
    
    def load_usuario_data(self):
        """Carga los datos del usuario"""
        if not self.usuario_id:
            return
            
        success, usuario = self.api_client.get_usuario(self.usuario_id)
        
        if success and usuario:
            # Llenar campos con datos del usuario
            self.username_label.setText(usuario.get('username', ''))
            
            nombre_completo = f"{usuario.get('first_name', '')} {usuario.get('last_name', '')}".strip()
            self.name_label.setText(nombre_completo)
            
            self.email_label.setText(usuario.get('email', ''))
            
            # Estado
            is_active = usuario.get('is_active', False)
            self.status_label.setText("Activo" if is_active else "Inactivo")
            self.status_label.setStyleSheet(
                "color: green; font-weight: bold;" if is_active else "color: red; font-weight: bold;"
            )
            
            # Acceso al admin
            is_staff = usuario.get('is_staff', False)
            self.staff_label.setText("Sí" if is_staff else "No")
            
            # Superusuario
            is_superuser = usuario.get('is_superuser', False)
            self.superuser_label.setText("Sí" if is_superuser else "No")
            
            # Fechas
            self.date_joined_label.setText(usuario.get('date_joined', ''))
            self.last_login_label.setText(usuario.get('last_login', ''))
            
            # Cargar grupos
            self.load_grupos(usuario.get('groups', []))
    
    def load_grupos(self, grupo_ids):
        """Carga los grupos del usuario"""
        success, grupos = self.api_client.get_grupos()
        
        if success and grupos:
            self.grupos_list.clear()
            
            for grupo in grupos:
                if grupo.get('id') in grupo_ids:
                    self.grupos_list.addItem(grupo.get('name', ''))
    
    def edit_usuario(self):
        """Abre el diálogo para editar el usuario"""
        from usuario_dialog import UsuarioDialog
        dialog = UsuarioDialog(self.parent(), self.api_client, self.usuario_id)
        if dialog.exec_():
            # Recargar datos
            self.load_usuario_data()
            # Notificar al padre que se actualizó el usuario
            self.parent().refresh_usuarios()

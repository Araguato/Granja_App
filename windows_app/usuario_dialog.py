from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QFormLayout, 
    QLabel, QLineEdit, QComboBox, QCheckBox, QPushButton, 
    QMessageBox, QListWidget, QListWidgetItem
)
from PyQt5.QtCore import Qt

class UsuarioDialog(QDialog):
    """Diálogo para crear o editar usuarios"""
    
    def __init__(self, parent=None, api_client=None, usuario_id=None):
        super().__init__(parent)
        self.api_client = api_client
        self.usuario_id = usuario_id
        self.usuario_data = {}
        self.grupos = []
        
        # Configurar diálogo
        self.setWindowTitle("Usuario" if not usuario_id else "Editar Usuario")
        self.setMinimumWidth(400)
        self.setMinimumHeight(500)
        
        # Crear layout principal
        self.layout = QVBoxLayout(self)
        
        # Crear formulario
        self.create_form()
        
        # Crear botones
        self.create_buttons()
        
        # Cargar datos si es edición
        if self.usuario_id:
            self.load_usuario_data()
        
        # Cargar lista de grupos
        self.load_grupos()
    
    def create_form(self):
        """Crea el formulario para los datos del usuario"""
        form_layout = QFormLayout()
        
        # Campos de usuario
        self.username_input = QLineEdit()
        form_layout.addRow("Nombre de usuario:", self.username_input)
        
        self.first_name_input = QLineEdit()
        form_layout.addRow("Nombre:", self.first_name_input)
        
        self.last_name_input = QLineEdit()
        form_layout.addRow("Apellido:", self.last_name_input)
        
        self.email_input = QLineEdit()
        form_layout.addRow("Email:", self.email_input)
        
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        form_layout.addRow("Contraseña:", self.password_input)
        
        self.confirm_password_input = QLineEdit()
        self.confirm_password_input.setEchoMode(QLineEdit.Password)
        form_layout.addRow("Confirmar contraseña:", self.confirm_password_input)
        
        # Checkbox para permisos
        self.is_active_checkbox = QCheckBox("Usuario activo")
        self.is_active_checkbox.setChecked(True)
        form_layout.addRow("", self.is_active_checkbox)
        
        self.is_staff_checkbox = QCheckBox("Acceso al admin")
        form_layout.addRow("", self.is_staff_checkbox)
        
        self.is_superuser_checkbox = QCheckBox("Superusuario")
        form_layout.addRow("", self.is_superuser_checkbox)
        
        # Lista de grupos
        form_layout.addRow(QLabel("Grupos:"))
        self.grupos_list = QListWidget()
        self.grupos_list.setSelectionMode(QListWidget.MultiSelection)
        form_layout.addRow(self.grupos_list)
        
        self.layout.addLayout(form_layout)
    
    def create_buttons(self):
        """Crea los botones de acción"""
        button_layout = QHBoxLayout()
        
        self.cancel_button = QPushButton("Cancelar")
        self.cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(self.cancel_button)
        
        self.save_button = QPushButton("Guardar")
        self.save_button.clicked.connect(self.save_usuario)
        button_layout.addWidget(self.save_button)
        
        self.layout.addLayout(button_layout)
    
    def load_usuario_data(self):
        """Carga los datos del usuario para edición"""
        success, usuario = self.api_client.get_usuario(self.usuario_id)
        
        if success and usuario:
            self.usuario_data = usuario
            
            # Llenar campos con datos del usuario
            self.username_input.setText(usuario.get('username', ''))
            self.first_name_input.setText(usuario.get('first_name', ''))
            self.last_name_input.setText(usuario.get('last_name', ''))
            self.email_input.setText(usuario.get('email', ''))
            
            # Campos de contraseña vacíos para edición
            self.password_input.clear()
            self.confirm_password_input.clear()
            
            # Checkboxes
            self.is_active_checkbox.setChecked(usuario.get('is_active', True))
            self.is_staff_checkbox.setChecked(usuario.get('is_staff', False))
            self.is_superuser_checkbox.setChecked(usuario.get('is_superuser', False))
    
    def load_grupos(self):
        """Carga la lista de grupos disponibles"""
        success, grupos = self.api_client.get_grupos()
        
        if success and grupos:
            self.grupos = grupos
            self.grupos_list.clear()
            
            # Grupos del usuario (si está en modo edición)
            usuario_grupos = self.usuario_data.get('groups', []) if self.usuario_id else []
            
            # Llenar lista de grupos
            for grupo in grupos:
                item = QListWidgetItem(grupo.get('name', ''))
                item.setData(Qt.UserRole, grupo.get('id'))
                self.grupos_list.addItem(item)
                
                # Seleccionar si el usuario pertenece al grupo
                if grupo.get('id') in usuario_grupos:
                    item.setSelected(True)
    
    def validate_form(self):
        """Valida el formulario antes de guardar"""
        # Verificar campos obligatorios
        if not self.username_input.text().strip():
            QMessageBox.warning(self, "Error", "El nombre de usuario es obligatorio")
            return False
        
        if not self.email_input.text().strip():
            QMessageBox.warning(self, "Error", "El email es obligatorio")
            return False
        
        # Verificar contraseñas en modo creación
        if not self.usuario_id:
            if not self.password_input.text():
                QMessageBox.warning(self, "Error", "La contraseña es obligatoria")
                return False
            
            if self.password_input.text() != self.confirm_password_input.text():
                QMessageBox.warning(self, "Error", "Las contraseñas no coinciden")
                return False
        # En modo edición, verificar solo si se ha ingresado una contraseña
        elif self.password_input.text() and self.password_input.text() != self.confirm_password_input.text():
            QMessageBox.warning(self, "Error", "Las contraseñas no coinciden")
            return False
        
        return True
    
    def get_selected_grupos(self):
        """Obtiene los IDs de los grupos seleccionados"""
        selected_grupos = []
        for i in range(self.grupos_list.count()):
            item = self.grupos_list.item(i)
            if item.isSelected():
                grupo_id = item.data(Qt.UserRole)
                selected_grupos.append(grupo_id)
        return selected_grupos
    
    def save_usuario(self):
        """Guarda los datos del usuario"""
        if not self.validate_form():
            return
        
        # Preparar datos
        usuario_data = {
            'username': self.username_input.text().strip(),
            'first_name': self.first_name_input.text().strip(),
            'last_name': self.last_name_input.text().strip(),
            'email': self.email_input.text().strip(),
            'is_active': self.is_active_checkbox.isChecked(),
            'is_staff': self.is_staff_checkbox.isChecked(),
            'is_superuser': self.is_superuser_checkbox.isChecked(),
            'groups': self.get_selected_grupos()
        }
        
        # Agregar contraseña solo si se ha ingresado
        if self.password_input.text():
            usuario_data['password'] = self.password_input.text()
        
        # Guardar usuario
        if self.usuario_id:
            success, result = self.api_client.update_usuario(self.usuario_id, usuario_data)
        else:
            success, result = self.api_client.create_usuario(usuario_data)
        
        if success:
            self.accept()
        else:
            QMessageBox.warning(self, "Error", f"Error al guardar usuario: {result}")

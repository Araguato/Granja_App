from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QFormLayout, 
    QLabel, QPushButton, QListWidget
)
from PyQt5.QtCore import Qt

class GrupoDetailsDialog(QDialog):
    """Diálogo para mostrar los detalles de un grupo"""
    
    def __init__(self, parent=None, api_client=None, grupo_id=None):
        super().__init__(parent)
        self.api_client = api_client
        self.grupo_id = grupo_id
        
        # Configurar diálogo
        self.setWindowTitle("Detalles de Grupo")
        self.setMinimumWidth(500)
        self.setMinimumHeight(300)
        
        # Crear layout principal
        self.layout = QVBoxLayout(self)
        
        # Crear formulario
        self.create_form()
        
        # Crear botones
        self.create_buttons()
        
        # Cargar datos del grupo
        self.load_grupo_data()
    
    def create_form(self):
        """Crea el formulario para mostrar los datos del grupo"""
        form_layout = QFormLayout()
        
        # Campos de grupo
        self.name_label = QLabel()
        self.name_label.setTextInteractionFlags(Qt.TextSelectableByMouse)
        form_layout.addRow("Nombre:", self.name_label)
        
        # Lista de usuarios en el grupo
        form_layout.addRow(QLabel("Usuarios en este grupo:"))
        self.usuarios_list = QListWidget()
        self.usuarios_list.setMaximumHeight(150)
        form_layout.addRow(self.usuarios_list)
        
        # Nota sobre permisos
        note_label = QLabel("Nota: La gestión de permisos debe realizarse desde el panel de administración de Django.")
        note_label.setStyleSheet("color: gray; font-style: italic;")
        form_layout.addRow(note_label)
        
        self.layout.addLayout(form_layout)
    
    def create_buttons(self):
        """Crea los botones de acción"""
        button_layout = QHBoxLayout()
        
        self.close_button = QPushButton("Cerrar")
        self.close_button.clicked.connect(self.accept)
        button_layout.addWidget(self.close_button)
        
        self.edit_button = QPushButton("Editar")
        self.edit_button.clicked.connect(self.edit_grupo)
        button_layout.addWidget(self.edit_button)
        
        self.layout.addLayout(button_layout)
    
    def load_grupo_data(self):
        """Carga los datos del grupo"""
        if not self.grupo_id:
            return
            
        success, grupo = self.api_client.get_grupo(self.grupo_id)
        
        if success and grupo:
            # Llenar campos con datos del grupo
            self.name_label.setText(grupo.get('name', ''))
            
            # Cargar usuarios del grupo
            self.load_usuarios_in_grupo()
    
    def load_usuarios_in_grupo(self):
        """Carga los usuarios que pertenecen al grupo"""
        success, usuarios = self.api_client.get_usuarios()
        
        if success and usuarios:
            self.usuarios_list.clear()
            
            for usuario in usuarios:
                grupos = usuario.get('groups', [])
                if self.grupo_id in grupos or str(self.grupo_id) in [str(g) for g in grupos]:
                    nombre = f"{usuario.get('username', '')} ({usuario.get('first_name', '')} {usuario.get('last_name', '')})".strip()
                    self.usuarios_list.addItem(nombre)
    
    def edit_grupo(self):
        """Abre el diálogo para editar el grupo"""
        from grupo_dialog import GrupoDialog
        dialog = GrupoDialog(self.parent(), self.api_client, self.grupo_id)
        if dialog.exec_():
            # Recargar datos
            self.load_grupo_data()
            # Notificar al padre que se actualizó el grupo
            self.parent().refresh_grupos()

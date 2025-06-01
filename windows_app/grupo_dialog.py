from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QFormLayout, 
    QLabel, QLineEdit, QPushButton, QMessageBox
)

class GrupoDialog(QDialog):
    """Diálogo para crear o editar grupos"""
    
    def __init__(self, parent=None, api_client=None, grupo_id=None):
        super().__init__(parent)
        self.api_client = api_client
        self.grupo_id = grupo_id
        self.grupo_data = {}
        
        # Configurar diálogo
        self.setWindowTitle("Grupo" if not grupo_id else "Editar Grupo")
        self.setMinimumWidth(400)
        self.setMinimumHeight(200)
        
        # Crear layout principal
        self.layout = QVBoxLayout(self)
        
        # Crear formulario
        self.create_form()
        
        # Crear botones
        self.create_buttons()
        
        # Cargar datos si es edición
        if self.grupo_id:
            self.load_grupo_data()
    
    def create_form(self):
        """Crea el formulario para los datos del grupo"""
        form_layout = QFormLayout()
        
        # Campos de grupo
        self.name_input = QLineEdit()
        form_layout.addRow("Nombre:", self.name_input)
        
        # Nota sobre permisos
        form_layout.addRow(QLabel("Nota: La gestión de permisos debe realizarse desde el panel de administración de Django."))
        
        self.layout.addLayout(form_layout)
    
    def create_buttons(self):
        """Crea los botones de acción"""
        button_layout = QHBoxLayout()
        
        self.cancel_button = QPushButton("Cancelar")
        self.cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(self.cancel_button)
        
        self.save_button = QPushButton("Guardar")
        self.save_button.clicked.connect(self.save_grupo)
        button_layout.addWidget(self.save_button)
        
        self.layout.addLayout(button_layout)
    
    def load_grupo_data(self):
        """Carga los datos del grupo para edición"""
        success, grupo = self.api_client.get_grupo(self.grupo_id)
        
        if success and grupo:
            self.grupo_data = grupo
            
            # Llenar campos con datos del grupo
            self.name_input.setText(grupo.get('name', ''))
    
    def validate_form(self):
        """Valida el formulario antes de guardar"""
        # Verificar campos obligatorios
        if not self.name_input.text().strip():
            QMessageBox.warning(self, "Error", "El nombre del grupo es obligatorio")
            return False
        
        return True
    
    def save_grupo(self):
        """Guarda los datos del grupo"""
        if not self.validate_form():
            return
        
        # Preparar datos
        grupo_data = {
            'name': self.name_input.text().strip(),
            'permissions': self.grupo_data.get('permissions', []) if self.grupo_id else []
        }
        
        # Guardar grupo
        if self.grupo_id:
            # Mostrar mensaje informativo ya que la funcionalidad está en desarrollo
            QMessageBox.information(
                self, 
                "Información", 
                "La funcionalidad de edición de grupos está en desarrollo. Por favor, utilice el panel de administración de Django."
            )
            self.accept()
        else:
            # Mostrar mensaje informativo ya que la funcionalidad está en desarrollo
            QMessageBox.information(
                self, 
                "Información", 
                "La funcionalidad de creación de grupos está en desarrollo. Por favor, utilice el panel de administración de Django."
            )
            self.accept()

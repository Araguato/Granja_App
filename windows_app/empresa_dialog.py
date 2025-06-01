from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QFormLayout, 
    QLabel, QLineEdit, QTextEdit, QPushButton
)

class EmpresaDialog(QDialog):
    """Diálogo para crear o editar una empresa"""
    
    def __init__(self, parent=None, empresa_data=None):
        super().__init__(parent)
        self.setWindowTitle("Empresa" if empresa_data else "Nueva Empresa")
        self.setMinimumWidth(400)
        
        # Datos de la empresa (si se está editando)
        self.empresa_data = empresa_data
        
        # Crear layout
        layout = QVBoxLayout(self)
        
        # Formulario
        form_layout = QFormLayout()
        
        # Nombre
        self.nombre_input = QLineEdit()
        if empresa_data:
            self.nombre_input.setText(empresa_data.get('nombre', ''))
        form_layout.addRow("Nombre:", self.nombre_input)
        
        # NIT
        self.nit_input = QLineEdit()
        if empresa_data:
            self.nit_input.setText(empresa_data.get('nit', ''))
        form_layout.addRow("NIT:", self.nit_input)
        
        # Dirección
        self.direccion_input = QLineEdit()
        if empresa_data:
            self.direccion_input.setText(empresa_data.get('direccion', ''))
        form_layout.addRow("Dirección:", self.direccion_input)
        
        # Teléfono
        self.telefono_input = QLineEdit()
        if empresa_data:
            self.telefono_input.setText(empresa_data.get('telefono', ''))
        form_layout.addRow("Teléfono:", self.telefono_input)
        
        # Email
        self.email_input = QLineEdit()
        if empresa_data:
            self.email_input.setText(empresa_data.get('email', ''))
        form_layout.addRow("Email:", self.email_input)
        
        # Sitio web
        self.sitio_web_input = QLineEdit()
        if empresa_data:
            self.sitio_web_input.setText(empresa_data.get('sitio_web', ''))
        form_layout.addRow("Sitio Web:", self.sitio_web_input)
        
        # Descripción
        self.descripcion_input = QTextEdit()
        self.descripcion_input.setMaximumHeight(100)
        if empresa_data:
            self.descripcion_input.setText(empresa_data.get('descripcion', ''))
        form_layout.addRow("Descripción:", self.descripcion_input)
        
        layout.addLayout(form_layout)
        
        # Botones
        buttons_layout = QHBoxLayout()
        
        cancel_button = QPushButton("Cancelar")
        cancel_button.clicked.connect(self.reject)
        buttons_layout.addWidget(cancel_button)
        
        save_button = QPushButton("Guardar")
        save_button.setStyleSheet("""
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
        save_button.clicked.connect(self.accept)
        buttons_layout.addWidget(save_button)
        
        layout.addLayout(buttons_layout)
    
    def get_data(self):
        """Obtiene los datos del formulario"""
        return {
            'nombre': self.nombre_input.text(),
            'nit': self.nit_input.text(),
            'direccion': self.direccion_input.text(),
            'telefono': self.telefono_input.text(),
            'email': self.email_input.text(),
            'sitio_web': self.sitio_web_input.text(),
            'descripcion': self.descripcion_input.toPlainText()
        }

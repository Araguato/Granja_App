import os
import datetime
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                            QPushButton, QTableWidget, QTableWidgetItem,
                            QDialog, QFormLayout, QLineEdit, QComboBox,
                            QMessageBox, QTextEdit, QSpinBox, QHeaderView, QStyle)
from PyQt5.QtCore import Qt, QDateTime

class CreateRazaDialog(QDialog):
    """Diálogo para crear una nueva raza"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Crear Nueva Raza")
        self.setMinimumWidth(400)
        
        # Crear layout
        layout = QVBoxLayout(self)
        
        # Formulario
        form_layout = QFormLayout()
        
        # Nombre
        self.nombre_input = QLineEdit()
        form_layout.addRow("Nombre:", self.nombre_input)
        
        # Tipo
        self.tipo_combo = QComboBox()
        self.tipo_combo.addItems(["Ponedora", "Engorde", "Doble Propósito"])
        form_layout.addRow("Tipo:", self.tipo_combo)
        
        # Producción de huevos (sólo para ponedoras)
        self.produccion_spin = QSpinBox()
        self.produccion_spin.setRange(0, 500)
        self.produccion_spin.setSuffix(" huevos/año")
        self.produccion_spin.setValue(280)
        form_layout.addRow("Producción:", self.produccion_spin)
        
        # Peso promedio
        self.peso_spin = QSpinBox()
        self.peso_spin.setRange(0, 10000)
        self.peso_spin.setSuffix(" g")
        self.peso_spin.setValue(2000)
        form_layout.addRow("Peso promedio:", self.peso_spin)
        
        # Descripción
        self.descripcion_input = QTextEdit()
        self.descripcion_input.setMaximumHeight(100)
        form_layout.addRow("Descripción:", self.descripcion_input)
        
        layout.addLayout(form_layout)
        
        # Botones
        button_layout = QHBoxLayout()
        
        self.cancel_button = QPushButton("Cancelar")
        self.cancel_button.clicked.connect(self.reject)
        
        self.save_button = QPushButton("Guardar")
        self.save_button.setStyleSheet("""
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
        self.save_button.clicked.connect(self.accept)
        
        button_layout.addWidget(self.cancel_button)
        button_layout.addWidget(self.save_button)
        
        layout.addLayout(button_layout)
        
        # Conectar eventos
        self.tipo_combo.currentIndexChanged.connect(self.update_form)
        
        # Inicializar formulario
        self.update_form()
    
    def update_form(self):
        """Actualiza el formulario según el tipo de raza seleccionado"""
        tipo = self.tipo_combo.currentText()
        
        # Mostrar/ocultar campos según el tipo
        if tipo == "Ponedora":
            self.produccion_spin.setEnabled(True)
        else:
            self.produccion_spin.setEnabled(False)
    
    def get_data(self):
        """Obtiene los datos del formulario"""
        return {
            'nombre': self.nombre_input.text(),
            'tipo': self.tipo_combo.currentText(),
            'produccion': self.produccion_spin.value() if self.tipo_combo.currentText() == "Ponedora" else 0,
            'peso': self.peso_spin.value(),
            'descripcion': self.descripcion_input.toPlainText()
        }

class EditRazaDialog(CreateRazaDialog):
    """Diálogo para editar una raza existente"""
    
    def __init__(self, parent=None, raza_data=None):
        super().__init__(parent)
        self.setWindowTitle("Editar Raza")
        
        # Llenar el formulario con los datos de la raza
        if raza_data:
            self.nombre_input.setText(raza_data.get('nombre', ''))
            
            tipo_index = self.tipo_combo.findText(raza_data.get('tipo', ''))
            if tipo_index >= 0:
                self.tipo_combo.setCurrentIndex(tipo_index)
            
            self.produccion_spin.setValue(raza_data.get('produccion', 280))
            self.peso_spin.setValue(raza_data.get('peso', 2000))
            self.descripcion_input.setPlainText(raza_data.get('descripcion', ''))

class RazasTab(QWidget):
    """Pestaña para gestionar razas"""
    
    def __init__(self, api_client):
        super().__init__()
        self.api_client = api_client
        
        # Crear layout principal
        layout = QVBoxLayout(self)
        
        # Título
        title_label = QLabel("Gestión de Razas")
        title_label.setStyleSheet("font-size: 24px; font-weight: bold; color: #5a5c69;")
        layout.addWidget(title_label)
        
        # Descripción
        desc_label = QLabel("Administra las razas de aves")
        desc_label.setStyleSheet("font-size: 14px; color: #858796; margin-bottom: 20px;")
        layout.addWidget(desc_label)
        
        # Botones de acción
        action_layout = QHBoxLayout()
        
        self.new_button = QPushButton("Nueva Raza")
        self.new_button.setStyleSheet("""
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
        self.new_button.clicked.connect(self.create_raza)
        
        self.refresh_button = QPushButton("Actualizar")
        self.refresh_button.setStyleSheet("""
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
        self.refresh_button.clicked.connect(self.refresh_data)
        
        action_layout.addWidget(self.new_button)
        action_layout.addWidget(self.refresh_button)
        action_layout.addStretch()
        
        layout.addLayout(action_layout)
        
        # Tabla de razas
        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels([
            "ID", "Nombre", "Tipo", "Producción", "Peso", "Acciones"
        ])
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        
        # Ajustar ancho de columnas
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(1, QHeaderView.Stretch)  # Nombre se estira
        
        layout.addWidget(self.table)
        
        # Cargar datos iniciales
        self.refresh_data()
    
    def refresh_data(self):
        """Actualiza los datos de la tabla de razas"""
        # En una aplicación real, estos datos vendrían de la API
        # Aquí usamos datos de ejemplo
        razas = [
            {
                'id': 1,
                'nombre': 'Isa Brown',
                'tipo': 'Ponedora',
                'produccion': 320,
                'peso': 1800,
                'descripcion': 'Excelente ponedora de huevos marrones. Alta producción y bajo consumo de alimento.'
            },
            {
                'id': 2,
                'nombre': 'Leghorn Blanca',
                'tipo': 'Ponedora',
                'produccion': 300,
                'peso': 1600,
                'descripcion': 'Ponedora de huevos blancos. Muy eficiente y resistente a enfermedades.'
            },
            {
                'id': 3,
                'nombre': 'Ross 308',
                'tipo': 'Engorde',
                'produccion': 0,
                'peso': 2800,
                'descripcion': 'Excelente para producción de carne. Rápido crecimiento y buena conversión alimenticia.'
            },
            {
                'id': 4,
                'nombre': 'Rhode Island Red',
                'tipo': 'Doble Propósito',
                'produccion': 250,
                'peso': 2500,
                'descripcion': 'Buena para producción de huevos y carne. Resistente y adaptable a diferentes climas.'
            }
        ]
        
        # Limpiar tabla
        self.table.setRowCount(0)
        
        # Llenar tabla con datos
        for row, raza in enumerate(razas):
            self.table.insertRow(row)
            
            # ID
            id_item = QTableWidgetItem(str(raza.get('id', '')))
            self.table.setItem(row, 0, id_item)
            
            # Nombre
            name_item = QTableWidgetItem(raza.get('nombre', ''))
            self.table.setItem(row, 1, name_item)
            
            # Tipo
            tipo_item = QTableWidgetItem(raza.get('tipo', ''))
            self.table.setItem(row, 2, tipo_item)
            
            # Producción
            produccion = raza.get('produccion', 0)
            produccion_text = f"{produccion} huevos/año" if produccion > 0 else "N/A"
            produccion_item = QTableWidgetItem(produccion_text)
            self.table.setItem(row, 3, produccion_item)
            
            # Peso
            peso_item = QTableWidgetItem(f"{raza.get('peso', 0)} g")
            self.table.setItem(row, 4, peso_item)
            
            # Acciones
            actions_widget = QWidget()
            actions_layout = QHBoxLayout(actions_widget)
            actions_layout.setContentsMargins(4, 4, 4, 4)
            
            # Botón de editar
            edit_button = QPushButton()
            edit_button.setIcon(self.style().standardIcon(QStyle.SP_FileDialogDetailedView))
            edit_button.setToolTip("Editar")
            edit_button.clicked.connect(lambda _, id=raza.get('id'): self.edit_raza(id))
            
            # Botón de eliminar
            delete_button = QPushButton()
            delete_button.setIcon(self.style().standardIcon(QStyle.SP_TrashIcon))
            delete_button.setToolTip("Eliminar")
            delete_button.clicked.connect(lambda _, id=raza.get('id'): self.delete_raza(id))
            
            actions_layout.addWidget(edit_button)
            actions_layout.addWidget(delete_button)
            actions_layout.addStretch()
            
            self.table.setCellWidget(row, 5, actions_widget)
        
        # Ajustar tamaño de columnas
        self.table.resizeColumnsToContents()
    
    def create_raza(self):
        """Abre el diálogo para crear una nueva raza"""
        dialog = CreateRazaDialog(self)
        
        if dialog.exec_() == QDialog.Accepted:
            # Obtener datos del formulario
            raza_data = dialog.get_data()
            
            # En una aplicación real, aquí se enviarían los datos a la API
            QMessageBox.information(self, "Información", 
                                   f"Raza '{raza_data['nombre']}' creada correctamente.")
            
            # Actualizar tabla
            self.refresh_data()
    
    def edit_raza(self, raza_id):
        """Abre el diálogo para editar una raza existente"""
        # En una aplicación real, aquí se obtendría la información de la raza de la API
        # Buscar la raza en la lista de ejemplo
        raza_data = None
        for row in range(self.table.rowCount()):
            if self.table.item(row, 0).text() == str(raza_id):
                raza_data = {
                    'id': raza_id,
                    'nombre': self.table.item(row, 1).text(),
                    'tipo': self.table.item(row, 2).text(),
                    'produccion': int(self.table.item(row, 3).text().split()[0]) if self.table.item(row, 3).text() != "N/A" else 0,
                    'peso': int(self.table.item(row, 4).text().split()[0]),
                    'descripcion': f"Descripción de la raza {self.table.item(row, 1).text()}"
                }
                break
        
        if not raza_data:
            QMessageBox.warning(self, "Advertencia", "No se encontró la raza seleccionada.")
            return
        
        dialog = EditRazaDialog(self, raza_data)
        
        if dialog.exec_() == QDialog.Accepted:
            # Obtener datos del formulario
            updated_data = dialog.get_data()
            
            # En una aplicación real, aquí se enviarían los datos a la API
            QMessageBox.information(self, "Información", 
                                   f"Raza '{updated_data['nombre']}' actualizada correctamente.")
            
            # Actualizar tabla
            self.refresh_data()
    
    def delete_raza(self, raza_id):
        """Confirma y elimina una raza"""
        reply = QMessageBox.question(
            self, 'Confirmar Eliminación',
            f'¿Está seguro de que desea eliminar la raza con ID {raza_id}?',
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            # En una aplicación real, aquí se enviaría la solicitud de eliminación a la API
            QMessageBox.information(self, "Información", 
                                   f"Raza con ID {raza_id} eliminada correctamente.")
            
            # Actualizar tabla
            self.refresh_data()

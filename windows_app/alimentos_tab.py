import os
import datetime
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                            QPushButton, QTableWidget, QTableWidgetItem,
                            QDialog, QFormLayout, QLineEdit, QComboBox,
                            QMessageBox, QFileDialog, QDoubleSpinBox,
                            QSpinBox, QHeaderView, QStyle)
from PyQt5.QtCore import Qt, QDateTime

class CreateAlimentoDialog(QDialog):
    """Diálogo para crear un nuevo alimento"""
    
    def __init__(self, parent=None, proveedores=None):
        super().__init__(parent)
        self.setWindowTitle("Crear Nuevo Alimento")
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
        self.tipo_combo.addItems(["Inicio", "Crecimiento", "Postura", "Engorde"])
        form_layout.addRow("Tipo:", self.tipo_combo)
        
        # Proteína
        self.proteina_spin = QDoubleSpinBox()
        self.proteina_spin.setRange(0, 100)
        self.proteina_spin.setSuffix("%")
        self.proteina_spin.setValue(18.0)
        form_layout.addRow("Proteína:", self.proteina_spin)
        
        # Costo por kg
        self.costo_spin = QDoubleSpinBox()
        self.costo_spin.setRange(0, 10000)
        self.costo_spin.setPrefix("$")
        self.costo_spin.setValue(1.5)
        form_layout.addRow("Costo por kg:", self.costo_spin)
        
        # Proveedor
        self.proveedor_combo = QComboBox()
        if proveedores:
            for proveedor in proveedores:
                self.proveedor_combo.addItem(proveedor.get('nombre', ''), proveedor.get('id'))
        form_layout.addRow("Proveedor:", self.proveedor_combo)
        
        # Stock
        self.stock_spin = QSpinBox()
        self.stock_spin.setRange(0, 100000)
        self.stock_spin.setSuffix(" kg")
        self.stock_spin.setValue(1000)
        form_layout.addRow("Stock Inicial:", self.stock_spin)
        
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
    
    def get_data(self):
        """Obtiene los datos del formulario"""
        return {
            'nombre': self.nombre_input.text(),
            'tipo': self.tipo_combo.currentText(),
            'proteina': self.proteina_spin.value(),
            'costo_kg': self.costo_spin.value(),
            'proveedor_id': self.proveedor_combo.currentData(),
            'stock': self.stock_spin.value()
        }

class EditAlimentoDialog(CreateAlimentoDialog):
    """Diálogo para editar un alimento existente"""
    
    def __init__(self, parent=None, proveedores=None, alimento_data=None):
        super().__init__(parent, proveedores)
        self.setWindowTitle("Editar Alimento")
        
        # Llenar el formulario con los datos del alimento
        if alimento_data:
            self.nombre_input.setText(alimento_data.get('nombre', ''))
            
            tipo_index = self.tipo_combo.findText(alimento_data.get('tipo', ''))
            if tipo_index >= 0:
                self.tipo_combo.setCurrentIndex(tipo_index)
            
            self.proteina_spin.setValue(alimento_data.get('proteina', 18.0))
            self.costo_spin.setValue(alimento_data.get('costo_kg', 1.5))
            
            proveedor_id = alimento_data.get('proveedor_id')
            if proveedor_id:
                proveedor_index = self.proveedor_combo.findData(proveedor_id)
                if proveedor_index >= 0:
                    self.proveedor_combo.setCurrentIndex(proveedor_index)
            
            self.stock_spin.setValue(alimento_data.get('stock', 1000))

class AlimentosTab(QWidget):
    """Pestaña para gestionar alimentos"""
    
    def __init__(self, api_client):
        super().__init__()
        self.api_client = api_client
        
        # Crear layout principal
        layout = QVBoxLayout(self)
        
        # Título
        title_label = QLabel("Gestión de Alimentos")
        title_label.setStyleSheet("font-size: 24px; font-weight: bold; color: #5a5c69;")
        layout.addWidget(title_label)
        
        # Descripción
        desc_label = QLabel("Administra los alimentos para las aves")
        desc_label.setStyleSheet("font-size: 14px; color: #858796; margin-bottom: 20px;")
        layout.addWidget(desc_label)
        
        # Botones de acción
        action_layout = QHBoxLayout()
        
        self.new_button = QPushButton("Nuevo Alimento")
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
        self.new_button.clicked.connect(self.create_alimento)
        
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
        
        # Tabla de alimentos
        self.table = QTableWidget()
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels([
            "ID", "Nombre", "Tipo", "Proteína", "Costo/kg", 
            "Stock (kg)", "Acciones"
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
        """Actualiza los datos de la tabla de alimentos"""
        # En una aplicación real, estos datos vendrían de la API
        # Aquí usamos datos de ejemplo
        alimentos = [
            {
                'id': 1,
                'nombre': 'Inicio Premium',
                'tipo': 'Inicio',
                'proteina': 22.5,
                'costo_kg': 2.35,
                'stock': 1500,
                'proveedor_id': 1,
                'proveedor_nombre': 'Nutriaves S.A.'
            },
            {
                'id': 2,
                'nombre': 'Postura Standard',
                'tipo': 'Postura',
                'proteina': 18.0,
                'costo_kg': 1.85,
                'stock': 2300,
                'proveedor_id': 1,
                'proveedor_nombre': 'Nutriaves S.A.'
            },
            {
                'id': 3,
                'nombre': 'Crecimiento Plus',
                'tipo': 'Crecimiento',
                'proteina': 20.0,
                'costo_kg': 2.10,
                'stock': 1800,
                'proveedor_id': 2,
                'proveedor_nombre': 'Avícola Insumos C.A.'
            }
        ]
        
        # Limpiar tabla
        self.table.setRowCount(0)
        
        # Llenar tabla con datos
        for row, alimento in enumerate(alimentos):
            self.table.insertRow(row)
            
            # ID
            id_item = QTableWidgetItem(str(alimento.get('id', '')))
            self.table.setItem(row, 0, id_item)
            
            # Nombre
            name_item = QTableWidgetItem(alimento.get('nombre', ''))
            self.table.setItem(row, 1, name_item)
            
            # Tipo
            tipo_item = QTableWidgetItem(alimento.get('tipo', ''))
            self.table.setItem(row, 2, tipo_item)
            
            # Proteína
            proteina_item = QTableWidgetItem(f"{alimento.get('proteina', 0)}%")
            self.table.setItem(row, 3, proteina_item)
            
            # Costo/kg
            costo_item = QTableWidgetItem(f"${alimento.get('costo_kg', 0):.2f}")
            self.table.setItem(row, 4, costo_item)
            
            # Stock
            stock_item = QTableWidgetItem(f"{alimento.get('stock', 0)} kg")
            self.table.setItem(row, 5, stock_item)
            
            # Acciones
            actions_widget = QWidget()
            actions_layout = QHBoxLayout(actions_widget)
            actions_layout.setContentsMargins(4, 4, 4, 4)
            
            # Botón de editar
            edit_button = QPushButton()
            edit_button.setIcon(self.style().standardIcon(QStyle.SP_FileDialogDetailedView))
            edit_button.setToolTip("Editar")
            edit_button.clicked.connect(lambda _, id=alimento.get('id'): self.edit_alimento(id))
            
            # Botón de eliminar
            delete_button = QPushButton()
            delete_button.setIcon(self.style().standardIcon(QStyle.SP_TrashIcon))
            delete_button.setToolTip("Eliminar")
            delete_button.clicked.connect(lambda _, id=alimento.get('id'): self.delete_alimento(id))
            
            actions_layout.addWidget(edit_button)
            actions_layout.addWidget(delete_button)
            actions_layout.addStretch()
            
            self.table.setCellWidget(row, 6, actions_widget)
        
        # Ajustar tamaño de columnas
        self.table.resizeColumnsToContents()
    
    def get_proveedores(self):
        """Obtiene la lista de proveedores"""
        # En una aplicación real, estos datos vendrían de la API
        # Aquí usamos datos de ejemplo
        return [
            {
                'id': 1,
                'nombre': 'Nutriaves S.A.'
            },
            {
                'id': 2,
                'nombre': 'Avícola Insumos C.A.'
            },
            {
                'id': 3,
                'nombre': 'Distribuidora Agropecuaria'
            }
        ]
    
    def create_alimento(self):
        """Abre el diálogo para crear un nuevo alimento"""
        proveedores = self.get_proveedores()
        dialog = CreateAlimentoDialog(self, proveedores)
        
        if dialog.exec_() == QDialog.Accepted:
            # Obtener datos del formulario
            alimento_data = dialog.get_data()
            
            # En una aplicación real, aquí se enviarían los datos a la API
            QMessageBox.information(self, "Información", 
                                   f"Alimento '{alimento_data['nombre']}' creado correctamente.")
            
            # Actualizar tabla
            self.refresh_data()
    
    def edit_alimento(self, alimento_id):
        """Abre el diálogo para editar un alimento existente"""
        # En una aplicación real, aquí se obtendría la información del alimento de la API
        # Aquí usamos datos de ejemplo
        alimento_data = {
            'id': alimento_id,
            'nombre': f'Alimento {alimento_id}',
            'tipo': 'Postura',
            'proteina': 18.0,
            'costo_kg': 2.0,
            'stock': 1000,
            'proveedor_id': 1
        }
        
        proveedores = self.get_proveedores()
        dialog = EditAlimentoDialog(self, proveedores, alimento_data)
        
        if dialog.exec_() == QDialog.Accepted:
            # Obtener datos del formulario
            updated_data = dialog.get_data()
            
            # En una aplicación real, aquí se enviarían los datos a la API
            QMessageBox.information(self, "Información", 
                                   f"Alimento '{updated_data['nombre']}' actualizado correctamente.")
            
            # Actualizar tabla
            self.refresh_data()
    
    def delete_alimento(self, alimento_id):
        """Confirma y elimina un alimento"""
        reply = QMessageBox.question(
            self, 'Confirmar Eliminación',
            f'¿Está seguro de que desea eliminar el alimento con ID {alimento_id}?',
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            # En una aplicación real, aquí se enviaría la solicitud de eliminación a la API
            QMessageBox.information(self, "Información", 
                                   f"Alimento con ID {alimento_id} eliminado correctamente.")
            
            # Actualizar tabla
            self.refresh_data()

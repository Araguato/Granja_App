import os
import datetime
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                            QPushButton, QTableWidget, QTableWidgetItem,
                            QDialog, QFormLayout, QLineEdit, QComboBox,
                            QMessageBox, QDateEdit, QSpinBox, QHeaderView, QStyle)
from PyQt5.QtCore import Qt, QDateTime, QDate

class CreateVacunaDialog(QDialog):
    """Diálogo para crear una nueva vacuna"""
    
    def __init__(self, parent=None, proveedores=None):
        super().__init__(parent)
        self.setWindowTitle("Crear Nueva Vacuna")
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
        self.tipo_combo.addItems([
            "Newcastle", "Bronquitis", "Gumboro", "Viruela", "Coriza", 
            "Marek", "Salmonella", "Cólera Aviar", "Otro"
        ])
        form_layout.addRow("Tipo:", self.tipo_combo)
        
        # Lote
        self.lote_input = QLineEdit()
        form_layout.addRow("Lote:", self.lote_input)
        
        # Fecha de vencimiento
        self.vencimiento_date = QDateEdit()
        self.vencimiento_date.setCalendarPopup(True)
        self.vencimiento_date.setDate(QDate.currentDate().addMonths(12))  # 1 año por defecto
        form_layout.addRow("Vencimiento:", self.vencimiento_date)
        
        # Dosis disponibles
        self.dosis_spin = QSpinBox()
        self.dosis_spin.setRange(1, 10000)
        self.dosis_spin.setValue(100)
        form_layout.addRow("Dosis disponibles:", self.dosis_spin)
        
        # Proveedor
        self.proveedor_combo = QComboBox()
        if proveedores:
            for proveedor in proveedores:
                self.proveedor_combo.addItem(proveedor.get('nombre', ''), proveedor.get('id'))
        form_layout.addRow("Proveedor:", self.proveedor_combo)
        
        # Vía de administración
        self.via_combo = QComboBox()
        self.via_combo.addItems([
            "Ocular", "Nasal", "Oral", "Inyectable", "Agua de bebida", "Spray"
        ])
        form_layout.addRow("Vía de administración:", self.via_combo)
        
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
            'lote': self.lote_input.text(),
            'vencimiento': self.vencimiento_date.date().toString("yyyy-MM-dd"),
            'dosis': self.dosis_spin.value(),
            'proveedor_id': self.proveedor_combo.currentData(),
            'via': self.via_combo.currentText()
        }

class EditVacunaDialog(CreateVacunaDialog):
    """Diálogo para editar una vacuna existente"""
    
    def __init__(self, parent=None, proveedores=None, vacuna_data=None):
        super().__init__(parent, proveedores)
        self.setWindowTitle("Editar Vacuna")
        
        # Llenar el formulario con los datos de la vacuna
        if vacuna_data:
            self.nombre_input.setText(vacuna_data.get('nombre', ''))
            
            tipo_index = self.tipo_combo.findText(vacuna_data.get('tipo', ''))
            if tipo_index >= 0:
                self.tipo_combo.setCurrentIndex(tipo_index)
            
            self.lote_input.setText(vacuna_data.get('lote', ''))
            
            vencimiento_str = vacuna_data.get('vencimiento', '')
            if vencimiento_str:
                try:
                    vencimiento_date = QDate.fromString(vencimiento_str, "yyyy-MM-dd")
                    self.vencimiento_date.setDate(vencimiento_date)
                except:
                    pass
            
            self.dosis_spin.setValue(vacuna_data.get('dosis', 100))
            
            proveedor_id = vacuna_data.get('proveedor_id')
            if proveedor_id:
                proveedor_index = self.proveedor_combo.findData(proveedor_id)
                if proveedor_index >= 0:
                    self.proveedor_combo.setCurrentIndex(proveedor_index)
            
            via_index = self.via_combo.findText(vacuna_data.get('via', ''))
            if via_index >= 0:
                self.via_combo.setCurrentIndex(via_index)

class VacunasTab(QWidget):
    """Pestaña para gestionar vacunas"""
    
    def __init__(self, api_client):
        super().__init__()
        self.api_client = api_client
        
        # Crear layout principal
        layout = QVBoxLayout(self)
        
        # Título
        title_label = QLabel("Gestión de Vacunas")
        title_label.setStyleSheet("font-size: 24px; font-weight: bold; color: #5a5c69;")
        layout.addWidget(title_label)
        
        # Descripción
        desc_label = QLabel("Administra las vacunas para las aves")
        desc_label.setStyleSheet("font-size: 14px; color: #858796; margin-bottom: 20px;")
        layout.addWidget(desc_label)
        
        # Botones de acción
        action_layout = QHBoxLayout()
        
        self.new_button = QPushButton("Nueva Vacuna")
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
        self.new_button.clicked.connect(self.create_vacuna)
        
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
        
        # Tabla de vacunas
        self.table = QTableWidget()
        self.table.setColumnCount(8)
        self.table.setHorizontalHeaderLabels([
            "ID", "Nombre", "Tipo", "Lote", "Vencimiento", 
            "Dosis", "Vía", "Acciones"
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
        """Actualiza los datos de la tabla de vacunas"""
        # En una aplicación real, estos datos vendrían de la API
        # Aquí usamos datos de ejemplo
        vacunas = [
            {
                'id': 1,
                'nombre': 'Newcastle B1',
                'tipo': 'Newcastle',
                'lote': 'NC-2025-001',
                'vencimiento': '2026-05-15',
                'dosis': 500,
                'proveedor_id': 1,
                'proveedor_nombre': 'Laboratorios Avícolas S.A.',
                'via': 'Ocular'
            },
            {
                'id': 2,
                'nombre': 'Bronquitis H120',
                'tipo': 'Bronquitis',
                'lote': 'BR-2025-045',
                'vencimiento': '2026-03-20',
                'dosis': 300,
                'proveedor_id': 1,
                'proveedor_nombre': 'Laboratorios Avícolas S.A.',
                'via': 'Spray'
            },
            {
                'id': 3,
                'nombre': 'Gumboro D78',
                'tipo': 'Gumboro',
                'lote': 'GB-2025-123',
                'vencimiento': '2026-07-10',
                'dosis': 250,
                'proveedor_id': 2,
                'proveedor_nombre': 'BioVet C.A.',
                'via': 'Agua de bebida'
            }
        ]
        
        # Limpiar tabla
        self.table.setRowCount(0)
        
        # Llenar tabla con datos
        for row, vacuna in enumerate(vacunas):
            self.table.insertRow(row)
            
            # ID
            id_item = QTableWidgetItem(str(vacuna.get('id', '')))
            self.table.setItem(row, 0, id_item)
            
            # Nombre
            name_item = QTableWidgetItem(vacuna.get('nombre', ''))
            self.table.setItem(row, 1, name_item)
            
            # Tipo
            tipo_item = QTableWidgetItem(vacuna.get('tipo', ''))
            self.table.setItem(row, 2, tipo_item)
            
            # Lote
            lote_item = QTableWidgetItem(vacuna.get('lote', ''))
            self.table.setItem(row, 3, lote_item)
            
            # Vencimiento
            vencimiento_str = vacuna.get('vencimiento', '')
            if vencimiento_str:
                try:
                    vencimiento_date = QDate.fromString(vencimiento_str, "yyyy-MM-dd")
                    vencimiento_item = QTableWidgetItem(vencimiento_date.toString("dd/MM/yyyy"))
                except:
                    vencimiento_item = QTableWidgetItem(vencimiento_str)
            else:
                vencimiento_item = QTableWidgetItem("")
            self.table.setItem(row, 4, vencimiento_item)
            
            # Dosis
            dosis_item = QTableWidgetItem(str(vacuna.get('dosis', '')))
            self.table.setItem(row, 5, dosis_item)
            
            # Vía
            via_item = QTableWidgetItem(vacuna.get('via', ''))
            self.table.setItem(row, 6, via_item)
            
            # Acciones
            actions_widget = QWidget()
            actions_layout = QHBoxLayout(actions_widget)
            actions_layout.setContentsMargins(4, 4, 4, 4)
            
            # Botón de editar
            edit_button = QPushButton()
            edit_button.setIcon(self.style().standardIcon(QStyle.SP_FileDialogDetailedView))
            edit_button.setToolTip("Editar")
            edit_button.clicked.connect(lambda _, id=vacuna.get('id'): self.edit_vacuna(id))
            
            # Botón de eliminar
            delete_button = QPushButton()
            delete_button.setIcon(self.style().standardIcon(QStyle.SP_TrashIcon))
            delete_button.setToolTip("Eliminar")
            delete_button.clicked.connect(lambda _, id=vacuna.get('id'): self.delete_vacuna(id))
            
            actions_layout.addWidget(edit_button)
            actions_layout.addWidget(delete_button)
            actions_layout.addStretch()
            
            self.table.setCellWidget(row, 7, actions_widget)
        
        # Ajustar tamaño de columnas
        self.table.resizeColumnsToContents()
    
    def get_proveedores(self):
        """Obtiene la lista de proveedores"""
        # En una aplicación real, estos datos vendrían de la API
        # Aquí usamos datos de ejemplo
        return [
            {
                'id': 1,
                'nombre': 'Laboratorios Avícolas S.A.'
            },
            {
                'id': 2,
                'nombre': 'BioVet C.A.'
            },
            {
                'id': 3,
                'nombre': 'Veterinaria Industrial'
            }
        ]
    
    def create_vacuna(self):
        """Abre el diálogo para crear una nueva vacuna"""
        proveedores = self.get_proveedores()
        dialog = CreateVacunaDialog(self, proveedores)
        
        if dialog.exec_() == QDialog.Accepted:
            # Obtener datos del formulario
            vacuna_data = dialog.get_data()
            
            # En una aplicación real, aquí se enviarían los datos a la API
            QMessageBox.information(self, "Información", 
                                   f"Vacuna '{vacuna_data['nombre']}' creada correctamente.")
            
            # Actualizar tabla
            self.refresh_data()
    
    def edit_vacuna(self, vacuna_id):
        """Abre el diálogo para editar una vacuna existente"""
        # En una aplicación real, aquí se obtendría la información de la vacuna de la API
        # Buscar la vacuna en la lista de ejemplo
        vacuna_data = None
        for row in range(self.table.rowCount()):
            if self.table.item(row, 0).text() == str(vacuna_id):
                # Convertir formato de fecha
                vencimiento_str = self.table.item(row, 4).text()
                try:
                    vencimiento_date = QDate.fromString(vencimiento_str, "dd/MM/yyyy")
                    vencimiento = vencimiento_date.toString("yyyy-MM-dd")
                except:
                    vencimiento = vencimiento_str
                
                vacuna_data = {
                    'id': vacuna_id,
                    'nombre': self.table.item(row, 1).text(),
                    'tipo': self.table.item(row, 2).text(),
                    'lote': self.table.item(row, 3).text(),
                    'vencimiento': vencimiento,
                    'dosis': int(self.table.item(row, 5).text()),
                    'proveedor_id': 1,  # En una aplicación real, esto vendría de la API
                    'via': self.table.item(row, 6).text()
                }
                break
        
        if not vacuna_data:
            QMessageBox.warning(self, "Advertencia", "No se encontró la vacuna seleccionada.")
            return
        
        proveedores = self.get_proveedores()
        dialog = EditVacunaDialog(self, proveedores, vacuna_data)
        
        if dialog.exec_() == QDialog.Accepted:
            # Obtener datos del formulario
            updated_data = dialog.get_data()
            
            # En una aplicación real, aquí se enviarían los datos a la API
            QMessageBox.information(self, "Información", 
                                   f"Vacuna '{updated_data['nombre']}' actualizada correctamente.")
            
            # Actualizar tabla
            self.refresh_data()
    
    def delete_vacuna(self, vacuna_id):
        """Confirma y elimina una vacuna"""
        reply = QMessageBox.question(
            self, 'Confirmar Eliminación',
            f'¿Está seguro de que desea eliminar la vacuna con ID {vacuna_id}?',
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            # En una aplicación real, aquí se enviaría la solicitud de eliminación a la API
            QMessageBox.information(self, "Información", 
                                   f"Vacuna con ID {vacuna_id} eliminada correctamente.")
            
            # Actualizar tabla
            self.refresh_data()

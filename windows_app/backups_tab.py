import os
import datetime
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                            QPushButton, QTableWidget, QTableWidgetItem,
                            QDialog, QFormLayout, QLineEdit, QComboBox,
                            QMessageBox, QFileDialog, QTextEdit, QHeaderView, QStyle)
from PyQt5.QtCore import Qt, QDateTime

class CreateBackupDialog(QDialog):
    """Diálogo para crear un nuevo respaldo"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Crear Nuevo Respaldo")
        self.setMinimumWidth(400)
        
        # Crear layout
        layout = QVBoxLayout(self)
        
        # Formulario
        form_layout = QFormLayout()
        
        # Tipo de respaldo
        self.backup_type_combo = QComboBox()
        self.backup_type_combo.addItems(["Completo", "Base de Datos", "Archivos de Medios"])
        form_layout.addRow("Tipo de Respaldo:", self.backup_type_combo)
        
        # Notas
        self.notes_input = QTextEdit()
        self.notes_input.setMaximumHeight(100)
        form_layout.addRow("Notas:", self.notes_input)
        
        layout.addLayout(form_layout)
        
        # Botones
        button_layout = QHBoxLayout()
        
        self.cancel_button = QPushButton("Cancelar")
        self.cancel_button.clicked.connect(self.reject)
        
        self.save_button = QPushButton("Crear Respaldo")
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
        backup_type = ""
        if self.backup_type_combo.currentText() == "Completo":
            backup_type = "FULL"
        elif self.backup_type_combo.currentText() == "Base de Datos":
            backup_type = "DB"
        else:
            backup_type = "MEDIA"
            
        return {
            'backup_type': backup_type,
            'notes': self.notes_input.toPlainText()
        }

class RestoreBackupDialog(QDialog):
    """Diálogo para confirmar la restauración de un respaldo"""
    
    def __init__(self, parent=None, backup_data=None):
        super().__init__(parent)
        self.setWindowTitle("Restaurar Respaldo")
        self.setMinimumWidth(400)
        
        # Crear layout
        layout = QVBoxLayout(self)
        
        # Mensaje de advertencia
        warning_label = QLabel(
            "¡Advertencia! Está a punto de restaurar el sistema desde un respaldo. "
            "Esta acción reemplazará los datos actuales y no se puede deshacer."
        )
        warning_label.setWordWrap(True)
        warning_label.setStyleSheet("color: #e74a3b; font-weight: bold;")
        layout.addWidget(warning_label)
        
        # Información del respaldo
        if backup_data:
            info_layout = QFormLayout()
            
            info_layout.addRow("Nombre:", QLabel(backup_data.get('name', '')))
            info_layout.addRow("Tipo:", QLabel(backup_data.get('backup_type', '')))
            info_layout.addRow("Fecha:", QLabel(backup_data.get('created_at', '')))
            info_layout.addRow("Tamaño:", QLabel(f"{backup_data.get('size_in_mb', 0)} MB"))
            
            layout.addLayout(info_layout)
        
        # Botones
        button_layout = QHBoxLayout()
        
        self.cancel_button = QPushButton("Cancelar")
        self.cancel_button.clicked.connect(self.reject)
        
        self.restore_button = QPushButton("Confirmar Restauración")
        self.restore_button.setStyleSheet("""
            QPushButton {
                background-color: #f6c23e;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #dda20a;
            }
        """)
        self.restore_button.clicked.connect(self.accept)
        
        button_layout.addWidget(self.cancel_button)
        button_layout.addWidget(self.restore_button)
        
        layout.addLayout(button_layout)

class BackupsTab(QWidget):
    """Pestaña para gestionar respaldos"""
    
    def __init__(self, api_client):
        super().__init__()
        self.api_client = api_client
        
        # Crear layout principal
        layout = QVBoxLayout(self)
        
        # Título
        title_label = QLabel("Gestión de Respaldos")
        title_label.setStyleSheet("font-size: 24px; font-weight: bold; color: #5a5c69;")
        layout.addWidget(title_label)
        
        # Descripción
        desc_label = QLabel("Administra los respaldos y restauraciones del sistema")
        desc_label.setStyleSheet("font-size: 14px; color: #858796; margin-bottom: 20px;")
        layout.addWidget(desc_label)
        
        # Botones de acción
        action_layout = QHBoxLayout()
        
        self.new_button = QPushButton("Nuevo Respaldo")
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
        self.new_button.clicked.connect(self.create_backup)
        
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
        
        # Tabla de respaldos
        self.table = QTableWidget()
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels([
            "ID", "Nombre", "Tipo", "Estado", "Tamaño (MB)", 
            "Fecha de Creación", "Acciones"
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
        """Actualiza los datos de la tabla de respaldos"""
        # En una aplicación real, estos datos vendrían de la API
        # Aquí usamos datos de ejemplo
        backups = [
            {
                'id': 1,
                'name': 'Respaldo_20250519_120000',
                'backup_type': 'FULL',
                'status': 'COMPLETED',
                'size_in_mb': 25.4,
                'created_at': '2025-05-19 12:00:00',
                'file_exists': True
            },
            {
                'id': 2,
                'name': 'Respaldo_20250518_120000',
                'backup_type': 'DB',
                'status': 'COMPLETED',
                'size_in_mb': 10.2,
                'created_at': '2025-05-18 12:00:00',
                'file_exists': True
            },
            {
                'id': 3,
                'name': 'Respaldo_20250517_120000',
                'backup_type': 'MEDIA',
                'status': 'COMPLETED',
                'size_in_mb': 15.8,
                'created_at': '2025-05-17 12:00:00',
                'file_exists': True
            }
        ]
        
        # Limpiar tabla
        self.table.setRowCount(0)
        
        # Llenar tabla con datos
        for row, backup in enumerate(backups):
            self.table.insertRow(row)
            
            # ID
            id_item = QTableWidgetItem(str(backup.get('id', '')))
            self.table.setItem(row, 0, id_item)
            
            # Nombre
            name_item = QTableWidgetItem(backup.get('name', ''))
            self.table.setItem(row, 1, name_item)
            
            # Tipo
            backup_type = backup.get('backup_type', '')
            backup_type_text = {
                'FULL': 'Completo',
                'DB': 'Base de Datos',
                'MEDIA': 'Archivos de Medios'
            }.get(backup_type, backup_type)
            type_item = QTableWidgetItem(backup_type_text)
            self.table.setItem(row, 2, type_item)
            
            # Estado
            status = backup.get('status', '')
            status_text = {
                'PENDING': 'Pendiente',
                'IN_PROGRESS': 'En Progreso',
                'COMPLETED': 'Completado',
                'FAILED': 'Fallido'
            }.get(status, status)
            status_item = QTableWidgetItem(status_text)
            self.table.setItem(row, 3, status_item)
            
            # Tamaño
            size_item = QTableWidgetItem(str(backup.get('size_in_mb', 0)))
            self.table.setItem(row, 4, size_item)
            
            # Fecha de Creación
            date_item = QTableWidgetItem(backup.get('created_at', ''))
            self.table.setItem(row, 5, date_item)
            
            # Acciones
            actions_widget = QWidget()
            actions_layout = QHBoxLayout(actions_widget)
            actions_layout.setContentsMargins(4, 4, 4, 4)
            
            # Botón de restaurar
            restore_button = QPushButton()
            restore_button.setIcon(self.style().standardIcon(QStyle.SP_BrowserReload))
            restore_button.setToolTip("Restaurar")
            restore_button.clicked.connect(lambda _, id=backup.get('id'): self.restore_backup(id))
            
            # Botón de eliminar
            delete_button = QPushButton()
            delete_button.setIcon(self.style().standardIcon(QStyle.SP_TrashIcon))
            delete_button.setToolTip("Eliminar")
            delete_button.clicked.connect(lambda _, id=backup.get('id'): self.delete_backup(id))
            
            actions_layout.addWidget(restore_button)
            actions_layout.addWidget(delete_button)
            actions_layout.addStretch()
            
            self.table.setCellWidget(row, 6, actions_widget)
        
        # Ajustar tamaño de columnas
        self.table.resizeColumnsToContents()
    
    def create_backup(self):
        """Abre el diálogo para crear un nuevo respaldo"""
        dialog = CreateBackupDialog(self)
        
        if dialog.exec_() == QDialog.Accepted:
            # Obtener datos del formulario
            backup_data = dialog.get_data()
            
            # En una aplicación real, aquí se enviarían los datos a la API
            QMessageBox.information(self, "Información", 
                                   "Se ha iniciado la creación del respaldo. "
                                   "Este proceso puede tardar varios minutos.")
            
            # Actualizar tabla
            self.refresh_data()
    
    def restore_backup(self, backup_id):
        """Abre el diálogo para restaurar un respaldo"""
        # En una aplicación real, aquí se obtendría la información del respaldo de la API
        backup_data = {
            'id': backup_id,
            'name': f'Respaldo_{backup_id}',
            'backup_type': 'Completo',
            'created_at': '2025-05-19 12:00:00',
            'size_in_mb': 25.4
        }
        
        dialog = RestoreBackupDialog(self, backup_data)
        
        if dialog.exec_() == QDialog.Accepted:
            # En una aplicación real, aquí se enviaría la solicitud de restauración a la API
            QMessageBox.information(self, "Información", 
                                   "Se ha iniciado la restauración del respaldo. "
                                   "Este proceso puede tardar varios minutos.")
    
    def delete_backup(self, backup_id):
        """Confirma y elimina un respaldo"""
        reply = QMessageBox.question(
            self, 'Confirmar Eliminación',
            f'¿Está seguro de que desea eliminar el respaldo {backup_id}?',
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            # En una aplicación real, aquí se enviaría la solicitud de eliminación a la API
            QMessageBox.information(self, "Información", 
                                   f"El respaldo {backup_id} ha sido eliminado.")
            
            # Actualizar tabla
            self.refresh_data()

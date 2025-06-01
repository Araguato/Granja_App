#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                            QPushButton, QTableWidget, QTableWidgetItem, 
                            QMessageBox, QComboBox, QSpinBox, QProgressBar,
                            QGroupBox, QFormLayout, QCheckBox, QListWidget,
                            QListWidgetItem, QSplitter, QFrame)
from PyQt5.QtCore import Qt, QDateTime, pyqtSignal
from PyQt5.QtGui import QIcon, QFont, QColor

from sync_manager import SyncManager

class SyncTab(QWidget):
    """Pestaña para gestionar la sincronización con el banco de datos y la app móvil"""
    
    def __init__(self, api_client):
        super().__init__()
        self.api_client = api_client
        self._first_show = True  # Bandera para primera vez que se muestra
        
        # Crear gestor de sincronización
        self.sync_manager = SyncManager(api_client)
        
        # Conectar señales
        self.sync_manager.sync_started.connect(self.on_sync_started)
        self.sync_manager.sync_completed.connect(self.on_sync_completed)
        self.sync_manager.sync_progress.connect(self.on_sync_progress)
        self.sync_manager.data_updated.connect(self.on_data_updated)
        
        self.setup_ui()
    
    def showEvent(self, event):
        """Maneja el evento de mostrar el widget"""
        super().showEvent(event)
        
        # Solo sincronizar la primera vez que se muestra el tab
        if self._first_show and not self.api_client.is_offline:
            self._first_show = False
            # Pequeño retraso para permitir que la interfaz se muestre
            from PyQt5.QtCore import QTimer
            QTimer.singleShot(500, self.on_sync_now_clicked)
        
    def setup_ui(self):
        """Configura la interfaz de usuario"""
        # Layout principal
        main_layout = QVBoxLayout()
        self.setLayout(main_layout)
        
        # Título
        title_label = QLabel("Sincronización con Banco de Datos y App Móvil")
        title_label.setStyleSheet("font-size: 18px; font-weight: bold; margin-bottom: 10px;")
        main_layout.addWidget(title_label)
        
        # Descripción
        desc_label = QLabel("Esta pestaña permite gestionar la sincronización de datos entre la aplicación de Windows, el banco de datos central y la aplicación móvil.")
        desc_label.setWordWrap(True)
        main_layout.addWidget(desc_label)
        
        # Splitter para dividir la pantalla
        splitter = QSplitter(Qt.Horizontal)
        main_layout.addWidget(splitter)
        
        # Panel izquierdo - Estado y controles
        left_panel = QWidget()
        left_layout = QVBoxLayout()
        left_panel.setLayout(left_layout)
        
        # Grupo de estado
        status_group = QGroupBox("Estado de Sincronización")
        status_layout = QVBoxLayout()
        status_group.setLayout(status_layout)
        
        # Última sincronización
        self.last_sync_label = QLabel("Última sincronización: Nunca")
        status_layout.addWidget(self.last_sync_label)
        
        # Estado actual
        self.status_label = QLabel("Estado: Inactivo")
        status_layout.addWidget(self.status_label)
        
        # Barra de progreso
        self.progress_bar = QProgressBar()
        self.progress_bar.setValue(0)
        status_layout.addWidget(self.progress_bar)
        
        # Entidad actual
        self.current_entity_label = QLabel("Entidad actual: Ninguna")
        status_layout.addWidget(self.current_entity_label)
        
        left_layout.addWidget(status_group)
        
        # Grupo de configuración
        config_group = QGroupBox("Configuración de Sincronización")
        config_layout = QFormLayout()
        config_group.setLayout(config_layout)
        
        # Intervalo de sincronización
        self.sync_interval_spin = QSpinBox()
        self.sync_interval_spin.setMinimum(1)
        self.sync_interval_spin.setMaximum(60)
        self.sync_interval_spin.setValue(15)
        self.sync_interval_spin.setSuffix(" minutos")
        self.sync_interval_spin.valueChanged.connect(self.on_sync_interval_changed)
        config_layout.addRow("Intervalo de sincronización:", self.sync_interval_spin)
        
        # Sincronización automática
        self.auto_sync_check = QCheckBox("Habilitar sincronización automática")
        self.auto_sync_check.setChecked(True)
        config_layout.addRow("", self.auto_sync_check)
        
        left_layout.addWidget(config_group)
        
        # Grupo de acciones
        actions_group = QGroupBox("Acciones")
        actions_layout = QVBoxLayout()
        actions_group.setLayout(actions_layout)
        
        # Botón de sincronización manual
        self.sync_now_btn = QPushButton("Sincronizar Ahora")
        self.sync_now_btn.clicked.connect(self.on_sync_now_clicked)
        actions_layout.addWidget(self.sync_now_btn)
        
        # Botón de verificación de conexión
        self.check_connection_btn = QPushButton("Verificar Conexión")
        self.check_connection_btn.clicked.connect(self.on_check_connection_clicked)
        actions_layout.addWidget(self.check_connection_btn)
        
        left_layout.addWidget(actions_group)
        
        # Panel derecho - Datos y cambios pendientes
        right_panel = QWidget()
        right_layout = QVBoxLayout()
        right_panel.setLayout(right_layout)
        
        # Grupo de entidades sincronizadas
        entities_group = QGroupBox("Entidades Sincronizadas")
        entities_layout = QVBoxLayout()
        entities_group.setLayout(entities_layout)
        
        # Lista de entidades
        self.entities_list = QListWidget()
        self.entities_list.addItems([
            "Lotes", "Galpones", "Alimentos", "Vacunas", "Razas", 
            "Seguimientos", "Tareas", "Usuarios", "Empresas", "Granjas"
        ])
        entities_layout.addWidget(self.entities_list)
        
        right_layout.addWidget(entities_group)
        
        # Grupo de cambios pendientes
        pending_group = QGroupBox("Cambios Pendientes")
        pending_layout = QVBoxLayout()
        pending_group.setLayout(pending_layout)
        
        # Tabla de cambios pendientes
        self.pending_table = QTableWidget()
        self.pending_table.setColumnCount(4)
        self.pending_table.setHorizontalHeaderLabels(["Entidad", "Operación", "ID", "Fecha"])
        self.pending_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.pending_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.pending_table.horizontalHeader().setStretchLastSection(True)
        pending_layout.addWidget(self.pending_table)
        
        right_layout.addWidget(pending_group)
        
        # Agregar paneles al splitter
        splitter.addWidget(left_panel)
        splitter.addWidget(right_panel)
        splitter.setSizes([400, 600])
        
        # Cargar datos iniciales
        self.load_pending_changes()
        self.update_last_sync_label()
    
    def on_sync_started(self):
        """Maneja el evento de inicio de sincronización"""
        self.status_label.setText("Estado: Sincronizando...")
        self.progress_bar.setValue(0)
        self.current_entity_label.setText("Entidad actual: Iniciando...")
        self.sync_now_btn.setEnabled(False)
    
    def on_sync_completed(self, success, message):
        """Maneja el evento de finalización de sincronización"""
        if success:
            self.status_label.setText("Estado: Sincronización completada")
            QMessageBox.information(self, "Sincronización Completada", message)
        else:
            self.status_label.setText("Estado: Error de sincronización")
            QMessageBox.warning(self, "Error de Sincronización", message)
        
        self.progress_bar.setValue(100)
        self.current_entity_label.setText("Entidad actual: Ninguna")
        self.sync_now_btn.setEnabled(True)
        
        # Actualizar datos
        self.load_pending_changes()
        self.update_last_sync_label()
    
    def on_sync_progress(self, progress, entity):
        """Maneja el evento de progreso de sincronización"""
        self.progress_bar.setValue(progress)
        self.current_entity_label.setText(f"Entidad actual: {entity}")
    
    def on_data_updated(self, entity):
        """Maneja el evento de actualización de datos"""
        # Resaltar la entidad en la lista
        for i in range(self.entities_list.count()):
            item = self.entities_list.item(i)
            if item.text().lower() == entity.capitalize():
                item.setBackground(QColor(200, 255, 200))
                break
        
        # Actualizar tabla de cambios pendientes
        self.load_pending_changes()
    
    def on_sync_interval_changed(self, value):
        """Maneja el cambio en el intervalo de sincronización"""
        self.sync_manager.set_sync_interval(value)
    
    def on_sync_now_clicked(self):
        """Maneja el clic en el botón de sincronización manual"""
        success, message = self.sync_manager.sync_now()
        if not success:
            QMessageBox.warning(self, "Error", message)
    
    def on_check_connection_clicked(self):
        """Maneja el clic en el botón de verificación de conexión"""
        success, message = self.api_client.test_connection()
        if success:
            QMessageBox.information(self, "Conexión Exitosa", "La conexión con el servidor es correcta.")
        else:
            QMessageBox.warning(self, "Error de Conexión", f"No se pudo conectar con el servidor: {message}")
    
    def load_pending_changes(self):
        """Carga los cambios pendientes en la tabla"""
        # Limpiar tabla
        self.pending_table.setRowCount(0)
        
        # Obtener cambios pendientes
        pending_changes = self.sync_manager.pending_changes
        
        # Llenar tabla
        row = 0
        for entity, changes in pending_changes.items():
            for change in changes:
                self.pending_table.insertRow(row)
                
                # Entidad
                self.pending_table.setItem(row, 0, QTableWidgetItem(entity.capitalize()))
                
                # Operación
                operation = change.get('operation', '')
                operation_text = {
                    'create': 'Crear',
                    'update': 'Actualizar',
                    'delete': 'Eliminar'
                }.get(operation, operation)
                self.pending_table.setItem(row, 1, QTableWidgetItem(operation_text))
                
                # ID
                data = change.get('data', {})
                id_value = data.get('id', 'N/A')
                self.pending_table.setItem(row, 2, QTableWidgetItem(str(id_value)))
                
                # Fecha
                timestamp = change.get('timestamp', '')
                if timestamp:
                    try:
                        dt = QDateTime.fromString(timestamp, Qt.ISODate)
                        formatted_date = dt.toString('yyyy-MM-dd HH:mm:ss')
                    except:
                        formatted_date = timestamp
                else:
                    formatted_date = 'Desconocida'
                self.pending_table.setItem(row, 3, QTableWidgetItem(formatted_date))
                
                row += 1
        
        # Ajustar tamaño de columnas
        self.pending_table.resizeColumnsToContents()
    
    def update_last_sync_label(self):
        """Actualiza la etiqueta de última sincronización"""
        if self.sync_manager.last_sync:
            last_sync = self.sync_manager.last_sync.strftime('%Y-%m-%d %H:%M:%S')
            self.last_sync_label.setText(f"Última sincronización: {last_sync}")
        else:
            self.last_sync_label.setText("Última sincronización: Nunca")

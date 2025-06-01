#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                            QPushButton, QTableWidget, QTableWidgetItem, 
                            QMessageBox, QComboBox, QDateEdit, QLineEdit,
                            QFormLayout, QDialog, QCheckBox, QTextEdit)
from PyQt5.QtCore import Qt, QDate, pyqtSignal
from PyQt5.QtGui import QIcon, QFont

class TareasTab(QWidget):
    """Pestaña para gestionar tareas y asignaciones"""
    
    def __init__(self, api_client):
        super().__init__()
        self.api_client = api_client
        self.setup_ui()
        
    def setup_ui(self):
        """Configura la interfaz de usuario"""
        # Layout principal
        main_layout = QVBoxLayout()
        self.setLayout(main_layout)
        
        # Título
        title_label = QLabel("Gestión de Tareas")
        title_label.setStyleSheet("font-size: 18px; font-weight: bold; margin-bottom: 10px;")
        main_layout.addWidget(title_label)
        
        # Botones de acción
        button_layout = QHBoxLayout()
        
        self.nueva_tarea_btn = QPushButton("Nueva Tarea")
        self.nueva_tarea_btn.clicked.connect(self.mostrar_dialogo_nueva_tarea)
        button_layout.addWidget(self.nueva_tarea_btn)
        
        self.editar_tarea_btn = QPushButton("Editar Tarea")
        self.editar_tarea_btn.clicked.connect(self.editar_tarea_seleccionada)
        button_layout.addWidget(self.editar_tarea_btn)
        
        self.eliminar_tarea_btn = QPushButton("Eliminar Tarea")
        self.eliminar_tarea_btn.clicked.connect(self.eliminar_tarea_seleccionada)
        button_layout.addWidget(self.eliminar_tarea_btn)
        
        self.completar_tarea_btn = QPushButton("Marcar como Completada")
        self.completar_tarea_btn.clicked.connect(self.marcar_tarea_completada)
        button_layout.addWidget(self.completar_tarea_btn)
        
        self.refresh_btn = QPushButton("Actualizar")
        self.refresh_btn.clicked.connect(self.cargar_tareas)
        button_layout.addWidget(self.refresh_btn)
        
        main_layout.addLayout(button_layout)
        
        # Filtros
        filtros_layout = QHBoxLayout()
        
        filtros_layout.addWidget(QLabel("Filtrar por:"))
        
        self.filtro_estado = QComboBox()
        self.filtro_estado.addItems(["Todas", "Pendientes", "Completadas"])
        self.filtro_estado.currentIndexChanged.connect(self.aplicar_filtros)
        filtros_layout.addWidget(self.filtro_estado)
        
        filtros_layout.addWidget(QLabel("Asignado a:"))
        self.filtro_asignado = QComboBox()
        self.filtro_asignado.addItems(["Todos", "Mis Tareas"])
        self.filtro_asignado.currentIndexChanged.connect(self.aplicar_filtros)
        filtros_layout.addWidget(self.filtro_asignado)
        
        filtros_layout.addWidget(QLabel("Fecha:"))
        self.filtro_fecha = QDateEdit()
        self.filtro_fecha.setDate(QDate.currentDate())
        self.filtro_fecha.setCalendarPopup(True)
        self.filtro_fecha.dateChanged.connect(self.aplicar_filtros)
        filtros_layout.addWidget(self.filtro_fecha)
        
        self.filtro_fecha_checkbox = QCheckBox("Filtrar por fecha")
        self.filtro_fecha_checkbox.stateChanged.connect(self.aplicar_filtros)
        filtros_layout.addWidget(self.filtro_fecha_checkbox)
        
        main_layout.addLayout(filtros_layout)
        
        # Tabla de tareas
        self.tabla_tareas = QTableWidget()
        self.tabla_tareas.setColumnCount(6)
        self.tabla_tareas.setHorizontalHeaderLabels(["ID", "Título", "Descripción", "Asignado a", "Fecha Límite", "Estado"])
        self.tabla_tareas.setSelectionBehavior(QTableWidget.SelectRows)
        self.tabla_tareas.setSelectionMode(QTableWidget.SingleSelection)
        self.tabla_tareas.setEditTriggers(QTableWidget.NoEditTriggers)
        self.tabla_tareas.horizontalHeader().setStretchLastSection(True)
        main_layout.addWidget(self.tabla_tareas)
        
        # Cargar datos iniciales
        self.cargar_tareas()
    
    def cargar_tareas(self):
        """Carga las tareas desde la API"""
        # Limpiar tabla
        self.tabla_tareas.setRowCount(0)
        
        # Obtener tareas
        success, tareas = self.api_client.get_tareas()
        
        if success:
            # Llenar tabla con datos
            for i, tarea in enumerate(tareas):
                self.tabla_tareas.insertRow(i)
                self.tabla_tareas.setItem(i, 0, QTableWidgetItem(str(tarea.get('id', ''))))
                self.tabla_tareas.setItem(i, 1, QTableWidgetItem(tarea.get('titulo', '')))
                self.tabla_tareas.setItem(i, 2, QTableWidgetItem(tarea.get('descripcion', '')[:50] + '...'))
                self.tabla_tareas.setItem(i, 3, QTableWidgetItem(tarea.get('asignado_a', '')))
                self.tabla_tareas.setItem(i, 4, QTableWidgetItem(tarea.get('fecha_limite', '')))
                
                estado = "Completada" if tarea.get('completada', False) else "Pendiente"
                estado_item = QTableWidgetItem(estado)
                if estado == "Completada":
                    estado_item.setBackground(Qt.green)
                else:
                    estado_item.setBackground(Qt.yellow)
                self.tabla_tareas.setItem(i, 5, estado_item)
        else:
            # Mostrar mensaje de error
            QMessageBox.warning(self, "Error", "No se pudieron cargar las tareas. Se mostrarán datos de ejemplo.")
            
            # Datos de ejemplo
            tareas_ejemplo = [
                {
                    'id': 1,
                    'titulo': 'Revisar galpón 1',
                    'descripcion': 'Verificar temperatura y humedad del galpón 1',
                    'asignado_a': 'Juan Pérez',
                    'fecha_limite': '2025-05-20',
                    'completada': False
                },
                {
                    'id': 2,
                    'titulo': 'Alimentar aves lote A',
                    'descripcion': 'Suministrar alimento al lote A según la programación',
                    'asignado_a': 'María López',
                    'fecha_limite': '2025-05-19',
                    'completada': True
                },
                {
                    'id': 3,
                    'titulo': 'Vacunación lote B',
                    'descripcion': 'Aplicar vacuna contra Newcastle al lote B',
                    'asignado_a': 'Carlos Rodríguez',
                    'fecha_limite': '2025-05-25',
                    'completada': False
                }
            ]
            
            # Llenar tabla con datos de ejemplo
            for i, tarea in enumerate(tareas_ejemplo):
                self.tabla_tareas.insertRow(i)
                self.tabla_tareas.setItem(i, 0, QTableWidgetItem(str(tarea.get('id', ''))))
                self.tabla_tareas.setItem(i, 1, QTableWidgetItem(tarea.get('titulo', '')))
                self.tabla_tareas.setItem(i, 2, QTableWidgetItem(tarea.get('descripcion', '')))
                self.tabla_tareas.setItem(i, 3, QTableWidgetItem(tarea.get('asignado_a', '')))
                self.tabla_tareas.setItem(i, 4, QTableWidgetItem(tarea.get('fecha_limite', '')))
                
                estado = "Completada" if tarea.get('completada', False) else "Pendiente"
                estado_item = QTableWidgetItem(estado)
                if estado == "Completada":
                    estado_item.setBackground(Qt.green)
                else:
                    estado_item.setBackground(Qt.yellow)
                self.tabla_tareas.setItem(i, 5, estado_item)
        
        # Ajustar tamaño de columnas
        self.tabla_tareas.resizeColumnsToContents()
    
    def aplicar_filtros(self):
        """Aplica los filtros seleccionados a la tabla de tareas"""
        # Obtener valores de filtros
        estado = self.filtro_estado.currentText()
        asignado = self.filtro_asignado.currentText()
        filtrar_por_fecha = self.filtro_fecha_checkbox.isChecked()
        fecha = self.filtro_fecha.date().toString("yyyy-MM-dd") if filtrar_por_fecha else None
        
        # Mostrar/ocultar filas según filtros
        for i in range(self.tabla_tareas.rowCount()):
            mostrar = True
            
            # Filtro de estado
            if estado != "Todas":
                estado_tarea = self.tabla_tareas.item(i, 5).text()
                if (estado == "Pendientes" and estado_tarea != "Pendiente") or \
                   (estado == "Completadas" and estado_tarea != "Completada"):
                    mostrar = False
            
            # Filtro de asignado
            if mostrar and asignado == "Mis Tareas":
                # Obtener usuario actual
                user_info = self.api_client.get_current_user_info()
                if user_info:
                    username = user_info.get('username', '')
                    asignado_tarea = self.tabla_tareas.item(i, 3).text()
                    if username != asignado_tarea:
                        mostrar = False
            
            # Filtro de fecha
            if mostrar and filtrar_por_fecha:
                fecha_tarea = self.tabla_tareas.item(i, 4).text()
                if fecha_tarea != fecha:
                    mostrar = False
            
            # Mostrar/ocultar fila
            self.tabla_tareas.setRowHidden(i, not mostrar)
    
    def mostrar_dialogo_nueva_tarea(self):
        """Muestra el diálogo para crear una nueva tarea"""
        dialogo = DialogoTarea(self.api_client, parent=self)
        if dialogo.exec_() == QDialog.Accepted:
            self.cargar_tareas()
    
    def editar_tarea_seleccionada(self):
        """Edita la tarea seleccionada"""
        # Obtener fila seleccionada
        filas_seleccionadas = self.tabla_tareas.selectedItems()
        if not filas_seleccionadas:
            QMessageBox.warning(self, "Advertencia", "Por favor, seleccione una tarea para editar.")
            return
        
        # Obtener ID de la tarea
        fila = filas_seleccionadas[0].row()
        tarea_id = int(self.tabla_tareas.item(fila, 0).text())
        
        # Obtener datos de la tarea
        tarea = {
            'id': tarea_id,
            'titulo': self.tabla_tareas.item(fila, 1).text(),
            'descripcion': self.tabla_tareas.item(fila, 2).text().replace('...', ''),
            'asignado_a': self.tabla_tareas.item(fila, 3).text(),
            'fecha_limite': self.tabla_tareas.item(fila, 4).text(),
            'completada': self.tabla_tareas.item(fila, 5).text() == "Completada"
        }
        
        # Mostrar diálogo de edición
        dialogo = DialogoTarea(self.api_client, tarea=tarea, parent=self)
        if dialogo.exec_() == QDialog.Accepted:
            self.cargar_tareas()
    
    def eliminar_tarea_seleccionada(self):
        """Elimina la tarea seleccionada"""
        # Obtener fila seleccionada
        filas_seleccionadas = self.tabla_tareas.selectedItems()
        if not filas_seleccionadas:
            QMessageBox.warning(self, "Advertencia", "Por favor, seleccione una tarea para eliminar.")
            return
        
        # Obtener ID de la tarea
        fila = filas_seleccionadas[0].row()
        tarea_id = int(self.tabla_tareas.item(fila, 0).text())
        
        # Confirmar eliminación
        respuesta = QMessageBox.question(
            self, 
            "Confirmar eliminación", 
            "¿Está seguro de que desea eliminar esta tarea?",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if respuesta == QMessageBox.Yes:
            # Eliminar tarea
            success, mensaje = self.api_client.eliminar_tarea(tarea_id)
            
            if success:
                QMessageBox.information(self, "Éxito", "Tarea eliminada correctamente.")
                self.cargar_tareas()
            else:
                QMessageBox.warning(self, "Error", f"No se pudo eliminar la tarea: {mensaje}")
    
    def marcar_tarea_completada(self):
        """Marca la tarea seleccionada como completada"""
        # Obtener fila seleccionada
        filas_seleccionadas = self.tabla_tareas.selectedItems()
        if not filas_seleccionadas:
            QMessageBox.warning(self, "Advertencia", "Por favor, seleccione una tarea para marcar como completada.")
            return
        
        # Obtener ID de la tarea
        fila = filas_seleccionadas[0].row()
        tarea_id = int(self.tabla_tareas.item(fila, 0).text())
        
        # Verificar si ya está completada
        estado_actual = self.tabla_tareas.item(fila, 5).text()
        if estado_actual == "Completada":
            QMessageBox.information(self, "Información", "Esta tarea ya está marcada como completada.")
            return
        
        # Marcar como completada
        success, mensaje = self.api_client.completar_tarea(tarea_id)
        
        if success:
            QMessageBox.information(self, "Éxito", "Tarea marcada como completada.")
            self.cargar_tareas()
        else:
            QMessageBox.warning(self, "Error", f"No se pudo marcar la tarea como completada: {mensaje}")


class DialogoTarea(QDialog):
    """Diálogo para crear o editar una tarea"""
    
    def __init__(self, api_client, tarea=None, parent=None):
        super().__init__(parent)
        self.api_client = api_client
        self.tarea = tarea  # None para nueva tarea, dict para editar
        self.setup_ui()
        
    def setup_ui(self):
        """Configura la interfaz de usuario del diálogo"""
        # Configurar diálogo
        self.setWindowTitle("Nueva Tarea" if not self.tarea else "Editar Tarea")
        self.setMinimumWidth(400)
        
        # Layout principal
        layout = QVBoxLayout()
        self.setLayout(layout)
        
        # Formulario
        form_layout = QFormLayout()
        
        # Campos
        self.titulo_input = QLineEdit()
        if self.tarea:
            self.titulo_input.setText(self.tarea.get('titulo', ''))
        form_layout.addRow("Título:", self.titulo_input)
        
        self.descripcion_input = QTextEdit()
        if self.tarea:
            self.descripcion_input.setText(self.tarea.get('descripcion', ''))
        form_layout.addRow("Descripción:", self.descripcion_input)
        
        self.asignado_input = QComboBox()
        # Cargar usuarios
        success, usuarios = self.api_client.get_usuarios()
        if success:
            for usuario in usuarios:
                self.asignado_input.addItem(usuario.get('username', ''))
        else:
            # Usuarios de ejemplo
            self.asignado_input.addItems(["Juan Pérez", "María López", "Carlos Rodríguez"])
        
        # Seleccionar usuario actual si es nueva tarea
        if not self.tarea:
            user_info = self.api_client.get_current_user_info()
            if user_info:
                username = user_info.get('username', '')
                index = self.asignado_input.findText(username)
                if index >= 0:
                    self.asignado_input.setCurrentIndex(index)
        else:
            # Seleccionar usuario asignado si es edición
            index = self.asignado_input.findText(self.tarea.get('asignado_a', ''))
            if index >= 0:
                self.asignado_input.setCurrentIndex(index)
        
        form_layout.addRow("Asignado a:", self.asignado_input)
        
        self.fecha_input = QDateEdit()
        self.fecha_input.setCalendarPopup(True)
        if self.tarea and self.tarea.get('fecha_limite'):
            try:
                fecha = QDate.fromString(self.tarea.get('fecha_limite'), "yyyy-MM-dd")
                self.fecha_input.setDate(fecha)
            except:
                self.fecha_input.setDate(QDate.currentDate().addDays(7))
        else:
            # Por defecto, una semana desde hoy
            self.fecha_input.setDate(QDate.currentDate().addDays(7))
        form_layout.addRow("Fecha límite:", self.fecha_input)
        
        self.completada_check = QCheckBox("Tarea completada")
        if self.tarea:
            self.completada_check.setChecked(self.tarea.get('completada', False))
        form_layout.addRow("", self.completada_check)
        
        layout.addLayout(form_layout)
        
        # Botones
        button_layout = QHBoxLayout()
        
        self.cancelar_btn = QPushButton("Cancelar")
        self.cancelar_btn.clicked.connect(self.reject)
        button_layout.addWidget(self.cancelar_btn)
        
        self.guardar_btn = QPushButton("Guardar")
        self.guardar_btn.clicked.connect(self.guardar_tarea)
        button_layout.addWidget(self.guardar_btn)
        
        layout.addLayout(button_layout)
    
    def guardar_tarea(self):
        """Guarda la tarea nueva o editada"""
        # Validar campos
        if not self.titulo_input.text().strip():
            QMessageBox.warning(self, "Error", "El título es obligatorio.")
            return
        
        # Recopilar datos
        tarea_data = {
            'titulo': self.titulo_input.text().strip(),
            'descripcion': self.descripcion_input.toPlainText().strip(),
            'asignado_a': self.asignado_input.currentText(),
            'fecha_limite': self.fecha_input.date().toString("yyyy-MM-dd"),
            'completada': self.completada_check.isChecked()
        }
        
        # Guardar tarea
        if self.tarea:  # Editar
            tarea_data['id'] = self.tarea.get('id')
            success, mensaje = self.api_client.actualizar_tarea(tarea_data)
        else:  # Nueva
            success, mensaje = self.api_client.crear_tarea(tarea_data)
        
        if success:
            QMessageBox.information(self, "Éxito", "Tarea guardada correctamente.")
            self.accept()
        else:
            QMessageBox.warning(self, "Error", f"No se pudo guardar la tarea: {mensaje}")

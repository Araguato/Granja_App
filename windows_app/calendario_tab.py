import os
import datetime
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                           QPushButton, QTableWidget, QTableWidgetItem,
                           QDialog, QFormLayout, QLineEdit, QTextEdit,
                           QMessageBox, QComboBox, QCalendarWidget, QTimeEdit,
                           QDateEdit, QSplitter, QHeaderView, QStyle, QFrame, QSizePolicy)
from PyQt5.QtCore import Qt, QSize, QDate, QTime, QDateTime
from PyQt5.QtGui import QFont, QColor, QIcon

class CreateEventoDialog(QDialog):
    """Diálogo para crear un nuevo evento"""
    
    def __init__(self, parent=None, categorias=None):
        super().__init__(parent)
        self.setWindowTitle("Crear Nuevo Evento")
        self.setMinimumWidth(500)
        self.setMinimumHeight(400)
        
        # Crear layout
        layout = QVBoxLayout(self)
        
        # Formulario
        form_layout = QFormLayout()
        
        # Título
        self.titulo_input = QLineEdit()
        form_layout.addRow("Título:", self.titulo_input)
        
        # Fecha
        self.fecha_edit = QDateEdit()
        self.fecha_edit.setCalendarPopup(True)
        self.fecha_edit.setDate(QDate.currentDate())
        form_layout.addRow("Fecha:", self.fecha_edit)
        
        # Hora
        self.hora_edit = QTimeEdit()
        self.hora_edit.setTime(QTime.currentTime())
        form_layout.addRow("Hora:", self.hora_edit)
        
        # Categoría
        self.categoria_combo = QComboBox()
        if categorias:
            for categoria in categorias:
                self.categoria_combo.addItem(categoria.get('nombre', ''), categoria.get('id'))
        form_layout.addRow("Categoría:", self.categoria_combo)
        
        # Tipo
        self.tipo_combo = QComboBox()
        self.tipo_combo.addItems([
            "Vacunación", "Alimentación", "Mantenimiento", "Revisión Veterinaria", 
            "Traslado", "Entrega", "Otro"
        ])
        form_layout.addRow("Tipo:", self.tipo_combo)
        
        # Recordatorio
        self.recordatorio_combo = QComboBox()
        self.recordatorio_combo.addItems([
            "Sin recordatorio", "15 minutos antes", "30 minutos antes", 
            "1 hora antes", "2 horas antes", "1 día antes"
        ])
        form_layout.addRow("Recordatorio:", self.recordatorio_combo)
        
        layout.addLayout(form_layout)
        
        # Descripción
        descripcion_label = QLabel("Descripción:")
        layout.addWidget(descripcion_label)
        
        self.descripcion_input = QTextEdit()
        self.descripcion_input.setMinimumHeight(150)
        layout.addWidget(self.descripcion_input)
        
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
            'titulo': self.titulo_input.text(),
            'fecha': self.fecha_edit.date().toString("yyyy-MM-dd"),
            'hora': self.hora_edit.time().toString("HH:mm"),
            'categoria_id': self.categoria_combo.currentData(),
            'categoria_nombre': self.categoria_combo.currentText(),
            'tipo': self.tipo_combo.currentText(),
            'recordatorio': self.recordatorio_combo.currentText(),
            'descripcion': self.descripcion_input.toPlainText()
        }

class EditEventoDialog(CreateEventoDialog):
    """Diálogo para editar un evento existente"""
    
    def __init__(self, parent=None, categorias=None, evento_data=None):
        super().__init__(parent, categorias)
        self.setWindowTitle("Editar Evento")
        
        # Llenar el formulario con los datos del evento
        if evento_data:
            self.titulo_input.setText(evento_data.get('titulo', ''))
            
            fecha_str = evento_data.get('fecha', '')
            if fecha_str:
                try:
                    fecha = QDate.fromString(fecha_str, "yyyy-MM-dd")
                    self.fecha_edit.setDate(fecha)
                except:
                    pass
            
            hora_str = evento_data.get('hora', '')
            if hora_str:
                try:
                    hora = QTime.fromString(hora_str, "HH:mm")
                    self.hora_edit.setTime(hora)
                except:
                    pass
            
            categoria_id = evento_data.get('categoria_id')
            if categoria_id:
                categoria_index = self.categoria_combo.findData(categoria_id)
                if categoria_index >= 0:
                    self.categoria_combo.setCurrentIndex(categoria_index)
            
            tipo_index = self.tipo_combo.findText(evento_data.get('tipo', ''))
            if tipo_index >= 0:
                self.tipo_combo.setCurrentIndex(tipo_index)
            
            recordatorio_index = self.recordatorio_combo.findText(evento_data.get('recordatorio', ''))
            if recordatorio_index >= 0:
                self.recordatorio_combo.setCurrentIndex(recordatorio_index)
            
            self.descripcion_input.setPlainText(evento_data.get('descripcion', ''))

class EventoWidget(QFrame):
    """Widget para mostrar un evento en el calendario"""
    
    def __init__(self, evento_data, parent=None):
        super().__init__(parent)
        self.evento_data = evento_data
        
        # Configurar estilo según la categoría
        categoria = evento_data.get('categoria_nombre', '').lower()
        color = "#4e73df"  # Color por defecto (azul)
        
        if "vacunación" in categoria or "sanidad" in categoria:
            color = "#e74a3b"  # Rojo
        elif "alimentación" in categoria or "nutrición" in categoria:
            color = "#1cc88a"  # Verde
        elif "producción" in categoria:
            color = "#f6c23e"  # Amarillo
        
        self.setStyleSheet(f"""
            QFrame {{
                background-color: {color};
                color: white;
                border-radius: 4px;
                padding: 4px;
                margin: 2px;
            }}
        """)
        
        # Crear layout
        layout = QVBoxLayout(self)
        layout.setContentsMargins(4, 4, 4, 4)
        layout.setSpacing(2)
        
        # Título
        titulo_label = QLabel(evento_data.get('titulo', ''))
        titulo_label.setStyleSheet("font-weight: bold;")
        layout.addWidget(titulo_label)
        
        # Hora
        hora_label = QLabel(evento_data.get('hora', ''))
        hora_label.setStyleSheet("font-size: 10px;")
        layout.addWidget(hora_label)
        
        # Tipo
        tipo_label = QLabel(evento_data.get('tipo', ''))
        tipo_label.setStyleSheet("font-size: 10px;")
        layout.addWidget(tipo_label)
        
        # Configurar tamaño
        self.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)

class CalendarioTab(QWidget):
    """Pestaña para gestionar el calendario de eventos"""
    
    def __init__(self, api_client):
        super().__init__()
        self.api_client = api_client
        
        # Crear layout principal
        layout = QVBoxLayout(self)
        
        # Título
        title_label = QLabel("Calendario de Eventos")
        title_label.setStyleSheet("font-size: 24px; font-weight: bold; color: #5a5c69;")
        layout.addWidget(title_label)
        
        # Descripción
        desc_label = QLabel("Gestión de eventos y recordatorios")
        desc_label.setStyleSheet("font-size: 14px; color: #858796; margin-bottom: 20px;")
        layout.addWidget(desc_label)
        
        # Botones de acción
        action_layout = QHBoxLayout()
        
        self.new_button = QPushButton("Nuevo Evento")
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
        self.new_button.clicked.connect(self.create_evento)
        
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
        
        # Crear splitter para dividir la vista
        splitter = QSplitter(Qt.Horizontal)
        
        # Calendario
        self.calendar_widget = QCalendarWidget()
        self.calendar_widget.setMinimumWidth(400)
        self.calendar_widget.setGridVisible(True)
        self.calendar_widget.selectionChanged.connect(self.on_date_selected)
        
        # Panel de eventos
        self.eventos_widget = QWidget()
        eventos_layout = QVBoxLayout(self.eventos_widget)
        
        self.fecha_label = QLabel()
        self.fecha_label.setStyleSheet("font-size: 18px; font-weight: bold; color: #5a5c69;")
        eventos_layout.addWidget(self.fecha_label)
        
        # Lista de eventos
        self.eventos_layout = QVBoxLayout()
        eventos_layout.addLayout(self.eventos_layout)
        eventos_layout.addStretch()
        
        # Agregar widgets al splitter
        splitter.addWidget(self.calendar_widget)
        splitter.addWidget(self.eventos_widget)
        
        # Establecer proporciones del splitter
        splitter.setSizes([400, 600])
        
        layout.addWidget(splitter)
        
        # Inicializar variables
        self.eventos = {}  # Diccionario de eventos por fecha
        self.current_date = QDate.currentDate()
        
        # Cargar datos iniciales
        self.refresh_data()
    
    def refresh_data(self):
        """Actualiza los datos del calendario"""
        # En una aplicación real, estos datos vendrían de la API
        # Aquí usamos datos de ejemplo
        eventos = [
            {
                'id': 1,
                'titulo': 'Vacunación Newcastle',
                'fecha': '2025-05-20',
                'hora': '09:00',
                'categoria_id': 2,
                'categoria_nombre': 'Sanidad',
                'tipo': 'Vacunación',
                'recordatorio': '1 hora antes',
                'descripcion': 'Aplicar vacuna Newcastle a lote 3 en galpón 2.'
            },
            {
                'id': 2,
                'titulo': 'Cambio de alimento',
                'fecha': '2025-05-20',
                'hora': '14:30',
                'categoria_id': 1,
                'categoria_nombre': 'Alimentación',
                'tipo': 'Alimentación',
                'recordatorio': '30 minutos antes',
                'descripcion': 'Cambiar a alimento de postura para lote 2.'
            },
            {
                'id': 3,
                'titulo': 'Revisión veterinaria',
                'fecha': '2025-05-21',
                'hora': '10:00',
                'categoria_id': 2,
                'categoria_nombre': 'Sanidad',
                'tipo': 'Revisión Veterinaria',
                'recordatorio': '1 día antes',
                'descripcion': 'Revisión general de salud para todos los lotes.'
            },
            {
                'id': 4,
                'titulo': 'Entrega de huevos',
                'fecha': '2025-05-22',
                'hora': '08:00',
                'categoria_id': 3,
                'categoria_nombre': 'Producción',
                'tipo': 'Entrega',
                'recordatorio': '1 hora antes',
                'descripcion': 'Entrega de 500 cajas de huevos a Supermercados ABC.'
            }
        ]
        
        # Organizar eventos por fecha
        self.eventos = {}
        for evento in eventos:
            fecha = evento.get('fecha', '')
            if fecha not in self.eventos:
                self.eventos[fecha] = []
            self.eventos[fecha].append(evento)
        
        # Actualizar calendario
        self.update_calendar()
        
        # Mostrar eventos para la fecha seleccionada
        self.show_eventos(self.current_date)
    
    def update_calendar(self):
        """Actualiza la visualización del calendario"""
        # Marcar fechas con eventos
        for fecha_str in self.eventos:
            try:
                fecha = QDate.fromString(fecha_str, "yyyy-MM-dd")
                formato = self.calendar_widget.dateTextFormat(fecha)
                formato.setFontWeight(QFont.Bold)
                formato.setBackground(QColor("#4e73df"))
                formato.setForeground(QColor("white"))
                self.calendar_widget.setDateTextFormat(fecha, formato)
            except:
                pass
    
    def on_date_selected(self):
        """Maneja la selección de una fecha en el calendario"""
        self.current_date = self.calendar_widget.selectedDate()
        self.show_eventos(self.current_date)
    
    def show_eventos(self, date):
        """Muestra los eventos para la fecha seleccionada"""
        # Actualizar etiqueta de fecha
        self.fecha_label.setText(date.toString("dddd, d 'de' MMMM 'de' yyyy"))
        
        # Limpiar lista de eventos
        while self.eventos_layout.count():
            item = self.eventos_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        
        # Obtener eventos para la fecha seleccionada
        fecha_str = date.toString("yyyy-MM-dd")
        eventos_del_dia = self.eventos.get(fecha_str, [])
        
        if not eventos_del_dia:
            # Mostrar mensaje de no eventos
            no_eventos_label = QLabel("No hay eventos programados para esta fecha.")
            no_eventos_label.setStyleSheet("color: #858796; font-style: italic;")
            self.eventos_layout.addWidget(no_eventos_label)
            return
        
        # Ordenar eventos por hora
        eventos_del_dia.sort(key=lambda x: x.get('hora', ''))
        
        # Mostrar eventos
        for evento in eventos_del_dia:
            # Crear widget de evento
            evento_widget = EventoWidget(evento)
            
            # Agregar botones de acción
            actions_layout = QHBoxLayout()
            
            edit_button = QPushButton()
            edit_button.setIcon(self.style().standardIcon(QStyle.SP_FileDialogDetailedView))
            edit_button.setToolTip("Editar")
            edit_button.clicked.connect(lambda _, id=evento.get('id'): self.edit_evento(id))
            
            delete_button = QPushButton()
            delete_button.setIcon(self.style().standardIcon(QStyle.SP_TrashIcon))
            delete_button.setToolTip("Eliminar")
            delete_button.clicked.connect(lambda _, id=evento.get('id'): self.delete_evento(id))
            
            actions_layout.addWidget(edit_button)
            actions_layout.addWidget(delete_button)
            actions_layout.addStretch()
            
            # Crear layout para el evento y sus acciones
            event_container = QWidget()
            event_layout = QVBoxLayout(event_container)
            event_layout.setContentsMargins(0, 0, 0, 0)
            event_layout.addWidget(evento_widget)
            event_layout.addLayout(actions_layout)
            
            self.eventos_layout.addWidget(event_container)
    
    def get_categorias(self):
        """Obtiene la lista de categorías"""
        # En una aplicación real, estos datos vendrían de la API
        # Aquí usamos datos de ejemplo
        return [
            {
                'id': 1,
                'nombre': 'Alimentación'
            },
            {
                'id': 2,
                'nombre': 'Sanidad'
            },
            {
                'id': 3,
                'nombre': 'Producción'
            }
        ]
    
    def get_evento_by_id(self, evento_id):
        """Obtiene un evento por su ID"""
        # En una aplicación real, estos datos vendrían de la API
        # Aquí buscamos en el diccionario de eventos
        for fecha, eventos in self.eventos.items():
            for evento in eventos:
                if evento.get('id') == evento_id:
                    return evento
        return None
    
    def create_evento(self):
        """Abre el diálogo para crear un nuevo evento"""
        categorias = self.get_categorias()
        dialog = CreateEventoDialog(self, categorias)
        
        # Establecer fecha seleccionada
        dialog.fecha_edit.setDate(self.current_date)
        
        if dialog.exec_() == QDialog.Accepted:
            # Obtener datos del formulario
            evento_data = dialog.get_data()
            
            # En una aplicación real, aquí se enviarían los datos a la API
            QMessageBox.information(self, "Información", 
                                   f"Evento '{evento_data['titulo']}' creado correctamente.")
            
            # Actualizar calendario
            self.refresh_data()
    
    def edit_evento(self, evento_id):
        """Edita un evento existente"""
        evento_data = self.get_evento_by_id(evento_id)
        if not evento_data:
            QMessageBox.warning(self, "Advertencia", "No se encontró el evento seleccionado.")
            return
        
        categorias = self.get_categorias()
        dialog = EditEventoDialog(self, categorias, evento_data)
        
        if dialog.exec_() == QDialog.Accepted:
            # Obtener datos del formulario
            updated_data = dialog.get_data()
            
            # En una aplicación real, aquí se enviarían los datos a la API
            QMessageBox.information(self, "Información", 
                                   f"Evento '{updated_data['titulo']}' actualizado correctamente.")
            
            # Actualizar calendario
            self.refresh_data()
    
    def delete_evento(self, evento_id):
        """Elimina un evento existente"""
        evento_data = self.get_evento_by_id(evento_id)
        if not evento_data:
            QMessageBox.warning(self, "Advertencia", "No se encontró el evento seleccionado.")
            return
        
        reply = QMessageBox.question(
            self, 'Confirmar Eliminación',
            f'¿Está seguro de que desea eliminar el evento "{evento_data.get("titulo")}"?',
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            # En una aplicación real, aquí se enviaría la solicitud de eliminación a la API
            QMessageBox.information(self, "Información", 
                                   f"Evento eliminado correctamente.")
            
            # Actualizar calendario
            self.refresh_data()

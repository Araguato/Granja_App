from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                            QPushButton, QTableWidget, QTableWidgetItem,
                            QDialog, QFormLayout, QLineEdit, QDateEdit,
                            QSpinBox, QComboBox, QMessageBox, QTabWidget,
                            QDoubleSpinBox, QDialogButtonBox)
from PyQt5.QtCore import Qt, QDate
from datetime import datetime

class LoteDialog(QDialog):
    """Diálogo para crear o editar un lote"""
    
    def __init__(self, parent=None, lote_data=None, api_client=None):
        super().__init__(parent)
        self.setWindowTitle("Lote" if lote_data else "Nuevo Lote")
        self.setMinimumWidth(500)
        self.setMinimumHeight(600)
        self.api_client = api_client
        self.lote_data = lote_data
        
        # Crear layout
        layout = QVBoxLayout(self)
        
        # Crear pestañas para organizar la información
        self.tabs = QTabWidget()
        
        # Pestaña de información general
        general_tab = QWidget()
        general_layout = QVBoxLayout(general_tab)
        
        # Formulario de información general
        form_layout = QFormLayout()
        
        # Campos del formulario
        self.nombre_input = QLineEdit()
        form_layout.addRow("Nombre:", self.nombre_input)
        
        self.fecha_ingreso = QDateEdit()
        self.fecha_ingreso.setCalendarPopup(True)
        self.fecha_ingreso.setDate(QDate.currentDate())
        form_layout.addRow("Fecha de Ingreso:", self.fecha_ingreso)
        
        self.cantidad_input = QSpinBox()
        self.cantidad_input.setRange(1, 100000)
        self.cantidad_input.setValue(100)
        form_layout.addRow("Cantidad de Aves:", self.cantidad_input)
        
        # Obtener razas y galpones desde la API
        self.raza_combo = QComboBox()
        self.galpon_combo = QComboBox()
        
        # Cargar razas y galpones
        self.cargar_razas_y_galpones()
        
        form_layout.addRow("Raza:", self.raza_combo)
        form_layout.addRow("Galpón:", self.galpon_combo)
        
        self.edad_input = QSpinBox()
        self.edad_input.setRange(0, 1000)
        self.edad_input.setSuffix(" días")
        form_layout.addRow("Edad:", self.edad_input)
        
        self.peso_promedio = QDoubleSpinBox()
        self.peso_promedio.setRange(0, 10000)
        self.peso_promedio.setSuffix(" g")
        self.peso_promedio.setDecimals(2)
        form_layout.addRow("Peso Promedio:", self.peso_promedio)
        
        general_layout.addLayout(form_layout)
        
        # Pestaña de seguimiento
        seguimiento_tab = QWidget()
        seguimiento_layout = QVBoxLayout(seguimiento_tab)
        
        # Formulario de seguimiento
        seguimiento_form = QFormLayout()
        
        self.mortalidad_diaria = QSpinBox()
        self.mortalidad_diaria.setRange(0, 1000)
        seguimiento_form.addRow("Mortalidad Diaria:", self.mortalidad_diaria)
        
        self.mortalidad_acumulada = QSpinBox()
        self.mortalidad_acumulada.setRange(0, 100000)
        seguimiento_form.addRow("Mortalidad Acumulada:", self.mortalidad_acumulada)
        
        self.produccion_huevos = QSpinBox()
        self.produccion_huevos.setRange(0, 100000)
        seguimiento_form.addRow("Producción de Huevos (diaria):", self.produccion_huevos)
        
        self.produccion_acumulada = QSpinBox()
        self.produccion_acumulada.setRange(0, 1000000)
        seguimiento_form.addRow("Producción Acumulada:", self.produccion_acumulada)
        
        self.fecha_ultimo_seguimiento = QDateEdit()
        self.fecha_ultimo_seguimiento.setCalendarPopup(True)
        self.fecha_ultimo_seguimiento.setDate(QDate.currentDate())
        seguimiento_form.addRow("Fecha Último Seguimiento:", self.fecha_ultimo_seguimiento)
        
        seguimiento_layout.addLayout(seguimiento_form)
        
        # Pestaña de alimentación
        alimentacion_tab = QWidget()
        alimentacion_layout = QVBoxLayout(alimentacion_tab)
        
        # Formulario de alimentación
        alimentacion_form = QFormLayout()
        
        self.alimento_combo = QComboBox()
        self.alimento_combo.addItems(["Balanceado", "Maíz", "Trigo", "Mixto"])
        alimentacion_form.addRow("Tipo de Alimento:", self.alimento_combo)
        
        self.consumo_diario = QDoubleSpinBox()
        self.consumo_diario.setRange(0, 10000)
        self.consumo_diario.setSuffix(" kg")
        self.consumo_diario.setDecimals(2)
        alimentacion_form.addRow("Consumo Diario:", self.consumo_diario)
        
        self.consumo_acumulado = QDoubleSpinBox()
        self.consumo_acumulado.setRange(0, 1000000)
        self.consumo_acumulado.setSuffix(" kg")
        self.consumo_acumulado.setDecimals(2)
        alimentacion_form.addRow("Consumo Acumulado:", self.consumo_acumulado)
        
        self.conversion_alimenticia = QDoubleSpinBox()
        self.conversion_alimenticia.setRange(0, 10)
        self.conversion_alimenticia.setDecimals(2)
        alimentacion_form.addRow("Conversión Alimenticia:", self.conversion_alimenticia)
        
        alimentacion_layout.addLayout(alimentacion_form)
        
        # Pestaña de consumos
        consumos_tab = QWidget()
        consumos_layout = QVBoxLayout(consumos_tab)
        
        # Formulario de consumo de agua
        agua_form = QFormLayout()
        agua_form.addRow(QLabel("<b>Consumo de Agua</b>"))
        
        self.consumo_agua = QDoubleSpinBox()
        self.consumo_agua.setRange(0, 100000)
        self.consumo_agua.setSuffix(" L")
        self.consumo_agua.setDecimals(2)
        agua_form.addRow("Consumo Diario:", self.consumo_agua)
        
        consumos_layout.addLayout(agua_form)
        
        # Formulario de consumo de energía
        energia_form = QFormLayout()
        energia_form.addRow(QLabel("<b>Consumo de Energía</b>"))
        
        self.consumo_energia = QDoubleSpinBox()
        self.consumo_energia.setRange(0, 100000)
        self.consumo_energia.setSuffix(" kWh")
        self.consumo_energia.setDecimals(2)
        energia_form.addRow("Consumo Energético (diario):", self.consumo_energia)
        
        consumos_layout.addLayout(energia_form)
        
        # Agregar pestañas al tab widget
        self.tabs.addTab(general_tab, "General")
        self.tabs.addTab(seguimiento_tab, "Seguimiento")
        self.tabs.addTab(alimentacion_tab, "Alimentación")
        self.tabs.addTab(consumos_tab, "Consumos")
        
        layout.addWidget(self.tabs)
        
        # Botones de aceptar y cancelar
        buttons = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel,
            Qt.Horizontal, self)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)
        
        # Si hay datos, cargarlos
        if lote_data:
            self.cargar_datos_lote()
    
    def cargar_razas_y_galpones(self):
        """Carga las razas y galpones desde la API"""
        # Limpiar combos
        self.raza_combo.clear()
        self.galpon_combo.clear()
        
        # Si no hay cliente API, usar datos de ejemplo
        if not self.api_client:
            self.raza_combo.addItems(["Broiler", "Ponedora", "Reproductora", "Isa Brown", "Ross 308", "Leghorn Blanca"])
            self.galpon_combo.addItems(["Galpón 1", "Galpón 2", "Galpón 3"])
            return
        
        # Cargar razas desde la API
        success, razas = self.api_client.get_razas() if hasattr(self.api_client, 'get_razas') else (True, [])
        if success and razas:
            # Guardar los datos completos para cada raza
            self.razas_data = razas
            # Agregar nombres al combo
            for raza in razas:
                self.raza_combo.addItem(raza.get('nombre', ''), raza.get('id'))
        else:
            # Datos de ejemplo
            self.razas_data = [
                {'id': 1, 'nombre': 'Broiler'},
                {'id': 2, 'nombre': 'Ponedora'},
                {'id': 3, 'nombre': 'Reproductora'},
                {'id': 4, 'nombre': 'Isa Brown'},
                {'id': 5, 'nombre': 'Ross 308'},
                {'id': 6, 'nombre': 'Leghorn Blanca'}
            ]
            for raza in self.razas_data:
                self.raza_combo.addItem(raza['nombre'], raza['id'])
        
        # Cargar galpones desde la API
        success, galpones = self.api_client.get_galpones()
        if success and galpones:
            # Guardar los datos completos para cada galpón
            self.galpones_data = galpones
            # Agregar nombres al combo
            for galpon in galpones:
                self.galpon_combo.addItem(galpon.get('nombre', ''), galpon.get('id'))
        else:
            # Datos de ejemplo
            self.galpones_data = [
                {'id': 1, 'nombre': 'Galpón 1'},
                {'id': 2, 'nombre': 'Galpón 2'},
                {'id': 3, 'nombre': 'Galpón 3'}
            ]
            for galpon in self.galpones_data:
                self.galpon_combo.addItem(galpon['nombre'], galpon['id'])
    
    def cargar_datos_lote(self):
        """Carga los datos del lote en el formulario"""
        if not self.lote_data:
            return
            
        # Cargar datos básicos
        self.nombre_input.setText(self.lote_data.get('nombre', ''))
        
        # Fecha de ingreso
        fecha_str = self.lote_data.get('fecha_ingreso', '')
        if fecha_str:
            try:
                fecha = QDate.fromString(fecha_str, "yyyy-MM-dd")
                if fecha.isValid():
                    self.fecha_ingreso.setDate(fecha)
            except:
                pass
        
        # Cantidad
        self.cantidad_input.setValue(self.lote_data.get('cantidad_inicial', 100))
        
        # Raza
        raza = self.lote_data.get('raza', {})
        if isinstance(raza, dict) and 'id' in raza:
            index = self.raza_combo.findData(raza['id'])
            if index >= 0:
                self.raza_combo.setCurrentIndex(index)
        
        # Galpón
        galpon = self.lote_data.get('galpon', {})
        if isinstance(galpon, dict) and 'id' in galpon:
            index = self.galpon_combo.findData(galpon['id'])
            if index >= 0:
                self.galpon_combo.setCurrentIndex(index)
        
        # Edad
        self.edad_input.setValue(self.lote_data.get('edad', 0))
        
        # Peso promedio
        self.peso_promedio.setValue(self.lote_data.get('peso_promedio', 0))
        
        # Mortalidad
        self.mortalidad_diaria.setValue(self.lote_data.get('mortalidad_diaria', 0))
        self.mortalidad_acumulada.setValue(self.lote_data.get('mortalidad_acumulada', 0))
        
        # Producción
        self.produccion_huevos.setValue(self.lote_data.get('produccion_huevos', 0))
        self.produccion_acumulada.setValue(self.lote_data.get('produccion_acumulada', 0))
        
        # Fecha último seguimiento
        fecha_seg_str = self.lote_data.get('fecha_ultimo_seguimiento', '')
        if fecha_seg_str:
            try:
                fecha_seg = QDate.fromString(fecha_seg_str, "yyyy-MM-dd")
                if fecha_seg.isValid():
                    self.fecha_ultimo_seguimiento.setDate(fecha_seg)
            except:
                pass
        
        # Alimentación
        self.consumo_diario.setValue(self.lote_data.get('consumo_alimento', 0))
        tipo_alimento = self.lote_data.get('tipo_alimento', '')
        if tipo_alimento:
            index = self.alimento_combo.findText(tipo_alimento)
            if index >= 0:
                self.alimento_combo.setCurrentIndex(index)
        
        # Consumos
        self.consumo_agua.setValue(self.lote_data.get('consumo_agua', 0))
        self.consumo_energia.setValue(self.lote_data.get('consumo_energia', 0))
    
    def get_data(self):
        """Obtiene los datos del formulario"""
        # Obtener ID de raza y galpón seleccionados
        raza_id = self.raza_combo.currentData()
        galpon_id = self.galpon_combo.currentData()
        
        # Si no hay IDs (datos de ejemplo), usar diccionarios con nombre
        if raza_id is None:
            raza = {'nombre': self.raza_combo.currentText(), 'id': self.raza_combo.currentIndex() + 1}
        else:
            raza = {'id': raza_id, 'nombre': self.raza_combo.currentText()}
            
        if galpon_id is None:
            galpon = {'nombre': self.galpon_combo.currentText(), 'id': self.galpon_combo.currentIndex() + 1}
        else:
            galpon = {'id': galpon_id, 'nombre': self.galpon_combo.currentText()}
        
        # Construir diccionario de datos
        data = {
            'nombre': self.nombre_input.text(),
            'fecha_ingreso': self.fecha_ingreso.date().toString("yyyy-MM-dd"),
            'cantidad_inicial': self.cantidad_input.value(),
            'cantidad_actual': self.cantidad_input.value() - self.mortalidad_acumulada.value(),
            'raza': raza,
            'galpon': galpon,
            'edad': self.edad_input.value(),
            'peso_promedio': self.peso_promedio.value(),
            'mortalidad_diaria': self.mortalidad_diaria.value(),
            'mortalidad_acumulada': self.mortalidad_acumulada.value(),
            'produccion_huevos': self.produccion_huevos.value(),
            'produccion_acumulada': self.produccion_acumulada.value(),
            'fecha_ultimo_seguimiento': self.fecha_ultimo_seguimiento.date().toString("yyyy-MM-dd"),
            'consumo_alimento': self.consumo_diario.value(),
            'tipo_alimento': self.alimento_combo.currentText(),
            'consumo_agua': self.consumo_agua.value(),
            'consumo_energia': self.consumo_energia.value()
        }
        
        # Si estamos editando, incluir el ID
        if self.lote_data and 'id' in self.lote_data:
            data['id'] = self.lote_data['id']
            
        return data


class LotesTab(QWidget):
    """Pestaña para gestionar lotes"""
    
    def __init__(self, api_client):
        super().__init__()
        self.api_client = api_client
        
        # Crear layout principal
        layout = QVBoxLayout(self)
        
        # Título
        title_label = QLabel("<h2>Gestión de Lotes</h2>")
        layout.addWidget(title_label)
        
        # Botones de acción
        button_layout = QHBoxLayout()
        
        self.refresh_button = QPushButton("Actualizar")
        self.refresh_button.clicked.connect(self.refresh_data)
        button_layout.addWidget(self.refresh_button)
        
        self.create_button = QPushButton("Nuevo Lote")
        self.create_button.clicked.connect(self.create_lote)
        button_layout.addWidget(self.create_button)
        
        self.edit_button = QPushButton("Editar")
        self.edit_button.clicked.connect(self.edit_lote)
        button_layout.addWidget(self.edit_button)
        
        self.delete_button = QPushButton("Eliminar")
        # self.delete_button.clicked.connect(self.delete_lote)
        button_layout.addWidget(self.delete_button)
        
        layout.addLayout(button_layout)
        
        # Tabla de lotes
        self.table = QTableWidget()
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels(["ID", "Nombre", "Fecha Ingreso", "Cantidad Inicial", "Cantidad Actual", "Raza", "Galpón"])
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setSelectionMode(QTableWidget.SingleSelection)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.setAlternatingRowColors(True)
        
        layout.addWidget(self.table)
        
        # Cargar datos
        self.refresh_data()
    
    def refresh_data(self):
        """Actualiza los datos de la tabla de lotes"""
        # Limpiar tabla
        self.table.setRowCount(0)
        
        # Obtener lotes desde la API
        success, lotes = self.api_client.get_lotes()
        
        if success and lotes:
            # Llenar tabla con datos
            for row, lote in enumerate(lotes):
                self.table.insertRow(row)
                
                # ID
                id_item = QTableWidgetItem(str(lote.get('id', '')))
                self.table.setItem(row, 0, id_item)
                
                # Nombre
                nombre_item = QTableWidgetItem(lote.get('nombre', ''))
                self.table.setItem(row, 1, nombre_item)
                
                # Fecha Ingreso
                fecha_item = QTableWidgetItem(lote.get('fecha_ingreso', ''))
                self.table.setItem(row, 2, fecha_item)
                
                # Cantidad Inicial
                cantidad_inicial_item = QTableWidgetItem(str(lote.get('cantidad_inicial', 0)))
                self.table.setItem(row, 3, cantidad_inicial_item)
                
                # Cantidad Actual
                cantidad_actual_item = QTableWidgetItem(str(lote.get('cantidad_actual', 0)))
                self.table.setItem(row, 4, cantidad_actual_item)
                
                # Raza
                raza = lote.get('raza', {})
                raza_nombre = raza.get('nombre', '') if isinstance(raza, dict) else ''
                raza_item = QTableWidgetItem(raza_nombre)
                self.table.setItem(row, 5, raza_item)
                
                # Galpón
                galpon = lote.get('galpon', {})
                galpon_nombre = galpon.get('nombre', '') if isinstance(galpon, dict) else ''
                galpon_item = QTableWidgetItem(galpon_nombre)
                self.table.setItem(row, 6, galpon_item)
            
            # Ajustar tamaño de columnas
            self.table.resizeColumnsToContents()
        else:
            # Si hay un error, mostrar mensaje
            QMessageBox.warning(self, "Modo sin conexión", 
                               "No se pudo conectar al servidor Django.\n\n"
                               "La aplicación mostrará datos de ejemplo.\n\n"
                               "Para ver datos reales, asegúrese de que el servidor Django esté en funcionamiento.")
            
            # Agregar fila de ejemplo para mostrar la estructura
            self.table.insertRow(0)
            self.table.setItem(0, 0, QTableWidgetItem("--"))
            self.table.setItem(0, 1, QTableWidgetItem("Ejemplo"))
            self.table.setItem(0, 2, QTableWidgetItem(datetime.now().strftime("%Y-%m-%d")))
            self.table.setItem(0, 3, QTableWidgetItem("100"))
            self.table.setItem(0, 4, QTableWidgetItem("95"))
            self.table.setItem(0, 5, QTableWidgetItem("Broiler"))
            self.table.setItem(0, 6, QTableWidgetItem("Galpón 1"))
            self.table.resizeColumnsToContents()
    
    def create_lote(self):
        """Abre el diálogo para crear un nuevo lote"""
        dialog = LoteDialog(self, api_client=self.api_client)
        
        if dialog.exec_() == QDialog.Accepted:
            # Obtener datos del formulario
            lote_data = dialog.get_data()
            
            # Crear lote en la API
            success, response = self.api_client.create_lote(lote_data)
            
            if success:
                QMessageBox.information(self, "Éxito", "Lote creado correctamente")
            else:
                QMessageBox.warning(self, "Error", f"Error al crear lote: {response}")
            
            # Actualizar tabla
            self.refresh_data()
    
    def edit_lote(self):
        """Abre el diálogo para editar un lote existente"""
        # Obtener fila seleccionada
        selected_row = self.table.currentRow()
        
        if selected_row >= 0:
            # Obtener ID del lote
            lote_id = self.table.item(selected_row, 0).text()
            
            # Obtener datos del lote
            success, lote_data = self.api_client.get_lote(lote_id)
            
            if success:
                # Abrir diálogo con datos del lote
                dialog = LoteDialog(self, lote_data, api_client=self.api_client)
                
                if dialog.exec_() == QDialog.Accepted:
                    # Obtener datos actualizados
                    updated_data = dialog.get_data()
                    
                    # Actualizar lote en la API
                    success, response = self.api_client.update_lote(lote_id, updated_data)
                    
                    if success:
                        QMessageBox.information(self, "Éxito", "Lote actualizado correctamente")
                    else:
                        QMessageBox.warning(self, "Error", f"Error al actualizar lote: {response}")
                    
                    # Actualizar tabla
                    self.refresh_data()
            else:
                QMessageBox.warning(self, "Error", f"Error al obtener lote: {lote_data}")
        else:
            QMessageBox.warning(self, "Advertencia", "Seleccione un lote para editar")

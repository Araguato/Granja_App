from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                            QPushButton, QTableWidget, QTableWidgetItem,
                            QDialog, QFormLayout, QLineEdit, QDateEdit,
                            QSpinBox, QDoubleSpinBox, QComboBox, QMessageBox,
                            QTabWidget, QCalendarWidget, QGroupBox, QStyle)
from PyQt5.QtCore import Qt, QDate
from PyQt5.QtGui import QPainter
from PyQt5.QtChart import QChart, QChartView, QLineSeries, QDateTimeAxis, QValueAxis
from datetime import datetime, timedelta

class SeguimientoDialog(QDialog):
    """Diálogo para registrar seguimiento diario de un lote"""
    
    def __init__(self, parent=None, lote_data=None, seguimiento_data=None):
        super().__init__(parent)
        self.setWindowTitle("Registro de Seguimiento")
        self.setMinimumWidth(500)
        
        # Datos del lote
        self.lote_data = lote_data
        
        # Crear layout
        layout = QVBoxLayout(self)
        
        # Información del lote
        if lote_data:
            lote_info = QGroupBox("Información del Lote")
            lote_layout = QFormLayout(lote_info)
            
            lote_nombre = QLabel(str(lote_data.get('nombre', 'Sin nombre')))
            lote_layout.addRow("Lote:", lote_nombre)
            
            # Manejar galpon que podría ser un diccionario o un string
            galpon = lote_data.get('galpon', {})
            galpon_nombre = galpon.get('nombre', '') if isinstance(galpon, dict) else str(galpon)
            lote_galpon = QLabel(galpon_nombre)
            lote_layout.addRow("Galpón:", lote_galpon)
            
            # Manejar raza que podría ser un diccionario o un string
            raza = lote_data.get('raza', {})
            raza_nombre = raza.get('nombre', '') if isinstance(raza, dict) else str(raza)
            lote_raza = QLabel(raza_nombre)
            lote_layout.addRow("Raza:", lote_raza)
            
            layout.addWidget(lote_info)
        
        # Formulario de seguimiento
        form_layout = QFormLayout()
        
        # Fecha
        self.fecha_input = QDateEdit()
        self.fecha_input.setCalendarPopup(True)
        self.fecha_input.setDate(QDate.currentDate())
        form_layout.addRow("Fecha:", self.fecha_input)
        
        # Mortalidad
        self.mortalidad_input = QSpinBox()
        self.mortalidad_input.setRange(0, 10000)
        form_layout.addRow("Mortalidad (aves):", self.mortalidad_input)
        
        # Producción de huevos
        self.produccion_input = QSpinBox()
        self.produccion_input.setRange(0, 100000)
        form_layout.addRow("Producción (huevos):", self.produccion_input)
        
        # Peso promedio
        self.peso_input = QDoubleSpinBox()
        self.peso_input.setRange(0, 10000)
        self.peso_input.setSuffix(" g")
        self.peso_input.setDecimals(2)
        form_layout.addRow("Peso promedio:", self.peso_input)
        
        # Consumo de alimento
        self.consumo_input = QDoubleSpinBox()
        self.consumo_input.setRange(0, 10000)
        self.consumo_input.setSuffix(" kg")
        self.consumo_input.setDecimals(2)
        form_layout.addRow("Consumo de alimento:", self.consumo_input)
        
        # Consumo de agua
        self.agua_input = QDoubleSpinBox()
        self.agua_input.setRange(0, 10000)
        self.agua_input.setSuffix(" L")
        self.agua_input.setDecimals(2)
        form_layout.addRow("Consumo de agua:", self.agua_input)
        
        # Temperatura
        self.temperatura_input = QDoubleSpinBox()
        self.temperatura_input.setRange(0, 50)
        self.temperatura_input.setSuffix(" °C")
        self.temperatura_input.setDecimals(1)
        self.temperatura_input.setValue(25.0)
        form_layout.addRow("Temperatura:", self.temperatura_input)
        
        # Humedad
        self.humedad_input = QDoubleSpinBox()
        self.humedad_input.setRange(0, 100)
        self.humedad_input.setSuffix(" %")
        self.humedad_input.setDecimals(1)
        self.humedad_input.setValue(60.0)
        form_layout.addRow("Humedad:", self.humedad_input)
        
        # Observaciones
        self.observaciones_input = QLineEdit()
        form_layout.addRow("Observaciones:", self.observaciones_input)
        
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
        
        # Si hay datos de seguimiento, cargarlos
        if seguimiento_data:
            self.fecha_input.setDate(QDate.fromString(seguimiento_data.get('fecha', ''), "yyyy-MM-dd"))
            self.mortalidad_input.setValue(seguimiento_data.get('mortalidad', 0))
            self.produccion_input.setValue(seguimiento_data.get('produccion', 0))
            self.peso_input.setValue(seguimiento_data.get('peso_promedio', 0))
            self.consumo_input.setValue(seguimiento_data.get('consumo_alimento', 0))
            self.agua_input.setValue(seguimiento_data.get('consumo_agua', 0))
            self.temperatura_input.setValue(seguimiento_data.get('temperatura', 25.0))
            self.humedad_input.setValue(seguimiento_data.get('humedad', 60.0))
            self.observaciones_input.setText(seguimiento_data.get('observaciones', ''))
    
    def get_data(self):
        """Obtiene los datos del formulario"""
        return {
            'fecha': self.fecha_input.date().toString("yyyy-MM-dd"),
            'mortalidad': self.mortalidad_input.value(),
            'produccion': self.produccion_input.value(),
            'peso_promedio': self.peso_input.value(),
            'consumo_alimento': self.consumo_input.value(),
            'consumo_agua': self.agua_input.value(),
            'temperatura': self.temperatura_input.value(),
            'humedad': self.humedad_input.value(),
            'observaciones': self.observaciones_input.text()
        }

class SeguimientoTab(QWidget):
    """Pestaña para gestionar el seguimiento diario de lotes"""
    
    def __init__(self, api_client):
        super().__init__()
        self.api_client = api_client
        
        # Crear layout principal
        layout = QVBoxLayout(self)
        
        # Crear pestañas
        self.tabs = QTabWidget()
        
        # Pestaña de registro diario
        self.registro_tab = self.create_registro_tab()
        self.tabs.addTab(self.registro_tab, "Registro Diario")
        
        # Pestaña de histórico
        self.historico_tab = self.create_historico_tab()
        self.tabs.addTab(self.historico_tab, "Histórico")
        
        # Pestaña de gráficos
        self.graficos_tab = self.create_graficos_tab()
        self.tabs.addTab(self.graficos_tab, "Gráficos")
        
        layout.addWidget(self.tabs)
        
        # Cargar datos
        self.refresh_data()
    
    def create_registro_tab(self):
        """Crea la pestaña de registro diario"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        # Selector de lote
        lote_layout = QHBoxLayout()
        lote_layout.addWidget(QLabel("Lote:"))
        self.lote_combo = QComboBox()
        self.lote_combo.currentIndexChanged.connect(self.on_lote_changed)
        lote_layout.addWidget(self.lote_combo)
        
        # Botón de nuevo registro
        self.nuevo_button = QPushButton("Nuevo Registro")
        self.nuevo_button.clicked.connect(self.create_seguimiento)
        lote_layout.addWidget(self.nuevo_button)
        
        layout.addLayout(lote_layout)
        
        # Tabla de registros
        self.table = QTableWidget()
        self.table.setColumnCount(9)
        self.table.setHorizontalHeaderLabels(["Fecha", "Mortalidad", "Producción", "Peso", "Alimento", "Agua", "Temp", "Humedad", "Observaciones"])
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.setAlternatingRowColors(True)
        
        layout.addWidget(self.table)
        
        return tab
    
    def create_historico_tab(self):
        """Crea la pestaña de histórico"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        # Filtros
        filtros_layout = QHBoxLayout()
        
        # Selector de lote
        filtros_layout.addWidget(QLabel("Lote:"))
        self.historico_lote_combo = QComboBox()
        filtros_layout.addWidget(self.historico_lote_combo)
        
        # Selector de fecha inicio
        filtros_layout.addWidget(QLabel("Desde:"))
        self.fecha_inicio = QDateEdit()
        self.fecha_inicio.setCalendarPopup(True)
        self.fecha_inicio.setDate(QDate.currentDate().addDays(-30))
        filtros_layout.addWidget(self.fecha_inicio)
        
        # Selector de fecha fin
        filtros_layout.addWidget(QLabel("Hasta:"))
        self.fecha_fin = QDateEdit()
        self.fecha_fin.setCalendarPopup(True)
        self.fecha_fin.setDate(QDate.currentDate())
        filtros_layout.addWidget(self.fecha_fin)
        
        # Botón de filtrar
        self.filtrar_button = QPushButton("Filtrar")
        self.filtrar_button.clicked.connect(self.filter_historico)
        filtros_layout.addWidget(self.filtrar_button)
        
        layout.addLayout(filtros_layout)
        
        # Tabla de histórico
        self.historico_table = QTableWidget()
        self.historico_table.setColumnCount(9)
        self.historico_table.setHorizontalHeaderLabels(["Fecha", "Mortalidad", "Producción", "Peso", "Alimento", "Agua", "Temp", "Humedad", "Observaciones"])
        self.historico_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.historico_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.historico_table.setAlternatingRowColors(True)
        
        layout.addWidget(self.historico_table)
        
        return tab
    
    def create_graficos_tab(self):
        """Crea la pestaña de gráficos"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        # Filtros
        filtros_layout = QHBoxLayout()
        
        # Selector de lote
        filtros_layout.addWidget(QLabel("Lote:"))
        self.grafico_lote_combo = QComboBox()
        filtros_layout.addWidget(self.grafico_lote_combo)
        
        # Selector de tipo de gráfico
        filtros_layout.addWidget(QLabel("Tipo:"))
        self.grafico_tipo_combo = QComboBox()
        self.grafico_tipo_combo.addItems(["Mortalidad y Producción", "Peso Promedio", "Consumo de Alimento", "Temperatura y Humedad"])
        filtros_layout.addWidget(self.grafico_tipo_combo)
        
        # Botón de actualizar
        self.actualizar_button = QPushButton("Actualizar")
        self.actualizar_button.clicked.connect(self.update_grafico)
        filtros_layout.addWidget(self.actualizar_button)
        
        layout.addLayout(filtros_layout)
        
        # Gráfico
        self.chart_view = QChartView()
        self.chart_view.setRenderHint(QPainter.Antialiasing)
        
        layout.addWidget(self.chart_view)
        
        return tab
    
    def refresh_data(self):
        """Actualiza los datos de las tablas y gráficos"""
        try:
            # Obtener lista de lotes
            success, lotes = self.api_client.get_lotes()
            
            if success:
                # Verificar si lotes es una lista
                if not isinstance(lotes, list):
                    print(f"Error: datos de lotes con formato inesperado: {type(lotes)}")
                    lotes = self.api_client.get_example_data('lotes')
                
                # Actualizar combobox de lotes
                self.lote_combo.clear()
                self.historico_lote_combo.clear()
                self.grafico_lote_combo.clear()
                
                for lote in lotes:
                    # Verificar que lote sea un diccionario
                    if not isinstance(lote, dict):
                        print(f"Error: lote con formato inesperado: {type(lote)}")
                        continue
                        
                    lote_nombre = str(lote.get('nombre', ''))
                    lote_id = str(lote.get('id', ''))
                    item_text = f"{lote_nombre} (ID: {lote_id})"
                    
                    self.lote_combo.addItem(item_text, lote_id)
                    self.historico_lote_combo.addItem(item_text, lote_id)
                    self.grafico_lote_combo.addItem(item_text, lote_id)
                
                # Actualizar tabla de registros si hay lotes
                if self.lote_combo.count() > 0:
                    self.on_lote_changed()
            else:
                # Si hay un error, mostrar mensaje
                print("No se pudo conectar al servidor Django. Mostrando datos de ejemplo.")
                
                # Agregar lotes de ejemplo
                self.lote_combo.clear()
                self.historico_lote_combo.clear()
                self.grafico_lote_combo.clear()
                
                ejemplos = [
                    {"id": 1, "nombre": "Lote A-001"},
                    {"id": 2, "nombre": "Lote B-002"},
                    {"id": 3, "nombre": "Lote C-003"}
                ]
                
                for lote in ejemplos:
                    lote_nombre = lote.get('nombre', '')
                    lote_id = lote.get('id', '')
                    item_text = f"{lote_nombre} (ID: {lote_id})"
                    
                    self.lote_combo.addItem(item_text, lote_id)
                    self.historico_lote_combo.addItem(item_text, lote_id)
                    self.grafico_lote_combo.addItem(item_text, lote_id)
                
                # Mostrar datos de ejemplo en la tabla
                self.mostrar_datos_ejemplo()
        except Exception as e:
            print(f"Error en refresh_data: {str(e)}")
            # En caso de error, mostrar datos de ejemplo
            self.mostrar_datos_ejemplo()
    
    def on_lote_changed(self):
        """Actualiza la tabla de registros cuando cambia el lote seleccionado"""
        try:
            # Obtener ID del lote seleccionado
            lote_id = self.lote_combo.currentData()
            
            if lote_id:
                # Obtener seguimientos del lote
                success, seguimientos = self.api_client.get_seguimientos(lote_id)
                
                if success:
                    # Verificar si seguimientos es una lista
                    if not isinstance(seguimientos, list):
                        print(f"Error: datos de seguimientos con formato inesperado: {type(seguimientos)}")
                        seguimientos = []
                    
                    # Limpiar tabla
                    self.table.setRowCount(0)
                    
                    # Llenar tabla con datos
                    for row, seguimiento in enumerate(seguimientos):
                        # Verificar que seguimiento sea un diccionario
                        if not isinstance(seguimiento, dict):
                            print(f"Error: seguimiento con formato inesperado: {type(seguimiento)}")
                            continue
                            
                        self.table.insertRow(row)
                        
                        # Fecha
                        fecha_item = QTableWidgetItem(str(seguimiento.get('fecha', '')))
                        self.table.setItem(row, 0, fecha_item)
                        
                        # Mortalidad
                        mortalidad_item = QTableWidgetItem(str(seguimiento.get('mortalidad', 0)))
                        self.table.setItem(row, 1, mortalidad_item)
                        
                        # Producción
                        produccion_item = QTableWidgetItem(str(seguimiento.get('produccion', 0)))
                        self.table.setItem(row, 2, produccion_item)
                        
                        # Peso promedio
                        peso_item = QTableWidgetItem(str(seguimiento.get('peso_promedio', 0)))
                        self.table.setItem(row, 3, peso_item)
                        
                        # Consumo alimento
                        consumo_item = QTableWidgetItem(str(seguimiento.get('consumo_alimento', 0)))
                        self.table.setItem(row, 4, consumo_item)
                        
                        # Consumo agua
                        agua_item = QTableWidgetItem(str(seguimiento.get('consumo_agua', 0)))
                        self.table.setItem(row, 5, agua_item)
                        
                        # Temperatura
                        temp_item = QTableWidgetItem(str(seguimiento.get('temperatura', 0)))
                        self.table.setItem(row, 6, temp_item)
                        
                        # Humedad
                        humedad_item = QTableWidgetItem(str(seguimiento.get('humedad', 0)))
                        self.table.setItem(row, 7, humedad_item)
                        
                        # Observaciones
                        obs_item = QTableWidgetItem(str(seguimiento.get('observaciones', '')))
                        self.table.setItem(row, 8, obs_item)
                    
                    # Ajustar tamaño de columnas
                    self.table.resizeColumnsToContents()
                else:
                    # Si hay un error, mostrar mensaje
                    print(f"Error al obtener seguimientos: {seguimientos}")
                    self.mostrar_datos_ejemplo()
        except Exception as e:
            print(f"Error en on_lote_changed: {str(e)}")
            # En caso de error, mostrar datos de ejemplo
            self.mostrar_datos_ejemplo()
    
    def mostrar_datos_ejemplo(self):
        """Muestra datos de ejemplo en la tabla"""
        # Limpiar tabla
        self.table.setRowCount(0)
        
        # Crear datos de ejemplo
        ejemplos = []
        fecha_actual = datetime.now()
        
        for i in range(5):
            fecha = fecha_actual - timedelta(days=i)
            ejemplos.append({
                'fecha': fecha.strftime('%Y-%m-%d'),
                'mortalidad': i,
                'produccion': 850 - i * 5,
                'peso_promedio': 1850.5 - i * 10,
                'consumo_alimento': 45.2 - i * 0.2,
                'consumo_agua': 90.5 - i * 0.5,
                'temperatura': 25.3 + i * 0.1,
                'humedad': 62.5 - i * 0.3,
                'observaciones': 'Datos de ejemplo'
            })
        
        # Agregar filas a la tabla
        for row, seguimiento in enumerate(ejemplos):
            self.table.insertRow(row)
            
            # Fecha
            self.table.setItem(row, 0, QTableWidgetItem(seguimiento['fecha']))
            
            # Mortalidad
            self.table.setItem(row, 1, QTableWidgetItem(str(seguimiento['mortalidad'])))
            
            # Producción
            self.table.setItem(row, 2, QTableWidgetItem(str(seguimiento['produccion'])))
            
            # Peso Promedio
            self.table.setItem(row, 3, QTableWidgetItem(str(seguimiento['peso_promedio'])))
            
            # Consumo Alimento
            self.table.setItem(row, 4, QTableWidgetItem(str(seguimiento['consumo_alimento'])))
            
            # Consumo Agua
            self.table.setItem(row, 5, QTableWidgetItem(str(seguimiento['consumo_agua'])))
            
            # Temperatura
            self.table.setItem(row, 6, QTableWidgetItem(str(seguimiento['temperatura'])))
            
            # Humedad
            self.table.setItem(row, 7, QTableWidgetItem(str(seguimiento['humedad'])))
            
            # Observaciones
            self.table.setItem(row, 8, QTableWidgetItem(seguimiento['observaciones']))
        
        # Ajustar tamaño de columnas
        self.table.resizeColumnsToContents()
    
    def filter_historico(self):
        """Filtra los datos históricos según los criterios seleccionados"""
        # Esta función se implementará más adelante
        pass
    
    def update_grafico(self):
        """Actualiza el gráfico según los criterios seleccionados"""
        try:
            # Obtener ID del lote seleccionado
            lote_id = self.grafico_lote_combo.currentData()
            
            if lote_id:
                # Obtener seguimientos del lote
                success, seguimientos = self.api_client.get_seguimientos(lote_id)
                
                if success and seguimientos and isinstance(seguimientos, list):
                    # Crear series según el tipo de gráfico seleccionado
                    tipo_grafico = self.grafico_tipo_combo.currentText()
                    
                    if tipo_grafico == "Mortalidad y Producción":
                        # Crear series para mortalidad y producción
                        series_mortalidad = QLineSeries()
                        series_mortalidad.setName("Mortalidad")
                        
                        series_produccion = QLineSeries()
                        series_produccion.setName("Producción")
                        
                        # Agregar puntos a las series
                        for seguimiento in sorted(seguimientos, key=lambda x: x.get('fecha', '')):
                            fecha_str = seguimiento.get('fecha', '')
                            mortalidad = seguimiento.get('mortalidad', 0)
                            produccion = seguimiento.get('produccion', 0)
                            
                            try:
                                # Convertir fecha a timestamp
                                fecha = QDate.fromString(fecha_str, "yyyy-MM-dd")
                                timestamp = fecha.startOfDay().toMSecsSinceEpoch()
                                
                                # Agregar puntos
                                series_mortalidad.append(timestamp, mortalidad)
                                series_produccion.append(timestamp, produccion)
                            except ValueError:
                                print(f"Error al convertir fecha: {fecha_str}")
                        
                        # Verificar que haya puntos en las series
                        if series_mortalidad.count() > 0 and series_produccion.count() > 0:
                            # Crear chart
                            chart = QChart()
                            chart.addSeries(series_mortalidad)
                            chart.addSeries(series_produccion)
                            chart.setTitle("Mortalidad y Producción")
                            
                            # Crear ejes
                            axis_x = QDateTimeAxis()
                            axis_x.setFormat("dd/MM/yyyy")
                            axis_x.setTitleText("Fecha")
                            chart.addAxis(axis_x, Qt.AlignBottom)
                            series_mortalidad.attachAxis(axis_x)
                            series_produccion.attachAxis(axis_x)
                            
                            axis_y = QValueAxis()
                            axis_y.setTitleText("Cantidad")
                            chart.addAxis(axis_y, Qt.AlignLeft)
                            series_mortalidad.attachAxis(axis_y)
                            series_produccion.attachAxis(axis_y)
                            
                            # Ajustar chart
                            chart.legend().setVisible(True)
                            chart.legend().setAlignment(Qt.AlignBottom)
                            
                            # Mostrar chart
                            self.chart_view.setChart(chart)
                        else:
                            # No hay suficientes puntos para graficar
                            chart = QChart()
                            chart.setTitle("No hay suficientes datos para mostrar el gráfico")
                            self.chart_view.setChart(chart)
                    else:
                        # Otros tipos de gráficos se implementarán más adelante
                        chart = QChart()
                        chart.setTitle(f"Gráfico de {tipo_grafico} en desarrollo")
                        self.chart_view.setChart(chart)
                else:
                    # Si no hay datos, mostrar mensaje
                    chart = QChart()
                    chart.setTitle("No hay datos disponibles")
                    self.chart_view.setChart(chart)
            else:
                # Si no hay lote seleccionado, mostrar mensaje
                chart = QChart()
                chart.setTitle("Seleccione un lote para ver gráficos")
                self.chart_view.setChart(chart)
        except Exception as e:
            print(f"Error en update_grafico: {str(e)}")
            # En caso de error, mostrar un gráfico vacío
            chart = QChart()
            chart.setTitle(f"Error al cargar el gráfico: {str(e)}")
            self.chart_view.setChart(chart)
    
    def create_seguimiento(self):
        """Abre el diálogo para crear un nuevo registro de seguimiento"""
        if self.lote_combo.count() == 0:
            QMessageBox.warning(self, "Advertencia", "No hay lotes disponibles para registrar seguimiento")
            return
        
        lote_id = self.lote_combo.currentData()
        
        # Obtener datos del lote
        success, lote_data = self.api_client.get_lote(lote_id)
        
        if success:
            # Abrir diálogo
            dialog = SeguimientoDialog(self, lote_data)
            
            if dialog.exec_() == QDialog.Accepted:
                # Obtener datos del formulario
                seguimiento_data = dialog.get_data()
                
                # Guardar seguimiento en la API
                success, result = self.api_client.create_seguimiento(lote_id, seguimiento_data)
                
                if success:
                    QMessageBox.information(self, "Información", "Seguimiento registrado correctamente")
                else:
                    QMessageBox.warning(self, "Error", f"Error al registrar seguimiento: {result}")
                
                # Actualizar tabla
                self.refresh_data()
                
                # Actualizar gráfico
                self.update_grafico()
        else:
            QMessageBox.warning(self, "Error", f"Error al obtener lote: {lote_data}")

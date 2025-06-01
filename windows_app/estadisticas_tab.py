import os
import datetime
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                            QPushButton, QComboBox, QGroupBox, QFormLayout,
                            QMessageBox, QFrame, QScrollArea, QTabWidget)
from PyQt5.QtCore import Qt, QDateTime
from PyQt5.QtGui import QPainter, QColor, QPen, QBrush
from PyQt5.QtChart import QChart, QChartView, QLineSeries, QBarSeries, QBarSet, QBarCategoryAxis, QValueAxis, QPieSeries

class ChartWidget(QWidget):
    """Widget para mostrar gráficos"""
    
    def __init__(self, title=""):
        super().__init__()
        
        # Crear layout
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Título
        if title:
            title_label = QLabel(title)
            title_label.setStyleSheet("font-size: 16px; font-weight: bold; color: #5a5c69;")
            layout.addWidget(title_label)
        
        # Crear gráfico
        self.chart = QChart()
        self.chart.setAnimationOptions(QChart.SeriesAnimations)
        self.chart.setBackgroundBrush(QBrush(QColor("#ffffff")))
        self.chart.legend().setVisible(True)
        
        # Vista del gráfico
        self.chart_view = QChartView(self.chart)
        self.chart_view.setRenderHint(QPainter.Antialiasing)
        
        layout.addWidget(self.chart_view)

class LineChartWidget(ChartWidget):
    """Widget para mostrar gráficos de líneas"""
    
    def __init__(self, title=""):
        super().__init__(title)
    
    def set_data(self, data, x_title="", y_title=""):
        """Establece los datos del gráfico de líneas"""
        try:
            # Limpiar gráfico
            self.chart.removeAllSeries()
            
            # Verificar si hay datos
            if not data or not isinstance(data, dict) or not any(data.values()):
                # No hay datos, mostrar mensaje
                self.chart.setTitle("No hay datos disponibles")
                return
            
            # Crear ejes
            axis_x = QBarCategoryAxis()
            axis_y = QValueAxis()
            
            # Establecer títulos de ejes
            if x_title:
                axis_x.setTitleText(x_title)
            if y_title:
                axis_y.setTitleText(y_title)
            
            # Agregar series
            categories = []
            max_value = 0
            
            for series_name, series_data in data.items():
                if not series_data or not isinstance(series_data, list):
                    continue
                    
                line_series = QLineSeries()
                line_series.setName(series_name)
                
                for i, point in enumerate(series_data):
                    try:
                        if isinstance(point, tuple) and len(point) >= 2:
                            label, value = point[0], point[1]
                        elif isinstance(point, dict) and 'label' in point and 'value' in point:
                            label, value = point['label'], point['value']
                        else:
                            continue
                            
                        if not isinstance(value, (int, float)):
                            try:
                                value = float(value)
                            except (ValueError, TypeError):
                                continue
                                
                        line_series.append(i, value)
                        if label not in categories:
                            categories.append(str(label))
                        if value > max_value:
                            max_value = value
                    except Exception as e:
                        print(f"Error al procesar punto de datos: {e}")
                        continue
                
                if line_series.count() > 0:  # Solo agregar series con puntos
                    self.chart.addSeries(line_series)
                
            # Verificar si se agregaron series
            if not self.chart.series().count() or not categories:
                self.chart.setTitle("No hay datos disponibles")
                return
            
            # Configurar ejes
            axis_x.append(categories)
            self.chart.addAxis(axis_x, Qt.AlignBottom)
            self.chart.addAxis(axis_y, Qt.AlignLeft)
            
            # Conectar series a ejes
            for i in range(self.chart.series().count()):
                series = self.chart.series()[i]
                series.attachAxis(axis_x)
                series.attachAxis(axis_y)
            
            # Ajustar rango del eje Y
            if max_value > 0:
                axis_y.setRange(0, max_value * 1.1)  # 10% más alto que el valor máximo
            else:
                axis_y.setRange(0, 10)  # Valor predeterminado si no hay datos
        except Exception as e:
            print(f"Error al configurar gráfico de líneas: {e}")
            self.chart.setTitle("Error al cargar datos")

class BarChartWidget(ChartWidget):
    """Widget para mostrar gráficos de barras"""
    
    def __init__(self, title=""):
        super().__init__(title)
    
    def set_data(self, data, x_title="", y_title=""):
        """Establece los datos del gráfico de barras"""
        try:
            # Limpiar gráfico
            self.chart.removeAllSeries()
            
            # Verificar si hay datos
            if not data or not isinstance(data, dict) or not any(data.values()):
                # No hay datos, mostrar mensaje
                self.chart.setTitle("No hay datos disponibles")
                return
            
            # Crear ejes
            axis_x = QBarCategoryAxis()
            axis_y = QValueAxis()
            
            # Establecer títulos de ejes
            if x_title:
                axis_x.setTitleText(x_title)
            if y_title:
                axis_y.setTitleText(y_title)
            
            # Crear series de barras
            bar_series = QBarSeries()
            
            # Agregar conjuntos de barras
            categories = []
            max_value = 0
            
            for series_name, series_data in data.items():
                if not series_data or not isinstance(series_data, list):
                    continue
                    
                bar_set = QBarSet(series_name)
                
                for point in series_data:
                    try:
                        if isinstance(point, tuple) and len(point) >= 2:
                            label, value = point[0], point[1]
                        elif isinstance(point, dict) and 'label' in point and 'value' in point:
                            label, value = point['label'], point['value']
                        else:
                            continue
                            
                        if not isinstance(value, (int, float)):
                            try:
                                value = float(value)
                            except (ValueError, TypeError):
                                continue
                                
                        bar_set.append(value)
                        if label not in categories:
                            categories.append(str(label))
                        if value > max_value:
                            max_value = value
                    except Exception as e:
                        print(f"Error al procesar punto de datos: {e}")
                        continue
                
                if bar_set.count() > 0:  # Solo agregar conjuntos con datos
                    bar_series.append(bar_set)
            
            # Verificar si se agregaron datos
            if bar_series.count() == 0 or not categories:
                self.chart.setTitle("No hay datos disponibles")
                return
            
            # Agregar series al gráfico
            self.chart.addSeries(bar_series)
            
            # Configurar ejes
            axis_x.append(categories)
            self.chart.addAxis(axis_x, Qt.AlignBottom)
            self.chart.addAxis(axis_y, Qt.AlignLeft)
            
            # Conectar series a ejes
            bar_series.attachAxis(axis_x)
            bar_series.attachAxis(axis_y)
            
            # Ajustar rango del eje Y
            if max_value > 0:
                axis_y.setRange(0, max_value * 1.1)  # 10% más alto que el valor máximo
            else:
                axis_y.setRange(0, 10)  # Valor predeterminado si no hay datos
        except Exception as e:
            print(f"Error al configurar gráfico de barras: {e}")
            self.chart.setTitle("Error al cargar datos")

class PieChartWidget(ChartWidget):
    """Widget para mostrar gráficos circulares"""
    
    def __init__(self, title=""):
        super().__init__(title)
    
    def set_data(self, data):
        """Establece los datos del gráfico circular"""
        try:
            # Limpiar gráfico
            self.chart.removeAllSeries()
            
            # Verificar si hay datos
            if not data or not isinstance(data, list) or len(data) == 0:
                # No hay datos, mostrar mensaje
                self.chart.setTitle("No hay datos disponibles")
                return
            
            # Crear serie
            pie_series = QPieSeries()
            
            # Procesar datos
            valid_data = []
            for point in data:
                try:
                    if isinstance(point, tuple) and len(point) >= 2:
                        label, value = point[0], point[1]
                    elif isinstance(point, dict) and 'label' in point and 'value' in point:
                        label, value = point['label'], point['value']
                    else:
                        continue
                        
                    if not isinstance(value, (int, float)):
                        try:
                            value = float(value)
                        except (ValueError, TypeError):
                            continue
                    
                    if value > 0:  # Solo incluir valores positivos
                        valid_data.append((str(label), value))
                except Exception as e:
                    print(f"Error al procesar punto de datos: {e}")
                    continue
            
            # Verificar si hay datos válidos
            if not valid_data:
                self.chart.setTitle("No hay datos disponibles")
                return
            
            # Agregar datos
            total = sum(value for _, value in valid_data)
            
            for label, value in valid_data:
                # Calcular porcentaje
                percentage = (value / total) * 100 if total > 0 else 0
                slice_label = f"{label}: {percentage:.1f}%"
                
                # Agregar slice
                slice = pie_series.append(slice_label, value)
                
                # Destacar slice
                slice.setExploded(True)
                slice.setLabelVisible(True)
            
            # Agregar serie al gráfico
            self.chart.addSeries(pie_series)
        except Exception as e:
            print(f"Error al configurar gráfico circular: {e}")
            self.chart.setTitle("Error al cargar datos")

class StatCard(QFrame):
    """Tarjeta para mostrar estadísticas"""
    
    def __init__(self, title, value, icon=None, color="#4e73df"):
        super().__init__()
        
        # Establecer estilo
        self.setStyleSheet(f"""
            QFrame {{
                background-color: white;
                border-left: 4px solid {color};
                border-radius: 4px;
                padding: 10px;
            }}
        """)
        
        # Crear layout
        layout = QHBoxLayout(self)
        
        # Información
        info_layout = QVBoxLayout()
        
        # Título
        self.title_label = QLabel(title)
        self.title_label.setStyleSheet("color: #5a5c69; font-weight: bold; font-size: 12px;")
        info_layout.addWidget(self.title_label)
        
        # Valor
        self.value_label = QLabel(value)
        self.value_label.setStyleSheet("color: #5a5c69; font-weight: bold; font-size: 20px;")
        info_layout.addWidget(self.value_label)
        
        layout.addLayout(info_layout)
        
        # Icono (si se proporciona)
        if icon:
            self.icon_label = QLabel()
            self.icon_label.setPixmap(icon.pixmap(32, 32))
            layout.addWidget(self.icon_label)

class EstadisticasTab(QWidget):
    """Pestaña para visualizar estadísticas"""
    
    def __init__(self, api_client):
        super().__init__()
        self.api_client = api_client
        
        # Crear layout principal
        main_layout = QVBoxLayout(self)
        
        # Título
        title_label = QLabel("Estadísticas de Producción")
        title_label.setStyleSheet("font-size: 24px; font-weight: bold; color: #5a5c69;")
        main_layout.addWidget(title_label)
        
        # Descripción
        desc_label = QLabel("Visualización de datos de producción y rendimiento")
        desc_label.setStyleSheet("font-size: 14px; color: #858796; margin-bottom: 20px;")
        main_layout.addWidget(desc_label)
        
        # Controles de filtro
        filter_layout = QHBoxLayout()
        
        # Filtro de galpón
        galpon_layout = QHBoxLayout()
        galpon_label = QLabel("Galpón:")
        self.galpon_combo = QComboBox()
        self.galpon_combo.setMinimumWidth(150)
        self.galpon_combo.currentIndexChanged.connect(self.cargar_lotes_por_galpon)
        
        galpon_layout.addWidget(galpon_label)
        galpon_layout.addWidget(self.galpon_combo)
        
        # Filtro de lote
        lote_layout = QHBoxLayout()
        lote_label = QLabel("Lote:")
        self.lote_combo = QComboBox()
        self.lote_combo.setMinimumWidth(150)
        
        lote_layout.addWidget(lote_label)
        lote_layout.addWidget(self.lote_combo)
        
        # Selector de período
        period_layout = QHBoxLayout()
        period_label = QLabel("Período:")
        self.period_combo = QComboBox()
        self.period_combo.addItems(["Última Semana", "Último Mes", "Último Año"])
        self.period_combo.currentIndexChanged.connect(self.refresh_data)
        
        period_layout.addWidget(period_label)
        period_layout.addWidget(self.period_combo)
        
        # Agregar todos los filtros al layout principal
        filter_layout.addLayout(galpon_layout)
        filter_layout.addLayout(lote_layout)
        filter_layout.addLayout(period_layout)
        
        # Botón de actualizar
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
        
        filter_layout.addLayout(period_layout)
        filter_layout.addStretch()
        filter_layout.addWidget(self.refresh_button)
        
        main_layout.addLayout(filter_layout)
        
        # Crear área de desplazamiento
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setFrameShape(QFrame.NoFrame)
        
        # Contenido desplazable
        scroll_content = QWidget()
        scroll_layout = QVBoxLayout(scroll_content)
        
        # Tarjetas de resumen
        cards_layout = QHBoxLayout()
        cards_layout.setSpacing(20)
        
        # Tarjeta de total de aves
        self.total_aves_card = StatCard("Total de Aves", "0", color="#4e73df")
        cards_layout.addWidget(self.total_aves_card)
        
        # Tarjeta de producción
        self.produccion_card = StatCard("Producción Diaria", "0", color="#1cc88a")
        cards_layout.addWidget(self.produccion_card)
        
        # Tarjeta de mortalidad
        self.mortalidad_card = StatCard("Mortalidad Diaria", "0", color="#e74a3b")
        cards_layout.addWidget(self.mortalidad_card)
        
        # Tarjeta de ventas
        self.ventas_card = StatCard("Ventas Diarias", "$0", color="#f6c23e")
        cards_layout.addWidget(self.ventas_card)
        
        scroll_layout.addLayout(cards_layout)
        
        # Filtros para comparación de razas
        filtros_group = QGroupBox("Filtros de Comparación")
        filtros_layout = QHBoxLayout(filtros_group)
        
        # Selector de razas
        razas_layout = QFormLayout()
        self.raza1_combo = QComboBox()
        self.raza2_combo = QComboBox()
        razas_layout.addRow("Raza 1:", self.raza1_combo)
        razas_layout.addRow("Raza 2:", self.raza2_combo)
        filtros_layout.addLayout(razas_layout)
        
        # Selector de período
        periodo_layout = QFormLayout()
        self.periodo_combo = QComboBox()
        self.periodo_combo.addItems(["Última semana", "Último mes", "Últimos 3 meses", "Último año"])
        periodo_layout.addRow("Período:", self.periodo_combo)
        filtros_layout.addLayout(periodo_layout)
        
        # Botón de actualizar
        self.actualizar_btn = QPushButton("Actualizar Comparación")
        self.actualizar_btn.clicked.connect(self.actualizar_comparacion_razas)
        filtros_layout.addWidget(self.actualizar_btn)
        
        scroll_layout.addWidget(filtros_group)
        
        # Gráficos de comparación de razas
        comparacion_group = QGroupBox("Comparación de Razas")
        comparacion_layout = QVBoxLayout(comparacion_group)
        
        # Tabs para diferentes métricas
        self.metricas_tabs = QTabWidget()
        
        # Tab de producción
        self.produccion_comp_tab = QWidget()
        produccion_comp_layout = QVBoxLayout(self.produccion_comp_tab)
        self.produccion_comp_chart = LineChartWidget()
        produccion_comp_layout.addWidget(self.produccion_comp_chart)
        self.metricas_tabs.addTab(self.produccion_comp_tab, "Producción")
        
        # Tab de peso
        self.peso_comp_tab = QWidget()
        peso_comp_layout = QVBoxLayout(self.peso_comp_tab)
        self.peso_comp_chart = LineChartWidget()
        peso_comp_layout.addWidget(self.peso_comp_chart)
        self.metricas_tabs.addTab(self.peso_comp_tab, "Peso Promedio")
        
        # Tab de mortalidad
        self.mortalidad_comp_tab = QWidget()
        mortalidad_comp_layout = QVBoxLayout(self.mortalidad_comp_tab)
        self.mortalidad_comp_chart = LineChartWidget()
        mortalidad_comp_layout.addWidget(self.mortalidad_comp_chart)
        self.metricas_tabs.addTab(self.mortalidad_comp_tab, "Mortalidad")
        
        # Tab de consumo
        self.consumo_comp_tab = QWidget()
        consumo_comp_layout = QVBoxLayout(self.consumo_comp_tab)
        self.consumo_comp_chart = LineChartWidget()
        consumo_comp_layout.addWidget(self.consumo_comp_chart)
        self.metricas_tabs.addTab(self.consumo_comp_tab, "Consumo Alimento")
        
        comparacion_layout.addWidget(self.metricas_tabs)
        scroll_layout.addWidget(comparacion_group)
        
        # Gráficos
        # Gráfico de producción
        produccion_group = QGroupBox("Producción de Huevos")
        produccion_layout = QVBoxLayout(produccion_group)
        self.produccion_chart = LineChartWidget()
        produccion_layout.addWidget(self.produccion_chart)
        scroll_layout.addWidget(produccion_group)
        
        # Gráfico de mortalidad
        mortalidad_group = QGroupBox("Mortalidad")
        mortalidad_layout = QVBoxLayout(mortalidad_group)
        self.mortalidad_chart = LineChartWidget()
        mortalidad_layout.addWidget(self.mortalidad_chart)
        scroll_layout.addWidget(mortalidad_group)
        
        # Gráfico de ventas
        ventas_group = QGroupBox("Ventas")
        ventas_layout = QVBoxLayout(ventas_group)
        self.ventas_chart = LineChartWidget()
        ventas_layout.addWidget(self.ventas_chart)
        scroll_layout.addWidget(ventas_group)
        
        # Gráficos de distribución
        distribucion_row = QHBoxLayout()
        
        # Distribución de tipos de huevo
        distribucion_group = QGroupBox("Distribución de Tipos de Huevo")
        distribucion_layout = QVBoxLayout(distribucion_group)
        self.distribucion_chart = PieChartWidget()
        distribucion_layout.addWidget(self.distribucion_chart)
        distribucion_row.addWidget(distribucion_group)
        
        # Inventario de alimentos
        inventario_group = QGroupBox("Inventario de Alimentos")
        inventario_layout = QVBoxLayout(inventario_group)
        self.inventario_chart = BarChartWidget()
        inventario_layout.addWidget(self.inventario_chart)
        distribucion_row.addWidget(inventario_group)
        
        scroll_layout.addLayout(distribucion_row)
        
        scroll_area.setWidget(scroll_content)
        main_layout.addWidget(scroll_area)
        
        # Cargar datos iniciales
        self.refresh_data()
    
    def actualizar_comparacion_razas(self):
        """Actualiza los gráficos de comparación de razas"""
        try:
            # Obtener razas seleccionadas
            raza1 = self.raza1_combo.currentText()
            raza2 = self.raza2_combo.currentText()
            periodo = self.periodo_combo.currentText()
            
            if not raza1 or not raza2 or raza1 == raza2:
                QMessageBox.warning(self, "Advertencia", "Por favor seleccione dos razas diferentes para comparar.")
                return
            
            # Obtener datos de la API para la comparación
            # En una implementación real, estos datos vendrían de la API
            # Por ahora, usaremos datos de ejemplo
            
            # Datos de producción por raza
            produccion_data = {
                raza1: [
                    ("Semana 1", 85),
                    ("Semana 2", 88),
                    ("Semana 3", 92),
                    ("Semana 4", 95),
                    ("Semana 5", 94),
                    ("Semana 6", 96),
                    ("Semana 7", 97),
                    ("Semana 8", 96)
                ],
                raza2: [
                    ("Semana 1", 80),
                    ("Semana 2", 82),
                    ("Semana 3", 85),
                    ("Semana 4", 88),
                    ("Semana 5", 90),
                    ("Semana 6", 91),
                    ("Semana 7", 92),
                    ("Semana 8", 91)
                ]
            }
            self.produccion_comp_chart.set_data(produccion_data, "Semana", "Producción (%)")
            
            # Datos de peso promedio por raza
            peso_data = {
                raza1: [
                    ("Semana 1", 1200),
                    ("Semana 2", 1350),
                    ("Semana 3", 1450),
                    ("Semana 4", 1550),
                    ("Semana 5", 1650),
                    ("Semana 6", 1700),
                    ("Semana 7", 1750),
                    ("Semana 8", 1780)
                ],
                raza2: [
                    ("Semana 1", 1100),
                    ("Semana 2", 1250),
                    ("Semana 3", 1380),
                    ("Semana 4", 1480),
                    ("Semana 5", 1550),
                    ("Semana 6", 1620),
                    ("Semana 7", 1680),
                    ("Semana 8", 1720)
                ]
            }
            self.peso_comp_chart.set_data(peso_data, "Semana", "Peso (g)")
            
            # Datos de mortalidad por raza
            mortalidad_data = {
                raza1: [
                    ("Semana 1", 0.5),
                    ("Semana 2", 0.3),
                    ("Semana 3", 0.2),
                    ("Semana 4", 0.4),
                    ("Semana 5", 0.3),
                    ("Semana 6", 0.2),
                    ("Semana 7", 0.1),
                    ("Semana 8", 0.2)
                ],
                raza2: [
                    ("Semana 1", 0.7),
                    ("Semana 2", 0.5),
                    ("Semana 3", 0.4),
                    ("Semana 4", 0.3),
                    ("Semana 5", 0.4),
                    ("Semana 6", 0.3),
                    ("Semana 7", 0.2),
                    ("Semana 8", 0.3)
                ]
            }
            self.mortalidad_comp_chart.set_data(mortalidad_data, "Semana", "Mortalidad (%)")
            
            # Datos de consumo de alimento por raza
            consumo_data = {
                raza1: [
                    ("Semana 1", 22),
                    ("Semana 2", 25),
                    ("Semana 3", 28),
                    ("Semana 4", 30),
                    ("Semana 5", 32),
                    ("Semana 6", 33),
                    ("Semana 7", 34),
                    ("Semana 8", 35)
                ],
                raza2: [
                    ("Semana 1", 20),
                    ("Semana 2", 23),
                    ("Semana 3", 26),
                    ("Semana 4", 28),
                    ("Semana 5", 30),
                    ("Semana 6", 31),
                    ("Semana 7", 32),
                    ("Semana 8", 33)
                ]
            }
            self.consumo_comp_chart.set_data(consumo_data, "Semana", "Consumo (g/ave/día)")
            
            # Mostrar mensaje de éxito
            QMessageBox.information(self, "Comparación Actualizada", f"Se ha actualizado la comparación entre {raza1} y {raza2} para el período: {periodo}")
            
        except Exception as e:
            print(f"Error al actualizar comparación de razas: {e}")
            QMessageBox.warning(self, "Error", f"Error al actualizar la comparación de razas: {str(e)}")
    
    def refresh_data(self):
        """Actualiza los datos de los gráficos"""
        try:
            # Cargar galpones disponibles
            self.galpon_combo.blockSignals(True)
            self.galpon_combo.clear()
            
            # Obtener galpones desde la API
            if hasattr(self.api_client, 'get_galpones'):
                success, galpones = self.api_client.get_galpones()
                
                if success and isinstance(galpones, list):
                    # Agregar opción para todos los galpones
                    self.galpon_combo.addItem("Todos los galpones", "0")
                    
                    for galpon in galpones:
                        if isinstance(galpon, dict):
                            galpon_nombre = str(galpon.get('nombre', ''))
                            galpon_id = str(galpon.get('id', ''))
                            self.galpon_combo.addItem(galpon_nombre, galpon_id)
                else:
                    # Si no hay datos, usar ejemplos
                    self.galpon_combo.addItem("Todos los galpones", "0")
                    self.galpon_combo.addItem("Galpón A", "1")
                    self.galpon_combo.addItem("Galpón B", "2")
                    self.galpon_combo.addItem("Galpón C", "3")
            else:
                # Si no existe el método, usar ejemplos
                self.galpon_combo.addItem("Todos los galpones", "0")
                self.galpon_combo.addItem("Galpón A", "1")
                self.galpon_combo.addItem("Galpón B", "2")
                self.galpon_combo.addItem("Galpón C", "3")
            
            self.galpon_combo.blockSignals(False)
            
            # Cargar lotes para el galpón seleccionado
            self.cargar_lotes_por_galpon()
            
            # Obtener datos de la API
            # En una aplicación real, aquí se obtendrían los datos de la API
            # Por ahora, usamos datos de ejemplo
            
            # Cargar razas disponibles para los combos de comparación
            self.cargar_razas_disponibles()
            
            # Obtener estadísticas del dashboard
            success, stats = self.api_client.get_dashboard_stats()
            
            if success and stats and isinstance(stats, dict):
                try:
                    # Actualizar tarjetas
                    self.total_aves_card.value_label.setText(str(stats.get('total_aves', 0)))
                    self.produccion_card.value_label.setText(str(stats.get('produccion_diaria', 0)))
                    self.mortalidad_card.value_label.setText(str(stats.get('mortalidad_diaria', 0)))
                    self.ventas_card.value_label.setText(f"${stats.get('ventas_diarias', 0)}")
                    
                    # Actualizar gráficos
                    # Datos de producción
                    if 'produccion_diaria' in stats and stats['produccion_diaria']:
                        produccion_items = [(item['fecha'], item['cantidad']) for item in stats['produccion_diaria'] if 'fecha' in item and 'cantidad' in item]
                        if produccion_items:
                            produccion_data = {"Huevos": produccion_items}
                            self.produccion_chart.set_data(produccion_data, "Fecha", "Cantidad")
                    
                    # Datos de mortalidad
                    if 'mortalidad_diaria' in stats and stats['mortalidad_diaria']:
                        mortalidad_items = [(item['fecha'], item['cantidad']) for item in stats['mortalidad_diaria'] if 'fecha' in item and 'cantidad' in item]
                        if mortalidad_items:
                            mortalidad_data = {"Mortalidad": mortalidad_items}
                            self.mortalidad_chart.set_data(mortalidad_data, "Fecha", "Cantidad")
                    
                    # Datos de ventas
                    if 'ventas_diarias' in stats and stats['ventas_diarias']:
                        ventas_items = [(item['fecha'], item['monto']) for item in stats['ventas_diarias'] if 'fecha' in item and 'monto' in item]
                        if ventas_items:
                            ventas_data = {"Ventas": ventas_items}
                            self.ventas_chart.set_data(ventas_data, "Fecha", "Monto ($)")
                    
                    # Datos de distribución de huevos
                    if 'distribucion_huevos' in stats and stats['distribucion_huevos']:
                        distribucion_items = [(item['tipo'], item['porcentaje']) for item in stats['distribucion_huevos'] if 'tipo' in item and 'porcentaje' in item]
                        if distribucion_items:
                            self.distribucion_chart.set_data(distribucion_items)
                    
                    # Datos de inventario de alimentos
                    if 'inventario_alimentos' in stats and stats['inventario_alimentos']:
                        inventario_items = [(item['tipo'], item['cantidad']) for item in stats['inventario_alimentos'] if 'tipo' in item and 'cantidad' in item]
                        if inventario_items:
                            inventario_data = {"Cantidad (kg)": inventario_items}
                            self.inventario_chart.set_data(inventario_data, "Tipo", "Cantidad (kg)")
                    
                    # Actualizar comparación de razas si hay razas seleccionadas
                    if self.raza1_combo.currentText() and self.raza2_combo.currentText():
                        self.actualizar_comparacion_razas()
                        
                except Exception as e:
                    print(f"Error al procesar datos de gráficos: {e}")
                    # Continuar con datos de ejemplo si hay error en el procesamiento
            else:
                # Si no hay conexión o los datos no son válidos, usar datos de ejemplo
                print("Usando datos de ejemplo para estadísticas")
                
                # Actualizar tarjetas con datos de ejemplo
                self.total_aves_card.value_label.setText("3,247")
                self.produccion_card.value_label.setText("2,150")
                self.mortalidad_card.value_label.setText("23")
                self.ventas_card.value_label.setText("$12,500")
                
                # Datos de ejemplo para gráficos
                # Datos de producción
                produccion_data = {
                    "Huevos": [
                        ("Lun", 1200),
                        ("Mar", 1350),
                        ("Mié", 1100),
                        ("Jue", 1400),
                        ("Vie", 1250),
                        ("Sáb", 1000),
                        ("Dom", 950)
                    ]
                }
                self.produccion_chart.set_data(produccion_data, "Día", "Cantidad")
                
                # Datos de mortalidad
                mortalidad_data = {
                    "Mortalidad": [
                        ("Lun", 2),
                        ("Mar", 3),
                        ("Mié", 1),
                        ("Jue", 2),
                        ("Vie", 4),
                        ("Sáb", 2),
                        ("Dom", 1)
                    ]
                }
                self.mortalidad_chart.set_data(mortalidad_data, "Día", "Cantidad")
                
                # Datos de ventas
                ventas_data = {
                    "Ventas": [
                        ("Lun", 5000),
                        ("Mar", 6200),
                        ("Mié", 4800),
                        ("Jue", 7500),
                        ("Vie", 8200),
                        ("Sáb", 9500),
                        ("Dom", 3800)
                    ]
                }
                self.ventas_chart.set_data(ventas_data, "Día", "Monto ($)")
                
                # Datos de distribución de huevos
                distribucion_data = [
                    ("Tipo A", 55),
                    ("Tipo B", 30),
                    ("Tipo C", 15)
                ]
                self.distribucion_chart.set_data(distribucion_data)
                
                # Datos de inventario de alimentos
                inventario_data = {
                    "Cantidad (kg)": [
                        ("Inicio", 500),
                        ("Crecimiento", 350),
                        ("Postura", 800),
                        ("Engorde", 250)
                    ]
                }
                self.inventario_chart.set_data(inventario_data, "Tipo", "Cantidad (kg)")
                
                # Cargar datos de ejemplo para la comparación de razas
                self.cargar_razas_ejemplo()
                if self.raza1_combo.count() > 0 and self.raza2_combo.count() > 0:
                    self.raza1_combo.setCurrentIndex(0)
                    self.raza2_combo.setCurrentIndex(1 if self.raza2_combo.count() > 1 else 0)
                    self.actualizar_comparacion_razas()
            
        except Exception as e:
            print(f"Error al actualizar estadísticas: {e}")
            # Mostrar mensaje de error en lugar de fallar completamente
            QMessageBox.warning(self, "Error", f"Error al actualizar estadísticas. La aplicación continuará con datos de ejemplo.")
            
            # Usar datos de ejemplo en caso de error
            self.total_aves_card.value_label.setText("3,247")
            self.produccion_card.value_label.setText("2,150")
            self.mortalidad_card.value_label.setText("23")
            self.ventas_card.value_label.setText("$12,500")
            
    def cargar_razas_disponibles(self):
        """Carga las razas disponibles en los combos de comparación"""
        try:
            # Obtener razas desde la API
            if hasattr(self.api_client, 'get_razas'):
                success, razas = self.api_client.get_razas()
                if success and razas and isinstance(razas, list):
                    # Guardar estado actual
                    raza1_actual = self.raza1_combo.currentText()
                    raza2_actual = self.raza2_combo.currentText()
                    
                    # Limpiar combos
                    self.raza1_combo.clear()
                    self.raza2_combo.clear()
                    
                    # Agregar razas a los combos
                    for raza in razas:
                        if isinstance(raza, dict) and 'nombre' in raza:
                            self.raza1_combo.addItem(raza['nombre'])
                            self.raza2_combo.addItem(raza['nombre'])
                    
                    # Restaurar selecciones previas si es posible
                    if raza1_actual:
                        index = self.raza1_combo.findText(raza1_actual)
                        if index >= 0:
                            self.raza1_combo.setCurrentIndex(index)
                    
                    if raza2_actual:
                        index = self.raza2_combo.findText(raza2_actual)
                        if index >= 0:
                            self.raza2_combo.setCurrentIndex(index)
                    
                    return
            
            # Si llegamos aquí, usar datos de ejemplo
            self.cargar_razas_ejemplo()
            
        except Exception as e:
            print(f"Error al cargar razas disponibles: {e}")
            self.cargar_razas_ejemplo()
    
    def cargar_razas_ejemplo(self):
        """Carga razas de ejemplo en los combos de comparación"""
        # Guardar estado actual
        raza1_actual = self.raza1_combo.currentText()
        raza2_actual = self.raza2_combo.currentText()
        
        # Limpiar combos
        self.raza1_combo.clear()
        self.raza2_combo.clear()
        
        # Agregar razas de ejemplo
        razas_ejemplo = ["Broiler", "Ponedora", "Reproductora", "Isa Brown", "Ross 308", "Leghorn Blanca"]
        for raza in razas_ejemplo:
            self.raza1_combo.addItem(raza)
            self.raza2_combo.addItem(raza)
        
        # Restaurar selecciones previas si es posible
        if raza1_actual:
            index = self.raza1_combo.findText(raza1_actual)
            if index >= 0:
                self.raza1_combo.setCurrentIndex(index)
        
        if raza2_actual:
            index = self.raza2_combo.findText(raza2_actual)
            if index >= 0:
                self.raza2_combo.setCurrentIndex(index)
                
    def cargar_lotes_por_galpon(self):
        """Carga los lotes disponibles para el galpón seleccionado"""
        try:
            # Obtener el galpón seleccionado
            if self.galpon_combo.count() == 0:
                return
                
            galpon_id = self.galpon_combo.currentData()
            
            # Limpiar el combo de lotes
            self.lote_combo.clear()
            
            # Obtener lotes para el galpón seleccionado
            if hasattr(self.api_client, 'get_lotes_por_galpon'):
                success, lotes = self.api_client.get_lotes_por_galpon(galpon_id)
                
                if success and isinstance(lotes, list):
                    for lote in lotes:
                        if isinstance(lote, dict):
                            lote_nombre = str(lote.get('nombre', ''))
                            lote_id = str(lote.get('id', ''))
                            self.lote_combo.addItem(lote_nombre, lote_id)
                    return
            
            # Si no hay datos de la API o hay un error, usar datos de ejemplo
            ejemplos = [
                {"id": 1, "nombre": "Lote A-001"},
                {"id": 2, "nombre": "Lote B-002"},
                {"id": 3, "nombre": "Lote C-003"}
            ]
            
            for lote in ejemplos:
                lote_nombre = lote.get('nombre', '')
                lote_id = lote.get('id', '')
                self.lote_combo.addItem(lote_nombre, lote_id)
                
        except Exception as e:
            print(f"Error al cargar lotes por galpón: {e}")
            # En caso de error, mostrar datos de ejemplo
            self.lote_combo.clear()
            self.lote_combo.addItem("Lote A-001", "1")
            self.lote_combo.addItem("Lote B-002", "2")
            self.lote_combo.addItem("Lote C-003", "3")

from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                            QPushButton, QComboBox, QGroupBox, QFormLayout,
                            QMessageBox, QFrame, QScrollArea, QDateEdit,
                            QFileDialog, QTableWidget, QTableWidgetItem,
                            QHeaderView, QCheckBox)
from PyQt5.QtCore import Qt, QDate
from PyQt5.QtGui import QPainter
from PyQt5.QtPrintSupport import QPrinter, QPrintDialog, QPrintPreviewDialog
import datetime
import csv
import os

class ReportesTab(QWidget):
    """Pestaña para generar reportes"""
    
    def __init__(self, api_client):
        super().__init__()
        self.api_client = api_client
        
        # Crear layout principal
        main_layout = QVBoxLayout(self)
        
        # Título
        title_label = QLabel("Generación de Reportes")
        title_label.setStyleSheet("font-size: 24px; font-weight: bold; color: #5a5c69;")
        main_layout.addWidget(title_label)
        
        # Descripción
        desc_label = QLabel("Genere reportes personalizados para análisis y seguimiento")
        desc_label.setStyleSheet("font-size: 14px; color: #858796; margin-bottom: 20px;")
        main_layout.addWidget(desc_label)
        
        # Área de desplazamiento
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setFrameShape(QFrame.NoFrame)
        
        # Contenido desplazable
        scroll_content = QWidget()
        scroll_layout = QVBoxLayout(scroll_content)
        
        # Sección de filtros
        filtros_group = QGroupBox("Filtros de Reporte")
        filtros_layout = QFormLayout(filtros_group)
        
        # Tipo de reporte
        self.tipo_reporte_combo = QComboBox()
        self.tipo_reporte_combo.addItems([
            "Producción diaria", 
            "Mortalidad por lote", 
            "Consumo de alimento", 
            "Rendimiento por raza",
            "Inventario de aves",
            "Histórico de ventas"
        ])
        self.tipo_reporte_combo.currentIndexChanged.connect(self.actualizar_opciones_reporte)
        filtros_layout.addRow("Tipo de reporte:", self.tipo_reporte_combo)
        
        # Filtro de galpón
        self.galpon_combo = QComboBox()
        self.galpon_combo.currentIndexChanged.connect(self.cargar_lotes_por_galpon)
        filtros_layout.addRow("Galpón:", self.galpon_combo)
        
        # Filtro de lote
        self.lote_combo = QComboBox()
        filtros_layout.addRow("Lote:", self.lote_combo)
        
        # Filtro de raza
        self.raza_combo = QComboBox()
        filtros_layout.addRow("Raza:", self.raza_combo)
        
        # Rango de fechas
        fecha_layout = QHBoxLayout()
        
        # Fecha inicial
        self.fecha_inicio_edit = QDateEdit()
        self.fecha_inicio_edit.setCalendarPopup(True)
        self.fecha_inicio_edit.setDate(QDate.currentDate().addDays(-30))
        fecha_layout.addWidget(QLabel("Desde:"))
        fecha_layout.addWidget(self.fecha_inicio_edit)
        
        # Fecha final
        self.fecha_fin_edit = QDateEdit()
        self.fecha_fin_edit.setCalendarPopup(True)
        self.fecha_fin_edit.setDate(QDate.currentDate())
        fecha_layout.addWidget(QLabel("Hasta:"))
        fecha_layout.addWidget(self.fecha_fin_edit)
        
        filtros_layout.addRow("Período:", fecha_layout)
        
        # Opciones adicionales
        self.opciones_group = QGroupBox("Opciones adicionales")
        self.opciones_layout = QVBoxLayout(self.opciones_group)
        
        # Incluir gráficos
        self.incluir_graficos_check = QCheckBox("Incluir gráficos")
        self.incluir_graficos_check.setChecked(True)
        self.opciones_layout.addWidget(self.incluir_graficos_check)
        
        # Incluir resumen
        self.incluir_resumen_check = QCheckBox("Incluir resumen estadístico")
        self.incluir_resumen_check.setChecked(True)
        self.opciones_layout.addWidget(self.incluir_resumen_check)
        
        # Incluir datos crudos
        self.incluir_datos_check = QCheckBox("Incluir datos crudos")
        self.incluir_datos_check.setChecked(True)
        self.opciones_layout.addWidget(self.incluir_datos_check)
        
        # Agregar secciones al layout
        scroll_layout.addWidget(filtros_group)
        scroll_layout.addWidget(self.opciones_group)
        
        # Vista previa de datos
        self.preview_group = QGroupBox("Vista previa de datos")
        preview_layout = QVBoxLayout(self.preview_group)
        
        # Tabla de vista previa
        self.preview_table = QTableWidget()
        self.preview_table.setAlternatingRowColors(True)
        self.preview_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        preview_layout.addWidget(self.preview_table)
        
        scroll_layout.addWidget(self.preview_group)
        
        # Botones de acción
        buttons_layout = QHBoxLayout()
        
        # Botón de vista previa
        self.preview_button = QPushButton("Generar Vista Previa")
        self.preview_button.clicked.connect(self.generar_vista_previa)
        self.preview_button.setStyleSheet("""
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
        buttons_layout.addWidget(self.preview_button)
        
        # Botón de exportar a PDF
        self.pdf_button = QPushButton("Exportar a PDF")
        self.pdf_button.clicked.connect(self.exportar_pdf)
        self.pdf_button.setStyleSheet("""
            QPushButton {
                background-color: #e74a3b;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #c72a1c;
            }
        """)
        buttons_layout.addWidget(self.pdf_button)
        
        # Botón de exportar a CSV
        self.csv_button = QPushButton("Exportar a CSV")
        self.csv_button.clicked.connect(self.exportar_csv)
        self.csv_button.setStyleSheet("""
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
        buttons_layout.addWidget(self.csv_button)
        
        scroll_layout.addLayout(buttons_layout)
        
        # Finalizar layout
        scroll_area.setWidget(scroll_content)
        main_layout.addWidget(scroll_area)
        
        # Cargar datos iniciales
        self.cargar_datos_iniciales()
        
    def cargar_datos_iniciales(self):
        """Carga los datos iniciales para los filtros"""
        try:
            # Cargar galpones
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
            
            # Cargar razas
            if hasattr(self.api_client, 'get_razas'):
                success, razas = self.api_client.get_razas()
                
                if success and isinstance(razas, list):
                    # Agregar opción para todas las razas
                    self.raza_combo.addItem("Todas las razas", "0")
                    
                    for raza in razas:
                        if isinstance(raza, dict):
                            raza_nombre = str(raza.get('nombre', ''))
                            raza_id = str(raza.get('id', ''))
                            self.raza_combo.addItem(raza_nombre, raza_id)
                else:
                    # Si no hay datos, usar ejemplos
                    self.raza_combo.addItem("Todas las razas", "0")
                    self.raza_combo.addItem("Broiler", "1")
                    self.raza_combo.addItem("Ponedora", "2")
                    self.raza_combo.addItem("Reproductora", "3")
                    self.raza_combo.addItem("Isa Brown", "4")
                    self.raza_combo.addItem("Ross 308", "5")
            else:
                # Si no existe el método, usar ejemplos
                self.raza_combo.addItem("Todas las razas", "0")
                self.raza_combo.addItem("Broiler", "1")
                self.raza_combo.addItem("Ponedora", "2")
                self.raza_combo.addItem("Reproductora", "3")
                self.raza_combo.addItem("Isa Brown", "4")
                self.raza_combo.addItem("Ross 308", "5")
            
            # Cargar lotes para el galpón seleccionado
            self.cargar_lotes_por_galpon()
            
            # Actualizar opciones según el tipo de reporte
            self.actualizar_opciones_reporte()
            
        except Exception as e:
            print(f"Error al cargar datos iniciales: {e}")
            QMessageBox.warning(self, "Error", f"Error al cargar datos iniciales: {e}")
    
    def cargar_lotes_por_galpon(self):
        """Carga los lotes disponibles para el galpón seleccionado"""
        try:
            # Obtener el galpón seleccionado
            if self.galpon_combo.count() == 0:
                return
                
            galpon_id = self.galpon_combo.currentData()
            
            # Limpiar el combo de lotes
            self.lote_combo.clear()
            
            # Agregar opción para todos los lotes
            self.lote_combo.addItem("Todos los lotes", "0")
            
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
            self.lote_combo.addItem("Todos los lotes", "0")
            self.lote_combo.addItem("Lote A-001", "1")
            self.lote_combo.addItem("Lote B-002", "2")
            self.lote_combo.addItem("Lote C-003", "3")
    
    def actualizar_opciones_reporte(self):
        """Actualiza las opciones disponibles según el tipo de reporte seleccionado"""
        tipo_reporte = self.tipo_reporte_combo.currentText()
        
        # Habilitar/deshabilitar filtros según el tipo de reporte
        if tipo_reporte == "Rendimiento por raza":
            self.raza_combo.setEnabled(True)
            self.galpon_combo.setEnabled(False)
            self.lote_combo.setEnabled(False)
        elif tipo_reporte == "Mortalidad por lote" or tipo_reporte == "Consumo de alimento":
            self.raza_combo.setEnabled(False)
            self.galpon_combo.setEnabled(True)
            self.lote_combo.setEnabled(True)
        elif tipo_reporte == "Inventario de aves":
            self.raza_combo.setEnabled(True)
            self.galpon_combo.setEnabled(True)
            self.lote_combo.setEnabled(False)
        else:
            # Para "Producción diaria" y "Histórico de ventas"
            self.raza_combo.setEnabled(True)
            self.galpon_combo.setEnabled(True)
            self.lote_combo.setEnabled(True)
    
    def generar_vista_previa(self):
        """Genera una vista previa de los datos del reporte"""
        try:
            tipo_reporte = self.tipo_reporte_combo.currentText()
            
            # Configurar tabla según el tipo de reporte
            if tipo_reporte == "Producción diaria":
                headers = ["Fecha", "Galpón", "Lote", "Raza", "Cantidad (huevos)", "Peso promedio (g)"]
                self.preview_table.setColumnCount(len(headers))
                self.preview_table.setHorizontalHeaderLabels(headers)
                
                # Datos de ejemplo para producción diaria
                datos = [
                    ["2025-05-15", "Galpón A", "Lote A-001", "Ponedora", "1850", "65.2"],
                    ["2025-05-16", "Galpón A", "Lote A-001", "Ponedora", "1920", "64.8"],
                    ["2025-05-17", "Galpón A", "Lote A-001", "Ponedora", "2050", "65.5"],
                    ["2025-05-18", "Galpón A", "Lote A-001", "Ponedora", "2150", "65.3"],
                    ["2025-05-19", "Galpón A", "Lote A-001", "Ponedora", "2300", "65.7"],
                    ["2025-05-15", "Galpón B", "Lote B-002", "Isa Brown", "2100", "62.1"],
                    ["2025-05-16", "Galpón B", "Lote B-002", "Isa Brown", "2150", "62.3"],
                    ["2025-05-17", "Galpón B", "Lote B-002", "Isa Brown", "2200", "62.5"],
                    ["2025-05-18", "Galpón B", "Lote B-002", "Isa Brown", "2250", "62.8"],
                    ["2025-05-19", "Galpón B", "Lote B-002", "Isa Brown", "2300", "63.0"]
                ]
                
            elif tipo_reporte == "Mortalidad por lote":
                headers = ["Fecha", "Galpón", "Lote", "Cantidad", "Causa", "Observaciones"]
                self.preview_table.setColumnCount(len(headers))
                self.preview_table.setHorizontalHeaderLabels(headers)
                
                # Datos de ejemplo para mortalidad
                datos = [
                    ["2025-05-15", "Galpón A", "Lote A-001", "3", "Enfermedad", "Síntomas respiratorios"],
                    ["2025-05-16", "Galpón A", "Lote A-001", "2", "Desconocida", ""],
                    ["2025-05-17", "Galpón A", "Lote A-001", "1", "Accidente", "Aplastamiento"],
                    ["2025-05-18", "Galpón A", "Lote A-001", "0", "", ""],
                    ["2025-05-19", "Galpón A", "Lote A-001", "2", "Enfermedad", "Diarrea"],
                    ["2025-05-15", "Galpón B", "Lote B-002", "1", "Desconocida", ""],
                    ["2025-05-16", "Galpón B", "Lote B-002", "0", "", ""],
                    ["2025-05-17", "Galpón B", "Lote B-002", "2", "Enfermedad", "Problemas respiratorios"],
                    ["2025-05-18", "Galpón B", "Lote B-002", "1", "Accidente", ""],
                    ["2025-05-19", "Galpón B", "Lote B-002", "0", "", ""]
                ]
                
            elif tipo_reporte == "Consumo de alimento":
                headers = ["Fecha", "Galpón", "Lote", "Consumo (kg)", "Consumo por ave (g)", "Tipo de alimento"]
                self.preview_table.setColumnCount(len(headers))
                self.preview_table.setHorizontalHeaderLabels(headers)
                
                # Datos de ejemplo para consumo
                datos = [
                    ["2025-05-15", "Galpón A", "Lote A-001", "250", "125", "Inicio"],
                    ["2025-05-16", "Galpón A", "Lote A-001", "255", "127.5", "Inicio"],
                    ["2025-05-17", "Galpón A", "Lote A-001", "260", "130", "Inicio"],
                    ["2025-05-18", "Galpón A", "Lote A-001", "265", "132.5", "Inicio"],
                    ["2025-05-19", "Galpón A", "Lote A-001", "270", "135", "Inicio"],
                    ["2025-05-15", "Galpón B", "Lote B-002", "300", "120", "Crecimiento"],
                    ["2025-05-16", "Galpón B", "Lote B-002", "305", "122", "Crecimiento"],
                    ["2025-05-17", "Galpón B", "Lote B-002", "310", "124", "Crecimiento"],
                    ["2025-05-18", "Galpón B", "Lote B-002", "315", "126", "Crecimiento"],
                    ["2025-05-19", "Galpón B", "Lote B-002", "320", "128", "Crecimiento"]
                ]
                
            elif tipo_reporte == "Rendimiento por raza":
                headers = ["Raza", "Producción promedio", "Peso promedio (g)", "Consumo promedio (g)", "Conversión alimenticia", "Mortalidad (%)"]
                self.preview_table.setColumnCount(len(headers))
                self.preview_table.setHorizontalHeaderLabels(headers)
                
                # Datos de ejemplo para rendimiento
                datos = [
                    ["Ponedora", "0.95", "65.3", "125", "1.8", "2.1"],
                    ["Isa Brown", "0.92", "62.5", "122", "1.9", "1.8"],
                    ["Leghorn Blanca", "0.94", "60.2", "115", "1.7", "2.0"],
                    ["Ross 308", "0", "2500", "180", "1.6", "3.2"],
                    ["Broiler", "0", "2350", "175", "1.65", "3.5"]
                ]
                
            elif tipo_reporte == "Inventario de aves":
                headers = ["Galpón", "Raza", "Cantidad inicial", "Mortalidad acumulada", "Ventas", "Cantidad actual"]
                self.preview_table.setColumnCount(len(headers))
                self.preview_table.setHorizontalHeaderLabels(headers)
                
                # Datos de ejemplo para inventario
                datos = [
                    ["Galpón A", "Ponedora", "2000", "42", "0", "1958"],
                    ["Galpón B", "Isa Brown", "2500", "45", "0", "2455"],
                    ["Galpón C", "Leghorn Blanca", "1800", "36", "0", "1764"],
                    ["Galpón D", "Ross 308", "3000", "96", "2500", "404"],
                    ["Galpón E", "Broiler", "3500", "122", "3000", "378"]
                ]
                
            else:  # "Histórico de ventas"
                headers = ["Fecha", "Galpón", "Lote", "Raza", "Cantidad", "Peso total (kg)", "Precio unitario", "Total"]
                self.preview_table.setColumnCount(len(headers))
                self.preview_table.setHorizontalHeaderLabels(headers)
                
                # Datos de ejemplo para ventas
                datos = [
                    ["2025-04-15", "Galpón D", "Lote D-001", "Ross 308", "1000", "2500", "$5.50", "$5,500"],
                    ["2025-04-20", "Galpón D", "Lote D-001", "Ross 308", "1500", "3750", "$5.50", "$8,250"],
                    ["2025-04-25", "Galpón E", "Lote E-001", "Broiler", "1200", "2820", "$5.25", "$6,300"],
                    ["2025-04-30", "Galpón E", "Lote E-001", "Broiler", "1800", "4230", "$5.25", "$9,450"],
                    ["2025-05-05", "Galpón A", "Lote A-001", "Ponedora", "1000", "65", "$0.25", "$250"]
                ]
            
            # Llenar tabla con datos
            self.preview_table.setRowCount(len(datos))
            for row, fila in enumerate(datos):
                for col, valor in enumerate(fila):
                    item = QTableWidgetItem(valor)
                    self.preview_table.setItem(row, col, item)
            
            # Ajustar tamaño de columnas
            self.preview_table.resizeColumnsToContents()
            
            QMessageBox.information(self, "Vista Previa", "Se ha generado la vista previa del reporte")
            
        except Exception as e:
            print(f"Error al generar vista previa: {e}")
            QMessageBox.warning(self, "Error", f"Error al generar vista previa: {e}")
    
    def exportar_pdf(self):
        """Exporta el reporte a un archivo PDF"""
        try:
            # Verificar si hay datos para exportar
            if self.preview_table.rowCount() == 0:
                QMessageBox.warning(self, "Advertencia", "No hay datos para exportar. Genere una vista previa primero.")
                return
            
            # Solicitar ubicación para guardar el archivo
            file_path, _ = QFileDialog.getSaveFileName(self, "Guardar Reporte", "", "Archivos PDF (*.pdf)")
            
            if not file_path:
                return
            
            # Asegurarse de que el archivo tenga extensión .pdf
            if not file_path.lower().endswith('.pdf'):
                file_path += '.pdf'
            
            # Crear impresora PDF
            printer = QPrinter(QPrinter.HighResolution)
            printer.setOutputFormat(QPrinter.PdfFormat)
            printer.setOutputFileName(file_path)
            
            # Mostrar diálogo de vista previa
            preview = QPrintPreviewDialog(printer, self)
            preview.paintRequested.connect(self.imprimir_documento)
            preview.exec_()
            
            QMessageBox.information(self, "Exportación Exitosa", f"El reporte se ha exportado correctamente a:\n{file_path}")
            
        except Exception as e:
            print(f"Error al exportar a PDF: {e}")
            QMessageBox.warning(self, "Error", f"Error al exportar a PDF: {e}")
    
    def imprimir_documento(self, printer):
        """Imprime el documento en la impresora especificada"""
        # Aquí se implementaría la lógica para generar el PDF con los datos de la tabla
        # Por simplicidad, solo mostraremos un mensaje
        QMessageBox.information(self, "Impresión", "Funcionalidad de impresión en desarrollo")
    
    def exportar_csv(self):
        """Exporta el reporte a un archivo CSV"""
        try:
            # Verificar si hay datos para exportar
            if self.preview_table.rowCount() == 0:
                QMessageBox.warning(self, "Advertencia", "No hay datos para exportar. Genere una vista previa primero.")
                return
            
            # Solicitar ubicación para guardar el archivo
            file_path, _ = QFileDialog.getSaveFileName(self, "Guardar Reporte", "", "Archivos CSV (*.csv)")
            
            if not file_path:
                return
            
            # Asegurarse de que el archivo tenga extensión .csv
            if not file_path.lower().endswith('.csv'):
                file_path += '.csv'
            
            # Obtener encabezados
            headers = []
            for col in range(self.preview_table.columnCount()):
                headers.append(self.preview_table.horizontalHeaderItem(col).text())
            
            # Escribir datos al archivo CSV
            with open(file_path, 'w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(headers)
                
                for row in range(self.preview_table.rowCount()):
                    row_data = []
                    for col in range(self.preview_table.columnCount()):
                        item = self.preview_table.item(row, col)
                        row_data.append(item.text() if item else "")
                    writer.writerow(row_data)
            
            QMessageBox.information(self, "Exportación Exitosa", f"El reporte se ha exportado correctamente a:\n{file_path}")
            
        except Exception as e:
            print(f"Error al exportar a CSV: {e}")
            QMessageBox.warning(self, "Error", f"Error al exportar a CSV: {e}")
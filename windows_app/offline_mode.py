"""
Versión de la aplicación que funciona completamente en modo offline
Esta versión no intenta conectarse al servidor Django en absoluto
"""
import sys
import os
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                            QHBoxLayout, QLabel, QPushButton, QTableWidget, 
                            QTableWidgetItem, QMessageBox, QTabWidget)
from PyQt5.QtGui import QIcon, QPixmap, QFont
from PyQt5.QtCore import Qt

class OfflineGalponesTab(QWidget):
    """Versión offline de la pestaña de galpones"""
    def __init__(self):
        super().__init__()
        
        # Crear layout principal
        layout = QVBoxLayout(self)
        
        # Crear encabezado
        header_layout = QHBoxLayout()
        
        # Título
        title = QLabel("Galpones")
        title.setFont(QFont("Arial", 14, QFont.Bold))
        header_layout.addWidget(title)
        
        # Espacio flexible
        header_layout.addStretch()
        
        # Botones
        self.new_button = QPushButton("Nuevo Galpón")
        self.new_button.clicked.connect(self.create_galpon)
        header_layout.addWidget(self.new_button)
        
        self.edit_button = QPushButton("Editar")
        self.edit_button.clicked.connect(self.edit_galpon)
        header_layout.addWidget(self.edit_button)
        
        self.refresh_button = QPushButton("Actualizar")
        self.refresh_button.clicked.connect(self.refresh_data)
        header_layout.addWidget(self.refresh_button)
        
        layout.addLayout(header_layout)
        
        # Crear tabla
        self.table = QTableWidget()
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels(["ID", "Nombre", "Capacidad", "Ancho (m)", "Largo (m)", "Área (m²)", "Estado"])
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setSelectionMode(QTableWidget.SingleSelection)
        self.table.setAlternatingRowColors(True)
        layout.addWidget(self.table)
        
        # Cargar datos de ejemplo
        self.refresh_data()
    
    def refresh_data(self):
        """Actualiza los datos de la tabla de galpones con datos de ejemplo"""
        # Limpiar tabla
        self.table.setRowCount(0)
        
        # Datos de ejemplo
        ejemplos = [
            {
                'id': 1,
                'nombre': 'Galpón 1',
                'capacidad': 1000,
                'ancho': 10,
                'largo': 20,
                'estado': 'Activo'
            },
            {
                'id': 2,
                'nombre': 'Galpón 2',
                'capacidad': 1500,
                'ancho': 12,
                'largo': 25,
                'estado': 'Activo'
            },
            {
                'id': 3,
                'nombre': 'Galpón 3',
                'capacidad': 800,
                'ancho': 8,
                'largo': 18,
                'estado': 'Mantenimiento'
            },
            {
                'id': 4,
                'nombre': 'Galpón 4',
                'capacidad': 1200,
                'ancho': 10,
                'largo': 24,
                'estado': 'Activo'
            },
            {
                'id': 5,
                'nombre': 'Galpón 5',
                'capacidad': 900,
                'ancho': 9,
                'largo': 20,
                'estado': 'Inactivo'
            }
        ]
        
        for row, galpon in enumerate(ejemplos):
            self.table.insertRow(row)
            
            # ID
            self.table.setItem(row, 0, QTableWidgetItem(str(galpon['id'])))
            
            # Nombre
            self.table.setItem(row, 1, QTableWidgetItem(galpon['nombre']))
            
            # Capacidad
            self.table.setItem(row, 2, QTableWidgetItem(str(galpon['capacidad'])))
            
            # Ancho
            self.table.setItem(row, 3, QTableWidgetItem(str(galpon['ancho'])))
            
            # Largo
            self.table.setItem(row, 4, QTableWidgetItem(str(galpon['largo'])))
            
            # Área
            area = galpon['ancho'] * galpon['largo']
            self.table.setItem(row, 5, QTableWidgetItem(str(area)))
            
            # Estado
            self.table.setItem(row, 6, QTableWidgetItem(galpon['estado']))
        
        self.table.resizeColumnsToContents()
    
    def create_galpon(self):
        """Simula la creación de un nuevo galpón"""
        QMessageBox.information(self, "Modo Offline", 
                               "Esta funcionalidad no está disponible en modo offline.\n\n"
                               "Para crear nuevos galpones, necesita conectarse al servidor Django.")
    
    def edit_galpon(self):
        """Simula la edición de un galpón existente"""
        QMessageBox.information(self, "Modo Offline", 
                               "Esta funcionalidad no está disponible en modo offline.\n\n"
                               "Para editar galpones, necesita conectarse al servidor Django.")

class OfflineLotesTab(QWidget):
    """Versión offline de la pestaña de lotes"""
    def __init__(self):
        super().__init__()
        
        # Crear layout principal
        layout = QVBoxLayout(self)
        
        # Crear encabezado
        header_layout = QHBoxLayout()
        
        # Título
        title = QLabel("Lotes")
        title.setFont(QFont("Arial", 14, QFont.Bold))
        header_layout.addWidget(title)
        
        # Espacio flexible
        header_layout.addStretch()
        
        # Botones
        self.new_button = QPushButton("Nuevo Lote")
        header_layout.addWidget(self.new_button)
        
        self.edit_button = QPushButton("Editar")
        header_layout.addWidget(self.edit_button)
        
        self.refresh_button = QPushButton("Actualizar")
        self.refresh_button.clicked.connect(self.refresh_data)
        header_layout.addWidget(self.refresh_button)
        
        layout.addLayout(header_layout)
        
        # Crear tabla
        self.table = QTableWidget()
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels(["ID", "Código", "Fecha Ingreso", "Cantidad", "Edad", "Galpon", "Estado"])
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setSelectionMode(QTableWidget.SingleSelection)
        self.table.setAlternatingRowColors(True)
        layout.addWidget(self.table)
        
        # Cargar datos de ejemplo
        self.refresh_data()
    
    def refresh_data(self):
        """Actualiza los datos de la tabla de lotes con datos de ejemplo"""
        # Limpiar tabla
        self.table.setRowCount(0)
        
        # Datos de ejemplo
        ejemplos = [
            {
                'id': 1,
                'codigo': 'L-2025-001',
                'fecha_ingreso': '2025-01-15',
                'cantidad': 950,
                'edad_semanas': 12,
                'galpon': 'Galpón 1',
                'estado': 'Activo'
            },
            {
                'id': 2,
                'codigo': 'L-2025-002',
                'fecha_ingreso': '2025-02-01',
                'cantidad': 1450,
                'edad_semanas': 8,
                'galpon': 'Galpón 2',
                'estado': 'Activo'
            },
            {
                'id': 3,
                'codigo': 'L-2025-003',
                'fecha_ingreso': '2025-02-15',
                'cantidad': 780,
                'edad_semanas': 6,
                'galpon': 'Galpón 3',
                'estado': 'Activo'
            },
            {
                'id': 4,
                'codigo': 'L-2025-004',
                'fecha_ingreso': '2025-03-01',
                'cantidad': 1100,
                'edad_semanas': 4,
                'galpon': 'Galpón 4',
                'estado': 'Activo'
            }
        ]
        
        for row, lote in enumerate(ejemplos):
            self.table.insertRow(row)
            
            # ID
            self.table.setItem(row, 0, QTableWidgetItem(str(lote['id'])))
            
            # Código
            self.table.setItem(row, 1, QTableWidgetItem(lote['codigo']))
            
            # Fecha Ingreso
            self.table.setItem(row, 2, QTableWidgetItem(lote['fecha_ingreso']))
            
            # Cantidad
            self.table.setItem(row, 3, QTableWidgetItem(str(lote['cantidad'])))
            
            # Edad
            self.table.setItem(row, 4, QTableWidgetItem(f"{lote['edad_semanas']} semanas"))
            
            # Galpón
            self.table.setItem(row, 5, QTableWidgetItem(lote['galpon']))
            
            # Estado
            self.table.setItem(row, 6, QTableWidgetItem(lote['estado']))
        
        self.table.resizeColumnsToContents()

class OfflineDashboardTab(QWidget):
    """Versión offline del dashboard"""
    def __init__(self):
        super().__init__()
        
        # Crear layout principal
        layout = QVBoxLayout(self)
        
        # Título
        title = QLabel("Dashboard - Modo Offline")
        title.setFont(QFont("Arial", 16, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        # Mensaje de modo offline
        message = QLabel("Estás trabajando en modo offline. Los datos mostrados son ejemplos y no reflejan el estado actual del sistema.")
        message.setStyleSheet("color: red; font-weight: bold;")
        message.setAlignment(Qt.AlignCenter)
        layout.addWidget(message)
        
        # Estadísticas rápidas
        stats_layout = QHBoxLayout()
        
        # Lotes activos
        lotes_widget = QWidget()
        lotes_layout = QVBoxLayout(lotes_widget)
        lotes_title = QLabel("Lotes Activos")
        lotes_title.setAlignment(Qt.AlignCenter)
        lotes_layout.addWidget(lotes_title)
        lotes_value = QLabel("4")
        lotes_value.setFont(QFont("Arial", 24, QFont.Bold))
        lotes_value.setAlignment(Qt.AlignCenter)
        lotes_layout.addWidget(lotes_value)
        lotes_widget.setStyleSheet("background-color: #e3f2fd; border-radius: 5px; padding: 10px;")
        stats_layout.addWidget(lotes_widget)
        
        # Galpones activos
        galpones_widget = QWidget()
        galpones_layout = QVBoxLayout(galpones_widget)
        galpones_title = QLabel("Galpones Activos")
        galpones_title.setAlignment(Qt.AlignCenter)
        galpones_layout.addWidget(galpones_title)
        galpones_value = QLabel("4")
        galpones_value.setFont(QFont("Arial", 24, QFont.Bold))
        galpones_value.setAlignment(Qt.AlignCenter)
        galpones_layout.addWidget(galpones_value)
        galpones_widget.setStyleSheet("background-color: #e8f5e9; border-radius: 5px; padding: 10px;")
        stats_layout.addWidget(galpones_widget)
        
        # Aves totales
        aves_widget = QWidget()
        aves_layout = QVBoxLayout(aves_widget)
        aves_title = QLabel("Aves Totales")
        aves_title.setAlignment(Qt.AlignCenter)
        aves_layout.addWidget(aves_title)
        aves_value = QLabel("4,280")
        aves_value.setFont(QFont("Arial", 24, QFont.Bold))
        aves_value.setAlignment(Qt.AlignCenter)
        aves_layout.addWidget(aves_value)
        aves_widget.setStyleSheet("background-color: #fff8e1; border-radius: 5px; padding: 10px;")
        stats_layout.addWidget(aves_widget)
        
        # Huevos hoy
        huevos_widget = QWidget()
        huevos_layout = QVBoxLayout(huevos_widget)
        huevos_title = QLabel("Huevos Hoy")
        huevos_title.setAlignment(Qt.AlignCenter)
        huevos_layout.addWidget(huevos_title)
        huevos_value = QLabel("3,850")
        huevos_value.setFont(QFont("Arial", 24, QFont.Bold))
        huevos_value.setAlignment(Qt.AlignCenter)
        huevos_layout.addWidget(huevos_value)
        huevos_widget.setStyleSheet("background-color: #ffebee; border-radius: 5px; padding: 10px;")
        stats_layout.addWidget(huevos_widget)
        
        layout.addLayout(stats_layout)
        
        # Mensaje de gráficos
        charts_message = QLabel("Los gráficos no están disponibles en modo offline")
        charts_message.setAlignment(Qt.AlignCenter)
        charts_message.setStyleSheet("font-style: italic; margin-top: 50px;")
        layout.addWidget(charts_message)
        
        # Espacio flexible al final
        layout.addStretch()

class OfflineMainWindow(QMainWindow):
    """Ventana principal de la aplicación en modo offline"""
    def __init__(self):
        super().__init__()
        self.setWindowTitle("App Granja - Modo Offline")
        self.setMinimumSize(1024, 768)
        
        # Crear widget central con pestañas
        self.tabs = QTabWidget()
        
        # Agregar pestañas
        self.dashboard_tab = OfflineDashboardTab()
        self.tabs.addTab(self.dashboard_tab, "Dashboard")
        
        self.galpones_tab = OfflineGalponesTab()
        self.tabs.addTab(self.galpones_tab, "Galpones")
        
        self.lotes_tab = OfflineLotesTab()
        self.tabs.addTab(self.lotes_tab, "Lotes")
        
        # Establecer widget central
        self.setCentralWidget(self.tabs)
        
        # Mostrar mensaje de modo offline
        QMessageBox.information(self, "Modo Offline", 
                               "La aplicación se está ejecutando en modo offline.\n\n"
                               "Todos los datos mostrados son ejemplos y no reflejan el estado actual del sistema.\n\n"
                               "Para acceder a datos reales, asegúrese de que el servidor Django esté en funcionamiento.")

def main():
    """Función principal"""
    app = QApplication(sys.argv)
    window = OfflineMainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()

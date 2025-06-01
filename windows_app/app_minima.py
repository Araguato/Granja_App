#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Aplicación mínima para App_Granja que no depende del código existente
"""

import sys
import os
import json
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                            QHBoxLayout, QLabel, QPushButton, QTabWidget,
                            QMessageBox, QTableWidget, QTableWidgetItem,
                            QComboBox, QFormLayout, QLineEdit, QSpinBox)
from PyQt5.QtGui import QIcon, QPixmap, QFont
from PyQt5.QtCore import Qt, QSize

class MainWindow(QMainWindow):
    """Ventana principal de la aplicación mínima"""
    
    def __init__(self):
        super().__init__()
        
        # Configuración de la ventana
        self.setWindowTitle("App Granja (Versión Mínima)")
        self.setMinimumSize(800, 600)
        
        # Crear widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Layout principal
        main_layout = QVBoxLayout(central_widget)
        
        # Crear pestañas
        self.tab_widget = QTabWidget()
        main_layout.addWidget(self.tab_widget)
        
        # Crear pestañas individuales
        self.crear_tab_dashboard()
        self.crear_tab_lotes()
        self.crear_tab_galpones()
        self.crear_tab_estadisticas()
        self.crear_tab_comparacion()
        
        # Barra de estado
        self.statusBar().showMessage("Aplicación en modo offline")
        
        # Mostrar mensaje de bienvenida
        QMessageBox.information(self, "Bienvenido", 
                               "Bienvenido a la versión mínima de App Granja.\n\n"
                               "Esta versión muestra solo las funcionalidades básicas "
                               "y utiliza datos de ejemplo.")
    
    def crear_tab_dashboard(self):
        """Crea la pestaña de dashboard"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        # Título
        titulo = QLabel("Dashboard")
        titulo.setFont(QFont("Arial", 16, QFont.Bold))
        layout.addWidget(titulo)
        
        # Tarjetas de estadísticas
        cards_layout = QHBoxLayout()
        
        # Tarjeta 1: Total de aves
        card1 = self.crear_tarjeta("Total de Aves", "3,247", "#4e73df")
        cards_layout.addWidget(card1)
        
        # Tarjeta 2: Producción diaria
        card2 = self.crear_tarjeta("Producción Diaria", "2,500", "#1cc88a")
        cards_layout.addWidget(card2)
        
        # Tarjeta 3: Mortalidad
        card3 = self.crear_tarjeta("Mortalidad", "12", "#e74a3b")
        cards_layout.addWidget(card3)
        
        # Tarjeta 4: Ventas
        card4 = self.crear_tarjeta("Ventas", "$1,800", "#f6c23e")
        cards_layout.addWidget(card4)
        
        layout.addLayout(cards_layout)
        
        # Mensaje de datos de ejemplo
        nota = QLabel("Nota: Todos los datos mostrados son ejemplos y no reflejan datos reales.")
        nota.setStyleSheet("color: gray; font-style: italic;")
        layout.addWidget(nota)
        
        # Añadir pestaña
        self.tab_widget.addTab(tab, "Dashboard")
    
    def crear_tab_lotes(self):
        """Crea la pestaña de lotes"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        # Título
        titulo = QLabel("Gestión de Lotes")
        titulo.setFont(QFont("Arial", 16, QFont.Bold))
        layout.addWidget(titulo)
        
        # Tabla de lotes
        tabla = QTableWidget()
        tabla.setColumnCount(6)
        tabla.setHorizontalHeaderLabels(["ID", "Código", "Fecha Ingreso", "Cantidad", "Raza", "Galpón"])
        
        # Datos de ejemplo
        datos = [
            (1, "L001", "2025-01-15", 5000, "Leghorn Blanca", "Galpón A"),
            (2, "L002", "2025-02-01", 4500, "Rhode Island Red", "Galpón B"),
            (3, "L003", "2025-03-01", 4800, "Plymouth Rock", "Galpón C")
        ]
        
        tabla.setRowCount(len(datos))
        for i, (id, codigo, fecha, cantidad, raza, galpon) in enumerate(datos):
            tabla.setItem(i, 0, QTableWidgetItem(str(id)))
            tabla.setItem(i, 1, QTableWidgetItem(codigo))
            tabla.setItem(i, 2, QTableWidgetItem(fecha))
            tabla.setItem(i, 3, QTableWidgetItem(str(cantidad)))
            tabla.setItem(i, 4, QTableWidgetItem(raza))
            tabla.setItem(i, 5, QTableWidgetItem(galpon))
        
        tabla.resizeColumnsToContents()
        layout.addWidget(tabla)
        
        # Añadir pestaña
        self.tab_widget.addTab(tab, "Lotes")
    
    def crear_tab_galpones(self):
        """Crea la pestaña de galpones"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        # Título
        titulo = QLabel("Gestión de Galpones")
        titulo.setFont(QFont("Arial", 16, QFont.Bold))
        layout.addWidget(titulo)
        
        # Tabla de galpones
        tabla = QTableWidget()
        tabla.setColumnCount(4)
        tabla.setHorizontalHeaderLabels(["ID", "Nombre", "Capacidad", "Estado"])
        
        # Datos de ejemplo
        datos = [
            (1, "Galpón A", 5000, "Ocupado"),
            (2, "Galpón B", 4500, "Ocupado"),
            (3, "Galpón C", 5000, "Ocupado")
        ]
        
        tabla.setRowCount(len(datos))
        for i, (id, nombre, capacidad, estado) in enumerate(datos):
            tabla.setItem(i, 0, QTableWidgetItem(str(id)))
            tabla.setItem(i, 1, QTableWidgetItem(nombre))
            tabla.setItem(i, 2, QTableWidgetItem(str(capacidad)))
            tabla.setItem(i, 3, QTableWidgetItem(estado))
        
        tabla.resizeColumnsToContents()
        layout.addWidget(tabla)
        
        # Añadir pestaña
        self.tab_widget.addTab(tab, "Galpones")
    
    def crear_tab_estadisticas(self):
        """Crea la pestaña de estadísticas"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        # Título
        titulo = QLabel("Estadísticas")
        titulo.setFont(QFont("Arial", 16, QFont.Bold))
        layout.addWidget(titulo)
        
        # Selector de galpón
        selector_layout = QHBoxLayout()
        selector_layout.addWidget(QLabel("Galpón:"))
        galpon_combo = QComboBox()
        galpon_combo.addItems(["Todos los galpones", "Galpón A", "Galpón B", "Galpón C"])
        selector_layout.addWidget(galpon_combo)
        selector_layout.addStretch()
        layout.addLayout(selector_layout)
        
        # Estadísticas de producción
        subtitulo1 = QLabel("Producción Diaria (últimos 7 días)")
        subtitulo1.setFont(QFont("Arial", 12, QFont.Bold))
        layout.addWidget(subtitulo1)
        
        # Tabla de producción
        tabla_prod = QTableWidget()
        tabla_prod.setColumnCount(2)
        tabla_prod.setHorizontalHeaderLabels(["Fecha", "Cantidad"])
        
        # Datos de ejemplo
        datos_prod = [
            ("2025-05-14", 2450),
            ("2025-05-15", 2480),
            ("2025-05-16", 2520),
            ("2025-05-17", 2490),
            ("2025-05-18", 2510),
            ("2025-05-19", 2530),
            ("2025-05-20", 2500)
        ]
        
        tabla_prod.setRowCount(len(datos_prod))
        for i, (fecha, cantidad) in enumerate(datos_prod):
            tabla_prod.setItem(i, 0, QTableWidgetItem(fecha))
            tabla_prod.setItem(i, 1, QTableWidgetItem(str(cantidad)))
        
        tabla_prod.resizeColumnsToContents()
        layout.addWidget(tabla_prod)
        
        # Añadir pestaña
        self.tab_widget.addTab(tab, "Estadísticas")
    
    def crear_tab_comparacion(self):
        """Crea la pestaña de comparación de razas"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        # Título
        titulo = QLabel("Comparación de Razas")
        titulo.setFont(QFont("Arial", 16, QFont.Bold))
        layout.addWidget(titulo)
        
        # Formulario de selección
        form_layout = QFormLayout()
        
        # Selector de raza 1
        raza1_combo = QComboBox()
        raza1_combo.addItems(["Leghorn Blanca", "Rhode Island Red", "Plymouth Rock"])
        form_layout.addRow("Raza 1:", raza1_combo)
        
        # Selector de raza 2
        raza2_combo = QComboBox()
        raza2_combo.addItems(["Rhode Island Red", "Leghorn Blanca", "Plymouth Rock"])
        form_layout.addRow("Raza 2:", raza2_combo)
        
        # Botón de comparar
        comparar_btn = QPushButton("Comparar")
        form_layout.addRow("", comparar_btn)
        
        layout.addLayout(form_layout)
        
        # Resultados de comparación
        subtitulo = QLabel("Resultados de Comparación")
        subtitulo.setFont(QFont("Arial", 12, QFont.Bold))
        layout.addWidget(subtitulo)
        
        # Tabla de comparación
        tabla_comp = QTableWidget()
        tabla_comp.setColumnCount(3)
        tabla_comp.setHorizontalHeaderLabels(["Métrica", "Leghorn Blanca", "Rhode Island Red"])
        
        # Datos de ejemplo
        datos_comp = [
            ("Producción esperada", "280", "260"),
            ("Producción actual", "265", "250"),
            ("Peso esperado (kg)", "1.8", "2.0"),
            ("Peso actual (kg)", "1.7", "1.9"),
            ("Mortalidad esperada (%)", "2.0", "2.5"),
            ("Mortalidad actual (%)", "2.5", "2.8")
        ]
        
        tabla_comp.setRowCount(len(datos_comp))
        for i, (metrica, valor1, valor2) in enumerate(datos_comp):
            tabla_comp.setItem(i, 0, QTableWidgetItem(metrica))
            tabla_comp.setItem(i, 1, QTableWidgetItem(valor1))
            tabla_comp.setItem(i, 2, QTableWidgetItem(valor2))
        
        tabla_comp.resizeColumnsToContents()
        layout.addWidget(tabla_comp)
        
        # Añadir pestaña
        self.tab_widget.addTab(tab, "Comparación")
    
    def crear_tarjeta(self, titulo, valor, color):
        """Crea una tarjeta de estadísticas"""
        card = QWidget()
        card.setStyleSheet(f"""
            QWidget {{
                background-color: white;
                border-left: 4px solid {color};
                border-radius: 4px;
                padding: 10px;
            }}
        """)
        
        layout = QVBoxLayout(card)
        
        # Título
        titulo_label = QLabel(titulo)
        titulo_label.setStyleSheet("color: #5a5c69; font-weight: bold; font-size: 12px;")
        layout.addWidget(titulo_label)
        
        # Valor
        valor_label = QLabel(valor)
        valor_label.setStyleSheet("color: #5a5c69; font-weight: bold; font-size: 20px;")
        layout.addWidget(valor_label)
        
        return card

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()

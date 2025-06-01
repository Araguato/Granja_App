#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                            QPushButton, QTableWidget, QTableWidgetItem, 
                            QMessageBox, QComboBox, QSpinBox, QProgressBar,
                            QGroupBox, QFormLayout, QCheckBox, QLineEdit,
                            QTextEdit, QTabWidget, QFrame, QSplitter)
from PyQt5.QtCore import Qt, QDateTime, pyqtSignal, QTimer
from PyQt5.QtGui import QIcon, QFont, QColor, QPixmap

from mobile_api import MobileAPIServer
import qrcode
import io
from PIL import Image

# Importar ImageQt con manejo de errores
try:
    from PIL.ImageQt import ImageQt
except ImportError:
    # Alternativa si ImageQt no está disponible
    from PyQt5.QtGui import QImage
    
    def ImageQt(img):
        """Convertir imagen PIL a QImage (alternativa a PIL.ImageQt)"""
        img = img.convert('RGBA')
        data = img.tobytes('raw', 'RGBA')
        qimg = QImage(data, img.size[0], img.size[1], QImage.Format_RGBA8888)
        return qimg

class MobileTab(QWidget):
    """Pestaña para gestionar la conexión con la aplicación móvil"""
    
    def __init__(self, api_client, sync_manager):
        super().__init__()
        self.api_client = api_client
        self.sync_manager = sync_manager
        
        # Crear servidor API para móviles
        self.mobile_server = MobileAPIServer(api_client, sync_manager)
        
        # Temporizador para actualizar estado
        self.status_timer = QTimer()
        self.status_timer.timeout.connect(self.update_status)
        self.status_timer.start(5000)  # Actualizar cada 5 segundos
        
        self.setup_ui()
        
    def setup_ui(self):
        """Configura la interfaz de usuario"""
        # Layout principal
        main_layout = QVBoxLayout()
        self.setLayout(main_layout)
        
        # Título
        title_label = QLabel("Conexión con Aplicación Móvil")
        title_label.setStyleSheet("font-size: 18px; font-weight: bold; margin-bottom: 10px;")
        main_layout.addWidget(title_label)
        
        # Descripción
        desc_label = QLabel("Esta pestaña permite gestionar la conexión entre la aplicación de Windows y la aplicación móvil.")
        desc_label.setWordWrap(True)
        main_layout.addWidget(desc_label)
        
        # Splitter para dividir la pantalla
        splitter = QSplitter(Qt.Horizontal)
        main_layout.addWidget(splitter)
        
        # Panel izquierdo - Servidor API
        left_panel = QWidget()
        left_layout = QVBoxLayout()
        left_panel.setLayout(left_layout)
        
        # Grupo de configuración del servidor
        server_group = QGroupBox("Servidor API para Móviles")
        server_layout = QFormLayout()
        server_group.setLayout(server_layout)
        
        # Host
        self.host_input = QLineEdit("localhost")
        server_layout.addRow("Host:", self.host_input)
        
        # Puerto
        self.port_input = QSpinBox()
        self.port_input.setMinimum(1024)
        self.port_input.setMaximum(65535)
        self.port_input.setValue(8080)
        server_layout.addRow("Puerto:", self.port_input)
        
        # SSL
        self.ssl_check = QCheckBox("Usar SSL (HTTPS)")
        server_layout.addRow("", self.ssl_check)
        
        # Botones de acción
        server_buttons_layout = QHBoxLayout()
        
        self.start_server_btn = QPushButton("Iniciar Servidor")
        self.start_server_btn.clicked.connect(self.on_start_server_clicked)
        server_buttons_layout.addWidget(self.start_server_btn)
        
        self.stop_server_btn = QPushButton("Detener Servidor")
        self.stop_server_btn.clicked.connect(self.on_stop_server_clicked)
        self.stop_server_btn.setEnabled(False)
        server_buttons_layout.addWidget(self.stop_server_btn)
        
        server_layout.addRow("", server_buttons_layout)
        
        # Estado del servidor
        self.server_status_label = QLabel("Estado: Detenido")
        server_layout.addRow("", self.server_status_label)
        
        left_layout.addWidget(server_group)
        
        # Grupo de conexión móvil
        mobile_group = QGroupBox("Conexión con Aplicación Móvil")
        mobile_layout = QVBoxLayout()
        mobile_group.setLayout(mobile_layout)
        
        # Instrucciones
        instructions_label = QLabel("Escanee el código QR con la aplicación móvil para conectarse:")
        instructions_label.setWordWrap(True)
        mobile_layout.addWidget(instructions_label)
        
        # Código QR
        self.qr_label = QLabel()
        self.qr_label.setAlignment(Qt.AlignCenter)
        self.qr_label.setMinimumSize(200, 200)
        mobile_layout.addWidget(self.qr_label)
        
        # URL de conexión
        self.url_label = QLabel("URL: -")
        self.url_label.setTextInteractionFlags(Qt.TextSelectableByMouse)
        mobile_layout.addWidget(self.url_label)
        
        # Botón para generar código QR
        self.generate_qr_btn = QPushButton("Generar Código QR")
        self.generate_qr_btn.clicked.connect(self.generate_qr_code)
        mobile_layout.addWidget(self.generate_qr_btn)
        
        left_layout.addWidget(mobile_group)
        
        # Panel derecho - Dispositivos conectados y logs
        right_panel = QWidget()
        right_layout = QVBoxLayout()
        right_panel.setLayout(right_layout)
        
        # Pestañas para dispositivos y logs
        tabs = QTabWidget()
        
        # Pestaña de dispositivos conectados
        devices_tab = QWidget()
        devices_layout = QVBoxLayout()
        devices_tab.setLayout(devices_layout)
        
        # Tabla de dispositivos
        self.devices_table = QTableWidget()
        self.devices_table.setColumnCount(4)
        self.devices_table.setHorizontalHeaderLabels(["Dispositivo", "IP", "Última Conexión", "Estado"])
        self.devices_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.devices_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.devices_table.horizontalHeader().setStretchLastSection(True)
        devices_layout.addWidget(self.devices_table)
        
        tabs.addTab(devices_tab, "Dispositivos Conectados")
        
        # Pestaña de logs
        logs_tab = QWidget()
        logs_layout = QVBoxLayout()
        logs_tab.setLayout(logs_layout)
        
        # Área de logs
        self.logs_text = QTextEdit()
        self.logs_text.setReadOnly(True)
        logs_layout.addWidget(self.logs_text)
        
        # Botón para limpiar logs
        self.clear_logs_btn = QPushButton("Limpiar Logs")
        self.clear_logs_btn.clicked.connect(self.clear_logs)
        logs_layout.addWidget(self.clear_logs_btn)
        
        tabs.addTab(logs_tab, "Logs")
        
        right_layout.addWidget(tabs)
        
        # Agregar paneles al splitter
        splitter.addWidget(left_panel)
        splitter.addWidget(right_panel)
        splitter.setSizes([400, 600])
        
        # Inicializar estado
        self.update_status()
        
    def on_start_server_clicked(self):
        """Maneja el clic en el botón de iniciar servidor"""
        host = self.host_input.text()
        port = self.port_input.value()
        use_ssl = self.ssl_check.isChecked()
        
        # Actualizar configuración del servidor
        self.mobile_server.host = host
        self.mobile_server.port = port
        self.mobile_server.use_ssl = use_ssl
        
        # Iniciar servidor
        success, message = self.mobile_server.start()
        
        if success:
            self.log(f"Servidor iniciado en {host}:{port}")
            self.start_server_btn.setEnabled(False)
            self.stop_server_btn.setEnabled(True)
            self.host_input.setEnabled(False)
            self.port_input.setEnabled(False)
            self.ssl_check.setEnabled(False)
            
            # Generar código QR
            self.generate_qr_code()
        else:
            self.log(f"Error al iniciar servidor: {message}")
            QMessageBox.warning(self, "Error", f"No se pudo iniciar el servidor: {message}")
        
        # Actualizar estado
        self.update_status()
    
    def on_stop_server_clicked(self):
        """Maneja el clic en el botón de detener servidor"""
        success, message = self.mobile_server.stop()
        
        if success:
            self.log("Servidor detenido")
            self.start_server_btn.setEnabled(True)
            self.stop_server_btn.setEnabled(False)
            self.host_input.setEnabled(True)
            self.port_input.setEnabled(True)
            self.ssl_check.setEnabled(True)
            
            # Limpiar código QR
            self.qr_label.clear()
            self.url_label.setText("URL: -")
        else:
            self.log(f"Error al detener servidor: {message}")
            QMessageBox.warning(self, "Error", f"No se pudo detener el servidor: {message}")
        
        # Actualizar estado
        self.update_status()
    
    def update_status(self):
        """Actualiza el estado del servidor"""
        status = self.mobile_server.get_status()
        
        if status['is_running']:
            self.server_status_label.setText(f"Estado: En ejecución ({status['host']}:{status['port']})")
            self.server_status_label.setStyleSheet("color: green;")
        else:
            self.server_status_label.setText("Estado: Detenido")
            self.server_status_label.setStyleSheet("color: red;")
    
    def generate_qr_code(self):
        """Genera un código QR con la URL de conexión"""
        if not self.mobile_server.is_running:
            QMessageBox.warning(self, "Error", "El servidor no está en ejecución")
            return
        
        # Obtener URL de conexión
        protocol = "https" if self.mobile_server.use_ssl else "http"
        host = self.mobile_server.host
        if host == "localhost" or host == "127.0.0.1":
            # Obtener IP local para que los dispositivos móviles puedan conectarse
            import socket
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                s.connect(("8.8.8.8", 80))
                host = s.getsockname()[0]
                s.close()
            except:
                pass
        
        port = self.mobile_server.port
        
        # Crear URL
        url = f"{protocol}://{host}:{port}/api/status"
        
        # Generar código QR
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(url)
        qr.make(fit=True)
        
        img = qr.make_image(fill_color="black", back_color="white")
        
        # Convertir a QPixmap
        buffer = io.BytesIO()
        img.save(buffer, format="PNG")
        buffer.seek(0)
        
        qimage = ImageQt(Image.open(buffer))
        pixmap = QPixmap.fromImage(qimage)
        
        # Mostrar código QR
        self.qr_label.setPixmap(pixmap.scaled(200, 200, Qt.KeepAspectRatio))
        self.url_label.setText(f"URL: {url}")
        
        self.log(f"Código QR generado para {url}")
    
    def log(self, message):
        """Agrega un mensaje al log"""
        timestamp = QDateTime.currentDateTime().toString("yyyy-MM-dd HH:mm:ss")
        self.logs_text.append(f"[{timestamp}] {message}")
    
    def clear_logs(self):
        """Limpia los logs"""
        self.logs_text.clear()

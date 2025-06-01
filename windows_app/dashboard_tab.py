from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                            QPushButton, QFrame, QGridLayout, QProgressBar)
from PyQt5.QtGui import QFont, QIcon, QPixmap
from PyQt5.QtCore import Qt, QTimer, QDate

class StatCard(QFrame):
    """Widget para mostrar una estadística en el dashboard"""
    
    def __init__(self, title, value, icon_name=None, color="#4e73df"):
        super().__init__()
        self.setObjectName("statCard")
        self.setStyleSheet(f"""
            #statCard {{
                background-color: white;
                border-left: 4px solid {color};
                border-radius: 4px;
                padding: 10px;
            }}
        """)
        
        # Crear layout
        layout = QHBoxLayout(self)
        
        # Contenido de la estadística
        content_layout = QVBoxLayout()
        
        # Título
        title_label = QLabel(title)
        title_label.setStyleSheet("color: #5a5c69; font-size: 12px;")
        content_layout.addWidget(title_label)
        
        # Valor
        value_label = QLabel(str(value))
        value_label.setStyleSheet("color: #5a5c69; font-size: 20px; font-weight: bold;")
        content_layout.addWidget(value_label)
        
        layout.addLayout(content_layout, 3)
        
        # Icono (si se proporciona)
        if icon_name:
            icon_label = QLabel()
            icon_path = f"icons/{icon_name}.png"
            try:
                pixmap = QPixmap(icon_path)
                icon_label.setPixmap(pixmap.scaled(48, 48, Qt.KeepAspectRatio, Qt.SmoothTransformation))
            except:
                # Si no se encuentra el icono, mostrar un texto
                icon_label.setText("📊")
                icon_label.setStyleSheet("color: #dddfeb; font-size: 24px;")
            
            icon_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
            layout.addWidget(icon_label, 1)

class DashboardTab(QWidget):
    """Pestaña de dashboard que muestra estadísticas generales"""
    
    def __init__(self, api_client):
        super().__init__()
        self.api_client = api_client
        
        # Crear layout principal
        layout = QVBoxLayout(self)
        
        # Encabezado con información de la empresa y granja
        header_frame = QFrame()
        header_frame.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 4px;
                padding: 15px;
            }
        """)
        header_layout = QVBoxLayout(header_frame)
        
        # Título principal con nombre de la empresa
        self.empresa_label = QLabel("Empresa: Cargando...")
        self.empresa_label.setStyleSheet("font-size: 24px; font-weight: bold; color: #5a5c69;")
        header_layout.addWidget(self.empresa_label)
        
        # Subtitulo con nombre de la granja
        self.granja_label = QLabel("Granja: Cargando...")
        self.granja_label.setStyleSheet("font-size: 18px; color: #4e73df; margin-bottom: 10px;")
        header_layout.addWidget(self.granja_label)
        
        # Información adicional
        info_layout = QHBoxLayout()
        
        # Fecha actual
        self.fecha_label = QLabel(f"Fecha: {QDate.currentDate().toString('dd/MM/yyyy')}")
        self.fecha_label.setStyleSheet("font-size: 14px; color: #858796;")
        info_layout.addWidget(self.fecha_label)
        
        # Usuario actual
        self.usuario_label = QLabel("Usuario: Cargando...")
        self.usuario_label.setStyleSheet("font-size: 14px; color: #858796;")
        info_layout.addWidget(self.usuario_label)
        
        # Estado de conexión
        self.conexion_label = QLabel("Estado: Conectado")
        self.conexion_label.setStyleSheet("font-size: 14px; color: #1cc88a;")
        info_layout.addWidget(self.conexion_label)
        
        header_layout.addLayout(info_layout)
        layout.addWidget(header_frame)
        
        # Título de la sección de estadísticas
        stats_title = QLabel("Estadísticas Generales")
        stats_title.setStyleSheet("font-size: 18px; font-weight: bold; color: #5a5c69; margin-top: 20px;")
        layout.addWidget(stats_title)
        
        # Tarjetas de estadísticas
        stats_layout = QGridLayout()
        
        # Crear tarjetas de estadísticas (inicialmente con valores de ejemplo)
        self.lotes_card = StatCard("Total Lotes", "0", "lotes", "#4e73df")
        self.aves_card = StatCard("Total Aves", "0", "aves", "#1cc88a")
        self.galpones_card = StatCard("Galpones", "0", "galpones", "#36b9cc")
        self.mortalidad_card = StatCard("Mortalidad", "0%", "mortalidad", "#f6c23e")
        
        # Agregar tarjetas al layout
        stats_layout.addWidget(self.lotes_card, 0, 0)
        stats_layout.addWidget(self.aves_card, 0, 1)
        stats_layout.addWidget(self.galpones_card, 1, 0)
        stats_layout.addWidget(self.mortalidad_card, 1, 1)
        
        layout.addLayout(stats_layout)
        
        # Botón de actualizar
        refresh_button = QPushButton("Actualizar")
        refresh_button.setStyleSheet("""
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
        refresh_button.clicked.connect(self.refresh_data)
        
        refresh_layout = QHBoxLayout()
        refresh_layout.addStretch()
        refresh_layout.addWidget(refresh_button)
        
        layout.addLayout(refresh_layout)
        
        # Espacio adicional
        layout.addStretch()
        
        # Cargar datos iniciales
        QTimer.singleShot(100, self.refresh_data)
    
    def refresh_data(self):
        """Actualiza los datos del dashboard"""
        # Obtener información del usuario actual
        user_info = self.api_client.get_current_user_info()
        
        # Actualizar información de empresa, granja y usuario
        if user_info:
            self.empresa_label.setText(f"Empresa: {user_info.get('empresa', 'No disponible')}")
            self.granja_label.setText(f"Granja: {user_info.get('granja', 'No disponible')}")
            self.usuario_label.setText(f"Usuario: {user_info.get('username', 'No disponible')}")
            
            # Actualizar estado de conexión
            if user_info.get('is_offline', False):
                self.conexion_label.setText("Estado: Sin conexión")
                self.conexion_label.setStyleSheet("font-size: 14px; color: #e74a3b;")
            else:
                self.conexion_label.setText("Estado: Conectado")
                self.conexion_label.setStyleSheet("font-size: 14px; color: #1cc88a;")
        else:
            # Si no hay información de usuario, mostrar datos genéricos
            self.empresa_label.setText("Empresa: App Granja")
            self.granja_label.setText("Granja: Modo Sin Conexión")
            self.usuario_label.setText("Usuario: Invitado")
            self.conexion_label.setText("Estado: Sin conexión")
            self.conexion_label.setStyleSheet("font-size: 14px; color: #e74a3b;")
        
        # Actualizar fecha
        self.fecha_label.setText(f"Fecha: {QDate.currentDate().toString('dd/MM/yyyy')}")
        
        # Obtener estadísticas generales
        success, data = self.api_client.get_dashboard_stats()
        
        if success:
            # Actualizar tarjetas con datos reales
            # Buscar los labels de valor dentro de cada tarjeta (el segundo label es el de valor)
            lotes_value_label = self.lotes_card.findChildren(QLabel)[1]
            aves_value_label = self.aves_card.findChildren(QLabel)[1]
            galpones_value_label = self.galpones_card.findChildren(QLabel)[1]
            mortalidad_value_label = self.mortalidad_card.findChildren(QLabel)[1]
            
            # Actualizar los valores
            lotes_value_label.setText(str(data.get('total_lotes', 0)))
            aves_value_label.setText(str(data.get('total_aves', 0)))
            galpones_value_label.setText(str(data.get('total_galpones', 0)))
            mortalidad_value_label.setText(f"{data.get('porcentaje_mortalidad', 0)}%")
        else:
            # Si hay un error, usar datos de ejemplo
            print(f"Error al obtener estadísticas: {data}")
            
            # Buscar los labels de valor dentro de cada tarjeta
            lotes_value_label = self.lotes_card.findChildren(QLabel)[1]
            aves_value_label = self.aves_card.findChildren(QLabel)[1]
            galpones_value_label = self.galpones_card.findChildren(QLabel)[1]
            mortalidad_value_label = self.mortalidad_card.findChildren(QLabel)[1]
            
            # Actualizar con datos de ejemplo
            lotes_value_label.setText("3")
            aves_value_label.setText("3,450")
            galpones_value_label.setText("5")
            mortalidad_value_label.setText("2.5%")

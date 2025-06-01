import sys
import os
import json
import requests
from datetime import datetime

from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                            QHBoxLayout, QLabel, QPushButton, QTableWidget, 
                            QTableWidgetItem, QMessageBox, QTabWidget, 
                            QLineEdit, QFormLayout, QComboBox, QSpinBox, 
                            QDoubleSpinBox, QDateEdit, QTextEdit, QGroupBox,
                            QDialog, QProgressBar, QFileDialog, QCheckBox,
                            QStatusBar, QToolBar, QAction, QMenu, QMenuBar,
                            QSystemTrayIcon)
from PyQt5.QtGui import QIcon, QPixmap, QFont, QColor
from PyQt5.QtCore import Qt, QSize, QDate, QThread, pyqtSignal

from api_client import ApiClient
from dashboard_tab import DashboardTab
from lotes_tab import LotesTab
from galpones_tab import GalponesTab
from alimentos_tab import AlimentosTab
from razas_tab import RazasTab
from vacunas_tab import VacunasTab
from backups_tab import BackupsTab
from estadisticas_tab import EstadisticasTab
from wiki_tab import WikiTab
from faq_tab import FaqTab
from bot_tab import BotTab
from calendario_tab import CalendarioTab
from config_tab import ConfigTab
from admin_tab import AdminTab
from seguimiento_tab import SeguimientoTab
from reportes_tab import ReportesTab
from tareas_tab import TareasTab
from sync_tab import SyncTab
from mobile_tab import MobileTab
from login_dialog import LoginDialog
from sync_manager import SyncManager

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("App Granja - Aplicación de Escritorio")
        self.setMinimumSize(1024, 768)
        
        # Inicializar variables
        self.login_attempts = 0
        self.user_info = None
        
        # Inicializar el cliente de API
        self.api_client = ApiClient()
        
        # Inicializar el gestor de sincronización
        self.sync_manager = SyncManager(self.api_client)
        
        # Configurar la interfaz de usuario
        self.setup_ui()
        
        # Verificar si hay un usuario con sesión activa
        self.user_info = self.api_client.get_current_user_info()
        
        # Siempre mostrar diálogo de login al iniciar, incluso si hay sesión guardada
        # Esto garantiza que solo usuarios autorizados puedan usar la aplicación
        self.show_login_dialog()
        
        # Si el diálogo de login se completó exitosamente, verificar conexión
        if self.user_info:
            # Verificar la conexión con el servidor
            self.check_server_connection()
            # Actualizar la interfaz con la información del usuario
            self.update_ui_with_user_info()
    
    def setup_ui(self):
        # Crear barra de menú
        self.setup_menu()
        
        # Crear barra de estado
        self.statusBar = QStatusBar()
        self.setStatusBar(self.statusBar)
        self.statusBar.showMessage("Bienvenido a App Granja")
        
        # Crear widget central con pestañas
        self.tab_widget = QTabWidget()
        
        # Crear pestañas
        self.dashboard_tab = DashboardTab(self.api_client)
        self.lotes_tab = LotesTab(self.api_client)
        self.galpones_tab = GalponesTab(self.api_client)
        self.alimentos_tab = AlimentosTab(self.api_client)
        self.razas_tab = RazasTab(self.api_client)
        self.vacunas_tab = VacunasTab(self.api_client)
        self.seguimiento_tab = SeguimientoTab(self.api_client)
        self.backups_tab = BackupsTab(self.api_client)
        self.estadisticas_tab = EstadisticasTab(self.api_client)
        self.wiki_tab = WikiTab(self.api_client)
        self.faq_tab = FaqTab(self.api_client)
        self.bot_tab = BotTab(self.api_client)
        self.calendario_tab = CalendarioTab(self.api_client)
        self.admin_tab = AdminTab(self.api_client)
        self.config_tab = ConfigTab(self.api_client)
        self.reportes_tab = ReportesTab(self.api_client)
        self.tareas_tab = TareasTab(self.api_client)
        self.sync_tab = SyncTab(self.api_client)
        self.mobile_tab = MobileTab(self.api_client, self.sync_manager)
        
        # Agregar pestañas al widget de pestañas
        self.tab_widget.addTab(self.dashboard_tab, "Dashboard")
        self.tab_widget.addTab(self.lotes_tab, "Lotes")
        self.tab_widget.addTab(self.galpones_tab, "Galpones")
        self.tab_widget.addTab(self.alimentos_tab, "Alimentos")
        self.tab_widget.addTab(self.razas_tab, "Razas")
        self.tab_widget.addTab(self.vacunas_tab, "Vacunas")
        self.tab_widget.addTab(self.seguimiento_tab, "Seguimiento")
        self.tab_widget.addTab(self.backups_tab, "Respaldos")
        self.tab_widget.addTab(self.estadisticas_tab, "Estadísticas")
        self.tab_widget.addTab(self.tareas_tab, "Tareas")
        self.tab_widget.addTab(self.wiki_tab, "Wiki")
        self.tab_widget.addTab(self.faq_tab, "FAQ")
        self.tab_widget.addTab(self.bot_tab, "Asistente")
        self.tab_widget.addTab(self.calendario_tab, "Calendario")
        self.tab_widget.addTab(self.admin_tab, "Administración")
        self.tab_widget.addTab(self.config_tab, "Configuración")
        self.tab_widget.addTab(self.reportes_tab, "Reportes")
        self.tab_widget.addTab(self.sync_tab, "Sincronización")
        self.tab_widget.addTab(self.mobile_tab, "App Móvil")
        
        
        # Establecer el widget central
        self.setCentralWidget(self.tab_widget)
    
    def setup_menu(self):
        # Crear barra de menú
        menubar = self.menuBar()
        
        # Menú Archivo
        file_menu = menubar.addMenu("Archivo")
        
        # Acción Configuración
        config_action = QAction("Configuración", self)
        config_action.triggered.connect(self.show_config)
        file_menu.addAction(config_action)
        
        # Menú Usuario
        self.user_menu = menubar.addMenu("Usuario")
        
        # Acción Iniciar Sesión
        self.login_action = QAction("Iniciar Sesión", self)
        self.login_action.triggered.connect(self.show_login_dialog)
        self.user_menu.addAction(self.login_action)
        
        # Acción Cerrar Sesión
        self.logout_action = QAction("Cerrar Sesión", self)
        self.logout_action.triggered.connect(self.logout)
        self.user_menu.addAction(self.logout_action)
        
        # Actualizar menú de usuario según estado de sesión
        self.update_user_menu()
        
        # Acción Salir
        exit_action = QAction("Salir", self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # Menú Ayuda
        help_menu = menubar.addMenu("Ayuda")
        
        # Acción Acerca de
        about_action = QAction("Acerca de", self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)
    
    def check_server_connection(self):
        """Verifica la conexión con el servidor"""
        try:
            response = self.api_client.test_connection()
            if response:
                self.statusBar.showMessage("Conectado al servidor")
                return True
            else:
                self.statusBar.showMessage("No se pudo conectar al servidor - Usando datos de ejemplo")
                QMessageBox.warning(self, "Modo sin conexión", 
                                   "No se pudo conectar al servidor. La aplicación funcionará con datos de ejemplo.\n\n"
                                   "Para usar datos reales, asegúrese de que el servidor Django esté en funcionamiento.")
                return False
        except Exception as e:
            self.statusBar.showMessage(f"Error de conexión: {str(e)} - Usando datos de ejemplo")
            QMessageBox.warning(self, "Modo sin conexión", 
                               f"Error de conexión: {str(e)}\n\n"
                               "La aplicación funcionará con datos de ejemplo.\n\n"
                               "Para usar datos reales, asegúrese de que el servidor Django esté en funcionamiento.")
            return False
    
    def show_config(self):
        """Muestra la pestaña de configuración"""
        self.tab_widget.setCurrentWidget(self.config_tab)
    
    def show_about(self):
        """Muestra el diálogo Acerca de"""
        QMessageBox.about(self, "Acerca de App Granja", 
                         "App Granja - Aplicación de Escritorio\n"
                         "Versión 1.0\n\n"
                         "© 2025 App Granja")
    
    def show_login_dialog(self):
        """Muestra el diálogo de inicio de sesión"""
        dialog = LoginDialog(self.api_client, self)
        dialog.login_successful.connect(self.on_login_successful)
        result = dialog.exec_()
        
        # Si el usuario cierra el diálogo sin iniciar sesión y no hay sesión activa
        if result != QDialog.Accepted and not self.user_info:
            # Verificar si es la primera vez que se muestra el diálogo
            if not hasattr(self, 'login_attempts'):
                self.login_attempts = 0
            
            self.login_attempts += 1
            
            # Si es el primer intento, mostrar advertencia y volver a intentar
            if self.login_attempts < 2:
                QMessageBox.warning(self, "Sesión requerida", "Se requiere iniciar sesión para usar la aplicación.")
                self.show_login_dialog()
            else:
                # Si es el segundo intento fallido, cerrar la aplicación
                QMessageBox.critical(self, "Sesión requerida", "No se ha iniciado sesión. La aplicación se cerrará.")
                self.close()
    
    def on_login_successful(self, user_info):
        """Maneja el evento de inicio de sesión exitoso"""
        self.user_info = user_info
        self.update_ui_with_user_info()
        self.update_user_menu()
        
        # Mostrar mensaje de bienvenida
        self.statusBar.showMessage(f"Bienvenido, {user_info.get('username', 'Usuario')}")
        
        # Actualizar datos del dashboard
        if hasattr(self, 'dashboard_tab'):
            self.dashboard_tab.refresh_data()
    
    def logout(self):
        """Cierra la sesión del usuario actual"""
        success, message = self.api_client.logout()
        
        if success:
            # Actualizar estado de la aplicación
            self.user_info = None
            
            # Actualizar interfaz de usuario
            self.update_user_menu()
            self.update_ui_with_user_info()
            
            # Actualizar dashboard
            if hasattr(self, 'dashboard_tab'):
                self.dashboard_tab.refresh_data()
            
            # Mostrar mensaje de cierre de sesión
            self.statusBar.showMessage("Sesión cerrada correctamente")
            
            # Informar al usuario
            QMessageBox.information(self, "Cierre de sesión", "La sesión se ha cerrado correctamente.")
            
            # Forzar inicio de sesión y bloquear la aplicación hasta que se inicie sesión
            dialog = LoginDialog(self.api_client, self)
            dialog.login_successful.connect(self.on_login_successful)
            result = dialog.exec_()
            
            # Si el usuario cierra el diálogo sin iniciar sesión, cerrar la aplicación
            if result != QDialog.Accepted:
                QMessageBox.warning(self, "Sesión requerida", "Se requiere iniciar sesión para usar la aplicación.")
                self.close()
        else:
            QMessageBox.warning(self, "Error", f"Error al cerrar sesión: {message}")
    
    def update_user_menu(self):
        """Actualiza el menú de usuario según el estado de la sesión"""
        if self.user_info:
            # Usuario con sesión activa
            self.login_action.setVisible(False)
            self.logout_action.setVisible(True)
            self.user_menu.setTitle(f"Usuario: {self.user_info.get('username', 'Usuario')}")
        else:
            # Sin sesión activa
            self.login_action.setVisible(True)
            self.logout_action.setVisible(False)
            self.user_menu.setTitle("Usuario")
    
    def update_ui_with_user_info(self):
        """Actualiza la interfaz con la información del usuario"""
        if self.user_info:
            # Actualizar título de la ventana
            empresa = self.user_info.get('empresa', 'App Granja')
            granja = self.user_info.get('granja', '')
            self.setWindowTitle(f"App Granja - {empresa} - {granja}")
            
            # Actualizar barra de estado
            if self.user_info.get('is_offline', False):
                self.statusBar.showMessage(f"Modo sin conexión - Usuario: {self.user_info.get('username', 'Invitado')}")
            else:
                self.statusBar.showMessage(f"Conectado - Usuario: {self.user_info.get('username', 'Usuario')}")
            
            # Actualizar dashboard
            if hasattr(self, 'dashboard_tab'):
                self.dashboard_tab.refresh_data()
        else:
            # Restaurar título por defecto
            self.setWindowTitle("App Granja - Aplicación de Escritorio")
            self.statusBar.showMessage("Sin sesión activa")

def main():
    app = QApplication(sys.argv)
    app.setStyle("Fusion")  # Estilo moderno
    
    # Establecer hoja de estilo
    try:
        with open(os.path.join(os.path.dirname(__file__), "style.css"), "r") as f:
            app.setStyleSheet(f.read())
    except Exception as e:
        print(f"Error al cargar hoja de estilo: {str(e)}")
    
    # Verificar si se solicitó el modo offline
    offline_mode = "--offline" in sys.argv
    if offline_mode:
        print("=== Iniciando en modo offline ===")
        
        # Crear/actualizar archivo de configuración para forzar modo offline
        config_path = os.path.join(os.path.dirname(__file__), "config.json")
        try:
            # Leer configuración existente si existe
            if os.path.exists(config_path):
                with open(config_path, "r") as f:
                    config = json.load(f)
            else:
                config = {}
            
            # Forzar modo offline
            config["is_offline"] = True
            
            # Asegurar que hay credenciales por defecto
            if "username" not in config:
                config["username"] = "admin"
            if "password" not in config:
                config["password"] = "admin123"
            
            # Guardar configuración
            with open(config_path, "w") as f:
                json.dump(config, f, indent=4)
                
            print("Configuración de modo offline guardada correctamente")
        except Exception as e:
            print(f"Error al configurar modo offline: {str(e)}")
    
    window = MainWindow()
    
    # Si estamos en modo offline, forzar el modo offline en el cliente API
    if offline_mode:
        window.api_client.is_offline = True
        print("Modo offline activado en ApiClient")
    
    window.show()
    
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()

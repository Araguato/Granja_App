import sys
import os
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QLabel, QPushButton
from PyQt6.QtCore import Qt
from dotenv import load_dotenv

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("App Granja - Windows Client")
        self.setGeometry(100, 100, 800, 600)
        
        # Load environment variables
        load_dotenv()
        
        # Set up the main widget and layout
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QVBoxLayout(main_widget)
        
        # Add a title label
        title_label = QLabel("Bienvenido a App Granja")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet("font-size: 24px; font-weight: bold; margin: 20px;")
        layout.addWidget(title_label)
        
        # Add a status label
        self.status_label = QLabel("Estado: Conectando...")
        layout.addWidget(self.status_label)
        
        # Add a test button
        test_button = QPushButton("Probar Conexión")
        test_button.clicked.connect(self.test_connection)
        layout.addWidget(test_button)
        
        # Add stretch to push content to the top
        layout.addStretch()
        
    def test_connection(self):
        # Test database connection
        try:
            # TODO: Add actual database connection test
            self.status_label.setText("Estado: Conexión exitosa")
        except Exception as e:
            self.status_label.setText(f"Error de conexión: {str(e)}")

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()

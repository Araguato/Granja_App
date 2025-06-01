import os
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                           QPushButton, QTableWidget, QTableWidgetItem,
                           QDialog, QFormLayout, QLineEdit, QTextEdit,
                           QMessageBox, QComboBox, QListWidget, QListWidgetItem,
                           QSplitter, QHeaderView, QStyle)
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QFont

class CreateFaqDialog(QDialog):
    """Diálogo para crear una nueva pregunta frecuente"""
    
    def __init__(self, parent=None, categorias=None):
        super().__init__(parent)
        self.setWindowTitle("Crear Nueva Pregunta Frecuente")
        self.setMinimumWidth(600)
        self.setMinimumHeight(400)
        
        # Crear layout
        layout = QVBoxLayout(self)
        
        # Formulario
        form_layout = QFormLayout()
        
        # Pregunta
        self.pregunta_input = QLineEdit()
        form_layout.addRow("Pregunta:", self.pregunta_input)
        
        # Categoría
        self.categoria_combo = QComboBox()
        if categorias:
            for categoria in categorias:
                self.categoria_combo.addItem(categoria.get('nombre', ''), categoria.get('id'))
        form_layout.addRow("Categoría:", self.categoria_combo)
        
        layout.addLayout(form_layout)
        
        # Respuesta
        respuesta_label = QLabel("Respuesta:")
        layout.addWidget(respuesta_label)
        
        self.respuesta_input = QTextEdit()
        self.respuesta_input.setMinimumHeight(200)
        layout.addWidget(self.respuesta_input)
        
        # Botones
        button_layout = QHBoxLayout()
        
        self.cancel_button = QPushButton("Cancelar")
        self.cancel_button.clicked.connect(self.reject)
        
        self.save_button = QPushButton("Guardar")
        self.save_button.setStyleSheet("""
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
        self.save_button.clicked.connect(self.accept)
        
        button_layout.addWidget(self.cancel_button)
        button_layout.addWidget(self.save_button)
        
        layout.addLayout(button_layout)
    
    def get_data(self):
        """Obtiene los datos del formulario"""
        return {
            'pregunta': self.pregunta_input.text(),
            'categoria_id': self.categoria_combo.currentData(),
            'categoria_nombre': self.categoria_combo.currentText(),
            'respuesta': self.respuesta_input.toPlainText()
        }

class EditFaqDialog(CreateFaqDialog):
    """Diálogo para editar una pregunta frecuente existente"""
    
    def __init__(self, parent=None, categorias=None, faq_data=None):
        super().__init__(parent, categorias)
        self.setWindowTitle("Editar Pregunta Frecuente")
        
        # Llenar el formulario con los datos de la FAQ
        if faq_data:
            self.pregunta_input.setText(faq_data.get('pregunta', ''))
            
            categoria_id = faq_data.get('categoria_id')
            if categoria_id:
                categoria_index = self.categoria_combo.findData(categoria_id)
                if categoria_index >= 0:
                    self.categoria_combo.setCurrentIndex(categoria_index)
            
            self.respuesta_input.setPlainText(faq_data.get('respuesta', ''))

class FaqTab(QWidget):
    """Pestaña para gestionar las preguntas frecuentes"""
    
    def __init__(self, api_client):
        super().__init__()
        self.api_client = api_client
        
        # Crear layout principal
        layout = QVBoxLayout(self)
        
        # Título
        title_label = QLabel("Preguntas Frecuentes")
        title_label.setStyleSheet("font-size: 24px; font-weight: bold; color: #5a5c69;")
        layout.addWidget(title_label)
        
        # Descripción
        desc_label = QLabel("Gestión de preguntas y respuestas frecuentes")
        desc_label.setStyleSheet("font-size: 14px; color: #858796; margin-bottom: 20px;")
        layout.addWidget(desc_label)
        
        # Botones de acción
        action_layout = QHBoxLayout()
        
        self.new_button = QPushButton("Nueva Pregunta")
        self.new_button.setStyleSheet("""
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
        self.new_button.clicked.connect(self.create_faq)
        
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
        
        action_layout.addWidget(self.new_button)
        action_layout.addWidget(self.refresh_button)
        action_layout.addStretch()
        
        layout.addLayout(action_layout)
        
        # Crear splitter para dividir la vista
        splitter = QSplitter(Qt.Horizontal)
        
        # Lista de preguntas
        self.list_widget = QListWidget()
        self.list_widget.setMinimumWidth(300)
        self.list_widget.currentItemChanged.connect(self.on_item_changed)
        
        # Panel de visualización
        self.content_widget = QWidget()
        content_layout = QVBoxLayout(self.content_widget)
        
        self.pregunta_label = QLabel()
        self.pregunta_label.setStyleSheet("font-size: 18px; font-weight: bold; color: #5a5c69;")
        self.pregunta_label.setWordWrap(True)
        content_layout.addWidget(self.pregunta_label)
        
        self.categoria_label = QLabel()
        self.categoria_label.setStyleSheet("font-size: 14px; color: #858796;")
        content_layout.addWidget(self.categoria_label)
        
        self.respuesta_text = QTextEdit()
        self.respuesta_text.setReadOnly(True)
        content_layout.addWidget(self.respuesta_text)
        
        # Botones de acción para la FAQ
        faq_actions = QHBoxLayout()
        
        self.edit_button = QPushButton("Editar")
        self.edit_button.setIcon(self.style().standardIcon(QStyle.SP_FileDialogDetailedView))
        self.edit_button.clicked.connect(self.edit_current_faq)
        
        self.delete_button = QPushButton("Eliminar")
        self.delete_button.setIcon(self.style().standardIcon(QStyle.SP_TrashIcon))
        self.delete_button.clicked.connect(self.delete_current_faq)
        
        faq_actions.addWidget(self.edit_button)
        faq_actions.addWidget(self.delete_button)
        faq_actions.addStretch()
        
        content_layout.addLayout(faq_actions)
        
        # Agregar widgets al splitter
        splitter.addWidget(self.list_widget)
        splitter.addWidget(self.content_widget)
        
        # Establecer proporciones del splitter
        splitter.setSizes([300, 700])
        
        layout.addWidget(splitter)
        
        # Inicializar variables
        self.current_faq_id = None
        
        # Cargar datos iniciales
        self.refresh_data()
    
    def refresh_data(self):
        """Actualiza los datos de las preguntas frecuentes"""
        # En una aplicación real, estos datos vendrían de la API
        # Aquí usamos datos de ejemplo
        faqs = [
            {
                'id': 1,
                'pregunta': '¿Cuál es la temperatura óptima para pollitas de 1 semana?',
                'respuesta': 'La temperatura óptima para pollitas de 1 semana de edad es de 32-33°C. Es importante mantener esta temperatura constante y monitorearla regularmente para asegurar el bienestar de las aves.',
                'categoria_id': 1,
                'categoria_nombre': 'Manejo de Aves'
            },
            {
                'id': 2,
                'pregunta': '¿Cuándo debo aplicar la vacuna contra Newcastle?',
                'respuesta': 'La vacuna contra Newcastle debe aplicarse según el siguiente esquema:\n\n- Primera dosis: 7-10 días de edad\n- Segunda dosis: 21-24 días de edad\n- Refuerzo: Cada 3-4 meses\n\nConsulte con su veterinario para ajustar el programa según las condiciones específicas de su granja.',
                'categoria_id': 2,
                'categoria_nombre': 'Sanidad'
            },
            {
                'id': 3,
                'pregunta': '¿Cómo puedo mejorar la producción de huevos?',
                'respuesta': 'Para mejorar la producción de huevos, considere los siguientes factores:\n\n1. Nutrición adecuada con niveles correctos de proteína y calcio\n2. Programa de iluminación óptimo (16 horas de luz)\n3. Control de temperatura (18-24°C)\n4. Manejo adecuado del estrés\n5. Programa de vacunación completo\n6. Calidad del agua\n7. Densidad de población adecuada',
                'categoria_id': 3,
                'categoria_nombre': 'Producción'
            },
            {
                'id': 4,
                'pregunta': '¿Qué hacer ante un brote de canibalismo?',
                'respuesta': 'Ante un brote de canibalismo:\n\n1. Reduzca la intensidad de la luz\n2. Identifique y separe las aves agresoras\n3. Verifique la densidad de población\n4. Asegure suficientes comederos y bebederos\n5. Revise la dieta (posible deficiencia de sal o proteína)\n6. Considere el uso de bloques de picoteo\n7. Consulte con su veterinario sobre posibles soluciones adicionales',
                'categoria_id': 1,
                'categoria_nombre': 'Manejo de Aves'
            }
        ]
        
        # Limpiar lista
        self.list_widget.clear()
        
        # Llenar lista con preguntas
        for faq in faqs:
            item = QListWidgetItem(faq.get('pregunta', ''))
            item.setData(Qt.UserRole, faq)
            self.list_widget.addItem(item)
        
        # Limpiar panel de visualización
        self.pregunta_label.setText("")
        self.categoria_label.setText("")
        self.respuesta_text.setText("")
        self.current_faq_id = None
        
        # Deshabilitar botones de acción
        self.edit_button.setEnabled(False)
        self.delete_button.setEnabled(False)
    
    def on_item_changed(self, current, previous):
        """Maneja el cambio de selección en la lista"""
        if not current:
            # Limpiar panel de visualización
            self.pregunta_label.setText("")
            self.categoria_label.setText("")
            self.respuesta_text.setText("")
            self.current_faq_id = None
            
            # Deshabilitar botones de acción
            self.edit_button.setEnabled(False)
            self.delete_button.setEnabled(False)
            return
        
        # Obtener datos de la pregunta seleccionada
        faq_data = current.data(Qt.UserRole)
        
        # Mostrar datos en el panel de visualización
        self.pregunta_label.setText(faq_data.get('pregunta', ''))
        self.categoria_label.setText(f"Categoría: {faq_data.get('categoria_nombre', '')}")
        self.respuesta_text.setText(faq_data.get('respuesta', ''))
        self.current_faq_id = faq_data.get('id')
        
        # Habilitar botones de acción
        self.edit_button.setEnabled(True)
        self.delete_button.setEnabled(True)
    
    def get_categorias(self):
        """Obtiene la lista de categorías"""
        # En una aplicación real, estos datos vendrían de la API
        # Aquí usamos datos de ejemplo
        return [
            {
                'id': 1,
                'nombre': 'Manejo de Aves'
            },
            {
                'id': 2,
                'nombre': 'Sanidad'
            },
            {
                'id': 3,
                'nombre': 'Producción'
            }
        ]
    
    def get_faq_by_id(self, faq_id):
        """Obtiene una pregunta frecuente por su ID"""
        # En una aplicación real, estos datos vendrían de la API
        # Aquí buscamos en la lista
        for i in range(self.list_widget.count()):
            item = self.list_widget.item(i)
            data = item.data(Qt.UserRole)
            if data and data.get('id') == faq_id:
                return data
        return None
    
    def create_faq(self):
        """Abre el diálogo para crear una nueva pregunta frecuente"""
        categorias = self.get_categorias()
        dialog = CreateFaqDialog(self, categorias)
        
        if dialog.exec_() == QDialog.Accepted:
            # Obtener datos del formulario
            faq_data = dialog.get_data()
            
            # En una aplicación real, aquí se enviarían los datos a la API
            QMessageBox.information(self, "Información", 
                                   "Pregunta frecuente creada correctamente.")
            
            # Actualizar lista
            self.refresh_data()
    
    def edit_current_faq(self):
        """Edita la pregunta frecuente actualmente seleccionada"""
        if not self.current_faq_id:
            QMessageBox.warning(self, "Advertencia", "No hay ninguna pregunta seleccionada.")
            return
        
        faq_data = self.get_faq_by_id(self.current_faq_id)
        if not faq_data:
            QMessageBox.warning(self, "Advertencia", "No se encontró la pregunta seleccionada.")
            return
        
        categorias = self.get_categorias()
        dialog = EditFaqDialog(self, categorias, faq_data)
        
        if dialog.exec_() == QDialog.Accepted:
            # Obtener datos del formulario
            updated_data = dialog.get_data()
            
            # En una aplicación real, aquí se enviarían los datos a la API
            QMessageBox.information(self, "Información", 
                                   "Pregunta frecuente actualizada correctamente.")
            
            # Actualizar lista y panel de visualización
            self.refresh_data()
    
    def delete_current_faq(self):
        """Elimina la pregunta frecuente actualmente seleccionada"""
        if not self.current_faq_id:
            QMessageBox.warning(self, "Advertencia", "No hay ninguna pregunta seleccionada.")
            return
        
        reply = QMessageBox.question(
            self, 'Confirmar Eliminación',
            '¿Está seguro de que desea eliminar esta pregunta frecuente?',
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            # En una aplicación real, aquí se enviaría la solicitud de eliminación a la API
            QMessageBox.information(self, "Información", 
                                   "Pregunta frecuente eliminada correctamente.")
            
            # Actualizar lista y panel de visualización
            self.refresh_data()

import os
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                           QPushButton, QTableWidget, QTableWidgetItem,
                           QDialog, QFormLayout, QLineEdit, QTextEdit,
                           QMessageBox, QComboBox, QTreeWidget, QTreeWidgetItem,
                           QSplitter, QHeaderView, QStyle)
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QFont

class CreateArticuloDialog(QDialog):
    """Diálogo para crear un nuevo artículo de wiki"""
    
    def __init__(self, parent=None, categorias=None):
        super().__init__(parent)
        self.setWindowTitle("Crear Nuevo Artículo")
        self.setMinimumWidth(600)
        self.setMinimumHeight(500)
        
        # Crear layout
        layout = QVBoxLayout(self)
        
        # Formulario
        form_layout = QFormLayout()
        
        # Título
        self.titulo_input = QLineEdit()
        form_layout.addRow("Título:", self.titulo_input)
        
        # Categoría
        self.categoria_combo = QComboBox()
        if categorias:
            for categoria in categorias:
                self.categoria_combo.addItem(categoria.get('nombre', ''), categoria.get('id'))
        form_layout.addRow("Categoría:", self.categoria_combo)
        
        # Resumen
        self.resumen_input = QLineEdit()
        form_layout.addRow("Resumen:", self.resumen_input)
        
        layout.addLayout(form_layout)
        
        # Contenido
        contenido_label = QLabel("Contenido:")
        layout.addWidget(contenido_label)
        
        self.contenido_input = QTextEdit()
        self.contenido_input.setMinimumHeight(300)
        layout.addWidget(self.contenido_input)
        
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
            'titulo': self.titulo_input.text(),
            'categoria_id': self.categoria_combo.currentData(),
            'categoria_nombre': self.categoria_combo.currentText(),
            'resumen': self.resumen_input.text(),
            'contenido': self.contenido_input.toPlainText()
        }

class EditArticuloDialog(CreateArticuloDialog):
    """Diálogo para editar un artículo existente"""
    
    def __init__(self, parent=None, categorias=None, articulo_data=None):
        super().__init__(parent, categorias)
        self.setWindowTitle("Editar Artículo")
        
        # Llenar el formulario con los datos del artículo
        if articulo_data:
            self.titulo_input.setText(articulo_data.get('titulo', ''))
            
            categoria_id = articulo_data.get('categoria_id')
            if categoria_id:
                categoria_index = self.categoria_combo.findData(categoria_id)
                if categoria_index >= 0:
                    self.categoria_combo.setCurrentIndex(categoria_index)
            
            self.resumen_input.setText(articulo_data.get('resumen', ''))
            self.contenido_input.setPlainText(articulo_data.get('contenido', ''))

class WikiTab(QWidget):
    """Pestaña para gestionar la wiki"""
    
    def __init__(self, api_client):
        super().__init__()
        self.api_client = api_client
        
        # Crear layout principal
        layout = QVBoxLayout(self)
        
        # Título
        title_label = QLabel("Wiki del Sistema")
        title_label.setStyleSheet("font-size: 24px; font-weight: bold; color: #5a5c69;")
        layout.addWidget(title_label)
        
        # Descripción
        desc_label = QLabel("Base de conocimiento y documentación del sistema")
        desc_label.setStyleSheet("font-size: 14px; color: #858796; margin-bottom: 20px;")
        layout.addWidget(desc_label)
        
        # Botones de acción
        action_layout = QHBoxLayout()
        
        self.new_button = QPushButton("Nuevo Artículo")
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
        self.new_button.clicked.connect(self.create_articulo)
        
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
        
        # Árbol de categorías y artículos
        self.tree = QTreeWidget()
        self.tree.setHeaderLabels(["Wiki"])
        self.tree.setMinimumWidth(250)
        self.tree.itemClicked.connect(self.on_tree_item_clicked)
        
        # Panel de visualización
        self.content_widget = QWidget()
        content_layout = QVBoxLayout(self.content_widget)
        
        self.titulo_label = QLabel()
        self.titulo_label.setStyleSheet("font-size: 20px; font-weight: bold; color: #5a5c69;")
        content_layout.addWidget(self.titulo_label)
        
        self.categoria_label = QLabel()
        self.categoria_label.setStyleSheet("font-size: 14px; color: #858796;")
        content_layout.addWidget(self.categoria_label)
        
        self.resumen_label = QLabel()
        self.resumen_label.setStyleSheet("font-size: 16px; font-style: italic; margin-top: 10px; margin-bottom: 20px;")
        self.resumen_label.setWordWrap(True)
        content_layout.addWidget(self.resumen_label)
        
        self.contenido_text = QTextEdit()
        self.contenido_text.setReadOnly(True)
        content_layout.addWidget(self.contenido_text)
        
        # Botones de acción para el artículo
        article_actions = QHBoxLayout()
        
        self.edit_button = QPushButton("Editar")
        self.edit_button.setIcon(self.style().standardIcon(QStyle.SP_FileDialogDetailedView))
        self.edit_button.clicked.connect(self.edit_current_articulo)
        
        self.delete_button = QPushButton("Eliminar")
        self.delete_button.setIcon(self.style().standardIcon(QStyle.SP_TrashIcon))
        self.delete_button.clicked.connect(self.delete_current_articulo)
        
        article_actions.addWidget(self.edit_button)
        article_actions.addWidget(self.delete_button)
        article_actions.addStretch()
        
        content_layout.addLayout(article_actions)
        
        # Agregar widgets al splitter
        splitter.addWidget(self.tree)
        splitter.addWidget(self.content_widget)
        
        # Establecer proporciones del splitter
        splitter.setSizes([250, 750])
        
        layout.addWidget(splitter)
        
        # Inicializar variables
        self.current_articulo_id = None
        
        # Cargar datos iniciales
        self.refresh_data()
    
    def refresh_data(self):
        """Actualiza los datos de la wiki"""
        # En una aplicación real, estos datos vendrían de la API
        # Aquí usamos datos de ejemplo
        categorias = [
            {
                'id': 1,
                'nombre': 'Manejo de Aves',
                'articulos': [
                    {
                        'id': 1,
                        'titulo': 'Guía de Alimentación',
                        'resumen': 'Recomendaciones para la alimentación de aves en diferentes etapas.',
                        'contenido': """# Guía de Alimentación para Aves

## Introducción
Una alimentación adecuada es fundamental para el desarrollo y la producción de las aves. Este artículo proporciona recomendaciones específicas para cada etapa de crecimiento.

## Etapa de Inicio (0-6 semanas)
- Proteína recomendada: 20-22%
- Energía metabolizable: 2900-3000 kcal/kg
- Alimentación: Ad libitum
- Consumo diario aproximado: 30-40g por ave

## Etapa de Crecimiento (7-14 semanas)
- Proteína recomendada: 16-18%
- Energía metabolizable: 2800-2900 kcal/kg
- Alimentación: Controlada para evitar sobrepeso
- Consumo diario aproximado: 60-70g por ave

## Etapa de Postura (15+ semanas)
- Proteína recomendada: 16-17%
- Energía metabolizable: 2700-2800 kcal/kg
- Calcio: 3.5-4.0%
- Alimentación: Ad libitum
- Consumo diario aproximado: 100-120g por ave

## Recomendaciones Generales
- Proporcionar agua limpia y fresca en todo momento
- Mantener los comederos limpios y con alimento fresco
- Ajustar la alimentación según la temporada y condiciones climáticas
- Monitorear el consumo diario y ajustar según sea necesario
"""
                    },
                    {
                        'id': 2,
                        'titulo': 'Control de Temperatura',
                        'resumen': 'Parámetros óptimos de temperatura para diferentes etapas de crecimiento.',
                        'contenido': 'Contenido detallado sobre control de temperatura...'
                    }
                ]
            },
            {
                'id': 2,
                'nombre': 'Sanidad',
                'articulos': [
                    {
                        'id': 3,
                        'titulo': 'Programa de Vacunación',
                        'resumen': 'Calendario recomendado de vacunación para ponedoras comerciales.',
                        'contenido': 'Contenido detallado sobre programa de vacunación...'
                    },
                    {
                        'id': 4,
                        'titulo': 'Bioseguridad',
                        'resumen': 'Medidas de bioseguridad para prevenir enfermedades en la granja.',
                        'contenido': 'Contenido detallado sobre bioseguridad...'
                    }
                ]
            },
            {
                'id': 3,
                'nombre': 'Producción',
                'articulos': [
                    {
                        'id': 5,
                        'titulo': 'Manejo de Registros',
                        'resumen': 'Guía para el correcto registro y análisis de datos de producción.',
                        'contenido': 'Contenido detallado sobre manejo de registros...'
                    }
                ]
            }
        ]
        
        # Limpiar árbol
        self.tree.clear()
        
        # Llenar árbol con categorías y artículos
        for categoria in categorias:
            # Crear ítem de categoría
            categoria_item = QTreeWidgetItem(self.tree)
            categoria_item.setText(0, categoria.get('nombre', ''))
            categoria_item.setData(0, Qt.UserRole, {'tipo': 'categoria', 'id': categoria.get('id')})
            font = QFont()
            font.setBold(True)
            categoria_item.setFont(0, font)
            
            # Agregar artículos a la categoría
            for articulo in categoria.get('articulos', []):
                articulo_item = QTreeWidgetItem(categoria_item)
                articulo_item.setText(0, articulo.get('titulo', ''))
                articulo_item.setData(0, Qt.UserRole, {
                    'tipo': 'articulo',
                    'id': articulo.get('id'),
                    'titulo': articulo.get('titulo', ''),
                    'categoria_id': categoria.get('id'),
                    'categoria_nombre': categoria.get('nombre', ''),
                    'resumen': articulo.get('resumen', ''),
                    'contenido': articulo.get('contenido', '')
                })
        
        # Expandir todas las categorías
        self.tree.expandAll()
        
        # Limpiar panel de visualización
        self.titulo_label.setText("")
        self.categoria_label.setText("")
        self.resumen_label.setText("")
        self.contenido_text.setText("")
        self.current_articulo_id = None
    
    def on_tree_item_clicked(self, item, column):
        """Maneja el clic en un ítem del árbol"""
        data = item.data(0, Qt.UserRole)
        if not data:
            return
        
        if data.get('tipo') == 'articulo':
            # Mostrar artículo
            self.titulo_label.setText(data.get('titulo', ''))
            self.categoria_label.setText(f"Categoría: {data.get('categoria_nombre', '')}")
            self.resumen_label.setText(data.get('resumen', ''))
            self.contenido_text.setText(data.get('contenido', ''))
            self.current_articulo_id = data.get('id')
            
            # Habilitar botones de acción
            self.edit_button.setEnabled(True)
            self.delete_button.setEnabled(True)
        else:
            # Limpiar panel de visualización para categorías
            self.titulo_label.setText("")
            self.categoria_label.setText("")
            self.resumen_label.setText("")
            self.contenido_text.setText("")
            self.current_articulo_id = None
            
            # Deshabilitar botones de acción
            self.edit_button.setEnabled(False)
            self.delete_button.setEnabled(False)
    
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
    
    def get_articulo_by_id(self, articulo_id):
        """Obtiene un artículo por su ID"""
        # En una aplicación real, estos datos vendrían de la API
        # Aquí buscamos en el árbol
        for i in range(self.tree.topLevelItemCount()):
            categoria_item = self.tree.topLevelItem(i)
            for j in range(categoria_item.childCount()):
                articulo_item = categoria_item.child(j)
                data = articulo_item.data(0, Qt.UserRole)
                if data and data.get('id') == articulo_id:
                    return data
        return None
    
    def create_articulo(self):
        """Abre el diálogo para crear un nuevo artículo"""
        categorias = self.get_categorias()
        dialog = CreateArticuloDialog(self, categorias)
        
        if dialog.exec_() == QDialog.Accepted:
            # Obtener datos del formulario
            articulo_data = dialog.get_data()
            
            # En una aplicación real, aquí se enviarían los datos a la API
            QMessageBox.information(self, "Información", 
                                   f"Artículo '{articulo_data['titulo']}' creado correctamente.")
            
            # Actualizar árbol
            self.refresh_data()
    
    def edit_current_articulo(self):
        """Edita el artículo actualmente seleccionado"""
        if not self.current_articulo_id:
            QMessageBox.warning(self, "Advertencia", "No hay ningún artículo seleccionado.")
            return
        
        articulo_data = self.get_articulo_by_id(self.current_articulo_id)
        if not articulo_data:
            QMessageBox.warning(self, "Advertencia", "No se encontró el artículo seleccionado.")
            return
        
        categorias = self.get_categorias()
        dialog = EditArticuloDialog(self, categorias, articulo_data)
        
        if dialog.exec_() == QDialog.Accepted:
            # Obtener datos del formulario
            updated_data = dialog.get_data()
            
            # En una aplicación real, aquí se enviarían los datos a la API
            QMessageBox.information(self, "Información", 
                                   f"Artículo '{updated_data['titulo']}' actualizado correctamente.")
            
            # Actualizar árbol y panel de visualización
            self.refresh_data()
    
    def delete_current_articulo(self):
        """Elimina el artículo actualmente seleccionado"""
        if not self.current_articulo_id:
            QMessageBox.warning(self, "Advertencia", "No hay ningún artículo seleccionado.")
            return
        
        reply = QMessageBox.question(
            self, 'Confirmar Eliminación',
            f'¿Está seguro de que desea eliminar este artículo?',
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            # En una aplicación real, aquí se enviaría la solicitud de eliminación a la API
            QMessageBox.information(self, "Información", 
                                   f"Artículo eliminado correctamente.")
            
            # Actualizar árbol y panel de visualización
            self.refresh_data()

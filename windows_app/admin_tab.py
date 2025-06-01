from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QTabWidget, QLabel, 
    QPushButton, QTableWidget, QTableWidgetItem, QHeaderView, 
    QStyle, QMessageBox, QDialog, QFormLayout, QLineEdit, QComboBox, QTextEdit
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from empresa_dialog import EmpresaDialog
from usuario_dialog import UsuarioDialog
from usuario_details_dialog import UsuarioDetailsDialog
from grupo_dialog import GrupoDialog
from grupo_details_dialog import GrupoDetailsDialog

class AdminTab(QWidget):
    """Pestaña para administración de Empresas, Granjas, Usuarios y Grupos"""
    
    def __init__(self, api_client):
        super().__init__()
        self.api_client = api_client
        
        # Crear layout principal
        layout = QVBoxLayout(self)
        
        # Título
        title_label = QLabel("Administración")
        title_label.setStyleSheet("font-size: 24px; font-weight: bold; color: #5a5c69;")
        layout.addWidget(title_label)
        
        # Descripción
        description_label = QLabel("Gestione empresas, granjas, usuarios y grupos.")
        description_label.setStyleSheet("font-size: 14px; color: #858796; margin-bottom: 20px;")
        layout.addWidget(description_label)
        
        # Crear pestañas para las diferentes secciones
        self.tabs = QTabWidget()
        
        # Crear las pestañas
        self.empresas_tab = self.create_empresas_tab()
        self.granjas_tab = self.create_granjas_tab()
        self.usuarios_tab = self.create_usuarios_tab()
        self.grupos_tab = self.create_grupos_tab()
        
        # Agregar pestañas al widget de pestañas
        self.tabs.addTab(self.empresas_tab, "Empresas")
        self.tabs.addTab(self.granjas_tab, "Granjas")
        self.tabs.addTab(self.usuarios_tab, "Usuarios")
        self.tabs.addTab(self.grupos_tab, "Grupos")
        
        layout.addWidget(self.tabs)
    
    def create_empresas_tab(self):
        """Crea la pestaña de empresas"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        # Encabezado
        header_layout = QHBoxLayout()
        
        title = QLabel("Listado de Empresas")
        title.setStyleSheet("font-size: 16px; font-weight: bold;")
        header_layout.addWidget(title)
        
        header_layout.addStretch()
        
        # Botón para agregar empresa
        add_button = QPushButton("Nueva Empresa")
        add_button.setStyleSheet("""
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
        add_button.clicked.connect(self.add_empresa)
        header_layout.addWidget(add_button)
        
        layout.addLayout(header_layout)
        
        # Tabla de empresas
        self.empresas_table = QTableWidget()
        self.empresas_table.setColumnCount(4)
        self.empresas_table.setHorizontalHeaderLabels(["ID", "Nombre", "NIT", "Acciones"])
        self.empresas_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)  # Nombre se estira
        self.empresas_table.horizontalHeader().setSectionResizeMode(2, QHeaderView.Stretch)  # NIT se estira
        self.empresas_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.empresas_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.empresas_table.verticalHeader().setVisible(False)
        
        layout.addWidget(self.empresas_table)
        
        # Cargar datos
        self.refresh_empresas()
        
        return tab
    
    def refresh_empresas(self):
        """Actualiza la tabla de empresas"""
        # Limpiar tabla
        self.empresas_table.setRowCount(0)
        
        # Obtener empresas desde la API
        success, empresas = self.api_client.get_empresas()
        
        if success and empresas:
            # Agregar filas
            for row, empresa in enumerate(empresas):
                self.empresas_table.insertRow(row)
                
                # ID
                self.empresas_table.setItem(row, 0, QTableWidgetItem(str(empresa.get('id', ''))))
                
                # Nombre
                self.empresas_table.setItem(row, 1, QTableWidgetItem(empresa.get('nombre', '')))
                
                # NIT
                self.empresas_table.setItem(row, 2, QTableWidgetItem(empresa.get('nit', '')))
                
                # Acciones
                actions_layout = QHBoxLayout()
                actions_layout.setContentsMargins(4, 4, 4, 4)
                
                # Botón de editar
                edit_button = QPushButton()
                edit_button.setIcon(self.style().standardIcon(QStyle.SP_FileDialogDetailedView))
                edit_button.setToolTip("Editar")
                edit_button.setMaximumWidth(30)
                edit_button.clicked.connect(lambda checked, eid=empresa.get('id'): self.edit_empresa(eid))
                actions_layout.addWidget(edit_button)
                
                # Botón de eliminar
                delete_button = QPushButton()
                delete_button.setIcon(self.style().standardIcon(QStyle.SP_TrashIcon))
                delete_button.setToolTip("Eliminar")
                delete_button.setMaximumWidth(30)
                delete_button.clicked.connect(lambda checked, eid=empresa.get('id'): self.delete_empresa(eid))
                actions_layout.addWidget(delete_button)
                
                # Widget contenedor para los botones
                actions_widget = QWidget()
                actions_widget.setLayout(actions_layout)
                
                self.empresas_table.setCellWidget(row, 3, actions_widget)
            
            # Ajustar tamaño de columnas
            self.empresas_table.resizeColumnsToContents()
        else:
            # Si hay un error, mostrar mensaje
            print(f"Error al obtener empresas: {empresas}")
    
    def add_empresa(self):
        """Abre el diálogo para agregar una nueva empresa"""
        dialog = EmpresaDialog(self)
        
        if dialog.exec_() == QDialog.Accepted:
            # Obtener datos del formulario
            empresa_data = dialog.get_data()
            
            # Crear empresa en la API
            success, result = self.api_client.create_empresa(empresa_data)
            
            if success:
                QMessageBox.information(self, "Información", "Empresa creada correctamente")
                self.refresh_empresas()
            else:
                QMessageBox.warning(self, "Error", f"Error al crear empresa: {result}")
    
    def edit_empresa(self, empresa_id):
        """Abre el diálogo para editar una empresa existente"""
        # Obtener datos de la empresa
        success, empresa_data = self.api_client.get_empresa(empresa_id)
        
        if success:
            dialog = EmpresaDialog(self, empresa_data)
            
            if dialog.exec_() == QDialog.Accepted:
                # Obtener datos actualizados
                updated_data = dialog.get_data()
                
                # Actualizar empresa en la API
                success, result = self.api_client.update_empresa(empresa_id, updated_data)
                
                if success:
                    QMessageBox.information(self, "Información", "Empresa actualizada correctamente")
                    self.refresh_empresas()
                else:
                    QMessageBox.warning(self, "Error", f"Error al actualizar empresa: {result}")
        else:
            QMessageBox.warning(self, "Error", f"Error al obtener empresa: {empresa_data}")
    
    def delete_empresa(self, empresa_id):
        """Elimina una empresa"""
        # Confirmar eliminación
        reply = QMessageBox.question(self, "Confirmar", "¿Está seguro de eliminar esta empresa?",
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        
        if reply == QMessageBox.Yes:
            # Eliminar empresa en la API
            success, result = self.api_client.delete_empresa(empresa_id)
            
            if success:
                QMessageBox.information(self, "Información", "Empresa eliminada correctamente")
                self.refresh_empresas()
            else:
                QMessageBox.warning(self, "Error", f"Error al eliminar empresa: {result}")
    
    def create_granjas_tab(self):
        """Crea la pestaña de granjas"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        # Título
        title_label = QLabel("<h2>Gestión de Granjas</h2>")
        layout.addWidget(title_label)
        
        # Botones de acción
        button_layout = QHBoxLayout()
        
        self.refresh_granjas_button = QPushButton("Actualizar")
        self.refresh_granjas_button.clicked.connect(self.refresh_granjas)
        button_layout.addWidget(self.refresh_granjas_button)
        
        self.add_granja_button = QPushButton("Nueva Granja")
        self.add_granja_button.clicked.connect(self.add_granja)
        button_layout.addWidget(self.add_granja_button)
        
        layout.addLayout(button_layout)
        
        # Tabla de granjas
        self.granjas_table = QTableWidget()
        self.granjas_table.setColumnCount(5)
        self.granjas_table.setHorizontalHeaderLabels(["ID", "Nombre", "Ubicación", "Empresa", "Acciones"])
        self.granjas_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.granjas_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.granjas_table.setAlternatingRowColors(True)
        self.granjas_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        
        layout.addWidget(self.granjas_table)
        
        # Cargar datos
        self.refresh_granjas()
        
        return tab
        
    def refresh_granjas(self):
        """Actualiza la tabla de granjas"""
        # Limpiar tabla
        self.granjas_table.setRowCount(0)
        
        # Obtener granjas desde la API
        success, granjas = self.api_client.get_granjas()
        
        if success and granjas:
            # Verificar si granjas es una lista
            if not isinstance(granjas, list):
                print(f"Error: datos de granjas con formato inesperado: {type(granjas)}")
                granjas = self.api_client.get_example_data('granjas')
                
            # Llenar tabla con datos
            for row, granja in enumerate(granjas):
                # Verificar que granja sea un diccionario
                if not isinstance(granja, dict):
                    print(f"Error: granja con formato inesperado: {type(granja)}")
                    continue
                    
                self.granjas_table.insertRow(row)
                
                # ID
                id_item = QTableWidgetItem(str(granja.get('id', '')))
                self.granjas_table.setItem(row, 0, id_item)
                
                # Nombre
                nombre_item = QTableWidgetItem(str(granja.get('nombre', '')))
                self.granjas_table.setItem(row, 1, nombre_item)
                
                # Ubicación
                ubicacion_item = QTableWidgetItem(str(granja.get('ubicacion', '')))
                self.granjas_table.setItem(row, 2, ubicacion_item)
                
                # Empresa
                empresa = granja.get('empresa', {})
                empresa_nombre = empresa.get('nombre', '') if isinstance(empresa, dict) else str(empresa)
                empresa_item = QTableWidgetItem(empresa_nombre)
                self.granjas_table.setItem(row, 3, empresa_item)
                
                # Acciones
                actions_layout = QHBoxLayout()
                actions_layout.setContentsMargins(4, 4, 4, 4)
                actions_layout.setSpacing(4)
                
                # Botón de editar
                edit_button = QPushButton()
                edit_button.setIcon(self.style().standardIcon(QStyle.SP_FileDialogDetailedView))
                edit_button.setToolTip("Editar")
                edit_button.setMaximumWidth(30)
                granja_id = granja.get('id')
                edit_button.clicked.connect(lambda checked, gid=granja_id: self.edit_granja(gid))
                actions_layout.addWidget(edit_button)
                
                # Botón de eliminar
                delete_button = QPushButton()
                delete_button.setIcon(self.style().standardIcon(QStyle.SP_TrashIcon))
                delete_button.setToolTip("Eliminar")
                delete_button.setMaximumWidth(30)
                delete_button.clicked.connect(lambda checked, gid=granja_id: self.delete_granja(gid))
                actions_layout.addWidget(delete_button)
                
                # Widget contenedor para los botones
                actions_widget = QWidget()
                actions_widget.setLayout(actions_layout)
                
                self.granjas_table.setCellWidget(row, 4, actions_widget)
            
            # Ajustar tamaño de columnas
            self.granjas_table.resizeColumnsToContents()
        else:
            # Si hay un error, mostrar mensaje
            print(f"Error al obtener granjas: {granjas}")
            
    def add_granja(self):
        """Abre el diálogo para agregar una nueva granja"""
        QMessageBox.information(self, "Información", "Funcionalidad en desarrollo. Por favor, utilice el panel de administración de Django para gestionar granjas.")
        
    def edit_granja(self, granja_id):
        """Abre el diálogo para editar una granja existente"""
        QMessageBox.information(self, "Información", "Funcionalidad en desarrollo. Por favor, utilice el panel de administración de Django para gestionar granjas.")
        
    def delete_granja(self, granja_id):
        """Elimina una granja"""
        QMessageBox.information(self, "Información", "Funcionalidad en desarrollo. Por favor, utilice el panel de administración de Django para gestionar granjas.")
    
    def create_usuarios_tab(self):
        """Crea la pestaña de usuarios"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        # Título
        title_label = QLabel("<h2>Gestión de Usuarios</h2>")
        layout.addWidget(title_label)
        
        # Botones de acción
        button_layout = QHBoxLayout()
        
        self.refresh_usuarios_button = QPushButton("Actualizar")
        self.refresh_usuarios_button.clicked.connect(self.refresh_usuarios)
        button_layout.addWidget(self.refresh_usuarios_button)
        
        self.add_usuario_button = QPushButton("Nuevo Usuario")
        self.add_usuario_button.clicked.connect(self.add_usuario)
        button_layout.addWidget(self.add_usuario_button)
        
        layout.addLayout(button_layout)
        
        # Tabla de usuarios
        self.usuarios_table = QTableWidget()
        self.usuarios_table.setColumnCount(5)
        self.usuarios_table.setHorizontalHeaderLabels(["ID", "Usuario", "Nombre", "Email", "Acciones"])
        self.usuarios_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.usuarios_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.usuarios_table.setAlternatingRowColors(True)
        self.usuarios_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        
        layout.addWidget(self.usuarios_table)
        
        # Cargar datos
        self.refresh_usuarios()
        
        return tab
        
    def refresh_usuarios(self):
        """Actualiza la tabla de usuarios"""
        # Limpiar tabla
        self.usuarios_table.setRowCount(0)
        
        # Obtener usuarios desde la API
        success, usuarios = self.api_client.get_usuarios()
        
        if success and usuarios:
            # Verificar si usuarios es una lista
            if not isinstance(usuarios, list):
                print(f"Error: datos de usuarios con formato inesperado: {type(usuarios)}")
                usuarios = self.api_client.get_example_data('usuarios')
                
            # Llenar tabla con datos
            for row, usuario in enumerate(usuarios):
                # Verificar que usuario sea un diccionario
                if not isinstance(usuario, dict):
                    print(f"Error: usuario con formato inesperado: {type(usuario)}")
                    continue
                    
                self.usuarios_table.insertRow(row)
                
                # ID
                id_item = QTableWidgetItem(str(usuario.get('id', '')))
                self.usuarios_table.setItem(row, 0, id_item)
                
                # Usuario
                username_item = QTableWidgetItem(str(usuario.get('username', '')))
                self.usuarios_table.setItem(row, 1, username_item)
                
                # Nombre completo
                nombre = f"{usuario.get('first_name', '')} {usuario.get('last_name', '')}".strip()
                nombre_item = QTableWidgetItem(nombre)
                self.usuarios_table.setItem(row, 2, nombre_item)
                
                # Email
                email_item = QTableWidgetItem(str(usuario.get('email', '')))
                self.usuarios_table.setItem(row, 3, email_item)
                
                # Acciones
                actions_layout = QHBoxLayout()
                actions_layout.setContentsMargins(4, 4, 4, 4)
                actions_layout.setSpacing(4)
                
                # Botón de editar
                edit_button = QPushButton()
                edit_button.setIcon(self.style().standardIcon(QStyle.SP_FileDialogDetailedView))
                edit_button.setToolTip("Editar")
                edit_button.setMaximumWidth(30)
                usuario_id = usuario.get('id')
                edit_button.clicked.connect(lambda checked, uid=usuario_id: self.edit_usuario(uid))
                actions_layout.addWidget(edit_button)
                
                # Botón de eliminar
                delete_button = QPushButton()
                delete_button.setIcon(self.style().standardIcon(QStyle.SP_TrashIcon))
                delete_button.setToolTip("Eliminar")
                delete_button.setMaximumWidth(30)
                delete_button.clicked.connect(lambda checked, uid=usuario_id: self.delete_usuario(uid))
                actions_layout.addWidget(delete_button)
                
                # Widget contenedor para los botones
                actions_widget = QWidget()
                actions_widget.setLayout(actions_layout)
                
                self.usuarios_table.setCellWidget(row, 4, actions_widget)
            
            # Ajustar tamaño de columnas
            self.usuarios_table.resizeColumnsToContents()
        else:
            # Si hay un error, mostrar mensaje
            print(f"Error al obtener usuarios: {usuarios}")
            
    def add_usuario(self):
        """Abre el diálogo para agregar un nuevo usuario"""
        dialog = UsuarioDialog(self, self.api_client)
        if dialog.exec_():
            self.refresh_usuarios()
        
    def edit_usuario(self, usuario_id):
        """Abre el diálogo para ver detalles de un usuario"""
        dialog = UsuarioDetailsDialog(self, self.api_client, usuario_id)
        if dialog.exec_():
            self.refresh_usuarios()
        
    def delete_usuario(self, usuario_id):
        """Elimina un usuario"""
        # Confirmar eliminación
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Warning)
        msg_box.setText("Está seguro de que desea eliminar este usuario?")
        msg_box.setWindowTitle("Confirmar eliminación")
        msg_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        msg_box.setDefaultButton(QMessageBox.No)
        
        if msg_box.exec_() == QMessageBox.Yes:
            success, result = self.api_client.delete_usuario(usuario_id)
            if success:
                self.refresh_usuarios()
                QMessageBox.information(self, "Información", "Usuario eliminado correctamente")
            else:
                QMessageBox.warning(self, "Error", f"Error al eliminar usuario: {result}")
    
    def create_grupos_tab(self):
        """Crea la pestaña de grupos"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        # Título
        title_label = QLabel("<h2>Gestión de Grupos</h2>")
        layout.addWidget(title_label)
        
        # Botones de acción
        button_layout = QHBoxLayout()
        
        self.refresh_grupos_button = QPushButton("Actualizar")
        self.refresh_grupos_button.clicked.connect(self.refresh_grupos)
        button_layout.addWidget(self.refresh_grupos_button)
        
        self.add_grupo_button = QPushButton("Nuevo Grupo")
        self.add_grupo_button.clicked.connect(self.add_grupo)
        button_layout.addWidget(self.add_grupo_button)
        
        layout.addLayout(button_layout)
        
        # Tabla de grupos
        self.grupos_table = QTableWidget()
        self.grupos_table.setColumnCount(3)
        self.grupos_table.setHorizontalHeaderLabels(["ID", "Nombre", "Acciones"])
        self.grupos_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.grupos_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.grupos_table.setAlternatingRowColors(True)
        self.grupos_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        
        layout.addWidget(self.grupos_table)
        
        # Cargar datos
        self.refresh_grupos()
        
        return tab
        
    def refresh_grupos(self):
        """Actualiza la tabla de grupos"""
        # Limpiar tabla
        self.grupos_table.setRowCount(0)
        
        # Obtener grupos desde la API
        success, grupos = self.api_client.get_grupos()
        
        if success and grupos:
            # Verificar si grupos es una lista
            if not isinstance(grupos, list):
                print(f"Error: datos de grupos con formato inesperado: {type(grupos)}")
                grupos = self.api_client.get_example_data('grupos')
                
            # Llenar tabla con datos
            for row, grupo in enumerate(grupos):
                # Verificar que grupo sea un diccionario
                if not isinstance(grupo, dict):
                    print(f"Error: grupo con formato inesperado: {type(grupo)}")
                    continue
                    
                self.grupos_table.insertRow(row)
                
                # ID
                id_item = QTableWidgetItem(str(grupo.get('id', '')))
                self.grupos_table.setItem(row, 0, id_item)
                
                # Nombre
                name_item = QTableWidgetItem(str(grupo.get('name', '')))
                self.grupos_table.setItem(row, 1, name_item)
                
                # Acciones
                actions_layout = QHBoxLayout()
                actions_layout.setContentsMargins(4, 4, 4, 4)
                actions_layout.setSpacing(4)
                
                # Botón de editar
                edit_button = QPushButton()
                edit_button.setIcon(self.style().standardIcon(QStyle.SP_FileDialogDetailedView))
                edit_button.setToolTip("Editar")
                edit_button.setMaximumWidth(30)
                grupo_id = grupo.get('id')
                edit_button.clicked.connect(lambda checked, gid=grupo_id: self.edit_grupo(gid))
                actions_layout.addWidget(edit_button)
                
                # Botón de eliminar
                delete_button = QPushButton()
                delete_button.setIcon(self.style().standardIcon(QStyle.SP_TrashIcon))
                delete_button.setToolTip("Eliminar")
                delete_button.setMaximumWidth(30)
                delete_button.clicked.connect(lambda checked, gid=grupo_id: self.delete_grupo(gid))
                actions_layout.addWidget(delete_button)
                
                # Widget contenedor para los botones
                actions_widget = QWidget()
                actions_widget.setLayout(actions_layout)
                
                self.grupos_table.setCellWidget(row, 2, actions_widget)
            
            # Ajustar tamaño de columnas
            self.grupos_table.resizeColumnsToContents()
        else:
            # Si hay un error, mostrar mensaje
            print(f"Error al obtener grupos: {grupos}")
            
    def add_grupo(self):
        """Abre el diálogo para agregar un nuevo grupo"""
        dialog = GrupoDialog(self, self.api_client)
        if dialog.exec_():
            self.refresh_grupos()
        
    def edit_grupo(self, grupo_id):
        """Abre el diálogo para ver detalles de un grupo"""
        dialog = GrupoDetailsDialog(self, self.api_client, grupo_id)
        if dialog.exec_():
            self.refresh_grupos()
        
    def delete_grupo(self, grupo_id):
        """Elimina un grupo"""
        # Confirmar eliminación
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Warning)
        msg_box.setText("Está seguro de que desea eliminar este grupo?")
        msg_box.setWindowTitle("Confirmar eliminación")
        msg_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        msg_box.setDefaultButton(QMessageBox.No)
        
        if msg_box.exec_() == QMessageBox.Yes:
            # Mostrar mensaje informativo ya que la funcionalidad está en desarrollo
            QMessageBox.information(
                self, 
                "Información", 
                "La funcionalidad de eliminación de grupos está en desarrollo. Por favor, utilice el panel de administración de Django."
            )

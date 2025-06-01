from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
                             QTableWidget, QTableWidgetItem, QMessageBox, QDialog,
                             QFormLayout, QLineEdit, QComboBox, QLabel, QHeaderView,
                             QDateEdit, QSpinBox, QDoubleSpinBox, QTabWidget, 
                             QApplication, QCheckBox)
from PyQt5.QtCore import Qt

class GalponDialog(QDialog):
    """Diálogo para crear o editar un galpón"""
    
    def __init__(self, parent=None, galpon_data=None):
        super().__init__(parent)
        self.setWindowTitle("Galpón" if galpon_data else "Nuevo Galpón")
        self.setMinimumWidth(500)
        self.setMinimumHeight(600)
        
        # Crear layout
        layout = QVBoxLayout(self)
        
        # Crear pestañas para organizar la información
        self.tabs = QTabWidget()
        
        # Pestaña de información general
        general_tab = QWidget()
        general_layout = QVBoxLayout(general_tab)
        
        # Formulario de información general
        form_layout = QFormLayout()
        
        # Campos del formulario
        self.nombre_input = QLineEdit()
        form_layout.addRow("Nombre:", self.nombre_input)
        
        self.capacidad_input = QSpinBox()
        self.capacidad_input.setRange(1, 100000)
        self.capacidad_input.setValue(1000)
        form_layout.addRow("Capacidad (aves):", self.capacidad_input)
        
        self.ancho_input = QDoubleSpinBox()
        self.ancho_input.setRange(1, 1000)
        self.ancho_input.setValue(10)
        self.ancho_input.setSuffix(" m")
        form_layout.addRow("Ancho:", self.ancho_input)
        
        self.largo_input = QDoubleSpinBox()
        self.largo_input.setRange(1, 1000)
        self.largo_input.setValue(20)
        self.largo_input.setSuffix(" m")
        form_layout.addRow("Largo:", self.largo_input)
        
        self.altura_input = QDoubleSpinBox()
        self.altura_input.setRange(1, 50)
        self.altura_input.setValue(3)
        self.altura_input.setSuffix(" m")
        form_layout.addRow("Altura:", self.altura_input)
        
        self.tipo_combo = QComboBox()
        self.tipo_combo.addItems(["Cría", "Producción", "Recría", "Engorde"])
        form_layout.addRow("Tipo:", self.tipo_combo)
        
        self.estado_combo = QComboBox()
        self.estado_combo.addItems(["Activo", "Inactivo", "Mantenimiento", "En Limpieza", "En Desinfección"])
        form_layout.addRow("Estado:", self.estado_combo)
        
        general_layout.addLayout(form_layout)
        
        # Pestaña de equipamiento
        equipamiento_tab = QWidget()
        equipamiento_layout = QVBoxLayout(equipamiento_tab)
        
        # Formulario de equipamiento
        equipamiento_form = QFormLayout()
        
        self.bebederos_input = QSpinBox()
        self.bebederos_input.setRange(0, 1000)
        equipamiento_form.addRow("Bebederos:", self.bebederos_input)
        
        self.comederos_input = QSpinBox()
        self.comederos_input.setRange(0, 1000)
        equipamiento_form.addRow("Comederos:", self.comederos_input)
        
        self.ventiladores_input = QSpinBox()
        self.ventiladores_input.setRange(0, 100)
        equipamiento_form.addRow("Ventiladores:", self.ventiladores_input)
        
        self.calefactores_input = QSpinBox()
        self.calefactores_input.setRange(0, 100)
        equipamiento_form.addRow("Calefactores:", self.calefactores_input)
        
        self.nidos_input = QSpinBox()
        self.nidos_input.setRange(0, 1000)
        equipamiento_form.addRow("Nidos:", self.nidos_input)
        
        self.sistema_alimentacion_combo = QComboBox()
        self.sistema_alimentacion_combo.addItems(["Manual", "Automático", "Semi-automático"])
        equipamiento_form.addRow("Sistema de Alimentación:", self.sistema_alimentacion_combo)
        
        self.sistema_agua_combo = QComboBox()
        self.sistema_agua_combo.addItems(["Manual", "Automático", "Semi-automático"])
        equipamiento_form.addRow("Sistema de Agua:", self.sistema_agua_combo)
        
        equipamiento_layout.addLayout(equipamiento_form)
        
        # Pestaña de sensores
        sensores_tab = QWidget()
        sensores_layout = QVBoxLayout(sensores_tab)
        
        # Formulario de sensores
        sensores_form = QFormLayout()
        
        self.sensor_temperatura = QCheckBox("Instalado")
        sensores_form.addRow("Sensor de Temperatura:", self.sensor_temperatura)
        
        self.sensor_humedad = QCheckBox("Instalado")
        sensores_form.addRow("Sensor de Humedad:", self.sensor_humedad)
        
        self.sensor_co2 = QCheckBox("Instalado")
        sensores_form.addRow("Sensor de CO2:", self.sensor_co2)
        
        self.sensor_amoniaco = QCheckBox("Instalado")
        sensores_form.addRow("Sensor de Amoníaco:", self.sensor_amoniaco)
        
        self.sensor_luz = QCheckBox("Instalado")
        sensores_form.addRow("Sensor de Luz:", self.sensor_luz)
        
        self.camara_vigilancia = QCheckBox("Instalada")
        sensores_form.addRow("Cámara de Vigilancia:", self.camara_vigilancia)
        
        sensores_layout.addLayout(sensores_form)
        
        # Pestaña de energía
        energia_tab = QWidget()
        energia_layout = QVBoxLayout(energia_tab)
        
        # Formulario de energía
        energia_form = QFormLayout()
        
        self.consumo_energia = QDoubleSpinBox()
        self.consumo_energia.setRange(0, 100000)
        self.consumo_energia.setSuffix(" kWh/mes")
        self.consumo_energia.setDecimals(2)
        energia_form.addRow("Consumo Energético:", self.consumo_energia)
        
        self.costo_energia = QDoubleSpinBox()
        self.costo_energia.setRange(0, 100000)
        self.costo_energia.setPrefix("$")
        self.costo_energia.setDecimals(2)
        energia_form.addRow("Costo Energético Mensual:", self.costo_energia)
        
        self.fuente_energia_combo = QComboBox()
        self.fuente_energia_combo.addItems(["Red Eléctrica", "Generador", "Energía Solar", "Híbrido"])
        energia_form.addRow("Fuente de Energía:", self.fuente_energia_combo)
        
        self.tiene_respaldo = QCheckBox("Disponible")
        energia_form.addRow("Sistema de Respaldo:", self.tiene_respaldo)
        
        energia_layout.addLayout(energia_form)
        
        # Agregar pestañas al widget de pestañas
        self.tabs.addTab(general_tab, "Información General")
        self.tabs.addTab(equipamiento_tab, "Equipamiento")
        self.tabs.addTab(sensores_tab, "Sensores")
        self.tabs.addTab(energia_tab, "Energía")
        
        layout.addWidget(self.tabs)
        
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
        
        # Si se proporciona datos de galpón, llenar el formulario
        if galpon_data:
            # Datos generales
            self.nombre_input.setText(galpon_data.get('nombre', ''))
            self.capacidad_input.setValue(galpon_data.get('capacidad', 1000))
            self.ancho_input.setValue(galpon_data.get('ancho', 10))
            self.largo_input.setValue(galpon_data.get('largo', 20))
            self.altura_input.setValue(galpon_data.get('altura', 3))
            
            tipo = galpon_data.get('tipo', '')
            if tipo:
                index = self.tipo_combo.findText(tipo)
                if index >= 0:
                    self.tipo_combo.setCurrentIndex(index)
            
            estado = galpon_data.get('estado', '')
            if estado:
                index = self.estado_combo.findText(estado)
                if index >= 0:
                    self.estado_combo.setCurrentIndex(index)
            
            # Datos de equipamiento
            equipamiento = galpon_data.get('equipamiento', {})
            if isinstance(equipamiento, dict):
                self.bebederos_input.setValue(equipamiento.get('bebederos', 0))
                self.comederos_input.setValue(equipamiento.get('comederos', 0))
                self.ventiladores_input.setValue(equipamiento.get('ventiladores', 0))
                self.calefactores_input.setValue(equipamiento.get('calefactores', 0))
                self.nidos_input.setValue(equipamiento.get('nidos', 0))
                
                sistema_alimentacion = equipamiento.get('sistema_alimentacion', '')
                if sistema_alimentacion:
                    index = self.sistema_alimentacion_combo.findText(sistema_alimentacion)
                    if index >= 0:
                        self.sistema_alimentacion_combo.setCurrentIndex(index)
                
                sistema_agua = equipamiento.get('sistema_agua', '')
                if sistema_agua:
                    index = self.sistema_agua_combo.findText(sistema_agua)
                    if index >= 0:
                        self.sistema_agua_combo.setCurrentIndex(index)
            
            # Datos de sensores
            sensores = galpon_data.get('sensores', {})
            if isinstance(sensores, dict):
                self.sensor_temperatura.setChecked(sensores.get('temperatura', False))
                self.sensor_humedad.setChecked(sensores.get('humedad', False))
                self.sensor_co2.setChecked(sensores.get('co2', False))
                self.sensor_amoniaco.setChecked(sensores.get('amoniaco', False))
                self.sensor_luz.setChecked(sensores.get('luz', False))
                self.camara_vigilancia.setChecked(sensores.get('camara', False))
            
            # Datos de energía
            energia = galpon_data.get('energia', {})
            if isinstance(energia, dict):
                self.consumo_energia.setValue(energia.get('consumo', 0))
                self.costo_energia.setValue(energia.get('costo', 0))
                
                fuente = energia.get('fuente', '')
                if fuente:
                    index = self.fuente_energia_combo.findText(fuente)
                    if index >= 0:
                        self.fuente_energia_combo.setCurrentIndex(index)
                
                self.tiene_respaldo.setChecked(energia.get('tiene_respaldo', False))
    
    def get_data(self):
        """Obtiene los datos del formulario"""
        return {
            # Datos generales
            'nombre': self.nombre_input.text(),
            'capacidad': self.capacidad_input.value(),
            'ancho': self.ancho_input.value(),
            'largo': self.largo_input.value(),
            'altura': self.altura_input.value(),
            'tipo': self.tipo_combo.currentText(),
            'estado': self.estado_combo.currentText(),
            
            # Datos de equipamiento
            'equipamiento': {
                'bebederos': self.bebederos_input.value(),
                'comederos': self.comederos_input.value(),
                'ventiladores': self.ventiladores_input.value(),
                'calefactores': self.calefactores_input.value(),
                'nidos': self.nidos_input.value(),
                'sistema_alimentacion': self.sistema_alimentacion_combo.currentText(),
                'sistema_agua': self.sistema_agua_combo.currentText()
            },
            
            # Datos de sensores
            'sensores': {
                'temperatura': self.sensor_temperatura.isChecked(),
                'humedad': self.sensor_humedad.isChecked(),
                'co2': self.sensor_co2.isChecked(),
                'amoniaco': self.sensor_amoniaco.isChecked(),
                'luz': self.sensor_luz.isChecked(),
                'camara': self.camara_vigilancia.isChecked()
            },
            
            # Datos de energía
            'energia': {
                'consumo': self.consumo_energia.value(),
                'costo': self.costo_energia.value(),
                'fuente': self.fuente_energia_combo.currentText(),
                'tiene_respaldo': self.tiene_respaldo.isChecked()
            }
        }

class GalponesTab(QWidget):
    """Pestaña para gestionar galpones"""
    
    def __init__(self, api_client):
        super().__init__()
        self.api_client = api_client
        
        # Crear layout principal
        layout = QVBoxLayout(self)
        
        # Título
        title_label = QLabel("Gestión de Galpones")
        title_label.setStyleSheet("font-size: 24px; font-weight: bold; color: #5a5c69;")
        layout.addWidget(title_label)
        
        # Descripción
        desc_label = QLabel("Administra los galpones del sistema avícola")
        desc_label.setStyleSheet("font-size: 14px; color: #858796; margin-bottom: 20px;")
        layout.addWidget(desc_label)
        
        # Botones de acción
        action_layout = QHBoxLayout()
        
        self.new_button = QPushButton("Nuevo Galpón")
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
        self.new_button.clicked.connect(self.create_galpon)
        
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
        
        # Tabla de galpones
        self.table = QTableWidget()
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels([
            "ID", "Nombre", "Capacidad", "Ancho (m)", "Largo (m)", 
            "Área (m²)", "Estado"
        ])
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.doubleClicked.connect(self.edit_galpon)
        
        layout.addWidget(self.table)
        
        # Cargar datos iniciales
        self.refresh_data()
    
    def refresh_data(self):
        """Actualiza los datos de la tabla de galpones"""
        success, data = self.api_client.get_galpones()
        
        # Limpiar tabla
        self.table.setRowCount(0)
        
        # Verificar si tenemos datos válidos
        if success and data:
            # Llenar tabla con datos
            for row, galpon in enumerate(data):
                if not isinstance(galpon, dict):
                    continue
                    
                self.table.insertRow(row)
                
                # ID
                id_item = QTableWidgetItem(str(galpon.get('id', '')))
                self.table.setItem(row, 0, id_item)
                
                # Nombre
                nombre_item = QTableWidgetItem(galpon.get('nombre', ''))
                self.table.setItem(row, 1, nombre_item)
                
                # Capacidad
                capacidad_item = QTableWidgetItem(str(galpon.get('capacidad', 0)))
                self.table.setItem(row, 2, capacidad_item)
                
                # Ancho
                ancho = galpon.get('ancho', 0)
                ancho_item = QTableWidgetItem(f"{ancho}")
                self.table.setItem(row, 3, ancho_item)
                
                # Largo
                largo = galpon.get('largo', 0)
                largo_item = QTableWidgetItem(f"{largo}")
                self.table.setItem(row, 4, largo_item)
                
                # Área
                area = ancho * largo
                area_item = QTableWidgetItem(f"{area}")
                self.table.setItem(row, 5, area_item)
                
                # Estado
                estado_item = QTableWidgetItem(galpon.get('estado', ''))
                self.table.setItem(row, 6, estado_item)
            
            # Ajustar tamaño de columnas
            self.table.resizeColumnsToContents()
        else:
            # Si hay un error, mostrar mensaje solo si no se pudo conectar
            if not success:
                QMessageBox.warning(self, "Modo sin conexión", 
                                "No se pudo conectar al servidor Django.\n\n"
                                "La aplicación mostrará datos de ejemplo.\n\n"
                                "Para ver datos reales, asegúrese de que el servidor Django esté en funcionamiento.")
            
            # Agregar filas de ejemplo para mostrar la estructura
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
        """Abre el diálogo para crear un nuevo galpón"""
        dialog = GalponDialog(self)
        
        if dialog.exec_() == QDialog.Accepted:
            # Obtener datos del formulario
            form_data = dialog.get_data()
            
            # Transformar los datos al formato esperado por la API
            galpon_data = {
                'numero_galpon': form_data.get('nombre', 'Nuevo Galpón'),
                'tipo_galpon': form_data.get('tipo', 'Producción'),
                'capacidad_aves': form_data.get('capacidad', 0),
                'area_metros_cuadrados': form_data.get('ancho', 0) * form_data.get('largo', 0),
                'altura': form_data.get('altura', 3.0),
                'estado': form_data.get('estado', 'Activo'),
                'equipamiento': form_data.get('equipamiento', {}),
                'sensores': form_data.get('sensores', {}),
                'energia': form_data.get('energia', {})
            }
            
            # Mostrar indicador de carga
            QApplication.setOverrideCursor(Qt.WaitCursor)
            
            try:
                # Llamar a la API para crear el galpón
                success, result = self.api_client.create_galpon(galpon_data)
                
                if success:
                    QMessageBox.information(
                        self, 
                        "Éxito", 
                        f"Galpón creado exitosamente con ID: {result.get('id', 'N/A')}"
                    )
                    # Actualizar tabla
                    self.refresh_data()
                else:
                    QMessageBox.critical(
                        self,
                        "Error",
                        f"No se pudo crear el galpón: {result}"
                    )
                    
            except Exception as e:
                import traceback
                error_details = traceback.format_exc()
                QMessageBox.critical(
                    self,
                    "Error inesperado",
                    f"Ocurrió un error al crear el galpón:\n{str(e)}\n\nDetalles:\n{error_details}"
                )
            finally:
                # Restaurar cursor
                QApplication.restoreOverrideCursor()
    
    def edit_galpon(self):
        """Abre el diálogo para editar un galpón existente"""
        # Obtener fila seleccionada
        selected_row = self.table.currentRow()
        
        if selected_row >= 0:
            # Obtener ID del galpón
            galpon_id = self.table.item(selected_row, 0).text()
            galpon_nombre = self.table.item(selected_row, 1).text()
            
            # Mostrar indicador de carga
            QApplication.setOverrideCursor(Qt.WaitCursor)
            
            try:
                # Obtener datos actuales del galpón
                success, galpon_data = self.api_client.get_galpon(galpon_id)
                
                if not success:
                    QMessageBox.warning(
                        self, 
                        "Error", 
                        f"No se pudieron cargar los datos del galpón: {galpon_data}"
                    )
                    return
                
                # Abrir diálogo con datos actuales
                dialog = GalponDialog(self, galpon_data)
                
                if dialog.exec_() == QDialog.Accepted:
                    # Obtener datos actualizados
                    updated_data = dialog.get_data()
                    
                    # Mostrar indicador de carga
                    QApplication.setOverrideCursor(Qt.WaitCursor)
                    
                    try:
                        # Llamar a la API para actualizar el galpón
                        success, result = self.api_client.update_galpon(galpon_id, updated_data)
                        
                        if success:
                            QMessageBox.information(
                                self, 
                                "Éxito", 
                                f"Galpón '{galpon_nombre}' actualizado correctamente"
                            )
                            # Actualizar tabla
                            self.refresh_data()
                        else:
                            QMessageBox.critical(
                                self,
                                "Error",
                                f"No se pudo actualizar el galpón: {result}"
                            )
                            
                    except Exception as e:
                        QMessageBox.critical(
                            self,
                            "Error inesperado",
                            f"Ocurrió un error al actualizar el galpón: {str(e)}"
                        )
                    finally:
                        # Restaurar cursor
                        QApplication.restoreOverrideCursor()
                        
            except Exception as e:
                QMessageBox.critical(
                    self,
                    "Error inesperado",
                    f"Ocurrió un error al cargar el galpón: {str(e)}"
                )
            finally:
                # Restaurar cursor
                QApplication.restoreOverrideCursor()
        else:
            QMessageBox.warning(
                self, 
                "Advertencia", 
                "Por favor, seleccione un galpón de la lista para editar"
            )

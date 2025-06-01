import os
import datetime
import time
import random
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                           QPushButton, QTextEdit, QLineEdit,
                           QScrollArea, QFrame, QSizePolicy, QApplication)
from PyQt5.QtCore import Qt, QSize, QThread, pyqtSignal
from PyQt5.QtGui import QFont, QColor

class BotThread(QThread):
    """Hilo para procesar las consultas del bot"""
    response_ready = pyqtSignal(str)
    
    def __init__(self, query):
        super().__init__()
        self.query = query
    
    def run(self):
        """Procesa la consulta y emite la respuesta"""
        # Simular tiempo de procesamiento
        time.sleep(1)
        
        # En una aplicación real, aquí se enviaría la consulta a un servicio de IA
        # y se procesaría la respuesta. Aquí usamos respuestas predefinidas.
        
        # Respuestas predefinidas para preguntas comunes
        responses = {
            "hola": "¡Hola! Soy el asistente virtual de App Granja. ¿En qué puedo ayudarte hoy?",
            "ayuda": "Puedo ayudarte con información sobre manejo de aves, alimentación, vacunación, y más. ¿Sobre qué tema necesitas ayuda?",
            "temperatura": "La temperatura óptima varía según la edad de las aves:\n- 1 semana: 32-33°C\n- 2 semanas: 30-31°C\n- 3 semanas: 28-29°C\n- 4 semanas: 26-27°C\n- 5 semanas: 24-25°C\n- 6+ semanas: 18-22°C",
            "alimentación": "La alimentación debe ajustarse según la etapa de crecimiento:\n- Inicio (0-6 semanas): 20-22% proteína\n- Crecimiento (7-14 semanas): 16-18% proteína\n- Postura (15+ semanas): 16-17% proteína con 3.5-4.0% calcio",
            "vacunación": "El programa básico de vacunación incluye:\n- Newcastle: 7-10 días y 21-24 días\n- Bronquitis: 1 día y 14 días\n- Gumboro: 12-14 días y 22-24 días\n- Viruela: 6-8 semanas\n- Consulte con su veterinario para un programa personalizado.",
            "producción": "Para mejorar la producción de huevos:\n1. Nutrición adecuada\n2. Programa de iluminación (16 horas)\n3. Control de temperatura (18-24°C)\n4. Manejo del estrés\n5. Programa de vacunación\n6. Calidad del agua\n7. Densidad adecuada"
        }
        
        # Procesar la consulta
        query_lower = self.query.lower()
        response = None
        
        # Buscar coincidencias exactas
        for key, value in responses.items():
            if key in query_lower:
                response = value
                break
        
        # Si no hay coincidencias exactas
        if not response:
            # Respuestas genéricas
            generic_responses = [
                "No tengo información específica sobre eso. ¿Podrías reformular tu pregunta?",
                "Esa es una buena pregunta. Te recomendaría consultar la sección de Wiki para información más detallada.",
                "No tengo suficiente información para responder adecuadamente. ¿Hay algo más en lo que pueda ayudarte?",
                "Estoy aprendiendo constantemente. Por ahora, te sugiero consultar con el administrador del sistema para obtener esa información."
            ]
            response = random.choice(generic_responses)
        
        # Emitir la respuesta
        self.response_ready.emit(response)

class MessageBubble(QFrame):
    """Burbuja de mensaje para el chat"""
    
    def __init__(self, text, is_user=False):
        super().__init__()
        
        # Configurar estilo según el remitente
        if is_user:
            self.setStyleSheet("""
                QFrame {
                    background-color: #4e73df;
                    color: white;
                    border-radius: 10px;
                    padding: 10px;
                    margin: 5px;
                }
            """)
        else:
            self.setStyleSheet("""
                QFrame {
                    background-color: #f8f9fc;
                    color: #5a5c69;
                    border-radius: 10px;
                    padding: 10px;
                    margin: 5px;
                }
            """)
        
        # Crear layout
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        
        # Etiqueta de remitente
        sender_label = QLabel("Tú" if is_user else "Asistente")
        sender_label.setStyleSheet("font-weight: bold; color: " + ("white" if is_user else "#4e73df"))
        layout.addWidget(sender_label)
        
        # Contenido del mensaje
        message_label = QLabel(text)
        message_label.setWordWrap(True)
        layout.addWidget(message_label)
        
        # Hora del mensaje
        time_label = QLabel(datetime.datetime.now().strftime("%H:%M"))
        time_label.setStyleSheet("font-size: 10px; color: " + ("rgba(255, 255, 255, 0.7)" if is_user else "rgba(90, 92, 105, 0.7)"))
        time_label.setAlignment(Qt.AlignRight)
        layout.addWidget(time_label)

class BotTab(QWidget):
    """Pestaña para el asistente virtual"""
    
    def __init__(self, api_client):
        super().__init__()
        self.api_client = api_client
        
        # Crear layout principal
        layout = QVBoxLayout(self)
        
        # Título
        title_label = QLabel("Asistente Virtual")
        title_label.setStyleSheet("font-size: 24px; font-weight: bold; color: #5a5c69;")
        layout.addWidget(title_label)
        
        # Descripción
        desc_label = QLabel("Consulta información y recibe asistencia en tiempo real")
        desc_label.setStyleSheet("font-size: 14px; color: #858796; margin-bottom: 20px;")
        layout.addWidget(desc_label)
        
        # Área de chat
        self.chat_area = QWidget()
        self.chat_layout = QVBoxLayout(self.chat_area)
        self.chat_layout.setAlignment(Qt.AlignTop)
        self.chat_layout.setSpacing(10)
        
        # Área de desplazamiento
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setWidget(self.chat_area)
        self.scroll_area.setFrameShape(QFrame.NoFrame)
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        
        layout.addWidget(self.scroll_area)
        
        # Área de entrada
        input_layout = QHBoxLayout()
        
        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText("Escribe tu pregunta aquí...")
        self.input_field.returnPressed.connect(self.send_message)
        
        self.send_button = QPushButton("Enviar")
        self.send_button.setStyleSheet("""
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
        self.send_button.clicked.connect(self.send_message)
        
        input_layout.addWidget(self.input_field)
        input_layout.addWidget(self.send_button)
        
        layout.addLayout(input_layout)
        
        # Mostrar mensaje de bienvenida
        self.add_bot_message("¡Hola! Soy el asistente virtual de App Granja. Estoy aquí para ayudarte con tus consultas sobre manejo de aves, alimentación, vacunación, producción y más. ¿En qué puedo ayudarte hoy?")
    
    def add_user_message(self, text):
        """Agrega un mensaje del usuario al chat"""
        message = MessageBubble(text, is_user=True)
        self.chat_layout.addWidget(message)
        self.chat_layout.addStretch()
        
        # Desplazar al final
        QApplication.processEvents()
        if hasattr(self, 'scroll_area') and self.scroll_area:
            self.scroll_area.verticalScrollBar().setValue(self.scroll_area.verticalScrollBar().maximum())
    
    def add_bot_message(self, text):
        """Agrega un mensaje del bot al chat"""
        message = MessageBubble(text, is_user=False)
        self.chat_layout.addWidget(message)
        self.chat_layout.addStretch()
        
        # Desplazar al final
        QApplication.processEvents()
        if hasattr(self, 'scroll_area') and self.scroll_area:
            self.scroll_area.verticalScrollBar().setValue(self.scroll_area.verticalScrollBar().maximum())
    
    def send_message(self):
        """Envía un mensaje al bot"""
        # Obtener texto del campo de entrada
        text = self.input_field.text().strip()
        if not text:
            return
        
        try:
            # Agregar mensaje del usuario al chat
            self.add_user_message(text)
            
            # Limpiar campo de entrada
            self.input_field.clear()
            
            # Procesar consulta en un hilo separado
            self.bot_thread = BotThread(text)
            self.bot_thread.response_ready.connect(self.handle_bot_response)
            self.bot_thread.start()
            
            # En lugar de mostrar "Escribiendo...", simular una respuesta inmediata
            # para evitar problemas con el indicador de escritura
            QApplication.processEvents()
            
            # Simular un pequeño retraso para que se vea natural
            time.sleep(0.5)
        except Exception as e:
            print(f"Error al enviar mensaje: {str(e)}")
            # Si hay un error, mostrar un mensaje genérico
            try:
                self.add_bot_message("Lo siento, ha ocurrido un error al procesar tu mensaje. Por favor, intenta de nuevo.")
            except:
                pass
    
    def handle_bot_response(self, response):
        """Maneja la respuesta del bot"""
        # Eliminar indicador de escritura
        try:
            if self.chat_layout.count() > 0:
                # Buscar el mensaje "Escribiendo..."
                for i in range(self.chat_layout.count()):
                    item = self.chat_layout.itemAt(i)
                    if item and item.widget():
                        widget = item.widget()
                        if isinstance(widget, MessageBubble):
                            # Verificar si es el mensaje "Escribiendo..."
                            for child in widget.children():
                                if hasattr(child, 'text') and child.text() == "Escribiendo...":
                                    widget.deleteLater()
                                    break
        except Exception as e:
            print(f"Error al eliminar indicador de escritura: {str(e)}")
        
        # Agregar respuesta del bot
        try:
            self.add_bot_message(response)
        except Exception as e:
            print(f"Error al agregar respuesta del bot: {str(e)}")

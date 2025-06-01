"""
Script para generar datos de prueba para la funcionalidad del Bot.
"""

import os
import django
from django.utils import timezone
from datetime import timedelta
import random

# Configurar el entorno de Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'granja.settings')
django.setup()

# Importar modelos
from django.contrib.auth import get_user_model
from bot.models import BotIntent, BotTrainingPhrase, BotResponse, BotConversation, BotMessage

User = get_user_model()

def create_bot_test_data():
    """
    Crea datos de prueba para la funcionalidad del Bot.
    """
    print("Generando datos de prueba para el Bot...")
    
    # Crear intenciones del bot
    if BotIntent.objects.count() == 0:
        print("Creando intenciones del bot...")
        
        # Intención de saludo
        saludo = BotIntent.objects.create(
            name="saludo",
            description="Saludos y bienvenida"
        )
        
        # Intención de consulta de estado de lotes
        estado_lotes = BotIntent.objects.create(
            name="consulta_estado_lotes",
            description="Consultas sobre el estado actual de los lotes"
        )
        
        # Intención de consulta de mortalidad
        mortalidad = BotIntent.objects.create(
            name="consulta_mortalidad",
            description="Consultas sobre tasas de mortalidad"
        )
        
        # Intención de consulta de producción
        produccion = BotIntent.objects.create(
            name="consulta_produccion",
            description="Consultas sobre niveles de producción"
        )
        
        # Intención de ayuda
        ayuda = BotIntent.objects.create(
            name="ayuda",
            description="Solicitudes de ayuda o información sobre el sistema"
        )
        
        # Intención de despedida
        despedida = BotIntent.objects.create(
            name="despedida",
            description="Despedidas y cierre de conversación"
        )
        
        print(f"Creadas {BotIntent.objects.count()} intenciones")
        
        # Crear frases de entrenamiento
        print("Creando frases de entrenamiento...")
        
        # Frases para saludo
        saludos = [
            "Hola", "Buenos días", "Buenas tardes", "Buenas noches", 
            "Saludos", "Qué tal", "Cómo estás", "Hola, ¿cómo estás?",
            "Hola bot", "Hey", "Inicio", "Comenzar"
        ]
        for texto in saludos:
            BotTrainingPhrase.objects.create(intent=saludo, text=texto)
        
        # Frases para consulta de estado de lotes
        consultas_lotes = [
            "¿Cómo están los lotes?", "Estado de los lotes", "Información de lotes",
            "Quiero saber sobre los lotes", "Dame información de los lotes activos",
            "¿Cuántos lotes hay activos?", "Estado actual de lotes", "Lotes activos",
            "Mostrar lotes", "Ver lotes", "Lotes disponibles"
        ]
        for texto in consultas_lotes:
            BotTrainingPhrase.objects.create(intent=estado_lotes, text=texto)
        
        # Frases para consulta de mortalidad
        consultas_mortalidad = [
            "¿Cuál es la tasa de mortalidad?", "Mortalidad actual", "Datos de mortalidad",
            "¿Cuántas aves han muerto?", "Estadísticas de mortalidad", "Mortalidad por lote",
            "Mortalidad semanal", "Reporte de mortalidad", "Mortalidad reciente"
        ]
        for texto in consultas_mortalidad:
            BotTrainingPhrase.objects.create(intent=mortalidad, text=texto)
        
        # Frases para consulta de producción
        consultas_produccion = [
            "¿Cómo va la producción?", "Datos de producción", "Estadísticas de producción",
            "Producción de huevos", "Producción semanal", "Reporte de producción",
            "¿Cuántos huevos se han producido?", "Rendimiento de producción",
            "Producción por lote", "Producción actual"
        ]
        for texto in consultas_produccion:
            BotTrainingPhrase.objects.create(intent=produccion, text=texto)
        
        # Frases para ayuda
        ayudas = [
            "Ayuda", "Necesito ayuda", "¿Cómo funciona esto?", "¿Qué puedes hacer?",
            "¿Qué comandos tienes?", "Instrucciones", "Manual", "Guía",
            "¿Cómo te uso?", "Opciones disponibles", "¿Qué puedo preguntarte?"
        ]
        for texto in ayudas:
            BotTrainingPhrase.objects.create(intent=ayuda, text=texto)
        
        # Frases para despedida
        despedidas = [
            "Adiós", "Hasta luego", "Chao", "Nos vemos", "Hasta pronto",
            "Gracias, adiós", "Terminar", "Finalizar", "Cerrar", "Salir",
            "Eso es todo", "Gracias por tu ayuda"
        ]
        for texto in despedidas:
            BotTrainingPhrase.objects.create(intent=despedida, text=texto)
        
        print(f"Creadas {BotTrainingPhrase.objects.count()} frases de entrenamiento")
        
        # Crear respuestas del bot
        print("Creando respuestas del bot...")
        
        # Respuestas para saludo
        BotResponse.objects.create(
            intent=saludo,
            text="¡Hola! Soy el asistente virtual de la granja. ¿En qué puedo ayudarte hoy?",
            order=0
        )
        BotResponse.objects.create(
            intent=saludo,
            text="¡Bienvenido! Estoy aquí para ayudarte con la gestión de tu granja avícola. ¿Qué necesitas?",
            order=1
        )
        BotResponse.objects.create(
            intent=saludo,
            text="¡Saludos! ¿En qué puedo asistirte hoy con respecto a tu granja?",
            order=2
        )
        
        # Respuestas para consulta de estado de lotes
        BotResponse.objects.create(
            intent=estado_lotes,
            text="Actualmente hay 3 lotes activos: 2 de ponedoras y 1 de engorde. Todos en buen estado sanitario.",
            order=0
        )
        BotResponse.objects.create(
            intent=estado_lotes,
            text="Los lotes actuales están en las siguientes etapas: Lote 1 (Producción), Lote 2 (Crecimiento), Lote 3 (Engorde final).",
            order=1
        )
        
        # Respuestas para consulta de mortalidad
        BotResponse.objects.create(
            intent=mortalidad,
            text="La tasa de mortalidad actual es del 2.3%, dentro de los parámetros normales para esta época del año.",
            order=0
        )
        BotResponse.objects.create(
            intent=mortalidad,
            text="En la última semana se registró una mortalidad del 0.5%, lo que indica un buen manejo sanitario.",
            order=1
        )
        
        # Respuestas para consulta de producción
        BotResponse.objects.create(
            intent=produccion,
            text="La producción actual es de 85% en el lote de ponedoras, con un promedio de 0.95 huevos por ave por día.",
            order=0
        )
        BotResponse.objects.create(
            intent=produccion,
            text="Esta semana la producción aumentó un 3% respecto a la semana anterior, alcanzando 10,500 huevos diarios.",
            order=1
        )
        
        # Respuestas para ayuda
        BotResponse.objects.create(
            intent=ayuda,
            text="Puedo ayudarte con información sobre: estado de lotes, mortalidad, producción, y más. Solo pregúntame lo que necesites saber.",
            order=0
        )
        BotResponse.objects.create(
            intent=ayuda,
            text="Estoy aquí para responder tus consultas sobre la granja. Puedes preguntarme sobre lotes, producción, mortalidad o cualquier otra información que necesites.",
            order=1
        )
        
        # Respuestas para despedida
        BotResponse.objects.create(
            intent=despedida,
            text="¡Hasta luego! Estoy aquí cuando me necesites.",
            order=0
        )
        BotResponse.objects.create(
            intent=despedida,
            text="¡Adiós! No dudes en volver si tienes más preguntas.",
            order=1
        )
        
        print(f"Creadas {BotResponse.objects.count()} respuestas del bot")
    
    # Crear conversaciones de ejemplo
    if BotConversation.objects.count() == 0:
        print("Creando conversaciones de ejemplo...")
        
        # Obtener usuario (si existe)
        user = None
        if User.objects.exists():
            user = User.objects.first()
        
        # Obtener intenciones
        intents = {intent.name: intent for intent in BotIntent.objects.all()}
        
        # Conversación 1: Consulta básica sobre lotes
        conv1 = BotConversation.objects.create(
            user=user,
            start_time=timezone.now() - timedelta(days=2, hours=3),
            end_time=timezone.now() - timedelta(days=2, hours=2, minutes=45),
            feedback_rating=5
        )
        
        # Mensajes de la conversación 1
        BotMessage.objects.create(
            conversation=conv1,
            sender='USER',
            text='Hola',
            timestamp=conv1.start_time,
            detected_intent=intents.get('saludo')
        )
        
        BotMessage.objects.create(
            conversation=conv1,
            sender='BOT',
            text='¡Hola! Soy el asistente virtual de la granja. ¿En qué puedo ayudarte hoy?',
            timestamp=conv1.start_time + timedelta(seconds=2),
            detected_intent=intents.get('saludo')
        )
        
        BotMessage.objects.create(
            conversation=conv1,
            sender='USER',
            text='¿Cómo están los lotes?',
            timestamp=conv1.start_time + timedelta(seconds=10),
            detected_intent=intents.get('consulta_estado_lotes')
        )
        
        BotMessage.objects.create(
            conversation=conv1,
            sender='BOT',
            text='Actualmente hay 3 lotes activos: 2 de ponedoras y 1 de engorde. Todos en buen estado sanitario.',
            timestamp=conv1.start_time + timedelta(seconds=12),
            detected_intent=intents.get('consulta_estado_lotes')
        )
        
        BotMessage.objects.create(
            conversation=conv1,
            sender='USER',
            text='¿Y cómo va la producción?',
            timestamp=conv1.start_time + timedelta(seconds=20),
            detected_intent=intents.get('consulta_produccion')
        )
        
        BotMessage.objects.create(
            conversation=conv1,
            sender='BOT',
            text='La producción actual es de 85% en el lote de ponedoras, con un promedio de 0.95 huevos por ave por día.',
            timestamp=conv1.start_time + timedelta(seconds=22),
            detected_intent=intents.get('consulta_produccion')
        )
        
        BotMessage.objects.create(
            conversation=conv1,
            sender='USER',
            text='Gracias, eso es todo',
            timestamp=conv1.start_time + timedelta(seconds=30),
            detected_intent=intents.get('despedida')
        )
        
        BotMessage.objects.create(
            conversation=conv1,
            sender='BOT',
            text='¡Hasta luego! Estoy aquí cuando me necesites.',
            timestamp=conv1.start_time + timedelta(seconds=32),
            detected_intent=intents.get('despedida')
        )
        
        # Conversación 2: Consulta sobre mortalidad
        conv2 = BotConversation.objects.create(
            user=user,
            start_time=timezone.now() - timedelta(days=1, hours=5),
            end_time=timezone.now() - timedelta(days=1, hours=4, minutes=50),
            feedback_rating=4
        )
        
        # Mensajes de la conversación 2
        BotMessage.objects.create(
            conversation=conv2,
            sender='USER',
            text='Buenos días',
            timestamp=conv2.start_time,
            detected_intent=intents.get('saludo')
        )
        
        BotMessage.objects.create(
            conversation=conv2,
            sender='BOT',
            text='¡Bienvenido! Estoy aquí para ayudarte con la gestión de tu granja avícola. ¿Qué necesitas?',
            timestamp=conv2.start_time + timedelta(seconds=2),
            detected_intent=intents.get('saludo')
        )
        
        BotMessage.objects.create(
            conversation=conv2,
            sender='USER',
            text='¿Cuál es la tasa de mortalidad actual?',
            timestamp=conv2.start_time + timedelta(seconds=10),
            detected_intent=intents.get('consulta_mortalidad')
        )
        
        BotMessage.objects.create(
            conversation=conv2,
            sender='BOT',
            text='La tasa de mortalidad actual es del 2.3%, dentro de los parámetros normales para esta época del año.',
            timestamp=conv2.start_time + timedelta(seconds=12),
            detected_intent=intents.get('consulta_mortalidad')
        )
        
        BotMessage.objects.create(
            conversation=conv2,
            sender='USER',
            text='¿Y cómo se compara con el mes pasado?',
            timestamp=conv2.start_time + timedelta(seconds=20),
            detected_intent=None  # Intención no detectada
        )
        
        BotMessage.objects.create(
            conversation=conv2,
            sender='BOT',
            text='Lo siento, no tengo información comparativa con el mes pasado. ¿Te gustaría consultar otra estadística?',
            timestamp=conv2.start_time + timedelta(seconds=22),
            detected_intent=None
        )
        
        BotMessage.objects.create(
            conversation=conv2,
            sender='USER',
            text='No, gracias. Adiós',
            timestamp=conv2.start_time + timedelta(seconds=30),
            detected_intent=intents.get('despedida')
        )
        
        BotMessage.objects.create(
            conversation=conv2,
            sender='BOT',
            text='¡Adiós! No dudes en volver si tienes más preguntas.',
            timestamp=conv2.start_time + timedelta(seconds=32),
            detected_intent=intents.get('despedida')
        )
        
        print(f"Creadas {BotConversation.objects.count()} conversaciones con {BotMessage.objects.count()} mensajes")
    
    print("Generación de datos de prueba para el Bot completada.")

if __name__ == "__main__":
    create_bot_test_data()

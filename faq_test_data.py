"""
Script para generar datos de prueba para el módulo de FAQ (Preguntas Frecuentes).
"""

import os
import django
from django.utils import timezone

# Configurar el entorno de Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'granja.settings')
django.setup()

# Importar modelos
from faq.models import FAQCategory, FAQ

def create_faq_test_data():
    """
    Crea datos de prueba para el módulo de FAQ.
    """
    print("Generando datos de prueba para el módulo de FAQ...")
    
    # Crear categorías de FAQ
    if FAQCategory.objects.count() == 0:
        print("Creando categorías de FAQ...")
        
        # Categoría: General
        cat_general = FAQCategory.objects.create(
            name="General",
            description="Preguntas generales sobre la aplicación",
            order=1
        )
        
        # Categoría: Producción
        cat_produccion = FAQCategory.objects.create(
            name="Producción",
            description="Preguntas relacionadas con la producción avícola",
            order=2
        )
        
        # Categoría: Sanidad
        cat_sanidad = FAQCategory.objects.create(
            name="Sanidad",
            description="Preguntas sobre sanidad y bienestar animal",
            order=3
        )
        
        # Categoría: Alimentación
        cat_alimentacion = FAQCategory.objects.create(
            name="Alimentación",
            description="Preguntas sobre alimentación y nutrición",
            order=4
        )
        
        # Categoría: Técnico
        cat_tecnico = FAQCategory.objects.create(
            name="Soporte Técnico",
            description="Preguntas sobre el uso de la aplicación",
            order=5
        )
        
        print(f"Creadas {FAQCategory.objects.count()} categorías de FAQ")
        
        # Crear preguntas frecuentes
        print("Creando preguntas frecuentes...")
        
        # Preguntas de la categoría General
        FAQ.objects.create(
            category=cat_general,
            question="¿Qué es App Granja?",
            answer="App Granja es una aplicación integral para la gestión de granjas avícolas. Permite llevar un control detallado de la producción, inventario, sanidad y más aspectos relacionados con la operación diaria de una granja avícola.",
            order=1,
            is_published=True
        )
        
        FAQ.objects.create(
            category=cat_general,
            question="¿Cómo puedo acceder a la aplicación?",
            answer="Puedes acceder a la aplicación a través de la web en cualquier navegador, o mediante la aplicación móvil disponible para Android e iOS. Necesitarás credenciales de acceso proporcionadas por el administrador del sistema.",
            order=2,
            is_published=True
        )
        
        FAQ.objects.create(
            category=cat_general,
            question="¿Es necesario tener conexión a internet para usar la aplicación?",
            answer="La aplicación web requiere conexión a internet. La aplicación móvil puede funcionar parcialmente sin conexión, pero necesitará sincronizarse cuando haya conexión disponible para actualizar los datos en el servidor.",
            order=3,
            is_published=True
        )
        
        # Preguntas de la categoría Producción
        FAQ.objects.create(
            category=cat_produccion,
            question="¿Cómo registro un nuevo lote de aves?",
            answer="Para registrar un nuevo lote, ve a la sección 'Producción' > 'Lotes' y haz clic en 'Nuevo Lote'. Completa la información requerida como fecha de ingreso, cantidad de aves, raza y galpón asignado.",
            order=1,
            is_published=True
        )
        
        FAQ.objects.create(
            category=cat_produccion,
            question="¿Cómo puedo ver las estadísticas de producción?",
            answer="Las estadísticas de producción están disponibles en el 'Dashboard' principal. También puedes acceder a reportes más detallados en la sección 'Estadísticas' > 'Producción', donde encontrarás gráficos y tablas con datos históricos.",
            order=2,
            is_published=True
        )
        
        FAQ.objects.create(
            category=cat_produccion,
            question="¿Cómo registro la producción diaria de huevos?",
            answer="Para registrar la producción diaria, ve a 'Producción' > 'Seguimiento Diario', selecciona el lote correspondiente y completa los datos de producción del día, incluyendo cantidad de huevos, clasificación por tamaño y observaciones relevantes.",
            order=3,
            is_published=True
        )
        
        # Preguntas de la categoría Sanidad
        FAQ.objects.create(
            category=cat_sanidad,
            question="¿Cómo registro la aplicación de una vacuna?",
            answer="Para registrar una vacunación, ve a 'Sanidad' > 'Registro de Vacunación', selecciona el lote, la vacuna aplicada, fecha, dosis y método de aplicación. También puedes añadir observaciones sobre la respuesta de las aves.",
            order=1,
            is_published=True
        )
        
        FAQ.objects.create(
            category=cat_sanidad,
            question="¿Cómo puedo llevar un control de la mortalidad?",
            answer="El registro de mortalidad se realiza en 'Producción' > 'Seguimiento Diario', donde puedes ingresar la cantidad de aves muertas y la causa probable. El sistema generará automáticamente reportes de mortalidad semanal y acumulada.",
            order=2,
            is_published=True
        )
        
        FAQ.objects.create(
            category=cat_sanidad,
            question="¿Qué debo hacer si detecto un brote de enfermedad?",
            answer="Si detectas signos de enfermedad, registra inmediatamente las observaciones en 'Sanidad' > 'Registro Sanitario'. Contacta a un veterinario y sigue el protocolo de bioseguridad establecido. La aplicación te permitirá dar seguimiento al evento sanitario.",
            order=3,
            is_published=True
        )
        
        # Preguntas de la categoría Alimentación
        FAQ.objects.create(
            category=cat_alimentacion,
            question="¿Cómo registro el consumo de alimento?",
            answer="El consumo de alimento se registra en 'Producción' > 'Seguimiento Diario', donde puedes ingresar la cantidad de alimento suministrado por lote. El sistema calculará automáticamente la conversión alimenticia.",
            order=1,
            is_published=True
        )
        
        FAQ.objects.create(
            category=cat_alimentacion,
            question="¿Cómo puedo saber si el consumo de alimento es adecuado?",
            answer="En la sección 'Estadísticas' > 'Alimentación' encontrarás comparativas entre el consumo real y el consumo esperado según la guía de la raza. También puedes consultar la conversión alimenticia y compararla con los parámetros ideales.",
            order=2,
            is_published=True
        )
        
        FAQ.objects.create(
            category=cat_alimentacion,
            question="¿Cómo gestiono el inventario de alimentos?",
            answer="El inventario de alimentos se gestiona en 'Inventario' > 'Alimentos', donde puedes registrar entradas, salidas y verificar el stock disponible. El sistema te alertará cuando el nivel de existencias esté por debajo del punto de reorden.",
            order=3,
            is_published=True
        )
        
        # Preguntas de la categoría Soporte Técnico
        FAQ.objects.create(
            category=cat_tecnico,
            question="¿Cómo puedo cambiar mi contraseña?",
            answer="Para cambiar tu contraseña, ve a 'Mi Perfil' en el menú superior derecho y selecciona 'Cambiar Contraseña'. Deberás ingresar tu contraseña actual y la nueva contraseña dos veces para confirmar.",
            order=1,
            is_published=True
        )
        
        FAQ.objects.create(
            category=cat_tecnico,
            question="¿Cómo puedo exportar datos para su análisis?",
            answer="Puedes exportar datos en formato Excel o CSV desde cualquier listado en la aplicación. Busca el botón 'Exportar' en la parte superior de la tabla de datos. También puedes generar reportes personalizados en la sección 'Reportes'.",
            order=2,
            is_published=True
        )
        
        FAQ.objects.create(
            category=cat_tecnico,
            question="¿Qué hago si encuentro un error en la aplicación?",
            answer="Si encuentras un error, por favor repórtalo a través de la sección 'Soporte' > 'Reportar Problema'. Incluye una descripción detallada del error, los pasos para reproducirlo y, si es posible, capturas de pantalla.",
            order=3,
            is_published=True
        )
        
        print(f"Creadas {FAQ.objects.count()} preguntas frecuentes")
    
    print("Generación de datos de prueba para el módulo de FAQ completada.")

if __name__ == "__main__":
    create_faq_test_data()

"""
Script para generar datos de prueba adicionales para el Bot relacionados con roles y permisos.
"""

import os
import django

# Configurar el entorno de Django primero
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'granja.settings')
django.setup()

# Importar después de configurar Django
from bot.models import BotIntent, BotTrainingPhrase, BotResponse

def create_bot_roles_data():
    """
    Crea datos de prueba para el Bot relacionados con roles y permisos.
    """
    print("Generando datos de prueba para el Bot relacionados con roles y permisos...")
    
    # Crear intención de consulta de roles
    roles_intent, created = BotIntent.objects.get_or_create(
        name="consulta_roles",
        defaults={"description": "Consultas sobre roles de usuario y permisos"}
    )
    
    if created:
        print("Creada intención 'consulta_roles'")
        
        # Frases para consulta de roles
        frases_roles = [
            "¿Qué roles hay en el sistema?",
            "¿Cuáles son los tipos de usuarios?",
            "¿Qué permisos tiene un operario?",
            "¿Qué puede hacer un supervisor?",
            "¿Qué diferencia hay entre un administrador y un supervisor?",
            "¿Qué puede hacer un veterinario?",
            "Roles de usuario",
            "Permisos de usuarios",
            "¿Qué grupos existen?",
            "¿Qué permisos tengo?",
            "¿Qué puedo hacer como operario?",
            "Funciones de un supervisor",
            "Acceso de administradores"
        ]
        
        for texto in frases_roles:
            BotTrainingPhrase.objects.create(intent=roles_intent, text=texto)
        
        print(f"Creadas {len(frases_roles)} frases de entrenamiento para 'consulta_roles'")
        
        # Respuestas para consulta de roles
        respuestas = [
            {
                "text": "En el sistema existen los siguientes roles de usuario:\n\n"
                        "- Administrador: Acceso completo a todas las funcionalidades.\n"
                        "- Supervisor: Gestión de granjas, galpones, lotes y seguimientos.\n"
                        "- Veterinario: Gestión de salud animal y seguimientos.\n"
                        "- Operario: Registro de datos diarios y consultas básicas.",
                "order": 0
            },
            {
                "text": "Los operarios pueden registrar datos diarios como seguimientos y mortalidad, "
                        "además de consultar información sobre granjas, galpones, lotes, alimentos, vacunas e insumos.",
                "order": 1
            },
            {
                "text": "Los supervisores pueden gestionar granjas, galpones, lotes, seguimientos, mortalidad, "
                        "alimentos, vacunas, insumos y proveedores. También pueden ver la wiki, FAQs y usar el asistente virtual.",
                "order": 2
            },
            {
                "text": "Los veterinarios pueden gestionar lotes, seguimientos, mortalidad y vacunas. "
                        "También pueden consultar información sobre granjas, galpones, alimentos e insumos.",
                "order": 3
            },
            {
                "text": "La principal diferencia entre roles es el nivel de acceso:\n\n"
                        "- Administradores: Control total del sistema\n"
                        "- Supervisores: Gestión operativa completa\n"
                        "- Veterinarios: Enfoque en salud animal\n"
                        "- Operarios: Registro de datos diarios",
                "order": 4
            }
        ]
        
        for respuesta in respuestas:
            BotResponse.objects.create(
                intent=roles_intent,
                text=respuesta["text"],
                order=respuesta["order"]
            )
        
        print(f"Creadas {len(respuestas)} respuestas para 'consulta_roles'")
    else:
        print("La intención 'consulta_roles' ya existe")
    
    # Crear intención de ayuda con permisos
    permisos_intent, created = BotIntent.objects.get_or_create(
        name="ayuda_permisos",
        defaults={"description": "Ayuda con problemas de permisos"}
    )
    
    if created:
        print("Creada intención 'ayuda_permisos'")
        
        # Frases para ayuda con permisos
        frases_permisos = [
            "No tengo acceso a",
            "No puedo acceder a",
            "No me deja entrar a",
            "Necesito permisos para",
            "¿Por qué no puedo ver?",
            "Error de permisos",
            "Acceso denegado",
            "No tengo permiso para",
            "Quiero acceder a",
            "Necesito usar",
            "No puedo modificar",
            "No puedo crear"
        ]
        
        for texto in frases_permisos:
            BotTrainingPhrase.objects.create(intent=permisos_intent, text=texto)
        
        print(f"Creadas {len(frases_permisos)} frases de entrenamiento para 'ayuda_permisos'")
        
        # Respuestas para ayuda con permisos
        respuestas = [
            {
                "text": "Si tienes problemas de acceso, es posible que no tengas los permisos necesarios para esa función. "
                        "Contacta con un administrador para que revise tus permisos según tu rol.",
                "order": 0
            },
            {
                "text": "Los permisos están asignados según tu rol en el sistema (Administrador, Supervisor, Veterinario u Operario). "
                        "Si necesitas acceso adicional, solicítalo a tu supervisor o al administrador del sistema.",
                "order": 1
            },
            {
                "text": "Para resolver problemas de permisos:\n\n"
                        "1. Verifica tu tipo de usuario en tu perfil\n"
                        "2. Confirma que estás asignado al grupo correcto\n"
                        "3. Contacta al administrador si necesitas permisos adicionales",
                "order": 2
            }
        ]
        
        for respuesta in respuestas:
            BotResponse.objects.create(
                intent=permisos_intent,
                text=respuesta["text"],
                order=respuesta["order"]
            )
        
        print(f"Creadas {len(respuestas)} respuestas para 'ayuda_permisos'")
    else:
        print("La intención 'ayuda_permisos' ya existe")
    
    print("Generación de datos de prueba para el Bot relacionados con roles y permisos completada.")

if __name__ == "__main__":
    create_bot_roles_data()

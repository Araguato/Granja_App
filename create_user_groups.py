"""
Script para crear grupos de usuarios y asignar permisos según los roles definidos.
"""

import os
import django

# Configurar el entorno de Django primero
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'granja.settings')
django.setup()

# Importar después de configurar Django
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType

# Importar modelos
from avicola.models import UserProfile
from produccion.models import Granja, Galpon, Lote, SeguimientoDiario, MortalidadDiaria
from inventario.models import Alimento, Vacuna, Insumo, Proveedor
from wiki.models import Category, Article
from faq.models import FAQCategory, FAQ
from bot.models import BotIntent, BotResponse, BotConversation

def create_user_groups():
    """
    Crea grupos de usuarios con permisos específicos según los roles.
    """
    print("Creando grupos de usuarios...")
    
    # Definir los grupos y sus permisos
    groups = {
        'Administradores': {
            'description': 'Acceso completo a todas las funcionalidades del sistema',
            'models': [
                UserProfile, Granja, Galpon, Lote, SeguimientoDiario, MortalidadDiaria,
                Alimento, Vacuna, Insumo, Proveedor, Category, Article, FAQCategory, FAQ,
                BotIntent, BotResponse, BotConversation
            ],
            'permissions': ['add', 'change', 'delete', 'view']
        },
        'Supervisores': {
            'description': 'Gestión de granjas, galpones, lotes y seguimientos',
            'models': [
                Granja, Galpon, Lote, SeguimientoDiario, MortalidadDiaria,
                Alimento, Vacuna, Insumo, Proveedor
            ],
            'permissions': ['add', 'change', 'view'],
            'extra_models': [
                Category, Article, FAQCategory, FAQ, BotConversation
            ],
            'extra_permissions': ['view']
        },
        'Veterinarios': {
            'description': 'Gestión de salud animal y seguimientos',
            'models': [
                Lote, SeguimientoDiario, MortalidadDiaria, Vacuna
            ],
            'permissions': ['add', 'change', 'view'],
            'extra_models': [
                Granja, Galpon, Alimento, Insumo, Category, Article, FAQCategory, FAQ, BotConversation
            ],
            'extra_permissions': ['view']
        },
        'Operarios': {
            'description': 'Registro de datos diarios y consultas básicas',
            'models': [
                SeguimientoDiario, MortalidadDiaria
            ],
            'permissions': ['add', 'change', 'view'],
            'extra_models': [
                Granja, Galpon, Lote, Alimento, Vacuna, Insumo, Category, Article, FAQCategory, FAQ, BotConversation
            ],
            'extra_permissions': ['view']
        }
    }
    
    # Crear los grupos y asignar permisos
    for group_name, group_data in groups.items():
        group, created = Group.objects.get_or_create(name=group_name)
        if created:
            print(f"Grupo '{group_name}' creado.")
        else:
            print(f"Grupo '{group_name}' ya existe.")
        
        # Asignar permisos principales
        for model in group_data['models']:
            content_type = ContentType.objects.get_for_model(model)
            for permission_name in group_data['permissions']:
                codename = f"{permission_name}_{model._meta.model_name}"
                try:
                    permission = Permission.objects.get(
                        codename=codename,
                        content_type=content_type,
                    )
                    group.permissions.add(permission)
                    print(f"  - Permiso '{permission.name}' añadido al grupo '{group_name}'")
                except Permission.DoesNotExist:
                    print(f"  - Permiso '{codename}' no encontrado para {model._meta.model_name}")
        
        # Asignar permisos adicionales
        if 'extra_models' in group_data and 'extra_permissions' in group_data:
            for model in group_data['extra_models']:
                content_type = ContentType.objects.get_for_model(model)
                for permission_name in group_data['extra_permissions']:
                    codename = f"{permission_name}_{model._meta.model_name}"
                    try:
                        permission = Permission.objects.get(
                            codename=codename,
                            content_type=content_type,
                        )
                        group.permissions.add(permission)
                        print(f"  - Permiso adicional '{permission.name}' añadido al grupo '{group_name}'")
                    except Permission.DoesNotExist:
                        print(f"  - Permiso adicional '{codename}' no encontrado para {model._meta.model_name}")
    
    print("Grupos de usuarios creados con éxito.")

def assign_users_to_groups():
    """
    Asigna usuarios existentes a los grupos según su tipo de usuario.
    """
    print("\nAsignando usuarios a grupos...")
    
    # Mapeo de tipos de usuario a grupos
    user_type_to_group = {
        'ADMIN': 'Administradores',
        'SUPERVISOR': 'Supervisores',
        'VETERINARIO': 'Veterinarios',
        'OPERARIO': 'Operarios',
    }
    
    # Obtener todos los usuarios
    users = UserProfile.objects.all()
    
    for user in users:
        group_name = user_type_to_group.get(user.user_type)
        if group_name:
            try:
                group = Group.objects.get(name=group_name)
                user.groups.add(group)
                print(f"Usuario '{user.username}' ({user.get_user_type_display()}) asignado al grupo '{group_name}'")
            except Group.DoesNotExist:
                print(f"Grupo '{group_name}' no encontrado para el usuario '{user.username}'")
    
    print("Asignación de usuarios a grupos completada.")

if __name__ == "__main__":
    create_user_groups()
    assign_users_to_groups()
    print("\nProceso completado con éxito.")

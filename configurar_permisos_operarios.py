#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Script para configurar permisos de operarios y crear dashboard específico
"""

import os
import sys
import django

# Configurar entorno Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'granja.settings')
django.setup()

from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.db.models import Q
from avicola.models import UserProfile  # Usar el modelo personalizado de usuario

def crear_permisos_operarios():
    """
    Crea permisos específicos para operarios
    """
    print("Creando permisos para operarios...")
    
    # Permisos para operarios
    permisos_operarios = [
        # Permisos para lotes
        {'app': 'produccion', 'model': 'lote', 'codename': 'view_lote', 'name': 'Puede ver lotes'},
        {'app': 'produccion', 'model': 'lote', 'codename': 'change_lote', 'name': 'Puede editar lotes'},
        {'app': 'produccion', 'model': 'lote', 'codename': 'add_seguimientodiario', 'name': 'Puede añadir seguimiento diario'},
        {'app': 'produccion', 'model': 'seguimientodiario', 'codename': 'view_seguimientodiario', 'name': 'Puede ver seguimiento diario'},
        {'app': 'produccion', 'model': 'seguimientodiario', 'codename': 'change_seguimientodiario', 'name': 'Puede editar seguimiento diario'},
        
        # Permisos para galpones
        {'app': 'produccion', 'model': 'galpon', 'codename': 'view_galpon', 'name': 'Puede ver galpones'},
        {'app': 'produccion', 'model': 'galpon', 'codename': 'change_galpon', 'name': 'Puede editar galpones'},
        
        # Permisos para dashboard
        {'app': 'avicola', 'model': 'dashboard', 'codename': 'view_dashboard_operario', 'name': 'Puede ver dashboard de operario'},
        
        # Permisos para tareas
        {'app': 'produccion', 'model': 'tarea', 'codename': 'view_tarea', 'name': 'Puede ver tareas'},
        {'app': 'produccion', 'model': 'tarea', 'codename': 'change_tarea', 'name': 'Puede editar tareas'},
        {'app': 'produccion', 'model': 'tarea', 'codename': 'add_tarea', 'name': 'Puede añadir tareas'},
        {'app': 'produccion', 'model': 'tarea', 'codename': 'complete_tarea', 'name': 'Puede completar tareas'},
        
        # Permisos para alimentos
        {'app': 'inventario', 'model': 'alimento', 'codename': 'view_alimento', 'name': 'Puede ver alimentos'},
        {'app': 'inventario', 'model': 'alimento', 'codename': 'change_alimento', 'name': 'Puede editar alimentos'},
        {'app': 'inventario', 'model': 'consumoalimento', 'codename': 'add_consumoalimento', 'name': 'Puede registrar consumo de alimentos'},
        {'app': 'inventario', 'model': 'consumoalimento', 'codename': 'view_consumoalimento', 'name': 'Puede ver consumo de alimentos'},
        {'app': 'inventario', 'model': 'consumoalimento', 'codename': 'change_consumoalimento', 'name': 'Puede editar consumo de alimentos'},
        
        # Permisos para vacunas
        {'app': 'inventario', 'model': 'vacuna', 'codename': 'view_vacuna', 'name': 'Puede ver vacunas'},
        {'app': 'inventario', 'model': 'aplicacionvacuna', 'codename': 'add_aplicacionvacuna', 'name': 'Puede registrar aplicación de vacunas'},
        {'app': 'inventario', 'model': 'aplicacionvacuna', 'codename': 'view_aplicacionvacuna', 'name': 'Puede ver aplicación de vacunas'},
        
        # Permisos para seguimiento de inventario
        {'app': 'inventario', 'model': 'seguimiento', 'codename': 'view_seguimiento', 'name': 'Puede ver seguimiento de inventario'},
        {'app': 'inventario', 'model': 'seguimiento', 'codename': 'add_seguimiento', 'name': 'Puede añadir seguimiento de inventario'},
        {'app': 'inventario', 'model': 'seguimiento', 'codename': 'change_seguimiento', 'name': 'Puede editar seguimiento de inventario'},
        
        # Permisos para wiki
        {'app': 'wiki', 'model': 'articulo', 'codename': 'view_articulo', 'name': 'Puede ver artículos de la wiki'},
        {'app': 'wiki', 'model': 'categoria', 'codename': 'view_categoria', 'name': 'Puede ver categorías de la wiki'},
        
        # Permisos para FAQ
        {'app': 'faq', 'model': 'pregunta', 'codename': 'view_pregunta', 'name': 'Puede ver preguntas frecuentes'},
        {'app': 'faq', 'model': 'categoria', 'codename': 'view_categoria', 'name': 'Puede ver categorías de FAQ'},
        
        # Permisos para bot
        {'app': 'bot', 'model': 'consulta', 'codename': 'add_consulta', 'name': 'Puede hacer consultas al bot'},
        {'app': 'bot', 'model': 'consulta', 'codename': 'view_consulta', 'name': 'Puede ver historial de consultas'},
        
        # Permisos para comparación de razas
        {'app': 'produccion', 'model': 'raza', 'codename': 'view_raza', 'name': 'Puede ver razas'},
        {'app': 'produccion', 'model': 'comparacionraza', 'codename': 'view_comparacionraza', 'name': 'Puede ver comparación de razas'},
    ]
    
    # Crear permisos
    for permiso in permisos_operarios:
        try:
            content_type = ContentType.objects.get(app_label=permiso['app'], model=permiso['model'])
            perm, created = Permission.objects.get_or_create(
                codename=permiso['codename'],
                name=permiso['name'],
                content_type=content_type,
            )
            if created:
                print(f"  Creado permiso: {permiso['name']}")
            else:
                print(f"  Ya existe permiso: {permiso['name']}")
        except ContentType.DoesNotExist:
            print(f"  Error: No existe content type para {permiso['app']}.{permiso['model']}")
        except Exception as e:
            print(f"  Error al crear permiso {permiso['name']}: {str(e)}")
    
    print("Permisos para operarios creados correctamente")

def configurar_grupo_operarios():
    """
    Configura el grupo de operarios con los permisos adecuados
    """
    print("\nConfigurando grupo de operarios...")
    
    # Obtener o crear grupo de operarios
    grupo_operarios, created = Group.objects.get_or_create(name='Operarios')
    if created:
        print("  Grupo 'Operarios' creado")
    else:
        print("  Grupo 'Operarios' ya existe")
    
    # Obtener permisos para operarios
    permisos = Permission.objects.filter(
        # Permisos de visualización para todos los modelos relevantes
        Q(codename__startswith='view_') |
        
        # Permisos de edición para modelos específicos
        Q(codename='change_lote') |
        Q(codename='change_galpon') |
        Q(codename='change_tarea') |
        Q(codename='change_alimento') |
        Q(codename='change_consumoalimento') |
        Q(codename='change_seguimientodiario') |
        Q(codename='change_seguimiento') |
        
        # Permisos para añadir registros
        Q(codename='add_tarea') |
        Q(codename='add_seguimientodiario') |
        Q(codename='add_seguimiento') |
        Q(codename='add_consumoalimento') |
        Q(codename='add_aplicacionvacuna') |
        Q(codename='add_consulta') |
        
        # Permisos especiales
        Q(codename='complete_tarea') |
        Q(codename='view_dashboard_operario')
    )
    
    # Asignar permisos al grupo
    grupo_operarios.permissions.set(permisos)
    
    print(f"  Asignados {permisos.count()} permisos al grupo 'Operarios'")
    print("Grupo de operarios configurado correctamente")

def asignar_permisos_a_usuario(username):
    """
    Asigna permisos específicos a un usuario operario
    """
    print(f"\nAsignando permisos al usuario '{username}'...")
    
    try:
        # Obtener usuario
        usuario = UserProfile.objects.get(username=username)
        
        # Obtener grupo de operarios
        grupo_operarios = Group.objects.get(name='Operarios')
        
        # Asignar grupo al usuario
        usuario.groups.add(grupo_operarios)
        
        # Guardar usuario
        usuario.save()
        
        print(f"Permisos asignados correctamente al usuario '{username}'")
        return True
    except UserProfile.DoesNotExist:
        print(f"El usuario '{username}' no existe")
        return False
    except Group.DoesNotExist:
        print("El grupo 'Operarios' no existe")
        return False
    except Exception as e:
        print(f"Error al asignar permisos: {str(e)}")
        return False

def crear_usuario_operario(username, password, email, nombre, apellido):
    """
    Crea un usuario operario si no existe
    """
    print(f"\nCreando usuario operario '{username}'...")
    
    try:
        # Verificar si el usuario ya existe
        if UserProfile.objects.filter(username=username).exists():
            print(f"El usuario '{username}' ya existe")
            return True
        
        # Crear usuario
        usuario = UserProfile.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=nombre,
            last_name=apellido
        )
        
        print(f"Usuario '{username}' creado correctamente")
        return True
    except Exception as e:
        print(f"Error al crear usuario '{username}': {str(e)}")
        return False

def main():
    """
    Función principal
    """
    print("=" * 60)
    print("CONFIGURACIÓN DE PERMISOS Y DASHBOARD PARA OPERARIOS")
    print("=" * 60)
    
    # Crear permisos
    crear_permisos_operarios()
    
    # Configurar grupo de operarios
    configurar_grupo_operarios()
    
    # Crear usuario operario si no existe
    crear_usuario_operario(
        username='pedro',
        password='pedro123',
        email='pedro@granjaapp.com',
        nombre='Pedro',
        apellido='Operario'
    )
    
    # Asignar permisos a usuario Pedro
    asignar_permisos_a_usuario('pedro')
    
    print("\nConfiguración completada")
    print("=" * 60)

if __name__ == "__main__":
    main()

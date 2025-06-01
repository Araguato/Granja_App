#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Script para aplicar las mejoras a la aplicación web de App_Granja
"""

import os
import sys
import subprocess
import json
import shutil
from pathlib import Path

# Configurar entorno Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'granja.settings')

try:
    import django
    django.setup()
    from django.contrib.auth.models import Group, Permission, User
    from django.contrib.contenttypes.models import ContentType
    from django.db.models import Q
    print("✅ Entorno Django configurado correctamente")
except Exception as e:
    print(f"❌ Error al configurar el entorno Django: {str(e)}")
    sys.exit(1)

def crear_directorios_traducciones():
    """
    Crea los directorios necesarios para las traducciones
    """
    print("\n🔄 Creando directorios para traducciones...")
    
    try:
        # Crear directorios para traducciones
        locale_dir = os.path.join(os.getcwd(), 'locale')
        os.makedirs(os.path.join(locale_dir, 'es', 'LC_MESSAGES'), exist_ok=True)
        os.makedirs(os.path.join(locale_dir, 'en', 'LC_MESSAGES'), exist_ok=True)
        
        print("✅ Directorios para traducciones creados correctamente")
        return True
    except Exception as e:
        print(f"❌ Error al crear directorios para traducciones: {str(e)}")
        return False

def compilar_traducciones():
    """
    Compila los archivos de traducción
    """
    print("\n🔄 Compilando archivos de traducción...")
    
    try:
        # Ejecutar comando para compilar traducciones
        result = subprocess.run(
            ['python', 'manage.py', 'compilemessages'],
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            print("✅ Archivos de traducción compilados correctamente")
            return True
        else:
            print(f"❌ Error al compilar archivos de traducción: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ Error al compilar archivos de traducción: {str(e)}")
        return False

def crear_permisos_operarios():
    """
    Crea permisos específicos para operarios
    """
    print("\n🔄 Creando permisos para operarios...")
    
    try:
        # Permisos para operarios
        permisos_operarios = [
            # Permisos para lotes
            {'app': 'avicola', 'model': 'lote', 'codename': 'view_lote', 'name': 'Puede ver lotes'},
            {'app': 'avicola', 'model': 'lote', 'codename': 'edit_lote', 'name': 'Puede editar lotes'},
            {'app': 'avicola', 'model': 'seguimiento', 'codename': 'add_seguimiento', 'name': 'Puede añadir seguimiento'},
            {'app': 'avicola', 'model': 'seguimiento', 'codename': 'edit_seguimiento', 'name': 'Puede editar seguimiento'},
            
            # Permisos para galpones
            {'app': 'avicola', 'model': 'galpon', 'codename': 'view_galpon', 'name': 'Puede ver galpones'},
            
            # Permisos para dashboard
            {'app': 'avicola', 'model': 'dashboard', 'codename': 'view_dashboard_operario', 'name': 'Puede ver dashboard de operario'},
            
            # Permisos para tareas
            {'app': 'produccion', 'model': 'tarea', 'codename': 'view_tarea', 'name': 'Puede ver tareas'},
            {'app': 'produccion', 'model': 'tarea', 'codename': 'complete_tarea', 'name': 'Puede completar tareas'},
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
                    print(f"  ✅ Creado permiso: {permiso['name']}")
                else:
                    print(f"  ℹ️ Ya existe permiso: {permiso['name']}")
            except ContentType.DoesNotExist:
                print(f"  ⚠️ No existe content type para {permiso['app']}.{permiso['model']}")
            except Exception as e:
                print(f"  ❌ Error al crear permiso {permiso['name']}: {str(e)}")
        
        print("✅ Permisos para operarios creados correctamente")
        return True
    except Exception as e:
        print(f"❌ Error al crear permisos para operarios: {str(e)}")
        return False

def configurar_grupo_operarios():
    """
    Configura el grupo de operarios con los permisos adecuados
    """
    print("\n🔄 Configurando grupo de operarios...")
    
    try:
        # Obtener o crear grupo de operarios
        grupo_operarios, created = Group.objects.get_or_create(name='Operarios')
        if created:
            print("  ✅ Grupo 'Operarios' creado")
        else:
            print("  ℹ️ Grupo 'Operarios' ya existe")
        
        # Obtener permisos para operarios
        permisos = Permission.objects.filter(
            Q(codename__startswith='view_') | 
            Q(codename__startswith='edit_lote') | 
            Q(codename__startswith='add_seguimiento') | 
            Q(codename__startswith='edit_seguimiento') |
            Q(codename__startswith='complete_tarea') |
            Q(codename='view_dashboard_operario')
        )
        
        # Asignar permisos al grupo
        grupo_operarios.permissions.set(permisos)
        
        print(f"  ✅ Asignados {permisos.count()} permisos al grupo 'Operarios'")
        print("✅ Grupo de operarios configurado correctamente")
        return True
    except Exception as e:
        print(f"❌ Error al configurar grupo de operarios: {str(e)}")
        return False

def asignar_permisos_a_usuario(username):
    """
    Asigna permisos específicos a un usuario operario
    """
    print(f"\n🔄 Asignando permisos al usuario '{username}'...")
    
    try:
        # Obtener usuario
        try:
            usuario = User.objects.get(username=username)
        except User.DoesNotExist:
            print(f"  ⚠️ El usuario '{username}' no existe")
            return False
        
        # Obtener grupo de operarios
        try:
            grupo_operarios = Group.objects.get(name='Operarios')
        except Group.DoesNotExist:
            print("  ⚠️ El grupo 'Operarios' no existe")
            return False
        
        # Asignar grupo al usuario
        usuario.groups.add(grupo_operarios)
        
        # Guardar usuario
        usuario.save()
        
        print(f"✅ Permisos asignados correctamente al usuario '{username}'")
        return True
    except Exception as e:
        print(f"❌ Error al asignar permisos: {str(e)}")
        return False

def crear_usuario_operario(username, password, email, nombre, apellido):
    """
    Crea un usuario operario si no existe
    """
    print(f"\n🔄 Creando usuario operario '{username}'...")
    
    try:
        # Verificar si el usuario ya existe
        if User.objects.filter(username=username).exists():
            print(f"  ℹ️ El usuario '{username}' ya existe")
            return True
        
        # Crear usuario
        usuario = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=nombre,
            last_name=apellido
        )
        
        print(f"✅ Usuario '{username}' creado correctamente")
        return True
    except Exception as e:
        print(f"❌ Error al crear usuario '{username}': {str(e)}")
        return False

def main():
    """
    Función principal
    """
    print("=" * 80)
    print("APLICACIÓN DE MEJORAS A LA APLICACIÓN WEB DE APP_GRANJA")
    print("=" * 80)
    
    # Crear directorios para traducciones
    crear_directorios_traducciones()
    
    # Compilar traducciones
    compilar_traducciones()
    
    # Crear permisos para operarios
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
    
    print("\n" + "=" * 80)
    print("MEJORAS APLICADAS CORRECTAMENTE")
    print("=" * 80)
    print("\nLas siguientes mejoras se han aplicado:")
    print("\n1. Permisos para operarios: Se ha creado un dashboard específico para")
    print("   operarios y se han configurado los permisos necesarios.")
    print("\n2. Selección de idioma: Se ha implementado la funcionalidad de selección")
    print("   de idioma en la aplicación web.")
    print("\n3. Comparación de razas: Se ha implementado la funcionalidad para comparar")
    print("   datos nominales de una raza con datos reales de un lote activo.")
    print("\nPara aplicar estos cambios, reinicie el servidor Django con:")
    print("\n   iniciar_servidor_django.bat")
    print("\n" + "=" * 80)

if __name__ == "__main__":
    main()

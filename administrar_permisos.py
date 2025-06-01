#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Script para administrar permisos de grupos en App_Granja
Permite ver y modificar los permisos de cada grupo de manera sencilla
"""

import os
import sys
import django
import argparse
import json
from collections import defaultdict

# Configurar entorno Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'granja.settings')
django.setup()

from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.db.models import Q
from avicola.models import UserProfile  # Usar el modelo personalizado de usuario

def obtener_todos_los_permisos():
    """
    Obtiene todos los permisos disponibles en el sistema organizados por app y modelo
    """
    permisos_por_app_modelo = defaultdict(lambda: defaultdict(list))
    
    for content_type in ContentType.objects.all().order_by('app_label', 'model'):
        app_label = content_type.app_label
        model = content_type.model
        
        permisos = Permission.objects.filter(content_type=content_type).order_by('codename')
        for permiso in permisos:
            accion = permiso.codename.split('_')[0]  # add, change, delete, view, etc.
            permisos_por_app_modelo[app_label][model].append({
                'id': permiso.id,
                'codename': permiso.codename,
                'name': permiso.name,
                'accion': accion
            })
    
    return permisos_por_app_modelo

def obtener_permisos_grupo(nombre_grupo):
    """
    Obtiene los permisos asignados a un grupo específico
    """
    try:
        grupo = Group.objects.get(name=nombre_grupo)
        permisos = grupo.permissions.all().order_by('content_type__app_label', 'content_type__model', 'codename')
        
        permisos_grupo = defaultdict(lambda: defaultdict(list))
        for permiso in permisos:
            app_label = permiso.content_type.app_label
            model = permiso.content_type.model
            accion = permiso.codename.split('_')[0]  # add, change, delete, view, etc.
            
            permisos_grupo[app_label][model].append({
                'id': permiso.id,
                'codename': permiso.codename,
                'name': permiso.name,
                'accion': accion
            })
        
        return permisos_grupo
    except Group.DoesNotExist:
        print(f"Error: El grupo '{nombre_grupo}' no existe")
        return None

def mostrar_permisos_grupo(nombre_grupo):
    """
    Muestra los permisos asignados a un grupo específico de manera organizada
    """
    try:
        grupo = Group.objects.get(name=nombre_grupo)
        permisos_grupo = obtener_permisos_grupo(nombre_grupo)
        
        if not permisos_grupo:
            print(f"El grupo '{nombre_grupo}' no tiene permisos asignados")
            return
        
        print(f"\nPermisos del grupo: {nombre_grupo}")
        print("=" * 80)
        
        # Contar usuarios en el grupo
        num_usuarios = UserProfile.objects.filter(groups=grupo).count()
        print(f"Usuarios en el grupo: {num_usuarios}")
        print("-" * 80)
        
        for app_label in sorted(permisos_grupo.keys()):
            print(f"\nAplicación: {app_label}")
            print("-" * 50)
            
            for model in sorted(permisos_grupo[app_label].keys()):
                print(f"  Modelo: {model}")
                
                # Agrupar permisos por modelo
                permisos = permisos_grupo[app_label][model]
                acciones = [p['accion'] for p in permisos]
                
                # Mostrar permisos de forma más legible
                if 'add' in acciones:
                    print("    ✓ Crear")
                if 'change' in acciones:
                    print("    ✓ Editar")
                if 'delete' in acciones:
                    print("    ✓ Eliminar")
                if 'view' in acciones:
                    print("    ✓ Ver")
                
                # Mostrar permisos personalizados
                for permiso in permisos:
                    if permiso['accion'] not in ['add', 'change', 'delete', 'view']:
                        print(f"    ✓ {permiso['name']}")
    
    except Group.DoesNotExist:
        print(f"Error: El grupo '{nombre_grupo}' no existe")

def exportar_permisos_grupo(nombre_grupo, archivo_salida):
    """
    Exporta los permisos de un grupo a un archivo JSON
    """
    try:
        grupo = Group.objects.get(name=nombre_grupo)
        permisos_grupo = obtener_permisos_grupo(nombre_grupo)
        
        if not permisos_grupo:
            print(f"El grupo '{nombre_grupo}' no tiene permisos asignados")
            return False
        
        # Convertir a formato más simple para JSON
        permisos_json = {}
        for app_label, modelos in permisos_grupo.items():
            permisos_json[app_label] = {}
            for model, permisos in modelos.items():
                permisos_json[app_label][model] = [p['codename'] for p in permisos]
        
        # Guardar en archivo JSON
        with open(archivo_salida, 'w', encoding='utf-8') as f:
            json.dump(permisos_json, f, indent=4, ensure_ascii=False)
        
        print(f"Permisos del grupo '{nombre_grupo}' exportados a {archivo_salida}")
        return True
    
    except Group.DoesNotExist:
        print(f"Error: El grupo '{nombre_grupo}' no existe")
        return False
    except Exception as e:
        print(f"Error al exportar permisos: {str(e)}")
        return False

def importar_permisos_grupo(nombre_grupo, archivo_entrada):
    """
    Importa permisos para un grupo desde un archivo JSON
    """
    try:
        # Verificar si el grupo existe
        grupo, created = Group.objects.get_or_create(name=nombre_grupo)
        if created:
            print(f"Grupo '{nombre_grupo}' creado")
        
        # Leer archivo JSON
        with open(archivo_entrada, 'r', encoding='utf-8') as f:
            permisos_json = json.load(f)
        
        # Convertir a lista de permisos
        permisos_ids = []
        for app_label, modelos in permisos_json.items():
            for model, codenames in modelos.items():
                try:
                    content_type = ContentType.objects.get(app_label=app_label, model=model)
                    for codename in codenames:
                        try:
                            permiso = Permission.objects.get(content_type=content_type, codename=codename)
                            permisos_ids.append(permiso.id)
                        except Permission.DoesNotExist:
                            print(f"  Advertencia: Permiso '{codename}' no encontrado para {app_label}.{model}")
                except ContentType.DoesNotExist:
                    print(f"  Advertencia: ContentType para '{app_label}.{model}' no encontrado")
        
        # Asignar permisos al grupo
        permisos = Permission.objects.filter(id__in=permisos_ids)
        grupo.permissions.set(permisos)
        
        print(f"Permisos importados correctamente para el grupo '{nombre_grupo}'")
        print(f"Se asignaron {len(permisos_ids)} permisos")
        return True
    
    except Exception as e:
        print(f"Error al importar permisos: {str(e)}")
        return False

def agregar_permiso_grupo(nombre_grupo, app_label, model, codename):
    """
    Agrega un permiso específico a un grupo
    """
    try:
        # Verificar si el grupo existe
        grupo = Group.objects.get(name=nombre_grupo)
        
        # Verificar si el content type existe
        try:
            content_type = ContentType.objects.get(app_label=app_label, model=model)
        except ContentType.DoesNotExist:
            print(f"Error: ContentType para '{app_label}.{model}' no encontrado")
            return False
        
        # Verificar si el permiso existe
        try:
            permiso = Permission.objects.get(content_type=content_type, codename=codename)
        except Permission.DoesNotExist:
            print(f"Error: Permiso '{codename}' no encontrado para {app_label}.{model}")
            return False
        
        # Agregar permiso al grupo
        if permiso in grupo.permissions.all():
            print(f"El permiso '{codename}' ya está asignado al grupo '{nombre_grupo}'")
            return True
        
        grupo.permissions.add(permiso)
        print(f"Permiso '{codename}' agregado correctamente al grupo '{nombre_grupo}'")
        return True
    
    except Group.DoesNotExist:
        print(f"Error: El grupo '{nombre_grupo}' no existe")
        return False
    except Exception as e:
        print(f"Error al agregar permiso: {str(e)}")
        return False

def eliminar_permiso_grupo(nombre_grupo, app_label, model, codename):
    """
    Elimina un permiso específico de un grupo
    """
    try:
        # Verificar si el grupo existe
        grupo = Group.objects.get(name=nombre_grupo)
        
        # Verificar si el content type existe
        try:
            content_type = ContentType.objects.get(app_label=app_label, model=model)
        except ContentType.DoesNotExist:
            print(f"Error: ContentType para '{app_label}.{model}' no encontrado")
            return False
        
        # Verificar si el permiso existe
        try:
            permiso = Permission.objects.get(content_type=content_type, codename=codename)
        except Permission.DoesNotExist:
            print(f"Error: Permiso '{codename}' no encontrado para {app_label}.{model}")
            return False
        
        # Eliminar permiso del grupo
        if permiso not in grupo.permissions.all():
            print(f"El permiso '{codename}' no está asignado al grupo '{nombre_grupo}'")
            return True
        
        grupo.permissions.remove(permiso)
        print(f"Permiso '{codename}' eliminado correctamente del grupo '{nombre_grupo}'")
        return True
    
    except Group.DoesNotExist:
        print(f"Error: El grupo '{nombre_grupo}' no existe")
        return False
    except Exception as e:
        print(f"Error al eliminar permiso: {str(e)}")
        return False

def listar_grupos():
    """
    Lista todos los grupos disponibles en el sistema
    """
    grupos = Group.objects.all().order_by('name')
    
    if not grupos:
        print("No hay grupos en el sistema")
        return
    
    print("\nGrupos disponibles:")
    print("-" * 50)
    
    for grupo in grupos:
        num_usuarios = UserProfile.objects.filter(groups=grupo).count()
        num_permisos = grupo.permissions.count()
        print(f"- {grupo.name} ({num_usuarios} usuarios, {num_permisos} permisos)")

def listar_permisos_disponibles():
    """
    Lista todos los permisos disponibles en el sistema
    """
    permisos_por_app_modelo = obtener_todos_los_permisos()
    
    print("\nPermisos disponibles en el sistema:")
    print("=" * 80)
    
    for app_label in sorted(permisos_por_app_modelo.keys()):
        print(f"\nAplicación: {app_label}")
        print("-" * 50)
        
        for model in sorted(permisos_por_app_modelo[app_label].keys()):
            print(f"  Modelo: {model}")
            
            # Agrupar permisos por modelo
            permisos = permisos_por_app_modelo[app_label][model]
            for permiso in permisos:
                print(f"    - {permiso['codename']}: {permiso['name']}")

def main():
    """
    Función principal
    """
    parser = argparse.ArgumentParser(description='Administración de permisos para grupos en App_Granja')
    
    # Subparsers para comandos
    subparsers = parser.add_subparsers(dest='comando', help='Comandos disponibles')
    
    # Comando 'listar-grupos'
    listar_grupos_parser = subparsers.add_parser('listar-grupos', help='Lista todos los grupos disponibles')
    
    # Comando 'listar-permisos'
    listar_permisos_parser = subparsers.add_parser('listar-permisos', help='Lista todos los permisos disponibles en el sistema')
    
    # Comando 'ver-permisos'
    ver_permisos_parser = subparsers.add_parser('ver-permisos', help='Muestra los permisos asignados a un grupo')
    ver_permisos_parser.add_argument('grupo', help='Nombre del grupo')
    
    # Comando 'exportar-permisos'
    exportar_permisos_parser = subparsers.add_parser('exportar-permisos', help='Exporta los permisos de un grupo a un archivo JSON')
    exportar_permisos_parser.add_argument('grupo', help='Nombre del grupo')
    exportar_permisos_parser.add_argument('archivo', help='Ruta del archivo de salida')
    
    # Comando 'importar-permisos'
    importar_permisos_parser = subparsers.add_parser('importar-permisos', help='Importa permisos para un grupo desde un archivo JSON')
    importar_permisos_parser.add_argument('grupo', help='Nombre del grupo')
    importar_permisos_parser.add_argument('archivo', help='Ruta del archivo de entrada')
    
    # Comando 'agregar-permiso'
    agregar_permiso_parser = subparsers.add_parser('agregar-permiso', help='Agrega un permiso específico a un grupo')
    agregar_permiso_parser.add_argument('grupo', help='Nombre del grupo')
    agregar_permiso_parser.add_argument('app', help='Nombre de la aplicación (app_label)')
    agregar_permiso_parser.add_argument('modelo', help='Nombre del modelo')
    agregar_permiso_parser.add_argument('permiso', help='Nombre del permiso (codename)')
    
    # Comando 'eliminar-permiso'
    eliminar_permiso_parser = subparsers.add_parser('eliminar-permiso', help='Elimina un permiso específico de un grupo')
    eliminar_permiso_parser.add_argument('grupo', help='Nombre del grupo')
    eliminar_permiso_parser.add_argument('app', help='Nombre de la aplicación (app_label)')
    eliminar_permiso_parser.add_argument('modelo', help='Nombre del modelo')
    eliminar_permiso_parser.add_argument('permiso', help='Nombre del permiso (codename)')
    
    # Parsear argumentos
    args = parser.parse_args()
    
    # Ejecutar comando correspondiente
    if args.comando == 'listar-grupos':
        listar_grupos()
    elif args.comando == 'listar-permisos':
        listar_permisos_disponibles()
    elif args.comando == 'ver-permisos':
        mostrar_permisos_grupo(args.grupo)
    elif args.comando == 'exportar-permisos':
        exportar_permisos_grupo(args.grupo, args.archivo)
    elif args.comando == 'importar-permisos':
        importar_permisos_grupo(args.grupo, args.archivo)
    elif args.comando == 'agregar-permiso':
        agregar_permiso_grupo(args.grupo, args.app, args.modelo, args.permiso)
    elif args.comando == 'eliminar-permiso':
        eliminar_permiso_grupo(args.grupo, args.app, args.modelo, args.permiso)
    else:
        # Si no se especifica un comando, mostrar la ayuda
        parser.print_help()
        print("\nEjemplos de uso:")
        print("  python administrar_permisos.py listar-grupos")
        print("  python administrar_permisos.py ver-permisos Operarios")
        print("  python administrar_permisos.py exportar-permisos Operarios permisos_operarios.json")
        print("  python administrar_permisos.py importar-permisos NuevoGrupo permisos_operarios.json")
        print("  python administrar_permisos.py agregar-permiso Operarios produccion lote view_lote")
        print("  python administrar_permisos.py eliminar-permiso Operarios produccion lote delete_lote")

if __name__ == "__main__":
    main()

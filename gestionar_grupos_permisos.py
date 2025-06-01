#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Script para gestionar grupos y permisos en App_Granja
Permite crear grupos, asignar permisos a grupos y asignar usuarios a grupos
"""

import os
import sys
import django
import argparse

# Configurar entorno Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'granja.settings')
django.setup()

from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.db.models import Q
from avicola.models import UserProfile  # Usar el modelo personalizado de usuario

# Definición de grupos y sus permisos
GRUPOS_PERMISOS = {
    'Administradores': {
        'descripcion': 'Acceso completo a todas las funcionalidades del sistema',
        'permisos': {
            'all': ['add', 'change', 'delete', 'view']
        }
    },
    'Gerentes': {
        'descripcion': 'Acceso a reportes, estadísticas y gestión de usuarios',
        'permisos': {
            'all': ['view'],
            'produccion.lote': ['add', 'change', 'view'],
            'produccion.galpon': ['add', 'change', 'view'],
            'produccion.tarea': ['add', 'change', 'view', 'complete'],
            'inventario.alimento': ['add', 'change', 'view'],
            'inventario.vacuna': ['add', 'change', 'view'],
            'reportes.reporte': ['add', 'change', 'view'],
        }
    },
    'Operarios': {
        'descripcion': 'Acceso a tareas diarias, seguimiento y registro de datos',
        'permisos': {
            'produccion.lote': ['view', 'change'],
            'produccion.galpon': ['view', 'change'],
            'produccion.tarea': ['view', 'change', 'add', 'complete'],
            'produccion.seguimientodiario': ['view', 'change', 'add'],
            'produccion.raza': ['view'],
            'produccion.comparacionraza': ['view'],
            'inventario.alimento': ['view', 'change'],
            'inventario.consumoalimento': ['view', 'change', 'add'],
            'inventario.vacuna': ['view'],
            'inventario.aplicacionvacuna': ['view', 'add'],
            'inventario.seguimiento': ['view', 'change', 'add'],
            'wiki.articulo': ['view'],
            'wiki.categoria': ['view'],
            'faq.pregunta': ['view'],
            'faq.categoria': ['view'],
            'bot.consulta': ['view', 'add'],
            'avicola.dashboard': ['view_dashboard_operario']
        }
    },
    'Veterinarios': {
        'descripcion': 'Acceso a seguimiento de salud, vacunaciones y tratamientos',
        'permisos': {
            'produccion.lote': ['view'],
            'produccion.galpon': ['view'],
            'produccion.seguimientodiario': ['view', 'change', 'add'],
            'inventario.vacuna': ['view', 'change', 'add'],
            'inventario.aplicacionvacuna': ['view', 'change', 'add'],
            'wiki.articulo': ['view'],
            'faq.pregunta': ['view'],
            'bot.consulta': ['view', 'add']
        }
    },
    'Vendedores': {
        'descripcion': 'Acceso a ventas, clientes e inventario de productos',
        'permisos': {
            'ventas.venta': ['view', 'change', 'add'],
            'ventas.cliente': ['view', 'change', 'add'],
            'ventas.tipohuevo': ['view'],
            'ventas.inventariohuevos': ['view'],
            'produccion.lote': ['view'],
            'wiki.articulo': ['view'],
            'faq.pregunta': ['view'],
            'bot.consulta': ['view', 'add']
        }
    }
}

def crear_grupos():
    """
    Crea los grupos definidos en GRUPOS_PERMISOS si no existen
    """
    print("\nCreando grupos...")
    
    for nombre_grupo, datos in GRUPOS_PERMISOS.items():
        grupo, created = Group.objects.get_or_create(name=nombre_grupo)
        if created:
            print(f"  Grupo '{nombre_grupo}' creado - {datos['descripcion']}")
        else:
            print(f"  Grupo '{nombre_grupo}' ya existe")
    
    print("Grupos creados correctamente")

def asignar_permisos_a_grupos():
    """
    Asigna los permisos definidos en GRUPOS_PERMISOS a cada grupo
    """
    print("\nAsignando permisos a grupos...")
    
    for nombre_grupo, datos in GRUPOS_PERMISOS.items():
        try:
            grupo = Group.objects.get(name=nombre_grupo)
            permisos_grupo = []
            
            # Procesar permisos para todos los modelos
            if 'all' in datos['permisos']:
                acciones = datos['permisos']['all']
                for content_type in ContentType.objects.all():
                    app_model = f"{content_type.app_label}.{content_type.model}"
                    for accion in acciones:
                        codename = f"{accion}_{content_type.model}"
                        try:
                            permiso = Permission.objects.get(
                                content_type=content_type,
                                codename=codename
                            )
                            permisos_grupo.append(permiso)
                        except Permission.DoesNotExist:
                            # Algunos modelos no tienen todos los permisos estándar
                            pass
            
            # Procesar permisos específicos por modelo
            for app_model, acciones in datos['permisos'].items():
                if app_model == 'all':
                    continue
                
                try:
                    app_label, model = app_model.split('.')
                    content_type = ContentType.objects.get(app_label=app_label, model=model)
                    
                    for accion in acciones:
                        if accion in ['add', 'change', 'delete', 'view']:
                            codename = f"{accion}_{model}"
                        else:
                            # Permisos personalizados como 'complete_tarea'
                            codename = f"{accion}_{model}"
                        
                        try:
                            permiso = Permission.objects.get(
                                content_type=content_type,
                                codename=codename
                            )
                            permisos_grupo.append(permiso)
                        except Permission.DoesNotExist:
                            print(f"    Permiso '{codename}' no encontrado para {app_model}")
                except ContentType.DoesNotExist:
                    print(f"    ContentType para '{app_model}' no encontrado")
                except ValueError:
                    print(f"    Formato incorrecto para '{app_model}', debe ser 'app_label.model'")
            
            # Asignar permisos al grupo
            grupo.permissions.set(permisos_grupo)
            print(f"  Asignados {len(permisos_grupo)} permisos al grupo '{nombre_grupo}'")
            
        except Group.DoesNotExist:
            print(f"  Error: Grupo '{nombre_grupo}' no existe")
    
    print("Permisos asignados correctamente")

def listar_usuarios():
    """
    Lista todos los usuarios del sistema
    """
    print("\nListando usuarios...")
    
    usuarios = UserProfile.objects.all().order_by('username')
    
    if not usuarios:
        print("  No hay usuarios en el sistema")
        return
    
    print("\n  {:<20} {:<30} {:<20} {:<30}".format("Usuario", "Nombre completo", "Email", "Grupos"))
    print("  " + "-" * 100)
    
    for usuario in usuarios:
        nombre_completo = f"{usuario.first_name} {usuario.last_name}".strip()
        grupos = ", ".join([g.name for g in usuario.groups.all()])
        print("  {:<20} {:<30} {:<20} {:<30}".format(
            usuario.username,
            nombre_completo if nombre_completo else "N/A",
            usuario.email,
            grupos if grupos else "Sin grupos"
        ))

def listar_grupos():
    """
    Lista todos los grupos del sistema y sus permisos
    """
    print("\nListando grupos...")
    
    grupos = Group.objects.all().order_by('name')
    
    if not grupos:
        print("  No hay grupos en el sistema")
        return
    
    for grupo in grupos:
        print(f"\n  Grupo: {grupo.name}")
        print("  " + "-" * 50)
        
        # Contar usuarios en el grupo
        num_usuarios = UserProfile.objects.filter(groups=grupo).count()
        print(f"  Usuarios: {num_usuarios}")
        
        # Listar permisos
        permisos = grupo.permissions.all().order_by('content_type__app_label', 'content_type__model', 'codename')
        if permisos:
            print("  Permisos:")
            for permiso in permisos:
                app_model = f"{permiso.content_type.app_label}.{permiso.content_type.model}"
                print(f"    - {app_model}: {permiso.codename}")
        else:
            print("  Permisos: Sin permisos asignados")

def crear_usuario(username, password, email, nombre, apellido):
    """
    Crea un usuario si no existe
    """
    print(f"\nCreando usuario '{username}'...")
    
    try:
        # Verificar si el usuario ya existe
        if UserProfile.objects.filter(username=username).exists():
            print(f"  El usuario '{username}' ya existe")
            return True
        
        # Crear usuario
        usuario = UserProfile.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=nombre,
            last_name=apellido
        )
        
        print(f"  Usuario '{username}' creado correctamente")
        return True
    except Exception as e:
        print(f"  Error al crear usuario '{username}': {str(e)}")
        return False

def asignar_usuario_a_grupo(username, nombre_grupo):
    """
    Asigna un usuario a un grupo
    """
    print(f"\nAsignando usuario '{username}' al grupo '{nombre_grupo}'...")
    
    try:
        # Obtener usuario
        usuario = UserProfile.objects.get(username=username)
        
        # Obtener grupo
        grupo = Group.objects.get(name=nombre_grupo)
        
        # Asignar grupo al usuario
        usuario.groups.add(grupo)
        
        # Guardar usuario
        usuario.save()
        
        print(f"  Usuario '{username}' asignado correctamente al grupo '{nombre_grupo}'")
        return True
    except UserProfile.DoesNotExist:
        print(f"  Error: El usuario '{username}' no existe")
        return False
    except Group.DoesNotExist:
        print(f"  Error: El grupo '{nombre_grupo}' no existe")
        return False
    except Exception as e:
        print(f"  Error al asignar usuario a grupo: {str(e)}")
        return False

def eliminar_usuario_de_grupo(username, nombre_grupo):
    """
    Elimina un usuario de un grupo
    """
    print(f"\nEliminando usuario '{username}' del grupo '{nombre_grupo}'...")
    
    try:
        # Obtener usuario
        usuario = UserProfile.objects.get(username=username)
        
        # Obtener grupo
        grupo = Group.objects.get(name=nombre_grupo)
        
        # Verificar si el usuario pertenece al grupo
        if grupo not in usuario.groups.all():
            print(f"  El usuario '{username}' no pertenece al grupo '{nombre_grupo}'")
            return False
        
        # Eliminar grupo del usuario
        usuario.groups.remove(grupo)
        
        # Guardar usuario
        usuario.save()
        
        print(f"  Usuario '{username}' eliminado correctamente del grupo '{nombre_grupo}'")
        return True
    except UserProfile.DoesNotExist:
        print(f"  Error: El usuario '{username}' no existe")
        return False
    except Group.DoesNotExist:
        print(f"  Error: El grupo '{nombre_grupo}' no existe")
        return False
    except Exception as e:
        print(f"  Error al eliminar usuario de grupo: {str(e)}")
        return False

def configuracion_inicial():
    """
    Realiza la configuración inicial del sistema:
    - Crea los grupos predefinidos
    - Asigna permisos a los grupos
    - Crea usuarios de ejemplo para cada grupo
    """
    print("=" * 80)
    print("CONFIGURACIÓN INICIAL DE GRUPOS Y PERMISOS")
    print("=" * 80)
    
    # Crear grupos
    crear_grupos()
    
    # Asignar permisos a grupos
    asignar_permisos_a_grupos()
    
    # Crear usuarios de ejemplo para cada grupo
    usuarios_ejemplo = [
        {'username': 'admin', 'password': 'admin123', 'email': 'admin@granjaapp.com', 'nombre': 'Administrador', 'apellido': 'Sistema', 'grupo': 'Administradores'},
        {'username': 'gerente', 'password': 'gerente123', 'email': 'gerente@granjaapp.com', 'nombre': 'Gerente', 'apellido': 'Principal', 'grupo': 'Gerentes'},
        {'username': 'pedro', 'password': 'pedro123', 'email': 'pedro@granjaapp.com', 'nombre': 'Pedro', 'apellido': 'Operario', 'grupo': 'Operarios'},
        {'username': 'maria', 'password': 'maria123', 'email': 'maria@granjaapp.com', 'nombre': 'María', 'apellido': 'Operaria', 'grupo': 'Operarios'},
        {'username': 'veterinario', 'password': 'veterinario123', 'email': 'veterinario@granjaapp.com', 'nombre': 'Carlos', 'apellido': 'Veterinario', 'grupo': 'Veterinarios'},
        {'username': 'vendedor', 'password': 'vendedor123', 'email': 'vendedor@granjaapp.com', 'nombre': 'Ana', 'apellido': 'Vendedora', 'grupo': 'Vendedores'}
    ]
    
    for usuario in usuarios_ejemplo:
        crear_usuario(
            username=usuario['username'],
            password=usuario['password'],
            email=usuario['email'],
            nombre=usuario['nombre'],
            apellido=usuario['apellido']
        )
        asignar_usuario_a_grupo(usuario['username'], usuario['grupo'])
    
    print("\nConfiguración inicial completada")
    print("=" * 80)

def main():
    """
    Función principal
    """
    parser = argparse.ArgumentParser(description='Gestión de grupos y permisos para App_Granja')
    
    # Subparsers para comandos
    subparsers = parser.add_subparsers(dest='comando', help='Comandos disponibles')
    
    # Comando 'inicializar'
    inicializar_parser = subparsers.add_parser('inicializar', help='Realiza la configuración inicial del sistema')
    
    # Comando 'listar-usuarios'
    listar_usuarios_parser = subparsers.add_parser('listar-usuarios', help='Lista todos los usuarios del sistema')
    
    # Comando 'listar-grupos'
    listar_grupos_parser = subparsers.add_parser('listar-grupos', help='Lista todos los grupos del sistema y sus permisos')
    
    # Comando 'crear-usuario'
    crear_usuario_parser = subparsers.add_parser('crear-usuario', help='Crea un nuevo usuario')
    crear_usuario_parser.add_argument('username', help='Nombre de usuario')
    crear_usuario_parser.add_argument('password', help='Contraseña')
    crear_usuario_parser.add_argument('email', help='Correo electrónico')
    crear_usuario_parser.add_argument('nombre', help='Nombre')
    crear_usuario_parser.add_argument('apellido', help='Apellido')
    
    # Comando 'asignar-grupo'
    asignar_grupo_parser = subparsers.add_parser('asignar-grupo', help='Asigna un usuario a un grupo')
    asignar_grupo_parser.add_argument('username', help='Nombre de usuario')
    asignar_grupo_parser.add_argument('grupo', help='Nombre del grupo')
    
    # Comando 'eliminar-grupo'
    eliminar_grupo_parser = subparsers.add_parser('eliminar-grupo', help='Elimina un usuario de un grupo')
    eliminar_grupo_parser.add_argument('username', help='Nombre de usuario')
    eliminar_grupo_parser.add_argument('grupo', help='Nombre del grupo')
    
    # Parsear argumentos
    args = parser.parse_args()
    
    # Ejecutar comando correspondiente
    if args.comando == 'inicializar':
        configuracion_inicial()
    elif args.comando == 'listar-usuarios':
        listar_usuarios()
    elif args.comando == 'listar-grupos':
        listar_grupos()
    elif args.comando == 'crear-usuario':
        crear_usuario(args.username, args.password, args.email, args.nombre, args.apellido)
    elif args.comando == 'asignar-grupo':
        asignar_usuario_a_grupo(args.username, args.grupo)
    elif args.comando == 'eliminar-grupo':
        eliminar_usuario_de_grupo(args.username, args.grupo)
    else:
        # Si no se especifica un comando, mostrar la ayuda
        parser.print_help()

if __name__ == "__main__":
    main()

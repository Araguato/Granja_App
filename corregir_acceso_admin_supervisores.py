"""
Script para corregir el acceso de supervisores al panel de administración de Django.
Este script asegura que los supervisores puedan acceder a las secciones de ventas y mortalidad.
"""
import os
import django
import sys

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'granja.settings')
django.setup()

from django.contrib.auth.models import Group, Permission, ContentType
from django.contrib.auth import get_user_model
from django.db import transaction

User = get_user_model()

def main():
    print("=== CORRECCIÓN DE ACCESO ADMIN PARA SUPERVISORES ===\n")
    
    # Verificar si hay supervisores en el sistema
    supervisores = User.objects.filter(user_type='SUPERVISOR')
    if not supervisores.exists():
        print("⚠️ No se encontraron usuarios con rol de supervisor.")
        return
    
    print(f"Se encontraron {supervisores.count()} supervisores en el sistema.")
    
    try:
        with transaction.atomic():
            # 1. Crear o obtener el grupo de Supervisores
            grupo_supervisores, created = Group.objects.get_or_create(name='Supervisores')
            print(f"✅ Grupo 'Supervisores': {'Creado' if created else 'Ya existía'}")
            
            # 2. Asignar TODOS los permisos necesarios para el admin
            permisos_admin = []
            
            # Permisos para el modelo LogEntry (necesario para acceder al admin)
            try:
                admin_ct = ContentType.objects.get(app_label='admin', model='logentry')
                for codename in ['add_logentry', 'change_logentry', 'delete_logentry', 'view_logentry']:
                    perm, _ = Permission.objects.get_or_create(
                        codename=codename,
                        content_type=admin_ct,
                        defaults={'name': f'Can {codename.split("_")[0]} log entry'}
                    )
                    permisos_admin.append(perm)
                print("✅ Permisos de LogEntry creados/verificados")
            except Exception as e:
                print(f"❌ Error con permisos LogEntry: {e}")
            
            # Permisos para MortalidadDiaria
            try:
                mortalidad_ct = ContentType.objects.get(app_label='produccion', model='mortalidaddiaria')
                for codename in ['add_mortalidaddiaria', 'change_mortalidaddiaria', 'delete_mortalidaddiaria', 'view_mortalidaddiaria']:
                    perm, _ = Permission.objects.get_or_create(
                        codename=codename,
                        content_type=mortalidad_ct,
                        defaults={'name': f'Can {codename.split("_")[0]} Mortalidad Diaria'}
                    )
                    permisos_admin.append(perm)
                print("✅ Permisos de MortalidadDiaria creados/verificados")
            except Exception as e:
                print(f"❌ Error con permisos MortalidadDiaria: {e}")
            
            # Permisos para SeguimientoDiario
            try:
                seguimiento_ct = ContentType.objects.get(app_label='produccion', model='seguimientodiario')
                for codename in ['add_seguimientodiario', 'change_seguimientodiario', 'delete_seguimientodiario', 'view_seguimientodiario']:
                    perm, _ = Permission.objects.get_or_create(
                        codename=codename,
                        content_type=seguimiento_ct,
                        defaults={'name': f'Can {codename.split("_")[0]} Seguimiento Diario'}
                    )
                    permisos_admin.append(perm)
                print("✅ Permisos de SeguimientoDiario creados/verificados")
            except Exception as e:
                print(f"❌ Error con permisos SeguimientoDiario: {e}")
            
            # Permisos para Lote (necesario para relacionar con MortalidadDiaria)
            try:
                lote_ct = ContentType.objects.get(app_label='produccion', model='lote')
                for codename in ['view_lote']:
                    perm, _ = Permission.objects.get_or_create(
                        codename=codename,
                        content_type=lote_ct,
                        defaults={'name': f'Can {codename.split("_")[0]} Lote'}
                    )
                    permisos_admin.append(perm)
                print("✅ Permisos de Lote creados/verificados")
            except Exception as e:
                print(f"❌ Error con permisos Lote: {e}")
            
            # 3. Asignar todos los permisos al grupo
            for permiso in permisos_admin:
                grupo_supervisores.permissions.add(permiso)
            
            print(f"✅ {len(permisos_admin)} permisos asignados al grupo Supervisores")
            
            # 4. Actualizar cada supervisor
            for supervisor in supervisores:
                # Asegurar que tenga is_staff=True
                if not supervisor.is_staff:
                    supervisor.is_staff = True
                    supervisor.save(update_fields=['is_staff'])
                    print(f"✅ Usuario '{supervisor.username}' actualizado a is_staff=True")
                
                # Asegurar que pertenezca al grupo de Supervisores
                if grupo_supervisores not in supervisor.groups.all():
                    supervisor.groups.add(grupo_supervisores)
                    print(f"✅ Usuario '{supervisor.username}' añadido al grupo Supervisores")
                
                # Asignar permisos directamente al usuario (además del grupo)
                for permiso in permisos_admin:
                    supervisor.user_permissions.add(permiso)
                
                print(f"✅ Usuario '{supervisor.username}' actualizado con todos los permisos necesarios")
    
    except Exception as e:
        print(f"❌ Error general: {e}")
    
    print("\n=== PROCESO COMPLETADO ===")
    print("\nPasos a seguir:")
    print("1. Reinicia el servidor Django: python manage.py runserver 0.0.0.0:8000")
    print("2. Pide a los supervisores que cierren sesión y vuelvan a iniciar sesión")
    print("3. Limpia las cookies del navegador")
    print("4. Intenta acceder a: http://127.0.0.1:8000/admin/produccion/mortalidaddiaria/add/")

if __name__ == "__main__":
    main()

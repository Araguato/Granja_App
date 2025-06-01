"""
Script para verificar y corregir los permisos de los supervisores.
Este script asegura que los supervisores tengan todos los permisos necesarios
para acceder a las secciones de ventas y mortalidad en el panel de administración.
"""
import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'granja.settings')
django.setup()

from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth import get_user_model

User = get_user_model()

def main():
    print("Verificando y corrigiendo permisos para supervisores...")
    
    # 1. Asegurarse de que exista el grupo de Supervisores
    grupo_supervisores, created = Group.objects.get_or_create(name='Supervisores')
    if created:
        print("✅ Grupo 'Supervisores' creado")
    else:
        print("✅ Grupo 'Supervisores' ya existe")
    
    # 2. Asignar permisos para MortalidadDiaria
    try:
        content_type = ContentType.objects.get(app_label='produccion', model='mortalidaddiaria')
        permisos_mortalidad = [
            Permission.objects.get_or_create(codename='add_mortalidaddiaria', name='Can add Mortalidad Diaria', content_type=content_type)[0],
            Permission.objects.get_or_create(codename='change_mortalidaddiaria', name='Can change Mortalidad Diaria', content_type=content_type)[0],
            Permission.objects.get_or_create(codename='view_mortalidaddiaria', name='Can view Mortalidad Diaria', content_type=content_type)[0],
            Permission.objects.get_or_create(codename='delete_mortalidaddiaria', name='Can delete Mortalidad Diaria', content_type=content_type)[0],
        ]
        
        for permiso in permisos_mortalidad:
            if permiso not in grupo_supervisores.permissions.all():
                grupo_supervisores.permissions.add(permiso)
                print(f"✅ Permiso '{permiso.codename}' asignado al grupo Supervisores")
            else:
                print(f"✅ Permiso '{permiso.codename}' ya estaba asignado")
    except Exception as e:
        print(f"❌ Error al asignar permisos de MortalidadDiaria: {e}")
    
    # 3. Asignar permisos para acceso al admin
    try:
        admin_content_type = ContentType.objects.get(app_label='admin', model='logentry')
        permiso_admin = Permission.objects.get_or_create(codename='view_logentry', name='Can view log entry', content_type=admin_content_type)[0]
        
        if permiso_admin not in grupo_supervisores.permissions.all():
            grupo_supervisores.permissions.add(permiso_admin)
            print(f"✅ Permiso '{permiso_admin.codename}' asignado al grupo Supervisores")
        else:
            print(f"✅ Permiso '{permiso_admin.codename}' ya estaba asignado")
    except Exception as e:
        print(f"❌ Error al asignar permisos de Admin: {e}")
    
    # 4. Asignar permisos para SeguimientoDiario
    try:
        content_type = ContentType.objects.get(app_label='produccion', model='seguimientodiario')
        permisos_seguimiento = [
            Permission.objects.get_or_create(codename='add_seguimientodiario', name='Can add Seguimiento Diario', content_type=content_type)[0],
            Permission.objects.get_or_create(codename='change_seguimientodiario', name='Can change Seguimiento Diario', content_type=content_type)[0],
            Permission.objects.get_or_create(codename='view_seguimientodiario', name='Can view Seguimiento Diario', content_type=content_type)[0],
        ]
        
        for permiso in permisos_seguimiento:
            if permiso not in grupo_supervisores.permissions.all():
                grupo_supervisores.permissions.add(permiso)
                print(f"✅ Permiso '{permiso.codename}' asignado al grupo Supervisores")
            else:
                print(f"✅ Permiso '{permiso.codename}' ya estaba asignado")
    except Exception as e:
        print(f"❌ Error al asignar permisos de SeguimientoDiario: {e}")
    
    # 5. Asegurarse de que todos los usuarios supervisores tengan is_staff=True
    supervisores = User.objects.filter(user_type='SUPERVISOR')
    for supervisor in supervisores:
        if not supervisor.is_staff:
            supervisor.is_staff = True
            supervisor.save()
            print(f"✅ Usuario '{supervisor.username}' actualizado a is_staff=True")
        else:
            print(f"✅ Usuario '{supervisor.username}' ya tiene is_staff=True")
        
        # Asegurarse de que pertenezca al grupo de Supervisores
        if grupo_supervisores not in supervisor.groups.all():
            supervisor.groups.add(grupo_supervisores)
            print(f"✅ Usuario '{supervisor.username}' añadido al grupo Supervisores")
        else:
            print(f"✅ Usuario '{supervisor.username}' ya pertenece al grupo Supervisores")
    
    print("\nVerificación y corrección de permisos completada.")
    print("\nIMPORTANTE:")
    print("1. Reinicia el servidor Django para que los cambios surtan efecto")
    print("2. Los supervisores deben cerrar sesión y volver a iniciar sesión")
    print("3. Limpia las cookies del navegador para eliminar sesiones antiguas")

if __name__ == "__main__":
    main()

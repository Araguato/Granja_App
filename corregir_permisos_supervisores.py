"""
Script simplificado para corregir los permisos de supervisores.
"""
import os
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'granja.settings')
django.setup()

from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth import get_user_model

User = get_user_model()

# Obtener o crear el grupo de Supervisores
grupo_supervisores, created = Group.objects.get_or_create(name='Supervisores')
print(f"Grupo Supervisores: {'Creado' if created else 'Ya existía'}")

# Asignar permisos para MortalidadDiaria
try:
    content_type = ContentType.objects.get(app_label='produccion', model='mortalidaddiaria')
    
    # Crear o obtener los permisos necesarios
    add_perm, _ = Permission.objects.get_or_create(
        codename='add_mortalidaddiaria',
        defaults={'name': 'Can add Mortalidad Diaria', 'content_type': content_type}
    )
    view_perm, _ = Permission.objects.get_or_create(
        codename='view_mortalidaddiaria',
        defaults={'name': 'Can view Mortalidad Diaria', 'content_type': content_type}
    )
    change_perm, _ = Permission.objects.get_or_create(
        codename='change_mortalidaddiaria',
        defaults={'name': 'Can change Mortalidad Diaria', 'content_type': content_type}
    )
    
    # Asignar permisos al grupo
    grupo_supervisores.permissions.add(add_perm, view_perm, change_perm)
    print("Permisos de MortalidadDiaria asignados correctamente")
except Exception as e:
    print(f"Error al asignar permisos de MortalidadDiaria: {e}")

# Asignar permiso para acceso al admin
try:
    admin_content_type = ContentType.objects.get(app_label='admin', model='logentry')
    admin_perm, _ = Permission.objects.get_or_create(
        codename='view_logentry',
        defaults={'name': 'Can view log entry', 'content_type': admin_content_type}
    )
    grupo_supervisores.permissions.add(admin_perm)
    print("Permiso de acceso al admin asignado correctamente")
except Exception as e:
    print(f"Error al asignar permiso de admin: {e}")

# Actualizar todos los usuarios supervisores
supervisores = User.objects.filter(user_type='SUPERVISOR')
for supervisor in supervisores:
    supervisor.is_staff = True
    supervisor.groups.add(grupo_supervisores)
    supervisor.save()
    print(f"Usuario {supervisor.username} actualizado correctamente")

print("\nProceso completado. Por favor reinicia el servidor Django y pide a los supervisores que cierren sesión y vuelvan a iniciar sesión.")

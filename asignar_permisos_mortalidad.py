"""
Script para asignar permisos específicos para MortalidadDiaria a los supervisores.
"""
import os
import django

# Configurar el entorno de Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'granja.settings')
django.setup()

from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from avicola.models import UserProfile

def asignar_permisos_mortalidad():
    """
    Asigna permisos específicos para MortalidadDiaria a los supervisores.
    """
    print("Asignando permisos para MortalidadDiaria a los supervisores...")
    
    try:
        # Obtener el grupo de Supervisores
        grupo_supervisores, created = Group.objects.get_or_create(name='Supervisores')
        if created:
            print("Se ha creado el grupo 'Supervisores'.")
        else:
            print("Se ha encontrado el grupo 'Supervisores'.")
        
        # Obtener el ContentType para MortalidadDiaria
        try:
            content_type = ContentType.objects.get(app_label='produccion', model='mortalidaddiaria')
            print(f"Se ha encontrado el ContentType para 'produccion.mortalidaddiaria'.")
        except ContentType.DoesNotExist:
            print(f"Error: No se encontró el ContentType para 'produccion.mortalidaddiaria'.")
            return
        
        # Tipos de permisos que queremos asignar
        tipos_permisos = ['view', 'add', 'change', 'delete']
        
        # Obtener y asignar los permisos
        permisos_asignados = 0
        for tipo in tipos_permisos:
            codename = f"{tipo}_mortalidaddiaria"
            try:
                permiso = Permission.objects.get(content_type=content_type, codename=codename)
                if permiso not in grupo_supervisores.permissions.all():
                    grupo_supervisores.permissions.add(permiso)
                    permisos_asignados += 1
                    print(f"Asignado permiso: {codename}")
                else:
                    print(f"El permiso {codename} ya estaba asignado.")
            except Permission.DoesNotExist:
                print(f"Error: No se encontró el permiso {codename}.")
        
        # Asegurarse de que todos los supervisores tengan is_staff=True
        supervisores = UserProfile.objects.filter(groups=grupo_supervisores)
        supervisores_actualizados = 0
        
        for supervisor in supervisores:
            if not supervisor.is_staff:
                supervisor.is_staff = True
                supervisor.save()
                supervisores_actualizados += 1
                print(f"Usuario {supervisor.username} ahora tiene acceso al panel de administración.")
        
        # Resumen
        print("\nResumen:")
        print(f"- Permisos asignados para MortalidadDiaria: {permisos_asignados}")
        print(f"- Supervisores actualizados para acceso al admin: {supervisores_actualizados}")
        print(f"- Total de supervisores en el sistema: {supervisores.count()}")
        
        if permisos_asignados == 0 and supervisores_actualizados == 0:
            print("\nNo fue necesario realizar cambios. Los supervisores ya tienen todos los permisos necesarios.")
        else:
            print("\nActualización completada con éxito.")
        
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    asignar_permisos_mortalidad()

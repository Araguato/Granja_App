"""
Script para actualizar los permisos de los supervisores y garantizar que tengan acceso
a las secciones de Ventas y Mortalidad en el panel de administración.
"""
import os
import django

# Configurar el entorno de Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'granja.settings')
django.setup()

from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from avicola.models import UserProfile

def actualizar_permisos_supervisores():
    """
    Actualiza los permisos de los supervisores para garantizar que tengan acceso
    a las secciones de Ventas y Mortalidad en el panel de administración.
    """
    print("Actualizando permisos de supervisores...")
    
    # Obtener el grupo de Supervisores
    try:
        grupo_supervisores, created = Group.objects.get_or_create(name='Supervisores')
        if created:
            print("Se ha creado el grupo 'Supervisores'.")
        else:
            print("Se ha encontrado el grupo 'Supervisores'.")
    except Exception as e:
        print(f"Error al obtener el grupo 'Supervisores': {str(e)}")
        return
    
    # Modelos a los que queremos dar acceso en el admin
    modelos_admin = [
        # Ventas
        {'app': 'ventas', 'modelo': 'venta'},
        {'app': 'ventas', 'modelo': 'cliente'},
        {'app': 'ventas', 'modelo': 'tipohuevo'},
        {'app': 'ventas', 'modelo': 'inventariohuevos'},
        {'app': 'ventas', 'modelo': 'detalleventa'},
        # Producción (para mortalidad)
        {'app': 'produccion', 'modelo': 'seguimientodiario'},
        {'app': 'produccion', 'modelo': 'lote'},
        {'app': 'produccion', 'modelo': 'galpon'},
    ]
    
    # Permisos que queremos asignar para cada modelo
    tipos_permisos = ['view', 'add', 'change', 'delete']
    
    # Obtener y asignar todos los permisos necesarios
    permisos_asignados = 0
    for modelo_info in modelos_admin:
        app = modelo_info['app']
        modelo = modelo_info['modelo']
        
        try:
            content_type = ContentType.objects.get(app_label=app, model=modelo)
            print(f"Procesando permisos para {app}.{modelo}...")
            
            for tipo in tipos_permisos:
                codename = f"{tipo}_{modelo}"
                try:
                    permiso = Permission.objects.get(content_type=content_type, codename=codename)
                    if permiso not in grupo_supervisores.permissions.all():
                        grupo_supervisores.permissions.add(permiso)
                        permisos_asignados += 1
                        print(f"  - Asignado permiso: {codename}")
                except Permission.DoesNotExist:
                    print(f"  - Permiso no encontrado: {codename}")
        
        except ContentType.DoesNotExist:
            print(f"Modelo no encontrado: {app}.{modelo}")
    
    # Asegurarse de que todos los supervisores tengan is_staff=True
    supervisores = UserProfile.objects.filter(groups=grupo_supervisores)
    supervisores_actualizados = 0
    
    for supervisor in supervisores:
        if not supervisor.is_staff:
            supervisor.is_staff = True
            supervisor.save()
            supervisores_actualizados += 1
            print(f"Usuario {supervisor.username} ahora tiene acceso al panel de administración")
    
    # Resumen
    print("\nResumen de la actualización:")
    print(f"- Permisos asignados: {permisos_asignados}")
    print(f"- Supervisores actualizados para acceso al admin: {supervisores_actualizados}")
    print(f"- Total de supervisores en el sistema: {supervisores.count()}")
    
    if permisos_asignados == 0 and supervisores_actualizados == 0:
        print("\nNo fue necesario realizar cambios. Los supervisores ya tienen todos los permisos necesarios.")
    else:
        print("\nActualización completada con éxito.")

if __name__ == "__main__":
    actualizar_permisos_supervisores()

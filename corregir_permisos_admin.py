"""
Script para corregir todos los permisos necesarios para que los supervisores
puedan acceder a todas las secciones del panel de administración, incluyendo
MortalidadDiaria.
"""
import os
import django

# Configurar el entorno de Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'granja.settings')
django.setup()

from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from avicola.models import UserProfile
from django.contrib.admin.models import LogEntry

def corregir_permisos_admin():
    """
    Corrige todos los permisos necesarios para que los supervisores puedan
    acceder a todas las secciones del panel de administración.
    """
    print("Corrigiendo permisos para acceso al panel de administración...")
    
    try:
        # Obtener el grupo de Supervisores
        grupo_supervisores, created = Group.objects.get_or_create(name='Supervisores')
        if created:
            print("Se ha creado el grupo 'Supervisores'.")
        else:
            print("Se ha encontrado el grupo 'Supervisores'.")
        
        # Modelos a los que queremos dar acceso en el admin
        modelos_admin = [
            # Producción
            {'app': 'produccion', 'modelo': 'mortalidaddiaria'},
            {'app': 'produccion', 'modelo': 'seguimientodiario'},
            {'app': 'produccion', 'modelo': 'lote'},
            {'app': 'produccion', 'modelo': 'galpon'},
            {'app': 'produccion', 'modelo': 'granja'},
            {'app': 'produccion', 'modelo': 'mortalidadsemanal'},
            {'app': 'produccion', 'modelo': 'seguimientoengorde'},
            # Ventas
            {'app': 'ventas', 'modelo': 'venta'},
            {'app': 'ventas', 'modelo': 'cliente'},
            {'app': 'ventas', 'modelo': 'tipohuevo'},
            {'app': 'ventas', 'modelo': 'inventariohuevos'},
            {'app': 'ventas', 'modelo': 'detalleventa'},
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
                        else:
                            print(f"  - El permiso {codename} ya estaba asignado.")
                    except Permission.DoesNotExist:
                        print(f"  - Permiso no encontrado: {codename}")
            
            except ContentType.DoesNotExist:
                print(f"Modelo no encontrado: {app}.{modelo}")
        
        # Asignar permisos para ver el admin
        try:
            admin_content_type = ContentType.objects.get(app_label='admin', model='logentry')
            for tipo in ['view', 'add', 'change', 'delete']:
                try:
                    codename = f"{tipo}_logentry"
                    permiso = Permission.objects.get(content_type=admin_content_type, codename=codename)
                    if permiso not in grupo_supervisores.permissions.all():
                        grupo_supervisores.permissions.add(permiso)
                        permisos_asignados += 1
                        print(f"Asignado permiso de admin: {codename}")
                except Permission.DoesNotExist:
                    print(f"Permiso de admin no encontrado: {codename}")
        except ContentType.DoesNotExist:
            print("ContentType para admin.logentry no encontrado")
        
        # Asegurarse de que todos los supervisores tengan is_staff=True
        supervisores = UserProfile.objects.filter(groups=grupo_supervisores)
        supervisores_actualizados = 0
        
        for supervisor in supervisores:
            if not supervisor.is_staff:
                supervisor.is_staff = True
                supervisor.save()
                supervisores_actualizados += 1
                print(f"Usuario {supervisor.username} ahora tiene acceso al panel de administración.")
            else:
                print(f"Usuario {supervisor.username} ya tenía acceso al panel de administración.")
        
        # Resumen
        print("\nResumen:")
        print(f"- Permisos asignados: {permisos_asignados}")
        print(f"- Supervisores actualizados para acceso al admin: {supervisores_actualizados}")
        print(f"- Total de supervisores en el sistema: {supervisores.count()}")
        
        if permisos_asignados == 0 and supervisores_actualizados == 0:
            print("\nNo fue necesario realizar cambios. Los supervisores ya tienen todos los permisos necesarios.")
        else:
            print("\nActualización completada con éxito.")
        
        # Imprimir información de los supervisores
        print("\nInformación de los supervisores:")
        for supervisor in supervisores:
            print(f"- Usuario: {supervisor.username}")
            print(f"  - Nombre completo: {supervisor.get_full_name()}")
            print(f"  - is_staff: {supervisor.is_staff}")
            print(f"  - is_superuser: {supervisor.is_superuser}")
            print(f"  - user_type: {supervisor.user_type}")
            print(f"  - Grupos: {', '.join([g.name for g in supervisor.groups.all()])}")
        
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    corregir_permisos_admin()

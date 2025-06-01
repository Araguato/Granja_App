from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.db.models import Q
from avicola.models import UserProfile

def is_admin(user):
    """Verificar si el usuario es administrador"""
    return user.is_superuser or user.user_type == 'ADMIN'

@login_required
@user_passes_test(is_admin)
def configurar_acceso_admin(request):
    """
    Vista para configurar los permisos de acceso al panel de administración
    para los supervisores. Esto garantiza que puedan acceder a las secciones
    de Ventas y Mortalidad en el admin.
    """
    if request.method == 'POST':
        try:
            # Obtener el grupo de Supervisores
            grupo_supervisores, created = Group.objects.get_or_create(name='Supervisores')
            
            # Modelos a los que queremos dar acceso en el admin
            modelos_admin = [
                # Ventas
                {'app': 'ventas', 'modelo': 'venta'},
                {'app': 'ventas', 'modelo': 'cliente'},
                {'app': 'ventas', 'modelo': 'tipohuevo'},
                {'app': 'ventas', 'modelo': 'inventariohuevos'},
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
                    
                    for tipo in tipos_permisos:
                        codename = f"{tipo}_{modelo}"
                        try:
                            permiso = Permission.objects.get(content_type=content_type, codename=codename)
                            if permiso not in grupo_supervisores.permissions.all():
                                grupo_supervisores.permissions.add(permiso)
                                permisos_asignados += 1
                        except Permission.DoesNotExist:
                            messages.warning(request, f"Permiso {codename} no encontrado para {app}.{modelo}")
                
                except ContentType.DoesNotExist:
                    messages.warning(request, f"Modelo {app}.{modelo} no encontrado")
            
            # Asignar permisos de acceso al admin
            try:
                # Permiso para acceder al admin
                admin_content_type = ContentType.objects.get(app_label='admin', model='logentry')
                admin_permission = Permission.objects.get(content_type=admin_content_type, codename='view_logentry')
                if admin_permission not in grupo_supervisores.permissions.all():
                    grupo_supervisores.permissions.add(admin_permission)
                    permisos_asignados += 1
            except (ContentType.DoesNotExist, Permission.DoesNotExist):
                # Si no existe el permiso específico, intentamos con un enfoque alternativo
                # Asegurar que todos los supervisores tengan is_staff=True
                supervisores = UserProfile.objects.filter(groups=grupo_supervisores)
                for supervisor in supervisores:
                    if not supervisor.is_staff:
                        supervisor.is_staff = True
                        supervisor.save()
                        messages.info(request, f"Usuario {supervisor.username} ahora tiene acceso al panel de administración")
            
            # Mensaje de éxito
            if permisos_asignados > 0:
                messages.success(request, f"Se han asignado {permisos_asignados} permisos de administración al grupo de Supervisores")
            else:
                messages.info(request, "No fue necesario asignar nuevos permisos de administración")
                
            # Verificar que todos los supervisores tengan is_staff=True
            supervisores = UserProfile.objects.filter(groups=grupo_supervisores)
            for supervisor in supervisores:
                if not supervisor.is_staff:
                    supervisor.is_staff = True
                    supervisor.save()
            
            return redirect('admin:index')
            
        except Exception as e:
            messages.error(request, f"Error al configurar los permisos de administración: {str(e)}")
    
    # Si es GET o hubo un error, mostrar la página de confirmación
    return render(request, 'avicola/configurar_acceso_admin.html')

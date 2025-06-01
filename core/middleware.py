"""
Middleware personalizado para la aplicación App_Granja.
"""
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.urls import resolve

class SupervisorPermissionsMiddleware:
    """
    Middleware que asegura que los supervisores tengan los permisos necesarios
    para acceder a las secciones de Ventas y Mortalidad.
    """
    def __init__(self, get_response):
        self.get_response = get_response
        # Inicializar el middleware una sola vez al inicio
        self._setup_complete = False

    def __call__(self, request):
        try:
            # Procesar la solicitud antes de la vista
            if request.user.is_authenticated and hasattr(request.user, 'user_type') and request.user.user_type == 'SUPERVISOR':
                # Asegurarse de que el usuario tenga is_staff=True siempre
                if not request.user.is_staff:
                    request.user.is_staff = True
                    request.user.save()
                
                # Verificar si el usuario pertenece al grupo de Supervisores
                try:
                    grupo_supervisores, created = Group.objects.get_or_create(name='Supervisores')
                    if grupo_supervisores not in request.user.groups.all():
                        request.user.groups.add(grupo_supervisores)
                        request.user.save()
                    
                    # Asignar permisos específicos para MortalidadDiaria
                    self._ensure_supervisor_permissions(grupo_supervisores)
                except Exception as e:
                    # Registrar el error pero no interrumpir la solicitud
                    print(f"Error al configurar permisos de supervisor: {e}")
            
            # Continuar con el procesamiento normal
            response = self.get_response(request)
            return response
        except Exception as e:
            # Capturar cualquier excepción para evitar que el middleware falle
            print(f"Error en SupervisorPermissionsMiddleware: {e}")
            # Asegurarse de que la solicitud continúe incluso si hay un error
            return self.get_response(request)
    
    def _ensure_supervisor_permissions(self, grupo):
        """Asegura que el grupo de supervisores tenga todos los permisos necesarios."""
        if self._setup_complete:
            return
        
        try:
            # Permisos para MortalidadDiaria
            content_type = ContentType.objects.get(app_label='produccion', model='mortalidaddiaria')
            permisos = [
                Permission.objects.get_or_create(codename='add_mortalidaddiaria', name='Can add Mortalidad Diaria', content_type=content_type)[0],
                Permission.objects.get_or_create(codename='change_mortalidaddiaria', name='Can change Mortalidad Diaria', content_type=content_type)[0],
                Permission.objects.get_or_create(codename='view_mortalidaddiaria', name='Can view Mortalidad Diaria', content_type=content_type)[0],
            ]
            
            # Permisos para acceso al admin
            admin_content_type = ContentType.objects.get(app_label='admin', model='logentry')
            permisos.append(Permission.objects.get_or_create(codename='view_logentry', name='Can view log entry', content_type=admin_content_type)[0])
            
            # Asignar todos los permisos al grupo
            for permiso in permisos:
                if permiso not in grupo.permissions.all():
                    grupo.permissions.add(permiso)
            
            self._setup_complete = True
        except Exception as e:
            print(f"Error al asignar permisos: {e}")
            # No marcar como completo si hay un error, para intentarlo de nuevo en la próxima solicitud

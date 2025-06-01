from django.contrib.auth.models import Permission
from django.utils.deprecation import MiddlewareMixin

class SupervisorPermissionsMiddleware(MiddlewareMixin):
    """
    Middleware que otorga permisos adicionales a los usuarios con tipo SUPERVISOR.
    Esto permite que los supervisores puedan realizar todas las acciones necesarias
    sin tener que asignar explícitamente todos los permisos a través del admin.
    """
    
    def process_request(self, request):
        # Solo procesar si el usuario está autenticado
        if not request.user.is_authenticated:
            return None
            
        # Verificar si el usuario es un supervisor
        if hasattr(request.user, 'user_type') and request.user.user_type == 'SUPERVISOR':
            # Otorgar permisos temporales durante esta solicitud
            # Estos permisos no se guardan en la base de datos
            
            # Lista de permisos que queremos otorgar a los supervisores
            supervisor_permissions = [
                # Permisos para Lotes
                'add_lote', 'change_lote', 'view_lote', 'delete_lote',
                # Permisos para Galpones
                'add_galpon', 'change_galpon', 'view_galpon', 'delete_galpon',
                # Permisos para Seguimientos
                'add_seguimientodiario', 'change_seguimientodiario', 'view_seguimientodiario', 'delete_seguimientodiario',
                # Permisos para Vacunas
                'add_vacuna', 'change_vacuna', 'view_vacuna', 'delete_vacuna',
                # Permisos para Alimentos
                'add_alimento', 'change_alimento', 'view_alimento', 'delete_alimento',
                # Permisos para Razas
                'add_raza', 'change_raza', 'view_raza', 'delete_raza',
            ]
            
            # Para cada permiso en la lista, verificar si el usuario ya lo tiene
            # Si no lo tiene, otorgárselo temporalmente
            for perm_codename in supervisor_permissions:
                # Determinar la app_label basada en el permiso
                if perm_codename.endswith(('_lote', '_galpon', '_seguimientodiario')):
                    app_label = 'produccion'
                elif perm_codename.endswith(('_vacuna', '_alimento', '_raza')):
                    app_label = 'inventario'
                else:
                    app_label = 'avicola'
                
                # Crear el nombre completo del permiso
                perm_name = f"{app_label}.{perm_codename}"
                
                # Verificar si el usuario ya tiene este permiso
                if not request.user.has_perm(perm_name):
                    # Si no lo tiene, agregarlo a la lista de permisos del usuario
                    # Esto no modifica la base de datos, solo afecta a esta solicitud
                    if not hasattr(request.user, '_supervisor_perms'):
                        request.user._supervisor_perms = set()
                    request.user._supervisor_perms.add(perm_name)
            
            # Sobreescribir el método has_perm para incluir los permisos temporales
            original_has_perm = request.user.has_perm
            
            def enhanced_has_perm(perm, obj=None):
                # Verificar primero si el permiso está en nuestra lista temporal
                if hasattr(request.user, '_supervisor_perms') and perm in request.user._supervisor_perms:
                    return True
                # Si no, usar el método original
                return original_has_perm(perm, obj)
            
            # Reemplazar el método has_perm con nuestra versión mejorada
            request.user.has_perm = enhanced_has_perm
            
        return None

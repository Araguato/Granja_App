from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from .models import UserProfile
from produccion.models import Lote, Galpon, SeguimientoDiario
from inventario.models import Vacuna, Alimento, Raza

def is_admin(user):
    """Verificar si el usuario es administrador"""
    return user.is_superuser or user.user_type == 'ADMIN'

@login_required
@user_passes_test(is_admin)
def actualizar_permisos_supervisores(request):
    """
    Vista para actualizar los permisos de todos los supervisores existentes.
    Solo accesible para administradores.
    """
    if request.method == 'POST':
        # Obtener todos los usuarios con tipo SUPERVISOR
        supervisores = UserProfile.objects.filter(user_type='SUPERVISOR')
        contador = 0
        
        # Lista de modelos a los que queremos dar permisos
        models_to_grant = [
            Lote, Galpon, SeguimientoDiario,  # Modelos de producción
            Vacuna, Alimento, Raza,          # Modelos de inventario
        ]
        
        # Para cada supervisor
        for supervisor in supervisores:
            # Para cada modelo, otorgamos todos los permisos
            for model in models_to_grant:
                content_type = ContentType.objects.get_for_model(model)
                permissions = Permission.objects.filter(content_type=content_type)
                
                for permission in permissions:
                    supervisor.user_permissions.add(permission)
            
            # También asignamos permisos para ver el dashboard y otras funcionalidades básicas
            basic_permissions = [
                'view_dashboard',  # Permiso personalizado definido en Empresa
            ]
            
            for perm_codename in basic_permissions:
                try:
                    perm = Permission.objects.get(codename=perm_codename)
                    supervisor.user_permissions.add(perm)
                except Permission.DoesNotExist:
                    # Si el permiso no existe, lo ignoramos
                    pass
            
            contador += 1
        
        messages.success(request, f"Se han actualizado los permisos de {contador} supervisores.")
        return redirect('admin:index')
    
    # Si es una solicitud GET, mostrar la página de confirmación
    supervisores = UserProfile.objects.filter(user_type='SUPERVISOR')
    return render(request, 'avicola/actualizar_permisos.html', {
        'supervisores': supervisores,
        'title': 'Actualizar Permisos de Supervisores'
    })

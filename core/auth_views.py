from django.contrib.auth import logout
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache


@never_cache
@login_required
def logout_view(request):
    """
    Vista personalizada para el cierre de sesión que asegura que la sesión
    se cierre correctamente y evita problemas de caché.
    """
    # Cerrar la sesión del usuario
    logout(request)
    
    # Renderizar la plantilla de logout
    response = render(request, 'core/logout.html')
    
    # Añadir encabezados para evitar caché
    response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response['Pragma'] = 'no-cache'
    response['Expires'] = '0'
    
    return response

from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseServerError, HttpResponseNotFound, HttpResponseForbidden, HttpResponseBadRequest
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_protect

def handler400(request, exception=None):
    return render(request, '400.html', status=400)

def handler403(request, exception=None):
    return render(request, '403.html', status=403)

def handler404(request, exception=None):
    return render(request, '404.html', status=404)

def handler500(request):
    return render(request, '500.html', status=500)

def home(request):
    """
    Home page view. Redirects to dashboard if user is authenticated,
    otherwise shows the login page.
    """
    if request.user.is_authenticated:
        return redirect('core:dashboard')
    return render(request, 'core/home.html')

@login_required
def dashboard(request):
    return render(request, 'core/dashboard.html', {
        'title': 'Panel de Control',
    })

@login_required
def perfil_usuario(request):
    """
    Vista para mostrar el perfil del usuario según su rol
    """
    user = request.user
    
    # Determinar la plantilla según el tipo de usuario
    if not hasattr(user, 'userprofile'):
        # Si por alguna razón no tiene perfil, redirigir a la página de error
        return render(request, '403.html', status=403)
    
    user_type = user.userprofile.user_type
    
    # Si es una solicitud POST, redirigir al formulario de edición apropiado
    if request.method == 'POST':
        if user_type == 'ADMIN' or user_type == 'SUPERVISOR':
            return redirect(f'/admin/avicola/userprofile/{user.userprofile.id}/change/')
        else:
            # Para otros roles, podrías redirigir a un formulario personalizado
            return redirect('core:editar_perfil')
    
    # Renderizar la plantilla correspondiente al rol
    template_name = f'core/perfiles/perfil_{user_type.lower()}.html'
    
    # Contexto común para todas las plantillas
    context = {
        'title': 'Mi Perfil',
        'user': user,
        'user_type': user_type,
        'user_type_display': user.get_user_type_display(),
    }
    
    # Agregar datos específicos según el rol
    if user_type in ['ADMIN', 'SUPERVISOR']:
        context['puede_editar'] = True
    else:
        context['puede_editar'] = False
    
    return render(request, template_name, context)

@login_required
@csrf_protect
@require_http_methods(["GET", "POST"])
def editar_perfil(request):
    """
    Vista para editar el perfil del usuario (para operarios y veterinarios)
    """
    user = request.user
    
    # Verificar si el usuario tiene permiso para editar su perfil
    if not hasattr(user, 'userprofile') or user.userprofile.user_type in ['ADMIN', 'SUPERVISOR']:
        return redirect('core:perfil_usuario')
    
    # Inicializar el formulario de cambio de contraseña
    password_form = PasswordChangeForm(user=user)
    
    if request.method == 'POST':
        # Manejar el cambio de contraseña
        if 'cambiar_password' in request.POST:
            password_form = PasswordChangeForm(user=user, data=request.POST)
            if password_form.is_valid():
                user = password_form.save()
                update_session_auth_hash(request, user)  # Mantener la sesión activa
                messages.success(request, 'Tu contraseña ha sido actualizada correctamente.')
                return redirect('core:editar_perfil')
        else:
            # Actualizar información básica del usuario
            user.first_name = request.POST.get('first_name', user.first_name)
            user.last_name = request.POST.get('last_name', user.last_name)
            user.email = request.POST.get('email', user.email)
            
            # Actualizar campos adicionales del perfil
            if hasattr(user, 'userprofile'):
                user.userprofile.telefono = request.POST.get('telefono', user.userprofile.telefono)
                user.userprofile.direccion = request.POST.get('direccion', user.userprofile.direccion)
                user.userprofile.save()
            
            user.save()
            messages.success(request, 'Tu perfil ha sido actualizado correctamente.')
            return redirect('core:perfil_usuario')
    
    return render(request, 'core/editar_perfil.html', {
        'title': 'Editar Perfil',
        'user': user,
        'password_form': password_form,
    })

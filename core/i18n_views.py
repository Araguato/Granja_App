from django.http import JsonResponse
from django.shortcuts import redirect
from django.utils import translation
from django.conf import settings
from django.views.decorators.http import require_POST

# Definir la clave de sesión para el idioma (ya no disponible directamente en Django 5.0+)
LANGUAGE_SESSION_KEY = 'django_language'

def set_language(request, language_code):
    """
    Vista para cambiar el idioma de la aplicación mediante una redirección.
    """
    if language_code in [lang_code for lang_code, lang_name in settings.LANGUAGES]:
        translation.activate(language_code)
        request.session[LANGUAGE_SESSION_KEY] = language_code
    
    next_url = request.GET.get('next', '/')
    return redirect(next_url)

@require_POST
def set_language_ajax(request):
    """
    Vista para cambiar el idioma de la aplicación mediante AJAX.
    """
    language_code = request.POST.get('language', '')
    
    if language_code in [lang_code for lang_code, lang_name in settings.LANGUAGES]:
        translation.activate(language_code)
        request.session[LANGUAGE_SESSION_KEY] = language_code
        return JsonResponse({'status': 'success'})
    
    return JsonResponse({'status': 'error', 'message': 'Código de idioma no válido'})

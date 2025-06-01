from django.http import HttpResponseRedirect
from django.utils import translation
from django.conf import settings
import logging

# Configurar logging
logger = logging.getLogger(__name__)

def set_language_simple(request, language_code):
    """
    Vista simplificada para cambiar el idioma de la aplicación.
    """
    logger.info(f"Cambiando idioma a: {language_code}")
    
    try:
        # Verificar que el idioma solicitado esté disponible
        if language_code in [lang_code for lang_code, lang_name in settings.LANGUAGES]:
            # Activar el idioma
            translation.activate(language_code)
            logger.info(f"Idioma activado: {language_code}")
            
            # Guardar el idioma en la sesión
            request.session['django_language'] = language_code
            
            # Obtener la URL de referencia o usar la raíz como fallback
            referer = request.META.get('HTTP_REFERER')
            redirect_url = referer if referer else '/'
            logger.info(f"Redirigiendo a: {redirect_url}")
            
            # Establecer la cookie de idioma
            response = HttpResponseRedirect(redirect_url)
            response.set_cookie(settings.LANGUAGE_COOKIE_NAME, language_code)
            
            return response
        else:
            logger.warning(f"Idioma no disponible: {language_code}")
    except Exception as e:
        logger.error(f"Error al cambiar idioma: {str(e)}")
    
    # Si hay algún error o el idioma no está disponible, redirigir a la página anterior
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

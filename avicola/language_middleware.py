#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Middleware para manejar la selección de idioma en la aplicación web
"""

from django.utils import translation
from django.utils.deprecation import MiddlewareMixin
from django.conf import settings

class LanguageMiddleware(MiddlewareMixin):
    """
    Middleware para manejar la selección de idioma
    """
    def process_request(self, request):
        """
        Procesa la solicitud y establece el idioma
        """
        # Obtener idioma de la sesión
        language = request.session.get('language', None)
        
        # Si no hay idioma en la sesión, intentar obtenerlo de la cookie
        if not language:
            language = request.COOKIES.get('language', settings.LANGUAGE_CODE)
            
        # Establecer idioma
        translation.activate(language)
        request.LANGUAGE_CODE = translation.get_language()
        
        return None
    
    def process_response(self, request, response):
        """
        Procesa la respuesta y establece la cookie de idioma
        """
        # Obtener idioma actual
        language = translation.get_language()
        
        # Establecer cookie de idioma
        response.set_cookie('language', language)
        
        return response

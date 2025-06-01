"""
Script para ajustar los colores del tema de administración de Django Admin Interface.
"""

import os
import django

# Configurar el entorno de Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'granja.settings')
django.setup()

# Importar el modelo Theme
from admin_interface.models import Theme

def fix_admin_colors():
    """
    Ajusta los colores del tema de administración para mejorar el contraste.
    """
    # Obtener el tema actual (o crear uno si no existe)
    try:
        theme = Theme.objects.first()
        if not theme:
            theme = Theme.objects.create(name='Default')
        
        print("Configuración actual del tema:")
        print(f"- Color del texto del módulo: {theme.css_module_text_color}")
        print(f"- Color del enlace del módulo: {theme.css_module_link_color}")
        
        # Modificar los colores para mejorar el contraste
        # Cambiar el color del texto del módulo a blanco para mejor contraste
        theme.css_module_text_color = '#FFFFFF'
        
        # Cambiar el color de los enlaces del módulo
        theme.css_module_link_color = '#FFFFFF'
        
        # Cambiar el color de los enlaces al pasar el ratón por encima
        theme.css_module_link_hover_color = '#FFFFFF'
        
        # Cambiar el color de los enlaces seleccionados
        theme.css_module_link_selected_color = '#FFFFFF'
        
        # Guardar los cambios
        theme.save()
        
        print("\nColores del tema actualizados:")
        print(f"- Color del texto del módulo: {theme.css_module_text_color}")
        print(f"- Color del enlace del módulo: {theme.css_module_link_color}")
        print(f"- Color del enlace hover: {theme.css_module_link_hover_color}")
        print(f"- Color del enlace seleccionado: {theme.css_module_link_selected_color}")
        
        print("\nLos cambios se han aplicado correctamente. Por favor, recarga la página de administración para ver los cambios.")
    
    except Exception as e:
        print(f"Error al actualizar los colores del tema: {str(e)}")

if __name__ == "__main__":
    fix_admin_colors()

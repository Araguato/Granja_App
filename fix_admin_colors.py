"""
Script para ajustar los colores del tema de administración de Django.
Este script modifica el tema actual para mejorar el contraste entre
el texto y el fondo en el menú de navegación.
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
        
        # Guardar el estado actual para informar de los cambios
        old_menu_text_color = theme.menu_text_color
        
        # Modificar los colores para mejorar el contraste
        # Cambiar el color del texto del menú a blanco para mejor contraste
        theme.menu_text_color = '#FFFFFF'
        
        # Cambiar el color del texto activo del menú
        theme.menu_item_active_text_color = '#FFFFFF'
        
        # Cambiar el color del texto al pasar el ratón por encima
        theme.menu_item_hover_text_color = '#FFFFFF'
        
        # Guardar los cambios
        theme.save()
        
        print(f"Colores del tema actualizados:")
        print(f"- Color del texto del menú: {old_menu_text_color} -> {theme.menu_text_color}")
        print(f"- Color del texto activo: {theme.menu_item_active_text_color}")
        print(f"- Color del texto hover: {theme.menu_item_hover_text_color}")
        
        print("\nLos cambios se han aplicado correctamente. Por favor, recarga la página de administración para ver los cambios.")
    
    except Exception as e:
        print(f"Error al actualizar los colores del tema: {str(e)}")

if __name__ == "__main__":
    fix_admin_colors()

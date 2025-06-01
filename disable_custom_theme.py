"""
Script para desactivar temporalmente los temas personalizados de django-admin-interface.
"""

import os
import django

# Configurar el entorno de Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'granja.settings')
django.setup()

# Importar el modelo Theme
from admin_interface.models import Theme

def disable_custom_themes():
    """
    Desactiva todos los temas personalizados para volver al tema predeterminado de Django.
    """
    try:
        # Desactivar todos los temas
        themes = Theme.objects.all()
        for theme in themes:
            theme.active = False
            theme.save()
        
        print(f"Se han desactivado {themes.count()} temas personalizados.")
        print("El panel de administración ahora utilizará el tema predeterminado de Django.")
        print("Por favor, reinicia el servidor y recarga la página de administración para ver los cambios.")
    
    except Exception as e:
        print(f"Error al desactivar los temas personalizados: {str(e)}")

if __name__ == "__main__":
    disable_custom_themes()

import os
import django

# Configurar el entorno de Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'granja.settings')
django.setup()

# Importar el modelo Theme
from admin_interface.models import Theme

# Actualizar o crear el tema
def update_admin_theme():
    # Intentar obtener el tema activo
    try:
        theme = Theme.objects.get(active=True)
        print(f"Tema encontrado: {theme.name}")
    except Theme.DoesNotExist:
        # Si no existe un tema activo, crear uno nuevo
        theme = Theme.objects.create(
            name="App Granja Theme",
            active=True
        )
        print(f"Nuevo tema creado: {theme.name}")
    
    # Actualizar el tema para eliminar "Django" del título
    theme.title = "App Granja - Administración"
    theme.css_header_text_color = "#FFFFFF"
    theme.css_header_background_color = "#4caf50"
    theme.css_header_link_color = "#FFFFFF"
    theme.css_header_link_hover_color = "#e8f5e9"
    theme.css_module_background_color = "#4caf50"
    theme.css_module_text_color = "#FFFFFF"
    theme.css_module_link_color = "#FFFFFF"
    theme.css_module_link_hover_color = "#e8f5e9"
    theme.css_generic_link_color = "#4caf50"
    theme.css_generic_link_hover_color = "#2e7d32"
    theme.css_save_button_background_color = "#4caf50"
    theme.css_save_button_background_hover_color = "#2e7d32"
    theme.css_delete_button_background_color = "#f44336"
    theme.css_delete_button_background_hover_color = "#d32f2f"
    theme.list_filter_dropdown = True
    theme.related_modal_active = True
    theme.related_modal_background_color = "#4caf50"
    theme.related_modal_background_opacity = 0.8
    theme.save()
    
    print("Tema actualizado con éxito!")
    print(f"Título: {theme.title}")

if __name__ == "__main__":
    update_admin_theme()

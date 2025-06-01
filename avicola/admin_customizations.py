"""
Personalizaciones para el panel de administración de Django.
"""
from django.contrib import admin
from django.contrib.auth.models import Group, Permission
from django.contrib.auth.admin import GroupAdmin as BaseGroupAdmin

class CustomGroupAdmin(BaseGroupAdmin):
    """
    Personalización de la administración de grupos para mostrar más información.
    """
    list_display = ('name', 'get_users_count', 'get_permissions_count')
    search_fields = ('name',)
    filter_horizontal = ('permissions',)
    
    def get_users_count(self, obj):
        """Muestra el número de usuarios en el grupo."""
        return obj.user_set.count()
    get_users_count.short_description = 'Usuarios'
    
    def get_permissions_count(self, obj):
        """Muestra el número de permisos asignados al grupo."""
        return obj.permissions.count()
    get_permissions_count.short_description = 'Permisos'

def register_group_admin():
    """
    Función para registrar el admin de grupos personalizado.
    Se debe llamar después de que las aplicaciones estén listas.
    """
    try:
        # Solo registrar si el modelo Group está registrado
        if Group in admin.site._registry:
            admin.site.unregister(Group)
        admin.site.register(Group, CustomGroupAdmin)
    except Exception as e:
        print(f"Error registrando GroupAdmin personalizado: {str(e)}")

# No registramos aquí directamente, se hará desde apps.py cuando sea seguro

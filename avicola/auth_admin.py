"""
Custom admin configurations for authentication models.
This is in a separate file to avoid circular imports.
"""
from django.contrib import admin
from django.contrib.auth.admin import GroupAdmin as BaseGroupAdmin
from django.contrib.auth.models import Group, Permission

class GroupAdmin(BaseGroupAdmin):
    """Custom Group admin with additional functionality."""
    list_display = ('name', 'get_users_count', 'get_permissions_count')
    search_fields = ('name',)
    filter_horizontal = ('permissions',)
    
    def get_users_count(self, obj):
        """Return the number of users in the group."""
        # Use the correct related name for UserProfile
        return obj.userprofile_set.count()
    get_users_count.short_description = 'Usuarios'
    
    def get_permissions_count(self, obj):
        """Return the number of permissions assigned to the group."""
        return obj.permissions.count()
    get_permissions_count.short_description = 'Permisos'

class PermissionAdmin(admin.ModelAdmin):
    """Custom Permission admin with improved display."""
    list_display = ('name', 'content_type', 'codename')
    list_filter = ('content_type',)
    search_fields = ('name', 'codename')

def register_auth_models(admin_site):
    """Register auth models with the given admin site."""
    try:
        admin_site.register(Group, GroupAdmin)
        admin_site.register(Permission, PermissionAdmin)
        return True
    except Exception as e:
        print(f"Error registering auth models: {e}")
        return False

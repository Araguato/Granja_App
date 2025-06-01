from django.contrib import admin
from django.contrib.admin.sites import AdminSite
from django.contrib.auth.models import User, Group, Permission
from django.contrib.auth.admin import UserAdmin, GroupAdmin
from django.contrib.contenttypes.models import ContentType
from django.apps import apps

class CustomAdminSite(AdminSite):
    site_header = 'Administración de App Granja'
    site_title = 'App Granja Admin'
    index_title = 'Panel de Administración'
    
    def register(self, model_or_iterable, admin_class=None, **options):
        """
        Register model(s) with the admin interface.
        """
        if admin_class is None:
            admin_class = ModelAdmin
            
        # Handle both a single model and an iterable of models
        if isinstance(model_or_iterable, type):
            model_or_iterable = [model_or_iterable]
            
        for model in model_or_iterable:
            # Skip if already registered
            if model in self._registry:
                continue
                
            # Skip Galpon model from galpones app if it exists (legacy check)
            if (model.__module__ == 'galpones.models' and 
                model.__name__ == 'Galpon'):
                continue
                
            # Special handling for Galpon model in produccion app
            if model.__name__ == 'Galpon' and model.__module__ == 'produccion.models':
                # Import the GalponAdmin from produccion.admin
                from produccion.admin import GalponAdmin
                admin_class = GalponAdmin
            
            # Register the model with this admin site
            super(CustomAdminSite, self).register(model, admin_class, **options)
    
    def has_permission(self, request):
        """
        Override to ensure superusers have full access and other users have appropriate permissions
        """
        if not request.user.is_active:
            return False
            
        if request.user.is_superuser:
            return True
            
        # Check if user has any permissions for this app
        if not request.user.has_module_perms('produccion'):
            return False
            
        return super().has_permission(request)
        
    def get_app_list(self, request, app_label=None):
        """
        Return a sorted list of all the installed apps that have been
        registered in this site.
        """
        app_dict = self._build_app_dict(request)
        
        # Sort the apps alphabetically.
        app_list = sorted(app_dict.values(), key=lambda x: x['name'].lower())

        # Sort the models alphabetically within each app.
        for app in app_list:
            app['models'].sort(key=lambda x: x['name'].lower())
            
        return app_list

# Create an instance of our custom admin site
# Using 'admin' as the name to match the URL namespace expected by templates
# and setting the app_name and namespace to match Django's default admin site
custom_admin_site = CustomAdminSite(name='admin')
custom_admin_site._registry = {}
custom_admin_site._actions = {}
custom_admin_site._global_actions = {}
custom_admin_site._registry_globals = {}
custom_admin_site.name = 'admin'
custom_admin_site.app_name = 'admin'
custom_admin_site.namespace = 'admin'

# Register the default auth models with our custom admin site
from django.contrib.auth import get_user_model
User = get_user_model()

class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff')
    list_filter = ('is_staff', 'is_superuser', 'is_active')
    search_fields = ('username', 'first_name', 'last_name', 'email')

class CustomGroupAdmin(GroupAdmin):
    list_display = ('name',)
    search_fields = ('name',)

# Register the User and Group models with our custom admin site
custom_admin_site.register(User, CustomUserAdmin)
custom_admin_site.register(Group, CustomGroupAdmin)

# Auto-register all models
def auto_register_models():
    from django.apps import apps
    from django.contrib import admin
    from django.contrib.admin.sites import AlreadyRegistered
    
    # Only exclude these specific apps from auto-registration
    EXCLUDE_APPS = [
        'django_summernote',
        'admin_interface',
        'colorfield',
    ]
    
    for app_config in apps.get_app_configs():
        if app_config.label in EXCLUDE_APPS:
            print(f"Skipping app: {app_config.label}")
            continue
            
        for model in app_config.get_models():
            # Skip if already registered
            if model in custom_admin_site._registry:
                continue
                
            # Skip if it's from django.contrib.auth or django.contrib.contenttypes or sessions
            if model._meta.app_label in ['auth', 'contenttypes', 'sessions']:
                continue
                
            # Skip abstract models
            if model._meta.abstract:
                continue
                
            # Skip models that are already registered in other apps
            if model._meta.app_label in EXCLUDE_APPS:
                continue
                
            # Create a basic ModelAdmin for the model
            try:
                admin_class = type(
                    f'{model.__name__}Admin',
                    (admin.ModelAdmin,),
                    {
                        'list_display': [field.name for field in model._meta.fields[:5] 
                                      if field.name != 'id' and not field.is_relation],
                        'list_filter': [field.name for field in model._meta.fields 
                                      if field.get_internal_type() in ('CharField', 'BooleanField', 'IntegerField', 'DateField', 'DateTimeField')
                                      and not field.is_relation],
                        'search_fields': [field.name for field in model._meta.fields 
                                        if field.get_internal_type() in ('CharField', 'TextField')
                                        and not field.is_relation],
                    }
                )
                
                # Register the model with our custom admin site
                custom_admin_site.register(model, admin_class)
                print(f"Auto-registered {model._meta.app_label}.{model.__name__}")
                
            except AlreadyRegistered:
                # Skip if already registered
                pass
            except Exception as e:
                print(f"Error registering {model._meta.app_label}.{model.__name__}: {str(e)}")

# Call the auto-register function
try:
    auto_register_models()
except Exception as e:
    print(f"Error auto-registering models: {e}")

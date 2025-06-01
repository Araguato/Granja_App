import sys
from django.apps import AppConfig
from django.contrib import admin

class ProduccionConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'produccion'
    verbose_name = 'Producción Avícola'
    
    def ready(self):
        # Import signals first
        import produccion.signals  # noqa
        
        # Then handle admin registration
        try:
            from .models import Galpon
            from .admin_galpon import GalponAdmin
            
            # Register with the default admin site
            if admin.site.is_registered(Galpon):
                admin.site.unregister(Galpon)
            admin.site.register(Galpon, GalponAdmin)
            
            # Also register with custom admin site if it exists
            try:
                from avicola.custom_admin import custom_admin_site
                if custom_admin_site.is_registered(Galpon):
                    custom_admin_site.unregister(Galpon)
                custom_admin_site.register(Galpon, GalponAdmin)
            except ImportError:
                pass
                
        except Exception as e:
            # Log error but don't crash the app
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f'Error registering Galpon admin: {str(e)}')
        # Ensure the admin site is properly registered
        from django.urls import clear_url_caches
        from importlib import import_module
        from django.conf import settings
        
        # Clear URL caches to ensure our changes take effect
        clear_url_caches()
        
        # Reload the URL configuration
        try:
            urlconf = settings.ROOT_URLCONF
            if urlconf in sys.modules:
                import_module(urlconf)
        except Exception as e:
            print(f"Error reloading URL configuration: {e}")

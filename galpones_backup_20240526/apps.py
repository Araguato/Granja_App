from django.apps import AppConfig


class GalponesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'galpones'
    verbose_name = 'Gestión de Galpones'
    
    def ready(self):
        """
        Se ejecuta cuando la aplicación está lista.
        Puedes agregar señales o configuraciones iniciales aquí.
        """
        pass

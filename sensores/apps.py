import sys
from django.apps import AppConfig


class SensoresConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'sensores'
    
    def ready(self):
        try:
            from django.contrib import admin
            from .admin import (
                TipoSensorAdmin, SensorAdmin, 
                LecturaSensorAdmin, AlertaSensorAdmin
            )
            from .models import (
                TipoSensor, Sensor, 
                LecturaSensor, AlertaSensor
            )
            
            # Register models with the admin site
            admin.site.register(TipoSensor, TipoSensorAdmin)
            admin.site.register(Sensor, SensorAdmin)
            admin.site.register(LecturaSensor, LecturaSensorAdmin)
            admin.site.register(AlertaSensor, AlertaSensorAdmin)
            
        except ImportError as e:
            print(f"Error registering sensores admin: {e}", file=sys.stderr)
        except Exception as e:
            print(f"Unexpected error in sensores.ready(): {e}", file=sys.stderr)

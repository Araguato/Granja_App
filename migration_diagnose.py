import os
import sys
import django
from django.conf import settings

def diagnose_migrations():
    print("Diagnóstico de Migraciones Django")
    print("=" * 30)
    
    try:
        # Configurar Django
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'granja.settings')
        django.setup()
        
        # Verificar aplicaciones instaladas
        print("\nAplicaciones Instaladas:")
        for app in settings.INSTALLED_APPS:
            print(f"- {app}")
        
        # Verificar configuración de base de datos
        print("\nConfiguracion de Base de Datos:")
        print(f"ENGINE: {settings.DATABASES['default']['ENGINE']}")
        print(f"NAME: {settings.DATABASES['default']['NAME']}")
        
    except Exception as e:
        print(f"\nError en diagnóstico: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    diagnose_migrations()

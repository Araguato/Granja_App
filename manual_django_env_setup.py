import os
import sys

# Configurar variables de entorno manualmente
os.environ['DJANGO_SETTINGS_MODULE'] = 'granja.settings'
os.environ['DJANGO_SECRET_KEY'] = '@f)f*yi7@em5knj8&xeri7%qyqr*4mmg&yz4aj+rqj@i6*i$ai'
os.environ['DB_NAME'] = 'DB_Avicola'
os.environ['DB_USER'] = 'usuario_avicola'
os.environ['DB_PASSWORD'] = 'Aves2025'
os.environ['DB_HOST'] = 'localhost'
os.environ['DB_PORT'] = '5432'
os.environ['DJANGO_DEBUG'] = 'True'

def manual_django_setup():
    print("Manual Django Environment Setup")
    print("=" * 35)
    
    # Intentar importar y configurar Django
    try:
        import django
        django.setup()
        
        # Importar y mostrar configuraciones
        from django.conf import settings
        
        print("\nDjango Configuration:")
        print(f"Django Version: {django.get_version()}")
        print(f"Secret Key: {settings.SECRET_KEY}")
        print(f"Debug Mode: {settings.DEBUG}")
        
        print("\nInstalled Apps:")
        for app in settings.INSTALLED_APPS:
            print(f"  - {app}")
        
        print("\nDatabase Configuration:")
        print(settings.DATABASES)
    
    except Exception as e:
        print(f"\nError during Django setup: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    manual_django_setup()

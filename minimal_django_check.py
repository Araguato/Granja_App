import os
import sys

def minimal_django_check():
    print("Minimal Django Diagnostic")
    print("=" * 30)
    
    # Configurar entorno de Django
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'granja.settings')
    
    try:
        import django
        print(f"Django Version: {django.get_version()}")
        
        # Importar configuraciones
        from django.conf import settings
        print("\nInstalled Apps:")
        for app in settings.INSTALLED_APPS:
            print(f"  - {app}")
    
    except Exception as e:
        print(f"Error: {e}")
        print("\nDetailed Traceback:")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    minimal_django_check()

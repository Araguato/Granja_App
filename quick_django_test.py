import os
import sys

def quick_django_test():
    print("Quick Django Configuration Test")
    print("=" * 40)
    
    # Configurar path del proyecto
    project_root = os.path.abspath(os.path.dirname(__file__))
    sys.path.insert(0, project_root)
    
    # Configurar variables de entorno
    os.environ['DJANGO_SETTINGS_MODULE'] = 'granja.settings'
    
    try:
        import django
        django.setup()
        
        # Importar configuraciones
        from django.conf import settings
        
        print("\nDjango Configuration:")
        print(f"  Version: {django.get_version()}")
        print(f"  Debug: {settings.DEBUG}")
        print(f"  Secret Key: {settings.SECRET_KEY[:10]}...")
        
        print("\nInstalled Apps:")
        for app in settings.INSTALLED_APPS:
            print(f"  - {app}")
    
    except Exception as e:
        print(f"\n❌ Django setup error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    quick_django_test()

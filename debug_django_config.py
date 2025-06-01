import os
import sys
import django

def debug_django_configuration():
    print("Django Configuration Debug Tool")
    print("=" * 40)
    
    # Check environment variables
    print("\nEnvironment Variables:")
    print(f"DJANGO_SETTINGS_MODULE: {os.environ.get('DJANGO_SETTINGS_MODULE', 'NOT SET')}")
    
    # Check Python path
    print("\nPython Path:")
    for path in sys.path:
        print(f"  - {path}")
    
    # Try to set up Django manually
    try:
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'granja.settings')
        django.setup()
        
        # If successful, print installed apps
        from django.conf import settings
        print("\nInstalled Apps:")
        for app in settings.INSTALLED_APPS:
            print(f"  - {app}")
    
    except Exception as e:
        print("\nError during Django setup:")
        print(f"  {type(e).__name__}: {e}")
        
        # Additional debugging for import issues
        print("\nTrying to diagnose import issues:")
        try:
            import granja.settings
            print("  granja.settings module found")
        except ImportError as ie:
            print(f"  Import error: {ie}")

if __name__ == "__main__":
    debug_django_configuration()

import os
import sys
import django
from django.conf import settings

def diagnose_django():
    print("Django Diagnostic Tool")
    print("=" * 30)
    
    # Verify Python path
    print("\nPython Path:")
    for path in sys.path:
        print(path)
    
    # Verify Django installation
    print("\nDjango Version:")
    print(django.get_version())
    
    # Verify settings
    print("\nSettings Module:")
    print(f"DJANGO_SETTINGS_MODULE: {os.environ.get('DJANGO_SETTINGS_MODULE')}")
    
    # Verify installed apps
    print("\nInstalled Apps:")
    for app in settings.INSTALLED_APPS:
        print(app)
    
    # Check app configurations
    print("\nApp Configurations:")
    from django.apps import apps
    for app_config in apps.get_app_configs():
        print(f"{app_config.name}: {app_config.path}")

if __name__ == "__main__":
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'granja.settings')
    django.setup()
    diagnose_django()

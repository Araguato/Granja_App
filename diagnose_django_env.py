import os
import sys
import traceback

def diagnose_django_environment():
    print("Django Environment Diagnostic Tool")
    print("=" * 40)
    
    # Check current working directory
    print(f"\nCurrent Working Directory: {os.getcwd()}")
    
    # Check Python path
    print("\nPython Path:")
    for path in sys.path:
        print(f"  - {path}")
    
    # Check environment variables
    print("\nEnvironment Variables:")
    print(f"  DJANGO_SETTINGS_MODULE: {os.environ.get('DJANGO_SETTINGS_MODULE', 'NOT SET')}")
    
    # Attempt to set up Django manually
    try:
        # Ensure the project root is in Python path
        project_root = os.path.abspath(os.path.join(os.path.dirname(__file__)))
        if project_root not in sys.path:
            sys.path.insert(0, project_root)
        
        # Set the settings module
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'granja.settings')
        
        # Try to import Django and set it up
        import django
        django.setup()
        
        # If successful, print more details
        from django.conf import settings
        print("\nDjango Configuration:")
        print(f"  Django Version: {django.get_version()}")
        print("\nInstalled Apps:")
        for app in settings.INSTALLED_APPS:
            print(f"  - {app}")
        
        # Try to import apps
        from django.apps import apps
        print("\nApp Configurations:")
        for app_config in apps.get_app_configs():
            print(f"  {app_config.name}: {app_config.path}")
    
    except Exception as e:
        print("\nError during Django setup:")
        print(f"  {type(e).__name__}: {e}")
        print("\nDetailed Traceback:")
        traceback.print_exc()

if __name__ == "__main__":
    diagnose_django_environment()

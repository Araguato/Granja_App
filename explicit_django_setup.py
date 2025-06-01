import os
import sys
import django
from django.conf import settings
from django.core.management import call_command

# Configurar path del proyecto
project_root = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(0, project_root)

# Configurar variables de entorno
os.environ['DJANGO_SETTINGS_MODULE'] = 'granja.settings'

def explicit_django_setup():
    print("Explicit Django Setup and Check")
    print("=" * 35)
    
    try:
        # Configurar Django explícitamente
        django.setup()
        
        # Intentar acceder a configuraciones
        print("\nDjango Configuration:")
        print(f"Django Version: {django.get_version()}")
        print(f"Secret Key: {settings.SECRET_KEY}")
        print(f"Debug Mode: {settings.DEBUG}")
        
        # Intentar ejecutar verificaciones de sistema
        print("\nRunning System Checks...")
        from django.core.management.commands.check import Command as CheckCommand
        check_command = CheckCommand()
        issues = check_command.handle(deploy=True)
        
        if not issues:
            print("✅ No deployment issues found")
        else:
            print("❌ Deployment issues detected")
    
    except Exception as e:
        print(f"\nError during Django setup: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    explicit_django_setup()

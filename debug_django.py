import os
import sys
import traceback

def debug_django_setup():
    print("Debugging Django Setup")
    print("=" * 20)
    
    # Configuraciones
    print(f"Python Version: {sys.version}")
    print(f"Python Executable: {sys.executable}")
    print(f"Current Directory: {os.getcwd()}")
    
    # Intentar configurar Django
    try:
        import django
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'granja.settings')
        django.setup()
        print("Django setup successful!")
    except Exception as e:
        print(f"Error setting up Django: {e}")
        traceback.print_exc()

if __name__ == "__main__":
    debug_django_setup()

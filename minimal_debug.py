import os
import sys

def minimal_debug():
    print("Minimal Debug Information")
    print("=" * 30)
    
    # Información básica del sistema
    print(f"Python Executable: {sys.executable}")
    print(f"Current Working Directory: {os.getcwd()}")
    print(f"Python Version: {sys.version}")
    
    # Variables de entorno
    print("\nEnvironment Variables:")
    print(f"DJANGO_SETTINGS_MODULE: {os.environ.get('DJANGO_SETTINGS_MODULE', 'NOT SET')}")
    
    # Intentar importar Django de manera básica
    try:
        import django
        print(f"\nDjango Version: {django.get_version()}")
    except ImportError as e:
        print(f"\nError importing Django: {e}")

if __name__ == "__main__":
    minimal_debug()

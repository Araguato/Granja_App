import os
import sys
import django

def diagnose():
    print("Diagnóstico del Sistema Django")
    print("=" * 30)
    
    # Información del sistema
    print(f"Python Version: {sys.version}")
    print(f"Python Executable: {sys.executable}")
    print(f"Current Directory: {os.getcwd()}")
    
    # Verificar variables de entorno
    print("\nVariables de Entorno:")
    print(f"DJANGO_SETTINGS_MODULE: {os.environ.get('DJANGO_SETTINGS_MODULE', 'No configurado')}")
    
    # Intentar configurar Django
    try:
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'granja.settings')
        django.setup()
        print("\nConfiguracion de Django: Exitosa")
    except Exception as e:
        print(f"\nError configurando Django: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    diagnose()

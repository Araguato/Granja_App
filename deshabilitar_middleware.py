"""
Script para deshabilitar temporalmente el middleware problemático.
"""
import os
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'granja.settings')
django.setup()

from django.conf import settings
import sys

def main():
    print("Verificando configuración del middleware...")
    
    # Verificar si el middleware está en la configuración
    middleware_name = 'core.middleware.SupervisorPermissionsMiddleware'
    middleware_list = settings.MIDDLEWARE
    
    if middleware_name in middleware_list:
        print(f"El middleware '{middleware_name}' está activo en la configuración.")
        
        # Crear copia de seguridad del archivo settings.py
        settings_path = os.path.join(settings.BASE_DIR, 'granja', 'settings.py')
        backup_path = os.path.join(settings.BASE_DIR, 'granja', 'settings.py.bak')
        
        print(f"Creando copia de seguridad de settings.py en {backup_path}")
        try:
            with open(settings_path, 'r', encoding='utf-8') as f:
                settings_content = f.read()
            
            with open(backup_path, 'w', encoding='utf-8') as f:
                f.write(settings_content)
            
            print("Copia de seguridad creada correctamente.")
            
            # Modificar el archivo settings.py para comentar el middleware
            print("Deshabilitando el middleware problemático...")
            new_content = settings_content.replace(
                f"    '{middleware_name}',",
                f"    # '{middleware_name}',  # Deshabilitado temporalmente"
            )
            
            with open(settings_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            
            print("Middleware deshabilitado correctamente.")
            print("\nIMPORTANTE:")
            print("1. Reinicia el servidor Django")
            print("2. Pide a los supervisores que cierren sesión y vuelvan a iniciar sesión")
            print("3. Intenta acceder nuevamente a las secciones problemáticas")
            print("\nSi deseas restaurar la configuración original, ejecuta:")
            print(f"copy {backup_path} {settings_path}")
            
        except Exception as e:
            print(f"Error al modificar el archivo settings.py: {e}")
    else:
        print(f"El middleware '{middleware_name}' no está activo en la configuración.")

if __name__ == "__main__":
    main()

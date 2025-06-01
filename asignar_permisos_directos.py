"""
Script para asignar permisos directamente a los usuarios supervisores.
Este script evita el uso del middleware y asigna los permisos directamente en la base de datos.
"""
import os
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'granja.settings')
django.setup()

from django.contrib.auth.models import Permission
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType

User = get_user_model()

def main():
    print("Asignando permisos directamente a los usuarios supervisores...")
    
    # Obtener todos los usuarios supervisores
    supervisores = User.objects.filter(user_type='SUPERVISOR')
    if not supervisores.exists():
        print("No se encontraron usuarios con rol de supervisor.")
        return
    
    print(f"Se encontraron {supervisores.count()} supervisores.")
    
    try:
        # Obtener el content type para MortalidadDiaria
        try:
            mortalidad_ct = ContentType.objects.get(app_label='produccion', model='mortalidaddiaria')
            print("Content Type para MortalidadDiaria encontrado.")
        except ContentType.DoesNotExist:
            print("Error: No se encontró el Content Type para MortalidadDiaria.")
            return
        
        # Obtener permisos para MortalidadDiaria
        permisos = []
        for accion in ['add', 'change', 'view', 'delete']:
            codename = f"{accion}_mortalidaddiaria"
            try:
                permiso = Permission.objects.get(content_type=mortalidad_ct, codename=codename)
                permisos.append(permiso)
                print(f"Permiso '{codename}' encontrado.")
            except Permission.DoesNotExist:
                print(f"Creando permiso '{codename}'...")
                permiso = Permission.objects.create(
                    content_type=mortalidad_ct,
                    codename=codename,
                    name=f"Can {accion} mortalidad diaria"
                )
                permisos.append(permiso)
        
        # Asignar permisos a cada supervisor
        for supervisor in supervisores:
            print(f"\nActualizando usuario: {supervisor.username}")
            
            # Asegurar que el usuario tenga is_staff=True
            if not supervisor.is_staff:
                supervisor.is_staff = True
                supervisor.save(update_fields=['is_staff'])
                print("✓ is_staff establecido a True")
            else:
                print("✓ is_staff ya era True")
            
            # Asignar permisos directamente al usuario
            for permiso in permisos:
                if permiso not in supervisor.user_permissions.all():
                    supervisor.user_permissions.add(permiso)
                    print(f"✓ Permiso '{permiso.codename}' asignado")
                else:
                    print(f"✓ Permiso '{permiso.codename}' ya estaba asignado")
            
            print(f"Usuario {supervisor.username} actualizado correctamente.")
        
        print("\nPermisos asignados correctamente a todos los supervisores.")
        print("\nIMPORTANTE:")
        print("1. Reinicia el servidor Django")
        print("2. Pide a los supervisores que cierren sesión y vuelvan a iniciar sesión")
        print("3. Intenta acceder a: http://127.0.0.1:8000/admin/produccion/mortalidaddiaria/add/")
    
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()

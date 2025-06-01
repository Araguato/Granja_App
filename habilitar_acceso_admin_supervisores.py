"""
Script para habilitar el acceso al panel de administración para todos los supervisores.
"""
import os
import django

# Configurar el entorno de Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'granja.settings')
django.setup()

from django.contrib.auth.models import Group
from avicola.models import UserProfile

def habilitar_acceso_admin():
    """
    Habilita el acceso al panel de administración para todos los supervisores
    configurando el atributo is_staff=True.
    """
    print("Habilitando acceso al panel de administración para supervisores...")
    
    try:
        # Obtener el grupo de Supervisores
        grupo_supervisores = Group.objects.get(name='Supervisores')
        
        # Obtener todos los usuarios que pertenecen al grupo de Supervisores
        supervisores = UserProfile.objects.filter(groups=grupo_supervisores)
        
        if not supervisores.exists():
            print("No se encontraron usuarios en el grupo de Supervisores.")
            return
        
        # Contar cuántos supervisores necesitan actualización
        supervisores_actualizados = 0
        
        # Actualizar el atributo is_staff para cada supervisor
        for supervisor in supervisores:
            if not supervisor.is_staff:
                supervisor.is_staff = True
                supervisor.save()
                supervisores_actualizados += 1
                print(f"Usuario {supervisor.username} ahora tiene acceso al panel de administración.")
        
        # Resumen
        if supervisores_actualizados > 0:
            print(f"\nSe ha habilitado el acceso al panel de administración para {supervisores_actualizados} supervisores.")
        else:
            print("\nTodos los supervisores ya tenían acceso al panel de administración.")
        
        print(f"Total de supervisores en el sistema: {supervisores.count()}")
        
    except Group.DoesNotExist:
        print("No se encontró el grupo 'Supervisores'. Debe crear este grupo primero.")
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    habilitar_acceso_admin()

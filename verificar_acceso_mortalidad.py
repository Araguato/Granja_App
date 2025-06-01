"""
Script para verificar el acceso a la URL específica de MortalidadDiaria.
"""
import os
import django
import sys

# Configurar el entorno de Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'granja.settings')
django.setup()

from django.contrib.auth.models import Group, Permission
from avicola.models import UserProfile
from django.urls import reverse
from django.test import Client
from django.contrib.auth import get_user_model

def verificar_acceso_mortalidad():
    """
    Verifica si un supervisor puede acceder a la URL de MortalidadDiaria.
    """
    print("Verificando acceso a MortalidadDiaria...")
    
    try:
        # Obtener un usuario supervisor
        supervisores = UserProfile.objects.filter(user_type='SUPERVISOR', is_staff=True)
        if not supervisores.exists():
            print("No se encontraron usuarios supervisores con is_staff=True.")
            return
        
        supervisor = supervisores.first()
        print(f"Verificando acceso para el supervisor: {supervisor.username}")
        
        # Verificar los permisos del supervisor
        print("\nPermisos del supervisor:")
        permisos_usuario = supervisor.get_all_permissions()
        for permiso in sorted(permisos_usuario):
            print(f"- {permiso}")
        
        # Verificar los grupos del supervisor
        print("\nGrupos del supervisor:")
        for grupo in supervisor.groups.all():
            print(f"- {grupo.name}")
            print("  Permisos del grupo:")
            for permiso in grupo.permissions.all():
                print(f"  - {permiso.codename}: {permiso.name}")
        
        # Verificar atributos importantes
        print("\nAtributos importantes:")
        print(f"- is_active: {supervisor.is_active}")
        print(f"- is_staff: {supervisor.is_staff}")
        print(f"- is_superuser: {supervisor.is_superuser}")
        print(f"- user_type: {supervisor.user_type}")
        
        print("\nPara acceder a la URL /admin/produccion/mortalidaddiaria/add/, el supervisor debe:")
        print("1. Tener is_staff=True")
        print("2. Tener el permiso 'add_mortalidaddiaria'")
        print("3. Tener permisos para acceder al admin (view_logentry, etc.)")
        
        # Verificar si tiene el permiso específico
        if 'produccion.add_mortalidaddiaria' in permisos_usuario:
            print("\n✅ El supervisor tiene el permiso 'produccion.add_mortalidaddiaria'")
        else:
            print("\n❌ El supervisor NO tiene el permiso 'produccion.add_mortalidaddiaria'")
        
        # Verificar si tiene acceso al admin
        if supervisor.is_staff:
            print("✅ El supervisor tiene is_staff=True")
        else:
            print("❌ El supervisor NO tiene is_staff=True")
        
        # Verificar si tiene permisos de admin.logentry
        if 'admin.view_logentry' in permisos_usuario:
            print("✅ El supervisor tiene el permiso 'admin.view_logentry'")
        else:
            print("❌ El supervisor NO tiene el permiso 'admin.view_logentry'")
        
        print("\nRecomendaciones:")
        print("1. Asegúrate de que el servidor Django se haya reiniciado después de los cambios")
        print("2. Verifica que el usuario supervisor haya cerrado sesión y vuelto a iniciar sesión")
        print("3. Limpia las cookies del navegador para eliminar cualquier sesión antigua")
        print("4. Si el problema persiste, considera reiniciar el servidor Django")
        
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    verificar_acceso_mortalidad()

"""
Script para asignar permisos a todos los supervisores existentes.
Este script debe ejecutarse con el entorno de Django activado.
"""
import os
import django

# Configurar el entorno de Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'granja.settings')
django.setup()

# Importar los modelos necesarios
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from avicola.models import UserProfile
from produccion.models import Lote, Galpon, SeguimientoDiario
from inventario.models import Vacuna, Alimento, Raza

def asignar_permisos_supervisores():
    """Asignar permisos a todos los supervisores existentes"""
    # Obtener todos los usuarios con tipo SUPERVISOR
    supervisores = UserProfile.objects.filter(user_type='SUPERVISOR')
    contador = 0
    
    print(f"Encontrados {supervisores.count()} supervisores.")
    
    # Lista de modelos a los que queremos dar permisos
    models_to_grant = [
        Lote, Galpon, SeguimientoDiario,  # Modelos de producción
        Vacuna, Alimento, Raza,          # Modelos de inventario
    ]
    
    # Para cada supervisor
    for supervisor in supervisores:
        print(f"Asignando permisos a: {supervisor.username} ({supervisor.get_full_name()})")
        
        # Para cada modelo, otorgamos todos los permisos
        for model in models_to_grant:
            content_type = ContentType.objects.get_for_model(model)
            permissions = Permission.objects.filter(content_type=content_type)
            
            for permission in permissions:
                supervisor.user_permissions.add(permission)
                print(f"  - Añadido permiso: {permission.codename}")
        
        # También asignamos permisos para ver el dashboard y otras funcionalidades básicas
        basic_permissions = [
            'view_dashboard',  # Permiso personalizado definido en Empresa
        ]
        
        for perm_codename in basic_permissions:
            try:
                perm = Permission.objects.get(codename=perm_codename)
                supervisor.user_permissions.add(perm)
                print(f"  - Añadido permiso básico: {perm_codename}")
            except Permission.DoesNotExist:
                print(f"  - Permiso no encontrado: {perm_codename}")
        
        # También asignamos permisos para acceder a la administración
        supervisor.is_staff = True
        supervisor.save()
        
        contador += 1
    
    print(f"\nSe han actualizado los permisos de {contador} supervisores.")

if __name__ == "__main__":
    asignar_permisos_supervisores()

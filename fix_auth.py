import os
import django
import sys

# Configure Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'granja.settings')
django.setup()

# Import models
from avicola.models import UserProfile
from django.contrib.auth.hashers import make_password
from django.db import connection

def check_auth_tables():
    """Verifica si las tablas de autenticación existen y están configuradas correctamente"""
    with connection.cursor() as cursor:
        # Verificar si la tabla de usuarios existe
        cursor.execute("""
        SELECT EXISTS (
            SELECT FROM information_schema.tables 
            WHERE table_name = 'avicola_userprofile'
        );
        """)
        user_table_exists = cursor.fetchone()[0]
        
        if not user_table_exists:
            print("ERROR: La tabla avicola_userprofile no existe.")
            return False
        
        # Verificar si las columnas necesarias existen
        cursor.execute("""
        SELECT column_name FROM information_schema.columns 
        WHERE table_name = 'avicola_userprofile';
        """)
        columns = [row[0] for row in cursor.fetchall()]
        
        required_columns = ['username', 'password', 'is_superuser', 'is_staff', 'is_active']
        missing_columns = [col for col in required_columns if col not in columns]
        
        if missing_columns:
            print(f"ERROR: Faltan columnas en la tabla de usuarios: {missing_columns}")
            return False
            
        print("Las tablas de autenticación están correctamente configuradas.")
        return True

def fix_user_permissions():
    """Asegura que los usuarios tengan los permisos correctos"""
    try:
        # Obtener todos los usuarios
        users = UserProfile.objects.all()
        print(f"Encontrados {len(users)} usuarios en la base de datos.")
        
        # Verificar y corregir permisos
        for user in users:
            if user.username == 'admin':
                user.is_superuser = True
                user.is_staff = True
                user.is_active = True
                # Establecer una contraseña conocida
                user.password = make_password('admin123')
                user.save()
                print(f"Usuario {user.username} actualizado con permisos de superusuario y contraseña 'admin123'")
            elif user.user_type == 'ADMIN':
                user.is_superuser = True
                user.is_staff = True
                user.is_active = True
                # Establecer una contraseña conocida
                user.password = make_password('admin123')
                user.save()
                print(f"Usuario {user.username} actualizado con permisos de superusuario y contraseña 'admin123'")
        
        return True
    except Exception as e:
        print(f"ERROR al actualizar permisos de usuarios: {e}")
        return False

def create_new_superuser():
    """Crea un nuevo superusuario con credenciales conocidas"""
    try:
        # Crear un nuevo superusuario
        superuser = UserProfile.objects.create(
            username='superadmin',
            email='superadmin@example.com',
            first_name='Super',
            last_name='Admin',
            user_type='ADMIN',
            is_superuser=True,
            is_staff=True,
            is_active=True,
            password=make_password('superadmin123')
        )
        print(f"Nuevo superusuario creado: username='superadmin', password='superadmin123'")
        return True
    except Exception as e:
        print(f"ERROR al crear nuevo superusuario: {e}")
        return False

if __name__ == '__main__':
    print("Verificando y reparando problemas de autenticación...")
    
    # Verificar tablas
    tables_ok = check_auth_tables()
    
    # Corregir permisos de usuarios existentes
    permissions_ok = fix_user_permissions()
    
    # Crear nuevo superusuario
    new_user_ok = create_new_superuser()
    
    if tables_ok and permissions_ok and new_user_ok:
        print("\nReparación completada con éxito.")
        print("\nPuedes iniciar sesión con cualquiera de estas credenciales:")
        print("1. Usuario: admin, Contraseña: admin123")
        print("2. Usuario: superadmin, Contraseña: superadmin123")
    else:
        print("\nSe encontraron problemas durante la reparación.")

import os
import django

# Configure Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'granja.settings')
django.setup()

# Import UserProfile model
from avicola.models import UserProfile

# Check if the superuser already exists
if not UserProfile.objects.filter(username='admin').exists():
    # Create a superuser
    superuser = UserProfile.objects.create_superuser(
        username='admin',
        email='admin@example.com',
        password='admin123',  # Cambia esta contraseña
        first_name='Administrador',
        last_name='Sistema',
        user_type='ADMIN'
    )
    print(f"Superusuario '{superuser.username}' creado exitosamente.")
else:
    print("El superusuario 'admin' ya existe.")
    
    # Reset password for existing admin user
    admin_user = UserProfile.objects.get(username='admin')
    admin_user.set_password('admin123')  # Cambia esta contraseña
    admin_user.save()
    print("Contraseña del superusuario 'admin' actualizada.")

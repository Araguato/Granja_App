from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from produccion.models import Galpon

class Command(BaseCommand):
    help = 'Check Galpon records and their visibility in admin'

    def handle(self, *args, **options):
        # Check if any Galpon records exist
        galpones = Galpon.objects.all()
        self.stdout.write(self.style.SUCCESS(f'Found {galpones.count()} Galpon records in the database'))
        
        # Display basic info about each Galpon
        for galpon in galpones:
            self.stdout.write(f"- {galpon.numero_galpon} (ID: {galpon.id}) - {galpon.granja.nombre if galpon.granja else 'No Granja'}")
        
        # Check permissions for the Galpon model
        content_type = ContentType.objects.get_for_model(Galpon)
        permissions = Permission.objects.filter(content_type=content_type)
        
        self.stdout.write("\nPermissions for Galpon model:")
        for perm in permissions:
            self.stdout.write(f"- {perm.codename} ({perm.name})")
        
        # Check if the default admin user has the right permissions
        User = get_user_model()
        try:
            admin = User.objects.get(username='admin')
            self.stdout.write(f"\nChecking permissions for user 'admin':")
            self.stdout.write(f"- Is superuser: {admin.is_superuser}")
            self.stdout.write(f"- Is staff: {admin.is_staff}")
            self.stdout.write(f"- Has 'view_galpon' permission: {admin.has_perm('produccion.view_galpon')}")
            
        except User.DoesNotExist:
            self.stdout.write(self.style.WARNING("User 'admin' does not exist"))
        
        # Check if the Galpon model is properly registered in admin
        from django.contrib import admin
        from produccion.models import Galpon as GalponModel
        
        if admin.site.is_registered(GalponModel):
            self.stdout.write(self.style.SUCCESS("\nGalpon model is registered in the default admin site"))
        else:
            self.stdout.write(self.style.ERROR("Galpon model is NOT registered in the default admin site"))
            
        # Check if the custom admin site has the Galpon model registered
        from avicola.custom_admin import custom_admin_site
        if GalponModel in custom_admin_site._registry:
            self.stdout.write(self.style.SUCCESS("Galpon model is registered in the custom admin site"))
        else:
            self.stdout.write(self.style.ERROR("Galpon model is NOT registered in the custom admin site"))

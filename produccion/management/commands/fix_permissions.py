from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.apps import apps

class Command(BaseCommand):
    help = 'Fix permissions for production models and assign them to appropriate groups'

    def handle(self, *args, **options):
        # Get or create groups
        supervisor_group, created = Group.objects.get_or_create(name='Supervisores')
        admin_group, created = Group.objects.get_or_create(name='Administradores')
        
        # Get content type for production models
        try:
            content_type = ContentType.objects.get(app_label='produccion', model='galpon')
            
            # Get all permissions for Galpon model
            permissions = Permission.objects.filter(content_type=content_type)
            
            # Assign permissions to groups
            for perm in permissions:
                supervisor_group.permissions.add(perm)
                admin_group.permissions.add(perm)
                
            self.stdout.write(self.style.SUCCESS('Successfully updated permissions for Galpon model'))
            
            # Also ensure other production models have correct permissions
            models = ['granja', 'lote', 'seguimientodiario', 'mortalidaddiaria', 'mortalidadsemanal', 'seguimientoengorde', 'consumoenergia']
            
            for model_name in models:
                try:
                    ct = ContentType.objects.get(app_label='produccion', model=model_name)
                    perms = Permission.objects.filter(content_type=ct)
                    for perm in perms:
                        admin_group.permissions.add(perm)
                        if model_name in ['granja', 'lote', 'seguimientodiario']:
                            supervisor_group.permissions.add(perm)
                except ContentType.DoesNotExist:
                    self.stdout.write(self.style.WARNING(f'ContentType for produccion.{model_name} does not exist'))
            
            self.stdout.write(self.style.SUCCESS('Successfully updated all production model permissions'))
            
        except ContentType.DoesNotExist:
            self.stdout.write(self.style.ERROR('ContentType for produccion.galpon does not exist'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error updating permissions: {str(e)}'))

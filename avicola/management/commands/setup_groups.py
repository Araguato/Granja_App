from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.db import transaction
from django.apps import apps

class Command(BaseCommand):
    help = 'Sets up default user groups with appropriate permissions'

    def handle(self, *args, **options):
        # Clear existing groups
        Group.objects.all().delete()
        
        # Define model to app mapping
        MODEL_APP_MAPPING = {
            # inventario app
            'alimento': 'inventario',
            'aplicacionvacuna': 'inventario',
            'consumoalimento': 'inventario',
            'guiadesempenoraza': 'inventario',
            'insumo': 'inventario',
            'proveedor': 'inventario',
            'raza': 'inventario',
            'vacuna': 'inventario',
            
            # produccion app
            'consumoenergia': 'produccion',
            'galpon': 'produccion',
            'granja': 'produccion',
            'lote': 'produccion',
            'mortalidaddiaria': 'produccion',
            'mortalidadsemanal': 'produccion',
            'seguimientodiario': 'produccion',
            'seguimientoengorde': 'produccion',
            
            # reportes app
            'plantillareporte': 'reportes',
            'reportegenerado': 'reportes',
            
            # ventas app
            'cliente': 'ventas',
            'detalleventa': 'ventas',
            'inventariohuevos': 'ventas',
            'tipohuevo': 'ventas',
            'venta': 'ventas',
            
            # wiki app
            'article': 'wiki',
            'category': 'wiki',
            
            # faq app
            'faq': 'faq',
            'faqcategory': 'faq',
        }

        # Define group permissions
        groups = {
            'Veterinarios': {
                'view': [
                    'alimento', 'aplicacionvacuna', 'consumoalimento', 'guiadesempenoraza',
                    'insumo', 'proveedor', 'raza', 'vacuna', 'consumoenergia', 'galpon',
                    'granja', 'lote', 'mortalidaddiaria', 'mortalidadsemanal',
                    'seguimientodiario', 'seguimientoengorde', 'plantillareporte',
                    'reportegenerado', 'cliente', 'detalleventa', 'inventariohuevos',
                    'tipohuevo', 'venta'
                ]
            },
            'Operarios': {
                'add': [
                    'lote', 'mortalidaddiaria', 'mortalidadsemanal', 'seguimientodiario',
                    'seguimientoengorde', 'consumoalimento', 'aplicacionvacuna',
                    'inventariohuevos', 'venta', 'detalleventa'
                ],
                'change': [
                    'lote', 'mortalidaddiaria', 'mortalidadsemanal', 'seguimientodiario',
                    'seguimientoengorde', 'consumoalimento', 'inventariohuevos'
                ],
                'view': [
                    'alimento', 'aplicacionvacuna', 'consumoalimento', 'guiadesempenoraza',
                    'insumo', 'proveedor', 'raza', 'vacuna', 'consumoenergia', 'galpon',
                    'granja', 'lote', 'mortalidaddiaria', 'mortalidadsemanal',
                    'seguimientodiario', 'seguimientoengorde', 'plantillareporte',
                    'reportegenerado', 'cliente', 'detalleventa', 'inventariohuevos',
                    'tipohuevo', 'venta'
                ]
            },
            'Supervisores': {
                'all': [
                    'alimento', 'aplicacionvacuna', 'consumoalimento', 'guiadesempenoraza',
                    'insumo', 'proveedor', 'raza', 'vacuna', 'consumoenergia', 'galpon',
                    'granja', 'lote', 'mortalidaddiaria', 'mortalidadsemanal',
                    'seguimientodiario', 'seguimientoengorde', 'plantillareporte',
                    'reportegenerado', 'cliente', 'detalleventa', 'inventariohuevos',
                    'tipohuevo', 'venta', 'faq', 'faqcategory', 'article', 'category'
                ]
            },
            'Administradores': {
                'all': '__all__'  # Full access to everything
            }
        }

        # Helper function to get content type for a model
        def get_content_type(model_name):
            app_label = MODEL_APP_MAPPING.get(model_name.lower())
            if not app_label:
                self.stdout.write(self.style.WARNING(f'No app label found for model: {model_name}'))
                return None
                
            try:
                return ContentType.objects.get(app_label=app_label, model=model_name.lower())
            except ContentType.DoesNotExist:
                self.stdout.write(self.style.WARNING(f'ContentType does not exist for {app_label}.{model_name}'))
                return None

        with transaction.atomic():
            for group_name, perms_config in groups.items():
                group, created = Group.objects.get_or_create(name=group_name)
                self.stdout.write(self.style.SUCCESS(f'Processing group: {group_name}'))
                
                if perms_config.get('all') == '__all__':
                    # Add all permissions
                    group.permissions.set(Permission.objects.all())
                else:
                    # Add specific permissions
                    for perm_type, model_names in perms_config.items():
                        if perm_type == 'all':
                            # Handle 'all' permission type
                            for model_name in model_names:
                                content_type = get_content_type(model_name)
                                if content_type:
                                    perms = Permission.objects.filter(content_type=content_type)
                                    group.permissions.add(*perms)
                        else:
                            # Handle specific permission types (add, change, view, delete)
                            for model_name in model_names:
                                content_type = get_content_type(model_name)
                                if content_type:
                                    codename = f'{perm_type}_{model_name.lower()}'
                                    try:
                                        perm = Permission.objects.get(
                                            content_type=content_type, 
                                            codename=codename
                                        )
                                        group.permissions.add(perm)
                                    except Permission.DoesNotExist:
                                        self.stdout.write(self.style.WARNING(
                                            f'Permission {perm_type} for {model_name} does not exist (codename: {codename})'
                                        ))

        self.stdout.write(self.style.SUCCESS('Successfully set up default groups and permissions'))
from django.core.management.base import BaseCommand
from inventario.models import Alimento, Proveedor

class Command(BaseCommand):
    help = 'Crea alimentos de ejemplo con datos nutricionales'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Creando alimentos de ejemplo con datos nutricionales...'))
        
        # Obtener o crear un proveedor
        proveedor, created = Proveedor.objects.get_or_create(
            rif='J-87654321-0',
            defaults={
                'nombre': 'Alimentos Premium, C.A.',
                'contacto_principal': 'Juan Pérez',
                'telefono': '0412-9876543',
                'email': 'ventas@alimentospremium.com'
            }
        )
        
        if created:
            self.stdout.write(self.style.SUCCESS('Proveedor creado'))
        else:
            self.stdout.write(self.style.SUCCESS('Proveedor existente utilizado'))
        
        # Alimentos con datos nutricionales
        alimentos = [
            ('Iniciador Broiler', 'Alimento para pollos de engorde', 'CONCENTRADO', 'INICIADOR', 23.0, 3100, 5.0, 3.0, 1.0, 0.5, 1.3),
            ('Crecimiento Broiler', 'Alimento para pollos en crecimiento', 'CONCENTRADO', 'CRECIMIENTO', 21.0, 3150, 6.0, 3.5, 0.9, 0.45, 1.2),
            ('Finalizador Broiler', 'Alimento para pollos en etapa final', 'CONCENTRADO', 'ENGORDE_FINALIZADOR', 19.0, 3200, 7.0, 3.2, 0.85, 0.42, 1.1),
            ('Pre-Postura', 'Alimento para gallinas antes de postura', 'CONCENTRADO', 'PREPOSTURA', 18.0, 2900, 4.0, 4.0, 2.5, 0.5, 0.9),
            ('Postura Fase 1', 'Alimento para gallinas en postura inicial', 'CONCENTRADO', 'POSTURA_FASE1', 17.5, 2850, 4.5, 3.8, 3.8, 0.45, 0.85)
        ]
        
        for nombre, descripcion, tipo, etapa, proteina, energia, grasa, fibra, calcio, fosforo, lisina in alimentos:
            alimento, created = Alimento.objects.update_or_create(
                nombre=nombre,
                defaults={
                    'proveedor': proveedor,
                    'descripcion': descripcion,
                    'tipo_alimento': tipo,
                    'etapa': etapa,
                    'contenido_proteina': proteina,
                    'energia_metabolizable': energia,
                    'grasa_cruda': grasa,
                    'fibra_cruda': fibra,
                    'calcio': calcio,
                    'fosforo': fosforo,
                    'lisina': lisina
                }
            )
            
            if created:
                self.stdout.write(self.style.SUCCESS(f'Alimento "{nombre}" creado'))
            else:
                self.stdout.write(self.style.SUCCESS(f'Alimento "{nombre}" actualizado'))
        
        self.stdout.write(self.style.SUCCESS('¡Creación de alimentos completada con éxito!'))

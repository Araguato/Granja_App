from django.core.management.base import BaseCommand
from produccion.models import Galpon

class Command(BaseCommand):
    help = 'Check Galpon data in the database'

    def handle(self, *args, **options):
        galpones = Galpon.objects.all().select_related('granja', 'responsable')
        
        if not galpones.exists():
            self.stdout.write(self.style.WARNING('No Galpones found in the database!'))
            return
            
        self.stdout.write(self.style.SUCCESS(f'Found {galpones.count()} Galpones in the database:'))
        
        for galpon in galpones:
            self.stdout.write(f"\nGalpón: {galpon.numero_galpon}")
            self.stdout.write(f"  Granja: {galpon.granja.nombre if galpon.granja else 'None'}")
            self.stdout.write(f"  Tipo: {galpon.get_tipo_galpon_display()}")
            self.stdout.write(f"  Responsable: {galpon.responsable.get_full_name() if galpon.responsable else 'None'}")
            self.stdout.write(f"  Capacidad: {galpon.capacidad_aves} aves")
            self.stdout.write(f"  Área: {galpon.area_metros_cuadrados or 'N/A'} m²")

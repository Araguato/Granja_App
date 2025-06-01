from django.core.management.base import BaseCommand
from inventario.models import Raza, GuiaDesempenoRaza
from decimal import Decimal

# Performance data for Ross 308 AP (Broiler)
ROSS_308_AP_DATA = [
    # Week, Weight (g), Daily Feed (g/bird), FCR, Viability (%)
    (1, 180, 25, 1.15, 99.0),
    (2, 460, 60, 1.25, 98.8),
    (3, 880, 100, 1.35, 98.5),
    (4, 1420, 140, 1.45, 98.2),
    (5, 2020, 175, 1.55, 98.0),
    (6, 2660, 210, 1.65, 97.8),
    (7, 3330, 245, 1.75, 97.5),
    (8, 4000, 275, 1.85, 97.2),
]

# Performance data for Cobb 500 (Broiler)
COBB_500_DATA = [
    # Week, Weight (g), Daily Feed (g/bird), FCR, Viability (%)
    (1, 175, 24, 1.16, 99.1),
    (2, 450, 58, 1.26, 98.9),
    (3, 870, 98, 1.36, 98.6),
    (4, 1410, 138, 1.46, 98.3),
    (5, 2010, 173, 1.56, 98.1),
    (6, 2650, 208, 1.66, 97.9),
    (7, 3320, 243, 1.76, 97.6),
    (8, 3990, 273, 1.86, 97.3),
]

class Command(BaseCommand):
    help = 'Importa datos de rendimiento para razas de pollos (Ross 308 AP y Cobb 500)'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Iniciando importación de datos de razas...'))
        
        # Create or update Ross 308 AP
        ross, created = Raza.objects.update_or_create(
            nombre='Ross 308 AP',
            defaults={
                'tipo_raza': 'ENGORDE',
                'descripcion': 'Ross 308 AP es un pollo de engorde de alto rendimiento con excelente conversión alimenticia y rendimiento de pechuga.'
            }
        )
        self._import_breed_data(ross, ROSS_308_AP_DATA, 'Ross 308 AP')
        
        # Create or update Cobb 500
        cobb, created = Raza.objects.update_or_create(
            nombre='Cobb 500',
            defaults={
                'tipo_raza': 'ENGORDE',
                'descripcion': 'Cobb 500 es una raza de pollo de engorde con excelente crecimiento, eficiencia alimenticia y rendimiento de carne.'
            }
        )
        self._import_breed_data(cobb, COBB_500_DATA, 'Cobb 500')
        
        self.stdout.write(self.style.SUCCESS('¡Importación completada exitosamente!'))
    
    def _import_breed_data(self, raza, data, raza_nombre):
        self.stdout.write(f'Importando datos para {raza_nombre}...')
        
        for week, weight, daily_feed, fcr, viability in data:
            # Calculate values for the week
            days = week * 7
            
            # Create or update the performance guide for this week
            GuiaDesempenoRaza.objects.update_or_create(
                raza=raza,
                dia_edad=days,
                defaults={
                    'peso_corporal_ideal_gr': Decimal(weight),
                    'consumo_alimento_diario_ideal_gr_ave': Decimal(daily_feed),
                    'consumo_alimento_acumulado_ideal_gr_ave': self._calculate_consumo_acumulado(daily_feed, days),
                    'conversion_alimenticia_ideal': Decimal(str(fcr)),
                    'mortalidad_acumulada_ideal_porc': Decimal(100 - float(viability)).quantize(Decimal('0.01')),
                    'ganancia_peso_diaria_ideal_gr': Decimal(weight / days).quantize(Decimal('0.01')),
                    'consumo_agua_diario_ideal_ml_ave': Decimal(float(daily_feed) * 1.8).quantize(Decimal('0.01')),  # Estimate water consumption as 1.8x feed
                    'viabilidad_ideal_porc': Decimal(viability),
                    'epef_ideal': self._calculate_epef(weight, fcr, viability, days),
                    'ie_ideal': self._calculate_ie(weight, fcr, days)
                }
            )
            
            self.stdout.write(f'  - Semana {week} (Día {days}): {weight}g, {daily_feed}g/día, FCR: {fcr}, Viabilidad: {viability}%')
    
    def _calculate_epef(self, weight, fcr, viability, age_days):
        """Calculate European Production Efficiency Factor"""
        try:
            epef = (Decimal(weight) * Decimal(viability/100)) / (Decimal(fcr) * Decimal(age_days)) * 100
            return epef.quantize(Decimal('0.01'))
        except:
            return None
    
    def _calculate_ie(self, weight, fcr, age_days):
        """Calculate Efficiency Index"""
        try:
            ie = (Decimal(weight) / (Decimal(fcr) * Decimal(age_days))) * 100
            return ie.quantize(Decimal('0.01'))
        except:
            return None
            
    def _calculate_consumo_acumulado(self, daily_feed, day):
        """Calculate accumulated feed consumption"""
        try:
            return (Decimal(daily_feed) * Decimal(day)).quantize(Decimal('0.01'))
        except:
            return None

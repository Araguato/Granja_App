from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from produccion.models import Granja, Galpon, Lote, SeguimientoDiario
from inventario.models import Raza, Alimento
from django.utils import timezone
from datetime import timedelta
import random

class Command(BaseCommand):
    help = 'Populate the database with sample data for testing'

    def handle(self, *args, **options):
        User = get_user_model()
        
        # Create a test user if it doesn't exist
        user, created = User.objects.get_or_create(
            username='testuser',
            defaults={
                'email': 'test@example.com',
                'first_name': 'Test',
                'last_name': 'User',
                'is_staff': True,
                'is_superuser': True
            }
        )
        if created:
            user.set_password('testpass123')
            user.save()
            self.stdout.write(self.style.SUCCESS('Created test user: testuser / testpass123'))
        
        # Create a sample farm
        granja, created = Granja.objects.get_or_create(
            codigo_granja='GRANJA-001',
            defaults={
                'nombre': 'Granja de Prueba',
                'direccion': 'Calle Falsa 123',
                'ubicacion_geografica': '10.12345, -66.98765',
                'telefono': '1234567890',
                'encargado': user,
                'capacidad_total_aves': 10000,
                'estado': 'ACTIVA',
                'empresa_id': 1  # Make sure this ID exists in the empresa table
            }
        )
        
        if created:
            self.stdout.write(self.style.SUCCESS(f'Created sample farm: {granja.nombre}'))
        
        # Create sample galpones
        for i in range(1, 4):
            galpon, created = Galpon.objects.get_or_create(
                granja=granja,
                numero_galpon=f'GALP-{i:03d}',
                defaults={
                    'tipo_galpon': 'PRODUCCION',
                    'capacidad_aves': 3000,
                    'area_metros_cuadrados': 1000,
                    'responsable': user
                }
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created sample galpon: {galpon.numero_galpon}'))
        
        # Get or create a sample raza
        raza, created = Raza.objects.get_or_create(
            nombre='Lohmann Brown',
            defaults={
                'descripcion': 'Raza de gallina ponedora marrón',
                'tipo_produccion': 'HUEVO',
                'edad_madura_semanas': 20,
                'peso_kg_adulto': 2.0,
                'color_huevo': 'MARRON'
            }
        )
        
        # Get or create sample alimento
        alimento, created = Alimento.objects.get_or_create(
            nombre='Alimento Inicial para Ponedoras',
            defaults={
                'tipo': 'INICIAL',
                'descripcion': 'Alimento balanceado para aves en etapa inicial',
                'proteina_porcentaje': 18.0,
                'energia_kcal_kg': 2800,
                'calcio_porcentaje': 1.0,
                'fosforo_porcentaje': 0.5
            }
        )
        
        # Create sample lotes
        galpones = Galpon.objects.all()
        for i, galpon in enumerate(galpones, 1):
            lote, created = Lote.objects.get_or_create(
                codigo_lote=f'LOTE-{i:03d}-2024',
                defaults={
                    'galpon': galpon,
                    'raza': raza,
                    'alimento': alimento,
                    'fecha_inicio': timezone.now().date() - timedelta(weeks=10),
                    'fecha_ingreso': timezone.now().date() - timedelta(weeks=10),
                    'cantidad_inicial_aves': 2500,
                    'edad_inicial_semanas': 1,
                    'edad_semanas': 10,
                    'estado': 'PRODUCCION'
                }
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created sample lote: {lote.codigo_lote}'))
                
                # Create sample seguimientos for the last 30 days
                for days_ago in range(30, 0, -1):
                    fecha = timezone.now().date() - timedelta(days=days_ago)
                    seguimiento = SeguimientoDiario.objects.create(
                        lote=lote,
                        fecha_seguimiento=fecha,
                        registrado_por=user,
                        tipo_seguimiento='PRODUCCION',
                        huevos_totales=random.randint(2000, 2400),
                        huevos_rotos=random.randint(0, 5),
                        huevos_sucios=random.randint(0, 3),
                        peso_promedio_ave=1.8 + (days_ago * 0.01),  # Slight daily increase
                        consumo_alimento_kg=round(random.uniform(180, 220), 2),
                        consumo_agua_litros=round(random.uniform(400, 500), 2),
                        temperatura_min=round(random.uniform(18, 22), 1),
                        temperatura_max=round(random.uniform(22, 26), 1),
                        humedad=round(random.uniform(50, 70), 1),
                        mortalidad=random.randint(0, 3),
                        causa_mortalidad='Natural' if random.random() > 0.7 else 'Enfermedad' if random.random() > 0.5 else 'Ataque',
                        observaciones='Seguimiento de prueba generado automáticamente.'
                    )
                    
                    # Create SeguimientoEngorde for some records
                    if random.random() > 0.7:  # 30% chance to have engorde data
                        from produccion.models import SeguimientoEngorde
                        SeguimientoEngorde.objects.create(
                            seguimiento_diario=seguimiento,
                            ganancia_diaria_peso=round(random.uniform(10, 30), 2),
                            conversion_alimenticia=round(random.uniform(1.6, 2.2), 2),
                            uniformidad=random.choice(['EXCELENTE', 'BUENA', 'REGULAR', 'DEFICIENTE']),
                            indice_productividad=round(random.uniform(300, 400), 2),
                            eficiencia_energetica=round(random.uniform(2.5, 3.5), 2),
                            eficiencia_proteica=round(random.uniform(0.4, 0.6), 2),
                            consumo_proteina=round(random.uniform(20, 30), 2),
                            consumo_energia=round(random.uniform(80, 120), 2),
                            relacion_energia_proteina=round(random.uniform(3.5, 4.5), 2),
                            longitud_corporal=round(random.uniform(30, 40), 1),
                            ancho_pechuga=round(random.uniform(10, 15), 1),
                            calidad_plumaje=random.randint(3, 5),
                            calidad_patas=random.randint(3, 5),
                            observaciones_engorde='Datos de engorde de prueba generados automáticamente.'
                        )
                
                self.stdout.write(self.style.SUCCESS(f'Added sample seguimientos for lote: {lote.codigo_lote}'))
        
        self.stdout.write(self.style.SUCCESS('Successfully populated database with sample data!'))

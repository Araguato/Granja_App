from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
import random
import decimal

from avicola.models import UserProfile
from inventario.models import Alimento
from produccion.models import Lote, SeguimientoDiario, SeguimientoEngorde

class Command(BaseCommand):
    help = 'Genera datos de ejemplo simplificados para probar las recomendaciones de alimentación'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Iniciando generación de datos simplificados...'))
        
        # Verificar que existan lotes
        lotes = Lote.objects.all()
        if lotes.count() == 0:
            self.stdout.write(self.style.ERROR('No hay lotes en la base de datos. Por favor, crea al menos un lote.'))
            return
        
        # Verificar que existan alimentos con datos nutricionales
        alimentos = Alimento.objects.filter(
            contenido_proteina__isnull=False,
            energia_metabolizable__isnull=False
        )
        
        if alimentos.count() == 0:
            self.stdout.write(self.style.ERROR('No hay alimentos con datos nutricionales.'))
            return
        
        # Obtener usuario para registrar seguimientos
        try:
            usuario = UserProfile.objects.first()
        except UserProfile.DoesNotExist:
            self.stdout.write(self.style.ERROR('No hay usuarios en la base de datos.'))
            return
        
        # Fecha actual
        fecha_actual = timezone.now().date()
        
        # Generar datos para cada lote
        for lote in lotes:
            self.stdout.write(f'Generando datos para el lote {lote.codigo_lote}...')
            
            # Asignar un alimento al lote si no tiene
            if not lote.alimento:
                lote.alimento = alimentos.first()
                lote.save()
                self.stdout.write(f'  Asignado alimento {lote.alimento.nombre} al lote')
            
            # Generar 10 días de seguimiento
            for i in range(1, 11):
                fecha_seguimiento = fecha_actual - timedelta(days=10-i)
                
                # Verificar si ya existe un seguimiento para esta fecha
                if SeguimientoDiario.objects.filter(lote=lote, fecha_seguimiento=fecha_seguimiento).exists():
                    self.stdout.write(f'  Ya existe seguimiento para el día {fecha_seguimiento}, saltando...')
                    continue
                
                # Valores simulados
                peso_promedio = decimal.Decimal(str(round(0.5 + (i * 0.1), 2)))  # Aumenta 100g por día
                consumo_alimento = decimal.Decimal(str(round(10 + (i * 0.5), 2)))  # kg para todo el lote
                mortalidad = random.randint(0, 3)
                
                # Crear seguimiento diario
                seguimiento_diario = SeguimientoDiario.objects.create(
                    lote=lote,
                    fecha_seguimiento=fecha_seguimiento,
                    tipo_seguimiento='ENGORDE',
                    peso_promedio_ave=peso_promedio,
                    consumo_alimento_kg=consumo_alimento,
                    consumo_agua_litros=consumo_alimento * 2,
                    mortalidad=mortalidad,
                    temperatura_min=decimal.Decimal('20.0'),
                    temperatura_max=decimal.Decimal('30.0'),
                    humedad=decimal.Decimal('60.0'),
                    observaciones=f'Seguimiento día {i}',
                    registrado_por=usuario
                )
                
                # Valores para seguimiento de engorde
                ganancia_diaria = decimal.Decimal('50.0') + (decimal.Decimal(str(i)) * decimal.Decimal('5.0'))  # g/día
                conversion = decimal.Decimal('1.8') - (decimal.Decimal(str(i)) * decimal.Decimal('0.02'))  # Mejora con el tiempo
                
                # Calcular eficiencias de forma segura
                alimento_actual = lote.alimento
                
                # Convertir a decimal para asegurar compatibilidad
                energia = alimento_actual.energia_metabolizable or decimal.Decimal('3000.0')
                proteina = alimento_actual.contenido_proteina or decimal.Decimal('20.0')
                
                # Calcular valores con límites seguros
                consumo_energia_val = consumo_alimento * energia
                consumo_energia = min(consumo_energia_val, decimal.Decimal('9999.99'))  # Limitar a max_digits=8
                
                consumo_proteina_val = consumo_alimento * proteina * decimal.Decimal('10.0')
                consumo_proteina = min(consumo_proteina_val, decimal.Decimal('999.99'))  # Limitar a max_digits=6
                
                # Valores de eficiencia con límites seguros
                base_eficiencia_e = decimal.Decimal('3.0') - (decimal.Decimal(str(i)) * decimal.Decimal('0.05'))
                eficiencia_energetica = min(base_eficiencia_e, decimal.Decimal('99.99'))  # Limitar a max_digits=6
                
                base_eficiencia_p = decimal.Decimal('0.45') - (decimal.Decimal(str(i)) * decimal.Decimal('0.01'))
                eficiencia_proteica = min(base_eficiencia_p, decimal.Decimal('9.99'))  # Limitar a max_digits=6
                
                relacion_energia_proteina = decimal.Decimal('150.0')
                
                # Crear seguimiento de engorde
                SeguimientoEngorde.objects.create(
                    seguimiento_diario=seguimiento_diario,
                    ganancia_diaria_peso=ganancia_diaria,
                    conversion_alimenticia=conversion,
                    uniformidad='BUENA',
                    consumo_energia=consumo_energia,
                    consumo_proteina=consumo_proteina,
                    eficiencia_energetica=eficiencia_energetica,
                    eficiencia_proteica=eficiencia_proteica,
                    relacion_energia_proteina=relacion_energia_proteina
                )
                
                self.stdout.write(f'  Creado seguimiento para el día {fecha_seguimiento}')
        
        self.stdout.write(self.style.SUCCESS('¡Generación de datos simplificados completada con éxito!'))

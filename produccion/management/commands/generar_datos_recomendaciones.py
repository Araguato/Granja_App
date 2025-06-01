from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
import random

from avicola.models import UserProfile
from inventario.models import Alimento
from produccion.models import Lote, SeguimientoDiario, SeguimientoEngorde

class Command(BaseCommand):
    help = 'Genera datos de ejemplo específicos para probar las recomendaciones de alimentación'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Iniciando generación de datos para recomendaciones...'))
        
        # Verificar que existan lotes
        if Lote.objects.count() == 0:
            self.stdout.write(self.style.ERROR('No hay lotes en la base de datos. Por favor, crea al menos un lote antes de ejecutar este comando.'))
            return
        
        # Verificar que existan alimentos con datos nutricionales
        alimentos_validos = Alimento.objects.filter(
            contenido_proteina__isnull=False,
            energia_metabolizable__isnull=False
        )
        
        if alimentos_validos.count() == 0:
            self.stdout.write(self.style.ERROR('No hay alimentos con datos nutricionales. Por favor, actualiza los alimentos con valores de proteína y energía.'))
            return
        
        # Obtener usuario para registrar seguimientos
        try:
            usuario = UserProfile.objects.first()
        except UserProfile.DoesNotExist:
            self.stdout.write(self.style.ERROR('No hay usuarios en la base de datos. Por favor, crea al menos un usuario.'))
            return
        
        # Generar datos de seguimiento para cada lote
        lotes = Lote.objects.all()
        fecha_actual = timezone.now().date()
        
        for lote in lotes:
            self.stdout.write(f'Generando datos para el lote {lote.codigo_lote}...')
            
            # Asignar un alimento al lote si no tiene
            if not lote.alimento:
                lote.alimento = alimentos_validos.order_by('?').first()
                lote.save()
                self.stdout.write(f'  Asignado alimento {lote.alimento.nombre} al lote')
            
            # Determinar cuántos días de seguimiento generar (últimos 30 días)
            dias_seguimiento = min(30, (fecha_actual - lote.fecha_ingreso).days)
            
            if dias_seguimiento <= 0:
                self.stdout.write(f'  El lote {lote.codigo_lote} es muy reciente, no se generarán datos')
                continue
            
            # Generar seguimientos diarios
            for dia in range(1, dias_seguimiento + 1):
                fecha_seguimiento = fecha_actual - timedelta(days=dias_seguimiento - dia)
                
                # Verificar si ya existe un seguimiento para esta fecha
                if SeguimientoDiario.objects.filter(lote=lote, fecha_seguimiento=fecha_seguimiento).exists():
                    self.stdout.write(f'  Ya existe seguimiento para el día {fecha_seguimiento}, saltando...')
                    continue
                
                # Calcular peso promedio basado en la edad (simulación simple de crecimiento)
                edad_dias = dia + (lote.edad_semanas * 7) - dias_seguimiento
                
                if edad_dias <= 0:
                    continue
                
                if lote.raza.tipo_raza == 'ENGORDE':
                    peso_base = 42  # Peso inicial en gramos
                    ganancia_diaria = random.uniform(50, 60)  # Ganancia diaria promedio en gramos
                else:  # Ponedora u otro
                    peso_base = 40
                    ganancia_diaria = random.uniform(45, 55)
                
                peso_promedio = peso_base + (ganancia_diaria * edad_dias)
                
                # Calcular consumo de alimento (aumenta con la edad)
                consumo_por_ave = 0.03 + (0.005 * edad_dias)  # kg por ave
                consumo_total = consumo_por_ave * (lote.cantidad_inicial_aves - random.randint(0, int(lote.cantidad_inicial_aves * 0.02)))
                
                # Calcular mortalidad (pequeña y aleatoria)
                mortalidad = random.randint(0, 5)
                
                # Temperatura y humedad
                temp_min = random.uniform(18, 22)
                temp_max = random.uniform(28, 32)
                humedad = random.uniform(50, 70)
                
                # Crear seguimiento diario
                seguimiento_diario = SeguimientoDiario.objects.create(
                    lote=lote,
                    fecha_seguimiento=fecha_seguimiento,
                    tipo_seguimiento='ENGORDE',
                    peso_promedio_ave=peso_promedio,
                    consumo_alimento_kg=consumo_total,
                    consumo_agua_litros=consumo_total * 2,
                    mortalidad=mortalidad,
                    temperatura_min=temp_min,
                    temperatura_max=temp_max,
                    humedad=humedad,
                    observaciones=f'Seguimiento día {dia}',
                    registrado_por=usuario
                )
                
                # Calcular datos de engorde
                if dia > 1:
                    # Obtener seguimiento anterior para calcular ganancia
                    try:
                        seguimiento_anterior = SeguimientoDiario.objects.get(
                            lote=lote,
                            fecha_seguimiento=fecha_seguimiento - timedelta(days=1)
                        )
                        peso_anterior = seguimiento_anterior.peso_promedio_ave
                        ganancia = peso_promedio - peso_anterior
                    except SeguimientoDiario.DoesNotExist:
                        ganancia = ganancia_diaria
                else:
                    ganancia = ganancia_diaria
                
                # Calcular conversión alimenticia
                conversion = (consumo_total * 1000) / (ganancia * (lote.cantidad_inicial_aves - mortalidad)) if ganancia > 0 else 0
                
                # Obtener valores nutricionales del alimento
                alimento_actual = lote.alimento
                if alimento_actual:
                    energia = alimento_actual.energia_metabolizable
                    proteina = alimento_actual.contenido_proteina
                    
                    # Calcular consumo de energía y proteína
                    consumo_energia = consumo_total * energia
                    consumo_proteina = consumo_total * proteina * 10  # Convertir % a g/kg
                    
                    # Calcular eficiencias
                    eficiencia_energetica = consumo_energia / ganancia if ganancia > 0 else 0
                    eficiencia_proteica = consumo_proteina / ganancia if ganancia > 0 else 0
                    relacion_energia_proteina = consumo_energia / consumo_proteina if consumo_proteina > 0 else 0
                    
                    # Añadir algo de variabilidad a las eficiencias
                    eficiencia_energetica *= random.uniform(0.9, 1.1)
                    eficiencia_proteica *= random.uniform(0.9, 1.1)
                    relacion_energia_proteina *= random.uniform(0.95, 1.05)
                else:
                    consumo_energia = 0
                    consumo_proteina = 0
                    eficiencia_energetica = 0
                    eficiencia_proteica = 0
                    relacion_energia_proteina = 0
                
                # Crear seguimiento de engorde
                SeguimientoEngorde.objects.create(
                    seguimiento_diario=seguimiento_diario,
                    ganancia_diaria_peso=ganancia,
                    conversion_alimenticia=conversion,
                    consumo_energia=consumo_energia,
                    consumo_proteina=consumo_proteina,
                    eficiencia_energetica=eficiencia_energetica,
                    eficiencia_proteica=eficiencia_proteica,
                    relacion_energia_proteina=relacion_energia_proteina
                )
                
                self.stdout.write(f'  Creado seguimiento para el día {fecha_seguimiento}')
        
        self.stdout.write(self.style.SUCCESS('¡Generación de datos para recomendaciones completada con éxito!'))

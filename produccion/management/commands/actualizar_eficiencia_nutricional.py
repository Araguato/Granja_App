from django.core.management.base import BaseCommand
from produccion.models import SeguimientoEngorde
from django.db.models import F
from django.utils import timezone
import logging

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Actualiza los valores de eficiencia energética y proteica en todos los registros de SeguimientoEngorde'

    def add_arguments(self, parser):
        parser.add_argument(
            '--dias',
            type=int,
            default=None,
            help='Actualizar solo registros de los últimos N días (opcional)',
        )

    def handle(self, *args, **options):
        dias = options['dias']
        
        # Filtrar registros según los días especificados
        queryset = SeguimientoEngorde.objects.all().select_related(
            'seguimiento_diario', 
            'seguimiento_diario__lote', 
            'seguimiento_diario__lote__alimento'
        )
        
        if dias:
            fecha_limite = timezone.now().date() - timezone.timedelta(days=dias)
            queryset = queryset.filter(seguimiento_diario__fecha_seguimiento__gte=fecha_limite)
            self.stdout.write(f"Actualizando registros desde {fecha_limite}")
        else:
            self.stdout.write("Actualizando todos los registros")
        
        total = queryset.count()
        actualizados = 0
        errores = 0
        
        self.stdout.write(f"Total de registros a procesar: {total}")
        
        # Procesar cada registro
        for seguimiento in queryset:
            try:
                # Verificar si el lote tiene alimento asignado
                lote = seguimiento.seguimiento_diario.lote
                alimento = lote.alimento
                
                if not alimento:
                    self.stdout.write(self.style.WARNING(
                        f"El lote {lote.codigo_lote} no tiene alimento asignado. Omitiendo registro ID {seguimiento.id}"
                    ))
                    continue
                
                # Verificar si el alimento tiene datos nutricionales
                if not hasattr(alimento, 'energia_metabolizable') or not alimento.energia_metabolizable:
                    self.stdout.write(self.style.WARNING(
                        f"El alimento {alimento.nombre} no tiene valor de energía metabolizable. Omitiendo registro ID {seguimiento.id}"
                    ))
                    continue
                
                if not hasattr(alimento, 'contenido_proteina') or not alimento.contenido_proteina:
                    self.stdout.write(self.style.WARNING(
                        f"El alimento {alimento.nombre} no tiene valor de contenido proteico. Omitiendo registro ID {seguimiento.id}"
                    ))
                    continue
                
                # Verificar si hay consumo de alimento registrado
                consumo_kg = seguimiento.seguimiento_diario.consumo_alimento_kg
                if not consumo_kg or consumo_kg <= 0:
                    self.stdout.write(self.style.WARNING(
                        f"No hay consumo de alimento registrado para el seguimiento ID {seguimiento.id}. Omitiendo registro."
                    ))
                    continue
                
                # Verificar si hay ganancia diaria de peso registrada
                ganancia_diaria = seguimiento.ganancia_diaria_peso
                if not ganancia_diaria or ganancia_diaria <= 0:
                    self.stdout.write(self.style.WARNING(
                        f"No hay ganancia diaria registrada para el seguimiento ID {seguimiento.id}. Omitiendo registro."
                    ))
                    continue
                
                # Calcular consumo de energía (kcal)
                consumo_energia = consumo_kg * alimento.energia_metabolizable
                
                # Calcular consumo de proteína (g)
                consumo_proteina = consumo_kg * alimento.contenido_proteina * 10  # Convertir % a g/kg
                
                # Calcular eficiencia energética (kcal/g)
                eficiencia_energetica = consumo_energia / ganancia_diaria if ganancia_diaria > 0 else 0
                
                # Calcular eficiencia proteica (g/g)
                eficiencia_proteica = consumo_proteina / ganancia_diaria if ganancia_diaria > 0 else 0
                
                # Calcular relación energía/proteína
                relacion_energia_proteina = consumo_energia / consumo_proteina if consumo_proteina > 0 else 0
                
                # Actualizar el registro
                seguimiento.consumo_energia = consumo_energia
                seguimiento.consumo_proteina = consumo_proteina
                seguimiento.eficiencia_energetica = eficiencia_energetica
                seguimiento.eficiencia_proteica = eficiencia_proteica
                seguimiento.relacion_energia_proteina = relacion_energia_proteina
                seguimiento.save()
                
                actualizados += 1
                
                if actualizados % 50 == 0:
                    self.stdout.write(f"Procesados {actualizados} de {total} registros...")
                
            except Exception as e:
                errores += 1
                logger.error(f"Error al procesar seguimiento ID {seguimiento.id}: {str(e)}")
                self.stdout.write(self.style.ERROR(f"Error al procesar seguimiento ID {seguimiento.id}: {str(e)}"))
        
        self.stdout.write(self.style.SUCCESS(
            f"Proceso completado. Registros actualizados: {actualizados}. Errores: {errores}."
        ))

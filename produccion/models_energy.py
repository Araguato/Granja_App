from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model

# Using string reference to avoid circular imports
# Galpon model will be referenced as 'produccion.Galpon'

class ConsumoEnergia(models.Model):
    """Modelo para registrar el consumo de energía de los galpones"""
    galpon = models.ForeignKey(
        'produccion.Galpon',  # Using app_label.ModelName string reference
        on_delete=models.CASCADE,
        related_name='consumos_energia',
        verbose_name="Galpón"
    )
    fecha_registro = models.DateTimeField(
        default=timezone.now,
        verbose_name="Fecha de Registro"
    )
    consumo_kwh = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Consumo (kWh)"
    )
    costo_por_kwh = models.DecimalField(
        max_digits=6,
        decimal_places=4,
        default=0.15,
        verbose_name="Costo por kWh (USD)"
    )
    temperatura_externa = models.DecimalField(
        max_digits=4,
        decimal_places=1,
        null=True,
        blank=True,
        verbose_name="Temperatura Externa (°C)"
    )
    humedad_relativa = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
        verbose_name="Humedad Relativa (%)"
    )
    horas_funcionamiento = models.DecimalField(
        max_digits=4,
        decimal_places=1,
        default=24,
        verbose_name="Horas de Funcionamiento"
    )
    registrado_por = models.ForeignKey(
        get_user_model(),
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Registrado por"
    )
    observaciones = models.TextField(
        blank=True,
        verbose_name="Observaciones"
    )

    class Meta:
        verbose_name = "Consumo de Energía"
        verbose_name_plural = "Consumos de Energía"
        ordering = ['-fecha_registro']
        indexes = [
            models.Index(fields=['fecha_registro']),
            models.Index(fields=['galpon']),
        ]

    def __str__(self):
        return f"{self.galpon} - {self.fecha_registro.strftime('%Y-%m-%d %H:%M')} - {self.consumo_kwh} kWh"

    @property
    def costo_total(self):
        return self.consumo_kwh * self.costo_por_kwh

    @classmethod
    def get_estadisticas_energia(cls, galpon_id=None):
        """Obtiene estadísticas de energía para el dashboard"""
        from django.db.models import Sum, Avg, F, ExpressionWrapper, FloatField
        from django.db.models.functions import TruncDay, TruncMonth
        
        hoy = timezone.now().date()
        inicio_mes = hoy.replace(day=1)
        
        # Consumo del día actual
        consumo_hoy = cls.objects.filter(
            fecha_registro__date=hoy
        )
        if galpon_id:
            consumo_hoy = consumo_hoy.filter(galpon_id=galpon_id)
        
        consumo_hoy = consumo_hoy.aggregate(
            total=Sum('consumo_kwh'),
            costo=Sum(ExpressionWrapper(F('consumo_kwh') * F('costo_por_kwh'), output_field=FloatField()))
        )
        
        # Consumo del mes actual
        consumo_mes = cls.objects.filter(
            fecha_registro__date__gte=inicio_mes,
            fecha_registro__date__lte=hoy
        )
        if galpon_id:
            consumo_mes = consumo_mes.filter(galpon_id=galpon_id)
            
        consumo_mes = consumo_mes.aggregate(
            total=Sum('consumo_kwh'),
            costo=Sum(ExpressionWrapper(F('consumo_kwh') * F('costo_por_kwh'), output_field=FloatField()))
        )
        
        # Promedio de consumo diario del mes
        dias_mes = hoy.day
        promedio_diario = consumo_mes['total'] / dias_mes if consumo_mes['total'] and dias_mes > 0 else 0
        
        # Consumo por día (últimos 7 días)
        fecha_inicio = hoy - timezone.timedelta(days=6)
        consumos_por_dia = cls.objects.filter(
            fecha_registro__date__gte=fecha_inicio,
            fecha_registro__date__lte=hoy
        )
        if galpon_id:
            consumos_por_dia = consumos_por_dia.filter(galpon_id=galpon_id)
            
        consumos_por_dia = consumos_por_dia.annotate(
            fecha=TruncDay('fecha_registro')
        ).values('fecha').annotate(
            consumo_total=Sum('consumo_kwh'),
            costo_total=Sum(ExpressionWrapper(F('consumo_kwh') * F('costo_por_kwh'), output_field=FloatField()))
        ).order_by('fecha')
        
        # Consumo por galpón (solo si no se filtró por galpón)
        consumo_por_galpon = None
        if not galpon_id:
            consumo_por_galpon = cls.objects.filter(
                fecha_registro__date__gte=inicio_mes,
                fecha_registro__date__lte=hoy
            ).values('galpon__numero_galpon').annotate(
                consumo_total=Sum('consumo_kwh'),
                costo_total=Sum(ExpressionWrapper(F('consumo_kwh') * F('costo_por_kwh'), output_field=FloatField()))
            ).order_by('galpon__numero_galpon')
        
        return {
            'hoy': {
                'consumo': consumo_hoy['total'] or 0,
                'costo': consumo_hoy['costo'] or 0,
                'fecha': hoy.strftime('%Y-%m-%d')
            },
            'mes': {
                'consumo': consumo_mes['total'] or 0,
                'costo': consumo_mes['costo'] or 0,
                'promedio_diario': promedio_diario,
                'dias': dias_mes
            },
            'consumos_por_dia': list(consumos_por_dia),
            'consumo_por_galpon': list(consumo_por_galpon) if consumo_por_galpon else None
        }

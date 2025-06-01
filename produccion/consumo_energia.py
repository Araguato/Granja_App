from django.db import models
from django.conf import settings

class ConsumoEnergia(models.Model):
    """
    Modelo para registrar el consumo de energía de los galpones.
    """
    galpon = models.ForeignKey(
        'produccion.Galpon',  # Using string reference to avoid circular import
        on_delete=models.CASCADE,
        related_name='consumos_energia',
        verbose_name="Galpón"
    )
    fecha_registro = models.DateField(verbose_name="Fecha de Registro")
    hora_inicio = models.TimeField(verbose_name="Hora de Inicio")
    hora_fin = models.TimeField(verbose_name="Hora de Fin")
    consumo_kwh = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Consumo (kWh)"
    )
    temperatura_ambiente = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name="Temperatura Ambiente (°C)"
    )
    humedad_relativa = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name="Humedad Relativa (%)"
    )
    observaciones = models.TextField(blank=True, verbose_name="Observaciones")
    registrado_por = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Registrado por"
    )
    fecha_creacion = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Creación")
    fecha_actualizacion = models.DateTimeField(auto_now=True, verbose_name="Última Actualización")

    class Meta:
        verbose_name = "Consumo de Energía"
        verbose_name_plural = "Consumos de Energía"
        ordering = ['-fecha_registro', 'galpon']
        unique_together = ['galpon', 'fecha_registro', 'hora_inicio', 'hora_fin']

    def __str__(self):
        return f"{self.galpon} - {self.fecha_registro} ({self.hora_inicio} - {self.hora_fin}): {self.consumo_kwh} kWh"

    @property
    def duracion_horas(self):
        """Calcula la duración en horas entre hora_inicio y hora_fin"""
        from datetime import datetime, date
        
        if not all([self.hora_inicio, self.hora_fin]):
            return 0
            
        # Crear objetos datetime para hoy con las horas correspondientes
        hoy = date.today()
        inicio = datetime.combine(hoy, self.hora_inicio)
        fin = datetime.combine(hoy, self.hora_fin)
        
        # Si la hora de fin es menor que la de inicio, asumir que es al día siguiente
        if fin <= inicio:
            fin = datetime.combine(hoy.replace(day=hoy.day + 1), self.hora_fin)
        
        # Calcular diferencia en horas
        diferencia = fin - inicio
        return round(diferencia.total_seconds() / 3600, 2)

    @property
    def consumo_promedio_kw(self):
        """Calcula el consumo promedio en kW"""
        horas = self.duracion_horas
        if horas <= 0:
            return 0
        return round(float(self.consumo_kwh) / horas, 2)

from django.db import models
from django.conf import settings  # Para AUTH_USER_MODEL
from django.core.validators import MinValueValidator

# ... (keep all other model classes the same until ConsumoAlimento)

class ConsumoAlimento(models.Model):
    """Registro de consumo de alimento por lote"""
    alimento = models.ForeignKey('Alimento', on_delete=models.PROTECT, related_name='consumos', verbose_name="Alimento")
    lote_aves = models.ForeignKey('produccion.Lote', on_delete=models.CASCADE, related_name='consumos_alimento', verbose_name="Lote de Aves")
    cantidad_kg = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Cantidad (kg)")
    fecha_consumo = models.DateField(verbose_name="Fecha de Consumo")
    registrado_por = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, verbose_name="Registrado por")
    fecha_registro = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Registro")
    observaciones = models.TextField(blank=True, verbose_name="Observaciones")

    class Meta:
        verbose_name = "Consumo de Alimento"
        verbose_name_plural = "Consumos de Alimento"
        ordering = ['-fecha_consumo', '-fecha_registro']

    def __str__(self):
        return f"{self.cantidad_kg}kg de {self.alimento} - {self.lote_aves} - {self.fecha_consumo}"

class AplicacionVacuna(models.Model):
    """Registro de aplicación de vacunas a lotes"""
    vacuna = models.ForeignKey('Vacuna', on_delete=models.PROTECT, related_name='aplicaciones', verbose_name="Vacuna")
    lote_aves = models.ForeignKey('produccion.Lote', on_delete=models.CASCADE, related_name='aplicaciones_vacuna', verbose_name="Lote de Aves")
    fecha_aplicacion = models.DateField(verbose_name="Fecha de Aplicación")
    dosis_ml = models.DecimalField(max_digits=6, decimal_places=2, verbose_name="Dosis Aplicada (ml)")
    aplicada_por = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, verbose_name="Aplicada por")
    fecha_registro = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Registro")
    observaciones = models.TextField(blank=True, verbose_name="Observaciones")
    lote_vacuna = models.CharField(max_length=50, blank=True, verbose_name="Lote de la Vacuna")
    proxima_aplicacion = models.DateField(null=True, blank=True, verbose_name="Próxima Aplicación")
    edad_aplicacion_semanas = models.PositiveIntegerField(null=True, blank=True, verbose_name="Edad en Aplicación (semanas)")
    via_aplicacion = models.CharField(max_length=50, blank=True, verbose_name="Vía de Aplicación")
    
    class Meta:
        verbose_name = "Aplicación de Vacuna"
        verbose_name_plural = "Aplicaciones de Vacuna"
        ordering = ['-fecha_aplicacion', '-fecha_registro']

    def __str__(self):
        return f"{self.vacuna} - {self.lote_aves} - {self.fecha_aplicacion}"

# ... (keep all other model classes the same after AplicacionVacuna)

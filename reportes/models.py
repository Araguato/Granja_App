from django.db import models
from django.conf import settings
from django.utils import timezone

class ReporteGenerado(models.Model):
    TIPO_REPORTE_CHOICES = [
        ('PRODUCCION_DIARIA', 'Producción Diaria'),
        ('PRODUCCION_SEMANAL', 'Producción Semanal'),
        ('PRODUCCION_MENSUAL', 'Producción Mensual'),
        ('MORTALIDAD', 'Mortalidad'),
        ('INVENTARIO', 'Inventario'),
        ('VENTAS', 'Ventas'),
        ('COSTOS', 'Costos'),
        ('RENDIMIENTO', 'Rendimiento'),
        ('PERSONALIZADO', 'Personalizado'),
    ]
    
    FORMATO_CHOICES = [
        ('PDF', 'PDF'),
        ('EXCEL', 'Excel'),
        ('CSV', 'CSV'),
    ]
    
    titulo = models.CharField(max_length=200, verbose_name="Título del Reporte")
    tipo_reporte = models.CharField(max_length=50, choices=TIPO_REPORTE_CHOICES, verbose_name="Tipo de Reporte")
    fecha_inicio = models.DateField(verbose_name="Fecha de Inicio")
    fecha_fin = models.DateField(verbose_name="Fecha de Fin")
    formato = models.CharField(max_length=10, choices=FORMATO_CHOICES, default='PDF', verbose_name="Formato")
    usuario_generador = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='reportes_generados', verbose_name="Usuario que generó")
    fecha_generacion = models.DateTimeField(default=timezone.now, verbose_name="Fecha de Generación")
    archivo = models.FileField(upload_to='reportes/', null=True, blank=True, verbose_name="Archivo Generado")
    parametros = models.JSONField(default=dict, blank=True, verbose_name="Parámetros del Reporte")
    
    class Meta:
        verbose_name = "Reporte Generado"
        verbose_name_plural = "Reportes Generados"
        ordering = ['-fecha_generacion']
    
    def __str__(self):
        return f"{self.titulo} ({self.get_tipo_reporte_display()}) - {self.fecha_generacion.strftime('%d/%m/%Y %H:%M')}"

class PlantillaReporte(models.Model):
    nombre = models.CharField(max_length=100, verbose_name="Nombre de la Plantilla")
    descripcion = models.TextField(blank=True, verbose_name="Descripción")
    tipo_reporte = models.CharField(max_length=50, choices=ReporteGenerado.TIPO_REPORTE_CHOICES, verbose_name="Tipo de Reporte")
    configuracion = models.JSONField(default=dict, verbose_name="Configuración de la Plantilla")
    usuario_creador = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='plantillas_reporte', verbose_name="Creado por")
    fecha_creacion = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Creación")
    fecha_modificacion = models.DateTimeField(auto_now=True, verbose_name="Última Modificación")
    es_predeterminada = models.BooleanField(default=False, verbose_name="Es Plantilla Predeterminada")
    
    class Meta:
        verbose_name = "Plantilla de Reporte"
        verbose_name_plural = "Plantillas de Reportes"
        ordering = ['nombre']
        unique_together = ['nombre', 'usuario_creador']
    
    def __str__(self):
        return f"{self.nombre} ({self.get_tipo_reporte_display()})"

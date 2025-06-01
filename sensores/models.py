from django.db import models
from django.conf import settings
from produccion.models import Galpon
from django.utils import timezone

class TipoSensor(models.Model):
    """Modelo para los diferentes tipos de sensores disponibles."""
    nombre = models.CharField(max_length=50, unique=True)
    codigo = models.SlugField(max_length=50, unique=True)
    descripcion = models.TextField(blank=True)
    unidad_medida = models.CharField(max_length=20, help_text="Ej: °C, %, ppm, etc.")
    rango_min = models.FloatField(help_text="Valor mínimo que puede medir el sensor")
    rango_max = models.FloatField(help_text="Valor máximo que puede medir el sensor")
    icono = models.CharField(max_length=50, default='fa-thermometer-half', 
                           help_text="Clase de icono de FontAwesome")
    color = models.CharField(max_length=20, default='#4e73df', 
                           help_text="Código de color en hexadecimal")
    activo = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Tipo de Sensor"
        verbose_name_plural = "Tipos de Sensores"
        ordering = ['nombre']

    def __str__(self):
        return f"{self.nombre} ({self.unidad_medida})"


class Sensor(models.Model):
    """Modelo para los sensores físicos instalados en los galpones."""
    ESTADOS = (
        ('ACTIVO', 'Activo'),
        ('MANTENIMIENTO', 'En Mantenimiento'),
        ('INACTIVO', 'Inactivo'),
        ('FALLA', 'En Falla'),
    )
    
    codigo = models.CharField(max_length=50, unique=True)
    nombre = models.CharField(max_length=100)
    tipo = models.ForeignKey(TipoSensor, on_delete=models.PROTECT, related_name='sensores')
    galpon = models.ForeignKey(Galpon, on_delete=models.CASCADE, related_name='sensores', 
                             null=True, blank=True)
    ubicacion = models.CharField(max_length=100, help_text="Ubicación física dentro del galpón")
    estado = models.CharField(max_length=20, choices=ESTADOS, default='ACTIVO')
    fecha_instalacion = models.DateField(default=timezone.now)
    ultima_calibracion = models.DateField(null=True, blank=True)
    activo = models.BooleanField(default=True)
    observaciones = models.TextField(blank=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Sensor"
        verbose_name_plural = "Sensores"
        ordering = ['galpon', 'tipo__nombre']

    def __str__(self):
        ubic = f" en {self.ubicacion}" if self.ubicacion else ""
        galpon = f"{self.galpon}" if self.galpon else "Sin asignar"
        return f"{self.tipo.nombre}{ubic} - {galpon}"


class LecturaSensor(models.Model):
    """Modelo para almacenar las lecturas de los sensores."""
    sensor = models.ForeignKey(Sensor, on_delete=models.CASCADE, related_name='lecturas')
    valor = models.FloatField()
    fecha_hora = models.DateTimeField(default=timezone.now)
    fecha_hora_lectura = models.DateTimeField(help_text="Fecha y hora real de la lectura del sensor")
    estado_sensor = models.CharField(max_length=20, default='OK', 
                                   help_text="Estado del sensor al momento de la lectura")
    latitud = models.FloatField(null=True, blank=True, 
                              help_text="Coordenada de latitud (opcional)")
    longitud = models.FloatField(null=True, blank=True, 
                               help_text="Coordenada de longitud (opcional)")
    bateria = models.FloatField(null=True, blank=True, 
                              help_text="Nivel de batería en porcentaje")
    senal = models.IntegerField(null=True, blank=True, 
                              help_text="Intensidad de la señal en dBm")
    metadata = models.JSONField(default=dict, blank=True, 
                              help_text="Metadatos adicionales en formato JSON")

    class Meta:
        verbose_name = "Lectura de Sensor"
        verbose_name_plural = "Lecturas de Sensores"
        ordering = ['-fecha_hora_lectura']
        indexes = [
            models.Index(fields=['sensor', '-fecha_hora_lectura']),
            models.Index(fields=['-fecha_hora_lectura']),
        ]

    def __str__(self):
        return f"{self.sensor}: {self.valor} {self.sensor.tipo.unidad_medida} @ {self.fecha_hora_lectura}"

    def save(self, *args, **kwargs):
        # Si no se especifica fecha_hora_lectura, usar la fecha/hora actual
        if not self.fecha_hora_lectura:
            self.fecha_hora_lectura = timezone.now()
        super().save(*args, **kwargs)


class AlertaSensor(models.Model):
    """Modelo para alertas generadas por lecturas de sensores."""
    TIPOS_ALERTA = (
        ('CRITICA', 'Crítica'),
        ('ALTA', 'Alta'),
        ('MEDIA', 'Media'),
        ('BAJA', 'Baja'),
        ('INFORMATIVA', 'Informativa'),
    )
    
    ESTADOS = (
        ('PENDIENTE', 'Pendiente'),
        ('EN_PROCESO', 'En Proceso'),
        ('RESUELTA', 'Resuelta'),
        ('DESCARTADA', 'Descartada'),
    )
    
    lectura = models.ForeignKey(LecturaSensor, on_delete=models.CASCADE, related_name='alertas')
    tipo = models.CharField(max_length=20, choices=TIPOS_ALERTA)
    mensaje = models.TextField()
    estado = models.CharField(max_length=20, choices=ESTADOS, default='PENDIENTE')
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    resuelta_por = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, 
                                   null=True, blank=True, related_name='alertas_resueltas')
    comentarios = models.TextField(blank=True)

    class Meta:
        verbose_name = "Alerta de Sensor"
        verbose_name_plural = "Alertas de Sensores"
        ordering = ['-fecha_creacion']
        indexes = [
            models.Index(fields=['estado', 'tipo']),
            models.Index(fields=['-fecha_creacion']),
        ]

    def __str__(self):
        return f"[{self.get_tipo_display()}] {self.mensaje[:50]}..."

    def marcar_como_resuelta(self, usuario, comentarios=''):
        self.estado = 'RESUELTA'
        self.resuelta_por = usuario
        self.comentarios = comentarios
        self.save(update_fields=['estado', 'resuelta_por', 'comentarios', 'fecha_actualizacion'])

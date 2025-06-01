from django.db import models
from django.conf import settings

class Galpon(models.Model):
    """Modelo para representar un galpón en la granja avícola"""
    
    # Opciones para el estado del galpón
    ESTADO_CHOICES = [
        ('activo', 'Activo'),
        ('inactivo', 'Inactivo'),
        ('mantenimiento', 'En Mantenimiento'),
        ('limpieza', 'En Limpieza'),
    ]
    
    # Opciones para el tipo de galpón
    TIPO_CHOICES = [
        ('crianza', 'Crianza'),
        ('postura', 'Postura'),
        ('engorde', 'Engorde'),
        ('recria', 'Recría'),
    ]
    
    numero = models.CharField(max_length=20, unique=True, verbose_name='Número de Galpón')
    nombre = models.CharField(max_length=100, verbose_name='Nombre del Galpón')
    capacidad = models.PositiveIntegerField(verbose_name='Capacidad (aves)')
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES, verbose_name='Tipo de Galpón')
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='activo', verbose_name='Estado')
    ubicacion = models.CharField(max_length=200, blank=True, null=True, verbose_name='Ubicación')
    fecha_creacion = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de Creación')
    fecha_actualizacion = models.DateTimeField(auto_now=True, verbose_name='Última Actualización')
    observaciones = models.TextField(blank=True, null=True, verbose_name='Observaciones')
    
    # Relaciones
    empresa = models.ForeignKey(
        'avicola.Empresa', 
        on_delete=models.CASCADE, 
        related_name='galpones',
        verbose_name='Empresa'
    )
    
    responsable = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='galpones_a_cargo',
        verbose_name='Responsable'
    )
    
    class Meta:
        verbose_name = 'Galpón'
        verbose_name_plural = 'Galpones'
        ordering = ['numero']
    
    def __str__(self):
        return f"Galpón {self.numero} - {self.nombre}"
    
    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('galpones:detalle', kwargs={'pk': self.pk})

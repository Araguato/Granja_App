from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
import os
import datetime


class Backup(models.Model):
    """Modelo para almacenar información sobre los respaldos realizados"""
    BACKUP_TYPES = [
        ('FULL', 'Respaldo Completo'),
        ('DB', 'Base de Datos'),
        ('MEDIA', 'Archivos de Medios'),
    ]
    
    STATUS_CHOICES = [
        ('PENDING', 'Pendiente'),
        ('IN_PROGRESS', 'En Progreso'),
        ('COMPLETED', 'Completado'),
        ('FAILED', 'Fallido'),
    ]
    
    name = models.CharField(max_length=255, verbose_name=_('Nombre'))
    file_path = models.CharField(max_length=500, verbose_name=_('Ruta del Archivo'))
    backup_type = models.CharField(max_length=10, choices=BACKUP_TYPES, default='FULL', verbose_name=_('Tipo de Respaldo'))
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='PENDING', verbose_name=_('Estado'))
    size = models.PositiveBigIntegerField(default=0, verbose_name=_('Tamaño (bytes)'))
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='backups_created', verbose_name=_('Creado por'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Fecha de Creación'))
    completed_at = models.DateTimeField(null=True, blank=True, verbose_name=_('Fecha de Finalización'))
    notes = models.TextField(blank=True, verbose_name=_('Notas'))
    is_auto = models.BooleanField(default=False, verbose_name=_('Automático'))
    
    class Meta:
        verbose_name = _('Respaldo')
        verbose_name_plural = _('Respaldos')
        ordering = ['-created_at']
    
    def __str__(self):
        return self.name
    
    @property
    def size_in_mb(self):
        """Retorna el tamaño del respaldo en MB"""
        return round(self.size / (1024 * 1024), 2)
    
    @property
    def file_exists(self):
        """Verifica si el archivo de respaldo existe"""
        return os.path.exists(self.file_path)
    
    @property
    def file_name(self):
        """Retorna el nombre del archivo sin la ruta"""
        return os.path.basename(self.file_path)


class RestoreLog(models.Model):
    """Modelo para registrar las restauraciones realizadas"""
    STATUS_CHOICES = [
        ('IN_PROGRESS', 'En Progreso'),
        ('COMPLETED', 'Completado'),
        ('FAILED', 'Fallido'),
    ]
    
    backup = models.ForeignKey(Backup, on_delete=models.CASCADE, related_name='restore_logs', verbose_name=_('Respaldo'))
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='IN_PROGRESS', verbose_name=_('Estado'))
    restored_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='restores', verbose_name=_('Restaurado por'))
    started_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Fecha de Inicio'))
    completed_at = models.DateTimeField(null=True, blank=True, verbose_name=_('Fecha de Finalización'))
    log_output = models.TextField(blank=True, verbose_name=_('Salida de Log'))
    notes = models.TextField(blank=True, verbose_name=_('Notas'))
    
    class Meta:
        verbose_name = _('Registro de Restauración')
        verbose_name_plural = _('Registros de Restauración')
        ordering = ['-started_at']
    
    def __str__(self):
        return f"Restauración de {self.backup} - {self.get_status_display()}"


class BackupConfiguration(models.Model):
    """Modelo para almacenar la configuración de respaldos"""
    max_backups = models.PositiveIntegerField(default=10, verbose_name=_('Máximo de Respaldos'))
    auto_backup_enabled = models.BooleanField(default=False, verbose_name=_('Respaldo Automático Habilitado'))
    auto_backup_frequency = models.PositiveIntegerField(default=24, verbose_name=_('Frecuencia de Respaldo (horas)'))
    include_database = models.BooleanField(default=True, verbose_name=_('Incluir Base de Datos'))
    include_media = models.BooleanField(default=True, verbose_name=_('Incluir Archivos de Medios'))
    compress_backup = models.BooleanField(default=True, verbose_name=_('Comprimir Respaldo'))
    encrypt_backup = models.BooleanField(default=False, verbose_name=_('Cifrar Respaldo'))
    notification_email = models.EmailField(blank=True, verbose_name=_('Email para Notificaciones'))
    last_auto_backup = models.DateTimeField(null=True, blank=True, verbose_name=_('Último Respaldo Automático'))
    backup_directory = models.CharField(max_length=500, default='backups', verbose_name=_('Directorio de Respaldos'))
    
    class Meta:
        verbose_name = _('Configuración de Respaldo')
        verbose_name_plural = _('Configuraciones de Respaldo')
    
    def __str__(self):
        return 'Configuración de Respaldos'
    
    @property
    def next_auto_backup(self):
        """Calcula la fecha del próximo respaldo automático"""
        if not self.auto_backup_enabled or not self.last_auto_backup:
            return None
        
        return self.last_auto_backup + datetime.timedelta(hours=self.auto_backup_frequency)

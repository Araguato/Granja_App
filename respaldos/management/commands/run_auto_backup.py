import os
import logging
from datetime import datetime, timedelta
from django.core.management.base import BaseCommand
from django.utils import timezone
from respaldos.models import BackupConfiguration, Backup
from respaldos.views import create_backup_file

# Configurar logging
logger = logging.getLogger('backup_system')

class Command(BaseCommand):
    help = 'Ejecuta el respaldo automático si está configurado y es el momento adecuado'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Verificando respaldos automáticos...'))
        
        # Obtener la configuración de respaldos
        try:
            config = BackupConfiguration.objects.get(pk=1)
        except BackupConfiguration.DoesNotExist:
            self.stdout.write(self.style.ERROR('No existe configuración de respaldos. Creando configuración por defecto...'))
            config = BackupConfiguration.objects.create(pk=1)
        
        # Verificar si los respaldos automáticos están habilitados
        if not config.auto_backup_enabled:
            self.stdout.write(self.style.WARNING('Los respaldos automáticos están deshabilitados.'))
            return
        
        # Verificar si es momento de realizar un respaldo automático
        now = timezone.now()
        last_backup = config.last_auto_backup
        
        if last_backup:
            next_backup_time = last_backup + timedelta(hours=config.auto_backup_frequency)
            if now < next_backup_time:
                self.stdout.write(self.style.WARNING(
                    f'Aún no es momento de realizar un respaldo automático. '
                    f'Próximo respaldo programado para: {next_backup_time}'
                ))
                return
        
        self.stdout.write(self.style.SUCCESS('Iniciando respaldo automático...'))
        
        # Determinar el tipo de respaldo basado en la configuración
        backup_type = 'FULL'
        if config.include_database and not config.include_media:
            backup_type = 'DB'
        elif not config.include_database and config.include_media:
            backup_type = 'MEDIA'
        
        # Crear un nombre para el respaldo automático
        timestamp = now.strftime('%Y%m%d_%H%M%S')
        backup_name = f'Auto_Backup_{timestamp}'
        
        try:
            # Crear el registro de respaldo
            backup = Backup.objects.create(
                name=backup_name,
                backup_type=backup_type,
                status='PENDING',
                is_auto=True,
                notes='Respaldo automático programado'
            )
            
            # Ejecutar el respaldo
            success, message = create_backup_file(backup, config)
            
            if success:
                # Actualizar la fecha del último respaldo automático
                config.last_auto_backup = now
                config.save()
                
                self.stdout.write(self.style.SUCCESS(f'Respaldo automático completado exitosamente: {backup_name}'))
                
                # Eliminar respaldos antiguos si se excede el límite
                self._cleanup_old_backups(config)
            else:
                self.stdout.write(self.style.ERROR(f'Error en respaldo automático: {message}'))
                
        except Exception as e:
            logger.error(f'Error al crear respaldo automático: {str(e)}')
            self.stdout.write(self.style.ERROR(f'Error al crear respaldo automático: {str(e)}'))
    
    def _cleanup_old_backups(self, config):
        """Elimina los respaldos más antiguos si se excede el límite configurado"""
        if config.max_backups <= 0:
            return
            
        # Obtener todos los respaldos completados ordenados por fecha (más antiguos primero)
        backups = Backup.objects.filter(status='COMPLETED').order_by('created_at')
        
        # Calcular cuántos respaldos hay que eliminar
        total_backups = backups.count()
        to_delete = total_backups - config.max_backups
        
        if to_delete <= 0:
            return
            
        self.stdout.write(self.style.WARNING(f'Eliminando {to_delete} respaldos antiguos...'))
        
        # Eliminar los respaldos más antiguos
        for i, backup in enumerate(backups[:to_delete]):
            try:
                # Eliminar el archivo físico si existe
                if backup.file_exists:
                    try:
                        os.remove(backup.file_path)
                        self.stdout.write(self.style.SUCCESS(f'Archivo eliminado: {backup.file_path}'))
                    except Exception as e:
                        self.stdout.write(self.style.ERROR(f'Error al eliminar archivo: {str(e)}'))
                
                # Eliminar el registro de la base de datos
                backup_name = backup.name
                backup.delete()
                self.stdout.write(self.style.SUCCESS(f'Respaldo eliminado: {backup_name}'))
                
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Error al eliminar respaldo: {str(e)}'))

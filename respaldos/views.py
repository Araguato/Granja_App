import os
import json
import subprocess
import threading
import datetime
from pathlib import Path

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.http import JsonResponse, HttpResponse, FileResponse
from django.urls import reverse
from django.conf import settings
from django.utils import timezone

from .models import Backup, RestoreLog, BackupConfiguration
from .forms import BackupConfigurationForm, CreateBackupForm


def is_admin(user):
    """Verifica si el usuario es administrador"""
    return user.is_authenticated and user.is_superuser


@login_required
@user_passes_test(is_admin)
def backup_dashboard(request):
    """Vista principal del panel de respaldos"""
    # Obtener configuración actual o crear una por defecto
    config, created = BackupConfiguration.objects.get_or_create(pk=1)
    
    # Obtener respaldos recientes
    recent_backups = Backup.objects.all()[:5]
    
    # Obtener estadísticas
    total_backups = Backup.objects.count()
    successful_backups = Backup.objects.filter(status='COMPLETED').count()
    failed_backups = Backup.objects.filter(status='FAILED').count()
    
    # Calcular espacio total usado por respaldos
    total_size = sum(backup.size for backup in Backup.objects.all())
    total_size_mb = round(total_size / (1024 * 1024), 2)
    
    # Verificar si hay respaldos en progreso
    in_progress = Backup.objects.filter(status='IN_PROGRESS').exists()
    
    context = {
        'config': config,
        'recent_backups': recent_backups,
        'total_backups': total_backups,
        'successful_backups': successful_backups,
        'failed_backups': failed_backups,
        'total_size_mb': total_size_mb,
        'in_progress': in_progress,
        'next_auto_backup': config.next_auto_backup,
    }
    
    return render(request, 'respaldos/dashboard.html', context)


@login_required
@user_passes_test(is_admin)
def backup_list(request):
    """Vista para listar todos los respaldos"""
    backups = Backup.objects.all()
    
    context = {
        'backups': backups,
    }
    
    return render(request, 'respaldos/backup_list.html', context)


@login_required
@user_passes_test(is_admin)
def backup_detail(request, backup_id):
    """Vista para mostrar detalles de un respaldo"""
    backup = get_object_or_404(Backup, pk=backup_id)
    restore_logs = backup.restore_logs.all()
    
    context = {
        'backup': backup,
        'restore_logs': restore_logs,
    }
    
    return render(request, 'respaldos/backup_detail.html', context)


@login_required
@user_passes_test(is_admin)
def create_backup(request):
    """Vista para crear un nuevo respaldo"""
    if request.method == 'POST':
        form = CreateBackupForm(request.POST)
        if form.is_valid():
            backup_type = form.cleaned_data['backup_type']
            notes = form.cleaned_data['notes']
            
            # Crear registro de respaldo
            timestamp = timezone.now().strftime("%Y%m%d_%H%M%S")
            backup_name = f"{backup_type.lower()}_backup_{timestamp}"
            
            backup = Backup(
                name=backup_name,
                file_path=os.path.join(settings.BASE_DIR, 'backups', f"{backup_name}.zip"),
                backup_type=backup_type,
                status='IN_PROGRESS',
                created_by=request.user,
                notes=notes
            )
            backup.save()
            
            # Iniciar proceso de respaldo en segundo plano
            thread = threading.Thread(
                target=run_backup_process,
                args=(backup, backup_type)
            )
            thread.daemon = True
            thread.start()
            
            messages.success(request, 'Respaldo iniciado correctamente. Este proceso puede tardar varios minutos.')
            return redirect('respaldos:backup_detail', backup_id=backup.id)
    else:
        form = CreateBackupForm()
    
    context = {
        'form': form,
    }
    
    return render(request, 'respaldos/create_backup.html', context)


@login_required
@user_passes_test(is_admin)
def restore_backup(request, backup_id):
    """Vista para restaurar un respaldo"""
    backup = get_object_or_404(Backup, pk=backup_id)
    
    # Verificar que el respaldo esté completo y el archivo exista
    if backup.status != 'COMPLETED' or not backup.file_exists:
        messages.error(request, 'No se puede restaurar este respaldo porque no está completo o el archivo no existe.')
        return redirect('respaldos:backup_detail', backup_id=backup.id)
    
    if request.method == 'POST':
        # Registrar el inicio de la restauración
        restore_log = RestoreLog(
            backup=backup,
            restored_by=request.user,
            status='IN_PROGRESS'
        )
        restore_log.save()
        
        # Iniciar proceso de restauración en segundo plano
        thread = threading.Thread(
            target=run_restore_process,
            args=(backup, restore_log)
        )
        thread.daemon = True
        thread.start()
        
        messages.success(request, 'Restauración iniciada correctamente. Este proceso puede tardar varios minutos.')
        return redirect('respaldos:backup_detail', backup_id=backup.id)
    
    context = {
        'backup': backup,
    }
    
    return render(request, 'respaldos/restore_backup.html', context)


@login_required
@user_passes_test(is_admin)
def download_backup(request, backup_id):
    """Vista para descargar un archivo de respaldo"""
    backup = get_object_or_404(Backup, pk=backup_id)
    
    # Verificar que el archivo exista
    if not backup.file_exists:
        messages.error(request, 'El archivo de respaldo no existe.')
        return redirect('respaldos:backup_detail', backup_id=backup.id)
    
    # Devolver el archivo como respuesta para descarga
    response = FileResponse(
        open(backup.file_path, 'rb'),
        as_attachment=True,
        filename=backup.file_name
    )
    return response


@login_required
@user_passes_test(is_admin)
def delete_backup(request, backup_id):
    """Vista para eliminar un respaldo"""
    backup = get_object_or_404(Backup, pk=backup_id)
    
    if request.method == 'POST':
        # Eliminar el archivo si existe
        if backup.file_exists:
            os.remove(backup.file_path)
        
        # Eliminar el registro
        backup.delete()
        
        messages.success(request, 'Respaldo eliminado correctamente.')
        return redirect('respaldos:backup_list')
    
    context = {
        'backup': backup,
    }
    
    return render(request, 'respaldos/delete_backup.html', context)


@login_required
@user_passes_test(is_admin)
def backup_config(request):
    """Vista para configurar los respaldos"""
    # Obtener configuración actual o crear una por defecto
    config, created = BackupConfiguration.objects.get_or_create(pk=1)
    
    if request.method == 'POST':
        form = BackupConfigurationForm(request.POST, instance=config)
        if form.is_valid():
            form.save()
            
            # Actualizar el archivo de configuración JSON
            update_backup_config_file(config)
            
            messages.success(request, 'Configuración de respaldos actualizada correctamente.')
            return redirect('respaldos:backup_dashboard')
    else:
        form = BackupConfigurationForm(instance=config)
    
    context = {
        'form': form,
        'config': config,
    }
    
    return render(request, 'respaldos/backup_config.html', context)


@login_required
@user_passes_test(is_admin)
def backup_status(request, backup_id):
    """Vista AJAX para verificar el estado de un respaldo"""
    backup = get_object_or_404(Backup, pk=backup_id)
    
    data = {
        'id': backup.id,
        'status': backup.status,
        'status_display': backup.get_status_display(),
        'size': backup.size_in_mb,
        'completed_at': backup.completed_at.isoformat() if backup.completed_at else None,
    }
    
    return JsonResponse(data)


# Funciones auxiliares

def run_backup_process(backup, backup_type):
    """Ejecuta el proceso de respaldo en segundo plano"""
    try:
        # Construir comando para ejecutar el script de respaldo
        cmd = [
            os.path.join(settings.BASE_DIR, 'venv', 'Scripts', 'python.exe'),
            os.path.join(settings.BASE_DIR, 'backup_system.py')
        ]
        
        # Añadir opciones según el tipo de respaldo
        if backup_type == 'DB':
            cmd.append('--backup-db')
        elif backup_type == 'MEDIA':
            cmd.append('--backup-media')
        else:  # FULL
            cmd.append('--backup-all')
        
        # Ejecutar el comando
        process = subprocess.run(
            cmd,
            cwd=settings.BASE_DIR,
            capture_output=True,
            text=True
        )
        
        # Actualizar el registro de respaldo
        if process.returncode == 0:
            # Buscar el archivo generado
            backup_dir = Path(settings.BASE_DIR) / 'backups'
            files = list(backup_dir.glob(f"*{backup.name}*"))
            
            if files:
                file_path = str(files[0])
                file_size = os.path.getsize(file_path)
                
                backup.file_path = file_path
                backup.size = file_size
                backup.status = 'COMPLETED'
                backup.completed_at = timezone.now()
            else:
                backup.status = 'FAILED'
                backup.notes += "\n\nNo se encontró el archivo de respaldo generado."
        else:
            backup.status = 'FAILED'
            backup.notes += f"\n\nError: {process.stderr}"
        
        backup.save()
        
        # Actualizar configuración si es un respaldo automático
        if backup.is_auto and backup.status == 'COMPLETED':
            config = BackupConfiguration.objects.get(pk=1)
            config.last_auto_backup = timezone.now()
            config.save()
    
    except Exception as e:
        # Registrar cualquier error
        backup.status = 'FAILED'
        backup.notes += f"\n\nExcepción: {str(e)}"
        backup.save()


def run_restore_process(backup, restore_log):
    """Ejecuta el proceso de restauración en segundo plano"""
    try:
        # Construir comando para ejecutar el script de respaldo en modo restauración
        cmd = [
            os.path.join(settings.BASE_DIR, 'venv', 'Scripts', 'python.exe'),
            os.path.join(settings.BASE_DIR, 'backup_system.py'),
            '--restore', backup.file_path
        ]
        
        # Ejecutar el comando
        process = subprocess.run(
            cmd,
            cwd=settings.BASE_DIR,
            capture_output=True,
            text=True
        )
        
        # Actualizar el registro de restauración
        restore_log.completed_at = timezone.now()
        
        if process.returncode == 0:
            restore_log.status = 'COMPLETED'
            restore_log.log_output = process.stdout
        else:
            restore_log.status = 'FAILED'
            restore_log.log_output = f"Error: {process.stderr}\n\nSalida: {process.stdout}"
        
        restore_log.save()
    
    except Exception as e:
        # Registrar cualquier error
        restore_log.status = 'FAILED'
        restore_log.log_output = f"Excepción: {str(e)}"
        restore_log.completed_at = timezone.now()
        restore_log.save()


def update_backup_config_file(config):
    """Actualiza el archivo de configuración JSON con los valores del modelo"""
    config_file = os.path.join(settings.BASE_DIR, 'backup_config.json')
    
    # Cargar configuración actual
    with open(config_file, 'r', encoding='utf-8') as f:
        backup_config = json.load(f)
    
    # Actualizar valores
    backup_config['backup_settings']['max_backups'] = config.max_backups
    backup_config['backup_settings']['include_media'] = config.include_media
    backup_config['backup_settings']['compress'] = config.compress_backup
    backup_config['backup_settings']['encrypt'] = config.encrypt_backup
    
    # Actualizar notificaciones
    if config.notification_email:
        backup_config['notification_settings']['enabled'] = True
        backup_config['notification_settings']['recipients'] = [config.notification_email]
    else:
        backup_config['notification_settings']['enabled'] = False
    
    # Guardar configuración actualizada
    with open(config_file, 'w', encoding='utf-8') as f:
        json.dump(backup_config, f, indent=4)

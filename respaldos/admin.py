from django.contrib import admin
from django.utils.html import format_html
from .models import Backup, RestoreLog, BackupConfiguration


class RestoreLogInline(admin.TabularInline):
    model = RestoreLog
    extra = 0
    readonly_fields = ['status', 'restored_by', 'started_at', 'completed_at']
    can_delete = False
    max_num = 0
    verbose_name = "Historial de Restauración"
    verbose_name_plural = "Historial de Restauraciones"


@admin.register(Backup)
class BackupAdmin(admin.ModelAdmin):
    list_display = ['name', 'backup_type', 'status_badge', 'size_display', 'created_at', 'created_by', 'file_exists_icon']
    list_filter = ['status', 'backup_type', 'is_auto', 'created_at']
    search_fields = ['name', 'notes']
    readonly_fields = ['name', 'file_path', 'backup_type', 'status', 'size', 'created_by', 'created_at', 'completed_at', 'is_auto', 'file_exists_display']
    fieldsets = [
        (None, {
            'fields': ['name', 'backup_type', 'status', 'size', 'file_path', 'file_exists_display']
        }),
        ('Información Adicional', {
            'fields': ['created_by', 'created_at', 'completed_at', 'is_auto', 'notes']
        }),
    ]
    inlines = [RestoreLogInline]
    
    def size_display(self, obj):
        return f"{obj.size_in_mb} MB"
    size_display.short_description = "Tamaño"
    
    def status_badge(self, obj):
        status_colors = {
            'PENDING': 'secondary',
            'IN_PROGRESS': 'info',
            'COMPLETED': 'success',
            'FAILED': 'danger',
        }
        color = status_colors.get(obj.status, 'secondary')
        return format_html('<span class="badge bg-{}">{}', color, obj.get_status_display())
    status_badge.short_description = "Estado"
    
    def file_exists_icon(self, obj):
        if obj.file_exists:
            return format_html('<i class="fas fa-check-circle text-success"></i>')
        return format_html('<i class="fas fa-times-circle text-danger"></i>')
    file_exists_icon.short_description = "Archivo"
    
    def file_exists_display(self, obj):
        if obj.file_exists:
            return format_html('<span class="badge bg-success">Disponible</span> {}', obj.file_name)
        return format_html('<span class="badge bg-danger">No disponible</span>')
    file_exists_display.short_description = "Estado del Archivo"
    
    def has_add_permission(self, request):
        return False
    
    def has_change_permission(self, request, obj=None):
        return False


@admin.register(BackupConfiguration)
class BackupConfigurationAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'max_backups', 'auto_backup_enabled', 'auto_backup_frequency', 'last_auto_backup']
    fieldsets = [
        ('Configuración General', {
            'fields': ['max_backups', 'backup_directory']
        }),
        ('Respaldo Automático', {
            'fields': ['auto_backup_enabled', 'auto_backup_frequency', 'last_auto_backup']
        }),
        ('Contenido', {
            'fields': ['include_database', 'include_media']
        }),
        ('Opciones Avanzadas', {
            'fields': ['compress_backup', 'encrypt_backup']
        }),
        ('Notificaciones', {
            'fields': ['notification_email']
        }),
    ]
    readonly_fields = ['last_auto_backup']
    
    def has_add_permission(self, request):
        # Solo permitir una configuración
        return BackupConfiguration.objects.count() == 0
    
    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(RestoreLog)
class RestoreLogAdmin(admin.ModelAdmin):
    list_display = ['backup', 'status', 'restored_by', 'started_at', 'completed_at']
    list_filter = ['status', 'started_at']
    readonly_fields = ['backup', 'status', 'restored_by', 'started_at', 'completed_at', 'log_output']
    
    def has_add_permission(self, request):
        return False
    
    def has_change_permission(self, request, obj=None):
        return False

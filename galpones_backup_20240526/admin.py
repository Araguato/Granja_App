from django.contrib import admin
from django.utils.html import format_html
from .models import Galpon


class GalponAdmin(admin.ModelAdmin):
    """Configuración del administrador para el modelo Galpon"""
    
    # Campos a mostrar en la lista
    list_display = ('numero', 'nombre', 'tipo', 'estado', 'capacidad', 'empresa', 'responsable_info', 'ubicacion_display')
    
    # Filtros laterales
    list_filter = ('tipo', 'estado', 'empresa')
    
    # Búsqueda
    search_fields = ('numero', 'nombre', 'ubicacion', 'observaciones')
    
    # Campos de solo lectura
    readonly_fields = ('fecha_creacion', 'fecha_actualizacion')
    
    # Agrupación de campos en el formulario de edición
    fieldsets = (
        ('Información Básica', {
            'fields': ('numero', 'nombre', 'tipo', 'estado', 'capacidad')
        }),
        ('Ubicación y Responsable', {
            'fields': ('ubicacion', 'empresa', 'responsable')
        }),
        ('Información Adicional', {
            'fields': ('observaciones', 'fecha_creacion', 'fecha_actualizacion'),
            'classes': ('collapse',)
        }),
    )
    
    # Métodos personalizados para mostrar información en la lista
    def responsable_info(self, obj):
        """Muestra el nombre completo del responsable"""
        if obj.responsable:
            return f"{obj.responsable.get_full_name() or obj.responsable.username}"
        return "Sin asignar"
    responsable_info.short_description = 'Responsable'
    
    def ubicacion_display(self, obj):
        """Muestra una versión abreviada de la ubicación"""
        if obj.ubicacion and len(obj.ubicacion) > 30:
            return f"{obj.ubicacion[:30]}..."
        return obj.ubicacion or ""
    ubicacion_display.short_description = 'Ubicación'
    
    # Ordenamiento por defecto
    ordering = ('numero',)
    
    # Personalización del título del sitio de administración
    site_header = 'Administración de Galpones'
    site_title = 'Sistema de Gestión Avícola'
    index_title = 'Panel de Control'


# Registrar el modelo con su configuración personalizada
admin.site.register(Galpon, GalponAdmin)

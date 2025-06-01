from django.contrib import admin
from .models import ReporteGenerado, PlantillaReporte

class ReporteGeneradoAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'tipo_reporte', 'fecha_inicio', 'fecha_fin', 'formato', 'usuario_generador', 'fecha_generacion')
    list_filter = ('tipo_reporte', 'formato', 'usuario_generador', 'fecha_generacion')
    search_fields = ('titulo', 'usuario_generador__username')
    date_hierarchy = 'fecha_generacion'
    readonly_fields = ('fecha_generacion',)
    fieldsets = (
        ('Información General', {
            'fields': ('titulo', 'tipo_reporte', 'formato')
        }),
        ('Periodo', {
            'fields': ('fecha_inicio', 'fecha_fin')
        }),
        ('Generación', {
            'fields': ('usuario_generador', 'fecha_generacion', 'archivo')
        }),
        ('Configuración Avanzada', {
            'classes': ('collapse',),
            'fields': ('parametros',)
        }),
    )

class PlantillaReporteAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'tipo_reporte', 'usuario_creador', 'fecha_creacion', 'es_predeterminada')
    list_filter = ('tipo_reporte', 'usuario_creador', 'es_predeterminada')
    search_fields = ('nombre', 'descripcion', 'usuario_creador__username')
    date_hierarchy = 'fecha_creacion'
    readonly_fields = ('fecha_creacion', 'fecha_modificacion')
    fieldsets = (
        ('Información General', {
            'fields': ('nombre', 'descripcion', 'tipo_reporte', 'es_predeterminada')
        }),
        ('Asignación', {
            'fields': ('usuario_creador', 'fecha_creacion', 'fecha_modificacion')
        }),
        ('Configuración', {
            'classes': ('collapse',),
            'fields': ('configuracion',)
        }),
    )

admin.site.register(ReporteGenerado, ReporteGeneradoAdmin)
admin.site.register(PlantillaReporte, PlantillaReporteAdmin)

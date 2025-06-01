from django.contrib import admin
from django.utils.html import format_html
from django.contrib.auth import get_user_model
from .models import Galpon

class GalponAdmin(admin.ModelAdmin):
    list_display = ('numero_galpon', 'get_granja_display', 'get_tipo_galpon_display', 'get_responsable_display', 'capacidad_aves', 'area_metros_cuadrados')
    list_display_links = ('numero_galpon',)
    list_editable = ('capacidad_aves', 'area_metros_cuadrados')
    search_fields = ('numero_galpon', 'granja__nombre', 'responsable__username')
    list_filter = ('granja', 'tipo_galpon')
    list_per_page = 20
    raw_id_fields = ('granja', 'responsable', 'creado_por', 'actualizado_por')
    readonly_fields = ('fecha_creacion', 'fecha_actualizacion', 'get_granja_display', 'get_responsable_display')
    
    fieldsets = (
        (None, {
            'fields': ('granja', 'numero_galpon', 'tipo_galpon', 'responsable', 'capacidad_aves', 'area_metros_cuadrados')
        }),
        ('Auditoría', {
            'fields': (('fecha_creacion', 'creado_por'), ('fecha_actualizacion', 'actualizado_por')),
            'classes': ('collapse',)
        }),
    )
    
    def get_granja_display(self, obj):
        return str(obj.granja) if obj.granja else "-"
    get_granja_display.short_description = "Granja"
    get_granja_display.admin_order_field = 'granja__nombre'
    
    def get_responsable_display(self, obj):
        return str(obj.responsable) if obj.responsable else "-"
    get_responsable_display.short_description = "Responsable"
    get_responsable_display.admin_order_field = 'responsable__username'
    
    def get_tipo_galpon_display(self, obj):
        return obj.get_tipo_galpon_display()
    get_tipo_galpon_display.short_description = 'Tipo de Galpón'
    get_tipo_galpon_display.admin_order_field = 'tipo_galpon'
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('granja', 'responsable', 'creado_por', 'actualizado_por')
    
    def get_search_results(self, request, queryset, search_term):
        queryset, use_distinct = super().get_search_results(request, queryset, search_term)
        try:
            queryset = self.model.objects.filter(pk__in=queryset.values_list('pk', flat=True))
        except (ValueError, self.model.DoesNotExist):
            pass
        return queryset, use_distinct
    
    def save_model(self, request, obj, form, change):
        if not obj.pk:  # Si es un nuevo objeto
            obj.creado_por = request.user
        obj.actualizado_por = request.user
        super().save_model(request, obj, form, change)

from django.contrib import admin
from .models import Galpon

class GalponAdmin(admin.ModelAdmin):
    # List display configuration
    list_display = ('numero_galpon', 'get_granja_display', 'get_tipo_galpon_display', 'get_responsable_display', 'capacidad_aves', 'area_metros_cuadrados')
    list_display_links = ('numero_galpon',)  # Make only the galpon number clickable
    list_editable = ('capacidad_aves', 'area_metros_cuadrados')
    
    # Search and filter options
    search_fields = ('numero_galpon', 'granja__nombre', 'responsable__username')
    list_filter = ('granja', 'tipo_galpon')
    list_per_page = 20
    
    # Form configuration
    raw_id_fields = ('granja', 'responsable', 'creado_por', 'actualizado_por')
    readonly_fields = ('fecha_creacion', 'fecha_actualizacion', 'get_granja_display', 'get_responsable_display')
    
    def get_granja_display(self, obj):
        return str(obj.granja) if obj.granja else ""
    get_granja_display.short_description = "Granja"
    get_granja_display.admin_order_field = 'granja__nombre'
    
    def get_responsable_display(self, obj):
        return str(obj.responsable) if obj.responsable else ""
    get_responsable_display.short_description = "Responsable"
    get_responsable_display.admin_order_field = 'responsable__username'
    
    def get_tipo_galpon_display(self, obj):
        return obj.get_tipo_galpon_display()
    get_tipo_galpon_display.short_description = 'Tipo de Galpón'
    get_tipo_galpon_display.admin_order_field = 'tipo_galpon'
    
    # Organize fields in the detail view
    fieldsets = (
        (None, {
            'fields': ('granja', 'numero_galpon', 'tipo_galpon', 'responsable', 'capacidad_aves', 'area_metros_cuadrados')
        }),
        ('Auditoría', {
            'fields': (('fecha_creacion', 'creado_por'), ('fecha_actualizacion', 'actualizado_por')),
            'classes': ('collapse',)
        }),
    )
    
    def get_queryset(self, request):
        qs = super().get_queryset(request).select_related('granja', 'responsable')
        return qs
        
    def get_search_results(self, request, queryset, search_term):
        queryset, use_distinct = super().get_search_results(request, queryset, search_term)
        if search_term:
            queryset |= self.model.objects.filter(
                granja__nombre__icontains=search_term
            ) | self.model.objects.filter(
                responsable__username__icontains=search_term
            )
        return queryset, use_distinct
    
    def save_model(self, request, obj, form, change):
        if not obj.pk:  # New record
            obj.creado_por = request.user
        obj.actualizado_por = request.user
        super().save_model(request, obj, form, change)

# Register the model with the custom admin site
from avicola.custom_admin import custom_admin_site
custom_admin_site.register(Galpon, GalponAdmin)

# Also register with default admin site for testing
from django.contrib import admin as default_admin
if not default_admin.site.is_registered(Galpon):
    default_admin.site.register(Galpon, GalponAdmin)

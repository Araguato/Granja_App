from django.contrib import admin
from .models import Proveedor, Raza, Alimento, Vacuna, Insumo, GuiaDesempenoRaza, ConsumoAlimento, AplicacionVacuna

# Import the custom admin site
from avicola.custom_admin import custom_admin_site as admin_site

class ProveedorAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'rif', 'contacto_principal', 'telefono', 'email')
    search_fields = ('nombre', 'rif', 'contacto_principal')
    list_filter = ('nombre',)

class RazaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'tipo_raza')
    search_fields = ('nombre',)
    list_filter = ('tipo_raza',)

class AlimentoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'etapa', 'proveedor', 'proteina_porcentaje')
    search_fields = ('nombre', 'etapa', 'proveedor__nombre')
    list_filter = ('etapa', 'proveedor', 'activo')
    autocomplete_fields = ['proveedor']
    list_select_related = ['proveedor']
    date_hierarchy = 'fecha_ingreso'

class VacunaAdmin(admin.ModelAdmin):
    list_display = ('nombre_comercial', 'principio_activo', 'proveedor', 'lote_fabricante', 'fecha_vencimiento')
    search_fields = ('nombre_comercial', 'principio_activo', 'proveedor__nombre', 'lote_fabricante')
    list_filter = ('proveedor', 'principio_activo')
    date_hierarchy = 'fecha_vencimiento'
    autocomplete_fields = ['proveedor']

class InsumoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'tipo_insumo', 'proveedor')
    search_fields = ('nombre', 'proveedor__nombre')
    list_filter = ('tipo_insumo', 'proveedor')
    autocomplete_fields = ['proveedor']

class ConsumoAlimentoAdmin(admin.ModelAdmin):
    list_display = ('alimento', 'lote_aves', 'cantidad_kg', 'fecha_consumo', 'registrado_por')
    list_filter = ('fecha_consumo', 'alimento', 'lote_aves')
    search_fields = ('alimento__nombre', 'lote_aves__codigo_lote', 'observaciones')
    date_hierarchy = 'fecha_consumo'
    autocomplete_fields = ['alimento', 'lote_aves', 'registrado_por']

class AplicacionVacunaAdmin(admin.ModelAdmin):
    list_display = ('vacuna', 'lote_aves', 'fecha_aplicacion', 'dosis_ml', 'aplicada_por')
    list_filter = ('vacuna', 'lote_aves', 'fecha_aplicacion')
    search_fields = ('vacuna__nombre_comercial', 'lote_aves__codigo_lote', 'observaciones')
    date_hierarchy = 'fecha_aplicacion'
    autocomplete_fields = ['vacuna', 'lote_aves', 'aplicada_por']

# Register models with the custom admin site
admin_site.register(Proveedor, ProveedorAdmin)
admin_site.register(Raza, RazaAdmin)
admin_site.register(Alimento, AlimentoAdmin)
admin_site.register(Vacuna, VacunaAdmin)
admin_site.register(Insumo, InsumoAdmin)
admin_site.register(ConsumoAlimento, ConsumoAlimentoAdmin)
admin_site.register(AplicacionVacuna, AplicacionVacunaAdmin)

class GuiaDesempenoRazaAdmin(admin.ModelAdmin):
    list_display = ('raza', 'dia_edad', 'peso_corporal_ideal_gr', 'consumo_alimento_diario_ideal_gr_ave', 'viabilidad_ideal_porc')
    list_filter = ('raza', 'dia_edad')
    search_fields = ('raza__nombre',)
    ordering = ('raza', 'dia_edad')
    autocomplete_fields = ['raza']

# Register models with the custom admin site
admin_site.register(Proveedor, ProveedorAdmin)
admin_site.register(Raza, RazaAdmin)
admin_site.register(Alimento, AlimentoAdmin)
admin_site.register(Vacuna, VacunaAdmin)
admin_site.register(Insumo, InsumoAdmin)
admin_site.register(ConsumoAlimento, ConsumoAlimentoAdmin)
admin_site.register(AplicacionVacuna, AplicacionVacunaAdmin)
admin_site.register(GuiaDesempenoRaza, GuiaDesempenoRazaAdmin)

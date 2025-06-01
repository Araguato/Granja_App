from django.contrib import admin
from .models import Cliente, TipoHuevo, InventarioHuevos, Venta, DetalleVenta
from produccion.models import Lote

# Import the custom admin site
from avicola.custom_admin import custom_admin_site as admin_site

class ClienteAdmin(admin.ModelAdmin):
    list_display = ('nombre_razon_social', 'rif_cedula', 'telefono_principal', 'email')
    search_fields = ('nombre_razon_social', 'rif_cedula', 'contacto_principal')

class TipoHuevoAdmin(admin.ModelAdmin):
    list_display = ('get_clasificacion_display', 'descripcion')
    search_fields = ('clasificacion', 'descripcion')

class InventarioHuevosAdmin(admin.ModelAdmin):
    list_display = ('tipo_huevo', 'cantidad_disponible', 'fecha_ingreso_inventario', 'lote_produccion')
    search_fields = ('tipo_huevo__clasificacion', 'lote_produccion__codigo_lote')
    list_filter = ('tipo_huevo', 'fecha_ingreso_inventario')
    date_hierarchy = 'fecha_ingreso_inventario'
    autocomplete_fields = ['tipo_huevo', 'lote_produccion']

class DetalleVentaInline(admin.TabularInline):
    model = DetalleVenta
    extra = 1 # Número de formularios extra para detalles
    autocomplete_fields = ['tipo_huevo', 'inventario_huevo_origen']

class VentaAdmin(admin.ModelAdmin):
    list_display = ('cliente', 'fecha_venta', 'total_venta', 'vendedor')
    search_fields = ('cliente__nombre_razon_social', 'numero_factura', 'vendedor__username')
    list_filter = ('fecha_venta', 'vendedor', 'estado_pago' if hasattr(Venta, 'estado_pago') else 'fecha_venta') # Condicional por si el campo no existe
    date_hierarchy = 'fecha_venta'
    inlines = [DetalleVentaInline]
    autocomplete_fields = ['cliente', 'vendedor']
    readonly_fields = ('subtotal', 'impuesto', 'total_venta') # Estos se calculan

# Register models with the custom admin site
admin_site.register(Cliente, ClienteAdmin)
admin_site.register(TipoHuevo, TipoHuevoAdmin)
admin_site.register(InventarioHuevos, InventarioHuevosAdmin)
admin_site.register(Venta, VentaAdmin)
# Register Lote model for autocomplete if not already registered
if Lote not in admin_site._registry:
    from produccion.admin import LoteAdmin
    admin_site.register(Lote, LoteAdmin)

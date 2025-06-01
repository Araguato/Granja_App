from django import forms
from django.contrib import admin
from django.forms import ModelForm
from django.utils.html import format_html
from django.contrib.auth import get_user_model

# Import models first to avoid circular imports
from .models import (
    Granja, Galpon, Lote, SeguimientoDiario, 
    MortalidadDiaria, MortalidadSemanal, SeguimientoEngorde
)
from .consumo_energia import ConsumoEnergia

# Import GalponAdmin from the separate file to avoid circular imports
from .galpon_admin import GalponAdmin

# Import the custom admin site function
def get_admin_site():
    from avicola.custom_admin import custom_admin_site
    return custom_admin_site

# Import default admin for fallback registration
from django.contrib import admin as default_admin

class SeguimientoDiarioForm(ModelForm):
    class Meta:
        model = SeguimientoDiario
        fields = '__all__'
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Hide tipo_seguimiento field in the form
        if 'tipo_seguimiento' in self.fields:
            self.fields['tipo_seguimiento'].widget = forms.HiddenInput()
    
    def clean(self):
        cleaned_data = super().clean()
        lote = cleaned_data.get('lote')
        
        # Set tipo_seguimiento based on lote's galpon type
        if lote and hasattr(lote, 'galpon') and lote.galpon:
            if lote.galpon.tipo_galpon == 'POSTURA':
                cleaned_data['tipo_seguimiento'] = 'PRODUCCION'  # Producción de Huevos
            elif lote.galpon.tipo_galpon in ['CRIA', 'RECRIA']:
                cleaned_data['tipo_seguimiento'] = 'ENGORDE'  # Engorde de Pollos
            elif lote.galpon.tipo_galpon == 'REPRODUCTOR':
                cleaned_data['tipo_seguimiento'] = 'MIXTO'  # Producción y Engorde
            # For other types (like CUARENTENA), it will use the default 'PRODUCCION' or the one already set
        
        return cleaned_data



class GranjaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'ubicacion_geografica', 'encargado', 'telefono')
    search_fields = ('nombre', 'ubicacion_geografica', 'encargado__username')
    list_filter = ('estado',)

class LoteAdmin(admin.ModelAdmin):
    list_display = ('codigo_lote', 'get_galpon_display', 'get_raza_display', 'cantidad_inicial_aves', 'fecha_ingreso', 'edad_semanas', 'estado')
    search_fields = ('codigo_lote', 'galpon__numero_galpon', 'raza__nombre')
    list_filter = ('raza', 'estado', 'fecha_ingreso')
    date_hierarchy = 'fecha_ingreso'
    raw_id_fields = ('galpon', 'raza', 'alimento')
    readonly_fields = ('edad_semanas', 'get_galpon_display', 'get_raza_display')
    
    def get_galpon_display(self, obj):
        try:
            if obj.galpon:
                return str(obj.galpon)
            return "[Galpón eliminado]"
        except Exception:
            return "[Error cargando galpón]"
    get_galpon_display.short_description = "Galpón"
    
    def get_raza_display(self, obj):
        return str(obj.raza) if obj.raza else ""
    get_raza_display.short_description = "Raza"
    
    def edad_semanas(self, obj):
        return obj.edad_semanas
    edad_semanas.short_description = "Edad Actual (Semanas)"
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('galpon', 'raza', 'alimento')
    
    def save_model(self, request, obj, form, change):
        if not obj.pk:  # Si es un nuevo objeto
            obj.creado_por = request.user
        obj.actualizado_por = request.user
        super().save_model(request, obj, form, change)
    
    def get_form(self, request, obj=None, **kwargs):
        # Import here to avoid circular imports
        from django import forms
        from django.contrib.admin.widgets import ForeignKeyRawIdWidget
        from django.contrib import admin
        from django.core.exceptions import ObjectDoesNotExist
        
        # Get the default form
        form = super().get_form(request, obj, **kwargs)
        
        # Customize the form fields if needed
        if 'galpon' in form.base_fields:
            try:
                form.base_fields['galpon'].widget = ForeignKeyRawIdWidget(
                    form.base_fields['galpon'].remote_field,
                    admin.site,
                    using=form.base_fields['galpon']._db
                )
            except (AttributeError, ObjectDoesNotExist):
                # If there's an issue with the galpon field, make it optional
                form.base_fields['galpon'].required = False
        
        if 'raza' in form.base_fields:
            try:
                form.base_fields['raza'].widget = ForeignKeyRawIdWidget(
                    form.base_fields['raza'].remote_field,
                    admin.site,
                    using=form.base_fields['raza']._db
                )
            except (AttributeError, ObjectDoesNotExist):
                form.base_fields['raza'].required = False
            
        if 'alimento' in form.base_fields:
            try:
                form.base_fields['alimento'].widget = ForeignKeyRawIdWidget(
                    form.base_fields['alimento'].remote_field,
                    admin.site,
                    using=form.base_fields['alimento']._db
                )
            except (AttributeError, ObjectDoesNotExist):
                form.base_fields['alimento'].required = False
                
        return form
        
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        # Use select_related to optimize database queries
        return qs.select_related('galpon', 'raza', 'alimento')
        
    def save_model(self, request, obj, form, change):
        # Add any custom save logic here
        try:
            super().save_model(request, obj, form, change)
        except Exception as e:
            from django.contrib import messages
            messages.error(request, f"Error al guardar el lote: {str(e)}")
            raise

class SeguimientoEngordeInline(admin.TabularInline):
    model = SeguimientoEngorde
    extra = 0
    can_delete = False
    verbose_name_plural = 'Detalles de Engorde'
    readonly_fields = ('eficiencia_energetica', 'eficiencia_proteica', 'relacion_energia_proteina')
    fieldsets = (
        (None, {
            'fields': (('ganancia_diaria_peso', 'conversion_alimenticia', 'uniformidad'),)
        }),
        ('Eficiencia Nutricional', {
            'fields': (('eficiencia_energetica', 'eficiencia_proteica', 'relacion_energia_proteina'),),
            'classes': ('collapse',),
            'description': 'Estos valores se calculan automáticamente al guardar el registro'
        }),
        ('Métricas Avanzadas', {
            'fields': (('indice_productividad', 'longitud_corporal', 'ancho_pechuga'),),
            'classes': ('collapse',)
        }),
        ('Evaluación de Salud', {
            'fields': (('calidad_plumaje', 'calidad_patas'),),
            'classes': ('collapse',)
        }),
        ('Observaciones', {
            'fields': ('observaciones_engorde',),
            'classes': ('collapse',)
        }),
    )

class MortalidadDiariaInline(admin.TabularInline):
    model = MortalidadDiaria
    extra = 0
    fields = ('fecha', 'cantidad_muertes', 'causa')
    verbose_name = "Registro de Mortalidad"
    verbose_name_plural = "Registros de Mortalidad"

class SeguimientoDiarioAdmin(admin.ModelAdmin):
    form = SeguimientoDiarioForm
    list_display = ('lote', 'fecha_seguimiento', 'tipo_seguimiento', 'huevos_totales', 'peso_promedio_ave', 'mortalidad', 'registrado_por')
    list_filter = ('tipo_seguimiento', 'lote__galpon__granja', 'lote', 'fecha_seguimiento')
    search_fields = (
        'lote__codigo_lote',
        'lote__galpon__numero_galpon',
        'lote__galpon__granja__nombre',
        'observaciones',
        'registrado_por__username',
        'registrado_por__first_name',
        'registrado_por__last_name',
        'tipo_seguimiento',
        'causa_mortalidad'
    )
    date_hierarchy = 'fecha_seguimiento'
    autocomplete_fields = ['lote', 'registrado_por']
    inlines = [SeguimientoEngordeInline]
    
    def get_readonly_fields(self, request, obj=None):
        # Make tipo_seguimiento read-only if the object already exists
        if obj:  # editing an existing object
            return ['tipo_seguimiento'] + list(self.readonly_fields)
        return self.readonly_fields
        
    def get_fieldsets(self, request, obj=None):
        fieldsets = super().get_fieldsets(request, obj)
        # If it's a new object, we'll set tipo_seguimiento automatically
        if not obj and 'tipo_seguimiento' in fieldsets[0][1]['fields'][1]:
            # Remove tipo_seguimiento from the form since we'll set it automatically
            fieldsets[0][1]['fields'] = [f for f in fieldsets[0][1]['fields'] if f != 'tipo_seguimiento']
        return fieldsets
    fieldsets = (
        (None, {
            'fields': (('lote', 'fecha_seguimiento', 'registrado_por'), 'tipo_seguimiento')
        }),
        ('Producción de Huevos', {
            'fields': (('huevos_totales', 'huevos_rotos', 'huevos_sucios'),),
            'classes': ('produccion-fields',),
            'description': 'Datos relevantes para lotes de producción de huevos'
        }),
        ('Peso y Alimentación', {
            'fields': (('peso_promedio_ave', 'consumo_alimento_kg', 'consumo_agua_litros'),),
        }),
        ('Ambiente y Condiciones', {
            'fields': (('temperatura_min', 'temperatura_max', 'humedad'),),
            'classes': ('collapse',)
        }),
        ('Mortalidad', {
            'fields': (('mortalidad', 'causa_mortalidad'),),
        }),
        ('Observaciones', {
            'fields': ('observaciones',),
            'classes': ('collapse',)
        }),
    )
    
    class Media:
        js = ('js/admin_seguimiento_diario.js',)
        css = {
            'all': ('css/admin_seguimiento_diario.css',)
        }
    
    def get_inlines(self, request, obj=None):
        if obj and obj.tipo_seguimiento == 'engorde':
            return [SeguimientoEngordeInline]
        return []
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser or request.user.groups.filter(name='Supervisor').exists():
            return qs
        return qs.filter(registrado_por=request.user)
    
    def save_model(self, request, obj, form, change):
        if not obj.pk:  # Solo si es un nuevo registro
            obj.registrado_por = request.user
        super().save_model(request, obj, form, change)

class SeguimientoEngordeAdmin(admin.ModelAdmin):
    list_display = (
        'get_lote', 
        'get_fecha', 
        'ganancia_diaria_peso', 
        'conversion_alimenticia', 
        'eficiencia_energetica_display', 
        'eficiencia_proteica_display', 
        'relacion_energia_proteina_display', 
        'indice_productividad'
    )
    
    list_filter = (
        'seguimiento_diario__lote__estado',
        'seguimiento_diario__lote__galpon',
        'seguimiento_diario__lote__alimento',
    )
    
    search_fields = ('seguimiento_diario__lote__codigo_lote', 'observaciones_engorde')
    
    readonly_fields = (
        'consumo_energia', 
        'consumo_proteina', 
        'eficiencia_energetica', 
        'eficiencia_proteica', 
        'relacion_energia_proteina'
    )
    
    fieldsets = (
        ('Información Básica', {
            'fields': ('seguimiento_diario', 'ganancia_diaria_peso', 'conversion_alimenticia', 'uniformidad')
        }),
        ('Eficiencia Nutricional', {
            'fields': (
                'consumo_energia', 
                'consumo_proteina', 
                'eficiencia_energetica', 
                'eficiencia_proteica', 
                'relacion_energia_proteina'
            )
        }),
        ('Medidas Corporales', {
            'fields': ('longitud_corporal', 'ancho_pechuga')
        }),
        ('Evaluación de Salud', {
            'fields': ('calidad_plumaje', 'calidad_patas')
        }),
        ('Observaciones', {
            'fields': ('observaciones_engorde',)
        }),
    )
    
    def get_lote(self, obj):
        return obj.seguimiento_diario.lote
    get_lote.short_description = 'Lote'
    get_lote.admin_order_field = 'seguimiento_diario__lote__codigo_lote'
    
    def get_fecha(self, obj):
        return obj.seguimiento_diario.fecha_seguimiento
    get_fecha.short_description = 'Fecha'
    get_fecha.admin_order_field = 'seguimiento_diario__fecha_seguimiento'
    
    def eficiencia_energetica_display(self, obj):
        if obj.eficiencia_energetica is not None:
            return f"{obj.eficiencia_energetica:.2f}"
        return "N/A"
    eficiencia_energetica_display.short_description = "Eficiencia Energética (kcal/g)"
    
    def eficiencia_proteica_display(self, obj):
        if obj.eficiencia_proteica is not None:
            return f"{obj.eficiencia_proteica:.2f}"
        return "N/A"
    eficiencia_proteica_display.short_description = "Eficiencia Proteica (g/g)"
    
    def relacion_energia_proteina_display(self, obj):
        if obj.relacion_energia_proteina is not None:
            return f"{obj.relacion_energia_proteina:.2f}"
        return "N/A"
    relacion_energia_proteina_display.short_description = "Relación E/P"

class MortalidadDiariaAdmin(admin.ModelAdmin):
    list_display = ('lote', 'fecha', 'cantidad_muertes', 'causa')
    list_filter = ('lote__galpon__granja', 'lote', 'fecha')
    search_fields = ('lote__codigo_lote', 'causa')
    date_hierarchy = 'fecha'
    autocomplete_fields = ['lote']

class MortalidadSemanalAdmin(admin.ModelAdmin):
    list_display = ('lote', 'semana', 'anio', 'total_muertes', 'porcentaje_mortalidad')
    list_filter = ('lote__galpon__granja', 'lote', 'anio', 'semana')
    search_fields = ('lote__codigo_lote',)
    autocomplete_fields = ['lote']

class ConsumoEnergiaAdmin(admin.ModelAdmin):
    list_display = ('get_galpon_display', 'fecha_registro', 'hora_inicio', 'hora_fin', 'consumo_kwh', 'temperatura_ambiente_display', 'humedad_relativa_display', 'get_registrado_por_display')
    list_filter = ('galpon__granja', 'galpon', 'fecha_registro')
    search_fields = ('galpon__numero_galpon', 'observaciones')
    date_hierarchy = 'fecha_registro'
    list_per_page = 20
    raw_id_fields = ('galpon', 'registrado_por')  # Changed from autocomplete_fields
    readonly_fields = ('get_galpon_display', 'get_registrado_por_display')
    
    fieldsets = (
        (None, {
            'fields': (('galpon', 'get_galpon_display'), 'fecha_registro', 'get_registrado_por_display')
        }),
        ('Horario', {
            'fields': (('hora_inicio', 'hora_fin'),)
        }),
        ('Consumo', {
            'fields': ('consumo_kwh',)
        }),
        ('Condiciones', {
            'fields': (('temperatura_ambiente', 'humedad_relativa'),),
            'classes': ('collapse',)
        }),
        ('Observaciones', {
            'fields': ('observaciones',),
            'classes': ('collapse',)
        }),
    )
    
    def get_galpon_display(self, obj):
        return str(obj.galpon) if obj.galpon else ""
    get_galpon_display.short_description = "Galpón (Vista previa)"
    
    def get_registrado_por_display(self, obj):
        return str(obj.registrado_por) if obj.registrado_por else ""
    get_registrado_por_display.short_description = "Registrado por (Vista previa)"
    
    def temperatura_ambiente_display(self, obj):
        if obj.temperatura_ambiente is not None:
            return f"{obj.temperatura_ambiente}°C"
        return "-"
    temperatura_ambiente_display.short_description = "Temp. Ambiente"
    
    def humedad_relativa_display(self, obj):
        if obj.humedad_relativa is not None:
            return f"{obj.humedad_relativa}%"
        return "-"
    humedad_relativa_display.short_description = "Humedad"
    
    def save_model(self, request, obj, form, change):
        if not obj.pk:  # Solo si es un nuevo registro
            obj.registrado_por = request.user
        super().save_model(request, obj, form, change)

def register_models():
    try:
        # Get the custom admin site
        admin_site = get_admin_site()
        
        # First unregister any existing registrations to avoid conflicts
        from django.contrib import admin as default_admin
        
        # List of models to register
        models_to_register = [
            (Granja, GranjaAdmin),
            (Galpon, GalponAdmin),
            (Lote, LoteAdmin),
            (SeguimientoDiario, SeguimientoDiarioAdmin),
            (SeguimientoEngorde, SeguimientoEngordeAdmin),
            (MortalidadDiaria, MortalidadDiariaAdmin),
            (MortalidadSemanal, MortalidadSemanalAdmin),
            (ConsumoEnergia, ConsumoEnergiaAdmin)
        ]
        
        # Unregister from default admin if registered there
        for model, _ in models_to_register:
            if default_admin.site.is_registered(model):
                default_admin.site.unregister(model)
        
        # Unregister from custom admin if already registered
        for model, _ in models_to_register:
            if admin_site.is_registered(model):
                admin_site.unregister(model)
        
        # Register models with the custom admin site
        for model, admin_class in models_to_register:
            try:
                admin_site.register(model, admin_class)
                print(f"Registered {model.__name__} with custom admin site")
            except Exception as e:
                print(f"Error registering {model.__name__}: {e}")
                # Fallback to default admin if custom registration fails
                default_admin.site.register(model, admin_class)
                print(f"Registered {model.__name__} with default admin site")
        
        print("Successfully registered all models with admin sites")
        return True
        
    except Exception as e:
        print(f"Error in register_models(): {e}")
        import traceback
        traceback.print_exc()
        return False

# Call the registration function when this module is imported
register_models()

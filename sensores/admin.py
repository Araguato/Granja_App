from django.contrib import admin
from django.utils import timezone
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe
from .models import TipoSensor, Sensor, LecturaSensor, AlertaSensor


@admin.register(TipoSensor)
class TipoSensorAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'unidad_medida', 'rango_min', 'rango_max', 'activo', 'fecha_creacion')
    list_filter = ('activo',)
    search_fields = ('nombre', 'descripcion', 'codigo')
    prepopulated_fields = {'codigo': ('nombre',)}
    readonly_fields = ('fecha_creacion', 'fecha_actualizacion')
    list_editable = ('activo',)
    fieldsets = (
        ('Información Básica', {
            'fields': ('nombre', 'codigo', 'descripcion', 'unidad_medida', 'activo')
        }),
        ('Configuración', {
            'fields': ('rango_min', 'rango_max', 'icono', 'color')
        }),
        ('Auditoría', {
            'fields': ('fecha_creacion', 'fecha_actualizacion'),
            'classes': ('collapse',)
        }),
    )


class LecturaSensorInline(admin.TabularInline):
    model = LecturaSensor
    extra = 0
    readonly_fields = ('fecha_hora_lectura', 'valor', 'estado_sensor', 'bateria', 'senal')
    can_delete = False
    show_change_link = True
    max_num = 5  # Mostrar solo las últimas 5 lecturas
    
    def has_add_permission(self, request, obj=None):
        return False


@admin.register(Sensor)
class SensorAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'tipo_display', 'galpon_display', 'ubicacion', 'estado', 'activo', 'fecha_instalacion')
    list_filter = ('estado', 'activo', 'tipo', 'galpon')
    search_fields = ('nombre', 'codigo', 'ubicacion', 'observaciones')
    list_editable = ('estado', 'activo')
    readonly_fields = ('fecha_creacion', 'fecha_actualizacion', 'ultima_lectura', 'estado_icono')
    inlines = [LecturaSensorInline]
    fieldsets = (
        ('Información Básica', {
            'fields': ('codigo', 'nombre', 'tipo', 'galpon', 'ubicacion')
        }),
        ('Estado y Mantenimiento', {
            'fields': ('estado', 'activo', 'fecha_instalacion', 'ultima_calibracion', 'observaciones')
        }),
        ('Última Lectura', {
            'fields': ('ultima_lectura', 'estado_icono'),
            'classes': ('collapse',)
        }),
        ('Auditoría', {
            'fields': ('fecha_creacion', 'fecha_actualizacion'),
            'classes': ('collapse',)
        }),
    )

    def tipo_display(self, obj):
        return f"{obj.tipo.nombre} ({obj.tipo.unidad_medida})"
    tipo_display.short_description = 'Tipo'
    tipo_display.admin_order_field = 'tipo__nombre'

    def galpon_display(self, obj):
        if obj.galpon:
            url = reverse('admin:produccion_galpon_change', args=[obj.galpon.id])
            return mark_safe(f'<a href="{url}">{obj.galpon}</a>')
        return "-"
    galpon_display.short_description = 'Galpón'
    galpon_display.allow_tags = True

    def ultima_lectura(self, obj):
        ultima = obj.lecturas.order_by('-fecha_hora_lectura').first()
        if ultima:
            url = reverse('admin:sensores_lecturasensor_change', args=[ultima.id])
            return mark_safe(f'<a href="{url}">{ultima.valor} {obj.tipo.unidad_medida} - {ultima.fecha_hora_lectura.strftime("%Y-%m-%d %H:%M")}</a>')
        return "Sin lecturas"
    ultima_lectura.short_description = 'Última Lectura'
    ultima_lectura.allow_tags = True

    def estado_icono(self, obj):
        if obj.estado == 'ACTIVO':
            return mark_safe('<span style="color: green;"><i class="fas fa-check-circle"></i> Activo</span>')
        elif obj.estado == 'FALLA':
            return mark_safe('<span style="color: red;"><i class="fas fa-exclamation-circle"></i> En Falla</span>')
        elif obj.estado == 'MANTENIMIENTO':
            return mark_safe('<span style="color: orange;"><i class="fas fa-tools"></i> En Mantenimiento</span>')
        return obj.get_estado_display()
    estado_icono.short_description = 'Estado'
    estado_icono.allow_tags = True

    class Media:
        css = {
            'all': ('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css',)
        }


class AlertaSensorInline(admin.TabularInline):
    model = AlertaSensor
    extra = 0
    readonly_fields = ('fecha_creacion', 'tipo', 'mensaje', 'estado')
    can_delete = False
    show_change_link = True
    max_num = 3  # Mostrar solo las últimas 3 alertas

    def has_add_permission(self, request, obj=None):
        return False


@admin.register(LecturaSensor)
class LecturaSensorAdmin(admin.ModelAdmin):
    list_display = ('fecha_hora_lectura', 'sensor_display', 'valor_unidad', 'estado_sensor', 'bateria', 'senal_display')
    list_filter = ('sensor__tipo', 'estado_sensor', 'sensor__galpon')
    search_fields = ('sensor__nombre', 'sensor__codigo', 'metadata')
    readonly_fields = ('fecha_hora_lectura', 'fecha_hora', 'sensor_display', 'valor_unidad', 'estado_sensor', 
                      'bateria', 'senal_display', 'mapa_ubicacion', 'metadata_display')
    date_hierarchy = 'fecha_hora_lectura'
    inlines = [AlertaSensorInline]
    fieldsets = (
        ('Información de la Lectura', {
            'fields': ('sensor_display', 'valor_unidad', 'fecha_hora_lectura', 'fecha_hora', 'estado_sensor')
        }),
        ('Ubicación', {
            'fields': ('mapa_ubicacion', 'latitud', 'longitud'),
            'classes': ('collapse',)
        }),
        ('Estado del Sensor', {
            'fields': ('bateria', 'senal_display'),
            'classes': ('collapse',)
        }),
        ('Metadatos', {
            'fields': ('metadata_display',),
            'classes': ('collapse',)
        }),
    )

    def sensor_display(self, obj):
        url = reverse('admin:sensores_sensor_change', args=[obj.sensor.id])
        return mark_safe(f'<a href="{url}">{obj.sensor}</a>')
    sensor_display.short_description = 'Sensor'
    sensor_display.admin_order_field = 'sensor__nombre'
    sensor_display.allow_tags = True

    def valor_unidad(self, obj):
        return f"{obj.valor} {obj.sensor.tipo.unidad_medida}"
    valor_unidad.short_description = 'Valor'
    valor_unidad.admin_order_field = 'valor'

    def senal_display(self, obj):
        if obj.senal is None:
            return "-"
        if obj.senal >= -70:  # Buena señal
            color = 'green'
            icon = 'signal'
        elif obj.senal >= -85:  # Señal regular
            color = 'orange'
            icon = 'signal'
        else:  # Mala señal
            color = 'red'
            icon = 'signal-slash'
        return mark_safe(f'<span style="color: {color};"><i class="fas fa-{icon}"></i> {obj.senal} dBm</span>')
    senal_display.short_description = 'Señal'
    senal_display.allow_tags = True

    def mapa_ubicacion(self, obj):
        if obj.latitud and obj.longitud:
            url = f"https://www.google.com/maps?q={obj.latitud},{obj.longitud}"
            return mark_safe(f'<a href="{url}" target="_blank"><i class="fas fa-map-marker-alt"></i> Ver en mapa</a>')
        return "Sin ubicación"
    mapa_ubicacion.short_description = 'Ubicación'
    mapa_ubicacion.allow_tags = True

    def metadata_display(self, obj):
        if not obj.metadata:
            return "-"
        items = [f"<strong>{k}:</strong> {v}" for k, v in obj.metadata.items()]
        return mark_safe("<br>".join(items))
    metadata_display.short_description = 'Metadatos'
    metadata_display.allow_tags = True


@admin.register(AlertaSensor)
class AlertaSensorAdmin(admin.ModelAdmin):
    list_display = ('fecha_creacion', 'tipo_display', 'lectura_display', 'estado', 'resuelta_por_display')
    list_filter = ('tipo', 'estado', 'fecha_creacion')
    search_fields = ('mensaje', 'comentarios', 'lectura__sensor__nombre')
    readonly_fields = ('fecha_creacion', 'fecha_actualizacion', 'lectura_display', 'tipo_display', 'estado_display')
    date_hierarchy = 'fecha_creacion'
    actions = ['marcar_como_resueltas']
    fieldsets = (
        ('Información de la Alerta', {
            'fields': ('tipo_display', 'estado_display', 'lectura_display', 'mensaje')
        }),
        ('Resolución', {
            'fields': ('resuelta_por_display', 'fecha_resolucion', 'comentarios')
        }),
        ('Auditoría', {
            'fields': ('fecha_creacion', 'fecha_actualizacion'),
            'classes': ('collapse',)
        }),
    )

    def tipo_display(self, obj):
        icon_map = {
            'CRITICA': ('exclamation-triangle', 'red'),
            'ADVERTENCIA': ('exclamation-circle', 'orange'),
            'INFORMATIVA': ('info-circle', 'blue')
        }
        icon, color = icon_map.get(obj.tipo, ('bell', 'gray'))
        return mark_safe(f'<span style="color: {color};"><i class="fas fa-{icon}"></i> {obj.get_tipo_display()}</span>')
    tipo_display.short_description = 'Tipo'
    tipo_display.allow_tags = True

    def lectura_display(self, obj):
        url = reverse('admin:sensores_lecturasensor_change', args=[obj.lectura.id])
        return mark_safe(f'<a href="{url}">{obj.lectura}</a>')
    lectura_display.short_description = 'Lectura'
    lectura_display.allow_tags = True

    def estado_display(self, obj):
        if obj.estado == 'PENDIENTE':
            return mark_safe('<span style="color: red;"><i class="fas fa-clock"></i> Pendiente</span>')
        elif obj.estado == 'EN_PROCESO':
            return mark_safe('<span style="color: orange;"><i class="fas fa-spinner fa-spin"></i> En Proceso</span>')
        else:
            return mark_safe(f'<span style="color: green;"><i class="fas fa-check"></i> Resuelta ({obj.fecha_resolucion.strftime("%Y-%m-%d %H:%M")})</span>')
    estado_display.short_description = 'Estado'
    estado_display.allow_tags = True

    def resuelta_por_display(self, obj):
        if obj.resuelta_por:
            url = reverse('admin:auth_user_change', args=[obj.resuelta_por.id])
            return mark_safe(f'<a href="{url}">{obj.resuelta_por.get_full_name() or obj.resuelta_por.username}</a>')
        return "-"
    resuelta_por_display.short_description = 'Resuelta por'
    resuelta_por_display.allow_tags = True

    def marcar_como_resueltas(self, request, queryset):
        updated = queryset.filter(estado__in=['PENDIENTE', 'EN_PROCESO']).update(
            estado='RESUELTA',
            resuelta_por=request.user,
            fecha_resolucion=timezone.now()
        )
        self.message_user(request, f"{updated} alertas marcadas como resueltas.")
    marcar_como_resueltas.short_description = "Marcar como resueltas"

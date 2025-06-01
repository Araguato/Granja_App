from django.db import models
from django.conf import settings # Para AUTH_USER_MODEL

# Modelos referenciados de otras apps. Se usan strings para evitar importación circular.
# 'avicola.Empresa', 'avicola.UserProfile', 'inventario.Raza', 'inventario.Alimento'

# Import ConsumoEnergia from the separate file
from .consumo_energia import ConsumoEnergia

__all__ = [
    'Granja', 'Galpon', 'Lote', 'SeguimientoDiario', 
    'MortalidadDiaria', 'MortalidadSemanal', 'SeguimientoEngorde',
    'ConsumoEnergia'
]

class Granja(models.Model):
    ESTADO_CHOICES = [
        ('ACTIVA', 'Activa'),
        ('INACTIVA', 'Inactiva'),
        ('MANTENIMIENTO', 'En Mantenimiento'),
    ]
    empresa = models.ForeignKey('avicola.Empresa', on_delete=models.CASCADE, verbose_name="Empresa Propietaria")
    codigo_granja = models.CharField(max_length=50, unique=True, verbose_name="Código de Granja")
    nombre = models.CharField(max_length=100, verbose_name="Nombre de la Granja")
    direccion = models.TextField(verbose_name="Dirección")
    ubicacion_geografica = models.CharField(max_length=100, blank=True, verbose_name="Ubicación Geográfica")
    telefono = models.CharField(max_length=20, blank=True, verbose_name="Teléfono")
    encargado = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='granjas_encargadas', verbose_name="Encargado Principal")
    capacidad_total_aves = models.PositiveIntegerField(default=0, verbose_name="Capacidad Total de Aves")
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='ACTIVA', verbose_name="Estado de la Granja")

    class Meta:
        verbose_name = "Granja"
        verbose_name_plural = "Granjas"
        ordering = ['nombre']

    def __str__(self):
        return f"{self.nombre} ({self.codigo_granja})"

class Galpon(models.Model):
    TIPO_GALPON_CHOICES = [
        ('CRIA', 'Cría (Engorde)'),
        ('RECRIA', 'Recría (Engorde)'),
        ('POSTURA', 'Postura (Huevos)'),
        ('REPRODUCTOR', 'Reproductor'),
        ('CUARENTENA', 'Cuarentena'),
    ]
    granja = models.ForeignKey(Granja, on_delete=models.CASCADE, related_name='galpones', verbose_name="Granja Asociada")
    numero_galpon = models.CharField(max_length=20, verbose_name="Número o Identificador del Galpón")
    tipo_galpon = models.CharField(max_length=20, choices=TIPO_GALPON_CHOICES, default='POSTURA', verbose_name="Tipo de Galpón")
    capacidad_aves = models.PositiveIntegerField(verbose_name="Capacidad Máxima de Aves")
    area_metros_cuadrados = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True, verbose_name="Área (m²)")
    responsable = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='galpones_responsable', verbose_name="Responsable del Galpón")
    
    # Campos de auditoría
    fecha_creacion = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de Creación')
    fecha_actualizacion = models.DateTimeField(auto_now=True, verbose_name='Última Actualización')
    creado_por = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, 
                                 related_name='galpones_creados', verbose_name='Creado Por')
    actualizado_por = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True,
                                      related_name='galpones_actualizados', verbose_name='Actualizado Por')

    class Meta:
        verbose_name = "Galpón"
        verbose_name_plural = "Galpones"
        unique_together = [('granja', 'numero_galpon')]
        ordering = ['granja', 'numero_galpon']

    def __str__(self):
        return f"Galpón {self.numero_galpon} ({self.granja.nombre}) - Tipo: {self.get_tipo_galpon_display()}"

class Lote(models.Model):
    ESTADO_LOTE_CHOICES = [
        ('INICIAL', 'Inicial'),
        ('CRECIMIENTO', 'Crecimiento'),
        ('PRODUCCION', 'Producción'),
        ('FINALIZACION', 'Finalización'),
    ]

    galpon = models.ForeignKey(Galpon, on_delete=models.PROTECT, related_name='lotes', verbose_name="Galpón Asignado")
    raza = models.ForeignKey('inventario.Raza', on_delete=models.PROTECT, verbose_name="Raza de Aves")
    alimento = models.ForeignKey('inventario.Alimento', on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Alimento Base")
    
    fecha_inicio = models.DateField(verbose_name="Fecha de Inicio del Lote")
    fecha_ingreso = models.DateField(verbose_name="Fecha de Ingreso", null=True, blank=True)
    cantidad_inicial_aves = models.PositiveIntegerField(verbose_name="Cantidad Inicial de Aves")
    edad_inicial_semanas = models.PositiveIntegerField(verbose_name="Edad Inicial (Semanas)", default=0)
    edad_semanas = models.PositiveIntegerField(verbose_name="Edad Actual (Semanas)", default=0)
    estado = models.CharField(max_length=20, choices=ESTADO_LOTE_CHOICES, default='INICIAL', verbose_name="Estado del Lote")
    codigo_lote = models.CharField(max_length=50, unique=True, verbose_name="Código de Lote")
    
    class Meta:
        verbose_name = "Lote"
        verbose_name_plural = "Lotes"
        ordering = ['-fecha_ingreso', 'codigo_lote']
    
    def __str__(self):
        return f"Lote {self.codigo_lote} - {self.raza.nombre} ({self.get_estado_display()})"
    
    def save(self, *args, **kwargs):
        # Si es un nuevo lote o edad_semanas no tiene valor, usar edad_inicial_semanas
        if not self.pk or not self.edad_semanas:
            self.edad_semanas = self.edad_inicial_semanas
            
        # Si no hay fecha de ingreso, usar fecha de inicio
        if not self.fecha_ingreso:
            self.fecha_ingreso = self.fecha_inicio
            
        super().save(*args, **kwargs)
    
    @property
    def calcular_edad_actual(self):
        """Calcula la edad actual en semanas basada en la fecha de inicio y la edad inicial"""
        from datetime import date
        today = date.today()
        dias_transcurridos = (today - self.fecha_inicio).days
        semanas_transcurridas = dias_transcurridos // 7
        return self.edad_inicial_semanas + semanas_transcurridas

class MortalidadDiaria(models.Model):
    lote = models.ForeignKey(Lote, on_delete=models.CASCADE, related_name='mortalidades_diarias', verbose_name="Lote")
    fecha = models.DateField(verbose_name="Fecha")
    cantidad_muertes = models.PositiveIntegerField(verbose_name="Número de Aves Muertas")
    causa = models.CharField(max_length=200, blank=True, verbose_name="Causa de la Mortalidad")
    observaciones = models.TextField(blank=True, verbose_name="Observaciones")

    class Meta:
        verbose_name = "Mortalidad Diaria"
        verbose_name_plural = "Mortalidades Diarias"
        unique_together = [('lote', 'fecha')]
        ordering = ['-fecha']

    def __str__(self):
        return f"Mortalidad {self.lote.codigo_lote} - {self.fecha} ({self.cantidad_muertes} aves)"

class SeguimientoDiario(models.Model):
    TIPO_SEGUIMIENTO_CHOICES = [
        ('PRODUCCION', 'Producción de Huevos'),
        ('ENGORDE', 'Engorde de Pollos'),
        ('MIXTO', 'Producción y Engorde'),
    ]
    
    lote = models.ForeignKey(Lote, on_delete=models.CASCADE, related_name='seguimientos_diarios', verbose_name="Lote")
    fecha_seguimiento = models.DateField(verbose_name="Fecha de Seguimiento")
    registrado_por = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Registrado Por")
    tipo_seguimiento = models.CharField(max_length=20, choices=TIPO_SEGUIMIENTO_CHOICES, default='PRODUCCION', verbose_name="Tipo de Seguimiento")
    
    # Producción de Huevos (relevante para tipo PRODUCCION y MIXTO)
    huevos_totales = models.PositiveIntegerField(default=0, verbose_name="Huevos Totales")
    huevos_rotos = models.PositiveIntegerField(default=0, verbose_name="Huevos Rotos")
    huevos_sucios = models.PositiveIntegerField(default=0, verbose_name="Huevos Sucios")
    
    # Peso y Alimentación (relevante para todos los tipos)
    peso_promedio_ave = models.DecimalField(max_digits=6, decimal_places=2, verbose_name="Peso Promedio (kg)")
    consumo_alimento_kg = models.DecimalField(max_digits=8, decimal_places=2, verbose_name="Consumo de Alimento (kg)")
    consumo_agua_litros = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True, verbose_name="Consumo de Agua (L)")
    
    # Ambiente y Condiciones (relevante para todos los tipos)
    temperatura_min = models.DecimalField(max_digits=4, decimal_places=1, null=True, blank=True, verbose_name="Temperatura Mínima (°C)")
    temperatura_max = models.DecimalField(max_digits=4, decimal_places=1, null=True, blank=True, verbose_name="Temperatura Máxima (°C)")
    humedad = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, verbose_name="Humedad (%)")
    
    # Mortalidad (relevante para todos los tipos)
    mortalidad = models.PositiveIntegerField(default=0, verbose_name="Mortalidad del Día")
    causa_mortalidad = models.CharField(max_length=200, blank=True, verbose_name="Causa de Mortalidad")
    
    # Observaciones generales
    observaciones = models.TextField(blank=True, verbose_name="Observaciones")
    
    class Meta:
        verbose_name = "Seguimiento Diario"
        verbose_name_plural = "Seguimientos Diarios"
        unique_together = [('lote', 'fecha_seguimiento')]
        ordering = ['-fecha_seguimiento']
    
    def __str__(self):
        return f"Seguimiento {self.lote.codigo_lote} - {self.fecha_seguimiento} ({self.get_tipo_seguimiento_display()})"
    
    def aves_presentes(self):
        # Calcular aves presentes (cantidad inicial - muertes acumuladas)
        try:
            muertes_acumuladas = self.lote.mortalidades_diarias.filter(
                fecha__lte=self.fecha_seguimiento
            ).aggregate(total=models.Sum('cantidad_muertes'))['total'] or 0
            
            return self.lote.cantidad_inicial_aves - muertes_acumuladas
        except (AttributeError, ValueError):
            # En caso de error, devolver la cantidad inicial
            return self.lote.cantidad_inicial_aves
    
    def mortalidad_del_dia(self):
        # Devolver la mortalidad registrada para este día
        return self.mortalidad
    
    def huevos_total_dia(self):
        return self.huevos_totales
    
    def calcular_conversion_alimenticia(self):
        """Calcula la conversión alimenticia (kg alimento / kg peso ganado)"""
        if self.tipo_seguimiento == 'PRODUCCION':
            return None
            
        # Buscar el seguimiento anterior para calcular la ganancia de peso
        seguimiento_anterior = SeguimientoDiario.objects.filter(
            lote=self.lote,
            fecha_seguimiento__lt=self.fecha_seguimiento
        ).order_by('-fecha_seguimiento').first()
        
        if not seguimiento_anterior:
            return None
            
        # Calcular ganancia de peso
        peso_anterior = float(seguimiento_anterior.peso_promedio_ave)
        peso_actual = float(self.peso_promedio_ave)
        ganancia_peso = peso_actual - peso_anterior
        
        if ganancia_peso <= 0:
            return None
            
        # Calcular conversión alimenticia
        aves_presentes = self.aves_presentes()
        if aves_presentes <= 0:
            return None
            
        consumo_total = self.consumo_alimento_kg
        ganancia_total = ganancia_peso * aves_presentes
        
        if ganancia_total <= 0:
            return None
            
        return consumo_total / ganancia_total


class MortalidadSemanal(models.Model):
    lote = models.ForeignKey(Lote, on_delete=models.CASCADE, related_name='mortalidades_semanales', verbose_name="Lote")
    semana = models.PositiveIntegerField(verbose_name="Número de Semana")
    anio = models.PositiveIntegerField(verbose_name="Año")
    total_muertes = models.PositiveIntegerField(verbose_name="Total de Muertes en la Semana")
    porcentaje_mortalidad = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="Porcentaje de Mortalidad")
    
    class Meta:
        verbose_name = "Mortalidad Semanal"
        verbose_name_plural = "Mortalidades Semanales"
        unique_together = [('lote', 'semana', 'anio')]
        ordering = ['-anio', '-semana']
    
    def __str__(self):
        return f"Mortalidad Semanal {self.lote.id} - Semana {self.semana}/{self.anio}: {self.total_muertes} aves"

class SeguimientoEngorde(models.Model):
    """Modelo para el seguimiento específico de engorde de pollos"""
    UNIFORMIDAD_CHOICES = [
        ('EXCELENTE', 'Excelente (>90%)'),
        ('BUENA', 'Buena (80-90%)'),
        ('REGULAR', 'Regular (70-80%)'),
        ('DEFICIENTE', 'Deficiente (<70%)'),
    ]
    
    seguimiento_diario = models.OneToOneField(SeguimientoDiario, on_delete=models.CASCADE, related_name='detalle_engorde', verbose_name="Seguimiento Diario")
    ganancia_diaria_peso = models.DecimalField(max_digits=6, decimal_places=2, verbose_name="Ganancia Diaria de Peso (g)")
    conversion_alimenticia = models.DecimalField(max_digits=4, decimal_places=2, verbose_name="Conversión Alimenticia")
    uniformidad = models.CharField(max_length=20, choices=UNIFORMIDAD_CHOICES, verbose_name="Uniformidad del Lote")
    indice_productividad = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True, verbose_name="Índice de Productividad")
    
    # Eficiencia energética y nutricional
    eficiencia_energetica = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True, verbose_name="Eficiencia Energética (kcal/g)")
    eficiencia_proteica = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True, verbose_name="Eficiencia Proteica (g/g)")
    consumo_proteina = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True, verbose_name="Consumo de Proteína (g)")
    consumo_energia = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True, verbose_name="Consumo de Energía (kcal)")
    relacion_energia_proteina = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True, verbose_name="Relación Energía/Proteína")
    
    # Medidas corporales
    longitud_corporal = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, verbose_name="Longitud Corporal (cm)")
    ancho_pechuga = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, verbose_name="Ancho de Pechuga (cm)")
    
    # Evaluación de salud
    calidad_plumaje = models.PositiveSmallIntegerField(null=True, blank=True, verbose_name="Calidad del Plumaje (1-5)")
    calidad_patas = models.PositiveSmallIntegerField(null=True, blank=True, verbose_name="Calidad de Patas (1-5)")
    
    # Observaciones específicas de engorde
    observaciones_engorde = models.TextField(blank=True, verbose_name="Observaciones de Engorde")
    
    class Meta:
        verbose_name = "Seguimiento de Engorde"
        verbose_name_plural = "Seguimientos de Engorde"
    
    def __str__(self):
        return f"Engorde {self.seguimiento_diario.lote.codigo_lote} - {self.seguimiento_diario.fecha_seguimiento}"
    
    def save(self, *args, **kwargs):
        # Asegurar que el seguimiento diario sea de tipo ENGORDE o MIXTO
        if self.seguimiento_diario.tipo_seguimiento not in ['ENGORDE', 'MIXTO']:
            raise ValueError("El seguimiento diario debe ser de tipo ENGORDE o MIXTO")
        
        # Calcular índice de productividad si no está establecido
        if not self.indice_productividad:
            # Fórmula: (Peso promedio (kg) * % Supervivencia) / (Edad en días * Conversión alimenticia) * 100
            lote = self.seguimiento_diario.lote
            edad_dias = (self.seguimiento_diario.fecha_seguimiento - lote.fecha_inicio).days
            
            if edad_dias > 0 and self.conversion_alimenticia > 0:
                aves_iniciales = lote.cantidad_inicial_aves  # Corregido el nombre del campo
                aves_actuales = self.seguimiento_diario.aves_presentes()
                supervivencia = (aves_actuales / aves_iniciales * 100) if aves_iniciales > 0 else 0
                
                self.indice_productividad = (self.seguimiento_diario.peso_promedio_ave * supervivencia) / (edad_dias * self.conversion_alimenticia) * 100
        
        # Calcular eficiencia energética y proteica si hay datos de alimento
        if self.seguimiento_diario.lote.alimento and self.seguimiento_diario.consumo_alimento_kg > 0:
            alimento = self.seguimiento_diario.lote.alimento
            consumo_kg = self.seguimiento_diario.consumo_alimento_kg
            ganancia_kg = self.ganancia_diaria_peso / 1000  # Convertir de g a kg
            
            # Si el alimento tiene datos nutricionales
            if hasattr(alimento, 'energia_metabolizable') and alimento.energia_metabolizable:
                # Consumo de energía = kg alimento * kcal/kg
                self.consumo_energia = consumo_kg * alimento.energia_metabolizable
                # Eficiencia energética = kcal consumidas / ganancia de peso (g)
                if self.ganancia_diaria_peso > 0:
                    self.eficiencia_energetica = self.consumo_energia / self.ganancia_diaria_peso
            
            if hasattr(alimento, 'contenido_proteina') and alimento.contenido_proteina:
                # Consumo de proteína = kg alimento * % proteína * 1000 (para convertir a g)
                self.consumo_proteina = consumo_kg * alimento.contenido_proteina * 10
                # Eficiencia proteica = g proteína consumida / ganancia de peso (g)
                if self.ganancia_diaria_peso > 0:
                    self.eficiencia_proteica = self.consumo_proteina / self.ganancia_diaria_peso
            
            # Relación energía/proteína
            if self.consumo_proteina and self.consumo_proteina > 0 and self.consumo_energia:
                self.relacion_energia_proteina = self.consumo_energia / self.consumo_proteina
        
        super().save(*args, **kwargs)
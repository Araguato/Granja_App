from django.db import models
from django.conf import settings  # Para AUTH_USER_MODEL
from django.core.validators import MinValueValidator

class Proveedor(models.Model):
    rif = models.CharField(max_length=20, unique=True, verbose_name="RIF/CI")
    nombre = models.CharField(max_length=150, verbose_name="Nombre o Razón Social")
    contacto_principal = models.CharField(max_length=100, blank=True, verbose_name="Persona de Contacto")
    telefono = models.CharField(max_length=30, blank=True, verbose_name="Teléfono")
    email = models.EmailField(max_length=100, blank=True, verbose_name="Correo Electrónico")
    direccion = models.TextField(blank=True, verbose_name="Dirección")

    class Meta:
        verbose_name = "Proveedor"
        verbose_name_plural = "Proveedores"
        ordering = ['nombre']

    def __str__(self):
        return f"{self.nombre} ({self.rif})"

class Raza(models.Model):
    TIPO_RAZA_CHOICES = [
        ('PONEDORA', 'Ponedora'),
        ('ENGORDE', 'Engorde'),
        ('DOBLE_PROPOSITO', 'Doble Propósito'),
    ]
    nombre = models.CharField(max_length=100, unique=True, verbose_name="Nombre de la Raza")
    tipo_raza = models.CharField(max_length=20, choices=TIPO_RAZA_CHOICES, verbose_name="Tipo de Raza")
    descripcion = models.TextField(blank=True, verbose_name="Descripción")

    class Meta:
        verbose_name = "Raza"
        verbose_name_plural = "Razas"
        ordering = ['nombre']

    def __str__(self):
        return f"{self.nombre} ({self.get_tipo_raza_display()})"

class Alimento(models.Model):
    ETAPA_CHOICES = [
        ('INICIADOR', 'Iniciador (0-3 semanas)'),
        ('CRECIMIENTO', 'Crecimiento (3-6 semanas)'),
        ('DESARROLLO', 'Desarrollo (6-12 semanas)'),
        ('PREPOSTURA', 'Pre-postura (12-18 semanas)'),
        ('POSTURA_FASE1', 'Postura Fase 1 (18-40 semanas)'),
        ('POSTURA_FASE2', 'Postura Fase 2 (40+ semanas)'),
        ('ENGORDE_INICIAL', 'Engorde Inicial (0-10 días)'),
        ('ENGORDE_CRECIMIENTO', 'Engorde Crecimiento (11-22 días)'),
        ('ENGORDE_TERMINACION', 'Engorde Terminación (22+ días)'),
    ]
    
    codigo = models.CharField(max_length=20, unique=True, null=True, blank=True, verbose_name="Código")
    nombre = models.CharField(max_length=100, verbose_name="Nombre del Alimento")
    descripcion = models.TextField(blank=True, verbose_name="Descripción")
    etapa = models.CharField(max_length=20, choices=ETAPA_CHOICES, verbose_name="Etapa")
    proteina_porcentaje = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="Proteína (%)", validators=[MinValueValidator(0)])
    energia_metabolizable_kcal_kg = models.PositiveIntegerField(verbose_name="Energía Metabolizable (Kcal/kg)")
    stock_kg = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="Stock (kg)")
    precio_kg = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Precio por kg")
    proveedor = models.ForeignKey(Proveedor, on_delete=models.SET_NULL, null=True, blank=True, related_name='alimentos', verbose_name="Proveedor")
    fecha_vencimiento = models.DateField(null=True, blank=True, verbose_name="Fecha de Vencimiento")
    lote_fabricante = models.CharField(max_length=50, blank=True, verbose_name="Lote del Fabricante")
    fecha_ingreso = models.DateField(auto_now_add=True, verbose_name="Fecha de Ingreso")
    activo = models.BooleanField(default=True, verbose_name="Activo")

    class Meta:
        verbose_name = "Alimento"
        verbose_name_plural = "Alimentos"
        ordering = ['nombre', 'etapa']

    def __str__(self):
        return f"{self.nombre} - {self.get_etapa_display()}"

class Vacuna(models.Model):
    proveedor = models.ForeignKey(Proveedor, on_delete=models.SET_NULL, null=True, blank=True, related_name='vacunas_suministradas', verbose_name="Proveedor")
    nombre_comercial = models.CharField(max_length=100, verbose_name="Nombre Comercial")
    principio_activo = models.CharField(max_length=150, verbose_name="Principio Activo / Enfermedad que previene")
    lote_fabricante = models.CharField(max_length=50, blank=True, verbose_name="Lote del Fabricante")
    fecha_vencimiento = models.DateField(null=True, blank=True, verbose_name="Fecha de Vencimiento")
    stock_ml = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="Stock (ml)")
    precio_ml = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Precio por ml")
    descripcion = models.TextField(blank=True, verbose_name="Descripción")
    fecha_ingreso = models.DateField(auto_now_add=True, verbose_name="Fecha de Ingreso")
    activo = models.BooleanField(default=True, verbose_name="Activo")

    class Meta:
        verbose_name = "Vacuna"
        verbose_name_plural = "Vacunas"
        ordering = ['nombre_comercial']

    def __str__(self):
        return f"{self.nombre_comercial} (Lote: {self.lote_fabricante or 'N/A'})"

class ConsumoAlimento(models.Model):
    """Registro de consumo de alimento por lote"""
    alimento = models.ForeignKey(Alimento, on_delete=models.PROTECT, related_name='consumos', verbose_name="Alimento")
    lote_aves = models.ForeignKey('produccion.Lote', on_delete=models.CASCADE, related_name='consumos_alimento', verbose_name="Lote de Aves")
    cantidad_kg = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Cantidad (kg)")
    fecha_consumo = models.DateField(verbose_name="Fecha de Consumo")
    registrado_por = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, verbose_name="Registrado por")
    fecha_registro = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Registro")
    observaciones = models.TextField(blank=True, verbose_name="Observaciones")

    class Meta:
        verbose_name = "Consumo de Alimento"
        verbose_name_plural = "Consumos de Alimento"
        ordering = ['-fecha_consumo', '-fecha_registro']

    def __str__(self):
        return f"{self.cantidad_kg}kg de {self.alimento} - {self.lote_aves} - {self.fecha_consumo}"

class AplicacionVacuna(models.Model):
    """Registro de aplicación de vacunas a lotes"""
    vacuna = models.ForeignKey(Vacuna, on_delete=models.PROTECT, related_name='aplicaciones', verbose_name="Vacuna")
    lote_aves = models.ForeignKey('produccion.Lote', on_delete=models.CASCADE, related_name='aplicaciones_vacuna', verbose_name="Lote de Aves")
    fecha_aplicacion = models.DateField(verbose_name="Fecha de Aplicación")
    dosis_ml = models.DecimalField(max_digits=6, decimal_places=2, verbose_name="Dosis Aplicada (ml)")
    aplicada_por = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, verbose_name="Aplicada por")
    fecha_registro = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Registro")
    observaciones = models.TextField(blank=True, verbose_name="Observaciones")
    lote_vacuna = models.CharField(max_length=50, blank=True, verbose_name="Lote de la Vacuna")
    proxima_aplicacion = models.DateField(null=True, blank=True, verbose_name="Próxima Aplicación")
    edad_aplicacion_semanas = models.PositiveIntegerField(null=True, blank=True, verbose_name="Edad en Aplicación (semanas)")
    via_aplicacion = models.CharField(max_length=50, blank=True, verbose_name="Vía de Aplicación")
    
    class Meta:
        verbose_name = "Aplicación de Vacuna"
        verbose_name_plural = "Aplicaciones de Vacuna"
        ordering = ['-fecha_aplicacion', '-fecha_registro']

    def __str__(self):
        return f"{self.vacuna} - {self.lote_aves} - {self.fecha_aplicacion}"

class Insumo(models.Model):
    TIPO_INSUMO_CHOICES = [
        ('MEDICAMENTO', 'Medicamento'),
        ('EQUIPO', 'Equipo'),
        ('LIMPIEZA', 'Producto de Limpieza/Desinfección'),
        ('OTRO', 'Otro'),
    ]
    nombre = models.CharField(max_length=100, verbose_name="Nombre del Insumo")
    descripcion = models.TextField(blank=True, verbose_name="Descripción")
    tipo_insumo = models.CharField(max_length=20, choices=TIPO_INSUMO_CHOICES, verbose_name="Tipo de Insumo")
    proveedor = models.ForeignKey(Proveedor, on_delete=models.SET_NULL, null=True, blank=True, related_name='insumos_suministrados', verbose_name="Proveedor")
    stock = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="Cantidad en Stock")
    unidad_medida = models.CharField(max_length=20, verbose_name="Unidad de Medida")
    stock_minimo = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="Stock Mínimo")
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Precio Unitario")
    fecha_ingreso = models.DateField(auto_now_add=True, verbose_name="Fecha de Ingreso")
    fecha_vencimiento = models.DateField(null=True, blank=True, verbose_name="Fecha de Vencimiento")
    lote = models.CharField(max_length=50, blank=True, verbose_name="Lote")
    activo = models.BooleanField(default=True, verbose_name="Activo")

    class Meta:
        verbose_name = "Insumo"
        verbose_name_plural = "Insumos"
        ordering = ['nombre']

    def __str__(self):
        return f"{self.nombre} ({self.get_tipo_insumo_display()})"

class GuiaDesempenoRaza(models.Model):
    raza = models.ForeignKey(Raza, on_delete=models.CASCADE, related_name='guias_desempeno', verbose_name="Raza")
    dia_edad = models.PositiveIntegerField(verbose_name="Día de Edad")
    peso_corporal_ideal_gr = models.DecimalField(max_digits=8, decimal_places=2, verbose_name="Peso Corporal Ideal (gr)")
    consumo_alimento_diario_ideal_gr_ave = models.DecimalField(max_digits=8, decimal_places=2, verbose_name="Consumo Diario Ideal (gr/ave)")
    consumo_alimento_acumulado_ideal_gr_ave = models.DecimalField(max_digits=8, decimal_places=2, verbose_name="Consumo Alimento Acumulado Ideal (g/ave)")
    conversion_alimenticia_ideal = models.DecimalField(max_digits=5, decimal_places=3, verbose_name="Conversión Alimenticia Ideal")
    mortalidad_acumulada_ideal_porc = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="Mortalidad Acumulada Ideal (%)")
    ganancia_peso_diaria_ideal_gr = models.DecimalField(max_digits=6, decimal_places=2, verbose_name="Ganancia Peso Diaria Ideal (g)")
    consumo_agua_diario_ideal_ml_ave = models.DecimalField(max_digits=7, decimal_places=2, verbose_name="Consumo Agua Diario Ideal (ml/ave)")
    viabilidad_ideal_porc = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="Viabilidad Ideal (%)")
    epef_ideal = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True, verbose_name="EPEF Ideal (Índice Europeo de Eficiencia Productiva)")
    ie_ideal = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True, verbose_name="IE Ideal (Índice de Eficiencia Energética)")

    class Meta:
        verbose_name = "Guía de Desempeño por Raza y Día"
        verbose_name_plural = "Guías de Desempeño por Raza y Día"
        unique_together = ('raza', 'dia_edad')
        ordering = ['raza', 'dia_edad']

    def __str__(self):
        return f"{self.raza} - Día {self.dia_edad}"

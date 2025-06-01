from django.db import models
from django.conf import settings # Para AUTH_USER_MODEL si se usa en el futuro
# from produccion.models import Lote # No directamente, pero sí para InventarioHuevos si se relaciona con Lote
# from avicola.models import UserProfile # Para el vendedor o registrador de la venta

class Cliente(models.Model):
    rif_cedula = models.CharField(max_length=20, unique=True, verbose_name="RIF/Cédula")
    nombre_razon_social = models.CharField(max_length=150, verbose_name="Nombre o Razón Social")
    contacto_principal = models.CharField(max_length=100, blank=True, verbose_name="Persona de Contacto")
    telefono_principal = models.CharField(max_length=30, verbose_name="Teléfono Principal")
    telefono_secundario = models.CharField(max_length=30, blank=True, verbose_name="Teléfono Secundario")
    email = models.EmailField(max_length=100, blank=True, verbose_name="Correo Electrónico")
    direccion_fiscal = models.TextField(verbose_name="Dirección Fiscal")
    # direccion_envio = models.TextField(blank=True, verbose_name="Dirección de Envío (si difiere)")
    # tipo_cliente = models.CharField(max_length=20, choices=[('MAYORISTA','Mayorista'), ('MINORISTA','Minorista'), ('PARTICULAR','Particular')], blank=True)
    # limite_credito = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name="Límite de Crédito")

    class Meta:
        verbose_name = "Cliente"
        verbose_name_plural = "Clientes"
        ordering = ['nombre_razon_social']

    def __str__(self):
        return f"{self.nombre_razon_social} ({self.rif_cedula})"

class TipoHuevo(models.Model):
    # Basado en el modelo que ya tenías en el respaldo de avicola/models.py
    CLASIFICACION_CHOICES = [
        ('AA', 'AA (Extra Grande > 69g)'),
        ('A', 'A (Grande 60-68g)'),
        ('B', 'B (Mediano 53-59g)'),
        ('C', 'C (Pequeño 45-52g)'),
        ('D', 'D (Cartón < 45g)'), # O Descarte / Industrial
        ('JUMBO', 'Jumbo (>70g)'),
    ]
    clasificacion = models.CharField(max_length=10, choices=CLASIFICACION_CHOICES, unique=True, verbose_name="Clasificación")
    descripcion = models.CharField(max_length=100, blank=True, verbose_name="Descripción (ej: Peso rango)")
    # precio_venta_por_unidad = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name="Precio de Venta por Unidad")
    # precio_venta_por_carton = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name="Precio de Venta por Cartón (30 Und)")


    class Meta:
        verbose_name = "Tipo de Huevo"
        verbose_name_plural = "Tipos de Huevo"
        ordering = ['clasificacion']

    def __str__(self):
        return self.get_clasificacion_display()

class InventarioHuevos(models.Model):
    # Este modelo es para el control de stock de huevos listos para la venta.
    # Se alimenta del SeguimientoDiario y se descuenta con las Ventas.
    tipo_huevo = models.ForeignKey(TipoHuevo, on_delete=models.PROTECT, verbose_name="Tipo de Huevo")
    lote_produccion = models.ForeignKey('produccion.Lote', on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Lote de Producción Origen") # Opcional, para trazabilidad
    fecha_ingreso_inventario = models.DateField(auto_now_add=True, verbose_name="Fecha de Ingreso a Inventario")
    cantidad_disponible = models.PositiveIntegerField(default=0, verbose_name="Cantidad Disponible (unidades)")
    # ubicacion_almacen = models.CharField(max_length=50, blank=True, verbose_name="Ubicación en Almacén")
    # precio_costo_estimado = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name="Precio de Costo Estimado")

    class Meta:
        verbose_name = "Inventario de Huevos"
        verbose_name_plural = "Inventarios de Huevos"
        ordering = ['tipo_huevo', '-fecha_ingreso_inventario']
        # unique_together = [('tipo_huevo', 'lote_produccion', 'fecha_ingreso_inventario')] # Para evitar duplicidad si se usa lote_produccion

    def __str__(self):
        return f"{self.cantidad_disponible} unidades de {self.tipo_huevo.get_clasificacion_display()} (Ingreso: {self.fecha_ingreso_inventario})"

class Venta(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.PROTECT, related_name='ventas', verbose_name="Cliente")
    fecha_venta = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Venta")
    # numero_factura = models.CharField(max_length=50, unique=True, blank=True, null=True, verbose_name="Número de Factura/Control")
    # tipo_documento = models.CharField(max_length=20, choices=[('FACTURA','Factura'), ('NOTA_ENTREGA','Nota de Entrega')], default='NOTA_ENTREGA')
    subtotal = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name="Subtotal")
    impuesto = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name="Impuesto (IVA)")
    total_venta = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name="Total Venta")
    # estado_pago = models.CharField(max_length=20, choices=[('PENDIENTE','Pendiente'), ('PAGADA','Pagada'), ('ABONADA','Abonada')], default='PENDIENTE')
    vendedor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='ventas_realizadas', verbose_name="Vendedor")
    observaciones = models.TextField(blank=True, verbose_name="Observaciones")

    class Meta:
        verbose_name = "Venta"
        verbose_name_plural = "Ventas"
        ordering = ['-fecha_venta']

    def __str__(self):
        return f"Venta a {self.cliente.nombre_razon_social} - {self.fecha_venta.strftime('%Y-%m-%d %H:%M')}"

    # Se necesitará un modelo DetalleVenta para los items
class DetalleVenta(models.Model):
    venta = models.ForeignKey(Venta, related_name='detalles', on_delete=models.CASCADE, verbose_name="Venta")
    tipo_huevo = models.ForeignKey(TipoHuevo, on_delete=models.PROTECT, verbose_name="Tipo de Huevo Vendido")
    inventario_huevo_origen = models.ForeignKey(InventarioHuevos, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Del Inventario") # Para trazabilidad y descuento de stock
    cantidad = models.PositiveIntegerField(verbose_name="Cantidad Vendida (unidades)")
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Precio Unitario")
    subtotal_item = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Subtotal Item")

    class Meta:
        verbose_name = "Detalle de Venta"
        verbose_name_plural = "Detalles de Venta"

    def __str__(self):
        return f"{self.cantidad} x {self.tipo_huevo.get_clasificacion_display()} @ {self.precio_unitario}"

    def save(self, *args, **kwargs):
        self.subtotal_item = self.cantidad * self.precio_unitario
        super().save(*args, **kwargs)
        # Aquí se podría agregar lógica para actualizar el total de la Venta y el InventarioHuevos

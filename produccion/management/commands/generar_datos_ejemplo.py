from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta, date
import random

from avicola.models import Empresa, UserProfile
from inventario.models import Proveedor, Raza, Alimento, Vacuna
from produccion.models import Granja, Galpon, Lote, SeguimientoDiario, SeguimientoEngorde
from ventas.models import Cliente, TipoHuevo, InventarioHuevos, Venta, DetalleVenta

class Command(BaseCommand):
    help = 'Genera datos de ejemplo para la aplicación App_Granja'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Iniciando generación de datos de ejemplo...'))
        
        # Crear usuario administrador si no existe
        if not UserProfile.objects.filter(username='admin').exists():
            admin = UserProfile.objects.create_superuser('admin', 'admin@example.com', 'admin123')
            admin.user_type = 'ADMIN'
            admin.telefono = '0414-1234567'
            admin.save()
            self.stdout.write(self.style.SUCCESS('Usuario administrador creado'))
        else:
            admin = UserProfile.objects.get(username='admin')
            self.stdout.write(self.style.SUCCESS('Usuario administrador ya existe'))
        
        # Crear empresa
        try:
            # Intentar obtener por RIF primero
            empresa = Empresa.objects.get(rif='J-12345678-9')
            self.stdout.write(self.style.SUCCESS('Empresa ya existe (encontrada por RIF)'))
        except Empresa.DoesNotExist:
            try:
                # Intentar obtener por nombre
                empresa = Empresa.objects.get(nombre='Avícola El Paraíso')
                self.stdout.write(self.style.SUCCESS('Empresa ya existe (encontrada por nombre)'))
            except Empresa.DoesNotExist:
                # Crear nueva empresa
                empresa = Empresa.objects.create(
                    nombre='Avícola El Paraíso',
                    rif='J-12345678-9',
                    direccion='Carretera Nacional, Km 5, El Paraíso',
                    telefono='0414-1234567',
                    encargado='Pedro Martínez',
                    pais='Venezuela',
                    moneda='USD'
                )
                self.stdout.write(self.style.SUCCESS('Empresa creada'))
        
        # El usuario ya tiene perfil integrado, no es necesario crear uno separado
        
        # Crear proveedores
        proveedores = [
            ('Alimentos Premium, C.A.', 'J-87654321-0', 'Juan Pérez', '0412-9876543', 'ventas@alimentospremium.com'),
            ('Vacunas y Más, S.A.', 'J-23456789-1', 'María Rodríguez', '0414-5678901', 'info@vacunasymas.com'),
            ('Distribuidora Avícola', 'J-34567890-2', 'Carlos González', '0416-7890123', 'ventas@distribuidoraavicola.com')
        ]
        
        for nombre, rif, contacto, telefono, email in proveedores:
            Proveedor.objects.get_or_create(
                rif=rif,
                defaults={
                    'nombre': nombre,
                    'contacto_principal': contacto,
                    'telefono': telefono,
                    'email': email
                }
            )
        
        self.stdout.write(self.style.SUCCESS('Proveedores creados'))
        
        # Crear razas
        razas = [
            ('Ross 308', 'ENGORDE', 'Raza de engorde de rápido crecimiento'),
            ('Cobb 500', 'ENGORDE', 'Raza de engorde eficiente en conversión alimenticia'),
            ('Hy-Line Brown', 'PONEDORA', 'Raza ponedora de huevos marrones'),
            ('Lohmann LSL', 'PONEDORA', 'Raza ponedora de huevos blancos')
        ]
        
        for nombre, tipo, descripcion in razas:
            Raza.objects.get_or_create(
                nombre=nombre,
                defaults={
                    'tipo_raza': tipo,
                    'descripcion': descripcion
                }
            )
        
        self.stdout.write(self.style.SUCCESS('Razas creadas'))
        
        # Crear alimentos
        proveedor_alimentos = Proveedor.objects.get(nombre='Alimentos Premium, C.A.')
        
        alimentos = [
            ('Iniciador Broiler', 'Alimento para pollos de engorde', 'CONCENTRADO', 'INICIADOR', 23.0, 3100, 5.0, 3.0, 1.0, 0.5, 1.3),
            ('Crecimiento Broiler', 'Alimento para pollos en crecimiento', 'CONCENTRADO', 'CRECIMIENTO', 21.0, 3150, 6.0, 3.5, 0.9, 0.45, 1.2),
            ('Finalizador Broiler', 'Alimento para pollos en etapa final', 'CONCENTRADO', 'ENGORDE_FINALIZADOR', 19.0, 3200, 7.0, 3.2, 0.85, 0.42, 1.1),
            ('Pre-Postura', 'Alimento para gallinas antes de postura', 'CONCENTRADO', 'PREPOSTURA', 18.0, 2900, 4.0, 4.0, 2.5, 0.5, 0.9),
            ('Postura Fase 1', 'Alimento para gallinas en postura inicial', 'CONCENTRADO', 'POSTURA_FASE1', 17.5, 2850, 4.5, 3.8, 3.8, 0.45, 0.85)
        ]
        
        for nombre, descripcion, tipo, etapa, proteina, energia, grasa, fibra, calcio, fosforo, lisina in alimentos:
            Alimento.objects.get_or_create(
                nombre=nombre,
                defaults={
                    'proveedor': proveedor_alimentos,
                    'descripcion': descripcion,
                    'tipo_alimento': tipo,
                    'etapa': etapa,
                    'contenido_proteina': proteina,
                    'energia_metabolizable': energia,
                    'grasa_cruda': grasa,
                    'fibra_cruda': fibra,
                    'calcio': calcio,
                    'fosforo': fosforo,
                    'lisina': lisina
                }
            )
        
        self.stdout.write(self.style.SUCCESS('Alimentos creados'))
        
        # Crear vacunas
        proveedor_vacunas = Proveedor.objects.get(nombre='Vacunas y Más, S.A.')
        
        vacunas = [
            ('Marek-Vac', 'Vacuna contra la enfermedad de Marek', 'Virus vivo', 'VM-123', date.today() + timedelta(days=365)),
            ('Newcastle-Vac', 'Vacuna contra la enfermedad de Newcastle', 'Virus inactivado', 'NV-456', date.today() + timedelta(days=300)),
            ('Bronquitis-Vac', 'Vacuna contra la bronquitis infecciosa', 'Virus vivo', 'BV-789', date.today() + timedelta(days=270))
        ]
        
        for nombre, descripcion, principio, lote, vencimiento in vacunas:
            Vacuna.objects.get_or_create(
                nombre_comercial=nombre,
                defaults={
                    'proveedor': proveedor_vacunas,
                    'descripcion': descripcion,
                    'principio_activo': principio,
                    'lote_fabricante': lote,
                    'fecha_vencimiento': vencimiento
                }
            )
        
        self.stdout.write(self.style.SUCCESS('Vacunas creadas'))
        
        # Crear granja
        granja, created = Granja.objects.get_or_create(
            nombre='Granja El Paraíso',
            defaults={
                'empresa': empresa,
                'direccion': 'Carretera Nacional, Km 5, El Paraíso',
                'capacidad_total': 50000,
                'encargado': 'Pedro Martínez',
                'telefono_contacto': '0414-9876543'
            }
        )
        
        if created:
            self.stdout.write(self.style.SUCCESS('Granja creada'))
        else:
            self.stdout.write(self.style.SUCCESS('Granja ya existe'))
        
        # Crear galpones
        galpones = [
            (1, 'ENGORDE', 10000, 12, 120, 'Galpón de engorde principal'),
            (2, 'ENGORDE', 8000, 10, 100, 'Galpón de engorde secundario'),
            (3, 'CRIA', 5000, 8, 80, 'Galpón de cría'),
            (4, 'POSTURA', 12000, 15, 150, 'Galpón de postura')
        ]
        
        galpon_objects = []
        for numero, tipo, capacidad, ancho, largo, descripcion in galpones:
            galpon, created = Galpon.objects.get_or_create(
                granja=granja,
                numero_galpon=numero,
                defaults={
                    'tipo_galpon': tipo,
                    'capacidad_aves': capacidad,
                    'ancho_metros': ancho,
                    'largo_metros': largo,
                    'descripcion': descripcion
                }
            )
            galpon_objects.append(galpon)
        
        self.stdout.write(self.style.SUCCESS('Galpones creados'))
        
        # Crear lotes
        fecha_actual = timezone.now().date()
        
        # Obtener razas
        raza_engorde_1 = Raza.objects.get(nombre='Ross 308')
        raza_engorde_2 = Raza.objects.get(nombre='Cobb 500')
        raza_ponedora = Raza.objects.get(nombre='Hy-Line Brown')
        
        # Obtener alimentos
        alimento_iniciador = Alimento.objects.get(nombre='Iniciador Broiler')
        alimento_crecimiento = Alimento.objects.get(nombre='Crecimiento Broiler')
        alimento_finalizador = Alimento.objects.get(nombre='Finalizador Broiler')
        
        lotes = [
            ('L-2025-001', galpon_objects[0], raza_engorde_1, fecha_actual - timedelta(days=42), 9500, 'CRECIMIENTO', 6, alimento_crecimiento),
            ('L-2025-002', galpon_objects[1], raza_engorde_2, fecha_actual - timedelta(days=28), 7800, 'CRECIMIENTO', 4, alimento_crecimiento),
            ('L-2025-003', galpon_objects[2], raza_engorde_1, fecha_actual - timedelta(days=14), 4900, 'INICIAL', 2, alimento_iniciador),
            ('L-2025-004', galpon_objects[3], raza_ponedora, fecha_actual - timedelta(days=140), 11500, 'PRODUCCION', 20, None)
        ]
        
        lote_objects = []
        for codigo, galpon, raza, fecha_ingreso, cantidad_inicial, estado, edad, alimento in lotes:
            lote, created = Lote.objects.get_or_create(
                codigo_lote=codigo,
                defaults={
                    'galpon': galpon,
                    'raza': raza,
                    'fecha_ingreso': fecha_ingreso,
                    'cantidad_inicial': cantidad_inicial,
                    'estado': estado,
                    'edad_semanas': edad,
                    'alimento': alimento
                }
            )
            lote_objects.append(lote)
        
        self.stdout.write(self.style.SUCCESS('Lotes creados'))
        
        # Crear seguimientos diarios y de engorde para los lotes de engorde
        for lote in lote_objects[:3]:  # Solo los lotes de engorde
            # Determinar cuántos días de seguimiento generar (desde el ingreso hasta hoy)
            dias_seguimiento = (fecha_actual - lote.fecha_ingreso).days
            
            for dia in range(1, dias_seguimiento + 1):
                fecha_seguimiento = lote.fecha_ingreso + timedelta(days=dia)
                edad_dias = dia
                
                # Calcular peso promedio basado en la edad (simulación simple de crecimiento)
                if lote.raza.nombre == 'Ross 308':
                    peso_base = 42  # Peso inicial en gramos
                    ganancia_diaria = 55  # Ganancia diaria promedio en gramos
                else:  # Cobb 500
                    peso_base = 40
                    ganancia_diaria = 53
                
                peso_promedio = peso_base + (ganancia_diaria * edad_dias)
                
                # Calcular consumo de alimento (aumenta con la edad)
                consumo_por_ave = 0.03 + (0.005 * edad_dias)  # kg por ave
                consumo_total = consumo_por_ave * (lote.cantidad_inicial - random.randint(0, int(lote.cantidad_inicial * 0.02)))
                
                # Calcular mortalidad (pequeña y aleatoria)
                mortalidad = random.randint(0, 5)
                
                # Temperatura y humedad
                temp_min = random.uniform(18, 22)
                temp_max = random.uniform(28, 32)
                humedad = random.uniform(50, 70)
                
                # Crear seguimiento diario
                seguimiento_diario, created = SeguimientoDiario.objects.get_or_create(
                    lote=lote,
                    fecha_seguimiento=fecha_seguimiento,
                    defaults={
                        'tipo_seguimiento': 'ENGORDE',
                        'peso_promedio_ave': peso_promedio,
                        'consumo_alimento_kg': consumo_total,
                        'consumo_agua_litros': consumo_total * 2,
                        'mortalidad': mortalidad,
                        'temperatura_min': temp_min,
                        'temperatura_max': temp_max,
                        'humedad': humedad,
                        'observaciones': f'Seguimiento día {dia}',
                        'registrado_por': admin
                    }
                )
                
                if created and seguimiento_diario.tipo_seguimiento == 'ENGORDE':
                    # Calcular datos de engorde
                    if dia > 1:
                        # Obtener seguimiento anterior para calcular ganancia
                        try:
                            seguimiento_anterior = SeguimientoDiario.objects.get(
                                lote=lote,
                                fecha_seguimiento=fecha_seguimiento - timedelta(days=1)
                            )
                            peso_anterior = seguimiento_anterior.peso_promedio_ave
                            ganancia = peso_promedio - peso_anterior
                        except SeguimientoDiario.DoesNotExist:
                            ganancia = ganancia_diaria
                    else:
                        ganancia = ganancia_diaria
                    
                    # Calcular conversión alimenticia
                    conversion = (consumo_total * 1000) / (ganancia * (lote.cantidad_inicial - mortalidad)) if ganancia > 0 else 0
                    
                    # Obtener valores nutricionales del alimento
                    alimento_actual = lote.alimento
                    if alimento_actual:
                        energia = alimento_actual.energia_metabolizable
                        proteina = alimento_actual.contenido_proteina
                        
                        # Calcular consumo de energía y proteína
                        consumo_energia = consumo_total * energia
                        consumo_proteina = consumo_total * proteina * 10  # Convertir % a g/kg
                        
                        # Calcular eficiencias
                        eficiencia_energetica = consumo_energia / ganancia if ganancia > 0 else 0
                        eficiencia_proteica = consumo_proteina / ganancia if ganancia > 0 else 0
                        relacion_energia_proteina = consumo_energia / consumo_proteina if consumo_proteina > 0 else 0
                    else:
                        consumo_energia = 0
                        consumo_proteina = 0
                        eficiencia_energetica = 0
                        eficiencia_proteica = 0
                        relacion_energia_proteina = 0
                    
                    # Crear seguimiento de engorde
                    SeguimientoEngorde.objects.create(
                        seguimiento_diario=seguimiento_diario,
                        ganancia_diaria_peso=ganancia,
                        conversion_alimenticia=conversion,
                        consumo_energia=consumo_energia,
                        consumo_proteina=consumo_proteina,
                        eficiencia_energetica=eficiencia_energetica,
                        eficiencia_proteica=eficiencia_proteica,
                        relacion_energia_proteina=relacion_energia_proteina
                    )
        
        self.stdout.write(self.style.SUCCESS('Seguimientos diarios y de engorde creados'))
        
        # Crear clientes
        clientes = [
            ('Supermercado El Ahorro', 'J-11223344-5', 'Ana Díaz', '0412-3456789', 'compras@elahorro.com'),
            ('Distribuidora Huevos Frescos', 'J-55667788-9', 'Luis Pérez', '0414-7654321', 'luis@huevosfrescos.com'),
            ('Panadería La Esquina', 'J-99887766-5', 'Roberto Sánchez', '0416-1234567', 'panaderia@laesquina.com')
        ]
        
        for nombre, rif, contacto, telefono, email in clientes:
            Cliente.objects.get_or_create(
                rif=rif,
                defaults={
                    'nombre': nombre,
                    'contacto_principal': contacto,
                    'telefono': telefono,
                    'email': email
                }
            )
        
        self.stdout.write(self.style.SUCCESS('Clientes creados'))
        
        # Crear tipos de huevo
        tipos_huevo = [
            ('AA', 'Extra grande', 73),
            ('A', 'Grande', 63),
            ('B', 'Mediano', 53),
            ('C', 'Pequeño', 43)
        ]
        
        for codigo, descripcion, peso_min in tipos_huevo:
            TipoHuevo.objects.get_or_create(
                codigo=codigo,
                defaults={
                    'nombre': f'Huevo {descripcion}',
                    'descripcion': f'Huevo de gallina {descripcion}',
                    'peso_minimo_gr': peso_min
                }
            )
        
        self.stdout.write(self.style.SUCCESS('Tipos de huevo creados'))
        
        # Crear inventario de huevos
        for tipo_huevo in TipoHuevo.objects.all():
            InventarioHuevos.objects.get_or_create(
                tipo_huevo=tipo_huevo,
                defaults={
                    'cantidad_disponible': random.randint(500, 2000),
                    'ultima_actualizacion': fecha_actual
                }
            )
        
        self.stdout.write(self.style.SUCCESS('Inventario de huevos creado'))
        
        # Crear ventas y detalles de venta
        for i in range(1, 11):  # 10 ventas de ejemplo
            fecha_venta = fecha_actual - timedelta(days=random.randint(1, 30))
            cliente = Cliente.objects.order_by('?').first()
            
            venta, created = Venta.objects.get_or_create(
                numero_factura=f'F-2025-{i:03d}',
                defaults={
                    'cliente': cliente,
                    'fecha_venta': fecha_venta,
                    'forma_pago': random.choice(['EFECTIVO', 'TRANSFERENCIA', 'CREDITO']),
                    'estado': 'PAGADA',
                    'observaciones': f'Venta de ejemplo #{i}'
                }
            )
            
            if created:
                # Crear detalles de venta
                total_venta = 0
                for tipo_huevo in TipoHuevo.objects.all():
                    if random.choice([True, False]):  # 50% de probabilidad de incluir este tipo
                        cantidad = random.randint(10, 100) * 12  # En unidades (múltiplos de docena)
                        precio_unitario = random.uniform(0.1, 0.3)  # Precio por unidad
                        subtotal = cantidad * precio_unitario
                        
                        DetalleVenta.objects.create(
                            venta=venta,
                            tipo_huevo=tipo_huevo,
                            cantidad=cantidad,
                            precio_unitario=precio_unitario,
                            subtotal=subtotal
                        )
                        
                        total_venta += subtotal
                
                # Actualizar total de la venta
                venta.total = total_venta
                venta.save()
        
        self.stdout.write(self.style.SUCCESS('Ventas y detalles de venta creados'))
        
        self.stdout.write(self.style.SUCCESS('¡Generación de datos de ejemplo completada con éxito!'))

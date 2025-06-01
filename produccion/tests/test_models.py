from django.test import TestCase
from django.contrib.auth import get_user_model
from django.utils import timezone
from avicola.models import Empresa
from inventario.models import Raza, Alimento, Proveedor
from produccion.models import Granja, Galpon, Lote, SeguimientoDiario, MortalidadDiaria

User = get_user_model()

class ProduccionModelsTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Create test data that will be used by all test methods
        cls.empresa = Empresa.objects.create(
            nombre="Empresa de Prueba",
            rif="J-123456789",
            direccion="Dirección de prueba"
        )
        
        cls.user = User.objects.create_user(
            username='testuser',
            password='testpass123',
            email='test@example.com'
        )
        
        cls.raza = Raza.objects.create(
            nombre="Híbrido de Engorde",
            tipo_raza="ENGORDE",
            descripcion="Raza para engorde"
        )
        
        # Create Proveedor first since it's required for Alimento
        cls.proveedor = Proveedor.objects.create(
            rif="J-123456789",
            nombre="Proveedor de Prueba",
            contacto_principal="Contacto de prueba",
            telefono="1234567890"
        )
        
        cls.alimento = Alimento.objects.create(
            nombre="Alimento Iniciador",
            etapa="INICIADOR",
            proveedor=cls.proveedor,
            proteina_porcentaje=20.5,
            fecha_vencimiento=timezone.now().date() + timezone.timedelta(days=180),
            lote_fabricante="LOTE-001"
        )
        
        cls.granja = Granja.objects.create(
            empresa=cls.empresa,
            codigo_granja="GRANJA-001",
            nombre="Granja de Prueba",
            direccion="Ubicación de prueba",
            capacidad_total_aves=10000
        )
        
        cls.galpon = Galpon.objects.create(
            granja=cls.granja,
            numero_galpon="GALPON-001",
            tipo_galpon="PRODUCCION",
            capacidad_aves=5000,
            area_metros_cuadrados=1000.00
        )
        
        today = timezone.now().date()
        cls.lote = Lote.objects.create(
            galpon=cls.galpon,
            raza=cls.raza,
            alimento=cls.alimento,
            fecha_inicio=today,
            fecha_ingreso=today,
            cantidad_inicial_aves=5000,
            edad_inicial_semanas=18,
            edad_semanas=18,
            estado="INICIAL",
            codigo_lote="LOTE-001"
        )
    
    def test_mortalidad_diaria_creation(self):
        """Test creation of MortalidadDiaria and its relationship with Lote"""
        today = timezone.now().date()
        
        # Create a daily mortality record
        mortalidad = MortalidadDiaria.objects.create(
            lote=self.lote,
            fecha=today,
            cantidad_muertes=5,
            causa="Enfermedad",
            observaciones="Primer registro de mortalidad"
        )
        
        # Test basic attributes
        self.assertEqual(mortalidad.cantidad_muertes, 5)
        self.assertEqual(mortalidad.causa, "Enfermedad")
        self.assertEqual(mortalidad.lote, self.lote)
        
        # Test string representation
        expected_str = f"Mortalidad {self.lote.codigo_lote} - {today} (5 aves)"
        self.assertEqual(str(mortalidad), expected_str)
        
        # Test the reverse relation from Lote
        self.assertIn(mortalidad, self.lote.mortalidades_diarias.all())
    
    def test_seguimiento_diario_with_mortalidad(self):
        """Test SeguimientoDiario's aves_presentes method with mortality records"""
        today = timezone.now().date()
        
        # Create daily mortality records
        MortalidadDiaria.objects.create(
            lote=self.lote,
            fecha=today,
            cantidad_muertes=5,
            causa="Enfermedad"
        )
        
        # Create a daily tracking record
        seguimiento = SeguimientoDiario.objects.create(
            lote=self.lote,
            fecha_seguimiento=today,
            registrado_por=self.user,
            tipo_seguimiento="PRODUCCION",
            huevos_totales=4500,
            peso_promedio_ave=1.75,
            consumo_alimento_kg=1000,
            mortalidad=5
        )
        
        # Test aves_presentes method
        expected_aves = self.lote.cantidad_inicial_aves - 5
        self.assertEqual(seguimiento.aves_presentes(), expected_aves)
        
        # Test mortalidad_del_dia method
        self.assertEqual(seguimiento.mortalidad_del_dia(), 5)
    
    def test_seguimiento_diario_conversion_alimenticia(self):
        """Test SeguimientoDiario's calcular_conversion_alimenticia method"""
        today = timezone.now().date()
        yesterday = today - timezone.timedelta(days=1)
        
        # Create a tracking record for yesterday
        SeguimientoDiario.objects.create(
            lote=self.lote,
            fecha_seguimiento=yesterday,
            registrado_por=self.user,
            tipo_seguimiento="ENGORDE",
            peso_promedio_ave=1.50,
            consumo_alimento_kg=1000
        )
        
        # Create a tracking record for today
        seguimiento_hoy = SeguimientoDiario.objects.create(
            lote=self.lote,
            fecha_seguimiento=today,
            registrado_por=self.user,
            tipo_seguimiento="ENGORDE",
            peso_promedio_ave=1.75,
            consumo_alimento_kg=1200
        )
        
        # Test conversion_alimenticia calculation
        conversion = seguimiento_hoy.calcular_conversion_alimenticia()
        self.assertIsNotNone(conversion)
        
        # Expected calculation: 1200 / (5000 * (1.75 - 1.50)) = 1200 / 1250 = 0.96
        self.assertAlmostEqual(conversion, 0.96, places=2)
    
    def test_seguimiento_diario_str_representation(self):
        """Test string representation of SeguimientoDiario"""
        today = timezone.now().date()
        
        seguimiento = SeguimientoDiario(
            lote=self.lote,
            fecha_seguimiento=today,
            tipo_seguimiento="PRODUCCION"
        )
        
        expected_str = f"Seguimiento {self.lote.codigo_lote} - {today} (Producción de Huevos)"
        self.assertEqual(str(seguimiento), expected_str)

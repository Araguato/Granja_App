"""
Tests for Inventario app URLs and views.
"""
from django.test import TestCase, Client
from django.urls import reverse, resolve
from django.contrib.auth import get_user_model
from produccion.models import Granja, Galpon, Lote
from inventario.models import Proveedor, Alimento, Vacuna, Insumo

User = get_user_model()

class InventarioURLTests(TestCase):
    """Test cases for Inventario app URLs and views."""
    
    @classmethod
    def setUpTestData(cls):
        """Set up test data for the whole TestCase."""
        # Create a test user
        cls.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123',
            role='supervisor'
        )
        
        # Create test data for related models
        cls.granja = Granja.objects.create(
            nombre='Granja de Prueba',
            direccion='Calle Falsa 123',
            telefono='123456789',
            encargado=cls.user
        )
        
        cls.galpon = Galpon.objects.create(
            granja=cls.granja,
            codigo='GAL-001',
            capacidad=5000,
            estado='disponible'
        )
        
        cls.lote = Lote.objects.create(
            galpon=cls.galpon,
            codigo='LOTE-001',
            fecha_ingreso='2023-01-01',
            cantidad_aves=1000,
            raza='Cobb',
            estado='activo'
        )
        
        # Create test data for inventario models
        cls.proveedor = Proveedor.objects.create(
            nombre='Proveedor de Prueba',
            contacto='Juan Perez',
            telefono='987654321',
            email='proveedor@test.com',
            direccion='Calle Proveedor 123'
        )
        
        cls.alimento = Alimento.objects.create(
            nombre='Alimento Inicial',
            descripcion='Alimento para aves en etapa inicial',
            unidad_medida='kg',
            stock_actual=1000,
            stock_minimo=100,
            proveedor=cls.proveedor
        )
        
        cls.vacuna = Vacuna.objects.create(
            nombre='Vacuna Test',
            descripcion='Vacuna de prueba',
            laboratorio='Lab Test',
            tipo='intramuscular',
            dosis_recomendada='0.5ml',
            stock_actual=100,
            stock_minimo=10
        )
        
        cls.insumo = Insumo.objects.create(
            nombre='Insumo Test',
            descripcion='Insumo de prueba',
            unidad_medida='unidad',
            stock_actual=50,
            stock_minimo=5
        )
    
    def setUp(self):
        """Set up test client and log in the test user."""
        self.client = Client()
        self.client.force_login(self.user)
    
    def test_alimento_urls_resolve(self):
        """Test that alimento URLs resolve to the correct views."""
        # Lista de alimentos
        url = reverse('inventario:lista_alimentos')
        self.assertEqual(resolve(url).view_name, 'inventario:lista_alimentos')
        
        # Detalle de alimento
        url = reverse('inventario:detalle_alimento', kwargs={'alimento_id': self.alimento.id})
        self.assertEqual(resolve(url).view_name, 'inventario:detalle_alimento')
        
        # Registrar consumo de alimento
        url = reverse('inventario:registrar_consumo')
        self.assertEqual(resolve(url).view_name, 'inventario:registrar_consumo')
    
    def test_vacuna_urls_resolve(self):
        """Test that vacuna URLs resolve to the correct views."""
        # Lista de vacunas
        url = reverse('inventario:lista_vacunas')
        self.assertEqual(resolve(url).view_name, 'inventario:lista_vacunas')
        
        # Detalle de vacuna
        url = reverse('inventario:detalle_vacuna', kwargs={'vacuna_id': self.vacuna.id})
        self.assertEqual(resolve(url).view_name, 'inventario:detalle_vacuna')
        
        # Registrar aplicación de vacuna
        url = reverse('inventario:registrar_aplicacion')
        self.assertEqual(resolve(url).view_name, 'inventario:registrar_aplicacion')
    
    def test_seguimiento_urls_resolve(self):
        """Test that seguimiento URLs resolve to the correct views."""
        # Registro de seguimiento
        url = reverse('inventario:registro_seguimiento')
        self.assertEqual(resolve(url).view_name, 'inventario:registro_seguimiento')
        
        # Nuevo seguimiento para lote
        url = reverse('inventario:nuevo_seguimiento', kwargs={'lote_id': self.lote.id})
        self.assertEqual(resolve(url).view_name, 'inventario:nuevo_seguimiento')
        
        # Historial de seguimiento de lote
        url = reverse('inventario:seguimiento_lote', kwargs={'lote_id': self.lote.id})
        self.assertEqual(resolve(url).view_name, 'inventario:seguimiento_lote')
    
    def test_login_required_redirects(self):
        """Test that protected URLs redirect to login when not authenticated."""
        self.client.logout()
        
        protected_urls = [
            reverse('inventario:lista_alimentos'),
            reverse('inventario:detalle_alimento', kwargs={'alimento_id': self.alimento.id}),
            reverse('inventario:lista_vacunas'),
            reverse('inventario:detalle_vacuna', kwargs={'vacuna_id': self.vacuna.id}),
            reverse('inventario:registro_seguimiento'),
        ]
        
        for url in protected_urls:
            response = self.client.get(url)
            self.assertEqual(response.status_code, 302)  # Redirect to login
            self.assertIn('/login/', response.url)
    
    def test_urls_return_correct_templates(self):
        """Test that URLs return the correct templates."""
        # Test list views
        list_views = [
            ('inventario:lista_alimentos', 'inventario/alimento_list.html'),
            ('inventario:lista_vacunas', 'inventario/vacuna_list.html'),
        ]
        
        for view_name, template in list_views:
            response = self.client.get(reverse(view_name))
            self.assertEqual(response.status_code, 200)
            self.assertTemplateUsed(response, template)
        
        # Test detail views
        detail_views = [
            ('inventario:detalle_alimento', {'alimento_id': self.alimento.id}, 'inventario/alimento_detail.html'),
            ('inventario:detalle_vacuna', {'vacuna_id': self.vacuna.id}, 'inventario/vacuna_detail.html'),
        ]
        
        for view_name, kwargs, template in detail_views:
            response = self.client.get(reverse(view_name, kwargs=kwargs))
            self.assertEqual(response.status_code, 200)
            self.assertTemplateUsed(response, template)
    
    def test_api_endpoints(self):
        """Test that API endpoints are accessible and return expected status codes."""
        # Test list endpoints
        list_endpoints = [
            '/api/alimentos/',
            '/api/vacunas/',
            '/api/insumos/',
            '/api/proveedores/',
        ]
        
        for endpoint in list_endpoints:
            response = self.client.get(endpoint)
            self.assertIn(response.status_code, [200, 204])  # 200 OK or 204 No Content
        
        # Test detail endpoints
        detail_endpoints = [
            f'/api/alimentos/{self.alimento.id}/',
            f'/api/vacunas/{self.vacuna.id}/',
            f'/api/insumos/{self.insumo.id}/',
            f'/api/proveedores/{self.proveedor.id}/',
        ]
        
        for endpoint in detail_endpoints:
            response = self.client.get(endpoint)
            self.assertEqual(response.status_code, 200)

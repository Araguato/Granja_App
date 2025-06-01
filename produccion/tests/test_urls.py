"""
Tests for Produccion app URLs and views.
"""
from django.test import TestCase, Client
from django.urls import reverse, resolve
from django.contrib.auth import get_user_model
from produccion.models import Granja, Galpon, Lote

User = get_user_model()

class ProduccionURLTests(TestCase):
    """Test cases for Produccion app URLs and views."""
    
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
        
        # Create test data
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
    
    def setUp(self):
        """Set up test client and log in the test user."""
        self.client = Client()
        self.client.force_login(self.user)
    
    def test_lote_urls_resolve(self):
        """Test that lote URLs resolve to the correct views."""
        # Lista de lotes
        url = reverse('produccion:lista_lotes')
        self.assertEqual(resolve(url).view_name, 'produccion:lista_lotes')
        
        # Detalle de lote
        url = reverse('produccion:detalle_lote', kwargs={'lote_id': self.lote.id})
        self.assertEqual(resolve(url).view_name, 'produccion:detalle_lote')
        
        # Nuevo lote
        url = reverse('produccion:nuevo_lote', kwargs={'galpon_id': self.galpon.id})
        self.assertEqual(resolve(url).view_name, 'produccion:nuevo_lote')
        
        # Editar lote
        url = reverse('produccion:editar_lote', kwargs={'lote_id': self.lote.id})
        self.assertEqual(resolve(url).view_name, 'produccion:editar_lote')
    
    def test_galpon_urls_resolve(self):
        """Test that galpon URLs resolve to the correct views."""
        # Lista de galpones
        url = reverse('produccion:lista_galpones')
        self.assertEqual(resolve(url).view_name, 'produccion:lista_galpones')
        
        # Detalle de galpón
        url = reverse('produccion:detalle_galpon', kwargs={'galpon_id': self.galpon.id})
        self.assertEqual(resolve(url).view_name, 'produccion:detalle_galpon')
        
        # Nuevo galpón
        url = reverse('produccion:nuevo_galpon')
        self.assertEqual(resolve(url).view_name, 'produccion:nuevo_galpon')
        
        # Editar galpón
        url = reverse('produccion:editar_galpon', kwargs={'galpon_id': self.galpon.id})
        self.assertEqual(resolve(url).view_name, 'produccion:editar_galpon')
    
    def test_login_required_redirects(self):
        """Test that protected URLs redirect to login when not authenticated."""
        self.client.logout()
        
        protected_urls = [
            reverse('produccion:lista_lotes'),
            reverse('produccion:detalle_lote', kwargs={'lote_id': self.lote.id}),
            reverse('produccion:lista_galpones'),
            reverse('produccion:detalle_galpon', kwargs={'galpon_id': self.galpon.id}),
        ]
        
        for url in protected_urls:
            response = self.client.get(url)
            self.assertEqual(response.status_code, 302)  # Redirect to login
            self.assertIn('/login/', response.url)
    
    def test_urls_return_correct_templates(self):
        """Test that URLs return the correct templates."""
        # Test list views
        list_views = [
            ('produccion:lista_lotes', 'produccion/lote_list.html'),
            ('produccion:lista_galpones', 'produccion/galpon_list.html'),
        ]
        
        for view_name, template in list_views:
            response = self.client.get(reverse(view_name))
            self.assertEqual(response.status_code, 200)
            self.assertTemplateUsed(response, template)
        
        # Test detail views
        detail_views = [
            ('produccion:detalle_lote', {'lote_id': self.lote.id}, 'produccion/lote_detail.html'),
            ('produccion:detalle_galpon', {'galpon_id': self.galpon.id}, 'produccion/galpon_detail.html'),
        ]
        
        for view_name, kwargs, template in detail_views:
            response = self.client.get(reverse(view_name, kwargs=kwargs))
            self.assertEqual(response.status_code, 200)
            self.assertTemplateUsed(response, template)

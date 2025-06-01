"""
Tests for Reportes app URLs and views.
"""
from django.test import TestCase, Client
from django.urls import reverse, resolve
from django.contrib.auth import get_user_model
from django.utils import timezone
from produccion.models import Granja, Galpon, Lote
from reportes.models import ReporteGenerado

User = get_user_model()

class ReportesURLTests(TestCase):
    """Test cases for Reportes app URLs and views."""
    
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
        
        # Create test report
        cls.reporte = ReporteGenerado.objects.create(
            nombre='Reporte de Prueba',
            descripcion='Este es un reporte de prueba',
            tipo='diario',
            parametros={},
            generado_por=cls.user,
            archivo='reportes/test_report.pdf'
        )
    
    def setUp(self):
        """Set up test client and log in the test user."""
        self.client = Client()
        self.client.force_login(self.user)
    
    def test_panel_reportes_url_resolves(self):
        """Test that panel_reportes URL resolves to the correct view."""
        url = reverse('reportes:panel_reportes')
        self.assertEqual(resolve(url).view_name, 'reportes:panel_reportes')
    
    def test_nuevo_reporte_url_resolves(self):
        """Test that nuevo_reporte URL resolves to the correct view."""
        url = reverse('reportes:nuevo_reporte')
        self.assertEqual(resolve(url).view_name, 'reportes:nuevo_reporte')
    
    def test_detalle_reporte_url_resolves(self):
        """Test that detalle_reporte URL resolves to the correct view."""
        url = reverse('reportes:detalle_reporte', kwargs={'reporte_id': self.reporte.id})
        self.assertEqual(resolve(url).view_name, 'reportes:detalle_reporte')
    
    def test_descargar_reporte_url_resolves(self):
        """Test that descargar_reporte URL resolves to the correct view."""
        url = reverse('reportes:descargar_reporte', kwargs={'reporte_id': self.reporte.id})
        self.assertEqual(resolve(url).view_name, 'reportes:descargar_reporte')
    
    def test_eliminar_reporte_url_resolves(self):
        """Test that eliminar_reporte URL resolves to the correct view."""
        url = reverse('reportes:eliminar_reporte', kwargs={'reporte_id': self.reporte.id})
        self.assertEqual(resolve(url).view_name, 'reportes:eliminar_reporte')
    
    def test_login_required_redirects(self):
        """Test that protected URLs redirect to login when not authenticated."""
        self.client.logout()
        
        protected_urls = [
            reverse('reportes:panel_reportes'),
            reverse('reportes:nuevo_reporte'),
            reverse('reportes:detalle_reporte', kwargs={'reporte_id': self.reporte.id}),
            reverse('reportes:descargar_reporte', kwargs={'reporte_id': self.reporte.id}),
            reverse('reportes:eliminar_reporte', kwargs={'reporte_id': self.reporte.id}),
        ]
        
        for url in protected_urls:
            response = self.client.get(url)
            self.assertEqual(response.status_code, 302)  # Redirect to login
            self.assertIn('/login/', response.url)
    
    def test_urls_return_correct_templates(self):
        """Test that URLs return the correct templates."""
        # Test panel reportes
        response = self.client.get(reverse('reportes:panel_reportes'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'reportes/panel_reportes.html')
        
        # Test nuevo reporte
        response = self.client.get(reverse('reportes:nuevo_reporte'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'reportes/nuevo_reporte.html')
        
        # Test detalle reporte
        response = self.client.get(reverse('reportes:detalle_reporte', kwargs={'reporte_id': self.reporte.id}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'reportes/detalle_reporte.html')
    
    def test_delete_report_requires_post(self):
        """Test that deleting a report requires a POST request."""
        # Try to delete with GET (should not work)
        response = self.client.get(reverse('reportes:eliminar_reporte', kwargs={'reporte_id': self.reporte.id}))
        self.assertEqual(response.status_code, 405)  # Method Not Allowed
        
        # Delete with POST
        response = self.client.post(reverse('reportes:eliminar_reporte', kwargs={'reporte_id': self.reporte.id}))
        self.assertEqual(response.status_code, 302)  # Redirect after deletion
        
        # Verify report was deleted
        with self.assertRaises(ReporteGenerado.DoesNotExist):
            ReporteGenerado.objects.get(id=self.reporte.id)

"""
Tests for URL configurations in the core app.
"""
from django.test import TestCase, Client
from django.urls import reverse, resolve
from django.contrib.auth import get_user_model

User = get_user_model()

class CoreURLTests(TestCase):
    """Test cases for core app URLs."""
    
    @classmethod
    def setUpTestData(cls):
        """Set up test data for the whole TestCase."""
        # Create a test user
        cls.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123',
            role='supervisor'  # Assuming you have a role field
        )
    
    def setUp(self):
        """Set up test client and log in the test user."""
        self.client = Client()
        self.client.force_login(self.user)
    
    def test_home_url_resolves(self):
        """Test that the home URL resolves to the correct view."""
        url = reverse('core:home')
        self.assertEqual(resolve(url).view_name, 'core:home')
    
    def test_dashboard_url_resolves(self):
        """Test that the dashboard URL resolves to the correct view."""
        url = reverse('core:dashboard')
        self.assertEqual(resolve(url).view_name, 'core:dashboard')
    
    def test_estadisticas_url_resolves(self):
        """Test that the statistics URL resolves to the correct view."""
        url = reverse('core:estadisticas')
        self.assertEqual(resolve(url).view_name, 'core:estadisticas')
    
    def test_recomendaciones_url_resolves(self):
        """Test that the recommendations URL resolves to the correct view."""
        url = reverse('core:recomendaciones')
        self.assertEqual(resolve(url).view_name, 'core:recomendaciones')
    
    def test_login_required_redirects(self):
        """Test that protected URLs redirect to login when not authenticated."""
        self.client.logout()
        protected_urls = [
            reverse('core:dashboard'),
            reverse('core:estadisticas'),
            reverse('core:recomendaciones'),
            reverse('core:perfil_usuario'),
        ]
        
        for url in protected_urls:
            response = self.client.get(url)
            self.assertEqual(response.status_code, 302)  # Redirect to login
            self.assertIn('/login/', response.url)
    
    def test_public_urls_accessible(self):
        """Test that public URLs are accessible without authentication."""
        self.client.logout()
        public_urls = [
            reverse('core:home'),
            reverse('core:login'),
        ]
        
        for url in public_urls:
            response = self.client.get(url)
            self.assertEqual(response.status_code, 200)
    
    def test_error_handlers(self):
        """Test custom error handlers."""
        # Test 404 error
        response = self.client.get('/non-existent-url/')
        self.assertEqual(response.status_code, 404)
        self.assertTemplateUsed('core/404.html')
        
        # Test 500 error (simulated by a view that raises an exception)
        # Note: You'll need to create a test view that raises an exception
        # or use the test client to simulate a 500 error
        response = self.client.get('/500/')
        self.assertEqual(response.status_code, 500)
        self.assertTemplateUsed('core/500.html')
    
    def test_language_switching(self):
        """Test language switching functionality."""
        # Test setting language via URL
        response = self.client.get('/lang/en/')
        self.assertEqual(response.status_code, 302)  # Should redirect back
        
        # Test setting language via AJAX
        response = self.client.post(
            reverse('core:set_language_ajax'),
            {'language': 'es'},
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(str(response.content, encoding='utf8'), {'status': 'ok'})

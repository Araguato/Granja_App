"""
Tests for API URL configurations.
"""
from django.test import TestCase
from django.urls import reverse, resolve
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase, APIClient
from rest_framework import status

User = get_user_model()

class APIURLTests(APITestCase):
    """Test cases for API URLs and endpoints."""
    
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
        """Set up test client and authenticate."""
        self.client = APIClient()
        # Get JWT token
        response = self.client.post(
            reverse('api:token_obtain_pair'),
            {'username': 'testuser', 'password': 'testpass123'},
            format='json'
        )
        self.token = response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
    
    def test_api_root_resolves(self):
        """Test that the API root URL resolves."""
        url = reverse('api:api-root')
        self.assertEqual(resolve(url).view_name, 'api:api-root')
    
    def test_token_obtain_pair_url(self):
        """Test JWT token obtain endpoint."""
        url = reverse('api:token_obtain_pair')
        self.assertEqual(resolve(url).view_name, 'api:token_obtain_pair')
    
    def test_token_refresh_url(self):
        """Test JWT token refresh endpoint."""
        url = reverse('api:token_refresh')
        self.assertEqual(resolve(url).view_name, 'api:token_refresh')
    
    def test_protected_endpoints_require_auth(self):
        """Test that protected endpoints require authentication."
        # Remove authentication
        self.client.credentials()
        
        protected_endpoints = [
            reverse('api:usuario-list'),
            reverse('api:granja-list'),
            reverse('api:galpon-list'),
            # Add more endpoints as needed
        ]
        
        for url in protected_endpoints:
            response = self.client.get(url)
            self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_api_endpoints_accessible(self):
        """Test that API endpoints are accessible with authentication."""
        endpoints = [
            ('api:usuario-list', {}),
            ('api:granja-list', {}),
            ('api:galpon-list', {}),
            # Add more endpoints as needed
        ]
        
        for endpoint_name, kwargs in endpoints:
            try:
                url = reverse(endpoint_name, kwargs=kwargs)
                response = self.client.get(url)
                self.assertIn(response.status_code, [status.HTTP_200_OK, status.HTTP_204_NO_CONTENT])
            except Exception as e:
                self.fail(f"Failed to access {endpoint_name}: {str(e)}")
    
    def test_api_endpoint_permissions(self):
        """Test that API endpoints enforce permissions correctly."""
        # Create a regular user with limited permissions
        regular_user = User.objects.create_user(
            username='regularuser',
            email='regular@example.com',
            password='testpass123',
            role='user'  # Assuming 'user' has limited permissions
        )
        
        # Get token for regular user
        response = self.client.post(
            reverse('api:token_obtain_pair'),
            {'username': 'regularuser', 'password': 'testpass123'},
            format='json'
        )
        token = response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        
        # Test endpoints that should be restricted
        restricted_endpoints = [
            # Add endpoints that require special permissions
        ]
        
        for endpoint_name, kwargs in restricted_endpoints:
            try:
                url = reverse(endpoint_name, kwargs=kwargs)
                response = self.client.get(url)
                self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
            except Exception as e:
                self.fail(f"Failed to test permissions for {endpoint_name}: {str(e)}")

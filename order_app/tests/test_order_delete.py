from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token

from auth_app.models import CustomUser
from ..models import Order

class OrderDeleteTest(APITestCase):
    def setUp(self):
        self.admin_user = CustomUser.objects.create_user(
            username='matthias_admin',
            email='matthias@badmin.de',
            password='password123',
            type='business',
            is_staff=True
        )
        self.admin_token, _ = Token.objects.get_or_create(user=self.admin_user)
        
        self.business_user = CustomUser.objects.create_user(
            username='max_business',
            email='max@business.de',
            password='password123',
            type='business'
        )
        self.business_token, _ = Token.objects.get_or_create(user=self.business_user)
        
        self.customer_user = CustomUser.objects.create_user(
            username='maria_customer',
            email='maria@customer.de',
            password='password123',
            type='customer'
        )
        self.customer_token, _ = Token.objects.get_or_create(user=self.customer_user)
        
        self.order = Order.objects.create(
            customer_user = self.customer_user,
            business_user = self.business_user,
            title = 'Test Order',
            revisions = 1,
            delivery_time_in_days = 2,
            price = 150,
            features = ['Feature 1', 'Feature 2'],
            offer_type = 'basic',
            status = 'in_progress',
        )
        
        self.url = reverse('order-single', kwargs={'pk': self.order.pk})
    
    # Staff löscht existierende Order	204
    def test_order_delete_success(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.admin_token.key)
        response = self.client.delete(self.url)
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Order.objects.filter(pk=self.order.pk).exists())
    
    # Nicht authentifiziert	401
    def test_order_delete_unauthenticated(self):
        self.client.credentials()
        response = self.client.delete(self.url)
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    # Authentifiziert aber kein Staff	403
    def test_order_delete_no_admin(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.business_token.key)
        response = self.client.delete(self.url)
        
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    # Order existiert nicht	404
    def test_order_delete_not_found(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.admin_token.key)
        url = reverse('order-single', kwargs={'pk': 9999})
        
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token

from auth_app.models import CustomUser
from ..models import Order

class OrderListTest(APITestCase):
    def setUp(self):
        self.business_user1 = CustomUser.objects.create_user(
            username='max_business',
            email='max@business.de',
            password='password123',
            type='business'
        )
        self.business_token1, _ = Token.objects.get_or_create(user=self.business_user1)
        
        self.customer_user1 = CustomUser.objects.create_user(
            username='maria_customer',
            email='maria@customer.de',
            password='password123',
            type='customer'
        )
        self.customer_token1, _ = Token.objects.get_or_create(user=self.customer_user1)
        
        self.customer_user2 = CustomUser.objects.create_user(
            username='martin_customer',
            email='martin@customer.de',
            password='password123',
            type='customer'
        )
        self.customer_token2, _ = Token.objects.get_or_create(user=self.customer_user2)

        
        self.order = Order.objects.create(
            customer_user = self.customer_user1,
            business_user = self.business_user1,
            title = 'Test Order',
            revisions = 1,
            delivery_time_in_days = 2,
            price = 150,
            features = ['Feature 1', 'Feature 2'],
            offer_type = 'basic',
            status = 'in_progress',
        )
        
        self.order2 = Order.objects.create(
            customer_user = self.customer_user1,
            business_user = self.business_user1,
            title = 'Test Order 2',
            revisions = 2,
            delivery_time_in_days = 4,
            price = 300,
            features = ['Feature 1', 'Feature 2'],
            offer_type = 'standard',
            status = 'in_progress',
        )
        
        self.url = reverse('order-list')
    
    def test_order_list_success(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.business_token1.key)
        
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_order_list_content(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.business_token1.key)
        
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertIn('customer_user', response.data[0]),
        self.assertIn('business_user', response.data[0])
        self.assertIn('created_at', response.data[0])
        self.assertIn('updated_at', response.data[0])
        self.assertIn('status', response.data[0])
        
    def test_offer_list_response(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.business_token1.key)

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('id', response.data[0])
        self.assertIn('customer_user', response.data[0])
        self.assertIn('business_user', response.data[0])
        self.assertIn('title', response.data[0])
        self.assertIn('revisions', response.data[0])
        self.assertIn('delivery_time_in_days', response.data[0])
        self.assertIn('price', response.data[0])
        self.assertIn('features', response.data[0])
        self.assertIn('offer_type', response.data[0])
        self.assertIn('status', response.data[0])
        self.assertIn('created_at', response.data[0])
        self.assertIn('updated_at', response.data[0])
    
    def test_order_user_unauthenticated(self):
        self.client.credentials()
        
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
    def test_order_user_filtering(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.customer_token2.key)
        
        response = self.client.get(self.url)
        self.assertEqual(len(response.data), 0)


from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token

from auth_app.models import CustomUser
from offer_app.models import Offer, OfferDetail
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
        
class OrderCreateTest(APITestCase):
    def setUp(self):
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
        
        self.offer = Offer.objects.create(
            user=self.business_user,
            title='Test Offer',
            description='This is a test offer.'
        )
        
        self.offer_detail = OfferDetail.objects.create(
            offer=self.offer,
            title='Basic Package',
            revisions=1,
            delivery_time_in_days=5,
            price=100,
            features=['Feature 1', 'Feature 2'],
            offer_type='basic'
        )
        
        self.valid_payload = {
            'offer_detail_id': self.offer_detail.pk
        }
        
        self.url = reverse('order-list')
    
    def test_order_create_success(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.customer_token.key)

        response = self.client.post(self.url, self.valid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('id', response.data)
        self.assertEqual(Order.objects.count(), 1)
    
    def test_order_missing_id(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.customer_token.key)
        offer_payload = self.valid_payload.copy()
        offer_payload.pop('offer_detail_id')
    
        response = self.client.post(self.url, offer_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_order_unauthenticated(self):
        self.client.credentials()
    
        response = self.client.post(self.url, self.valid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
    def test_order_logged_in_as_business_user(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.business_token.key)
        
        response = self.client.post(self.url, self.valid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    
    def test_order_id_not_found(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.customer_token.key)
        invalid_payload = {
            'offer_detail_id': 9999
        }
        
        response = self.client.post(self.url, invalid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
import copy

from auth_app.models import CustomUser
from offer_app.models import Offer, OfferDetail

class TestOfferCreate(APITestCase):
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
        
        self.valid_payload = {
            'title': "Test Offer 1",
            'description': "Test description 1",
            'details': [
                {
                    'title': 'Basic Package',
                    'revisions': 1,
                    'delivery_time_in_days': 5,
                    'price': 100,
                    'features': ['Feature 1', 'Feature 2'],
                    'offer_type': 'basic'
                },
                {
                    'title': 'Standard Package',
                    'revisions': 2,
                    'delivery_time_in_days': 10,
                    'price': 200,
                    'features': ['Feature 1', 'Feature 2', 'Feature 3'],
                    'offer_type': 'standard'
                },
                {
                    'title': 'Premium Package',
                    'revisions': 3,
                    'delivery_time_in_days': 15,
                    'price': 300,
                    'features': ['Feature 1', 'Feature 2', 'Feature 3', 'Feature 4'],
                    'offer_type': 'premium'
                }
            ]
        }

        self.url = reverse('offer-list')
        
    def test_offer_create_success(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.business_token.key)
        response = self.client.post(self.url, self.valid_payload, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('id', response.data)
        self.assertEqual(len(response.data['details']), 3)
        
    def test_offer_create_missing_detail(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.business_token.key)
        offer_payload = copy.deepcopy(self.valid_payload)
        offer_payload['details'].pop()
        response = self.client.post(self.url, offer_payload, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
    def test_offer_create_Unauthenticated(self):
        self.client.credentials()
        offer_payload = copy.deepcopy(self.valid_payload)
        response = self.client.post(self.url, offer_payload, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_offer_create_customer_forbidden(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.customer_token.key)
        offer_payload = copy.deepcopy(self.valid_payload)
        response = self.client.post(self.url, offer_payload, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
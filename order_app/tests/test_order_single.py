from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token

from auth_app.models import CustomUser
from offer_app.models import Offer, OfferDetail
from ..models import Order

class UpdateStatusOrderSingleTest(APITestCase):
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
        
        self.valid_payload = {
            'status': 'completed'
        }
        
        self.url = reverse('order-single', kwargs={'pk': self.order.pk})
    
    def test_order_patch_success(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.business_token.key)

        response = self.client.patch(self.url, self.valid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_order_patch_invalid_status(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.business_token.key)
        invalid_payload = {
            'status': 'invalid_status'
        }

        response = self.client.patch(self.url, invalid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_order_patch_unauthenticated(self):
        self.client.credentials()

        response = self.client.patch(self.url, self.valid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_order_patch_wrong_user(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.customer_token.key)

        response = self.client.patch(self.url, self.valid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_order_patch_not_found(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.business_token.key)
        url = reverse('order-single', kwargs={'pk': 9999})

        response = self.client.patch(url, self.valid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token

from auth_app.models import CustomUser
from offer_app.models import Offer, OfferDetail

class TestOfferSingle(APITestCase):
    def setUp(self):
        self.business_user = CustomUser.objects.create_user(
            username='max_business',
            email='max@business.de',
            password='password123',
            type='business'
        )
        self.business_token, _ = Token.objects.get_or_create(user=self.business_user)
        
        self.offer = Offer.objects.create(
            user=self.business_user,
            title='Test Offer',
            description='This is a test offer.'
        )
        
        OfferDetail.objects.create(
            offer=self.offer,
            title='Basic Package',
            revisions=1,
            delivery_time_in_days=5,
            price=100,
            features=['Feature 1', 'Feature 2'],
            offer_type='basic'
        )

        self.url = reverse('offer-single', kwargs={'pk': self.offer.pk})

    def test_offer_single_success(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.business_token.key)
        response = self.client.get(self.url, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_offer_single_unauthorized(self):
        self.client.credentials()
        response = self.client.get(self.url, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_offer_single_not_found(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.business_token.key)
        url = reverse('offer-single', kwargs={'pk': 9999})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
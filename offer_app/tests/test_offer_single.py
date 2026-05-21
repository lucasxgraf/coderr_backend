from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token

from auth_app.models import CustomUser
from offer_app.models import Offer, OfferDetail

class OfferSingleTests(APITestCase):
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

class UpdateOfferSingleTests(APITestCase):
    def setUp(self):
        self.business_user1 = CustomUser.objects.create_user(
            username='max_business',
            email='max@business.de',
            password='password123',
            type='business'
        )
        self.business_token1, _ = Token.objects.get_or_create(user=self.business_user1)
        
        self.business_user2 = CustomUser.objects.create_user(
            username='maria_business',
            email='maria@business.de',
            password='password123',
            type='business'
        )
        self.business_token2, _ = Token.objects.get_or_create(user=self.business_user2)
        
        self.offer = Offer.objects.create(
            user=self.business_user1,
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
        
        OfferDetail.objects.create(
            offer=self.offer,
            title='Standard Package',
            revisions=2,
            delivery_time_in_days=10,
            price=200,
            features=['Feature 1', 'Feature 2'],
            offer_type='standard'
        )
        
        OfferDetail.objects.create(
            offer=self.offer,
            title='Premium Package',
            revisions=3,
            delivery_time_in_days=15,
            price=300,
            features=['Feature 1', 'Feature 2'],
            offer_type='premium'
        )
        
        self.url = reverse('offer-single', kwargs={'pk': self.offer.pk})
        
    def test_patch_offer_success(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.business_token1.key)
        data = {
            'details': [{
                'title': 'Title updated',
                'offer_type': 'premium' 
            }]
        }
        
        response = self.client.patch(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_patch_offer_invalid_data(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.business_token1.key)
        data = {
            'details': [{
                'title': 'Title updated',
            }]
        }
        
        response = self.client.patch(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_patch_offer_unauthenticated(self):
        self.client.credentials()
        data = {
            'details': [{
                'title': 'Title updated',
                'offer_type': 'premium' 
            }]
        }
        
        response = self.client.patch(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_patch_offer_other_user(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.business_token2.key)
        data = {
            'details': [{
                'title': 'Title updated',
                'offer_type': 'premium' 
            }]
        }
        
        response = self.client.patch(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_patch_offer_not_found(self):
        self.url = reverse('offer-single', kwargs={'pk': 9999})
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.business_token1.key)
        data = {
            'details': [{
                'title': 'Title updated',
                'offer_type': 'premium'
            }]
        }

        response = self.client.patch(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class DeleteOfferSingleTests(APITestCase):
    def setUp(self):
        self.business_user1 = CustomUser.objects.create_user(
            username='max_business',
            email='max@business.de',
            password='password123',
            type='business'
        )
        self.business_token1, _ = Token.objects.get_or_create(user=self.business_user1)

        self.business_user2 = CustomUser.objects.create_user(
            username='maria_business',
            email='maria@business.de',
            password='password123',
            type='business'
        )
        self.business_token2, _ = Token.objects.get_or_create(user=self.business_user2)

        self.offer = Offer.objects.create(
            user=self.business_user1,
            title='Test Offer',
            description='This is a test offer.'
        )

        self.url = reverse('offer-single', kwargs={'pk': self.offer.pk})

    def test_delete_offer_success(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.business_token1.key)
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Offer.objects.filter(pk=self.offer.pk).exists())

    def test_delete_offer_unauthenticated(self):
        self.client.credentials()
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_offer_forbidden(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.business_token2.key)
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_offer_not_found(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.business_token1.key)
        url = reverse('offer-single', kwargs={'pk': 9999})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
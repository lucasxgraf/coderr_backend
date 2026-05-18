from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.utils import timezone
from datetime import timedelta

from auth_app.models import CustomUser
from offer_app.models import Offer, OfferDetail

class OfferListTests(APITestCase):
    def setUp(self):
        self.business_user = CustomUser.objects.create_user(
            username='max_business',
            email='max@business.de',
            password='password123',
            type='business'
        )
        
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
        
        self.url = reverse('offer-list')
    
    def test_offer_list_success(self):
        response = self.client.get(self.url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_offer_list_content(self):
        response = self.client.get(self.url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)
        self.assertIn('next', response.data)
        self.assertIn('previous', response.data)
        self.assertEqual(len(response.data['results']), 1)
    
    def test_offer_list_response(self):
        response = self.client.get(self.url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('id', response.data['results'][0])
        self.assertIn('user', response.data['results'][0])
        self.assertIn('title', response.data['results'][0])
        self.assertIn('image', response.data['results'][0])
        self.assertIn('description', response.data['results'][0])
        self.assertIn('created_at', response.data['results'][0])
        self.assertIn('updated_at', response.data['results'][0])
        self.assertIn('details', response.data['results'][0])
        self.assertIn('min_price', response.data['results'][0])
        self.assertIn('min_delivery_time', response.data['results'][0])
        self.assertIn('user_details', response.data['results'][0])
        
    def test_offer_min_price(self):
        response = self.client.get(self.url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['results'][0]['min_price'], 100)
    
    def test_offer_min_delivery_time(self):
        response = self.client.get(self.url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['results'][0]['min_delivery_time'], 5)
        
    def test_offer_user_details(self):
        response = self.client.get(self.url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('first_name', response.data['results'][0]['user_details'])
        self.assertIn('last_name', response.data['results'][0]['user_details'])
        self.assertIn('username', response.data['results'][0]['user_details'])
    
    def test_offer_details(self):
        response = self.client.get(self.url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results'][0]['details']), 3)
        for detail in response.data['results'][0]['details']:
            self.assertIn('id', detail)
            self.assertIn('url', detail)

class OfferFilterTests(APITestCase):
    def setUp(self):
        self.business_user1 = CustomUser.objects.create_user(
            username='max_business',
            email='max@business.de',
            password='password123',
            type='business'
        )
        
        self.business_user2 = CustomUser.objects.create_user(
            username='maria_business',
            email='maria@business.de',
            password='password123',
            type='business'
        )
        
        self.offer1 = Offer.objects.create(
            user=self.business_user1,
            title='Test Offer 1',
            description='This is a test offer.'
        )
        
        OfferDetail.objects.create(
            offer=self.offer1,
            title='Basic Package',
            revisions=1,
            delivery_time_in_days=5,
            price=100,
            features=['Feature 1', 'Feature 2'],
            offer_type='basic'
        )
        
        self.offer2 = Offer.objects.create(
            user=self.business_user2,
            title='Test Offer 2',
            description='This is a test offer.'
        )
        
        OfferDetail.objects.create(
            offer=self.offer2,
            title='Standard Package',
            revisions=2,
            delivery_time_in_days=10,
            price=200,
            features=['Feature 1', 'Feature 2'],
            offer_type='standard'
        )
        
        Offer.objects.filter(pk=self.offer1.pk).update(updated_at=timezone.now() - timedelta(days=1))
        
        self.url = reverse('offer-list')
        
    def test_offer_filter_creator_id(self):
        response = self.client.get(self.url, {'creator_id': self.business_user1.id})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['title'], 'Test Offer 1')
        
    def test_offer_filter_creator_id_400(self):
        response = self.client.get(self.url, {'creator_id': "invalid"})
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
    def test_offer_filter_min_price(self):
        response = self.client.get(self.url, {'min_price': 150})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertGreaterEqual(response.data['results'][0]['min_price'], 150)
        
    def test_offer_filter_min_price_400(self):
        response = self.client.get(self.url, {'min_price': "invalid"})
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
    def test_offer_filter_max_delivery_time(self):
        response = self.client.get(self.url, {'max_delivery_time': 7})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertLessEqual(response.data['results'][0]['min_delivery_time'], 7)
        
    def test_offer_filter_max_delivery_time_400(self):
        response = self.client.get(self.url, {'max_delivery_time': "invalid"})
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_offer_filter_search(self):
         response = self.client.get(self.url, {'search': 'Offer 1'})
         
         self.assertEqual(response.status_code, status.HTTP_200_OK)
         self.assertEqual(len(response.data['results']), 1)
         self.assertIn('Offer 1', response.data['results'][0]['title'])
         
    def test_offer_filter_ordering_min_price(self):
        response = self.client.get(self.url, {'ordering': 'min_price'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['results'][0]['title'], 'Test Offer 1')
        self.assertEqual(response.data['results'][1]['title'], 'Test Offer 2')
        
    def test_offer_filter_ordering_min_price_reverse(self):
        response = self.client.get(self.url, {'ordering': '-min_price'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['results'][0]['title'], 'Test Offer 2')
        self.assertEqual(response.data['results'][1]['title'], 'Test Offer 1')
        
    def test_offer_filter_ordering_updated_at(self):
        response = self.client.get(self.url, {'ordering': 'updated_at'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['results'][0]['title'], 'Test Offer 1')
        self.assertEqual(response.data['results'][1]['title'], 'Test Offer 2')
        
    def test_offer_filter_ordering_updated_at_reverse(self):
        response = self.client.get(self.url, {'ordering': '-updated_at'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['results'][0]['title'], 'Test Offer 2')
        self.assertEqual(response.data['results'][1]['title'], 'Test Offer 1')
        
class OfferPaginationTests(APITestCase):
    def setUp(self):
        self.business_user = CustomUser.objects.create_user(
            username='max_business',
            email='max@business.de',
            password='password123',
            type='business'
        )
        
        for i in range(7):
            Offer.objects.create(
                user=self.business_user,
                title=f'Offer {i}',
                description='Test {i}'
            )
        
        self.url = reverse('offer-list')
    
    def test_offer_filter_page_size(self):
        response = self.client.get(self.url, {'page_size': '2'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)
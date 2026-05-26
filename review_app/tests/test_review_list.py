from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from django.utils import timezone
from datetime import timedelta

from auth_app.models import CustomUser
from ..models import Review

class ReviewListTest(APITestCase):
    def setUp(self):
        self.business_user = CustomUser.objects.create_user(
            username='max_business',
            email='max@business.de',
            password='password123',
            type='business'
        )
        self.business_token, _ = Token.objects.get_or_create(user=self.business_user)
        
        self.reviewer = CustomUser.objects.create_user(
            username='maria_reviewer',
            email='maria@reviewer.de',
            password='password123',
            type='customer'
        )
        self.reviewer_token, _ = Token.objects.get_or_create(user=self.reviewer)
        
        self.review = Review.objects.create(
            business_user = self.business_user,
            reviewer = self.reviewer,
            rating = 4,
            description = "Very professional service.",
        )
        
        self.url = reverse('review-list')
    
    def test_review_success(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.business_token.key)
        
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_review_list_content(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.business_token.key)
        
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertIn('id', response.data[0])
        self.assertIn('business_user', response.data[0])
        self.assertIn('reviewer', response.data[0]),
        self.assertIn('rating', response.data[0])
        self.assertIn('description', response.data[0])
        self.assertIn('created_at', response.data[0])
        self.assertIn('updated_at', response.data[0])
    
    def test_review_unauthenticated(self):
        self.client.credentials()
        
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

class ReviewFilterAndOrderingTest(APITestCase):
    def setUp(self):
        self.business_user1 = CustomUser.objects.create_user(
            username='max_business',
            email='max@business.de',
            password='password123',
            type='business'
        )
        self.business_token1, _ = Token.objects.get_or_create(user=self.business_user1)
        
        self.business_user2 = CustomUser.objects.create_user(
            username='maximilian_business',
            email='maximilian@business.de',
            password='password123',
            type='business'
        )
        self.business_token2, _ = Token.objects.get_or_create(user=self.business_user2)
        
        self.reviewer1 = CustomUser.objects.create_user(
            username='maria_reviewer',
            email='maria@reviewer.de',
            password='password123',
            type='customer'
        )
        self.reviewer_token1, _ = Token.objects.get_or_create(user=self.reviewer1)
        
        self.reviewer2 = CustomUser.objects.create_user(
            username='mia_reviewer',
            email='mia@reviewer.de',
            password='password123',
            type='customer'
        )
        self.reviewer_token2, _ = Token.objects.get_or_create(user=self.reviewer2)
        
        self.review1 = Review.objects.create(
            business_user = self.business_user1,
            reviewer = self.reviewer1,
            rating = 4,
            description = "Very good service.",
        )
        
        self.review2 = Review.objects.create(
            business_user = self.business_user2,
            reviewer = self.reviewer2,
            rating = 1,
            description = "Very poor service.",
        )
        
        Review.objects.filter(pk=self.review1.pk).update(updated_at=timezone.now() - timedelta(days=1))
        
        self.url = reverse('review-list')
        
    def test_review_filter_business_user_id(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.business_token1.key)
        
        response = self.client.get(self.url, {'business_user_id': self.business_user1.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['description'], 'Very good service.')
    
    def test_review_filter_reviewer_id(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.reviewer_token1.key)        
        
        response = self.client.get(self.url, {'reviewer_id': self.reviewer1.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['description'], 'Very good service.')
        
    def test_review_ordering_rating(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.business_token1.key)
        
        response = self.client.get(self.url, {'ordering': 'rating'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['description'], "Very poor service.")
        self.assertEqual(response.data[1]['description'], "Very good service.")

    def test_review_ordering_rating_reverse(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.business_token1.key)
        
        response = self.client.get(self.url, {'ordering': '-rating'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[1]['description'], "Very poor service.")
        self.assertEqual(response.data[0]['description'], "Very good service.")
        
    def test_review_ordering_updated_at(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.business_token1.key)
        
        response = self.client.get(self.url, {'ordering': 'updated_at'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[1]['description'], "Very poor service.")
        self.assertEqual(response.data[0]['description'], "Very good service.")
    
    def test_review_ordering_updated_at_reverse(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.business_token1.key)
        
        response = self.client.get(self.url, {'ordering': '-updated_at'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['description'], "Very poor service.")
        self.assertEqual(response.data[1]['description'], "Very good service.")
        
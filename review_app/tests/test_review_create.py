from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token

from auth_app.models import CustomUser
from ..models import Review

class ReviewCreateTest(APITestCase):
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
        
        self.valid_payload = {
            "business_user": self.business_user.pk,
            "rating": 4,
            "description": "Everything was amazing!"
        }

        self.url = reverse('review-list')
        
    def test_review_create_success(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.reviewer_token.key)

        response = self.client.post(self.url, self.valid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('id', response.data)
        self.assertEqual(Review.objects.count(), 1)
        self.assertEqual(response.data['reviewer'], self.reviewer.pk)
    
    def test_review_create_duplicat(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.reviewer_token.key)

        self.client.post(self.url, self.valid_payload, format='json')
        response = self.client.post(self.url, self.valid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    
    def test_review_create_unauthenticated(self):
        self.client.credentials()

        response = self.client.post(self.url, self.valid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_review_create_forbidden(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.business_token.key)

        response = self.client.post(self.url, self.valid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
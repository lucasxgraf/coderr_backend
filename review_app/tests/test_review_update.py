from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token

from auth_app.models import CustomUser
from ..models import Review

class ReviewUpdateTest(APITestCase):
    def setUp(self):
        self.business_user = CustomUser.objects.create_user(
            username='max_business',
            email='max@business.de',
            password='password123',
            type='business'
        )
        self.business_token, _ = Token.objects.get_or_create(user=self.business_user)
        
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
        
        self.review = Review.objects.create(
            business_user = self.business_user,
            reviewer = self.reviewer1,
            rating = 4,
            description = "Very professional service.",
        )
        
        self.url = reverse('review-single', kwargs={'pk': self.review.pk})
    
    def test_review_update_success(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.reviewer_token1.key)
        data = {
            'rating' : 5,
            'description' : 'Updated: Exceptional service!'
        }

        response = self.client.patch(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_review_update_invalid_data(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.reviewer_token1.key)
        data = {
            'rating' : 7,
            'description' : 'Updated: Exceptional service!'
        }

        response = self.client.patch(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_review_update_unauthenticated(self):
        self.client.credentials()
        data = {
            'rating' : 5,
            'description' : 'Updated: Exceptional service!'
        }

        response = self.client.patch(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_review_update_forbidden(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.reviewer_token2.key)
        data = {
            'rating' : 5,
            'description' : 'Updated: Exceptional service!'
        }

        response = self.client.patch(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from auth_app.models import CustomUser

def create_test_users():
    business_user = CustomUser.objects.create_user(
        username='max_business',
        email='max@business.de',
        password='password123',
        type='business'
    )
    customer_user = CustomUser.objects.create_user(
        username='customer_jane',
        email='jane@customer.de',
        password='password123',
        type='customer'
    )
    return business_user, customer_user

def assert_profile_fields(response_data, is_business=False):
    for field in ['location', 'tel', 'description', 'working_hours']:
        if is_business or field not in ['working_hours', 'description']:
            assert field in response_data
            assert isinstance(response_data[field], str)
class ProfileBusinessListTests(APITestCase):
    def setUp(self):
        self.business_user, self.customer_user = create_test_users()

        token, _ = Token.objects.get_or_create(user=self.business_user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        
    def test_business_profile_list_success(self):
        url = reverse('business-profile')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        usernames = [profile['username'] for profile in response.data]
        self.assertEqual(len(response.data), 1)
        self.assertIn(self.business_user.username, usernames)
        self.assertNotIn(self.customer_user.username, usernames)
        
    def test_business_profile_list_unauthenticated(self):
        url = reverse('business-profile')
        self.client.credentials()
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
class ProfileCustomerListTests(APITestCase):
    def setUp(self):
        self.business_user, self.customer_user = create_test_users()

        token, _ = Token.objects.get_or_create(user=self.customer_user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        
    def test_customer_profile_list_success(self):
        url = reverse('customer-profile')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        usernames = [profile['username'] for profile in response.data]
        self.assertEqual(len(response.data), 1)
        self.assertIn(self.customer_user.username, usernames)
        self.assertNotIn(self.business_user.username, usernames)
        
    def test_customer_profile_list_unauthenticated(self):
        url = reverse('customer-profile')
        self.client.credentials()
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
class SingleProfileTests(APITestCase):
    def setUp(self):
        self.business_user, self.customer_user = create_test_users()

        token, _ = Token.objects.get_or_create(user=self.business_user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        
    def test_single_business_profile(self):
        url = reverse('profile-detail', kwargs={'pk': self.business_user.id})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        profile_data = response.data
        
        expected_fields = [
            'user', 
            'username', 
            'first_name', 
            'last_name', 
            'file',
            'uploaded_at', 
            'location', 
            'tel', 
            'description', 
            'working_hours', 
            'type',
            'email',
            'created_at',
        ]
        for field in expected_fields:
            self.assertIn(field, profile_data)
    
    def test_single_customer_profile(self):
        url = reverse('profile-detail', kwargs={'pk': self.customer_user.id})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        profile_data = response.data
        
        expected_fields = [
            'user', 
            'username', 
            'first_name', 
            'last_name', 
            'file',
            'uploaded_at',
            'type',
            'email',
            'created_at'
        ]
        for field in expected_fields:
            self.assertIn(field, profile_data)
    
    def test_profile_not_found(self):
        url = reverse('profile-detail', kwargs={'pk': 9999})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        
    def test_single_customer_profile_contains_all_fields(self):
        url = reverse('profile-detail', kwargs={'pk': self.customer_user.id})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        expected_fields = [
            'user', 
            'username', 
            'first_name', 
            'last_name', 
            'location', 
            'tel', 
            'description', 
            'working_hours', 
            'type'
        ]
        
        for field in expected_fields:
            self.assertIn(field, response.data)
        
        self.assertEqual(response.data['location'], "")
        self.assertEqual(response.data['working_hours'], "")
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from auth_app.models import CustomUser


class RegistrationViewTests(APITestCase):
    def setUp(self):
        self.user_data = {
            "username": "exampleUsername",
            "email": "example@mail.de",
            "password": "examplePassword",
            "repeated_password": "examplePassword",
            "type": "customer"
        }
    
    def test_registration_success(self):
        url = reverse('registration')
        response = self.client.post(url, self.user_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('token', response.data)
        self.assertIn('username', response.data)
        self.assertIn('email', response.data)
        self.assertIn('user_id', response.data)
        self.assertEqual(CustomUser.objects.count(), 1)

    # def test_registration_password_mismatch(self):
    #     pass
    
    # def test_registration_invalid_type(self):
    #     pass
    
    # def test_registration_duplicate_username(self):
    #     pass
    
    # def test_registration_duplicate_email(self):
    #     pass
    
    # def test_registration_missing_fields(self):
    #     pass
    

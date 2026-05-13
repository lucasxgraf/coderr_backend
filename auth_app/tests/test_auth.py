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
        self.assertIsInstance(response.data['user_id'], int)
        self.assertIsInstance(response.data['token'], str)
        self.assertEqual(CustomUser.objects.count(), 1)
        
    def test_registration_empty_fields(self):
        url = reverse('registration')
        user_data = self.user_data.copy()
        empty_fields = ['username', 'email', 'password', 'repeated_password', 'type']

        for field in empty_fields:
            with self.subTest(field=field):
                user_data[field] = ''
                response = self.client.post(url, user_data, format='json')
                self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
                self.assertEqual(CustomUser.objects.count(), 0)

    def test_registration_missing_fields(self):
        url = reverse('registration')
        user_data = self.user_data.copy()
        user_data.pop('email')

        response = self.client.post(url, user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(CustomUser.objects.count(), 0)
    
    def test_registration_password_mismatch(self):
        url = reverse('registration')
        user_data = self.user_data.copy()
        user_data['repeated_password'] = 'differentPassword'

        response = self.client.post(url, user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(CustomUser.objects.count(), 0)
    
    def test_registration_password_too_short(self):
        url = reverse('registration')
        user_data = self.user_data.copy()
        user_data['password'] = '123'
        user_data['repeated_password'] = '123'

        response = self.client.post(url, user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(CustomUser.objects.count(), 0)

    def test_registration_duplicate_username(self):
        url = reverse('registration')
        user_data = self.user_data.copy()
        self.client.post(url, user_data, format='json')

        response = self.client.post(url, user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(CustomUser.objects.count(), 1)

    def test_registration_duplicate_email(self):
        url = reverse('registration')
        user_data = self.user_data.copy()
        self.client.post(url, user_data, format='json')
        user_data['username'] = 'differentUsername'

        response = self.client.post(url, user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(CustomUser.objects.count(), 1)

    def test_registration_invalid_email(self):
        url = reverse('registration')
        user_data = self.user_data.copy()
        user_data['email'] = 'invalid_email'

        response = self.client.post(url, user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(CustomUser.objects.count(), 0)

    def test_registration_invalid_type(self):
        url = reverse('registration')
        user_data = self.user_data.copy()
        user_data['type'] = 'invalid_type'

        response = self.client.post(url, user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(CustomUser.objects.count(), 0)

class LoginViewTests(APITestCase):
    def setUp(self):
        self.user_data = {
            "username": "exampleUsername",
            "password": "examplePassword",
        }
        self.user = CustomUser.objects.create_user(
            email="example@mail.de",
            **self.user_data
        )
    
    def test_login_success(self):
        url = reverse('login')
        token_obj, created = Token.objects.get_or_create(user=self.user)
        
        response = self.client.post(url, self.user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('username', response.data)
        self.assertIn('email', response.data)
        self.assertIn('user_id', response.data)
        self.assertIsInstance(response.data['user_id'], int)
        self.assertIsInstance(response.data['token'], str)
   
    def test_login_invalid_username(self):
        url = reverse('login')
        user_data = self.user_data.copy()
        user_data['username'] = 'wrongUsername'

        response = self.client.post(url, user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
    def test_login_invalid_password(self):
        url = reverse('login')
        user_data = self.user_data.copy()
        user_data['password'] = 'wrongPassword'

        response = self.client.post(url, user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
    def test_login_missing_username(self):
        url = reverse('login')
        user_data = self.user_data.copy()
        user_data.pop('username')

        response = self.client.post(url, user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
    def test_login_missing_password(self):
        url = reverse('login')
        user_data = self.user_data.copy()
        user_data.pop('password')

        response = self.client.post(url, user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_login_empty_credentials(self):
        url = reverse('login')
        user_data = self.user_data.copy()
        user_data['username'] = ""
        user_data['password'] = ""

        response = self.client.post(url, user_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
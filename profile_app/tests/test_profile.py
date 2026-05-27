from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse

from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from auth_app.models import CustomUser


def create_test_users():
    """Create and return one business and one customer user for test setup."""
    business_user = CustomUser.objects.create_user(
        username='max_business',
        email='max@business.de',
        password='password123',
        type='business',
    )
    customer_user = CustomUser.objects.create_user(
        username='customer_jane',
        email='jane@customer.de',
        password='password123',
        type='customer',
    )
    return business_user, customer_user


def assert_profile_fields(response_data, is_business=False):
    """Assert that expected string profile fields are present in the response."""
    for field in ['location', 'tel', 'description', 'working_hours']:
        if is_business or field not in ['working_hours', 'description']:
            assert field in response_data
            assert isinstance(response_data[field], str)


class ProfileBusinessListTests(APITestCase):
    """Tests for the business profile list endpoint."""

    def setUp(self):
        self.business_user, self.customer_user = create_test_users()
        token, _ = Token.objects.get_or_create(user=self.business_user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

    def test_business_profile_list_success(self):
        """Authenticated user receives only business profiles."""
        url = reverse('business-profile')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        usernames = [profile['username'] for profile in response.data]
        self.assertEqual(len(response.data), 1)
        self.assertIn(self.business_user.username, usernames)
        self.assertNotIn(self.customer_user.username, usernames)

    def test_business_profile_list_unauthenticated(self):
        """Unauthenticated request to business list returns 401."""
        url = reverse('business-profile')
        self.client.credentials()
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class ProfileCustomerListTests(APITestCase):
    """Tests for the customer profile list endpoint."""

    def setUp(self):
        self.business_user, self.customer_user = create_test_users()
        token, _ = Token.objects.get_or_create(user=self.customer_user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

    def test_customer_profile_list_success(self):
        """Authenticated user receives only customer profiles."""
        url = reverse('customer-profile')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        usernames = [profile['username'] for profile in response.data]
        self.assertEqual(len(response.data), 1)
        self.assertIn(self.customer_user.username, usernames)
        self.assertNotIn(self.business_user.username, usernames)

    def test_customer_profile_list_unauthenticated(self):
        """Unauthenticated request to customer list returns 401."""
        url = reverse('customer-profile')
        self.client.credentials()
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class SingleProfileTests(APITestCase):
    """Tests for retrieving a single profile by pk."""

    def setUp(self):
        self.business_user, self.customer_user = create_test_users()
        token, _ = Token.objects.get_or_create(user=self.business_user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

    def test_single_business_profile(self):
        """Business profile response contains all expected fields."""
        url = reverse('profile-detail', kwargs={'pk': self.business_user.id})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        expected_fields = [
            'user', 'username', 'first_name', 'last_name', 'file',
            'uploaded_at', 'location', 'tel', 'description',
            'working_hours', 'type', 'email', 'created_at',
        ]
        for field in expected_fields:
            self.assertIn(field, response.data)

    def test_single_customer_profile(self):
        """Customer profile response contains all expected fields."""
        url = reverse('profile-detail', kwargs={'pk': self.customer_user.id})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        expected_fields = [
            'user', 'username', 'first_name', 'last_name', 'file',
            'uploaded_at', 'type', 'email', 'created_at',
        ]
        for field in expected_fields:
            self.assertIn(field, response.data)

    def test_single_profile_unauthenticated(self):
        """Unauthenticated request to profile detail returns 401."""
        url = reverse('profile-detail', kwargs={'pk': self.customer_user.id})
        self.client.credentials()
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_profile_not_found(self):
        """Request for a non-existent profile pk returns 404."""
        url = reverse('profile-detail', kwargs={'pk': 9999})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_single_customer_profile_contains_all_fields(self):
        """Empty string fields are never returned as null."""
        url = reverse('profile-detail', kwargs={'pk': self.customer_user.id})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        expected_fields = [
            'user', 'username', 'first_name', 'last_name',
            'location', 'tel', 'description', 'working_hours', 'type',
        ]
        for field in expected_fields:
            self.assertIn(field, response.data)
        self.assertEqual(response.data['location'], "")
        self.assertEqual(response.data['working_hours'], "")


class UpdateProfileTests(APITestCase):
    """Tests for patching profile fields."""

    def setUp(self):
        self.business_user, self.customer_user = create_test_users()
        self.token, _ = Token.objects.get_or_create(user=self.business_user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

    def test_patch_own_profile_success(self):
        """Owner can update their own profile fields."""
        url = reverse('profile-detail', kwargs={'pk': self.business_user.id})
        response = self.client.patch(url, {'first_name': 'Maria', 'location': 'Berlin'}, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.business_user.refresh_from_db()
        self.assertEqual(self.business_user.first_name, 'Maria')
        self.assertEqual(self.business_user.location, 'Berlin')
        self.assertEqual(response.data['first_name'], 'Maria')

    def test_patch_other_profile_forbidden(self):
        """Patching another user's profile returns 403."""
        url = reverse('profile-detail', kwargs={'pk': self.customer_user.id})
        response = self.client.patch(url, {'first_name': 'Hacker'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_patch_unauthenticated(self):
        """Unauthenticated patch request returns 401."""
        url = reverse('profile-detail', kwargs={'pk': self.business_user.id})
        self.client.credentials()
        response = self.client.patch(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_patch_profile_not_found(self):
        """Patching a non-existent profile pk returns 404."""
        url = reverse('profile-detail', kwargs={'pk': 9999})
        response = self.client.patch(url, {'first_name': 'Ghost'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_patch_file_sets_uploaded_at(self):
        """Uploading a file sets the uploaded_at timestamp on the profile."""
        url = reverse('profile-detail', kwargs={'pk': self.business_user.id})
        file = SimpleUploadedFile("test.jpg", b"file_content", content_type="image/jpeg")
        response = self.client.patch(url, {'file': file}, format='multipart')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNotNone(response.data['uploaded_at'])

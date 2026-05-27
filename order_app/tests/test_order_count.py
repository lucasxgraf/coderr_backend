from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token

from auth_app.models import CustomUser
from ..models import Order


class OrderCountTest(APITestCase):
    def setUp(self):
        self.business_user = CustomUser.objects.create_user(
            username='max_business',
            email='max@business.de',
            password='password123',
            type='business'
        )
        self.business_token, _ = Token.objects.get_or_create(
            user=self.business_user)

        self.customer_user = CustomUser.objects.create_user(
            username='maria_customer',
            email='maria@customer.de',
            password='password123',
            type='customer'
        )
        self.customer_token, _ = Token.objects.get_or_create(
            user=self.customer_user)

        self.order = Order.objects.create(
            customer_user=self.customer_user,
            business_user=self.business_user,
            title='Test Order',
            revisions=1,
            delivery_time_in_days=2,
            price=150,
            features=['Feature 1', 'Feature 2'],
            offer_type='basic',
            status='in_progress',
        )

        self.url = reverse(
            'order-count',
            kwargs={
                'business_user_id': self.business_user.id})

    def test_order_count_success(self):
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' +
            self.business_token.key)

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['order_count'], 1)

    def test_order_count_unauthenticated(self):
        self.client.credentials()

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_order_count_business_user_not_found(self):
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' +
            self.business_token.key)
        url = reverse('order-count', kwargs={'business_user_id': 9999})

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class CompletedOrderCountTest(APITestCase):
    def setUp(self):
        self.business_user = CustomUser.objects.create_user(
            username='max_business',
            email='max@business.de',
            password='password123',
            type='business'
        )
        self.business_token, _ = Token.objects.get_or_create(
            user=self.business_user)

        self.customer_user = CustomUser.objects.create_user(
            username='maria_customer',
            email='maria@customer.de',
            password='password123',
            type='customer'
        )
        self.customer_token, _ = Token.objects.get_or_create(
            user=self.customer_user)

        self.order = Order.objects.create(
            customer_user=self.customer_user,
            business_user=self.business_user,
            title='Test Order',
            revisions=1,
            delivery_time_in_days=2,
            price=150,
            features=['Feature 1', 'Feature 2'],
            offer_type='basic',
            status='completed',
        )

        self.url = reverse('completed-order-count',
                           kwargs={'business_user_id': self.business_user.id})

    def test_order_count_success(self):
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' +
            self.business_token.key)

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['completed_order_count'], 1)

    def test_order_count_unauthenticated(self):
        self.client.credentials()

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_order_count_business_user_not_found(self):
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' +
            self.business_token.key)
        url = reverse(
            'completed-order-count',
            kwargs={
                'business_user_id': 9999})

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import CustomUser, Newsletter

class UserRegisterAPITestCase(APITestCase):
    def test_user_registration(self):
        url = reverse('api:register')
        data = {
            'email': 'test@example.com',
            'name': 'omid',
            'family': 'naderi',
            'password': 'password123',
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(CustomUser.objects.count(), 1)
        self.assertEqual(CustomUser.objects.get().email, 'test@example.com')

class UserActivationAPITestCase(APITestCase):
    def test_user_activation(self):
        user = CustomUser.objects.create(email='test@example.com', name='Omid', family='Naderi')
        user.active_code = '123456'  # Set the activation code
        user.save()

        url = reverse('api:auth')
        data = {
            'email': 'test@example.com',
            'active_code': '123456',
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        user.refresh_from_db()
        self.assertTrue(user.is_active)

class SubscribeNewsletterAPITestCase(APITestCase):
    def test_subscribe_newsletter(self):
        user = CustomUser.objects.create(email='test@example.com', name='Omid', family='Naderi')
        url = reverse('api:subscribe')
        data = {'email': 'test@example.com'}
        self.client.force_authenticate(user=user)
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        user.refresh_from_db()
        self.assertTrue(user.subscribed_newletter)

class UnsubscribeNewsletterAPITestCase(APITestCase):
    def test_unsubscribe_newsletter(self):
        user = CustomUser.objects.create(email='test@example.com', name='Omid', family='Naderi', subscribed_newletter=True)
        url = reverse('api:unsubscribe')
        data = {'email': 'test@example.com'}
        self.client.force_authenticate(user=user)
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        user.refresh_from_db()
        self.assertFalse(user.subscribed_newletter)

class NewsletterAPITestCase(APITestCase):
    def test_create_newsletter(self):
        user = CustomUser.objects.create(email='admin@example.com', name='Admin', family='User', is_admin=True)
        url = reverse('api:send')
        data = {
            'subject': 'Test Newsletter',
            'content': 'This is a test newsletter content.',
        }
        self.client.force_authenticate(user=user)
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Newsletter.objects.count(), 1)

class LoginAPITestCase(APITestCase):
    def test_user_login(self):
        user = CustomUser.objects.create(email='test@example.com', name='Omid', family='Naderi', is_active=True)
        url = reverse('api:login')
        data = {
            'email': 'test@example.com',
            'password': 'password123',
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)

class LogoutAPITestCase(APITestCase):
    def test_user_logout(self):
        user = CustomUser.objects.create(email='test@example.com', name='Omid', family='Naderi', is_active=True)
        url = reverse('api:logout')
        self.client.force_authenticate(user=user)
        response = self.client.post(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)



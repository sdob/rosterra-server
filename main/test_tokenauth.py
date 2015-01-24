from django.core.urlresolvers import reverse

from rest_framework import status
from rest_framework.test import APIRequestFactory
from rest_framework.test import APITestCase, APIClient
from rest_framework.test import force_authenticate

from rest_framework.authtoken.models import Token
from custom_auth.models import User

class TokenAuthenticationTestCase(APITestCase):
    def setUp(self):
        self.u = User.objects.create_user(email='u@example.com', password='p')
    
    def test_correct_creds_return_token(self):
        res = self.client.post(
                reverse('token-auth'),
                data={'username': 'u@example.com', 'password': 'p'}, format='json')
        self.assertEqual(res.data['token'], Token.objects.get(user=self.u).key)

    def test_correct_creds_return_http_200(self):
        res = self.client.post(
                reverse('token-auth'),
                data={'username': 'u@example.com', 'password': 'p'}, format='json')
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_incorrect_creds_do_not_return_token(self):
        res = self.client.post(
                reverse('token-auth'),
                data={'username': 'u@example.com', 'password': 'bad'}, format='json')
        self.assertNotIn('token', res.data.keys())

    def test_incorrect_creds_return_http_400(self):
        res = self.client.post(
                reverse('token-auth'),
                data={'username': 'u@example.com', 'password': 'bad'}, format='json')
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

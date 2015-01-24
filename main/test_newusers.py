from django.core.urlresolvers import reverse
from django.db.models import Q

from rest_framework import status
from rest_framework.test import APITestCase, APIRequestFactory
from rest_framework.authtoken.models import Token
from custom_auth.models import User
from models import Company, Employment, Location, Employee
from permissions import IsManagerOrReadOnly
from serializers import EmployeeSerializer

class UserCreationTestCase(APITestCase):

    def setUp(self):
        self.u = User.objects.create_user(email='foo@example.com', password='p')
        # Force authentication --- we're not testing token-based auth here
        self.client.force_authenticate(user=self.u)

    def test_token_created(self):
        self.assertTrue(Token.objects.filter(user=self.u).exists())

    def test_creating_user_creates_employee(self):
        self.assertTrue(Employee.objects.filter(user=self.u).exists())

    def test_new_user_list_returns_200(self):
        response = self.client.get(reverse('employee-list'))
        expected_value = status.HTTP_200_OK
        self.assertEqual(response.status_code, expected_value)

    def test_new_user_can_see_themselves(self):
        response = self.client.get(reverse('employee-list'))
        expected_response = EmployeeSerializer(
                Employee.objects.filter(user=self.u),
                many=True)
        self.assertEqual(expected_response.data, response.data)


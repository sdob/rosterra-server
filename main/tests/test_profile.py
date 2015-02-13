from rest_framework.test import APITestCase, APIRequestFactory
from custom_auth.models import User
from main.models import Company, Employment, Location, Employee

class ProfileTestCase(APITestCase):

    def setUp(self):
        self.e = User.objects.create_user(email="e@example.com", password="p").profile
        self.gorman = Employee.objects.get(user__email="gorman@example.com")

    def test_get_profile(self):
        self.client.force_authenticate(self.gorman.user)
        response = self.client.get('/employees/%d/profile/' % self.gorman.id)
        #self.client.force_authenticate(self.e.user)
        #response = self.client.get('/employees/%d/profile/' % self.e.id)
        #print response

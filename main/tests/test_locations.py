import datetime
from django.utils import timezone
from django.core.urlresolvers import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIRequestFactory
from custom_auth.models import User
from main.models import Company, Employment, Location, RosterEntry, Activity
from main.permissions import IsManagerOrReadOnly

class LocationCreationDeletionTestCase(APITestCase):
    
    def test_unpermitted_location_create_fails(self):
        """Try to create a Location when not a manager."""
        self.client.force_authenticate(user=self.timc.user)
        response = self.client.post(reverse('location-list'), self.data)
        self.assertFalse(Location.objects.filter(name='redmond').exists())

    def test_unpermitted_location_create_returns_403(self):
        self.client.force_authenticate(user=self.timc.user)
        response = self.client.post(reverse('location-list'), self.data)
        expected_response = status.HTTP_403_FORBIDDEN
        self.assertTrue(response.status_code, expected_response)

    def test_permitted_location_create_succeeds(self):
        self.client.force_authenticate(user=self.billg.user)
        response = self.client.post(reverse('location-list'), self.data)
        self.assertTrue(Location.objects.filter(name='redmond').exists())

    def test_permitted_location_create_returns_201(self):
        self.client.force_authenticate(user=self.billg.user)
        response = self.client.post(reverse('location-list'), self.data)
        expected_response = status.HTTP_201_CREATED
        self.assertTrue(response.status_code, expected_response)

    def setUp(self):
        self.timc = User.objects.create_user(email='timc@example.com',
                name='timc', password='p').profile
        self.billg = User.objects.create_user(email='billg@example.com',
                name='billg', password='p').profile
        self.microsoft = Company.objects.create(name='microsoft')
        Employment.objects.create(employee=self.timc, company=self.microsoft,
                is_manager=False).save()
        Employment.objects.create(employee=self.billg, company=self.microsoft,
                is_manager=True).save()
        self.data = {'name': 'redmond', 'company': self.microsoft.id}

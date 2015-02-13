import datetime
from django.utils import timezone
from django.core.urlresolvers import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIRequestFactory
from custom_auth.models import User
from main.models import Company, Employment, Location, RosterEntry, Activity
from main.permissions import IsManagerOrReadOnly

class CompanyDeletionTestCase(APITestCase):

    def test_unpermitted_company_delete_fails(self):
        self.client.force_authenticate(user=self.timc.user)
        self.response = self.client.delete(
                reverse('company-detail', args=[self.microsoft.id])
                )
        self.assertTrue(Company.objects.filter(id=self.microsoft.id).exists())

    def test_unpermitted_company_delete_returns_403(self):
        self.client.force_authenticate(user=self.timc.user)
        self.response = self.client.delete(
                reverse('company-detail', args=[self.microsoft.id])
                )
        expected_value = status.HTTP_403_FORBIDDEN
        self.assertEqual(self.response.status_code, expected_value)

    def test_permitted_company_delete_succeeds(self):
        self.client.force_authenticate(user=self.billg.user)
        self.response = self.client.delete(
                reverse('company-detail', args=[self.microsoft.id])
                )
        self.assertFalse(Company.objects.filter(id=self.microsoft.id).exists())

    def test_permitted_company_delete_returns_204(self):
        self.client.force_authenticate(user=self.billg.user)
        self.response = self.client.delete(
                reverse('company-detail', args=[self.microsoft.id])
                )
        expected_value = status.HTTP_204_NO_CONTENT
        self.assertEqual(self.response.status_code, expected_value)

    def setUp(self):
        self.timc = User.objects.create_user(email='timc@example.com',
                name='Tim', password='p').profile
        self.microsoft = Company.objects.create(name="Microsoft")       
        Employment.objects.create(employee=self.timc, company=self.microsoft,
                is_manager=False).save()
        self.billg = User.objects.create_user(email='billg@example.com',
                name='billg', password='p').profile
        Employment.objects.create(employee=self.billg, company=self.microsoft,
                is_manager=True).save()


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

class IsManagerOrReadOnlyTestCase(APITestCase):

    def setUp(self):
        # 2 employees
        self.timc = User.objects.create_user(email='timc@example.com', name='Tim', password='p').profile
        self.billg = User.objects.create_user(email='billg@example.com', password='p').profile
        # 2 companies
        self.microsoft = Company.objects.create(name="Microsoft")       
        self.apple = Company.objects.create(name="Apple")
        # timc works for both microsoft and apple but is only a manager at apple
        Employment.objects.create(employee=self.timc, company=self.apple, is_manager=True).save()
        Employment.objects.create(employee=self.timc, company=self.microsoft, is_manager=False).save()
        # billg just works for microsoft
        Employment.objects.create(employee=self.billg, company=self.microsoft, is_manager=True).save()
        # 4 locations, 2 for each company
        self.redmond = Location.objects.create(name="Redmond", company=self.microsoft)
        self.sandyford = Location.objects.create(name="Sandyford", company=self.microsoft)
        self.cupertino = Location.objects.create(name="Cupertino", company=self.apple)
        self.mayfield = Location.objects.create(name="Mayfield", company=self.apple)

import datetime
from django.utils import timezone
from django.core.urlresolvers import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIRequestFactory
from custom_auth.models import User
from main.models import Company, Employment, Location, RosterEntry, Activity
from main.permissions import IsManagerOrReadOnly

class Base(APITestCase):

    def setUp(self):
        """
        Set up for the base test scenarios is as follows:
        * User 'kenfi' is employed by Microsoft
        * User 'billg' is a manager at Microsoft
        * User 'bob' isn't employed by Microsoft
        """
        self.kenfi = User.objects.create_user(email='kenfi@example.com',
                name='Tim', password='p').profile
        self.microsoft = Company.objects.create(name="Microsoft")       
        self.billg = User.objects.create_user(email='billg@example.com',
                name='billg', password='p').profile
        self.microsoft.hire(self.kenfi)
        self.microsoft.hire(self.billg, is_manager=True)
        self.bob = User.objects.create_user(email='bob@example.com', password='p').profile



class Retrieve(Base):

    def setUp(self):
        super(Retrieve, self).setUp()
        self.url = reverse('company-detail', args=[self.microsoft.id])
    
    def test_staff_retrieve(self):
        "An user can retrieve the ID and name of a company they work for"
        self.client.force_authenticate(user=self.kenfi.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        d = response.data
        self.assertEqual(d.keys(), ['id', 'name'])
        self.assertEqual(d['id'], self.microsoft.id)
        self.assertEqual(d['name'], self.microsoft.name)

    def test_manager_retrieve(self):
        "A user can retrieve the ID and name of a company they manage"
        self.client.force_authenticate(user=self.billg.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        d = response.data
        self.assertEqual(d['id'], self.microsoft.id)
        self.assertEqual(d['name'], self.microsoft.name)

    def test_unpermitted_retrieve(self):
        "A user can't retrieve the ID and name of a company they don't work for"
        self.client.force_authenticate(user=self.bob.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertFalse('id' in response.data.keys())
        self.assertFalse('name' in response.data.keys())

    def test_unauthenticated_retrieve(self):
        "An unauthenticated user can't retrieve the ID and name of a company"
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertFalse('id' in response.data.keys())
        self.assertFalse('name' in response.data.keys())


class List(Base):

    def setUp(self):
        super(List, self).setUp()
        self.apple = Company.objects.create(name='Apple')
        self.apple.hire(self.kenfi)
        self.kenfi.join(self.apple)
        self.url = reverse('company-list')

    def test_list_returns_multiple_companies(self):
        "A user employed by multiple companies can get a list of all those companies"
        self.client.force_authenticate(user=self.kenfi.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        d = response.data
        self.assertEqual(len(d), 2)
        self.assertTrue({'id': self.microsoft.id, 'name': self.microsoft.name} in d)
        self.assertTrue({'id': self.apple.id, 'name': self.apple.name} in d)

    def test_list_returns_single_company(self):
        "A user employed by one company can get a list containing that company"
        self.client.force_authenticate(user=self.billg.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        d = response.data
        self.assertEqual(len(d), 1)
        self.assertTrue({'id': self.microsoft.id, 'name': self.microsoft.name} in d)

    def test_list_returns_no_companies(self):
        "A user employed by no companies can get an empty list"
        self.client.force_authenticate(user=self.bob.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)
    
    def test_unauthenticated_list(self):
        "An unauthenticated user can't get a list of companies"
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class Patch(Base):

    def setUp(self):
        super(Patch, self).setUp()
        self.url = reverse('company-detail', args=[self.microsoft.id])

    def test_staff_patch(self):
        """A user can't rename a company they're employed by"""
        self.client.force_authenticate(user=self.kenfi.user)
        data = {'name': 'Oracle'}
        response = self.client.patch(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

class Delete(Base):

    def setUp(self):
        super(Delete, self).setUp()
        self.url = reverse('company-detail', args=[self.microsoft.id])

    def test_staff_delete(self):
        "A user can't delete a company they are employed by"
        self.client.force_authenticate(user=self.kenfi.user)
        response = self.client.delete(self.url)
        self.assertTrue(Company.objects.filter(id=self.microsoft.id).exists())
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_non_employee_delete(self):
        "A user can't delete a company they aren't employed by"
        self.client.force_authenticate(user=self.bob.user)
        response = self.client.delete(self.url)
        self.assertTrue(Company.objects.filter(id=self.microsoft.id).exists())
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_manager_delete(self):
        "A user can delete a company they manage"
        self.client.force_authenticate(user=self.billg.user)
        response = self.client.delete(self.url)
        self.assertFalse(Company.objects.filter(id=self.microsoft.id).exists())
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_unauthenticated_delete(self):
        "An unauthenticated user can't delete a company"
        response = self.client.delete(self.url)
        self.assertTrue(Company.objects.filter(id=self.microsoft.id).exists())
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

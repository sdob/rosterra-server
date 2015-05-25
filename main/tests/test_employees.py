import datetime
from django.utils import timezone

from django.core.urlresolvers import reverse

from rest_framework import status
from rest_framework.test import APITestCase, APIRequestFactory

from country_utils import countries
from custom_auth.models import User
from main.models import Company, Employment, Location, RosterEntry, Activity,\
        Employee

class EmployeeTestCaseBase(APITestCase):

    def setUp(self):
        self.e = User.objects.create_user(email='e@example.com', name='fred', password='p').profile
        self.e.address_line_1 = "123 Fake Street"
        self.e.city = "Anytown"
        self.e.country = 'US'
        self.e.save()
        self.c = Company.objects.create(name="c")
        self.c.hire(self.e)
        self.e.join(self.c)
        # Another employee --- non-manager, same company
        self.e2 = User.objects.create_user(email='e2@example.com', password='p').profile
        self.c.hire(self.e2)
        self.e2.join(self.c)
        self.e2.save()
        # Employee from different company
        self.c2 = Company.objects.create(name='c2')
        self.e3 = User.objects.create_user(email='e3@example.com', password='p').profile
        self.c2.hire(self.e3)
        self.e3.join(self.c2)
        self.e3.save()


class Create(EmployeeTestCaseBase):

    def test_create_profile(self):
        count_employees = Employee.objects.all().count()
        data = {
                'user': self.e.user.id
                }
        self.client.force_authenticate(self.e.user)
        #response = self.client.post(reverse('employee-list'), data=data)
        #print response

class Retrieve(EmployeeTestCaseBase):

    def test_access_full_profile(self):
        self.client.force_authenticate(user=self.e.user)
        response = self.client.get(reverse('employee-detail', args=[self.e.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK) # status code
        d = response.data
        print d
        self.assertEqual(d['email'], self.e.email)
        self.assertEqual(d['name'], self.e.name)
        self.assertEqual(d['address_line_1'], self.e.address_line_1)
        self.assertEqual(d['city'], self.e.city)
    
    def test_access_same_company_not_manager(self):
        # Log in as a non-managerial employee of the same company
        e2 = self.e2
        self.client.force_authenticate(user=e2.user)
        response = self.client.get(reverse('employee-detail', args=[self.e.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Non-manager at same company gets user ID and name
        d = response.data
        self.assertEqual(d['id'], self.e.id)
        self.assertEqual(d['name'], self.e.name)
        # Nothing unexpected is present
        for k in ['email', 'address_line_1', 'address_line_2', 'city', 'country']:
            self.assertFalse(k in d.keys())

    def test_access_different_company(self):
        e3 = self.e3
        self.client.force_authenticate(user=e3.user)
        response = self.client.get(reverse('employee-detail', args=[self.e.id]))
        # Accessing another employee's profile returns a 404
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        d = response.data
        for k in ['id', 'name', 'email', 'address_line_1', 'address_line_2',
                'city', 'country']:
            self.assertFalse(k in d.keys())

    def test_same_company_and_manager(self):
        pass


class Patch(EmployeeTestCaseBase):

    def setUp(self):
        super(Patch, self).setUp()
        self.patch_url = reverse('employee-detail', args=[self.e.id])
        self.new_address = '742 Evergreen Terrace'
        self.data = {'id': self.e.id, 'address_line_1': self.new_address}

    def test_patch_own_profile(self):
        self.client.force_authenticate(user=self.e.user)
        response = self.client.patch(self.patch_url, data=self.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        e = Employee.objects.get(id=self.e.id)
        self.assertEqual(e.address_line_1, self.new_address)

    def test_patch_others_profile(self):
        old_address = Employee.objects.get(id=self.e.id).address_line_1
        self.client.force_authenticate(user=self.e2.user)
        response = self.client.patch(self.patch_url, data=self.data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(old_address, Employee.objects.get(id=self.e.id).address_line_1)

class Delete(EmployeeTestCaseBase):
    
    def setUp(self):
        super(Delete, self).setUp()
        self.delete_url = reverse('employee-detail', args=[self.e.id])

    def test_delete_own_profile(self):
        self.client.force_authenticate(user=self.e.user)
        response = self.client.delete(self.delete_url)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        self.assertTrue(Employee.objects.filter(id=self.e.id).exists())

    def test_delete_other_profile(self):
        self.client.force_authenticate(user=self.e2.user)
        response = self.client.delete(self.delete_url)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        self.assertTrue(Employee.objects.filter(id=self.e.id).exists())


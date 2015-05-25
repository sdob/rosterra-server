from json import loads
from django.core.urlresolvers import reverse

from rest_framework.test import APIRequestFactory
from rest_framework.test import APITestCase, APIClient
from rest_framework.test import force_authenticate
from rest_framework import status

from custom_auth.models import User

from main.models import Employee, Company, Employment as ECM, Location
from main.serializers import LocationSerializer, EmployeeSerializer,\
        CompanySerializer


class LocationViewDetailTestCase(APITestCase):

    def setUp(self):
        # 2 users
        self.timc = User.objects.create_user(email='timc@example.com', name='Tim', password='p')
        self.billg = User.objects.create_user(email='billg@example.com', password='p')
        # 2 companies
        self.microsoft = Company.objects.create(name="Microsoft")       
        self.apple = Company.objects.create(name="Apple")
        # timc works for both microsoft and apple and is a manager at apple
        ECM.objects.create(employee=self.timc.profile, company=self.apple, is_manager=True).save()
        ECM.objects.create(employee=self.timc.profile, company=self.microsoft, is_manager=False).save()
        # billg just works for microsoft
        ECM.objects.create(employee=self.billg.profile, company=self.microsoft, is_manager=True).save()
        # 4 locations, 2 for each company
        self.redmond = Location.objects.create(name="Redmond", company=self.microsoft)
        self.sandyford = Location.objects.create(name="Sandyford", company=self.microsoft)
        self.cupertino = Location.objects.create(name="Cupertino", company=self.apple)
        self.mayfield = Location.objects.create(name="Mayfield", company=self.apple)

    def test_users_can_list_locations_of_all_companies_employing_them(self):
        self.client.force_authenticate(user=self.timc)
        response = self.client.get(reverse('location-list'))
        self.assertEqual(len(response.data), 
                len(self.microsoft.locations.all()) + len(self.apple.locations.all()))

    def test_users_cant_list_locations_of_companies_not_employing_them(self):
        self.client.force_authenticate(user=self.billg)
        response = self.client.get(reverse('location-list'))
        self.assertFalse(LocationSerializer(self.cupertino).data in response.data)

    def test_users_can_view_locations_of_companies_employing_them(self):
        self.client.force_authenticate(user=self.timc)
        response = self.client.get(reverse('location-detail', args=[self.cupertino.id]))
        self.assertEqual(LocationSerializer(self.cupertino).data, response.data)

    def test_users_cant_view_locations_of_companies_not_employing_them(self):
        billg = self.billg
        loc = self.cupertino
        self.client.force_authenticate(user=self.billg)
        response = self.client.get(reverse('location-detail', args=[loc.id]))
        self.assertNotEqual(LocationSerializer(loc).data, response.data)

    def test_users_cant_view_locations_of_companies_not_employing_them_status(self):
        billg = self.billg
        loc = self.cupertino
        self.client.force_authenticate(user=self.billg)
        response = self.client.get(reverse('location-detail', args=[loc.id]))
        self.assertTrue(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_users_can_filter_locations_by_company(self):
        self.client.force_authenticate(user=self.timc)
        response = self.client.get('%s?company=%d' % (reverse('location-list'), self.apple.id))
        expected_response = LocationSerializer(
                Location.objects.filter(company=self.apple), many=True
                )
        self.assertEqual(expected_response.data, response.data)


class EmployeeViewDetailTestCase(APITestCase):

    def setUp(self):
        # Set up 2 companies and several users 
        self.timc = User.objects.create_user(email='timc@example.com', name='Tim', password='p')
        self.jonyi = User.objects.create_user(email='jonyi@example.com', password='p')
        self.billg = User.objects.create_user(email='billg@example.com', password='p')
        self.steveb = User.objects.create_user(email='steveb@example.com', password='p')
        self.microsoft = Company.objects.create(name="Microsoft")       
        self.apple = Company.objects.create(name="Apple")
        ECM.objects.create(employee=self.timc.profile, company=self.apple, is_manager=True).save()
        ECM.objects.create(employee=self.jonyi.profile, company=self.apple, is_manager=False).save()
        ECM.objects.create(employee=self.billg.profile, company=self.microsoft, is_manager=True).save()
        ECM.objects.create(employee=self.steveb.profile, company=self.microsoft, is_manager=False).save()
        self.redmond = Location.objects.create(name="Redmond", company=self.microsoft)
        self.sandyford = Location.objects.create(name="Sandyford", company=self.microsoft)
        self.cupertino = Location.objects.create(name="Cupertino", company=self.apple)
        self.mayfield = Location.objects.create(name="Mayfield", company=self.apple)

    def test_managers_can_list_employees_of_their_companies(self):
        timc = self.timc
        # Log in as an Apple manager 
        self.client.force_authenticate(user=timc)
        response = self.client.get(reverse('employee-list'))
        # Check that Apple employees are present and Microsoft employees absent
        expected_response = EmployeeSerializer(Employee.objects.filter(companies=self.apple), many=True)
        self.assertEqual(expected_response.data, response.data)
    
    def test_users_cannot_view_employees_in_different_companies(self):
        self.client.force_authenticate(self.jonyi)
        response = self.client.get(reverse('employee-detail', args=[self.billg.id]))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_requesting_your_own_profile_data_returns_http_200(self):
        self.client.force_authenticate(self.timc)
        response = self.client.get(reverse('employee-detail', args=[self.timc.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_users_can_view_their_own_profiles(self):
        self.client.force_authenticate(self.timc)
        response = self.client.get(reverse('employee-detail', args=[self.timc.id]))
        expected_response = EmployeeSerializer(Employee.objects.get(id=self.timc.id))
        self.assertEqual(expected_response.data, response.data)


class CompanyViewDetailTestCase(APITestCase):

    def setUp(self):
        # 2 users
        self.timc = User.objects.create_user(email='timc@example.com', name='Tim', password='p')
        self.billg = User.objects.create_user(email='billg@example.com', password='p')
        # 2 companies
        self.microsoft = Company.objects.create(name="Microsoft")       
        self.apple = Company.objects.create(name="Apple")
        # timc works for both microsoft and apple
        ECM.objects.create(employee=self.timc.profile, company=self.apple, is_manager=True).save()
        ECM.objects.create(employee=self.timc.profile, company=self.microsoft, is_manager=False).save()
        # billg just works for microsoft
        ECM.objects.create(employee=self.billg.profile, company=self.microsoft, is_manager=True).save()
        # 4 locations, 2 for each company
        self.redmond = Location.objects.create(name="Redmond", company=self.microsoft)
        self.sandyford = Location.objects.create(name="Sandyford", company=self.microsoft)
        self.cupertino = Location.objects.create(name="Cupertino", company=self.apple)
        self.mayfield = Location.objects.create(name="Mayfield", company=self.apple)

    def test_list_companies(self):
        self.client.force_authenticate(user=self.timc)
        response = self.client.get(reverse('company-list'))
        self.assertEqual(len(response.data), 2)
        #expected_response = CompanySerializer(Company.objects.filter(id__in=[self.apple.id, self.microsoft.id]), many=True)
        #self.assertEqual(expected_response.data, response.data)

    def test_list_companies_return_single(self):
        self.client.force_authenticate(user=self.billg)
        self.client.login(username=self.billg.email, password='p')
        response = self.client.get(reverse('company-list'))
        expected_response = CompanySerializer([self.microsoft], many=True)
        self.assertEqual(response.data, expected_response.data)

    def test_view_company_allowed_status(self):
        self.client.force_authenticate(user=self.timc)
        response = self.client.get(reverse('company-detail', args=[self.apple.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_view_company_disallowed_status(self):
        self.client.force_authenticate(user=self.billg)
        response = self.client.get(reverse('company-detail', args=[self.apple.id]))
        expected_status_code = status.HTTP_404_NOT_FOUND
        self.assertEqual(response.status_code, expected_status_code)

    def test_view_company_disallowed(self):
        self.client.force_authenticate(user=self.billg)
        response = self.client.get(reverse('company-detail', args=[self.apple.id]))
        expected_absent_response = CompanySerializer(self.apple)
        self.assertNotEqual(expected_absent_response.data, response.data)

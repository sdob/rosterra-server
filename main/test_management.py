from rest_framework.test import APITestCase

from custom_auth.models import User
from main.models import Company, Employment, Location

class ManagementCheckTestCase(APITestCase):

    def setUp(self):
        # 2 employees
        self.timc = User.objects.create_user(email='timc@example.com',
                name='Tim', password='p').profile
        self.billg = User.objects.create_user(email='billg@example.com',
                password='p').profile
        # 2 companies
        self.microsoft = Company.objects.create(name="Microsoft")       
        self.apple = Company.objects.create(name="Apple")
        # timc works for both microsoft and apple but is only a manager at apple
        Employment.objects.create(employee=self.timc, company=self.apple,
                is_manager=True).save()
        Employment.objects.create(employee=self.timc, company=self.microsoft,
                is_manager=False).save()
        # billg just works for microsoft
        Employment.objects.create(employee=self.billg, company=self.microsoft,
                is_manager=True).save()
        # 4 locations, 2 for each company
        self.redmond = Location.objects.create(name="Redmond", company=self.microsoft)
        self.sandyford = Location.objects.create(name="Sandyford", company=self.microsoft)
        self.cupertino = Location.objects.create(name="Cupertino", company=self.apple)
        self.mayfield = Location.objects.create(name="Mayfield", company=self.apple)

    def test_manager_is_manager_of_company(self):
        self.assertTrue(self.apple.is_managed_by(self.timc))

    def test_employee_is_not_manager_of_company(self):
        self.assertFalse(self.apple.is_managed_by(self.billg))

    def test_non_employee_is_not_manager_of_company(self):
        self.assertFalse(self.apple.is_managed_by(self.billg))

    def test_manager_is_manager_of_location(self):
        self.assertTrue(self.cupertino.is_managed_by(self.timc))

    def test_employee_is_not_manager_of_location(self):
        self.assertFalse(self.redmond.is_managed_by(self.timc))

    def test_non_employee_is_not_manager_of_location(self):
        self.assertFalse(self.cupertino.is_managed_by(self.billg))

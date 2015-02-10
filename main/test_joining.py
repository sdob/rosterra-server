from rest_framework.test import APITestCase, APIRequestFactory
from custom_auth.models import User
from models import Company, Employment, Location, Employee

class JoiningTestCase(APITestCase):

    def setUp(self):
        self.c = Company.objects.create(name='c')
        self.e = User.objects.create(email='foo@example.com', password='x').profile

    def test_employee_acceptance_is_recorded(self):
        self.e.join(self.c)
        self.assertTrue(self.e.has_accepted_employment_from(self.c))
    
    def test_company_acceptance_is_recorded(self):
        self.c.hire(self.e)
        self.assertTrue(self.c.has_accepted(self.e))

    def test_employee_acceptance_doesnt_create_company_acceptance(self):
        self.e.join(self.c)
        self.assertFalse(self.c.has_accepted(self.e))

    def test_company_acceptance_doesnt_create_employee_acceptance(self):
        self.c.hire(self.e)
        self.assertFalse(self.e.has_accepted_employment_from(self.c))
    
    def test_joining_something_that_isnt_a_company_throws_exception(self):
        location = Location.objects.create(name='x', company=self.c)
        try:
            self.e.join(location)
            self.fail("Didn't raise ValueError")
        except ValueError, e:
            pass

    def test_hiring_something_that_isnt_a_company_throws_exception(self):
        location = Location.objects.create(name='x', company=self.c)
        try:
            self.c.hire(location)
            self.fail("Didn't raise ValueError")
        except ValueError, e:
            pass

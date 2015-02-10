from rest_framework.test import APITestCase, APIRequestFactory
from rest_framework.renderers import JSONRenderer

from .serializers import CompanySerializer as CS, CompanyManagementSerializer as CMS
from .models import Company, Employee
from custom_auth.models import User

class CompanySerializerTestCase(APITestCase):

    def setUp(self):
        self.c = Company.objects.create(name="Company")
        for i in xrange(10):
            e = User.objects.create(email="u%d@example.com" % i, password="p").profile
            e.name = "Employee %d" % i
            e.save()
            self.c.hire(e)
            e.join(self.c)

    def test_regular_serializer_doesnt_list_employees(self):
        s = CS(self.c)
        self.assertFalse('employees' in s.data)

    def test_management_serializer_lists_employees(self):
        s = CMS(self.c)
        self.assertTrue('employees' in s.data)

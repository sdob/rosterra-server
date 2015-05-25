import datetime
from django.utils import timezone
from django.core.urlresolvers import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIRequestFactory
from rest_framework.request import Request
from django.http import HttpRequest

from custom_auth.models import User
from main.models import Company, Employment, Location, RosterEntry, Activity
from main.permissions import IsManagerOrReadOnly, IsOwnerOrReadOnly

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

class IsOwnerOrReadOnlyTestCase(APITestCase):

    pass

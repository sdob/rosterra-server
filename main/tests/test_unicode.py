# -*- coding: utf8 -*-

from rest_framework.test import APITestCase

from custom_auth.models import User
from main.models import Company, Employment, Location
from main.serializers import LocationSerializer

class UnicodeLocationNameTestCase(APITestCase):

    def setUp(self):
        self.c = Company.objects.create(name='FrobozzCo')

    def test_can_create_and_save_unicode_location(self):
        l = Location(name=u"ó", company=self.c)
        l.save()

    def test_can_serialize_unicode_location(self):
        l = Location(name=u"ó", company=self.c)
        l.save()
        s = LocationSerializer(instance=l)

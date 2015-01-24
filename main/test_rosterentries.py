from django.core.urlresolvers import reverse

from rest_framework import status
from rest_framework.test import APITestCase, APIRequestFactory

from custom_auth.models import User
from models import Company, Employment, Location, RosterEntry

class RosterEntryTestCase(APITestCase):
    pass

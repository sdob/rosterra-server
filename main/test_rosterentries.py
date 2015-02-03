import datetime
from django.utils import timezone

from django.core.urlresolvers import reverse

from rest_framework import status
from rest_framework.test import APITestCase, APIRequestFactory

from custom_auth.models import User
from models import Company, Employment, Location, RosterEntry, Activity

class RosterEntryTestCase(APITestCase):

    def setUp(self):
        self.c = Company.objects.create(name='c')
        self.e = User.objects.create(email="u@example.com", password='p').profile
        self.c.hire(self.e)
        self.e.join(self.c)
        self.manager = User.objects.create(email='m@example.com', password='p').profile
        self.c.hire(self.manager)
        self.manager.join(self.c)
        ecm = Employment.objects.get(employee=self.manager, company=self.c)
        ecm.is_manager = True
        ecm.save()
        self.start = timezone.now()
        self.end = self.start + datetime.timedelta(hours=1)
        self.a = Activity.objects.create(name='a', company=self.c)
        self.base_data = {
                'company': self.c.id,
                'employee': self.e.id,
                'activity': self.a.id,
                'start': self.start.strftime('%Y-%m-%dT%H:%M:%S'),
                'end': self.end.strftime('%Y-%m-%dT%H:%M:%S')
                }

    def test_non_manager_cant_create_roster_entry(self):
        self.client.force_authenticate(user=self.e.user)
        response = self.client.post(
                reverse('roster_entry-list'),
                data=self.base_data
                )
        self.assertEquals(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertFalse(RosterEntry.objects.filter(company=self.c).exists())

    def test_manager_can_create_roster_entry(self):
        self.client.force_authenticate(user=self.manager.user)
        response = self.client.post(
                reverse('roster_entry-list'),
                data=self.base_data)
        self.assertEquals(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(RosterEntry.objects.filter(company=self.c).exists())
    
    def test_bad_start_end_times_return_400(self):
        self.client.force_authenticate(user=self.manager.user)
        data = {_: self.base_data[_] for _ in self.base_data}
        data['start'], data['end'] = data['end'], data['start']
        response = self.client.post(
                reverse('roster_entry-list'),
                data=data)
        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)

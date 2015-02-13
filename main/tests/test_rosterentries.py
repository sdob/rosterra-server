import datetime
from django.utils import timezone

from django.core.urlresolvers import reverse

from rest_framework import status
from rest_framework.test import APITestCase, APIRequestFactory

from custom_auth.models import User
from models import Company, Employment, Location, RosterEntry, Activity

class RosterEntryTestCaseBase(APITestCase):
    def setUp(self):
        # Company
        self.c = Company.objects.create(name='c')
        # Non-manager user
        self.e = User.objects.create(email="u@example.com", password='p').profile
        self.c.hire(self.e)
        self.e.join(self.c)
        # Manager user
        self.manager = User.objects.create(email='m@example.com', password='p').profile
        self.c.hire(self.manager)
        self.manager.join(self.c)
        ecm = Employment.objects.get(employee=self.manager, company=self.c)
        ecm.is_manager = True
        ecm.save()
        # Create two activities
        self.a = Activity.objects.create(name='a', company=self.c)
        self.a2 = Activity.objects.create(name='b', company=self.c)
        # RosterEntry
        self.start = timezone.now()
        self.end = self.start + timezone.timedelta(hours=1)
        self.base_data = {
                'company': self.c.id,
                'employee': self.e.id,
                'activity': self.a.id,
                'start': self.start.strftime('%Y-%m-%dT%H:%M:%S'),
                'end': self.end.strftime('%Y-%m-%dT%H:%M:%S')
                }
        RosterEntry.objects.create(company=self.c,
                employee=self.e,
                activity=self.a,
                start=self.start,
                end=self.end
                )
        # Get the old RosterEntry
        self.re_old = RosterEntry.objects.get(employee=self.e.id)
        # Store a count of the RosterEntries
        self.count = RosterEntry.objects.all().count()

class ListTestCase(RosterEntryTestCaseBase):

    def setUp(self):
        super(ListTestCase, self).setUp()

    def test_filter_on_start_time_include(self):
        self.client.force_authenticate(user=self.manager.user)
        response = self.client.get(reverse('roster_entry-list') + 
                '?start=%s' % (self.start - timezone.timedelta(hours=1)).strftime('%Y-%m-%dT%H:%M:%S'))
        self.assertEqual(len(response.data), 1)

    def test_filter_on_bad_start_time(self):
        self.client.force_authenticate(user=self.manager.user)
        self.client.post(reverse('roster_entry-list'), data=self.base_data)
        response = self.client.get(reverse('roster_entry-list') + '?start=')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_filter_on_bad_end_time(self):
        self.client.force_authenticate(user=self.manager.user)
        response = self.client.get(reverse('roster_entry-list') + '?end=')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_filter_on_start_time_exclude(self):
        self.client.force_authenticate(user=self.manager.user)
        response = self.client.get(reverse('roster_entry-list') + 
                '?start=%s' % (self.start + timezone.timedelta(hours=1)).strftime('%Y-%m-%dT%H:%M:%SZ'))
        self.assertEqual(len(response.data), 0)

    def test_filter_on_end_time_include(self):
        self.client.force_authenticate(user=self.manager.user)
        end_string = (self.end + timezone.timedelta(hours=1)).strftime('%Y-%m-%dT%H:%M:%SZ')
        response = self.client.get(reverse('roster_entry-list') + '?end=%s' % end_string)
        self.assertEqual(len(response.data), 1)

    def test_filter_on_end_time_exclude(self):
        self.client.force_authenticate(user=self.manager.user)
        self.client.post(reverse('roster_entry-list'), data=self.base_data)
        end_string = (self.end - timezone.timedelta(hours=1)).strftime('%Y-%m-%dT%H:%M:%SZ')
        response = self.client.get(reverse('roster_entry-list') + '?end=%s' % end_string)
        self.assertEqual(len(response.data), 0)
    

class CreateTestCase(RosterEntryTestCaseBase):

    def setUp(self):
        super(CreateTestCase, self).setUp()

    def test_non_manager_cant_create_roster_entry(self):
        count = RosterEntry.objects.filter(company=self.c).count()
        self.client.force_authenticate(user=self.e.user)
        response = self.client.post(
                reverse('roster_entry-list'),
                data=self.base_data
                )
        self.assertEquals(response.status_code, status.HTTP_403_FORBIDDEN)
        new_count = RosterEntry.objects.filter(company=self.c).count()
        self.assertEquals(count, new_count)

    def test_manager_can_create_roster_entry(self):
        count = RosterEntry.objects.filter(company=self.c).count()
        self.client.force_authenticate(user=self.manager.user)
        response = self.client.post(
                reverse('roster_entry-list'),
                data=self.base_data)
        self.assertEquals(response.status_code, status.HTTP_201_CREATED)
        new_count = RosterEntry.objects.filter(company=self.c).count()
        self.assertEquals(new_count, count + 1)

    def test_bad_start_end_times_return_400(self):
        self.client.force_authenticate(user=self.manager.user)
        data = {_: self.base_data[_] for _ in self.base_data}
        data['start'], data['end'] = data['end'], data['start']
        response = self.client.post(
                reverse('roster_entry-list'),
                data=data)
        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)


class PatchUpdateBase(RosterEntryTestCaseBase):
    def setUp(self):
        super(PatchUpdateBase, self).setUp()
        # Build a stub for the PATCH data
        self.new_data = {'id': self.re_old.id}
        # Get the PATCH URL
        self.patch_url = reverse('roster_entry-detail', args=[self.re_old.id])


class PermittedPatchUpdates(PatchUpdateBase):
    def setUp(self):
        super(PermittedPatchUpdates, self).setUp()
        # Log in as manager
        self.client.force_authenticate(user=self.manager.user)

    def test_patch_change_start_time(self):
        new_start = self.re_old.start + timezone.timedelta(minutes=1)
        self.new_data['start'] = new_start
        response = self.client.patch(self.patch_url, data=self.new_data)
        # Status code is OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # No extra entry has been created
        self.assertEqual(1, RosterEntry.objects.filter(employee=self.e.id).count())
        re = RosterEntry.objects.get(employee=self.e.id)
        # Same ID
        self.assertEqual(self.re_old.id, re.id)
        # Correct start time
        self.assertEqual(new_start, re.start)
        # Different from old start time
        self.assertNotEqual(self.re_old.start, re.start)

    def test_patch_change_end_time(self):
        new_end = self.re_old.end + timezone.timedelta(minutes=1)
        self.new_data['end'] = new_end
        response = self.client.patch(self.patch_url, data=self.new_data)
        # Status code is OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # No extra entry has been created
        self.assertEqual(1, RosterEntry.objects.filter(employee=self.e.id).count())
        re = RosterEntry.objects.get(employee=self.e.id)
        # Same ID
        self.assertEqual(self.re_old.id, re.id)
        # Correct end time
        self.assertEqual(new_end, re.end)
        # Different from old end time
        self.assertNotEqual(self.re_old.end, re.end)

    def test_patch_change_employee(self):
        self.new_data['employee'] = self.manager.id
        response = self.client.patch(self.patch_url, data=self.new_data)
        # Status code is OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # No new entry has been created
        self.assertEqual(self.count, RosterEntry.objects.all().count())
        # Now the employee has no RosterEntries and the manager has one
        self.assertEqual(0, RosterEntry.objects.filter(employee=self.e.id).count())
        self.assertEqual(1, RosterEntry.objects.filter(employee=self.manager.id).count())
        re = RosterEntry.objects.get(employee=self.manager.id)
        # Same ID
        self.assertEqual(self.re_old.id, re.id)
        # Correct employee
        self.assertEqual(self.manager.id, re.employee.id)

    def test_patch_change_activity(self):
        self.new_data['activity'] = self.a2.id
        response = self.client.patch(self.patch_url, data=self.new_data)
        # Status code is OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # No new entry has been created
        self.assertEqual(self.count, RosterEntry.objects.all().count())
        # Now the first activity has no roster entries and the second has one
        self.assertEqual(0, RosterEntry.objects.filter(activity=self.a.id).count())
        self.assertEqual(1, RosterEntry.objects.filter(activity=self.a2.id).count())
        re = RosterEntry.objects.get(activity=self.a2.id)
        # Same ID
        self.assertEqual(self.re_old.id, re.id)
        # Correct activity
        self.assertEqual(self.a2.id, re.activity.id)


class UnpermittedPatchUpdates(PatchUpdateBase):
    def setUp(self):
        super(UnpermittedPatchUpdates, self).setUp()
        # Log in as employee
        self.client.force_authenticate(user=self.e.user)

    def test_patch_change_start_time(self):
        new_start = self.re_old.start + timezone.timedelta(minutes=1)
        self.new_data['start'] = new_start
        response = self.client.patch(self.patch_url, data=self.new_data)
        # Status code is 403
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        # No extra entry has been created
        self.assertEqual(1, RosterEntry.objects.filter(employee=self.e.id).count())
        re = RosterEntry.objects.get(employee=self.e.id)
        # Same ID
        self.assertEqual(self.re_old.id, re.id)
        # Correct start time
        self.assertEqual(self.re_old.start, re.start)

    def test_patch_change_end_time(self):
        new_end = self.re_old.end + timezone.timedelta(minutes=1)
        self.new_data['end'] = new_end
        response = self.client.patch(self.patch_url, data=self.new_data)
        # Status code is 403
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        # No extra entry has been created
        self.assertEqual(1, RosterEntry.objects.filter(employee=self.e.id).count())
        re = RosterEntry.objects.get(employee=self.e.id)
        # Same ID
        self.assertEqual(self.re_old.id, re.id)
        # Correct end time
        self.assertEqual(self.re_old.end, re.end)

    def test_patch_change_employee(self):
        self.new_data['employee'] = self.manager.id
        response = self.client.patch(self.patch_url, data=self.new_data)
        # Status code is 403
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        # No new entry has been created
        self.assertEqual(self.count, RosterEntry.objects.all().count())
        # The re-assignment failed
        self.assertEqual(0, RosterEntry.objects.filter(employee=self.manager.id).count())
        self.assertEqual(1, RosterEntry.objects.filter(employee=self.e.id).count())
        # Check that the RosterEntry in the database is OK
        re = RosterEntry.objects.get(employee=self.e.id)
        # Same ID
        self.assertEqual(self.re_old.id, re.id)
        # Correct employee
        self.assertEqual(self.e.id, re.employee.id)

    def test_patch_change_activity(self):
        self.new_data['activity'] = self.a2.id
        response = self.client.patch(self.patch_url, data=self.new_data)
        # Status code is 403
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        # No new entry has been created
        self.assertEqual(self.count, RosterEntry.objects.all().count())
        # The re-assignment failed
        self.assertEqual(1, RosterEntry.objects.filter(activity=self.a.id).count())
        self.assertEqual(0, RosterEntry.objects.filter(activity=self.a2.id).count())
        # Check that the original RosterEntry is OK
        re = RosterEntry.objects.get(activity=self.a.id)
        # Same ID
        self.assertEqual(self.re_old.id, re.id)
        # Correct activity ID
        self.assertEqual(self.a.id, re.activity.id)

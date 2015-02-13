# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.utils import timezone


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_data_migration'),
    ]

    def add_roster_entries_and_activities(apps, schema_editor):
        Company = apps.get_model('main', 'Company')
        Activity = apps.get_model('main', 'Activity')
        Employee = apps.get_model('main', 'Employee')
        RosterEntry = apps.get_model('main', 'RosterEntry')
        # Create some activities for the Weyland-Yutani Corporation!
        wy = Company.objects.get(name='Weyland-Yutani')
        fighting_aliens = Activity.objects.create(name="Fighting xenomorphs",
                company=wy)
        gorman = Employee.objects.get(user__email='gorman@example.com')
        first_start_date = timezone.datetime(2015, 2, 5, 9, tzinfo=timezone.utc)
        # Three months of fighting xenomorphs for Gorman
        for i in xrange(1,101):
            start_time = first_start_date + timezone.timedelta(days=i)
            end_time = start_time + timezone.timedelta(hours=8)
            re = RosterEntry.objects.create(
                    employee=gorman,
                    company=wy,
                    start=start_time,
                    end=end_time,
                    activity=fighting_aliens)

    def rollback(apps, schema_editor):
        Activity = apps.get_model('main', 'Activity')
        Employee = apps.get_model('main', 'Employee')
        RosterEntry = apps.get_model('main', 'RosterEntry')
        # Remove all created activities
        Activity.objects.all().delete()
        # Remove all created roster entries
        RosterEntry.objects.all().delete()

    operations = [
            migrations.RunPython(add_roster_entries_and_activities, reverse_code=rollback),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.utils import timezone


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0008_auto_20150211_1932'),
    ]

    def roster_gorman_for_frobozzco(apps, schema_editor):
        Company = apps.get_model('main', 'Company')
        Activity = apps.get_model('main', 'Activity')
        Employee = apps.get_model('main', 'Employee')
        RosterEntry = apps.get_model('main', 'RosterEntry')
        gorman = Employee.objects.get(user__email='gorman@example.com')
        frobozzco = Company.objects.get(name="FrobozzCo")
        # Create some activities
        zorkmid_collection = Activity.objects.create(
                name="Zorkmid collection",
                company=frobozzco)
        being_eaten_by_a_grue = Activity.objects.create(
                name="Being eaten by a grue",
                company=frobozzco)
        # Roster Gorman for some of these, starting 5/2/2015 @ 9.00.
        # They conflict with his duties at Weyland-Yutani, but that's not
        # my problem.
        first_start_date = timezone.datetime(2015, 2, 5, 9, tzinfo=timezone.utc)
        for i in xrange(1,101):
            start_time = first_start_date + timezone.timedelta(days=i)
            end_time = start_time + timezone.timedelta(hours=6)
            if i % 2 == 0:
                re = RosterEntry.objects.create(
                        employee=gorman,
                        company=frobozzco,
                        start=start_time,
                        end=end_time,
                        activity=zorkmid_collection)
            else:
                re = RosterEntry.objects.create(
                        employee=gorman,
                        company=frobozzco,
                        start=start_time,
                        end=end_time,
                        activity=being_eaten_by_a_grue
                        )

    def rollback(apps, schema_editor):
        Company = apps.get_model('main', 'Company')
        Activity = apps.get_model('main', 'Activity')
        Employee = apps.get_model('main', 'Employee')
        RosterEntry = apps.get_model('main', 'RosterEntry')
        frobozzco = Company.objects.filter(name="Frobozzco")
        RosterEntry.objects.filter(company__in=frobozzco).delete()
        Activity.objects.filter(company__in=frobozzco).delete()


    operations = [
            migrations.RunPython(roster_gorman_for_frobozzco, reverse_code=rollback),
            ]


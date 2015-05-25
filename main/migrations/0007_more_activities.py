# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.utils import timezone


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_roster_entries'),
    ]

    def add_stuff_for_ferro_and_vasquez(apps, schema_editor):
        Company = apps.get_model('main', 'Company')
        Activity = apps.get_model('main', 'Activity')
        Employee = apps.get_model('main', 'Employee')
        RosterEntry = apps.get_model('main', 'RosterEntry')
        # Create some more activities for the Weyland-Yutani Corporation
        wy = Company.objects.get(name='Weyland-Yutani')
        piloting_dropship = Activity.objects.create(name="Piloting dropship", company=wy)
        never_being_mistaken_for_a_man = Activity.objects.create(
                name="Never being mistaken for a man",
                company=wy
                )
        ferro = Employee.objects.get(user__email='ferro@example.com')
        vasquez = Employee.objects.get(user__email="vasquez@example.com")
        bishop = Employee.objects.get(user__email="bishop@example.com")
        first_start_date = timezone.datetime(2015, 2, 5, 9, tzinfo=timezone.utc)
        # Three months of piloting dropships 6 hr/day every other day for Ferro
        for i in xrange(1,101,2):
            start_time = first_start_date + timezone.timedelta(days=i)
            end_time = start_time + timezone.timedelta(hours=6)
            re = RosterEntry.objects.create(
                    employee=ferro,
                    company=wy,
                    start=start_time,
                    end=end_time,
                    activity=piloting_dropship)
        # Bishop can pilot the dropship too!
        for i in xrange(1,101,2):
            start_time = first_start_date + timezone.timedelta(days=i) + timezone.timedelta(hours=6)
            end_time = start_time + timezone.timedelta(hours=6)
            re = RosterEntry.objects.create(
                    employee=bishop,
                    company=wy,
                    start=start_time,
                    end=end_time,
                    activity=piloting_dropship)
        # Vasquez has never been mistaken for a man and nor will she be
        for i in xrange(1,101,3):
            start_time = first_start_date + timezone.timedelta(days=i)
            end_time = start_time + timezone.timedelta(hours=12)
            re = RosterEntry.objects.create(
                    employee=vasquez,
                    company=wy,
                    start=start_time,
                    end=end_time,
                    activity=never_being_mistaken_for_a_man)

    def rollback(apps, schema_editor):
        Activity = apps.get_model('main', 'Activity')
        Employee = apps.get_model('main', 'Employee')
        RosterEntry = apps.get_model('main', 'RosterEntry')
        piloting_dropship = Activity.objects.get(name="Piloting dropship")
        never_being_mistaken_for_a_man = Activity.objects.get(
                name="Never being mistaken for a man"
                )
        # Remove created roster entries
        RosterEntry.objects.filter(activity=piloting_dropship).delete()
        RosterEntry.objects.filter(activity=never_being_mistaken_for_a_man).delete()
        # Remove created activities
        piloting_dropship.delete()
        never_being_mistaken_for_a_man.delete()

    operations = [
            migrations.RunPython(add_stuff_for_ferro_and_vasquez, reverse_code=rollback),
    ]

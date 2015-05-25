# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.core.management import call_command

def add_data(apps, schema_editor):
    call_command('loaddata', 'sample_data.json')

def remove_data(apps, schema_editor):
    call_command('flush')

class Migration(migrations.Migration):

    dependencies = [
            #('main', '0004_country_company'),
            ('main', '0010_add_employee_addresses'),
            ]

    operations = [
            migrations.RunPython(add_data, reverse_code=remove_data)
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0007_more_activities'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rosterentry',
            name='company',
            field=models.ForeignKey(related_name=b'rosterentries', to='main.Company'),
        ),
        migrations.AlterField(
            model_name='rosterentry',
            name='employee',
            field=models.ForeignKey(related_name=b'rosterentries', to='main.Employee'),
        ),
    ]

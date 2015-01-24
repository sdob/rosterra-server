# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_auto_20150120_1403'),
    ]

    operations = [
        migrations.AddField(
            model_name='employment',
            name='accepted_by_company',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='employment',
            name='accepted_by_employee',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]

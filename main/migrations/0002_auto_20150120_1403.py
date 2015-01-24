# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.core import serializers

import rosterra

class Migration(migrations.Migration):

    def forward(apps, schema_editor):
        # Load companies from JSON file
        with open(rosterra.settings.BASE_DIR + "/main/fixtures/companies.json") as f:
            objects = serializers.deserialize('json', f)
            for obj in objects:
                obj.save()
        with open(rosterra.settings.BASE_DIR + "/main/fixtures/locations.json") as f:
            objects = serializers.deserialize('json', f)
            for obj in objects:
                obj.save()

    dependencies = [
            ('main', '0001_initial'),
    ]

    operations = [
            migrations.RunPython(forward)
    ]

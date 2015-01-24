# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Activity',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=72)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200)),
            ],
            options={
                'verbose_name': 'company',
                'verbose_name_plural': 'companies',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('user', models.OneToOneField(related_name='profile', to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Employment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date_added', models.DateTimeField(auto_now_add=True)),
                ('is_manager', models.BooleanField(default=False)),
                ('company', models.ForeignKey(to='main.Company')),
                ('employee', models.ForeignKey(to='main.Employee')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200)),
                ('company', models.ForeignKey(related_name='locations', to='main.Company')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='RosterEntry',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('start', models.DateTimeField()),
                ('end', models.DateTimeField()),
                ('activity', models.ForeignKey(to='main.Activity')),
                ('company', models.ForeignKey(related_name='activities', to='main.Company')),
                ('employee', models.ForeignKey(related_name='activities', to='main.Employee')),
            ],
            options={
                'verbose_name': 'roster_entry',
                'verbose_name_plural': 'roster_entries',
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='employment',
            unique_together=set([('employee', 'company')]),
        ),
        migrations.AddField(
            model_name='company',
            name='employees',
            field=models.ManyToManyField(related_name='companies', through='main.Employment', to='main.Employee'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='activity',
            name='company',
            field=models.ForeignKey(related_name='activity_types', to='main.Company'),
            preserve_default=True,
        ),
    ]

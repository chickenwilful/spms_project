# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('agents', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AgentIProperty',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200, null=True)),
                ('phone_number', models.CharField(max_length=20, null=True)),
                ('estate_name', models.CharField(max_length=200, null=True)),
                ('lic_number', models.CharField(max_length=20, null=True)),
                ('reg_number', models.CharField(max_length=20, null=True)),
                ('url', models.CharField(max_length=200, null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='AgentStProperty',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200, null=True)),
                ('phone_number', models.CharField(max_length=20, null=True)),
                ('estate_name', models.CharField(max_length=200, null=True)),
                ('lic_number', models.CharField(max_length=20, null=True)),
                ('reg_number', models.CharField(max_length=20, null=True)),
                ('url', models.CharField(max_length=200, null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Agent',
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
            name='BadNum',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('numstr', models.CharField(unique=True, max_length=10)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]

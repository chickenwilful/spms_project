# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('type', models.CharField(default=b'h', max_length=1, choices=[(b'c', b'Condo'), (b'd', b'HDB')])),
                ('name', models.CharField(max_length=200, null=True, blank=True)),
                ('room_count', models.IntegerField(null=True, blank=True)),
                ('year', models.IntegerField(null=True, blank=True)),
                ('month', models.IntegerField(null=True, blank=True)),
                ('address', models.CharField(max_length=200, null=True, blank=True)),
                ('postal_code', models.CharField(max_length=10, null=True, blank=True)),
                ('area_sqm_min', models.FloatField(null=True, blank=True)),
                ('area_sqm_max', models.FloatField(null=True, blank=True)),
                ('monthly_rent', models.FloatField(null=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]

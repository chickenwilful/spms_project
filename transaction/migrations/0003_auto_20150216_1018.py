# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('transaction', '0002_auto_20150204_1911'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='latitude',
            field=models.FloatField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='transaction',
            name='longitude',
            field=models.FloatField(null=True, blank=True),
            preserve_default=True,
        ),
    ]

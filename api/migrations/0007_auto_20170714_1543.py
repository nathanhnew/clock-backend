# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-07-14 20:43
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0006_remove_clock_metric'),
    ]

    operations = [
        migrations.AlterField(
            model_name='accountsettings',
            name='metric',
            field=models.IntegerField(default=3),
        ),
    ]

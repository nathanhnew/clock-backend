# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-07-14 20:46
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0007_auto_20170714_1543'),
    ]

    operations = [
        migrations.AlterField(
            model_name='accountsettings',
            name='metric',
            field=models.CharField(default='both', max_length=4),
        ),
    ]
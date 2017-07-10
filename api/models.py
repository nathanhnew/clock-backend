# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.conf import settings
# from django.core.validators import MaxValueValidator
# import jwt


class AccountSettings(models.Model):
    owner = models.OneToOneField(settings.AUTH_USER_MODEL,
                                 on_delete=models.CASCADE,
                                 related_name="settings")
    theme = models.CharField(max_length=50, default='')
    alerts = models.BooleanField(default=False)
    fullDay = models.BooleanField(default=True)
    metric = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = "settings"

    def __str__(self):
        return self.owner.username+' settings'


class City(models.Model):
    place_id = models.CharField(max_length=250, unique=True)
    name = models.CharField(max_length=250)
    country = models.CharField(max_length=250)
    lat = models.DecimalField(max_digits=9, decimal_places=6)
    lon = models.DecimalField(max_digits=9, decimal_places=6)
    tz = models.CharField(max_length=200)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "cities"


class Clock(models.Model):
    clock_id = models.AutoField(primary_key=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL,
                              on_delete=models.CASCADE,
                              related_name='clock')
    city = models.ForeignKey(City, on_delete=models.CASCADE,
                             related_name='city')
    fullDay = models.BooleanField(default=True)
    arrIndex = models.IntegerField()

    def __str__(self):
        return self.owner.username+' '+self.city.name

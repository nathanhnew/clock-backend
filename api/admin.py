# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from api.models import AccountSettings, City, Clock


admin.site.register(AccountSettings)
admin.site.register(City)
admin.site.register(Clock)

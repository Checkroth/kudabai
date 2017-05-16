# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
import fruits

class FruitAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'reg_date', 'unit_price')

admin.site.register(fruits.models.Fruit, FruitAdmin)
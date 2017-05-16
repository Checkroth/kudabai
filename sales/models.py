# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
import fruits

# Create your models here.
class Sale(models.Model):
    fruit = models.ForeignKey(fruits.models.Fruit)
    number = models.IntegerField()
    earnings = models.IntegerField()
    sales_date = models.DateTimeField()



# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Fruit(models.Model):
    name = models.CharField(max_length=255)
    reg_date = models.DateTimeField(auto_now_add=True)
    unit_price = models.IntegerField()

    def __unicode__(self):
        return self.name
    

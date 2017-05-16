# -*- coding: utf-8 -*-
from django import forms
import fruits

class FruitForm(forms.ModelForm):
    class Meta:
        model = fruits.models.Fruit
        fields = ['name', 'unit_price']
        labels = {
            'name': '名称',
            'unit_price': '単価'
        }
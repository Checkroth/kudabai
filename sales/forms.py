# -*- coding: utf-8 -*-
from django import forms
import sales

class SaleForm(forms.ModelForm):
    class Meta:
        model = sales.models.Sale
        fields = ['fruit', 'number', 'sales_date']
        labels = {
            'fruit': '果物',
            'number': '個数',
            'sales_date': '販売日時',
        }
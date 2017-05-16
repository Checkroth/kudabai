# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django import http, urls
import fruits
import fruits.forms

def mgmt_top(request):
    return render(request, 'top.html')

def master(request):
    fs = fruits.models.Fruit.objects.all()
    return render(request, 'master.html', {
        'fruits': fs
    })

def edit_fruit(request, fruit_id):
    if request.POST:
        inst = fruits.models.Fruit.objects.get(pk=fruit_id)
        form = fruits.forms.FruitForm(request.POST, instance=inst)
        form.save()
        return http.HttpResponseRedirect(urls.reverse('master'))
    fruit = fruits.models.Fruit.objects.get(pk=fruit_id)
    form = fruits.forms.FruitForm(instance=fruit)
    return render(request, 'editfruit.html', {
        'edit_form': form
    })

def del_fruit(request, fruit_id):
    fruits.models.Fruit.objects.get(pk=fruit_id).delete()
    return http.HttpResponseRedirect(urls.reverse('master'))

def add_fruit(request):
    if request.POST:
        form = fruits.forms.FruitForm(request.POST)
        form.save()
        return http.HttpResponseRedirect(urls.reverse('master'))
    form = fruits.forms.FruitForm()
    return render(request, 'addfruit.html', {
        'add_form': form
    })
    # return fruits.forms.FruitForm() 
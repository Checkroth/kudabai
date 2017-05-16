# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django import http, urls
import sales
import sales.forms
import csv
import codecs
import fruits
from datetime import datetime
from django.db.models.functions import TruncMonth, TruncDate
from django.db.models import Sum, Count
from collections import defaultdict, OrderedDict

def show_sales(request):
    sale_list = sales.models.Sale.objects.all().order_by('sales_date')
    failures = []
    if 'failures' in request.session:
        failures = request.session['failures']
        del request.session['failures']
    return render(request, 'sales.html', {
        'sales': sale_list,
        'failures': failures
    })

def add_sale(request):
    if request.POST:
        form = sales.forms.SaleForm(request.POST)
        if form.is_valid():
            sale = form.save(False)
            sale.earnings = sale.number * sale.fruit.unit_price
            sale.save()
            return http.HttpResponseRedirect(urls.reverse('show_sales'))
        else:
            return render(request, 'addsale.html', {
                'add_form': form,
            })
    form = sales.forms.SaleForm()
    return render(request, 'addsale.html', {
        'add_form': form,
    })


def edit_sale(request, sale_id):
    inst = sales.models.Sale.objects.get(pk=sale_id)
    if request.POST:
        form = sales.forms.SaleForm(request.POST, instance=inst)
        if form.is_valid():
            sale = form.save(False)
            sale.earnings = sale.number * sale.fruit.unit_price
            form.save()
            return http.HttpResponseRedirect(urls.reverse('show_sales'))
        else:
            return render(request, 'editsale.html', {
                'edit_form': form,
            })
    form = sales.forms.SaleForm(instance=inst)
    return render(request, 'editsale.html', {
        'edit_form': form
    })

def bulk_add_sale(request):
    failures = []
    if request.POST:
        csv_file = request.FILES['csv']
        dialect = csv.Sniffer().sniff(codecs.EncodedFile(csv_file, "utf-8").read(1024))
        csv_file.open()
        reader = csv.reader(codecs.EncodedFile(csv_file, "utf-8"), delimiter=str(u','), dialect=dialect)
        for line in reader:
            if len(line) == 4:
                try:
                    fname = fruits.models.Fruit.objects.filter(name=line[0]).first()
                    count = line[1]
                    earning = line[2]
                    date = datetime.strptime(line[3], "%Y-%m-%d %H:%M")
                    sales.models.Sale.objects.create(fruit=fname, number=count, earnings=earning, sales_date=date)
                except:
                    failures.append(line)
    request.session['failures'] = failures
    return http.HttpResponseRedirect(urls.reverse('show_sales'))
    
def del_sale(request, sale_id):
    sales.models.Sale.objects.get(pk=sale_id).delete()
    return http.HttpResponseRedirect(urls.reverse('show_sales'))

def sales_stats(request):
    # 月別の計算
    trunc_month = sales.models.Sale.objects \
        .annotate(month=TruncMonth('sales_date'))

    third_month = trunc_month \
        .values('month') \
        .order_by('-month') \
        .distinct()[:3]

    # len(third_month) used because third_month.last() gets outside queryset
    monthly = trunc_month \
        .filter(month__gte=third_month[len(third_month)-1]['month']) \
        .values('month', 'fruit') \
        .annotate(total=Sum('earnings'), c=Sum('number'))

    mgs = OrderedDict()
    for m in monthly:
        mgs.setdefault(m['month'], []).append({
            'fruit': fruits.models.Fruit.objects.get(pk=m['fruit']), 
            'count': m['c'], 
            'sales_value': m['total']
            })
    month_groups = OrderedDict(sorted(mgs.items(), reverse=True))
    
    for m in month_groups:
        month_groups[m].append({
            'grand_total': sum(month['sales_value'] for month in month_groups[m])
        })


    # 日別の計算
    trunc_day = sales.models.Sale.objects \
        .annotate(day=TruncDate('sales_date'))

    third_day = trunc_day \
        .values('day') \
        .order_by('-day') \
        .distinct()[:3]

    daily = trunc_day \
        .filter(day__gte=third_day[len(third_day)-1]['day']) \
        .values('day', 'fruit') \
        .annotate(total=Sum('earnings'), c=Sum('number')) \
        .order_by('-sales_date')

    dgs = OrderedDict()
    for d in daily:
        dgs.setdefault(d['day'], []).append({
            'fruit': fruits.models.Fruit.objects.get(pk=d['fruit']),
            'count': d['c'],
            'sales_value': d['total']
        })
    day_groups = OrderedDict(sorted(dgs.items(), reverse=True))

    for d in day_groups:
        day_groups[d].append({'grand_total': sum(day['sales_value'] for day in day_groups[d])})

    # 全ての計算
    sales_total = sales.models.Sale.objects.all() \
        .aggregate(Sum('earnings'))

    return render(request, "salesstats.html", {
        'months': month_groups,
        'days': day_groups,
        'sales_total': sales_total,
    })

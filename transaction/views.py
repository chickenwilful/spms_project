from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from json_utils import json_success

# Create your views here.
import re
from transaction.forms import FilterForm
from transaction.models import Transaction


def misc(request):
    return HttpResponse("hehe")


def map(request, template='map.html'):

    transactions = Transaction.objects.filter(latitude__isnull=True)

    address_list = [trans.address for trans in transactions]
    address_list = set(address_list)
    return render(request, template, {'count': len(address_list),
                                      'address_list': address_list})


def coordinate(request):
    if request.GET:
        addr = request.GET['addr']
        lat = request.GET['lat']
        lng = request.GET['lng']
        print addr
        transactions = Transaction.objects.filter(address=addr)
        print len(transactions)

        for trans in transactions:
            trans.latitude = lat
            trans.longitude = lng
            trans.save()
        return HttpResponse("done")
    else:
        return HttpResponse("not done")


def camelcase(str):
    new_str = re.sub(r'^\s+|\s+$|\s+(?=\s)', '', str)
    return new_str.title()


def chart_retrieve(request, transactions):
    chart = {}

    cnt = [[0 for month in range(0, 13)] for year in range(0, 2016)]
    amt = [[0 for month in range(0, 13)] for year in range(0, 2016)]
    for transaction in transactions:
        if transaction.year and transaction.month and transaction.monthly_rent:
            year, month = transaction.year, transaction.month
            cnt[year][month] += 1
            amt[year][month] += transaction.monthly_rent

    chart['price'] = []
    chart['count'] = []

    for year in range(2012, 2016):
        for month in range(1, 13):
            if year < 2015 or month == 1:
                if cnt[year][month] > 0:
                    chart['price'].append(round(amt[year][month] / cnt[year][month]))
                else:
                    chart['price'].append(None)
                chart['count'].append(cnt[year][month])
    return chart


def transaction_list(request, estimate=False):
    MAX_LENGTH = 200
    if not request.POST or request.GET:
        form = FilterForm()
        transactions = Transaction.objects.all()
        result_count = len(transactions)
        chart = chart_retrieve(request, transactions)

        if len(transactions) > MAX_LENGTH:
            transactions = transactions[:MAX_LENGTH]

        return render(request, 'transaction_list.html', {'transactions': transactions,
                                                         'result_count': result_count,
                                                         'chart': chart,
                                                         'form': form})
    else:
        # Handle the form
        type = request.POST['type']
        name = camelcase(request.POST['name'])
        postal_code = request.POST['postal_code']
        address = camelcase(request.POST['address'])
        room_count = request.POST['room_count']

        if type != '':
            transactions = Transaction.objects.filter(type=type)
        else:
            transactions = Transaction.objects.all()

        if name != "":
            transactions = transactions.filter(name=name)

        if address != "":
            transactions = transactions.filter(address=address)

        if room_count == "u":
            transactions = transactions.filter(room_count=None)
        elif room_count != "":
            transactions = transactions.filter(room_count=room_count)

        if postal_code != "":
            if not estimate:
                transactions = transactions.filter(postal_code=postal_code)
            else:
                postal_code = postal_code[:len(postal_code)-1]
                transactions = [trans for trans in transactions if trans.postal_code and trans.postal_code.startswith(postal_code)]

        result_count = len(transactions)
        form = FilterForm(request.POST)
        chart = chart_retrieve(request, transactions)
        if len(transactions) > MAX_LENGTH:
            transactions = transactions[:MAX_LENGTH]
        return render(request, 'transaction_list.html', {'transactions': transactions,
                                                         'form': form,
                                                         'chart': chart,
                                                         'result_count': result_count})


def transaction_list_estimate(request):
    return transaction_list(request, estimate=True)
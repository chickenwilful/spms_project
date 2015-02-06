from django.http import HttpResponse
from django.shortcuts import render
from json_utils import json_success

# Create your views here.
import re
from transaction.forms import FilterForm
from transaction.models import Transaction


def camelcase(str):
    new_str = re.sub(r'^\s+|\s+$|\s+(?=\s)', '', str)
    return new_str.title()


def chart(request):
    return render(request, 'chart.html')


def chart_retrieve(request, transactions):
    chart = {}

    cnt = [[0 for month in range(0, 13)] for year in range(0, 2016)]
    amt = [[0 for month in range(0, 13)] for year in range(0, 2016)]
    for transaction in transactions:
        if transaction.year and transaction.month and transaction.monthly_rent:
            year, month = transaction.year, transaction.month
            cnt[year][month] += 1
            amt[year][month] += transaction.monthly_rent

    for year in range(2010, 2016):
        chart[year] = []
        for month in range(1, 13):
            print cnt[year][month], amt[year][month]
            if cnt[year][month] > 0:
                chart[year].append(round(amt[year][month] / cnt[year][month]))
            else:
                chart[year].append(0)
    return chart


def transaction_list(request):
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

        if postal_code != "":
            transactions = transactions.filter(postal_code=postal_code)

        if address != "":
            transactions = transactions.filter(address=address)

        if room_count == "u":
            transactions = transactions.filter(room_count=None)
        elif room_count != "":
            transactions = transactions.filter(room_count=room_count)

        result_count = len(transactions)
        form = FilterForm(request.POST)
        chart = chart_retrieve(request, transactions)
        if len(transactions) > MAX_LENGTH:
            transactions = transactions[:MAX_LENGTH]
        return render(request, 'transaction_list.html', {'transactions': transactions,
                                                         'form': form,
                                                         'chart': chart,
                                                         'result_count': result_count})

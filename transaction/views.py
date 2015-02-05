from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
import re
from transaction.forms import FilterForm
from transaction.models import Transaction


def camelcase(str):
    new_str = re.sub(r'^\s+|\s+$|\s+(?=\s)', '', str)
    return new_str.title()


def transaction_list(request):
    MAX_LENGTH = 500
    if not request.POST or request.GET:
        form = FilterForm()
        transactions = Transaction.objects.all()
        result_count = len(transactions)
        if len(transactions) > MAX_LENGTH:
            transactions = transactions[:MAX_LENGTH]
        return render(request, 'transaction_list.html', {'transactions': transactions,
                                                         'result_count': result_count,
                                                         'form': form,
                                                         'message': "Display the first 500 results"})
    else:
        # Handle the form
        type = request.POST['type']
        name = camelcase(request.POST['name'])
        postal_code = request.POST['postal_code']
        address = camelcase(request.POST['address'])
        room_count = request.POST['room_count']

        # TODO: filter not case-sensitive
        
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
        if len(transactions) > MAX_LENGTH:
            transactions = transactions[:MAX_LENGTH]
        return render(request, 'transaction_list.html', {'transactions': transactions,
                                                         'form': form,
                                                         'result_count': result_count,
                                                         'message': "Display the first 500 results"})

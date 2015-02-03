from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from transaction.forms import FilterForm
from transaction.models import Transaction


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
        name = request.POST['name']
        postal_code = request.POST['postal_code']
        address = request.POST['address']
        if name != "":
            transactions = Transaction.objects.filter(name=name)
        else:
            transactions = Transaction.objects.all()

        if postal_code != "":
            transactions = transactions.filter(postal_code=postal_code)

        if address != "":
            transactions = transactions.filter(address=address)

        result_count = len(transactions)
        form = FilterForm(request.POST)
        if len(transactions) > MAX_LENGTH:
            transactions = transactions[:MAX_LENGTH]
        return render(request, 'transaction_list.html', {'transactions': transactions,
                                                         'form': form,
                                                         'result_count': result_count,
                                                         'message': "Display the first 500 results"})

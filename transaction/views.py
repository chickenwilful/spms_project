from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from transaction.forms import FilterForm
from transaction.models import Transaction


def transaction_list(request):
    if not request.POST or request.GET:
        form = FilterForm()
        transactions = Transaction.objects.all()[:500]
        return render(request, 'transaction_list.html', {'transaction_list': transactions,
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

        form = FilterForm(request.POST)
        return render(request, 'transaction_list.html', {'transaction_list': transactions,
                                                         'form': form,
                                                         'message': "Display the first 500 results"})

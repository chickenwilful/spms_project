from django.http import HttpResponse
from django.shortcuts import render
from transaction.charts import Chart
from transaction.forms import FilterForm, ChartFilterForm
from transaction.models import Transaction
import logging
from transaction.templatetags.transaction_template_tags import camelcase

logger = logging.getLogger(__name__)


def map(request, template='map.html'):
    # transactions = Transaction.objects.filter(latitude__isnull=True)
    # address_list = set([trans.address for trans in transactions])
    # return render(request, template, {'count': len(address_list),
    #                                   'address_list': address_list})
    transactions = Transaction.objects.filter(latitude__isnull=True)
    postalcodes = set([trans.postal_code for trans in transactions])
    return render(request, "map2.html", {'count': len(postalcodes),
                                         'postal_codes': postalcodes})


def coordinate(request):
    """
    View to get coordinate of all transactions' addresses
    """
    if request.GET:
        postal_code, lat, lng = request.GET['postalcode'], request.GET['lat'], request.GET['lng']
        transactions = Transaction.objects.filter(postal_code=postal_code)
        for trans in transactions:
            trans.latitude, trans.longitude = lat, lng
            trans.save()
        print len(transactions)
        return HttpResponse("Transactions updated!")
    else:
        return HttpResponse("Not GET request")


def transaction_list(request, template="transaction_list.html"):
    """
    View to display transaction list and related charts.
    """
    MAX_LENGTH = 50

    logger.debug("transaction list debug")

    if not request.POST or request.GET:
        transactions = Transaction.objects.all()

        chart = {
            'by_itself': Chart.chart_retrieve(transactions)
        }

        result_count = len(transactions)
        if len(transactions) > MAX_LENGTH:
            transactions = transactions[:MAX_LENGTH]

        return render(request, template, {'transactions': transactions,
                                          'result_count': result_count,
                                          'chart': chart,
                                          'filter_form': FilterForm(),
                                          'chart_form': ChartFilterForm()})
    else:
        # Handle the POST request
        type = request.POST['type']
        name = camelcase(request.POST['name'])
        postal_code = request.POST['postal_code']
        address = camelcase(request.POST['address'])
        room_count = request.POST['room_count']

        transactions = Transaction.get_transactions(type=type, room_count=room_count)

        # Refine request: name <--> address <--> postal_code
        temp = Transaction.get_transactions(transactions, name=name, postal_code=postal_code, address=address)
        if address == "":
            address = Transaction.get_address(name=name, postal_code=postal_code)
        if postal_code == "":
            postal_code = Transaction.get_postal_code(name=name, address=address)

        print("name = {0}, address = {1}, postal_code = {2}".format(name, address, postal_code))

        chart = {}
        # Handle chart series
        chart_series = request.POST.getlist('series')
        if Chart.ITSELF in chart_series:
            chart['by_itself'] = Chart.chart_retrieve(temp)
        if Chart.NEIGHBOR_POSTALCODE in chart_series:
            chart['by_postalcode'] = Chart.chart_by_neighbor_postal_code(transactions, postal_code)
        if Chart.NEIGHBOR_ADDRESS in chart_series:
            chart['by_address'] = Chart.chart_by_neighbor_address(transactions, address)

        # Handle displayed list
        display_list = request.POST['list']
        if display_list == Chart.ITSELF:
            transactions = temp
        elif display_list == Chart.NEIGHBOR_POSTALCODE:
            transactions = Chart.get_transactions_by_neighbor_postal_code(transactions, postal_code)
        else:
            transactions = Chart.get_transactions_by_neighbor_address(transactions, address, include=True)

        result_count = len(transactions)
        if len(transactions) > MAX_LENGTH:
            transactions = transactions[:MAX_LENGTH]

        return render(request, template, {'transactions': transactions,
                                          'result_count': result_count,
                                          'filter_form': FilterForm(request.POST),
                                          'chart_form': ChartFilterForm(request.POST),
                                          'chart': chart})

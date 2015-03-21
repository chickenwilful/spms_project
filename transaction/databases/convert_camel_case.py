import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "spms_site.settings")

import django
django.setup()

from transaction.models import Transaction
from transaction.views import camelcase


def convert_camel_case():
    transactions = Transaction.objects.all()
    for transaction in transactions:
        if transaction.name:
            transaction.name = camelcase(transaction.name)
        if transaction.address:
            transaction.address = camelcase(transaction.address)
        transaction.save()


if __name__ == '__main__':
    convert_camel_case()
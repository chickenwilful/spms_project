import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "spms_site.settings")

import django
django.setup()

from transaction.models import Transaction


def process():
    transactions = Transaction.objects.filter(postal_code__isnull=True)
    dict = {}
    for trans in transactions:
        if trans.address in dict.keys():
            trans.postal_code = dict[trans.address]
        else:
            trans.postal_code = Transaction.get_postal_code(name=trans.name, address=trans.address)
            dict[trans.address] = trans.postal_code
        if trans.postal_code:
            print "{0} - {1} - {2}".format(trans.name, trans.address, trans.postal_code)


if __name__ == "__main__":
    process()

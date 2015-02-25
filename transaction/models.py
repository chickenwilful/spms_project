from django.db import models

# Create your models here.
from transaction.templatetags.transaction_template_tags import camelcase


HOUSE_TYPE = (
    ('c', 'Condo'),
    ('h', 'HDB'),
)


class Transaction(models.Model):
    type = models.CharField(max_length=1, choices=HOUSE_TYPE, default='h')
    name = models.CharField(max_length=200, null=True, blank=True)
    room_count = models.IntegerField(null=True, blank=True)
    year = models.IntegerField(null=True, blank=True)
    month = models.IntegerField(null=True, blank=True)
    address = models.CharField(max_length=200, null=True, blank=True)
    postal_code = models.CharField(max_length=10, null=True, blank=True)
    area_sqm_min = models.FloatField(null=True, blank=True)
    area_sqm_max = models.FloatField(null=True, blank=True)
    monthly_rent = models.FloatField(null=True, blank=True)
    area_sqft_min = models.FloatField(null=True, blank=True)
    area_sqft_max = models.FloatField(null=True, blank=True)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)

    def __unicode__(self):
        if self.name:
            return 'name : ' + self.name
        else:
            return 'address: {0}'.format(self.address)

    def print_transaction(self):
        print "name: {0}; room_count: {1}; year: {2}; month: {3}; address: {4}; postal_code: {5}; " \
              "area_sqm_min: {6}; area_sqm_max: {7}; monthly_rent: {8}; type: {9}".format(
            self.name,
            self.room_count,
            self.year,
            self.month,
            self.address,
            self.postal_code,
            self.area_sqm_min,
            self.area_sqm_max,
            self.monthly_rent,
            self.type
        )


    @staticmethod
    def get_transactions(transactions=None, type="", postal_code="", name="", address="", room_count=""):

        if transactions is None:
            transactions = Transaction.objects.all()

        if type != '':
            transactions = Transaction.objects.filter(type=type)

        if name != "":
            transactions = transactions.filter(name=name)

        if address != "":
            transactions = transactions.filter(address=address)

        if room_count == "u":
            transactions = transactions.filter(room_count=None)
        elif room_count != "":
            transactions = transactions.filter(room_count=room_count)

        if postal_code != "":
            transactions = transactions.filter(postal_code=postal_code)

        return transactions

    @staticmethod
    def get_address(name="", postal_code=""):
        address = None
        transactions = Transaction.objects.all()
        if name and name != "":
            transactions = transactions.filter(name=name)
        if postal_code and postal_code != "":
            transactions = transactions.filter(postal_code=postal_code)
        if transactions:
            address = transactions[0].address
        return address

    @staticmethod
    def get_postal_code(name="", address=""):
        postal_code = None
        transactions = Transaction.objects.all()
        if name and name != "":
            transactions = transactions.filter(name=name)
        if address and address != "":
            transactions = transactions.filter(address=address)
        if transactions:
            postal_code = transactions[0].postal_code
        return postal_code

    @staticmethod
    def is_same_property(trans1, trans2):
        return trans1.address == trans2.address and (trans1.postal_code == trans2.postal_code or not trans1.postal_code or not trans2.postal_code)

    @staticmethod
    def is_neighbor(trans1, trans2):
        return (not Transaction.is_same_property(trans1, trans2)) \
            and (abs(trans1.latitude - trans2.latitude) <= 0.005) \
            and (abs(trans1.longitude - trans2.longitude) <= 0.005)


from django.db import models

# Create your models here.


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

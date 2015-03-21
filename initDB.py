import os
import datetime
from transaction.templatetags.transaction_template_tags import camelcase

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "spms_site.settings")
import django
django.setup()

import xlrd
from transaction.models import Transaction, NewTransaction


def read_hdb_rental(input_path='HDB_rental.xlsx'):
    book = xlrd.open_workbook(input_path)
    sheet = book.sheet_by_index(0)

    list = []

    for row in range(2, sheet.nrows):
        room_count = int(sheet.cell(row, 0).value)
        year = int(sheet.cell(row, 1).value)
        month = int(sheet.cell(row, 2).value)
        address = sheet.cell(row, 3).value
        postal_code = sheet.cell(row, 4).value
        if postal_code == "nil" or postal_code == "":
            postal_code = None
        try:
            area_sqm = float(sheet.cell(row, 5).value)
        except ValueError:
            area_sqm = None
        monthly_rent = float(sheet.cell(row, 6).value)

        transaction = Transaction(type='h',
                                  room_count=room_count,
                                  year=year,
                                  month=month,
                                  address=address,
                                  postal_code=postal_code,
                                  area_sqm_min=area_sqm,
                                  area_sqm_max=area_sqm,
                                  monthly_rent=monthly_rent)
        list.append(transaction)
    print(len(list))
    return list


def read_hdb_rental_new(input_path='HDB_rental_new.xlsx'):

    book = xlrd.open_workbook(input_path)
    sheet = book.sheet_by_index(0)

    list = []

    for row in range(1, sheet.nrows):
        date = datetime.datetime(*xlrd.xldate_as_tuple(sheet.cell(row, 1).value, book.datemode))
        month = date.month
        year = date.year
        try:
            room_count = int(sheet.cell(row, 2).value[0])
        except ValueError:
            room_count = None
        area_sqm_min = sheet.cell(row, 3).value
        area_sqm_max = area_sqm_min
        monthly_rent = sheet.cell(row, 4).value
        address = camelcase(sheet.cell(row, 6).value)
        # temp = Transaction.get_transaction_by_address(address)
        # if temp:
        #     postal_code = temp.postal_code
        #     longitude = temp.longitude
        #     latitude = temp.latitude
        # else:
        postal_code = longitude = latitude = None
        try:
            transaction = NewTransaction(type='h',
                                      name=None,
                                      year=year,
                                      month=month,
                                      postal_code=postal_code,
                                      address=address,
                                      area_sqm_min=area_sqm_min,
                                      area_sqm_max=area_sqm_max,
                                      room_count=room_count,
                                      monthly_rent=monthly_rent,
                                      longitude=longitude,
                                      latitude=latitude)
            list.append(transaction)
            transaction.save()
        except ValueError:
            print year, month, postal_code, address, area_sqm_min, monthly_rent, longitude, latitude
    print len(list)
    return list


def read_hdb_sale(input_path='HDB_sales.xlsx'):

    book = xlrd.open_workbook(input_path)
    sheet = book.sheet_by_index(0)

    list = []

    for row in range(1, sheet.nrows):
        date = datetime.datetime(*xlrd.xldate_as_tuple(sheet.cell(row, 1).value, book.datemode))
        month = date.month
        year = date.year
        try:
            room_count = int(sheet.cell(row, 2).value[0])
        except ValueError:
            room_count = None
        area_sqm_min = sheet.cell(row, 5).value
        area_sqm_max = area_sqm_min
        monthly_rent = sheet.cell(row, 6).value
        address = camelcase(sheet.cell(row, 8).value)
        # temp = Transaction.get_transaction_by_address(address)
        # if temp:
        #     postal_code = temp.postal_code
        #     longitude = temp.longitude
        #     latitude = temp.latitude
        # else:
        postal_code = longitude = latitude = None
        try:
            transaction = NewTransaction(type='h',
                                      name=None,
                                      year=year,
                                      month=month,
                                      postal_code=postal_code,
                                      address=address,
                                      area_sqm_min=area_sqm_min,
                                      area_sqm_max=area_sqm_max,
                                      room_count=room_count,
                                      monthly_rent=monthly_rent,
                                      longitude=longitude,
                                      latitude=latitude)
            list.append(transaction)
            transaction.save()
        except ValueError:
            print year, month, postal_code, address, area_sqm_min, monthly_rent, longitude, latitude

    print len(list)
    return list


def read_condo_rental(input_path='Residential_rental.xlsx'):

    book = xlrd.open_workbook(input_path)
    sheet = book.sheet_by_index(0)

    list = []

    for row in range(2, sheet.nrows):
        name = sheet.cell(row, 0).value
        year = int(sheet.cell(row, 1).value)
        month = int(sheet.cell(row, 2).value)
        postal_code = sheet.cell(row, 3).value
        if postal_code == "nil" or postal_code == "":
            postal_code = None
        address = sheet.cell(row, 4).value
        area_sqm = sheet.cell(row, 5).value.replace(',','')
        if area_sqm[0] == '>':
            area_sqm_min = area_sqm[1:]
            area_sqm_max = None
        else:
            area_sqm = area_sqm.split(' to ')
            area_sqm_min = float(area_sqm[0])
            area_sqm_max = float(area_sqm[1])
        try:
            room_count = int(sheet.cell(row, 6).value)
        except ValueError:
            room_count = None
        monthly_rent = float(sheet.cell(row, 7).value)

        transaction = Transaction(type='c',
                                  name=name,
                                  year=year,
                                  month=month,
                                  postal_code=postal_code,
                                  address=address,
                                  area_sqm_min=area_sqm_min,
                                  area_sqm_max=area_sqm_max,
                                  room_count=room_count,
                                  monthly_rent=monthly_rent)
        list.append(transaction)

    print len(list)
    return list


def update_postal_code_and_coordinate():

    newtransactions = NewTransaction.objects.filter(type='h').filter(address__isnull=False).filter(latitude__isnull=True)

    addresses = set([newtrans.address for newtrans in newtransactions])

    print len(addresses)
    for address in addresses:
        if address:
            trans = Transaction.get_transaction_by_address(address)
            NewTransaction.objects.filter(type='h').filter(address=address)\
                .update(postal_code=trans.postal_code, longitude=trans.longitude, latitude=trans.latitude)


if __name__ == '__main__':
    # read_hdb_rental_new()
    # read_hdb_sale()
    # Read old condos
    # update_postal_code_and_coordinate()

    newtransactions = NewTransaction.objects.all()
    for newtrans in newtransactions:
        trans = Transaction(type=newtrans.type,
                            name=newtrans.name,
                            year=newtrans.year,
                            month=newtrans.month,
                            room_count=newtrans.room_count,
                            address=newtrans.address,
                            postal_code=newtrans.postal_code,
                            monthly_rent=newtrans.monthly_rent,
                            area_sqm_min=newtrans.area_sqm_min,
                            area_sqm_max=newtrans.area_sqm_max,
                            area_sqft_min=newtrans.area_sqft_min,
                            area_sqft_max=newtrans.area_sqft_max,
                            longitude=newtrans.longitude,
                            latitude=newtrans.latitude)
        trans.save()
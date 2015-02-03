import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "spms_site.settings")

import xlrd
from transaction.models import Transaction


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


if __name__ == '__main__':
    list1 = read_hdb_rental()
    list2 = read_condo_rental()
    list = list1 + list2

    # sort all transactions by year in descending order
    list = sorted(list, key=lambda x: -x.year)

    for transaction in list:
        transaction.save()
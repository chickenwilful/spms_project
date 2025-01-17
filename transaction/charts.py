from transaction.models import Transaction


class Chart(object):
    ITSELF = 'i'
    NEIGHBOR_POSTALCODE = 'p'
    NEIGHBOR_ADDRESS = 'a'

    CHART_SERIES_CHOICES = (
        (ITSELF, 'Itself'),
        (NEIGHBOR_POSTALCODE, 'Neighbor Postal Code'),
        (NEIGHBOR_ADDRESS, 'Neighbor Address'),
    )

    LIST_CHOICES = (
        (ITSELF, 'Itself'),
        (NEIGHBOR_POSTALCODE, 'Neighbor Postal Code'),
        (NEIGHBOR_ADDRESS, 'Neighbor Address'),
    )

    @staticmethod
    def chart_retrieve(transactions):
        cnt = [[0 for month in range(0, 13)] for year in range(0, 2016)]
        amt = [[0 for month in range(0, 13)] for year in range(0, 2016)]
        for transaction in transactions:
            if transaction.year and transaction.month and transaction.monthly_rent:
                year, month = transaction.year, transaction.month
                cnt[year][month] += 1
                amt[year][month] += transaction.monthly_rent

        chart = {'count': [], 'price': []}
        for year in range(2012, 2016):
            for month in range(1, 13):
                if year < 2015 or month == 1:
                    if cnt[year][month] > 0:
                        chart['price'].append(round(amt[year][month] / cnt[year][month]))
                    else:
                        chart['price'].append(None)
                    chart['count'].append(cnt[year][month])
        return chart

    @staticmethod
    def chart_avg_by_addresses(transactions, address):
        transactions = Chart.get_transactions_by_address(transactions=transactions, address=address)
        return Chart.chart_retrieve(transactions)

    @staticmethod
    def chart_avg_by_neighbor_addresses(transactions, address):
        transactions = Chart.get_transactions_by_neighbor_address(transactions, address)
        return Chart.chart_retrieve(transactions)

    @staticmethod
    def chart_by_neighbor_address(transactions, address):

        avg_by_address = Chart.chart_avg_by_addresses(transactions, address)
        avg_by_neighbor_address = Chart.chart_avg_by_neighbor_addresses(transactions, address)

        chart = {'price': [], 'count': []}
        for i in range(len(avg_by_address['price'])):
            chart['price'].append(avg_price(avg_by_address['price'][i], avg_by_neighbor_address['price'][i]))
            chart['count'].append(avg_by_address['count'][i] + avg_by_neighbor_address['count'][i])
        return chart

    @staticmethod
    def chart_by_neighbor_postal_code(transactions=None, postal_code=None):
        transactions = Chart.get_transactions_by_neighbor_postal_code(transactions, postal_code)
        return Chart.chart_retrieve(transactions)

    @staticmethod
    def get_transactions_by_address(transactions=Transaction.objects.all(), address=""):
        transactions = [trans for trans in transactions if trans.address == address]
        return transactions

    @staticmethod
    def get_transactions_by_neighbor_postal_code(transactions=Transaction.objects.all(), postal_code=None):
        if not postal_code or postal_code == "":
            return []
        postal_code = postal_code[:len(postal_code) - 1]
        results = [trans for trans in transactions if trans.postal_code and trans.postal_code.startswith(postal_code)]
        return results

    @staticmethod
    def get_transactions_by_neighbor_address(transactions=Transaction.objects.all(), address=None, include=False):
        if not address or address == "":
            return []
        transaction_list = transactions.filter(address=address)
        if len(transaction_list) == 0:
            return []
        transaction = transaction_list[0]
        if not include:
            results = [trans for trans in transactions if Transaction.is_neighbor(trans, transaction)]
        else:
            results = [trans for trans in transactions if Transaction.is_neighbor(trans, transaction)
                       or Transaction.is_same_property(trans, transaction)]
        return results


def avg_price(price_by_addr, price_by_neighbor_addr):
        if not price_by_addr:
            return price_by_neighbor_addr
        else:
            return 0.8 * price_by_addr + 0.2 * price_by_neighbor_addr

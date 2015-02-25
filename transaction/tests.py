from django.test import TestCase

# Create your tests here.
from transaction.charts import Chart, avg_price
from transaction.models import Transaction


class TransactionTest(TestCase):

    fixtures = ['transactions.json']

    def test_get_postal_code(self):
        self.assertEquals(Transaction.get_postal_code(address="144 Jalan Bukit Merah"), None)
        self.assertEquals(Transaction.get_postal_code(address="146 Simei Street 2"), None)
        self.assertEquals(Transaction.get_postal_code(address="10 Telok Blangah Crescent"), "090010")
        self.assertEquals(Transaction.get_postal_code(address="1 Haig Road"), "430001")
        self.assertEquals(Transaction.get_postal_code(name="Aa Centre", address="River Valley Road"), "238366")
        self.assertEquals(Transaction.get_postal_code(name="283 Studio", address="River Valley Road"), "238324")

    def test_get_address(self):
        self.assertEquals(Transaction.get_address(name="Aa Centre", postal_code="238366"), "River Valley Road")
        self.assertEquals(Transaction.get_address(name="283 Studio", postal_code="238324"), "River Valley Road")
        self.assertEquals(Transaction.get_address(postal_code="400010"), "10 Eunos Crescent")

    def test_is_same_property(self):
        trans1 = Transaction(id=1, address="1", postal_code="1")
        trans2 = Transaction(id=2, address="2", postal_code="1")
        trans3 = Transaction(id=3, address="2", postal_code="3")
        trans4 = Transaction(id=4, address="2", postal_code="1")
        self.assertEquals(Transaction.is_same_property(trans1, trans2), False)
        self.assertEquals(Transaction.is_same_property(trans2, trans3), False)
        self.assertEquals(Transaction.is_same_property(trans2, trans4), True)

    def test_is_neighbor(self):
        trans1 = Transaction(latitude=0.005, longitude=0.000, address="1")
        trans2 = Transaction(latitude=0.000, longitude=-0.005, address="2")
        trans3 = Transaction(latitude=-0.005, longitude=-0.001, address="3")
        self.assertEquals(Transaction.is_neighbor(trans1, trans2), True)
        self.assertEquals(Transaction.is_neighbor(trans1, trans3), False)
        self.assertEquals(Transaction.is_neighbor(trans2, trans3), True)
        self.assertEquals(Transaction.is_neighbor(trans1, trans1), False)


    # class ChartTest(TestCase):

    def test(self):
        pass

    # Test display
    def test_get_transactions_by_neighbor_postal_code(self):
        transactions = Chart.get_transactions_by_neighbor_postal_code(postal_code="090010")
        self.assertEquals(len(transactions), 21)
        for trans in transactions:
            self.assertEquals(trans.postal_code[:len(trans.postal_code)-1], "09001")

    def test_get_transactions_by_neighbor_address(self):
        address = "10 Telok Blangah Crescent"

        # Test include=True
        transactions = Chart.get_transactions_by_neighbor_address(address=address, include=True)
        self.assertEquals(len(transactions), 628)

        # Test include=False
        transaction = Transaction.objects.filter(address=address)[0]
        transactions = Chart.get_transactions_by_neighbor_address(address=address, include=False)
        for trans in transactions:
            self.assertEquals(Transaction.is_neighbor(trans, transaction), True)

    def test_get_transactions_by_address(self):
        address = "10 Telok Blangah Crescent"
        self.assertEquals(Chart.get_transactions_by_address([], address), [])
        self.assertEquals(len(Chart.get_transactions_by_address(address=address)), 4)
        self.assertEquals(len(Chart.get_transactions_by_address(
            Chart.get_transactions_by_address(address=address)[:3], address=address)), 3)

    # Test avg price
    def test_avg_price(self):
        self.assertEquals(avg_price(price_by_addr=None, price_by_neighbor_addr=3.4), 3.4)
        self.assertEquals(avg_price(price_by_addr=2, price_by_neighbor_addr=3), 2.2)

    # Test avg price chart
    def test_chart_retrieve(self):
        chart = Chart.chart_retrieve(Transaction.objects.all())
        self.assertEquals(len(chart['count']), 37)
        self.assertEquals(chart['count'][0], 2226)
        self.assertEquals(chart['count'][33], 7086)
        self.assertEquals(chart['price'][0], 4131)
        self.assertEquals(chart['price'][36], 2274)





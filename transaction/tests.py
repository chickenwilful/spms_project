from django.test import TestCase

# Create your tests here.
from transaction.models import Transaction


class TransactionModelTest(TestCase):

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


class ChartTest(TestCase):

    def test(self):
        pass


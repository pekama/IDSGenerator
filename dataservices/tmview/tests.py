from unittest import TestCase
from tmviewdata import TMViewData, TMViewClient

class TMViewDataTests(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.tmview = TMViewData()
        cls.trademarks = cls.tmview.get_trademarks('nike')

    def test_gets_all_trademarks(self):
        self.assertEqual(len(self.trademarks), 1071)

    def test_first_trademark_fetches_correctly(self):
        self.assertEqual(self.trademarks[0]['trademark'], u'"NIKE RIDE"')

    def test_last_trademark_fetches_correctly(self):
        self.assertEqual(self.trademarks[-1]['trademark'], 'x-nike sekil')

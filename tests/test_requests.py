import unittest, sys

sys.path.append('../workspace') # imports python file from parent directory
from backend.logic import get_RSI, get_SMA, get_current_price, get_insider_transactions

class RequestsTests(unittest.TestCase):

    # executed prior to each test
    def setUp(self):
        pass

    ###############
    #### tests ####
    ###############

    def test_get_RSI(self):
        self.assertTrue(get_RSI("AAPL") > 0)

    def test_get_SMA(self):
        self.assertTrue(get_SMA("AAPL") > 0)

    def test_get_current_price(self):
        self.assertTrue(get_current_price("AAPL") > 0)

    def test_get_insider_transactions(self):
        self.assertIn(get_insider_transactions("AAPL"), ["BUY", "SELL", "HOLD"])

if __name__ == "__main__":
    unittest.main()
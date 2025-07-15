import unittest, sys

sys.path.append('../workspace') # imports python file from parent directory
from app import app # imports flask app object

class WebpageTests(unittest.TestCase):

    # executed prior to each test
    def setUp(self):
        self.app = app.test_client()

    ###############
    #### tests ####
    ###############

    def test_home_page(self):
        response = self.app.get('/', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        response = self.app.get('/home', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_about_page(self):
        response = self.app.get("/about", follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_trade_page(self):
        response = self.app.get("/trade", follow_redirects=True)
        self.assertEqual(response.status_code, 200)

if __name__ == "__main__":
    unittest.main()
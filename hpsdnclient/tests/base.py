import unittest
import hpsdnclient as hp

SDNCTL = '10.44.254.129'
USER = 'sdn'
PASS = 'skyline'

class ApiBaseTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        auth = hp.XAuthToken(controller=SDNCTL, user=USER, password=PASS)
        cls._api = hp.Api(controller=SDNCTL, auth=auth)

    @classmethod
    def tearDownClass(cls):
        cls._api = None


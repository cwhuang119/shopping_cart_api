from . import BaseUnitTestCase
from db.client import get_db_client

def TestCaseDBClient(BaseUnitTestCase):

    def test_db_client(self):
        db_client = get_db_client()
        db_client2 = get_db_client()
        self.assertEqual(id(db_client),id(db_client2))
        self.assertEqual(db_client.connection_str,'sqlite://')
    
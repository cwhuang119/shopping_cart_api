from . import BaseTestCase

class TestAccountAPI(BaseTestCase):

    def test_login(self):
        response = self.client.post('/account/login')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {'message':'Login success.'})
        
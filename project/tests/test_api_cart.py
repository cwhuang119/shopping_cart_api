from . import BaseTestCase

class TestCartAPI(BaseTestCase):

    def test_add_cart_without_login(self):
        response = self.client.post('/cart/add',data = {'product_name':'apple'})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.json, {"message": "Please login first.","redirect_url": "/account/login"})
    
    def test_checkout_without_login(self):
        response = self.client.post('/cart/checkout')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.json, {"message": "Please login first.","redirect_url": "/account/login"})
    
    def test_checkout_with_empty_cart(self):
        response = self.client.post('/account/login')
        self.assertEqual(response.status_code, 200)
        response = self.client.post('/cart/checkout')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {"message": "Cart is empty."})


    def test_add_cart_with_login_and_checkout(self):
        response = self.client.post('/account/login')
        self.assertEqual(response.status_code, 200)
        response = self.client.post('/cart/add',data = {'product_name':'apple'})
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json,{
            "message": "Product apple add to cart."
        })
        response = self.client.post('/cart/add',data = {'product_name':'banana'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json,{
            "message": "Product banana add to cart."
        })
        response = self.client.post('/cart/add',data = {'product_name':'banana'})
        self.assertEqual(response.status_code, 200)

        response = self.client.post('/cart/checkout')
        self.assertEqual(response.status_code, 200)
        order_response = response.json
        order_info = order_response['payload']['order_info']
        self.assertEqual(order_info['order_amount'],20)
        self.assertEqual(order_info['order_id'],0)
        self.assertEqual(order_info['order_items'][0]['product_name'],'apple')
        self.assertEqual(order_info['username'],'test_account')

        response = self.client.post('/cart/add',data = {'product_name':'banana'})
        self.assertEqual(response.status_code, 200)
        response = self.client.post('/cart/add',data = {'product_name':'banana'})
        self.assertEqual(response.status_code, 200)

        response = self.client.post('/cart/checkout')
        self.assertEqual(response.status_code, 200)
        order_response = response.json
        self.assertEqual(order_response['message'],"Total amount :5 \nTotal quantity: 1.")
        order_info = order_response['payload']['order_info']
        self.assertEqual(order_info['order_amount'],5)
        self.assertEqual(order_info['order_id'],1)
        self.assertEqual(order_info['order_items'][0]['product_name'],'banana')
        self.assertEqual(order_info['username'],'test_account')

    def test_add_cart_with_stock_out_and_checkout(self):
        response = self.client.post('/account/login')
        self.assertEqual(response.status_code, 200)
        response = self.client.post('/cart/add',data = {'product_name':'apple'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json,{
            "message": "Product apple add to cart."
        })
        response = self.client.post('/cart/add',data = {'product_name':'apple'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json,{
            "message": "Product apple out of stock."
        })

        response = self.client.post('/cart/checkout')
        self.assertEqual(response.status_code, 200)
        order_response = response.json
        order_info = order_response['payload']['order_info']
        self.assertEqual(order_info['order_amount'],10)
        #123
        self.assertEqual(order_info['order_id'],2)
        self.assertEqual(order_info['order_items'][0]['product_name'],'apple')
        self.assertEqual(order_info['username'],'test_account')

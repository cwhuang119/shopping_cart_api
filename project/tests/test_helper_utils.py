from . import BaseTestCase, BaseUnitTestCase
from helper.utils import ResponseFlow, CartOp
from flask import make_response, jsonify

class TestCaseResponseFlow(BaseTestCase):
    
    def test_response_flow(self):

        # test init value
        response_flow = ResponseFlow()
        self.assertEqual(response_flow.code,200)
        self.assertEqual(response_flow.finish,True)
        self.assertEqual(response_flow.content,{})

        # test init value
        response_flow = ResponseFlow(
            False,500,{'test':'123'}
        )
        self.assertEqual(response_flow.code,500)
        self.assertEqual(response_flow.finish,False)
        self.assertEqual(response_flow.content,{'test':'123'})

class TestCaseCartOp(BaseUnitTestCase):

    def test_get_user_cart(self):
        # username in cart
        username = 'test_account'
        cart = {
            username:{'test':'123'}
        }
        user_cart = CartOp.get_user_cart(username,cart)
        self.assertEqual(user_cart,{'test':'123'})

        # username not in cart
        username = 'test_account123'
        cart = {
            'test_acount':{'test':'123'}
        }
        user_cart = CartOp.get_user_cart(username,cart)
        self.assertEqual(user_cart,{})

    def test_get_quantity(self):

        # get quantity
        username = 'test_account'
        cart = {
            username:{'apple':2}
        }
        quantity = CartOp.get_quantity(username,cart,product_name='apple')
        self.assertEqual(quantity,2)
        # no such item in cart
        quantity = CartOp.get_quantity(username,cart,product_name='banana')
        self.assertEqual(quantity,0)

    def test_add_item(self):
        
        username = 'test_account'
        cart = {
            username:{'apple':2}
        }

        user_cart = CartOp.add_item(username,cart,product_name='apple',quantity=2)
        self.assertEqual(
            user_cart,
            {
                username:{'apple':4}
            }   
        )

        user_cart = CartOp.add_item(username,cart,product_name='banana',quantity=2)
        self.assertEqual(
            user_cart,
            {
                username:{'apple':4,'banana':2}
            }   
        )
    
    def test_checkout(self):
        username = 'test_account'
        cart = {
            username:{'apple':2,'banana':2},
            'test':{'apple':1}
        }
        price_list = {
            'apple':2,
            'banana':3
        }
        total_amount,total_quantities,cart_list = CartOp.checkout(username,cart,price_list)
        self.assertEqual(total_amount,10)
        self.assertEqual(total_quantities,4)
        self.assertEqual(cart_list,{'apple':{'price':2,'quantity':2},'banana':{'price':3,'quantity':2}})

    def test_empty_cart(self):
        username = 'test_account'
        cart = {
            username:{'apple':2},
            'test':{'apple':1}
        }
        # username in cart
        cart_result = CartOp.empty_cart(username,cart)
        self.assertEqual(cart_result,{'test':{'apple':1}})
        # username not in cart
        cart_result = CartOp.empty_cart('123',cart_result)
        self.assertEqual(cart_result,{'test':{'apple':1}})
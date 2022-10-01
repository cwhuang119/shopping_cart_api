
from . import BaseUnitTestCase
from helper.logics import (
    verify_login,
    verify_username,
    verify_product_name,
    checkout,
    add_product_to_cart,
    account_login
)

class TestCaseLogics(BaseUnitTestCase):

    def test_verify_login(self):

        # username is None
        username,cart = None,{}
        response_flow = verify_login(username,cart)
        self.assertEqual(response_flow.code,302)
        self.assertEqual(response_flow.finish,True)
        self.assertEqual(response_flow.content,{
                'message':'Please login first.',
                'redirect_url':'/account/login'
            })

        # cart is None
        username,cart = 'test_account',None
        response_flow = verify_login(username,cart)
        self.assertEqual(response_flow.code,302)
        self.assertEqual(response_flow.finish,True)
        self.assertEqual(response_flow.content,{
                'message':'Please login first.',
                'redirect_url':'/account/login'
            })
        
        # username found
        username,cart = 'test_account',{}
        response_flow = verify_login(username,cart)
        self.assertEqual(response_flow.code,200)
        self.assertEqual(response_flow.finish,False)

        # username not found
        username,cart = 'test_account123',{}
        response_flow = verify_login(username,cart)
        self.assertEqual(response_flow.code,400)
        self.assertEqual(response_flow.finish,True)
        self.assertEqual(response_flow.content,{'message': 'Username test_account123 not found.'})

    def test_verify_username(self):

        # username found
        username,cart = 'test_account',{}
        response_flow = verify_username(username)
        self.assertEqual(response_flow.code,200)
        self.assertEqual(response_flow.finish,False)

        # username not found
        username,cart = 'test_account123',{}
        response_flow = verify_username(username)
        self.assertEqual(response_flow.code,400)
        self.assertEqual(response_flow.finish,True)
        self.assertEqual(response_flow.content,{'message': 'Username test_account123 not found.'})

    def test_verify_product_name(self):

        # product name is None
        username,cart,product_name = 'test_account',{},None
        response_flow = verify_product_name(username,cart,product_name)
        self.assertEqual(response_flow.code,400)
        self.assertEqual(response_flow.finish,True)
        self.assertEqual(response_flow.content,{'message':'Missing product name.'})

        # product out of stock
        username,cart,product_name = 'test_account',{},'grape'
        response_flow = verify_product_name(username,cart,product_name)
        self.assertEqual(response_flow.code,200)
        self.assertEqual(response_flow.finish,True)
        self.assertEqual(response_flow.content,{'message':'Product grape out of stock.'})

    def test_checkout(self):
        # cart is empty
        username = 'test_account'
        cart = {
            username:{}
        }
        
        response_flow = checkout(username,cart)
        self.assertEqual(response_flow.code,200)
        self.assertEqual(response_flow.finish,True)
        self.assertEqual(response_flow.content,{'message':'Cart is empty.'})

        # test cart addup function
        cart = {
            username:{
                'apple':1,
                'orange':1
            }
        }
        response_flow = checkout(username,cart)
        self.assertEqual(response_flow.code,200)
        self.assertEqual(response_flow.finish,True)
        self.assertEqual(response_flow.content['message'],'Total amount :22 \nTotal quantity: 2.')

        cart = {
            username:{
                'apple':1,
                'orange':1,
                'banana':2
            }
        }
        response_flow = checkout(username,cart)
        self.assertEqual(response_flow.code,200)
        self.assertEqual(response_flow.finish,True)
        self.assertEqual(response_flow.content['message'],'Total amount :32 \nTotal quantity: 4.')



    def test_add_product_to_cart(self):
        username = 'test_account'
        cart = {
            username:{
                'apple':1,
                'orange':1,
                'banana':2
            }
        }
        product_name='banana'
        response_flow = add_product_to_cart(username,cart,product_name)
        self.assertEqual(response_flow.code,200)
        self.assertEqual(response_flow.finish,True)
        self.assertEqual(response_flow.content['message'],'Product banana add to cart.')


    def test_account_login(self):

        response_flow = account_login()
        self.assertEqual(response_flow.code,200)
        self.assertEqual(response_flow.finish,True)
        self.assertEqual(response_flow.content['message'],'Login success.')
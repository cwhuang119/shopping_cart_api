from statistics import quantiles
from . import BaseUnitTestCase
from db.ops import get_db_client, User, Product, Order, OrderItem
from db.ops import (
    get_rows,
    get_product,
    get_user,
    subtract_inventory,
    get_price_list,
    create_order,
)

class TestCaseDBOPS(BaseUnitTestCase):

    def test_get_row(self):

        db_client = get_db_client()
        user = get_rows(db_client,User,True,username='123')
        self.assertEqual(user,None)
        user = get_rows(db_client,User,True,username='test_account')
        self.assertEqual(user.username,'test_account')

        products = get_rows(db_client,Product,False)
        self.assertEqual(len(products),4)

    def test_get_product(self):
        db_client = get_db_client()
        product = get_product(product_name='apple')
        self.assertEqual(product.name,'apple')
        product = get_product(product_name='apple123')
        self.assertEqual(product,None)

    def test_get_user(self):
        db_client = get_db_client()
        user = get_rows(db_client,User,True,username='test_account')
        self.assertEqual(user.username,'test_account')
        user = get_rows(db_client,User,True,username='test_account1')
        self.assertEqual(user,None)
    
    def test_subtract_inventory(self):
        # failed to subtract since inventory not enough
        product_name = 'apple'
        quantity = 2
        success = subtract_inventory(product_name,quantity)
        self.assertEqual(success,False)

        # success subtract
        product_name = 'apple'
        quantity = 1
        success = subtract_inventory(product_name,quantity)
        self.assertEqual(success,True)

    def test_get_price_list(self):

        price_list = {
            'apple':10,
            'banana':5,
            'orange':12,
            'grape':5
        }

        self.assertEqual(get_price_list(),price_list)

    def test_create_order(self):
        username = 'test_account'
        cart_list = {
            'apple':{'price':1,'quantity':2},
            'banana':{'price':3,'quantity':2},
            'orange':{'price':2,'quantity':1},
        }

        order_info = create_order(username,cart_list)
        self.assertEqual(order_info['username'],username)
        self.assertEqual(order_info['order_id'],4)
        self.assertEqual(order_info['order_amount'],8)
        apple_order_item = [x for x in order_info['order_items'] if x ['product_name']=='apple'][0]
        self.assertEqual(apple_order_item['success'],False)
        self.assertEqual(apple_order_item['item_amount'],0)

        banana_order_item = [x for x in order_info['order_items'] if x ['product_name']=='banana'][0]
        self.assertEqual(banana_order_item['success'],True)
        self.assertEqual(banana_order_item['item_amount'],6)


        orange_order_item = [x for x in order_info['order_items'] if x ['product_name']=='orange'][0]
        self.assertEqual(orange_order_item['success'],True)
        self.assertEqual(orange_order_item['item_amount'],2)


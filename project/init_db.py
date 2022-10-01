from db.client import get_db_client
from db.ops import get_rows
from db.model import User, Product, Base
import os
def init_test_data():
    db_client = get_db_client()
    db_path = db_client.connection_str.replace('sqlite:///','')
    if os.path.exists(db_path):
        os.remove(db_path)
    db_client.create_tables(Base)
    
    default_user_name = 'test_account'
    default_products = [
        {
            'name':'apple',
            'inventory':1,
            'price':10
        },
        {
            'name':'orange',
            'inventory':2,
            'price':12
        },
        {
            'name':'banana',
            'inventory':3,
            'price':5
        },
        {
            'name':'grape',
            'inventory':0,
            'price':5
        }
    ]
    db_client = get_db_client()
    user = get_rows(db_client,User,True,username=default_user_name)
    if user is None:
        # create user
        user = User(
            username=default_user_name
        )
        db_client.update(user)
        user = get_rows(db_client,User,True,username=default_user_name)
    for default_product in default_products:

        product = get_rows(db_client,Product,True,name=default_product['name'])
        if product is None:
            # create product
            product = Product(
                name=default_product['name'],
                price=default_product['price'],
                inventory=default_product['inventory']
            )
        else:
            # reset inventory
            product.inventory = default_product['inventory']
        db_client.update(product)
        
if __name__ == '__main__':

    init_test_data()
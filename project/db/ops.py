from db.model import User, Product, Order, OrderItem
from db.client import get_db_client
import datetime

def get_rows(db_client,table,single_row=True,**kwargs):
    # get db rows and return result
    rows = db_client.query(table).filter_by(**kwargs).all()
    if len(rows)>0:
        if single_row:
            return rows[0]
        else:
            return rows
    
def get_product(product_name):
    # get single product
    db_client = get_db_client()
    return get_rows(db_client,Product,True,name=product_name)

def get_user(username):
    # get single user
    db_client = get_db_client()
    return get_rows(db_client,User,True,username=username)

def subtract_inventory(product_name,quantity=1):
    # subtract inventory from DB
    db_client = get_db_client()
    product = get_rows(db_client,Product,True,**{'name':product_name})
    current_inventory = product.inventory
    if current_inventory>= quantity:
        current_inventory -= quantity
        product.inventory = current_inventory
        db_client = get_db_client()
        db_client.update(product)
        return True
    else:
        return False

def get_price_list():
    # get all product price
    db_client = get_db_client()
    price_list = {}
    products = get_rows(db_client,Product,False)
    for product in products:
        price_list[product.name]=product.price
    return price_list

def create_order(username,cart_list):
    #create order item and order 
    db_client = get_db_client()
    # set order id as last id + 1
    orders = get_rows(db_client,Order,False)
    if orders is None:
        order_id = 0
    else:
        order_id = len(orders)
    # get user id
    user_id = get_rows(db_client,User,True,username=username).id
    order_items = []
    order_amount=0

    # loop through product and create order item
    for product_name,data in cart_list.items():
        product_id = get_product(product_name).id
        quantity = data['quantity']
        price = data['price']
        success = subtract_inventory(product_name,quantity)
        if success:
            item_amount = round(quantity*price,2)
            order_amount+=item_amount
            
            # create order item
            order_item = OrderItem(
                order_id=order_id,
                product_id=product_id,
                quantity=quantity,
                price=price
            )

            # append order item info
            order_items.append({
                'product_id':product_id,
                'product_name':product_name,
                'quantity':quantity,
                'price':price,
                'item_amount':item_amount,
                'success':True
            })
            db_client.update(order_item)
        else:
            # append order item info
            order_items.append({
                'product_id':product_id,
                'product_name':product_name,
                'quantity':0,
                'price':price,
                'item_amount':0,
                'success':False
            })

    # create order
    order = Order(id=order_id,user_id=user_id)
    db_client.update(order)

    # formate order info for response
    order_info = {
        'username':username,
        'order_id':order_id,
        'order_items':order_items,
        'order_amount':order_amount,
        'time_created':datetime.datetime.strftime(order.time_created,'%Y-%m-%d %H:%M:%S')
    }

    return order_info


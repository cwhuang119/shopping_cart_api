from helper.utils import CartOp, ResponseFlow
from db.ops import get_product,get_user, subtract_inventory, get_price_list, create_order

def verify_login(username,cart):
    # check if user alreay login and username will be sorce in session
    if username is None or cart is None:
        return ResponseFlow(
            finish=True,
            code=302,
            content={
                'message':'Please login first.',
                'redirect_url':'/account/login'
            }
        )
    else:
        return verify_username(username)


def verify_username(username):
    #verify username is valid
    user = get_user(username)
    if user is None:
        return ResponseFlow(
            finish=True,
            code=400,
            content={
                'message':f'Username {username} not found.'
            }
        )
    return ResponseFlow(finish=False)

def verify_product_name(username,cart,product_name):
    # check if product name is provided and valid
    if product_name is None:
        return ResponseFlow(
            finish=True,
            code=400,
            content={
                'message':f'Missing product name.'
            }
        )
    product = get_product(product_name)
    quantity = CartOp.get_quantity(username,cart,product_name)
    if product.in_stock(quantity):
        return ResponseFlow(finish=False)
    else:
        return ResponseFlow(
            finish=True,
            code=200,
            content={
                'message':f'Product {product_name} out of stock.'
            }
        )


def checkout(username,cart):
    # checkout cart's items and sum up amount and quantities
    price_list = get_price_list()
    # get cart item formatted
    total_amount,total_quantities,cart_list = CartOp.checkout(username,cart,price_list)
    # create order
    order_info = create_order(username,cart_list)

    # empty cart
    CartOp.empty_cart(username,cart)
    if total_quantities==0:
        return ResponseFlow(
            finish=True,
            code=200,
            content={
                'message':'Cart is empty.'
            }
        )
    else:
        return ResponseFlow(
            finish=True,
            code=200,
            content={
                'message':f'Total amount :{total_amount} \nTotal quantity: {total_quantities}.',
                'payload':{
                    'order_info':order_info
                }
            }
        )

def add_product_to_cart(username,cart,product_name):
    CartOp.add_item(username,cart,product_name,1)
    return ResponseFlow(
            finish=True,
            code=200,
            content={
                'message':f'Product {product_name} add to cart.'
            }
        )

def account_login():
    # login response
    return ResponseFlow(
        finish=True,
        code=200,
        content={
            'message':'Login success.'
        }
    )
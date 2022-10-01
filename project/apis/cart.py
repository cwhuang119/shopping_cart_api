from apis import cart_controller as controller
from flask import request,session
from helper.logics import verify_login, verify_product_name, add_product_to_cart, checkout
from flasgger import swag_from

@controller.route('/add',methods=['POST'])
@swag_from('api_specs/cart_add.yml')
def cart_add():
    # get username and cart from session
    username,cart = session.get('username'),session.get('cart')
    
    # verify username and cart is not None and valid
    login_verification = verify_login(username,cart)
    if login_verification.finish:
        return login_verification.to_json_response()
    
    # get product name from request
    product_name = request.form.get('product_name')

    # verify product name is valid and within DB
    product_verification = verify_product_name(username,cart,product_name)
    if product_verification.finish:
        return product_verification.to_json_response()
    
    # add item to cart(session) and subtract inventory from DB
    add_cart_verification = add_product_to_cart(username,cart,product_name)
    return add_cart_verification.to_json_response()

@controller.route('/checkout',methods=['POST'])
@swag_from('api_specs/cart_checkout.yml')
def cart_checkout():
    # get username and cart from session
    username,cart = session.get('username'),session.get('cart')

    # verify username and cart is not None and valid
    login_verification = verify_login(username,cart)
    if login_verification.finish:
        return login_verification.to_json_response()
    
    # checkout and get order response
    order_response = checkout(username,cart)
    return order_response.to_json_response()

from flask import make_response, jsonify

class ResponseFlow:
    """
    ResponseFlow instance can be convert to flask response
    flow control is able to use finish protery to 
    determine whether return data to client or continue to operate
    """
    def __init__(self,finish=True,code=200,content={}):
        self.finish = finish
        self.code = code
        self.content = content
    
    def to_json_response(self):
        response = make_response(jsonify(self.content),self.code)
        response.headers["Content-Type"] = "application/json"
        return response


class CartOp:

    """
    CartOp
    since flask session can only be dictionary type 
    these functions are able to help manipulate data inside dictionary(cart)
    """

    @classmethod
    def get_user_cart(cls, username, cart):
        if username in cart:
            return cart[username]
        else:
            cart[username]={}
            return cart[username]
    @classmethod
    def get_quantity(cls, username, cart, product_name):
        user_cart = cls.get_user_cart(username, cart)
        if product_name not in user_cart:
            return 0
        return user_cart[product_name]

    @classmethod
    def add_item(cls, username, cart, product_name, quantity=1):
        user_cart = cls.get_user_cart(username, cart)
        if product_name not in user_cart:
            user_cart[product_name] = quantity
        else:
            user_cart[product_name]+=quantity
        return cart
    @classmethod
    def checkout(cls, username, cart, price_list):
        user_cart = cls.get_user_cart(username, cart)
        total_amount = 0
        total_quantities = 0
        cart_list = {}
        for product_name,quantity in user_cart.items():
            price = price_list[product_name]
            total_amount+=quantity*price
            total_quantities+=quantity
            cart_list[product_name] = {
                'price':price,
                'quantity':quantity
            }
        return total_amount,total_quantities,cart_list
    

    @classmethod
    def empty_cart(cls, username, cart):
        if username in cart:
            del cart[username]
        return cart
from flask import Blueprint

account_controller = Blueprint('account',__name__)
cart_controller = Blueprint('cart',__name__)

from . import account
from . import cart

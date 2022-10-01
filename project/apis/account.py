from flask import session
from apis import account_controller as controller
from helper.logics import account_login
from flasgger import swag_from

@controller.route('/login',methods=['POST'])
@swag_from('api_specs/login.yml')
def login():
    # setup username and init cart
    session['username'] = 'test_account'
    session['cart'] = {}
    session.permanent = True

    # generate login response
    login_verification = account_login()
    return login_verification.to_json_response()


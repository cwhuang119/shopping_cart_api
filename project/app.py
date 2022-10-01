from flask import Flask
from configs import ProductionConfig
from apis import account_controller,cart_controller
from helper.utils import ResponseFlow
from flasgger import Swagger, swag_from
# init app instance
app = Flask(__name__)
# setup swagger docs
swagger = Swagger(app)

# update with production configs
app.config.from_object(ProductionConfig)

# 404 error handler
@app.errorhandler(404)
def page_not_found(error):
    return ResponseFlow(
        finish=True,
        code=404,
        content={
            'message':'Page not found'
        }
    ).to_json_response()

# other error handler
# @app.errorhandler(Exception)
# def page_not_found(error):
#     return ResponseFlow(
#         finish=True,
#         code=500,
#         content={
#             'message':f'Internal server error',
#         }
#     ).to_json_response()


# registering blueprints
app.register_blueprint(account_controller, url_prefix='/account')
app.register_blueprint(cart_controller, url_prefix='/cart')

if __name__=='__main__':

    app.run(host='0.0.0.0',port=8000)
from textwrap import indent
from urllib import response
from chalice import Chalice
from tda import auth, client
import os
import json
import datetime
from chalicelib import config

app = Chalice(app_name='tda-api')

token_path = os.path.join(os.path.dirname(__file__), 'chalicelib', 'token.json')

c = auth.client_from_token_file(config.token_path, config.api_key)


@app.route('/quote/{symbol}')
def quote(symbol):
    response = c.get_quote(symbol)
    
    return response.json()

@app.route('/option/chain/{symbol}')
def option_chain(symbol):
    response = c.get_option_chain(symbol)

    return response.json()

@app.route('/option/order', methods=['POST'])
def option_order():
    webhook_message = app.current_request.json_body

    print(webhook_message)

    if 'passphase' not in webhook_message:
        return {
            "code": "error",
            "message": "Unauthorized, no passphrase"
        }

    if webhook_message['passphrase'] != config.passphrase:
        return {
            "code": "error",
            "message": "Invalid passphrase"
        }

    order_spec = {
        "complexOrderStrategyType": "NONE",
        "orderType": "LIMIT",
        "session": "NORMAL",
        "price": webhook_message["price"],
        "duration": "DAY",
        "orderStrategyType": "SINGLE",
        "orderLegCollection": [
            {
            "instruction": "BUY_TO_OPEN",
            "quantity": webhook_message["quantity"],
            "instrument": {
                "symbol": webhook_message["symbol"],
                "assetType": "OPTION"
            }
            }
        ]
    }

    response = c.place_order(config.account_id, order_spec)

    return {
        "code": "ok"
    }

# The view function above will return {"hello": "world"}
# whenever you make an HTTP GET request to '/'.
#
# Here are a few more examples:
#
# @app.route('/hello/{name}')
# def hello_name(name):
#    # '/hello/james' -> {"hello": "james"}
#    return {'hello': name}
#
# @app.route('/users', methods=['POST'])
# def create_user():
#     # This is the JSON body the user sent in their POST request.
#     user_as_json = app.current_request.json_body
#     # We'll echo the json body back to the user in a 'user' key.
#     return {'user': user_as_json}
#
# See the README documentation for more examples.
#

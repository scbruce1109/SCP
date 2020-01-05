import requests
import base64
import json

from django.conf import settings

PAYPAL_CLIENT_ID = getattr(settings, "PAYPAL_CLIENT_ID")
PAYPAL_CLIENT_SECRET = getattr(settings, "PAYPAL_CLIENT_SECRET")



def get_paypal_token():
    client_id = PAYPAL_CLIENT_ID
    client_secret = PAYPAL_CLIENT_SECRET

    credentials = "%s:%s" % (client_id, client_secret)
    encode_credential = base64.b64encode(credentials.encode('utf-8')).decode('utf-8').replace("\n", "")

    headers = {
        "Authorization": ("Basic %s" % encode_credential),
        'Accept': 'application/json',
        'Accept-Language': 'en_US',
    }

    param = {
        'grant_type': 'client_credentials',
    }

    url = 'https://api.sandbox.paypal.com/v1/oauth2/token'
    r = requests.post(url, headers=headers, data=param)
    ting = json.loads(r.text)
    token = ting.get('access_token')
    if token is not None:
        print(token)
        return token
    return None


def get_order_details(order_id):
    print(order_id)
    token = get_paypal_token()
    url = 'https://api.sandbox.paypal.com/v2/checkout/orders/' + order_id
    headers = {
        "Content-Type": "application/json",
        "Authorization": ("Bearer %s" % token),
    }
    r = requests.get(url, headers=headers)
    detail_json = json.loads(r.text)
    return detail_json

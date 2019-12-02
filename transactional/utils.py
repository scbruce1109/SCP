import json
import hashlib
import json
import re
import requests

from django.conf import settings

SENDINBLUE_API_KEY = getattr(settings, "SENDINBLUE_API_KEY_V3", None)


def get_subscriber_hash(member_email):
    check_email(member_email)
    member_email = member_email.lower().encode()
    m = hashlib.md5(member_email)
    return m.hexdigest()


def check_email(email):
    if not re.match(r".+@.+\..+", email):
        raise ValueError('String passed is not a valid email address')
    return email


class SendInBlue(object):
    def __init__(self):
        super(SendInBlue, self).__init__()
        self.key = SENDINBLUE_API_KEY
        self.api_url = 'https://api.sendinblue.com/v3/'
        self.headers = {
        'api-key': self.key,
        'accept': "application/json",
        'content-type': "application/json"
        }

    def add_contact(self, email):
        contact_endpoint = 'contacts'
        url = self.api_url + contact_endpoint
        data = {
            'email': email,
            'updateEnabled': False
        }

        response = requests.request("POST", url, data=json.dumps(data), headers=self.headers)
        return response.text

import json
import hashlib
import json
import re
import requests

from django.conf import settings

SENDINBLUE_API_KEY = getattr(settings, "SENDINBLUE_API_KEY_V3", None)


def get_email_hash(member_email):
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

    def add_contact(self, email, attributes=None):
        contact_endpoint = 'contacts'
        url = self.api_url + contact_endpoint
        data = {
            'email': email,
            'updateEnabled': False
        }

        if attributes:
            atts = {
                'FNAME': attributes['FNAME'],
                'LNAME': attributes['LNAME']
            }
            data['attributes'] = atts

        response = requests.request("POST", url, data=json.dumps(data), headers=self.headers)
        return response.text


    def update_contact(self, email, attributes):
        url = self.api_url + 'contacts/' + email
        data = {
            'attributes': {
                'FIRSTNAME': attributes['FNAME'],
                'LASTNAME': attributes['LNAME']
            }
        }

        response = requests.request('PUT', url, data=json.dumps(data), headers=self.headers)
        return response


    def send_transactional_email(self, email, html, text, subject):
        url = self.api_url + '/smtp/email'
        data = {
            'sender': {
                'name': 'Steve from SplitCloud',
                'email': 'bruce.stephenc@gmail.com'
            },
            'to': [{
                'email': email,
            }],
            'htmlContent': html,
            'textContent': text,
            'subject': subject,
            'replyTo': {
                'email': 'bruce.stephenc@gmail.com'
            },
        }
        response = requests.request('POST', url, data=json.dumps(data), headers=self.headers)
        return response



    def send_contact_email(self, name, email, html, text, subject):
        url = self.api_url + '/smtp/email'
        data = {
            'sender': {
                'name': name,
                'email': email
            },
            'to': [{
                'email': 'bruce.stephenc@gmail.com',
            }],
            'htmlContent': html,
            'textContent': text,
            'subject': subject,
            'replyTo': {
                'email': email
            },
        }
        response = requests.request('POST', url, data=json.dumps(data), headers=self.headers)
        return response

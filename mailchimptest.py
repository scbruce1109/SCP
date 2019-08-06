import requests
import json

def subscribe():
    key = "9e79de70011408f4e910afaa8d6e683f-us20"
    list_id = "4b77bf728d"
    data_center = 'us20'


    data = {"email_address": "guy@place.com", "status": "subscribed"}

    url = 'https://us20.api.mailchimp.com/3.0/lists/4b77bf728d/members'

    r = requests.put(url, auth=("", key), data=json.dumps(data))
    return r.status_code, r.json()

print(subscribe())

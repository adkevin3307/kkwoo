import json
import requests
from kkbox_developer_sdk.auth_flow import KKBOXOAuth

access_token = ''

host = 'https://api.kkbox.com/v1.1/'
headers = {
    'accept': 'application/json',
    'authorization': 'Bearer {}'.format(access_token),
}

def me():
    r = requests.get(host + 'me', headers = headers)
    return json.loads(r.text)

def playlists(limit):
    r = requests.get(host + 'me/playlists?limit={}'.format(limit), headers = headers)
    return json.loads(r.text)
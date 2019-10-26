import json
import requests
from flask import session
from kkbox_developer_sdk.auth_flow import KKBOXOAuth

with open('config.json', 'r') as file:
    config = json.load(file)

def _getHeader():
    headers = {
        'accept': 'application/json',
        'authorization': 'Bearer {}'.format(session.get('access_token'))
    }
    return headers

def access_token(code):
    url = 'https://account.kkbox.com/oauth2/token'
    headers = {
        'Accept': 'application/x-www-form-urlencoded',
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    data = {
        'grant_type': 'authorization_code',
        'code': code,
        'client_id': config['ID'],
        'client_secret': config['SECRET']
    }
    r = requests.post(url, headers = headers, data = data)
    session['access_token'] = json.loads(r.text)['access_token']

def me():
    r = requests.get('https://api.kkbox.com/v1.1/me', headers = _getHeader())
    session['user_id'] = json.loads(r.text)['id']

def playlist_tracks(playlist_id):
    r = requests.get('https://api.kkbox.com/v1.1/shared-playlists/{}/tracks'.format(playlist_id), headers = _getHeader())
    return json.loads(r.text)

def artist_albums(artist_id):
    r = requests.get('https://api.kkbox.com/v1.1/artists/{}/albums'.format(artist_id), headers = _getHeader())
    return json.loads(r.text)

def album_tracks(album_id):
    r = requests.get('https://api.kkbox.com/v1.1/albums/{}/tracks'.format(album_id), headers = _getHeader())
    return json.loads(r.text)

def user_album_collection(user_id):
    r = requests.get('https://api.kkbox.com/v1.1/users/{}/album-collection'.format(user_id), headers = _getHeader())
    return json.loads(r.text)

def user_playlist_collection(user_id):
    r = requests.get('https://api.kkbox.com/v1.1/users/{}/playlist-collection'.format(user_id), headers = _getHeader())
    return json.loads(r.text)

def user_shared_playlists(user_id):
    r = requests.get('https://api.kkbox.com/v1.1/users/{}/shared-playlists'.format(user_id), headers = _getHeader())
    return json.loads(r.text)
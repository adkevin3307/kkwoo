import json
import requests
from flask import session
from kkbox_developer_sdk.auth_flow import KKBOXOAuth

with open('config.json', 'r') as file:
    config = json.load(file)

territories = ['TW', 'HK', 'SG', 'MY', 'JP']

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
    session['username'] = json.loads(r.text)['name']
    session['room'] = session.get('user_id')

def playlist_tracks(playlist_id):
    result = {'data': []}
    for territory in territories:
        r = requests.get('https://api.kkbox.com/v1.1/shared-playlists/{}/tracks?territory={}'.format(playlist_id, territory), headers = _getHeader())
        data = json.loads(r.text)
        if 'data' in data:
            result['data'].extend(data['data'])
    return result

def artist_albums(artist_id):
    result = {'data': []}
    for territory in territories:
        r = requests.get('https://api.kkbox.com/v1.1/artists/{}/albums?territory={}'.format(artist_id, territory), headers = _getHeader())
        data = json.loads(r.text)
        if 'data' in data:
            result['data'].extend(data['data'])
    return result

def album_tracks(album_id):
    result = {
        'summary': {
            'total': 0
        }
    }
    for territory in territories:
        r = requests.get('https://api.kkbox.com/v1.1/albums/{}/tracks?territory={}'.format(album_id, territory), headers = _getHeader())
        data = json.loads(r.text)
        if 'data' in data and 'summary' in data:
            result['summary']['total'] += data['summary']['total']
    return result

def user_album_collection(user_id):
    r = requests.get('https://api.kkbox.com/v1.1/users/{}/album-collection'.format(user_id), headers = _getHeader())
    return json.loads(r.text)

def user_playlist_collection(user_id):
    r = requests.get('https://api.kkbox.com/v1.1/users/{}/playlist-collection'.format(user_id), headers = _getHeader())
    return json.loads(r.text)

def user_shared_playlists(user_id):
    r = requests.get('https://api.kkbox.com/v1.1/users/{}/shared-playlists'.format(user_id), headers = _getHeader())
    return json.loads(r.text)

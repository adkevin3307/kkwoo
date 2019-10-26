import kkbox_api
from collections import defaultdict

def _calculate(user_id):
    artist = defaultdict(int)
    albums = kkbox_api.user_album_collection(user_id)['data']
    playlists = kkbox_api.user_playlist_collection(user_id)['data']
    shared_playlists = kkbox_api.user_shared_playlists(user_id)['data']

    for album in albums:
        artist[album['artist']['id']] += kkbox_api.album_tracks(album['id'])['data']['track_number']
    for playlist in playlists:
        for track in kkbox_api.playlist_tracks(playlist['id'])['data']:
            artist[track['artist']['id']] += 1
    for playlist in shared_playlists:
        for track in kkbox_api.playlist_tracks(playlist['id'])['data']:
            artist[track['artist']['id']] += 1
    
    return artist

def rate(user_id_1, user_id_2):
    weight = 0
    artist_1 = _calculate(user_id_1)
    artist_2 = _calculate(user_id_2)
    same_artist = set(artist_1.keys()) & set(artist_2.keys())
    for artist in same_artist:
        artist_weight = (artist_1[artist] * artist_2[artist]) ** 2
        artist_total = 0
        for album in kkbox_api.artist_albums(artist)['data']:
            artist_total += kkbox_api.album_tracks(album['id'])['data']['track_number']
        weight += artist_weight / artist_total
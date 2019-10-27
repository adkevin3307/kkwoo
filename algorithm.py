import kkbox_api
from collections import defaultdict

def _getArtist(user_id):
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

def _artist_tracks(artist_id):
    total_tracks = 0
    for album in kkbox_api.artist_albums(artist_id)['data']:
        total_tracks += kkbox_api.album_tracks(album['id'])['data']['track_number']
    return total_tracks

def _calculate(artist_1, artist_2):
    success = []
    artist_ids = set(artist_1.keys()) | set(artist_2.keys())
    for artist_id in artist_ids:
        n = _artist_tracks(artist_id)
        n1, n2 = artist_1[artist_id], artist_2[artist_id]
        rate = (n1 * n2) / ((n ** 0.5) * abs(n1 - n2 + 1))
        success.append(rate >= (0.6 * n))
    return sum(success) / len(success)

def is_suit(user_id_1, user_id_2):
    artist_1 = _getArtist(user_id_1)
    artist_2 = _getArtist(user_id_2)
    success_rate = _calculate(artist_1, artist_2)
    return success_rate >= 0.25
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv
import spotipy
import random
import os

load_dotenv(dotenv_path="./config/.env")

CLIENT_ID = os.environ.get('CLIENT_ID')
SECRET_KEY = os.environ.get('SECRET_KEY')
REDIRECT_URI = os.environ.get('REDIRECT_URI')

def get_music(search_query):
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=CLIENT_ID, client_secret=SECRET_KEY, redirect_uri=REDIRECT_URI))
    result = sp.search(f'{search_query}', limit=50, type='track')
    
    if result['tracks']['items']:
        random_track = random.choice(result['tracks']['items'])
        track_info = {
            'artist': random_track['artists'][0]['name'],
            'title': random_track['name'],
            'music_url': random_track['external_urls']['spotify'],
            'thumbnail': random_track['album']['images'][0]['url']
        }
        print(track_info)
        return result_music(track_info)
    else:
        return None
    
def result_music(playlist):
    music_body = {
        "thumbnail": playlist['thumbnail'],
        "song_title": f"{playlist['artist']} - {playlist['title']}",
        "artist": playlist['artist'],
        "music_url": playlist['music_url']
    }
    return music_body
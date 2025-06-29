from spotipy.oauth2 import SpotifyOAuth
from fastapi.responses import RedirectResponse
from data.config import SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET, SPOTIFY_REDIRECT_URI
from fastapi import Query
import spotipy
from models.defs import get_lyrics

# Spotipy OAuth setup
sp_oauth = SpotifyOAuth(
client_id=SPOTIFY_CLIENT_ID,
client_secret=SPOTIFY_CLIENT_SECRET,
redirect_uri=SPOTIFY_REDIRECT_URI,
scope="user-read-currently-playing",
)


def spotify_login():
    auth_url = sp_oauth.get_authorize_url()
    return RedirectResponse(auth_url)


def callback(code: str):
    token_info = sp_oauth.get_access_token(code)
    # Store the token in a session or database in production
    # For now, we'll redirect to current-song with the token
    return RedirectResponse(url=f"/current-song?access_token={token_info['access_token']}")


def current_song(access_token: str = Query(...)):
    sp = spotipy.Spotify(auth=access_token)
    current_track = sp.current_user_playing_track()

    if not current_track:
        # If no song is playing, show a message
        return {
            "song": "",
            "artist": "",
            "lyrics": "No song currently playing."
        }
        
    
    song_name = current_track["item"]["name"]
    artist = current_track["item"]["artists"][0]["name"]
    lyrics = get_lyrics(song_name, artist)
    
    return {
            "song": song_name,
            "artist": artist,
            "lyrics": lyrics
        }    
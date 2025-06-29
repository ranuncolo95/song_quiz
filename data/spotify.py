from spotipy.oauth2 import SpotifyOAuth
from fastapi.responses import RedirectResponse
from data.config import SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET, SPOTIFY_REDIRECT_URI


def spotify_login():
    # Spotipy OAuth setup
    sp_oauth = SpotifyOAuth(
    client_id=SPOTIFY_CLIENT_ID,
    client_secret=SPOTIFY_CLIENT_SECRET,
    redirect_uri=SPOTIFY_REDIRECT_URI,
    scope="user-read-currently-playing",
    )

    auth_url = sp_oauth.get_authorize_url()
    return RedirectResponse(auth_url)
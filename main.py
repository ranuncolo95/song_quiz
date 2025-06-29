from fastapi import FastAPI, Request, HTTPException, Depends, Query, Form
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from spotipy.oauth2 import SpotifyOAuth
from pydantic import BaseModel
from typing import Optional
import requests
import spotipy
import os
from web import lyric as web
from models.song import Song

app = FastAPI()
templates = Jinja2Templates(directory="view/templates")
app.mount("/static", StaticFiles(directory="view/static"), name="static")

app.include_router(web.router)


@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse(request=request, name="index.html")


@app.post("/result", response_class=HTMLResponse)
async def get_lyric(request: Request, 
             artist: str = Form(...), 
             song: str = Form(...)):

        lyric = web.get_one(artist, song)
        url = Song(artist, song).url

        return templates.TemplateResponse(request=request, 
                                        name="result.html", 
                                        context={'song': song, "artist" : artist, "lyric" : lyric, "url" : url})


from dotenv import load_dotenv
load_dotenv()  # Load environment variables from .env


# Load Spotify credentials from .env
SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
SPOTIFY_REDIRECT_URI = "https://129d-151-59-7-64.ngrok-free.app/callback"  # Must match Spotify Dashboard

# Spotipy OAuth setup
sp_oauth = SpotifyOAuth(
    client_id=SPOTIFY_CLIENT_ID,
    client_secret=SPOTIFY_CLIENT_SECRET,
    redirect_uri=SPOTIFY_REDIRECT_URI,
    scope="user-read-currently-playing",
)

# Model for the current song
class CurrentSong(BaseModel):
    song: str
    artist: str
    lyrics: Optional[str] = None

# --- Routes ---

@app.get("/spotify-login")
async def spotify_login():
    auth_url = sp_oauth.get_authorize_url()
    return RedirectResponse(auth_url)

@app.get("/callback")
async def callback(code: str):
    token_info = sp_oauth.get_access_token(code)
    # Store the token in a session or database in production
    # For now, we'll redirect to current-song with the token
    return RedirectResponse(url=f"/current-song?access_token={token_info['access_token']}")

@app.get("/current-song", response_class=HTMLResponse)
async def current_song(request: Request, access_token: str = Query(...)):
    sp = spotipy.Spotify(auth=access_token)
    current_track = sp.current_user_playing_track()
    
    if not current_track:
        # If no song is playing, show a message
        return templates.TemplateResponse(
            "current_song.html",
        {
            "request": request,
            "song": "",
            "artist": "",
            "lyrics": "No song currently playing."
        }
        )
    
    song_name = current_track["item"]["name"]
    artist = current_track["item"]["artists"][0]["name"]
    lyrics = await get_lyrics(song_name, artist)
    
    return templates.TemplateResponse(
        "current_song.html",
        {
            "request": request,
            "song": song_name,
            "artist": artist,
            "lyrics": lyrics
        }
    )

# --- Lyrics Fetching ---
async def get_lyrics(song: str, artist: str) -> str:
    try:
        response = requests.get(f"https://api.lyrics.ovh/v1/{artist}/{song}")
        return response.json().get("lyrics", "Lyrics not found.")
    except:
        return "Could not fetch lyrics."

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", reload=True)


from fastapi import FastAPI, Request, HTTPException, Query, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from web import lyric as web_lyric
from web import spotify as web_spotify
from models.song import Song

app = FastAPI()
templates = Jinja2Templates(directory="view/templates")
app.mount("/static", StaticFiles(directory="view/static"), name="static")


@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse(request=request, name="index.html")


@app.post("/result", response_class=HTMLResponse)
async def get_lyric(request: Request, 
             artist: str = Form(...), 
             song: str = Form(...)):

        lyric = web_lyric.get_one(artist, song)
        url = Song(artist, song).url

        return templates.TemplateResponse(request=request, 
        name="result.html", 
        context={'song': song, "artist" : artist, "lyrics" : lyric, "url" : url})


# --- Spotify Routes ---

@app.get("/spotify-login")
def spotify_login():
    return web_spotify.spotify_login()

@app.get("/callback")
def callback(code: str):
    return web_spotify.callback(code)

@app.get("/current-song", response_class=HTMLResponse)
async def current_song(request: Request, access_token: str = Query(...)):
    r = web_spotify.current_song(access_token)

    return templates.TemplateResponse(request=request, 
    name="result.html", 
    context={'song': r["song"], "artist" : r["artist"], "lyrics" : r["lyrics"], "url" : "Spotify current song"})


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", reload=True)


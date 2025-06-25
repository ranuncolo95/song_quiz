from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from web import lyric as web
from models.song import Song
from fastapi.templating import Jinja2Templates


app = FastAPI()
templates = Jinja2Templates(directory="view/templates")

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



if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", reload=True)
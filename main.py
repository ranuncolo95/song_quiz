from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from web import lyric
from fastapi.templating import Jinja2Templates


app = FastAPI()
templates = Jinja2Templates(directory="view/templates")

app.include_router(lyric.router)


@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse(request=request, name="index.html")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", reload=True)
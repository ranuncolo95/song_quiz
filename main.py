from fastapi import FastAPI
from web import lyric

app = FastAPI()

app.include_router(lyric.router)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", reload=True)
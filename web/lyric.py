from fastapi import APIRouter, HTTPException
from models.song import Song
from service import lyric as service


router = APIRouter(prefix = "/lyric")


@router.get("")
@router.get("/")

def get_one(artist: str, song: str):
    return service.get_one(artist, song)

@router.get("/{name}")

def get_one(artist: str, song: str):
    return service.get_one(artist, song)


#router.post("", status_code=201)
#router.post("/", status_code=201)

#def create(explorer: Song):
#    return service.create(explorer)
    
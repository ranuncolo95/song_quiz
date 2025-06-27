from fastapi import APIRouter, HTTPException
from models.song import Song
from service import lyric as service


router = APIRouter(prefix = "/lyric")


@router.get("")
@router.get("/")

def get_one(artist: str, song: str):
    return service.get_one(artist, song)
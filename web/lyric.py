from fastapi import  HTTPException
from service import lyric as service


def get_one(artist: str, song: str):
    return service.get_one(artist, song)
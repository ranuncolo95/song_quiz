from fastapi import  HTTPException
from service import spotify as service


def spotify_login():
    return service.spotify_login()
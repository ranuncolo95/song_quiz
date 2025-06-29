from fastapi import  HTTPException
from service import spotify as service
from fastapi import HTTPException, Query


def spotify_login():
    return service.spotify_login()


def callback(code: str):
    return service.callback(code)


def current_song(access_token: str = Query(...)):
    return service.current_song(access_token)
from data import spotify as data
from fastapi import HTTPException, Query

def spotify_login():
    return data.spotify_login()


def callback(code: str):
    return data.callback(code)


def current_song(access_token: str = Query(...)):
    return data.current_song(access_token)
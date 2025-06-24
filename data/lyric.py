from models.song import Song


def get_one(artist: str, song: str):
    lyric = Song(artist, song).lyrics
    return lyric
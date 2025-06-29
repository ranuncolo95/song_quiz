from pydantic import BaseModel
from typing import Optional
from .defs import *

class Song():
  def __init__(self, artist: str, song: str):

    self.artist = artist
    self.song = song
    self.url = create_genius_url(artist, song)

    lyrics = scrape_genius_lyrics(self.url)
    lyrics = erase_before_bracket(lyrics)
    lyrics = remove_text_inside_brackets(lyrics)
    lyrics = adjust_lowercase_starts(lyrics)
    lyrics = extract_parenthetical_blocks(lyrics)
    lyrics = merge_comma_lines(lyrics)

    self.lyrics = lyrics

  # Model for the current song
class CurrentSong(BaseModel):
    song: str
    artist: str
    lyrics: Optional[str] = None
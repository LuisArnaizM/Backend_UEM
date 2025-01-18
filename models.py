from pydantic import BaseModel, EmailStr, Field
from typing import List

class User(BaseModel):
    id: str = None
    name: str
    email: EmailStr
    age: int

class Preference(BaseModel):
    user_id: int
    favorite_genres: List[str]
    favorite_artists: List[str]

class SpotifyTrack(BaseModel):
    track_name: str
    artist_name: str
    album_name: str

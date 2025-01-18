from fastapi import APIRouter, HTTPException, Query
from models import SpotifyTrack
from fastapi.responses import RedirectResponse
import requests
import os
from utils import get_access_token, get_user_top_items
from dotenv import load_dotenv

load_dotenv()

router = APIRouter()
CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
REDIRECT_URI = os.getenv("SPOTIFY_REDIRECT_URI")

SPOTIFY_SEARCH_URL = "https://api.spotify.com/v1/search"
SPOTIFY_AUTH_URL = "https://accounts.spotify.com/authorize"
SPOTIFY_TOKEN_URL = "https://accounts.spotify.com/api/token"
SPOTIFY_TOP_ITEMS_URL = "https://api.spotify.com/v1/me/top/{type}"

user_tokens = {}

@router.get("/tracks", response_model=SpotifyTrack)
def search_track(query: str):
    token = get_access_token()
    headers = {"Authorization": f"Bearer {token}"}
    params = {"q": query, "type": "track", "limit": 1}
    response = requests.get(SPOTIFY_SEARCH_URL, headers=headers, params=params)
    if response.status_code != 200:
        raise HTTPException(status_code=500, detail="Failed to fetch track data")
    data = response.json()
    track = data['tracks']['items'][0]
    return SpotifyTrack(
        track_name=track['name'],
        artist_name=track['artists'][0]['name'],
        album_name=track['album']['name']
    )
    # for track in data['tracks']['items']
    # ]
@router.get("/")
def home():
    """
    Redirige al usuario a la página de autenticación de Spotify.
    """
    scope = "user-top-read"
    auth_url = (
        f"{SPOTIFY_AUTH_URL}?"
        f"client_id={CLIENT_ID}&response_type=code&redirect_uri={REDIRECT_URI}&scope={scope}"
    )
    return RedirectResponse(auth_url)


@router.get("/callback")
def callback(code: str):
    if not code:
        raise HTTPException(status_code=400, detail="Código de autorización no proporcionado")
    """
    Maneja el flujo de autorización de Spotify y obtiene un token.
    """
    data = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": REDIRECT_URI,
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
    }

    response = requests.post(SPOTIFY_TOKEN_URL, data=data)
    if response.status_code != 200:
        raise HTTPException(status_code=400, detail="Error al obtener el token")

    token_data = response.json()
    user_tokens["access_token"] = token_data["access_token"]
    user_tokens["refresh_token"] = token_data["refresh_token"]
    return {"message": "Autenticación exitosa", "tokens": token_data}


@router.get("/top-items/{item_type}")
def get_top_items(
    item_type: str,
    time_range: str = Query("short_term", regex="^(short_term|medium_term|long_term)$"),
    limit: int = Query(10, ge=1, le=50),
):
    """
    Devuelve los artistas o pistas principales del usuario.
    """
    # Recuperar el token de acceso del usuario
    access_token = user_tokens.get("access_token")
    if not access_token:
        raise HTTPException(status_code=401, detail="Usuario no autenticado")

    # Usar la función get_user_top_items para obtener los elementos principales
    top_items = get_user_top_items(access_token, item_type, time_range, limit)
    
    # Verificar si la solicitud a la API de Spotify fue exitosa
    if not top_items:
        raise HTTPException(status_code=400, detail="Error al obtener los elementos principales")
    
    return top_items
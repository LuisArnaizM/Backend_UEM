from fastapi import APIRouter, HTTPException, Query
from models import SpotifyTrack
from fastapi.responses import RedirectResponse
import requests
import os
from utils import get_access_token
from dotenv import load_dotenv

#Almacenamiento de tokens
import json

# Guardar el token en un archivo
def save_tokens_to_file(tokens):
    with open("tokens.json", "w") as file:
        json.dump(tokens, file)

# Cargar el token desde un archivo
def load_tokens_from_file():
    try:
        with open("tokens.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return None

load_dotenv("../config.env")

router = APIRouter()
CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
REDIRECT_URI = os.getenv("SPOTIFY_REDIRECT_URI")

SPOTIFY_SEARCH_URL = "https://api.spotify.com/v1/search"
SPOTIFY_AUTH_URL = "https://accounts.spotify.com/authorize"
SPOTIFY_TOKEN_URL = "https://accounts.spotify.com/api/token"
SPOTIFY_TOP_ITEMS_URL = "https://api.spotify.com/v1/me/top/{type}"

user_tokens = {}


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
    save_tokens_to_file(token_data)

    return {"message": "Autenticación exitosa", "tokens": token_data}


@router.get("/top-items/{item_type}")
def get_top_items(
    item_type: str,
    time_range: str = Query("short_term", regex="^(short_term|medium_term|long_term)$"),
    limit: int = Query(10, ge=1, le=50),
):
    tokens = load_tokens_from_file()
    """
    Devuelve los artistas o pistas principales del usuario.
    """
    access_token = tokens.get("access_token")
    if not access_token:
        raise HTTPException(status_code=401, detail="Usuario no autenticado")

    url = SPOTIFY_TOP_ITEMS_URL.format(type=item_type)
    headers = {"Authorization": f"Bearer {access_token}"}
    params = {"time_range": time_range, "limit": limit}

    response = requests.get(url, headers=headers, params=params)

    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.json())

    return response.json()

@router.get("/tracks")
def search_track(query: str):
    """
    Busca una pista por su nombre.
    """
    access_token = user_tokens.get("access_token")
    if not access_token:
        raise HTTPException(status_code=401, detail="Usuario no autenticado")

    headers = {"Authorization": f"Bearer {access_token}"}
    params = {"q": query, "type": "track", "limit": 1}
    response = requests.get(SPOTIFY_SEARCH_URL, headers=headers, params=params)
    if response.status_code != 200:
        raise HTTPException(status_code=500, detail="Error al buscar la pista")
    
    data = response.json()
    if not data['tracks']['items']:
        raise HTTPException(status_code=404, detail="Pista no encontrada")

    track = data['tracks']['items'][0]
    return {
        "track_name": track['name'],
        "artist_name": track['artists'][0]['name'],
        "album_name": track['album']['name'],
    }
from fastapi import APIRouter, HTTPException, Request
import requests
import os
from fastapi.responses import JSONResponse
from dotenv import load_dotenv
#Almacenamiento de tokens
import secrets
import httpx
from fastapi.responses import RedirectResponse, JSONResponse
from urllib.parse import urlencode

load_dotenv()

router = APIRouter()
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
SCOPES = "user-top-read"
REDIRECT_URI = "http://localhost:8000/spotify/callback"
SPOTIFY_SEARCH_URL = "https://api.spotify.com/v1/search"
SPOTIFY_AUTH_URL = "https://accounts.spotify.com/authorize"
SPOTIFY_TOKEN_URL = "https://accounts.spotify.com/api/token"
SPOTIFY_TOP_ARTISTS_URL = "https://api.spotify.com/v1/me/top/artists"
SPOTIFY_TOP_TRACKS_URL = "https://api.spotify.com/v1/me/top/tracks"
SPOTIFY_API_URL = "https://api.spotify.com/v1"

states = {}
tokens = {}

from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import RedirectResponse
from urllib.parse import urlencode
import httpx

router = APIRouter()

# Almacenaje temporal de tokens
tokens = {}

# Ruta de login que redirige al usuario a Spotify
@router.get("/login")
async def login():
    # Generar un estado aleatorio para proteger la solicitud
    state = secrets.token_urlsafe(16)
    tokens["state"] = state
    scope = "user-top-read user-read-private user-read-email"

    params = {
        "response_type": "code",
        "client_id": CLIENT_ID,
        "redirect_uri": REDIRECT_URI,
        "scope": scope,
        "state": state
    }

    auth_url = f"{SPOTIFY_AUTH_URL}?{urlencode(params)}"
    return RedirectResponse(auth_url)

# Ruta callback para obtener el token
@router.get("/callback")
async def callback(request: Request):
    """Recibe el código de autorización y solicita los tokens"""

    # Obtener el código y estado de la URL
    code = request.query_params.get('code')
    state = request.query_params.get('state')

    if not code or not state:
        raise HTTPException(status_code=400, detail="Faltan los parámetros 'code' o 'state'")

    # Verificar que el estado sea el esperado
    if state != tokens.get("state"):
        raise HTTPException(status_code=400, detail="Estado inválido")

    # Eliminar el estado después de validarlo
    del tokens["state"]

    # Intercambiar el código de autorización por los tokens
    data = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": REDIRECT_URI,
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET
    }

    headers = {"Content-Type": "application/x-www-form-urlencoded"}

    async with httpx.AsyncClient() as client:
        response = await client.post(SPOTIFY_TOKEN_URL, data=data, headers=headers)

    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail="Error obteniendo token")

    # Guardar los tokens en un diccionario global (en producción usar algo más seguro como base de datos)
    tokens["access_token"] = response.json().get("access_token")
    tokens["refresh_token"] = response.json().get("refresh_token")

    # Devuelve el access_token directamente para ser usado en futuras peticiones
    return {"access_token": tokens["access_token"], "refresh_token": tokens["refresh_token"]}

# Ruta para obtener los artistas más escuchados usando el access_token
@router.get("/top-artists")
async def top_artists():
    """Obtiene los artistas más escuchados usando el access token"""

    access_token = tokens.get("access_token")
    if not access_token:
        raise HTTPException(status_code=401, detail="No se ha obtenido un token de acceso")

    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    async with httpx.AsyncClient() as client:
        response = await client.get(SPOTIFY_TOP_ARTISTS_URL, headers=headers)

    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail="Error obteniendo artistas")

    top_artists = response.json().get("items", [])

    # Mostrar los artistas
    return {"top_artists": top_artists}
# Ruta para obtener los artistas más escuchados usando el access_token
@router.get("/top-tracks")
async def top_artists():
    """Obtiene los artistas más escuchados usando el access token"""

    access_token = tokens.get("access_token")
    if not access_token:
        raise HTTPException(status_code=401, detail="No se ha obtenido un token de acceso")

    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    async with httpx.AsyncClient() as client:
        response = await client.get(SPOTIFY_TOP_TRACKS_URL, headers=headers)

    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail="Error obteniendo artistas")

    top_tracks = response.json().get("items", [])

    # Mostrar los artistas
    return {"top_tracks": top_tracks}

# Ruta para refrescar el access token usando el refresh_token
@router.get("/refresh-token")
async def refresh_token():
    """Renueva el access token usando el refresh token"""

    refresh_token = tokens.get("refresh_token")
    if not refresh_token:
        raise HTTPException(status_code=401, detail="No se ha encontrado un refresh token")

    data = {
        "grant_type": "refresh_token",
        "refresh_token": refresh_token,
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET
    }
    headers = {"Content-Type": "application/x-www-form-urlencoded"}

    async with httpx.AsyncClient() as client:
        response = await client.post(SPOTIFY_TOKEN_URL, data=data, headers=headers)

    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail="Error renovando el token")

    # Actualizar el access token
    tokens["access_token"] = response.json().get("access_token")

    return {"access_token": tokens["access_token"]}

@router.get("/token")
async def get_spotify_token():
    data = {
        "grant_type": "client_credentials",
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET
    }
    headers = {"Content-Type": "application/x-www-form-urlencoded"}

    async with httpx.AsyncClient() as client:
        response = await client.post(SPOTIFY_TOKEN_URL, data=data, headers=headers)

    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail="Error obteniendo token")

    return response.json()

@router.get("/tracks")
def search_track(query: str):
    """
    Busca una pista por su nombre.
    """
    access_token = tokens.get("access_token")
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
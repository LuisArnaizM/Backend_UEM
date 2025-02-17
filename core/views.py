import requests
import os
import secrets
from dotenv import load_dotenv
from django.http import JsonResponse, HttpResponseRedirect
from rest_framework import viewsets
from rest_framework.decorators import api_view
from .models import CustomUser, Preference
from .serializers import UserSerializer, PreferenceSerializer
from rest_framework.response import Response
from base64 import b64encode

load_dotenv()
SPOTIFY_AUTH_URL = "https://accounts.spotify.com/authorize"
SPOTIFY_TOKEN_URL = "https://accounts.spotify.com/api/token"
SPOTIFY_API_URL = "https://api.spotify.com/v1"
SPOTIFY_SEARCH_URL="https://api.spotify.com/v1/search"
# Variables de entorno
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
REDIRECT_URI = os.getenv("REDIRECT_URI")
# tokens = {}

@api_view(['GET'])
def spotify_login(request):
    """Redirige al usuario a Spotify para autenticación"""
    state = secrets.token_urlsafe(16)
    # tokens["state"] = state
    request.session["spotify_state"] = state
    scope = "user-top-read user-read-private user-read-email"
    auth_url = f"https://accounts.spotify.com/authorize?client_id={CLIENT_ID}&response_type=code&redirect_uri={REDIRECT_URI}&scope={scope}&state={state}"
    return HttpResponseRedirect(auth_url)

@api_view(['GET'])
def spotify_callback(request):
    code = request.GET.get('code')
    state = request.GET.get('state')
    if not code:
        return JsonResponse({"error": "No code provided"}, status=400)
    saved_state = request.session.get("spotify_state") 
    if state != saved_state:
        return JsonResponse({"error": "Invalid state"}, status=400)
    data = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": REDIRECT_URI,
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
    }
    response = requests.post(f"{SPOTIFY_TOKEN_URL}", data=data)

    if response.status_code != 200:
        return JsonResponse({"error": "Failed to get token"}, status=500)

    tokens = response.json()
    request.session["spotify_access_token"] = tokens["access_token"]  # Guardamos el token en sesión
    request.session["spotify_refresh_token"] = tokens["refresh_token"]
    return JsonResponse(tokens)

@api_view(["GET"])
def top_artists(request):
    """Obtiene los artistas más escuchados del usuario"""
    access_token = request.session.get("spotify_access_token")
    if not access_token:
        return JsonResponse({"error": "No autenticado"}, status=401)

    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(f"{SPOTIFY_API_URL}/me/top/artists", headers=headers)
    if response.status_code != 200:
        return JsonResponse({"error": "Error obteniendo artistas"}, status=response.status_code)

    return JsonResponse(response.json())

@api_view(["GET"])
def top_tracks(request):
    """Obtiene las canciones más escuchadas del usuario"""
    access_token = request.session.get("spotify_access_token")
    if not access_token:
        return JsonResponse({"error": "No autenticado"}, status=401)

    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(f"{SPOTIFY_API_URL}/me/top/tracks", headers=headers)

    if response.status_code != 200:
        return JsonResponse({"error": "Error obteniendo canciones"}, status=response.status_code)

    return JsonResponse(response.json())
@api_view(["GET"])
def refresh_spotify_token(request):
    """Refresca el token de acceso usando el refresh_token almacenado en sesión"""
    refresh_token = request.session.get("spotify_refresh_token")

    if not refresh_token:
        return JsonResponse({"error": "No refresh token available"}, status=401)

    data = {
        "grant_type": "refresh_token",
        "refresh_token": refresh_token,
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
    }

    response = requests.post(SPOTIFY_TOKEN_URL, data=data)

    if response.status_code != 200:
        return JsonResponse({"error": "Failed to refresh token"}, status=500)

    new_tokens = response.json()

    # Actualizamos solo el access_token (el refresh_token no siempre cambia)
    request.session["spotify_access_token"] = new_tokens.get("access_token")

    return JsonResponse(new_tokens)
api_view(['GET'])

@api_view(['GET'])
def search_track(request):
    """ Busca una pista en Spotify por nombre """
    
    query = request.query_params.get('query')
    
    if not query:
        return Response({"error": "Debes proporcionar un parámetro 'query'."}, status=400)

    access_token = request.session.get("spotify_access_token")

    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    params = {
        "q": query,
        "type": "track",
        "limit": 1
    }

    response = requests.get(SPOTIFY_SEARCH_URL, headers=headers, params=params)

    if response.status_code != 200:
        return Response({"error": "Error en la búsqueda de la pista"}, status=response.status_code)

    data = response.json()
    if not data['tracks']['items']:
        return Response({"error": "Pista no encontrada"}, status=404)

    track = data['tracks']['items'][0]
    return Response({
        "track_name": track['name'],
        "artist_name": track['artists'][0]['name'],
        "album_name": track['album']['name'],
        "preview_url": track.get("preview_url", "No disponible"),
        "external_url": track["external_urls"]["spotify"]
    })
# CRUD de Usuarios
class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer

# CRUD de Preferencias
class PreferenceViewSet(viewsets.ModelViewSet):
    queryset = Preference.objects.all()
    serializer_class = PreferenceSerializer


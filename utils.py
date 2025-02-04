import os
import requests
from dotenv import load_dotenv
import json

import random
import string

load_dotenv('.env')
CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
SPOTIFY_SEARCH_URL = "https://api.spotify.com/v1/search"
SPOTIFY_AUTH_URL = "https://accounts.spotify.com/authorize"
SPOTIFY_TOKEN_URL = "https://accounts.spotify.com/api/token"
SPOTIFY_TOP_ITEMS_URL = "https://api.spotify.com/v1/me/top/{type}"
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
    
def generate_random_string(length: int = 16) -> str:
    """Genera una cadena aleatoria para la autenticación."""
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))


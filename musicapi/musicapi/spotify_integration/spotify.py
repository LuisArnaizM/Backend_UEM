import requests

def get_spotify_data(artist_name):
    headers = {
        'Authorization': 'Bearer YOUR_SPOTIFY_ACCESS_TOKEN',  # Sustituye con tu token de acceso de Spotify
    }

    url = f'https://api.spotify.com/v1/search?q={artist_name}&type=artist&limit=1'
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        artist_info = data['artists']['items'][0]
        return {
            'name': artist_info['name'],
            'genres': artist_info['genres'],
            'followers': artist_info['followers']['total'],
            'spotify_url': artist_info['external_urls']['spotify']
        }
    else:
        return {"error": "Failed to fetch data from Spotify"}

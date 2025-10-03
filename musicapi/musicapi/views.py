from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import User, Preference
from .serializers import UserSerializer, PreferenceSerializer
from .spotify_integration.spotify import get_spotify_data  # Para la integración con Spotify


class UserListCreateView(APIView):
    def get(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserRetrieveUpdateDeleteView(APIView):
    def get(self, request, pk):
        try:
            user = User.objects.get(pk=pk)
        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = UserSerializer(user)
        return Response(serializer.data)

    def put(self, request, pk):
        user = User.objects.get(pk=pk)
        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        user = User.objects.get(pk=pk)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class SpotifySearchView(APIView):
    def get(self, request):
        artist_name = request.query_params.get('artist')
        if artist_name:
            spotify_data = get_spotify_data(artist_name)  # Función para obtener datos de Spotify
            return Response(spotify_data, status=status.HTTP_200_OK)
        return Response({"error": "Artist name is required"}, status=status.HTTP_400_BAD_REQUEST)
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from rest_framework.decorators import api_view
from rest_framework.response import Response

SPOTIFY_CLIENT_ID = 'tu_client_id'
SPOTIFY_CLIENT_SECRET = 'tu_client_secret'

client_credentials_manager = SpotifyClientCredentials(
    client_id=SPOTIFY_CLIENT_ID,
    client_secret=SPOTIFY_CLIENT_SECRET
)
spotify = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

@api_view(['GET'])
def search_artist(request, artist_name):
    results = spotify.search(q=artist_name, type='artist', limit=1)
    return Response(results)

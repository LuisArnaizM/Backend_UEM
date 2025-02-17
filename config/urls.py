"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path
from rest_framework.routers import DefaultRouter
from core.views import spotify_login, spotify_callback, top_artists, top_tracks, refresh_spotify_token, search_track, UserViewSet, PreferenceViewSet

urlpatterns = [
    path("admin/", admin.site.urls),
]
router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'preferences', PreferenceViewSet)

urlpatterns = [
    path("spotify/login/", spotify_login, name="spotify_login"),
    path("spotify/callback/", spotify_callback, name="spotify_callback"),
    path("spotify/get-tracks/", top_tracks, name="get_tracks"),
    path("spotify/get-artists/", top_artists, name="get_artists"),
    path("spotify/refresh-token/", refresh_spotify_token, name="refresh_token"),
    path("spotify/tracks/", search_track, name="search_track"),
] + router.urls

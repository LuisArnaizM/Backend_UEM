from fastapi import FastAPI
from routers import users, preferences, spotify

app = FastAPI(
    title="Music Preferences API",
    description="Gestión de usuarios y sus preferencias musicales con integración de Spotify",
    version="1.0.0"
)

# Registrar los routers
app.include_router(users.router, prefix="/users", tags=["Users"])
app.include_router(preferences.router, prefix="/preferences", tags=["Preferences"])
app.include_router(spotify.router, prefix="/spotify", tags=["Spotify"])

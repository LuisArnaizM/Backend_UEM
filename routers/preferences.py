from fastapi import APIRouter, HTTPException
from models import Preference
from database import get_preferences, save_preferences

router = APIRouter()

@router.post("/", response_model=Preference)
def set_preferences(preference: Preference):
    preferences = get_preferences()
    existing_preference = next((p for p in preferences if p["user_id"] == preference.user_id), None)
    if existing_preference:
        preferences = [p for p in preferences if p["user_id"] != preference.user_id]
    preferences.append(preference.model_dump())
    save_preferences(preferences)
    return preference

@router.get("/{user_id}", response_model=Preference)
def get_preferences(user_id: int):
    preferences = get_preferences()
    preference = next((p for p in preferences if p["user_id"] == user_id), None)
    if not preference:
        raise HTTPException(status_code=404, detail="Preferences not found for user")
    return preference

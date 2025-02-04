from fastapi import APIRouter, HTTPException
from models import Preference
from database import get_preferences as db_get_preferences, save_preferences

router = APIRouter()

@router.post("/", response_model=Preference)
def set_preferences(preference: Preference):
    """Crea o actualiza las preferencias de un usuario."""
    preferences = db_get_preferences()
    preferences = [p for p in preferences if p["user_id"] != preference.user_id]  
    preferences.append(preference.model_dump())  
    save_preferences(preferences)
    return preference

@router.get("/{user_id}", response_model=Preference)
def get_user_preferences(user_id: int):
    """Obtiene las preferencias de un usuario por su ID."""
    preferences = db_get_preferences()
    preference = next((p for p in preferences if p["user_id"] == user_id), None)
    if not preference:
        raise HTTPException(status_code=404, detail="Preferences not found for user")
    return preference

@router.put("/{user_id}", response_model=Preference)
def update_preferences(user_id: int, updated_preference: Preference):
    """Actualiza las preferencias de un usuario si existen."""
    preferences = db_get_preferences()
    index = next((i for i, p in enumerate(preferences) if p["user_id"] == user_id), None)
    if index is None:
        raise HTTPException(status_code=404, detail="Preferences not found for user")
    
    preferences[index] = updated_preference.model_dump()  
    save_preferences(preferences)
    return updated_preference

@router.delete("/{user_id}")
def delete_preferences(user_id: int):
    """Elimina las preferencias de un usuario por su ID."""
    preferences = db_get_preferences()
    new_preferences = [p for p in preferences if p["user_id"] != user_id]
    
    if len(preferences) == len(new_preferences):  
        raise HTTPException(status_code=404, detail="Preferences not found for user")
    
    save_preferences(new_preferences)
    return {"message": "Preferences deleted successfully"}

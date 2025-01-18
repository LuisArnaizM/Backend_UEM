from fastapi import APIRouter, HTTPException
from models import User
from database import get_users, save_users
import uuid

router = APIRouter()


@router.post("/", response_model=User)
def create_user(user: User):
    """
    Crear un nuevo usuario con ID único generado automáticamente.
    """
    users = get_users()  # Obtener la lista de usuarios existentes
    
    # Generar un ID único
    user_id = str(uuid.uuid4())
    user.id = user_id  # Asignar el ID generado al usuario
    
    users.append(user.model_dump())  # Añadir el usuario con el nuevo ID
    save_users(users)  # Guardar los usuarios actualizados en la base de datos
    return user

@router.get("/{user_id}", response_model=User)
def get_user(user_id: int):
    users = get_users()
    user = next((u for u in users if u["id"] == user_id), None)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.put("/{user_id}", response_model=User)
def update_user(user_id: int, updated_user: User):
    users = get_users()
    for idx, user in enumerate(users):
        if user["id"] == user_id:
            users[idx] = updated_user.model_dump()
            save_users(users)
            return updated_user
    raise HTTPException(status_code=404, detail="User not found")

@router.delete("/{user_id}")
def delete_user(user_id: int):
    users = get_users()
    updated_users = [user for user in users if user["id"] != user_id]
    if len(updated_users) == len(users):
        raise HTTPException(status_code=404, detail="User not found")
    save_users(updated_users)
    return {"message": "User deleted successfully"}

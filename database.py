import json
from pathlib import Path

DB_FILE = Path("db.json")

# Función para cargar datos desde el archivo JSON
def load_data():
    if not DB_FILE.exists():
        DB_FILE.write_text(json.dumps({"users": [], "preferences": []}, indent=4))
    with open(DB_FILE, "r") as file:
        return json.load(file)

# Función para guardar datos en el archivo JSON
def save_data(data):
    with open(DB_FILE, "w") as file:
        json.dump(data, file, indent=3)

# Obtener usuarios y preferencias desde el archivo
def get_users():
    return load_data().get("users", [])

def get_preferences():
    return load_data().get("preferences", [])

# Guardar usuarios y preferencias en el archivo
def save_users(users):
    data = load_data()
    data["users"] = users
    save_data(data)

def save_preferences(preferences):
    data = load_data()
    data["preferences"] = preferences
    save_data(data)

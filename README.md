# 🎵 Music API - Django REST Framework

Una API REST desarrollada con Django y Django REST Framework para gestionar usuarios y sus preferencias musicales, con integración a la API de Spotify.

## 📋 Características

- **Gestión de Usuarios**: CRUD completo para usuarios
- **Preferencias Musicales**: Almacenamiento de artistas y canciones favoritas
- **Integración con Spotify**: Búsqueda de artistas a través de la API de Spotify
- **API RESTful**: Endpoints bien estructurados siguiendo estándares REST
- **Documentación**: API documentada y fácil de usar

## 🛠 Tecnologías Utilizadas

- **Python 3.x**
- **Django 5.1.5**
- **Django REST Framework**
- **SQLite** (base de datos por defecto)
- **Spotipy** (cliente de Spotify API)
- **Requests** (cliente HTTP)

## 🚀 Instalación y Configuración

### Prerrequisitos

- Python 3.8 o superior
- pip (gestor de paquetes de Python)

### Pasos de Instalación

1. **Clonar el repositorio**
   ```bash
   git clone https://github.com/LuisArnaizM/Backend_UEM.git
   cd Backend_UEM
   ```

2. **Crear un entorno virtual**
   ```bash
   python -m venv musicapi_env
   source musicapi_env/bin/activate  # En macOS/Linux
   # musicapi_env\Scripts\activate   # En Windows
   ```

3. **Instalar dependencias**
   ```bash
   pip install django djangorestframework spotipy requests
   ```

4. **Navegar al directorio del proyecto**
   ```bash
   cd musicapi
   ```

5. **Configurar la base de datos**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

6. **Crear superusuario (opcional)**
   ```bash
   python manage.py createsuperuser
   ```

### Configuración de Spotify API

Para utilizar la integración con Spotify, necesitas configurar las credenciales:

1. **Registrarse en Spotify for Developers**
   - Visita [Spotify for Developers](https://developer.spotify.com/)
   - Crea una nueva aplicación
   - Obtén tu `Client ID` y `Client Secret`

2. **Configurar credenciales**
   - En `musicapi/views.py`, reemplaza:
     ```python
     SPOTIFY_CLIENT_ID = 'tu_client_id'
     SPOTIFY_CLIENT_SECRET = 'tu_client_secret'
     ```
   
   - En `spotify_integration/spotify.py`, actualiza:
     ```python
     'Authorization': 'Bearer YOUR_SPOTIFY_ACCESS_TOKEN'
     ```

## 🚀 Ejecutar la Aplicación

```bash
python manage.py runserver
```

La API estará disponible en: `http://127.0.0.1:8000/`

## 📚 Endpoints de la API

### Usuarios

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/users/` | Obtener todos los usuarios |
| POST | `/users/` | Crear un nuevo usuario |
| GET | `/users/{id}/` | Obtener un usuario específico |
| PUT | `/users/{id}/` | Actualizar un usuario |
| DELETE | `/users/{id}/` | Eliminar un usuario |

### Spotify Integration

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/spotify/?artist={nombre}` | Buscar información de un artista |

### Ejemplos de Uso

#### Crear un usuario
```bash
curl -X POST http://127.0.0.1:8000/users/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "john_doe",
    "email": "john@example.com"
  }'
```

#### Buscar un artista en Spotify
```bash
curl -X GET "http://127.0.0.1:8000/spotify/?artist=The Beatles"
```

## 📊 Modelos de Datos

### Usuario
```python
{
  "id": 1,
  "username": "john_doe",
  "email": "john@example.com",
  "date_joined": "2024-01-01T00:00:00Z"
}
```

### Preferencia
```python
{
  "user": 1,
  "favorite_artist": "The Beatles",
  "favorite_song": "Hey Jude"
}
```

### Respuesta de Spotify
```python
{
  "name": "The Beatles",
  "genres": ["rock", "pop"],
  "followers": 15000000,
  "spotify_url": "https://open.spotify.com/artist/..."
}
```

## 🛡 Administración

Puedes acceder al panel de administración de Django en:
`http://127.0.0.1:8000/admin/`

Utiliza las credenciales del superusuario que creaste anteriormente.

## 🔧 Estructura del Proyecto

```
musicapi/
├── manage.py
├── musicapi/
│   ├── __init__.py
│   ├── settings.py          # Configuración de Django
│   ├── urls.py             # URLs principales
│   ├── wsgi.py             # Configuración WSGI
│   ├── asgi.py             # Configuración ASGI
│   ├── models.py           # Modelos de datos
│   ├── views.py            # Vistas de la API
│   ├── serializers.py      # Serializadores DRF
│   ├── permissions.py      # Permisos personalizados
│   ├── migrations/         # Migraciones de base de datos
│   └── spotify_integration/
│       ├── __init__.py
│       ├── spotify.py      # Integración con Spotify API
│       └── serializers.py  # Serializadores específicos
```

## 🚀 Despliegue

### Variables de Entorno Recomendadas

```bash
DEBUG=False
SECRET_KEY=your-secret-key
ALLOWED_HOSTS=your-domain.com
SPOTIFY_CLIENT_ID=your-spotify-client-id
SPOTIFY_CLIENT_SECRET=your-spotify-client-secret
```

### Para Producción

1. **Configurar base de datos de producción** (PostgreSQL recomendado)
2. **Configurar archivos estáticos**
3. **Establecer DEBUG=False**
4. **Configurar ALLOWED_HOSTS**
5. **Usar variables de entorno para credenciales**

## 🤝 Contribución

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para más detalles.

## 👨‍💻 Autor

**Luis Arnaiz**
- GitHub: [@LuisArnaizM](https://github.com/LuisArnaizM)

## 📞 Soporte

Si tienes alguna pregunta o problema, no dudes en abrir un issue en el repositorio.

---

⭐ ¡Si te gusta este proyecto, no olvides darle una estrella!
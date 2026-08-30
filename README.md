# User Notes API

🇪🇸 [Español](#español) | 🇬🇧 [English](#english)

---

## Español

API REST para la gestión de notas de usuario, construida con **FastAPI**, **SQLAlchemy** y **PostgreSQL**. Cada nota pertenece a un usuario autenticado y solo su dueño puede consultarla, modificarla o eliminarla.

### Características

- Registro y login de usuarios con contraseñas hasheadas (**bcrypt**).
- Autenticación mediante **JWT** (OAuth2 Password Flow).
- CRUD completo de notas (crear, listar, obtener, actualizar y eliminar), protegido por usuario propietario.
- Búsqueda de notas por texto en título o contenido.
- Limitación de tasa (*rate limiting*) en el login (5 intentos por minuto por IP) con **slowapi**.
- Validación de datos con **Pydantic**.
- Persistencia con **SQLAlchemy ORM** sobre **PostgreSQL**.
- Migraciones de esquema gestionadas con **Alembic**.
- Fechas de creación/actualización serializadas en la zona horaria `America/Bogota`.
- Suite de pruebas con **pytest** sobre una base de datos SQLite en memoria.
- Endpoint de *health check* (`GET /`).

### Stack técnico

| Herramienta | Uso |
|---|---|
| Python | >= 3.14 |
| FastAPI | Framework web |
| SQLAlchemy | ORM |
| Alembic | Migraciones de base de datos |
| psycopg2 | Driver de PostgreSQL |
| Pydantic | Validación y serialización |
| passlib (bcrypt) | Hashing de contraseñas |
| python-jose | Firma y verificación de JWT |
| python-dotenv | Carga de variables de entorno |
| slowapi | Rate limiting |
| pytest | Pruebas automatizadas |
| uv | Gestión de dependencias y entorno |

### Estructura del proyecto

```
src/user_notes/
├── main.py                     # Punto de entrada de la app FastAPI
├── database.py                 # Configuración de la conexión y sesión de BD
├── core/
│   ├── security.py             # Hashing de contraseñas y manejo de JWT
│   ├── dependencies.py         # Dependencia get_current_user
│   └── limiter.py              # Configuración de rate limiting (slowapi)
├── models/
│   ├── notes.py                # Modelo ORM de Notes
│   └── users.py                # Modelo ORM de Users
├── schemas/
│   ├── notes.py                # Esquemas Pydantic de notas
│   └── users.py                # Esquemas Pydantic de usuarios y token
├── routers/
│   ├── notes.py                # Endpoints de /notes
│   └── users.py                # Endpoints de /users
└── services/
    ├── notes_service.py        # Lógica de acceso a datos de notas
    └── users_service.py        # Lógica de acceso a datos de usuarios

alembic/                        # Migraciones de base de datos
tests/                          # Suite de pruebas (pytest)
```

### Requisitos previos

- Python 3.14 o superior.
- Una base de datos PostgreSQL accesible.
- [uv](https://docs.astral.sh/uv/) instalado.

### Instalación

1. Clona el repositorio e ingresa a la carpeta del proyecto.
2. Instala las dependencias:

   ```bash
   uv sync
   ```

3. Copia el archivo de variables de entorno de ejemplo y complétalo:

   ```bash
   cp .env_example .env
   ```

   ```env
   DATABASE_URL=postgresql://usuario:password@host:puerto/nombre_bd
   SECRET_KEY=una_clave_secreta_larga_y_aleatoria
   ALGORITHM=HS256
   ACCESS_TOKEN_EXPIRE_MINUTES=30
   ```

4. Aplica las migraciones de base de datos:

   ```bash
   uv run alembic upgrade head
   ```

### Ejecución

Con el entorno virtual gestionado por `uv`, levanta el servidor en modo desarrollo:

```bash
uv run fastapi dev src/user_notes/main.py
```

La API quedará disponible en `http://127.0.0.1:8000` y la documentación interactiva (Swagger UI) en `http://127.0.0.1:8000/docs`.

> El esquema de la base de datos se gestiona con Alembic (`uv run alembic upgrade head`); ya no se crea automáticamente al iniciar la aplicación.

### Pruebas

Ejecuta la suite de pruebas con:

```bash
uv run pytest
```

### Autenticación

1. Registra un usuario en `POST /users/register`.
2. Inicia sesión en `POST /users/login` (formulario `x-www-form-urlencoded`: `username` = email, `password`) para obtener un `access_token`.
3. Envía el token en cada solicitud protegida con el encabezado `Authorization: Bearer <access_token>`.

### Endpoints

| Método | Ruta | Auth | Descripción |
|---|---|---|---|
| GET | `/` | No | Health check |
| POST | `/users/register` | No | Registra un nuevo usuario |
| POST | `/users/login` | No | Inicia sesión y devuelve un JWT (limitado a 5 solicitudes/minuto por IP) |
| GET | `/users/me` | Sí | Devuelve el usuario autenticado |
| GET | `/notes/` | Sí | Lista las notas del usuario autenticado |
| POST | `/notes/` | Sí | Crea una nueva nota para el usuario autenticado |
| POST | `/notes/search?q=` | Sí | Busca notas del usuario cuyo título o contenido contenga `q` |
| GET | `/notes/{note_id}` | Sí | Obtiene una nota por id (solo el dueño) |
| PATCH | `/notes/{note_id}` | Sí | Actualiza una nota existente (solo el dueño) |
| DELETE | `/notes/{note_id}` | Sí | Elimina una nota (solo el dueño) |

#### Modelo de usuario

```json
{
  "id": 1,
  "email": "usuario@example.com"
}
```

#### Modelo de nota

```json
{
  "id": 1,
  "title": "Título de la nota",
  "content": "Contenido de la nota",
  "owner_id": 1,
  "created_at": "2026-08-23T09:00:00-05:00",
  "updated_at": "2026-08-23T09:00:00-05:00"
}
```

`title` y `content` son requeridos y no pueden estar vacíos. Intentar acceder a una nota que no pertenece al usuario autenticado devuelve `403 Forbidden`.

---

## English

REST API for managing user notes, built with **FastAPI**, **SQLAlchemy**, and **PostgreSQL**. Each note belongs to an authenticated user, and only its owner can view, update, or delete it.

### Features

- User registration and login with hashed passwords (**bcrypt**).
- **JWT**-based authentication (OAuth2 Password Flow).
- Full CRUD for notes (create, list, retrieve, update, delete), scoped to the owning user.
- Text search over notes by title or content.
- Rate limiting on login (5 attempts per minute per IP) with **slowapi**.
- Data validation with **Pydantic**.
- Persistence via **SQLAlchemy ORM** on top of **PostgreSQL**.
- Schema migrations managed with **Alembic**.
- Created/updated timestamps serialized in the `America/Bogota` timezone.
- Test suite with **pytest** running against an in-memory SQLite database.
- Health check endpoint (`GET /`).

### Tech stack

| Tool | Purpose |
|---|---|
| Python | >= 3.14 |
| FastAPI | Web framework |
| SQLAlchemy | ORM |
| Alembic | Database migrations |
| psycopg2 | PostgreSQL driver |
| Pydantic | Validation and serialization |
| passlib (bcrypt) | Password hashing |
| python-jose | JWT signing and verification |
| python-dotenv | Environment variable loading |
| slowapi | Rate limiting |
| pytest | Automated testing |
| uv | Dependency and environment management |

### Project structure

```
src/user_notes/
├── main.py                     # FastAPI app entry point
├── database.py                 # DB connection/session setup
├── core/
│   ├── security.py             # Password hashing and JWT handling
│   ├── dependencies.py         # get_current_user dependency
│   └── limiter.py              # Rate limiting setup (slowapi)
├── models/
│   ├── notes.py                # Notes ORM model
│   └── users.py                # Users ORM model
├── schemas/
│   ├── notes.py                # Note Pydantic schemas
│   └── users.py                # User and token Pydantic schemas
├── routers/
│   ├── notes.py                # /notes endpoints
│   └── users.py                # /users endpoints
└── services/
    ├── notes_service.py        # Notes data access logic
    └── users_service.py        # Users data access logic

alembic/                        # Database migrations
tests/                          # Test suite (pytest)
```

### Prerequisites

- Python 3.14 or higher.
- An accessible PostgreSQL database.
- [uv](https://docs.astral.sh/uv/) installed.

### Installation

1. Clone the repository and enter the project folder.
2. Install dependencies:

   ```bash
   uv sync
   ```

3. Copy the example environment file and fill it in:

   ```bash
   cp .env_example .env
   ```

   ```env
   DATABASE_URL=postgresql://user:password@host:port/db_name
   SECRET_KEY=a_long_random_secret_key
   ALGORITHM=HS256
   ACCESS_TOKEN_EXPIRE_MINUTES=30
   ```

4. Apply database migrations:

   ```bash
   uv run alembic upgrade head
   ```

### Running the app

With the virtual environment managed by `uv`, start the dev server:

```bash
uv run fastapi dev src/user_notes/main.py
```

The API will be available at `http://127.0.0.1:8000`, with interactive docs (Swagger UI) at `http://127.0.0.1:8000/docs`.

> The database schema is managed with Alembic (`uv run alembic upgrade head`); it is no longer created automatically on startup.

### Tests

Run the test suite with:

```bash
uv run pytest
```

### Authentication

1. Register a user at `POST /users/register`.
2. Log in at `POST /users/login` (`x-www-form-urlencoded` form: `username` = email, `password`) to obtain an `access_token`.
3. Send the token on every protected request via the `Authorization: Bearer <access_token>` header.

### Endpoints

| Method | Path | Auth | Description |
|---|---|---|---|
| GET | `/` | No | Health check |
| POST | `/users/register` | No | Registers a new user |
| POST | `/users/login` | No | Logs in and returns a JWT (rate-limited to 5 requests/minute per IP) |
| GET | `/users/me` | Yes | Returns the authenticated user |
| GET | `/notes/` | Yes | Lists the authenticated user's notes |
| POST | `/notes/` | Yes | Creates a new note for the authenticated user |
| POST | `/notes/search?q=` | Yes | Searches the user's notes whose title or content contains `q` |
| GET | `/notes/{note_id}` | Yes | Retrieves a note by id (owner only) |
| PATCH | `/notes/{note_id}` | Yes | Updates an existing note (owner only) |
| DELETE | `/notes/{note_id}` | Yes | Deletes a note (owner only) |

#### User model

```json
{
  "id": 1,
  "email": "user@example.com"
}
```

#### Note model

```json
{
  "id": 1,
  "title": "Note title",
  "content": "Note content",
  "owner_id": 1,
  "created_at": "2026-08-23T09:00:00-05:00",
  "updated_at": "2026-08-23T09:00:00-05:00"
}
```

`title` and `content` are required and cannot be empty. Attempting to access a note that does not belong to the authenticated user returns `403 Forbidden`.

# User Notes API

🇪🇸 [Español](#español) | 🇬🇧 [English](#english)

---

## Español

API REST para la gestión de notas de usuario, construida con **FastAPI**, **SQLAlchemy** y **PostgreSQL**.

### Características

- CRUD completo de notas (crear, listar, obtener, actualizar y eliminar).
- Validación de datos con **Pydantic**.
- Persistencia con **SQLAlchemy ORM** sobre **PostgreSQL**.
- Fechas de creación/actualización serializadas en la zona horaria `America/Bogota`.
- Endpoint de *health check* (`GET /`).

### Stack técnico

| Herramienta | Uso |
|---|---|
| Python | >= 3.14 |
| FastAPI | Framework web |
| SQLAlchemy | ORM |
| psycopg2 | Driver de PostgreSQL |
| Pydantic | Validación y serialización |
| python-dotenv | Carga de variables de entorno |
| uv | Gestión de dependencias y entorno |

### Estructura del proyecto

```
src/user_notes/
├── main.py                 # Punto de entrada de la app FastAPI
├── database.py              # Configuración de la conexión y sesión de BD
├── models/
│   └── notes.py              # Modelo ORM de Notes
├── schemas/
│   └── notes.py              # Esquemas Pydantic (request/response)
├── routers/
│   └── notes.py              # Endpoints de /notes
└── services/
    └── notes_service.py      # Lógica de acceso a datos
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
   ```

### Ejecución

Con el entorno virtual gestionado por `uv`, levanta el servidor en modo desarrollo:

```bash
uv run fastapi dev src/user_notes/main.py
```

La API quedará disponible en `http://127.0.0.1:8000` y la documentación interactiva (Swagger UI) en `http://127.0.0.1:8000/docs`.

> Las tablas se crean automáticamente al iniciar la aplicación (`Base.metadata.create_all`), no se requiere ejecutar migraciones por separado.

### Endpoints

| Método | Ruta | Descripción |
|---|---|---|
| GET | `/` | Health check |
| GET | `/notes/` | Lista todas las notas |
| POST | `/notes/` | Crea una nueva nota |
| GET | `/notes/{note_id}` | Obtiene una nota por id |
| PATCH | `/notes/{note_id}` | Actualiza una nota existente |
| DELETE | `/notes/{note_id}` | Elimina una nota |

#### Modelo de nota

```json
{
  "id": 1,
  "title": "Título de la nota",
  "content": "Contenido de la nota",
  "created_at": "2026-08-23T09:00:00-05:00",
  "updated_at": "2026-08-23T09:00:00-05:00"
}
```

`title` y `content` son requeridos y no pueden estar vacíos.

---

## English

REST API for managing user notes, built with **FastAPI**, **SQLAlchemy**, and **PostgreSQL**.

### Features

- Full CRUD for notes (create, list, retrieve, update, delete).
- Data validation with **Pydantic**.
- Persistence via **SQLAlchemy ORM** on top of **PostgreSQL**.
- Created/updated timestamps serialized in the `America/Bogota` timezone.
- Health check endpoint (`GET /`).

### Tech stack

| Tool | Purpose |
|---|---|
| Python | >= 3.14 |
| FastAPI | Web framework |
| SQLAlchemy | ORM |
| psycopg2 | PostgreSQL driver |
| Pydantic | Validation and serialization |
| python-dotenv | Environment variable loading |
| uv | Dependency and environment management |

### Project structure

```
src/user_notes/
├── main.py                 # FastAPI app entry point
├── database.py              # DB connection/session setup
├── models/
│   └── notes.py              # Notes ORM model
├── schemas/
│   └── notes.py              # Pydantic schemas (request/response)
├── routers/
│   └── notes.py              # /notes endpoints
└── services/
    └── notes_service.py      # Data access logic
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
   ```

### Running the app

With the virtual environment managed by `uv`, start the dev server:

```bash
uv run fastapi dev src/user_notes/main.py
```

The API will be available at `http://127.0.0.1:8000`, with interactive docs (Swagger UI) at `http://127.0.0.1:8000/docs`.

> Tables are created automatically on startup (`Base.metadata.create_all`) — no separate migration step is required.

### Endpoints

| Method | Path | Description |
|---|---|---|
| GET | `/` | Health check |
| GET | `/notes/` | List all notes |
| POST | `/notes/` | Create a new note |
| GET | `/notes/{note_id}` | Retrieve a note by id |
| PATCH | `/notes/{note_id}` | Update an existing note |
| DELETE | `/notes/{note_id}` | Delete a note |

#### Note model

```json
{
  "id": 1,
  "title": "Note title",
  "content": "Note content",
  "created_at": "2026-08-23T09:00:00-05:00",
  "updated_at": "2026-08-23T09:00:00-05:00"
}
```

`title` and `content` are required and cannot be empty.

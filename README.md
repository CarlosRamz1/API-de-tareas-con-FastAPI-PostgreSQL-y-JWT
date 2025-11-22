# API de Gestión de Tareas

API REST para gestión de tareas con autenticación JWT, desarrollada con FastAPI y PostgreSQL.

## Descripción

Este proyecto es una API backend que permite a los usuarios registrarse, autenticarse y gestionar sus tareas personales. Cada usuario solo puede ver y modificar sus propias tareas.

## Tecnologías

- FastAPI
- PostgreSQL
- SQLAlchemy
- Alembic
- JWT para autenticación
- Pydantic para validación

## Instalación

### Requisitos

- Python 3.12 o superior
- PostgreSQL
- Git

### Pasos

1. Clonar el repositorio
git clone https://github.com/TU_USUARIO/api-tareas.git
cd api-tareas

2. Crear y activar entorno virtual
python -m venv venv
venv\Scripts\activate


3. Instalar dependencias
pip install -r requirements.txt


4. Configurar PostgreSQL

Crear la base de datos y el usuario:
CREATE DATABASE tareas_db;
CREATE USER tareas_user WITH PASSWORD 'tu_contraseña';
GRANT ALL PRIVILEGES ON DATABASE tareas_db TO tareas_user;
ALTER DATABASE tareas_db OWNER TO tareas_user;
GRANT ALL ON SCHEMA public TO tareas_user;


5. Configurar archivo .env

Crear archivo .env en la raíz del proyecto:
PROJECT_NAME=API de Tareas
DATABASE_URL=postgresql://tareas_user:tu_contraseña@localhost:5432/tareas_db
SECRET_KEY=tu_clave_secreta
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
ENVIRONMENT=development

Generar SECRET_KEY:
python -c "import secrets; print(secrets.token_urlsafe(32))"


6. Ejecutar migraciones
alembic upgrade head


7. Iniciar servidor
python run.py


La API estará disponible en http://localhost:8000

## Documentación

Accede a la documentación interactiva:

- Swagger: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Endpoints Principales

### Autenticación

- POST /api/auth/register - Registrar nuevo usuario
- POST /api/auth/login - Iniciar sesión

### Tareas

- GET /api/tasks/ - Obtener todas las tareas del usuario
- POST /api/tasks/ - Crear nueva tarea
- GET /api/tasks/{id} - Obtener tarea específica
- PUT /api/tasks/{id} - Actualizar tarea
- DELETE /api/tasks/{id} - Eliminar tarea

Todos los endpoints de tareas requieren autenticación mediante token JWT.

## Estructura del Proyecto

api-tareas/
├── app/
│ ├── api/endpoints/ # Rutas de la API
│ ├── core/ # Configuración y seguridad
│ ├── crud/ # Operaciones de base de datos
│ ├── db/ # Conexión a base de datos
│ ├── models/ # Modelos de datos
│ ├── schemas/ # Validación de datos
│ └── main.py # Aplicación principal
├── alembic/ # Migraciones
├── .env # Variables de entorno
└── requirements.txt # Dependencias
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.api.endpoints.auth import router as auth_router
from app.api.endpoints.task import router as tasks_router


# Crear la aplicación FastAPI
app = FastAPI(
    title=settings.PROJECT_NAME,
    description="API para gestión de tareas con autenticación JWT",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configurar CORS (Cross-Origin Resource Sharing)
# Permite que el frontend en otros dominios pueda consumir la API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción, especifica dominios específicos
    allow_credentials=True,
    allow_methods=["*"],  # Permite todos los métodos HTTP
    allow_headers=["*"],  # Permite todos los headers
)

# Incluir routers de la API
app.include_router(
    auth_router,
    prefix="/api/auth",
    tags=["Autenticación"]
)

app.include_router(
    tasks_router,
    prefix="/api/tasks",
    tags=["Tareas"]
)



# Ruta raíz de bienvenida
@app.get("/", tags=["Root"])
def root():
    """
    Endpoint raíz de la API.
    Retorna información básica de bienvenida.
    """
    return {
        "message": "Bienvenido a la API de Gestión de Tareas",
        "version": "1.0.0",
        "docs": "/docs",
        "redoc": "/redoc"
    }


# Endpoint de salud para verificar que la API está funcionando
@app.get("/health", tags=["Health"])
def health_check():
    """
    Endpoint de salud para monitoreo.
    """
    return {
        "status": "ok",
        "environment": settings.ENVIRONMENT
    }

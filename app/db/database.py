from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from app.core.config import settings

# Crear el motor de la base de datos
# echo=True muestra las consultas SQL en la consola (útil para aprendizaje)
engine = create_engine(
    settings.DATABASE_URL,
    echo=True,
    pool_pre_ping=True
)

# Crear el fabricante de sesiones
# Una sesión es lo que usaremos para hacer operaciones en la base de datos
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# Crear la clase base para los modelos
# Todos los modelos heredarán de esta clase
Base = declarative_base()


# Función de dependencia para obtener una sesión de base de datos
def get_db():
    """
    Crea una sesión de base de datos y la cierra automáticamente al terminar.
    Se usa como dependencia en los endpoints de FastAPI.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

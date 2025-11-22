from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field


class TaskBase(BaseModel):
    """
    Propiedades comunes de tarea.
    """
    title: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = None
    is_completed: bool = False


class TaskCreate(TaskBase):
    """
    Propiedades para crear una tarea.
    """
    pass


class TaskUpdate(BaseModel):
    """
    Propiedades para actualizar una tarea.
    Todos los campos son opcionales.
    """
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = None
    is_completed: Optional[bool] = None


class TaskInDB(TaskBase):
    """
    Propiedades almacenadas en la base de datos.
    """
    id: int
    owner_id: int
    created_at: datetime
    updated_at: Optional[datetime]
    
    class Config:
        from_attributes = True


class Task(TaskInDB):
    """
    Propiedades para devolver al cliente.
    """
    pass

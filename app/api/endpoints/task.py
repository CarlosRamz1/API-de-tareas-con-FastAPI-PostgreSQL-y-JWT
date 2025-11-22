from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.schemas.task import Task, TaskCreate, TaskUpdate
from app.crud import task as crud_task
from app.api.dependencies.auth import get_current_active_user
from app.models.user import User

router = APIRouter()


@router.get("/", response_model=List[Task])
def get_my_tasks(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Obtener todas las tareas del usuario autenticado.
    
    - **skip**: Cantidad de registros a saltar (para paginación)
    - **limit**: Cantidad máxima de registros a devolver (máximo 100)
    """
    tasks = crud_task.get_tasks_by_owner(
        db=db,
        owner_id=current_user.id,
        skip=skip,
        limit=limit
    )
    return tasks


@router.post("/", response_model=Task, status_code=status.HTTP_201_CREATED)
def create_task(
    task_in: TaskCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Crear una nueva tarea para el usuario autenticado.
    
    - **title**: Título de la tarea (obligatorio)
    - **description**: Descripción detallada (opcional)
    - **is_completed**: Estado inicial (por defecto False)
    """
    task = crud_task.create_task(db=db, task=task_in, owner_id=current_user.id)
    return task


@router.get("/{task_id}", response_model=Task)
def get_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Obtener una tarea específica por su ID.
    
    Solo se puede acceder a tareas propias del usuario.
    """
    task = crud_task.get_task(db=db, task_id=task_id)
    
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tarea no encontrada"
        )
    
    # Verificar que la tarea pertenece al usuario actual
    if task.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permiso para acceder a esta tarea"
        )
    
    return task


@router.put("/{task_id}", response_model=Task)
def update_task(
    task_id: int,
    task_in: TaskUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Actualizar una tarea existente.
    
    Solo se pueden actualizar tareas propias del usuario.
    Todos los campos son opcionales.
    """
    # Verificar que la tarea existe y pertenece al usuario
    task = crud_task.get_task(db=db, task_id=task_id)
    
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tarea no encontrada"
        )
    
    if task.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permiso para modificar esta tarea"
        )
    
    # Actualizar la tarea
    task = crud_task.update_task(db=db, task_id=task_id, task=task_in)
    return task


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Eliminar una tarea.
    
    Solo se pueden eliminar tareas propias del usuario.
    """
    # Verificar que la tarea existe y pertenece al usuario
    task = crud_task.get_task(db=db, task_id=task_id)
    
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tarea no encontrada"
        )
    
    if task.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permiso para eliminar esta tarea"
        )
    
    # Eliminar la tarea
    crud_task.delete_task(db=db, task_id=task_id)
    return None

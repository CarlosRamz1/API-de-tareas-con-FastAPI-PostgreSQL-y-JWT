from typing import Optional
from sqlalchemy.orm import Session

from app.models.task import Task
from app.schemas.task import TaskCreate, TaskUpdate


def get_task(db: Session, task_id: int) -> Optional[Task]:
    """
    Obtiene una tarea por su ID.
    """
    return db.query(Task).filter(Task.id == task_id).first()


def get_tasks(db: Session, skip: int = 0, limit: int = 100) -> list[Task]:
    """
    Obtiene todas las tareas con paginación.
    """
    return db.query(Task).offset(skip).limit(limit).all()


def get_tasks_by_owner(
    db: Session, 
    owner_id: int, 
    skip: int = 0, 
    limit: int = 100
) -> list[Task]:
    """
    Obtiene todas las tareas de un usuario específico.
    """
    return db.query(Task).filter(
        Task.owner_id == owner_id
    ).offset(skip).limit(limit).all()


def create_task(db: Session, task: TaskCreate, owner_id: int) -> Task:
    """
    Crea una nueva tarea asociada a un usuario.
    """
    db_task = Task(
        **task.model_dump(),
        owner_id=owner_id
    )
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task


def update_task(db: Session, task_id: int, task: TaskUpdate) -> Optional[Task]:
    """
    Actualiza una tarea existente.
    Solo actualiza los campos que no son None.
    """
    db_task = get_task(db, task_id)
    if not db_task:
        return None
    
    update_data = task.model_dump(exclude_unset=True)
    
    for field, value in update_data.items():
        setattr(db_task, field, value)
    
    db.commit()
    db.refresh(db_task)
    return db_task


def delete_task(db: Session, task_id: int) -> bool:
    """
    Elimina una tarea de la base de datos.
    Retorna True si se eliminó, False si no existía.
    """
    db_task = get_task(db, task_id)
    if not db_task:
        return False
    
    db.delete(db_task)
    db.commit()
    return True

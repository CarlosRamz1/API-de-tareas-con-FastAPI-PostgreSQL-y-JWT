from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db.database import Base


class Task(Base):
    """
    Modelo de Tarea.
    Representa la tabla 'tasks' en la base de datos.
    """
    __tablename__ = "tasks"
    
    # Columnas de la tabla
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    is_completed = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Llave foránea que conecta con el usuario
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Relación con usuario
    owner = relationship("User", back_populates="tasks")

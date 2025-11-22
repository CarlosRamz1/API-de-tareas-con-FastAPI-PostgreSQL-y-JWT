from typing import Optional
from datetime import datetime
from pydantic import BaseModel, EmailStr, Field


class UserBase(BaseModel):
    """
    Propiedades comunes de usuario.
    """
    email: EmailStr
    username: str = Field(..., min_length=3, max_length=50)


class UserCreate(UserBase):
    """
    Propiedades para crear un usuario.
    Incluye la contraseña en texto plano que luego se encriptará.
    """
    password: str = Field(..., min_length=8)


class UserUpdate(BaseModel):
    """
    Propiedades para actualizar un usuario.
    Todos los campos son opcionales.
    """
    email: Optional[EmailStr] = None
    username: Optional[str] = Field(None, min_length=3, max_length=50)
    password: Optional[str] = Field(None, min_length=8)


class UserInDB(UserBase):
    """
    Propiedades almacenadas en la base de datos.
    """
    id: int
    is_active: bool
    is_superuser: bool
    created_at: datetime
    updated_at: Optional[datetime]
    
    class Config:
        from_attributes = True


class User(UserInDB):
    """
    Propiedades para devolver al cliente.
    Hereda todo de UserInDB.
    """
    pass


class Token(BaseModel):
    """
    Esquema para el token de acceso.
    """
    access_token: str
    token_type: str


class TokenData(BaseModel):
    """
    Datos contenidos en el token JWT.
    """
    user_id: Optional[int] = None

from typing import Optional
from pydantic import BaseModel


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

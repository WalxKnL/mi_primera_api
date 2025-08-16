from pydantic import BaseModel, validator
from typing import Optional
from datetime import datetime
import re

class UserBase(BaseModel):
    nombre: str
    email: str
    edad: int
    cedula: str

    @validator('cedula')
    def validate_cedula(cls, v):
        if not re.match(r'^\d{7,10}$', v):
            raise ValueError('La cédula debe tener entre 7 y 10 dígitos')
        return v
    
    @validator('edad')
    def validate_edad(cls, v):
        if v < 0 or v > 120:
            raise ValueError('La edad debe estar entre 0 y 120 años')
        return v

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    id: int
    fecha_creacion: datetime
    activo: bool = True
    
    class Config:
        from_attributes = True

class UserUpdate(BaseModel):
    nombre: Optional[str] = None
    email: Optional[str] = None
    edad: Optional[int] = None
    cedula: Optional[str] = None
    activo: Optional[bool] = None

    @validator('cedula')
    def validate_cedula(cls, v):
        if v is not None and not re.match(r'^\d{7,10}$', v):
            raise ValueError('La cédula debe tener entre 7 y 10 dígitos')
        return 
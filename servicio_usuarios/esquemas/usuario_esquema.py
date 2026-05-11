from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime

class CrearUsuarioRequest(BaseModel):
    email: EmailStr
    nombre: str = Field(..., min_length=3, max_length=100)
    apellido: Optional[str] = Field(None, max_length=100)
    telefono: Optional[str] = None
    cedula: Optional[str] = None
    fecha_nacimiento: Optional[str] = None
    direccion: Optional[str] = None
    ciudad: Optional[str] = None
    genero: Optional[str] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "email": "juan@clinica.com",
                "nombre": "Juan",
                "apellido": "Pérez",
                "telefono": "3001234567",
                "cedula": "1234567890",
                "fecha_nacimiento": "1990-05-15"
            }
        }

class ActualizarUsuarioRequest(BaseModel):
    nombre: Optional[str] = None
    apellido: Optional[str] = None
    telefono: Optional[str] = None
    direccion: Optional[str] = None
    ciudad: Optional[str] = None
    genero: Optional[str] = None
    biografia: Optional[str] = None
    numero_emergencia: Optional[str] = None

class UsuarioResponse(BaseModel):
    id: str
    email: str
    nombre: str
    apellido: Optional[str]
    telefono: Optional[str]
    cedula: Optional[str]
    fecha_nacimiento: Optional[str]
    direccion: Optional[str]
    ciudad: Optional[str]
    genero: Optional[str]
    rol: str
    activo: bool
    verificado: bool
    fecha_creacion: datetime
    
    class Config:
        from_attributes = True

class ListaUsuariosResponse(BaseModel):
    usuarios: list
    total: int
    limite: int
    desplazamiento: int

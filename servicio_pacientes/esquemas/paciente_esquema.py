from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime

class CrearPacienteRequest(BaseModel):
    numero_identidad: str = Field(..., min_length=8, max_length=12)
    nombre: str = Field(..., min_length=3, max_length=100)
    apellido: Optional[str] = None
    email: EmailStr
    telefono: Optional[str] = None
    fecha_nacimiento: Optional[str] = None
    genero: Optional[str] = None
    direccion: Optional[str] = None
    ciudad: Optional[str] = None
    tipo_sangre: Optional[str] = None
    alergias: Optional[str] = None
    condiciones_preexistentes: Optional[str] = None
    medicamentos_actuales: Optional[str] = None
    contacto_emergencia_nombre: Optional[str] = None
    contacto_emergencia_telefono: Optional[str] = None
    contacto_emergencia_relacion: Optional[str] = None

class ActualizarPacienteRequest(BaseModel):
    nombre: Optional[str] = None
    apellido: Optional[str] = None
    telefono: Optional[str] = None
    direccion: Optional[str] = None
    ciudad: Optional[str] = None
    alergias: Optional[str] = None
    condiciones_preexistentes: Optional[str] = None
    medicamentos_actuales: Optional[str] = None
    contacto_emergencia_nombre: Optional[str] = None
    contacto_emergencia_telefono: Optional[str] = None
    contacto_emergencia_relacion: Optional[str] = None

class PacienteResponse(BaseModel):
    id: str
    numero_identidad: str
    nombre: str
    apellido: Optional[str]
    email: str
    telefono: Optional[str]
    fecha_nacimiento: Optional[str]
    genero: Optional[str]
    tipo_sangre: Optional[str]
    alergias: Optional[str]
    condiciones_preexistentes: Optional[str]
    contacto_emergencia_nombre: Optional[str]
    activo: bool
    fecha_creacion: datetime
    
    class Config:
        from_attributes = True

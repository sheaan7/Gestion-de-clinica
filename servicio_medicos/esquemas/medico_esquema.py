from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime

class CrearMedicoRequest(BaseModel):
    email: EmailStr
    nombre: str = Field(..., min_length=3, max_length=100)
    apellido: Optional[str] = None
    telefono: Optional[str] = None
    especialidad: str
    licencia_medica: str = Field(..., min_length=5, max_length=50)
    experiencia_años: Optional[int] = 0
    biografia: Optional[str] = None
    horario_inicio: Optional[str] = None
    horario_fin: Optional[str] = None
    dias_laborales: Optional[str] = None
    foto_perfil: Optional[str] = None

class ActualizarMedicoRequest(BaseModel):
    nombre: Optional[str] = None
    apellido: Optional[str] = None
    telefono: Optional[str] = None
    especialidad: Optional[str] = None
    experiencia_años: Optional[int] = None
    biografia: Optional[str] = None
    horario_inicio: Optional[str] = None
    horario_fin: Optional[str] = None
    dias_laborales: Optional[str] = None
    disponible: Optional[bool] = None
    activo: Optional[bool] = None
    foto_perfil: Optional[str] = None

class MedicoResponse(BaseModel):
    id: str
    email: str
    nombre: str
    apellido: Optional[str]
    telefono: Optional[str]
    especialidad: str
    licencia_medica: str
    experiencia_años: int
    biografia: Optional[str]
    horario_inicio: Optional[str]
    horario_fin: Optional[str]
    dias_laborales: Optional[str]
    disponible: bool
    activo: bool
    foto_perfil: Optional[str]
    fecha_creacion: datetime
    
    class Config:
        from_attributes = True

from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class CrearCitaRequest(BaseModel):
    paciente_id: str = Field(..., min_length=1)
    medico_id: str = Field(..., min_length=1)
    fecha_cita: str = Field(..., pattern=r"^\d{4}-\d{2}-\d{2}$")
    hora_inicio: str = Field(..., pattern=r"^\d{2}:\d{2}$")
    hora_fin: str = Field(..., pattern=r"^\d{2}:\d{2}$")
    motivo: str = Field(..., min_length=3, max_length=255)
    notas: Optional[str] = None

class ActualizarCitaRequest(BaseModel):
    fecha_cita: Optional[str] = Field(None, pattern=r"^\d{4}-\d{2}-\d{2}$")
    hora_inicio: Optional[str] = Field(None, pattern=r"^\d{2}:\d{2}$")
    hora_fin: Optional[str] = Field(None, pattern=r"^\d{2}:\d{2}$")
    motivo: Optional[str] = Field(None, min_length=3, max_length=255)
    estado: Optional[str] = Field(None)
    notas: Optional[str] = None

class CancelarCitaRequest(BaseModel):
    razon_cancelacion: str = Field(..., min_length=5)

class CitaResponse(BaseModel):
    id: str
    paciente_id: str
    medico_id: str
    fecha_cita: str
    hora_inicio: str
    hora_fin: str
    motivo: str
    estado: str
    notas: Optional[str]
    cancelada_por: Optional[str]
    razon_cancelacion: Optional[str]
    fecha_creacion: datetime
    fecha_actualizacion: datetime
    
    class Config:
        from_attributes = True

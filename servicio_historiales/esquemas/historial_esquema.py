from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class CrearHistorialRequest(BaseModel):
    paciente_id: str = Field(..., min_length=1)
    medico_id: str = Field(..., min_length=1)
    cita_id: Optional[str] = None
    diagnostico: str = Field(..., min_length=1)
    tratamiento: str = Field(..., min_length=1)
    medicamentos_prescritos: Optional[str] = None
    observaciones: Optional[str] = None
    estado_paciente: str = Field(default="estable", pattern="^(crítico|grave|estable|mejoría)$")
    proxima_cita_recomendada: Optional[str] = None
    resultados_laboratorio: Optional[str] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "paciente_id": "uuid-paciente",
                "medico_id": "uuid-medico",
                "cita_id": "uuid-cita",
                "diagnostico": "Hipertensión arterial",
                "tratamiento": "Cambio en dieta y medicación",
                "medicamentos_prescritos": "Enalapril 10mg",
                "observaciones": "Paciente con buen cumplimiento terapéutico",
                "estado_paciente": "estable",
                "proxima_cita_recomendada": "15 días",
                "resultados_laboratorio": "Presión arterial: 140/90"
            }
        }

class ActualizarHistorialRequest(BaseModel):
    diagnostico: Optional[str] = None
    tratamiento: Optional[str] = None
    medicamentos_prescritos: Optional[str] = None
    observaciones: Optional[str] = None
    estado_paciente: Optional[str] = None
    proxima_cita_recomendada: Optional[str] = None
    resultados_laboratorio: Optional[str] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "estado_paciente": "mejoría",
                "observaciones": "Paciente muestra mejoría significativa"
            }
        }

class HistorialResponse(BaseModel):
    id: str
    paciente_id: str
    medico_id: str
    cita_id: Optional[str]
    fecha_registro: datetime
    diagnostico: str
    tratamiento: str
    medicamentos_prescritos: Optional[str]
    observaciones: Optional[str]
    estado_paciente: str
    proxima_cita_recomendada: Optional[str]
    resultados_laboratorio: Optional[str]
    fecha_creacion: datetime
    fecha_actualizacion: datetime
    
    class Config:
        from_attributes = True

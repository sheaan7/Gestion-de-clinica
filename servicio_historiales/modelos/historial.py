from sqlalchemy import Column, String, DateTime, Text, func, Index
from sqlalchemy.dialects.mysql import CHAR
from servicio_historiales.base_datos.conexion import Base
from uuid import uuid4

class Historial(Base):
    __tablename__ = "historiales"
    
    id = Column(CHAR(36), primary_key=True, default=lambda: str(uuid4()))
    paciente_id = Column(String(36), nullable=False, index=True)
    medico_id = Column(String(36), nullable=False, index=True)
    cita_id = Column(String(36), nullable=True)
    fecha_registro = Column(DateTime, default=func.now())
    diagnostico = Column(Text, nullable=False)
    tratamiento = Column(Text, nullable=False)
    medicamentos_prescritos = Column(Text, nullable=True)
    observaciones = Column(Text, nullable=True)
    estado_paciente = Column(String(50), nullable=False, default="estable")
    proxima_cita_recomendada = Column(String(255), nullable=True)
    resultados_laboratorio = Column(Text, nullable=True)
    fecha_creacion = Column(DateTime, default=func.now())
    fecha_actualizacion = Column(DateTime, default=func.now(), onupdate=func.now())
    
    __table_args__ = (
        Index('idx_paciente_fecha', 'paciente_id', 'fecha_registro'),
        Index('idx_medico_fecha', 'medico_id', 'fecha_registro'),
    )
    
    def __repr__(self):
        return f"<Historial(id={self.id}, paciente_id={self.paciente_id}, medico_id={self.medico_id})>"

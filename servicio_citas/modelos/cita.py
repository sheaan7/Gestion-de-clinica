from sqlalchemy import Column, String, DateTime, func
from sqlalchemy.dialects.mysql import CHAR, TEXT
from servicio_citas.base_datos.conexion import Base
from uuid import uuid4

class Cita(Base):
    __tablename__ = "citas"
    
    id = Column(CHAR(36), primary_key=True, default=lambda: str(uuid4()))
    paciente_id = Column(String(36), nullable=False, index=True)
    medico_id = Column(String(36), nullable=False, index=True)
    fecha_cita = Column(String(10), nullable=False, index=True)
    hora_inicio = Column(String(5), nullable=False)
    hora_fin = Column(String(5), nullable=False)
    motivo = Column(String(255), nullable=False)
    estado = Column(String(50), default="pendiente", nullable=False, index=True)
    notas = Column(TEXT, nullable=True)
    cancelada_por = Column(String(36), nullable=True)
    razon_cancelacion = Column(TEXT, nullable=True)
    fecha_creacion = Column(DateTime, default=func.now())
    fecha_actualizacion = Column(DateTime, default=func.now(), onupdate=func.now())
    
    def __repr__(self):
        return f"<Cita(id={self.id}, paciente_id={self.paciente_id}, medico_id={self.medico_id}, fecha={self.fecha_cita})>"

from sqlalchemy import Column, String, DateTime, Boolean, Integer, func
from sqlalchemy.dialects.mysql import CHAR, TEXT
from servicio_medicos.base_datos.conexion import Base
from uuid import uuid4

class Medico(Base):
    __tablename__ = "medicos"
    
    id = Column(CHAR(36), primary_key=True, default=lambda: str(uuid4()))
    email = Column(String(255), unique=True, nullable=False, index=True)
    nombre = Column(String(255), nullable=False)
    apellido = Column(String(255), nullable=True)
    telefono = Column(String(20), nullable=True)
    especialidad = Column(String(100), nullable=False, index=True)
    licencia_medica = Column(String(50), unique=True, nullable=False, index=True)
    experiencia_años = Column(Integer, nullable=True, default=0)
    biografia = Column(TEXT, nullable=True)
    horario_inicio = Column(String(5), nullable=True)
    horario_fin = Column(String(5), nullable=True)
    dias_laborales = Column(String(255), nullable=True)
    disponible = Column(Boolean, default=True)
    activo = Column(Boolean, default=True)
    foto_perfil = Column(String(255), nullable=True)
    fecha_creacion = Column(DateTime, default=func.now())
    fecha_actualizacion = Column(DateTime, default=func.now(), onupdate=func.now())
    
    def __repr__(self):
        return f"<Medico(id={self.id}, nombre={self.nombre}, especialidad={self.especialidad})>"

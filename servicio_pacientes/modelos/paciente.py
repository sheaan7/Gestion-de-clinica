from sqlalchemy import Column, String, DateTime, Boolean, func
from sqlalchemy.dialects.mysql import CHAR, TEXT
from servicio_pacientes.base_datos.conexion import Base
from uuid import uuid4

class Paciente(Base):
    __tablename__ = "pacientes"
    
    id = Column(CHAR(36), primary_key=True, default=lambda: str(uuid4()))
    numero_identidad = Column(String(12), unique=True, nullable=False, index=True)
    nombre = Column(String(255), nullable=False)
    apellido = Column(String(255), nullable=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    telefono = Column(String(20), nullable=True)
    fecha_nacimiento = Column(String(10), nullable=True)
    genero = Column(String(20), nullable=True)
    direccion = Column(String(255), nullable=True)
    ciudad = Column(String(100), nullable=True)
    tipo_sangre = Column(String(5), nullable=True)
    alergias = Column(TEXT, nullable=True)
    condiciones_preexistentes = Column(TEXT, nullable=True)
    medicamentos_actuales = Column(TEXT, nullable=True)
    contacto_emergencia_nombre = Column(String(255), nullable=True)
    contacto_emergencia_telefono = Column(String(20), nullable=True)
    contacto_emergencia_relacion = Column(String(100), nullable=True)
    activo = Column(Boolean, default=True)
    fecha_creacion = Column(DateTime, default=func.now())
    fecha_actualizacion = Column(DateTime, default=func.now(), onupdate=func.now())
    
    def __repr__(self):
        return f"<Paciente(id={self.id}, nombre={self.nombre})>"

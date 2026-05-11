from sqlalchemy import Column, String, DateTime, Boolean, func
from sqlalchemy.dialects.mysql import CHAR
from servicio_autenticacion.base_datos.conexion import Base
from uuid import uuid4

class Usuario(Base):
    __tablename__ = "usuarios"
    
    id = Column(CHAR(36), primary_key=True, default=lambda: str(uuid4()))
    email = Column(String(255), unique=True, nullable=False, index=True)
    nombre = Column(String(255), nullable=False)
    contraseña_hash = Column(String(255), nullable=False)
    rol = Column(String(50), nullable=False, default="usuario")
    activo = Column(Boolean, default=True)
    verificado = Column(Boolean, default=False)
    fecha_creacion = Column(DateTime, default=func.now())
    fecha_actualizacion = Column(DateTime, default=func.now(), onupdate=func.now())
    fecha_ultimo_acceso = Column(DateTime, nullable=True)
    
    def __repr__(self):
        return f"<Usuario(id={self.id}, email={self.email}, rol={self.rol})>"

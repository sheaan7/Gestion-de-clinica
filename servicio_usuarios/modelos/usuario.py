from sqlalchemy import Column, String, DateTime, Boolean, func
from sqlalchemy.dialects.mysql import CHAR, TEXT
from servicio_usuarios.base_datos.conexion import Base
from uuid import uuid4

class Usuario(Base):
    __tablename__ = "usuarios"
    
    id = Column(CHAR(36), primary_key=True, default=lambda: str(uuid4()))
    email = Column(String(255), unique=True, nullable=False, index=True)
    nombre = Column(String(255), nullable=False)
    apellido = Column(String(255), nullable=True)
    telefono = Column(String(20), nullable=True)
    cedula = Column(String(12), unique=True, nullable=True, index=True)
    fecha_nacimiento = Column(String(10), nullable=True)
    direccion = Column(String(255), nullable=True)
    ciudad = Column(String(100), nullable=True)
    genero = Column(String(20), nullable=True)
    foto_perfil = Column(String(255), nullable=True)
    rol = Column(String(50), nullable=False, default="usuario")
    activo = Column(Boolean, default=True)
    verificado = Column(Boolean, default=False)
    biografia = Column(TEXT, nullable=True)
    numero_emergencia = Column(String(20), nullable=True)
    fecha_creacion = Column(DateTime, default=func.now())
    fecha_actualizacion = Column(DateTime, default=func.now(), onupdate=func.now())
    
    def __repr__(self):
        return f"<Usuario(id={self.id}, nombre={self.nombre}, email={self.email})>"

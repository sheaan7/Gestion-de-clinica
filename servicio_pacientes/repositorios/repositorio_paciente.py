from sqlalchemy.orm import Session
from servicio_pacientes.modelos.paciente import Paciente
from servicio_pacientes.utilidades.excepciones import RecursoNoEncontrado
from typing import Optional

class RepositorioPaciente:
    def __init__(self, sesion: Session):
        self.sesion = sesion
    
    def crear(self, paciente: Paciente) -> Paciente:
        self.sesion.add(paciente)
        self.sesion.commit()
        self.sesion.refresh(paciente)
        return paciente
    
    def obtener_por_id(self, paciente_id: str) -> Paciente:
        paciente = self.sesion.query(Paciente).filter(Paciente.id == paciente_id).first()
        if not paciente:
            raise RecursoNoEncontrado("Paciente")
        return paciente
    
    def obtener_por_numero_identidad(self, numero_identidad: str) -> Optional[Paciente]:
        return self.sesion.query(Paciente).filter(Paciente.numero_identidad == numero_identidad).first()
    
    def obtener_por_email(self, email: str) -> Optional[Paciente]:
        return self.sesion.query(Paciente).filter(Paciente.email == email).first()
    
    def obtener_todos(self, limite: int = 100, desplazamiento: int = 0) -> list:
        return self.sesion.query(Paciente).limit(limite).offset(desplazamiento).all()
    
    def contar_total(self) -> int:
        return self.sesion.query(Paciente).count()
    
    def buscar_por_nombre(self, nombre: str, limite: int = 100) -> list:
        patron = f"%{nombre}%"
        return self.sesion.query(Paciente).filter(Paciente.nombre.ilike(patron)).limit(limite).all()
    
    def actualizar(self, paciente_id: str, datos: dict) -> Paciente:
        paciente = self.obtener_por_id(paciente_id)
        for clave, valor in datos.items():
            if hasattr(paciente, clave) and valor is not None:
                setattr(paciente, clave, valor)
        self.sesion.commit()
        self.sesion.refresh(paciente)
        return paciente
    
    def eliminar(self, paciente_id: str) -> bool:
        paciente = self.obtener_por_id(paciente_id)
        self.sesion.delete(paciente)
        self.sesion.commit()
        return True
    
    def existe_numero_identidad(self, numero_identidad: str) -> bool:
        return self.sesion.query(Paciente).filter(Paciente.numero_identidad == numero_identidad).first() is not None
    
    def existe_email(self, email: str) -> bool:
        return self.sesion.query(Paciente).filter(Paciente.email == email).first() is not None

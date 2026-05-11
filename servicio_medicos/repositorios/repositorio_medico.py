from sqlalchemy.orm import Session
from servicio_medicos.modelos.medico import Medico
from servicio_medicos.utilidades.excepciones import RecursoNoEncontrado
from typing import Optional

class RepositorioMedico:
    def __init__(self, sesion: Session):
        self.sesion = sesion
    
    def crear(self, medico: Medico) -> Medico:
        self.sesion.add(medico)
        self.sesion.commit()
        self.sesion.refresh(medico)
        return medico
    
    def obtener_por_id(self, medico_id: str) -> Medico:
        medico = self.sesion.query(Medico).filter(Medico.id == medico_id).first()
        if not medico:
            raise RecursoNoEncontrado("Médico")
        return medico
    
    def obtener_por_email(self, email: str) -> Optional[Medico]:
        return self.sesion.query(Medico).filter(Medico.email == email).first()
    
    def obtener_por_licencia(self, licencia: str) -> Optional[Medico]:
        return self.sesion.query(Medico).filter(Medico.licencia_medica == licencia).first()
    
    def obtener_por_especialidad(self, especialidad: str, limite: int = 100) -> list:
        return self.sesion.query(Medico).filter(Medico.especialidad == especialidad).limit(limite).all()
    
    def obtener_disponibles(self, especialidad: Optional[str] = None, limite: int = 100) -> list:
        query = self.sesion.query(Medico).filter(Medico.disponible == True, Medico.activo == True)
        if especialidad:
            query = query.filter(Medico.especialidad == especialidad)
        return query.limit(limite).all()
    
    def obtener_todos(self, limite: int = 100, desplazamiento: int = 0) -> list:
        return self.sesion.query(Medico).limit(limite).offset(desplazamiento).all()
    
    def contar_total(self) -> int:
        return self.sesion.query(Medico).count()
    
    def actualizar(self, medico_id: str, datos: dict) -> Medico:
        medico = self.obtener_por_id(medico_id)
        for clave, valor in datos.items():
            if hasattr(medico, clave) and valor is not None:
                setattr(medico, clave, valor)
        self.sesion.commit()
        self.sesion.refresh(medico)
        return medico
    
    def eliminar(self, medico_id: str) -> bool:
        medico = self.obtener_por_id(medico_id)
        self.sesion.delete(medico)
        self.sesion.commit()
        return True
    
    def existe_email(self, email: str) -> bool:
        return self.sesion.query(Medico).filter(Medico.email == email).first() is not None
    
    def existe_licencia(self, licencia: str) -> bool:
        return self.sesion.query(Medico).filter(Medico.licencia_medica == licencia).first() is not None

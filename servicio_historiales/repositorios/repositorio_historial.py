from sqlalchemy.orm import Session
from servicio_historiales.modelos.historial import Historial
from servicio_historiales.utilidades.excepciones import RecursoNoEncontrado
from typing import Optional
from datetime import datetime

class RepositorioHistorial:
    def __init__(self, sesion: Session):
        self.sesion = sesion
    
    def crear(self, historial_nueva_instancia: Historial) -> Historial:
        self.sesion.add(historial_nueva_instancia)
        self.sesion.commit()
        self.sesion.refresh(historial_nueva_instancia)
        return historial_nueva_instancia
    
    def obtener_por_id(self, historial_id: str) -> Historial:
        historial = self.sesion.query(Historial).filter(Historial.id == historial_id).first()
        if not historial:
            raise RecursoNoEncontrado("Historial")
        return historial
    
    def obtener_por_paciente(self, paciente_id: str, limite: int = 100) -> list:
        return self.sesion.query(Historial).filter(
            Historial.paciente_id == paciente_id
        ).order_by(Historial.fecha_registro.desc()).limit(limite).all()
    
    def obtener_por_medico(self, medico_id: str, limite: int = 100) -> list:
        return self.sesion.query(Historial).filter(
            Historial.medico_id == medico_id
        ).order_by(Historial.fecha_registro.desc()).limit(limite).all()
    
    def obtener_por_fecha_rango(self, fecha_inicio: datetime, fecha_fin: datetime) -> list:
        return self.sesion.query(Historial).filter(
            Historial.fecha_registro >= fecha_inicio,
            Historial.fecha_registro <= fecha_fin
        ).order_by(Historial.fecha_registro.desc()).all()
    
    def obtener_todos(self, limite: int = 100, desplazamiento: int = 0) -> list:
        return self.sesion.query(Historial).order_by(
            Historial.fecha_registro.desc()
        ).limit(limite).offset(desplazamiento).all()
    
    def contar_total(self) -> int:
        return self.sesion.query(Historial).count()
    
    def actualizar(self, historial_id: str, datos_actualizacion: dict) -> Historial:
        historial = self.obtener_por_id(historial_id)
        for clave, valor in datos_actualizacion.items():
            if hasattr(historial, clave) and valor is not None:
                setattr(historial, clave, valor)
        self.sesion.commit()
        self.sesion.refresh(historial)
        return historial
    
    def eliminar(self, historial_id: str) -> bool:
        historial = self.obtener_por_id(historial_id)
        self.sesion.delete(historial)
        self.sesion.commit()
        return True
    
    def obtener_ultimo_historial_paciente(self, paciente_id: str) -> Optional[Historial]:
        return self.sesion.query(Historial).filter(
            Historial.paciente_id == paciente_id
        ).order_by(Historial.fecha_registro.desc()).first()

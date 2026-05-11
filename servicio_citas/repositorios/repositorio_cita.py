from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
from servicio_citas.modelos.cita import Cita
from typing import List, Optional

class RepositorioCita:
    def __init__(self, sesion: Session):
        self.sesion = sesion
    
    def crear(self, cita: Cita) -> Cita:
        self.sesion.add(cita)
        self.sesion.commit()
        self.sesion.refresh(cita)
        return cita
    
    def obtener_por_id(self, cita_id: str) -> Optional[Cita]:
        return self.sesion.query(Cita).filter(Cita.id == cita_id).first()
    
    def obtener_por_paciente(self, paciente_id: str, limite: int = 50) -> List[Cita]:
        return self.sesion.query(Cita)\
            .filter(Cita.paciente_id == paciente_id)\
            .order_by(Cita.fecha_cita.desc())\
            .limit(limite)\
            .all()
    
    def obtener_por_medico(self, medico_id: str, limite: int = 50) -> List[Cita]:
        return self.sesion.query(Cita)\
            .filter(Cita.medico_id == medico_id)\
            .order_by(Cita.fecha_cita.desc())\
            .limit(limite)\
            .all()
    
    def obtener_por_fecha(self, fecha: str) -> List[Cita]:
        return self.sesion.query(Cita)\
            .filter(Cita.fecha_cita == fecha)\
            .order_by(Cita.hora_inicio)\
            .all()
    
    def obtener_por_fecha_rango(self, fecha_inicio: str, fecha_fin: str) -> List[Cita]:
        return self.sesion.query(Cita)\
            .filter(and_(
                Cita.fecha_cita >= fecha_inicio,
                Cita.fecha_cita <= fecha_fin
            ))\
            .order_by(Cita.fecha_cita, Cita.hora_inicio)\
            .all()
    
    def obtener_todas(self, limite: int = 50, desplazamiento: int = 0) -> List[Cita]:
        return self.sesion.query(Cita)\
            .order_by(Cita.fecha_cita.desc())\
            .offset(desplazamiento)\
            .limit(limite)\
            .all()
    
    def contar_total(self) -> int:
        return self.sesion.query(Cita).count()
    
    def actualizar(self, cita_id: str, datos: dict) -> Optional[Cita]:
        cita = self.obtener_por_id(cita_id)
        if cita:
            for clave, valor in datos.items():
                if valor is not None:
                    setattr(cita, clave, valor)
            self.sesion.commit()
            self.sesion.refresh(cita)
        return cita
    
    def eliminar(self, cita_id: str) -> bool:
        cita = self.obtener_por_id(cita_id)
        if cita:
            self.sesion.delete(cita)
            self.sesion.commit()
            return True
        return False
    
    def obtener_conflictos(self, medico_id: str, fecha: str, hora_inicio: str, hora_fin: str) -> List[Cita]:
        """
        Obtiene conflictos horarios del médico en la fecha especificada.
        Una cita entra en conflicto si:
        - Es del mismo médico
        - Es en la misma fecha
        - Su horario se solapa con el horario especificado
        - No está cancelada
        """
        conflictos = self.sesion.query(Cita).filter(
            and_(
                Cita.medico_id == medico_id,
                Cita.fecha_cita == fecha,
                Cita.estado != "cancelada",
                or_(
                    # La cita existente comienza antes de que termine la nueva
                    and_(
                        Cita.hora_inicio < hora_fin,
                        Cita.hora_fin > hora_inicio
                    )
                )
            )
        ).all()
        return conflictos

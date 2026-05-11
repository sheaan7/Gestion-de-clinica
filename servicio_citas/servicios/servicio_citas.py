from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from servicio_citas.modelos.cita import Cita
from servicio_citas.repositorios.repositorio_cita import RepositorioCita
from servicio_citas.esquemas.cita_esquema import CrearCitaRequest, ActualizarCitaRequest, CancelarCitaRequest
from typing import List, Optional

class ServicioCitas:
    def __init__(self, sesion: Session):
        self.repositorio = RepositorioCita(sesion)
        self.sesion = sesion
    
    def validar_fecha_futura(self, fecha_str: str) -> bool:
        """Valida que la fecha no sea anterior a hoy"""
        try:
            fecha = datetime.strptime(fecha_str, "%Y-%m-%d").date()
            hoy = datetime.now().date()
            return fecha >= hoy
        except ValueError:
            return False
    
    def validar_horarios(self, hora_inicio: str, hora_fin: str) -> bool:
        """Valida que hora_fin > hora_inicio"""
        try:
            inicio = datetime.strptime(hora_inicio, "%H:%M").time()
            fin = datetime.strptime(hora_fin, "%H:%M").time()
            return fin > inicio
        except ValueError:
            return False
    
    def validar_horario_disponible(self, medico_id: str, fecha: str, hora_inicio: str, hora_fin: str) -> bool:
        """
        Valida que no haya conflictos horarios.
        Retorna True si está disponible (sin conflictos)
        """
        conflictos = self.repositorio.obtener_conflictos(
            medico_id, fecha, hora_inicio, hora_fin
        )
        return len(conflictos) == 0
    
    def agendar_cita(self, datos: CrearCitaRequest) -> dict:
        """
        Agenda una nueva cita con todas las validaciones.
        Retorna diccionario con resultado y detalles.
        """
        # Validar formato de fecha
        if not self.validar_fecha_futura(datos.fecha_cita):
            return {
                "exito": False,
                "mensaje": "La fecha de la cita debe ser en el futuro",
                "codigo": "FECHA_INVALIDA"
            }
        
        # Validar horarios
        if not self.validar_horarios(datos.hora_inicio, datos.hora_fin):
            return {
                "exito": False,
                "mensaje": "La hora de fin debe ser mayor a la hora de inicio",
                "codigo": "HORARIO_INVALIDO"
            }
        
        # Validar conflictos horarios (CRÍTICO)
        if not self.validar_horario_disponible(datos.medico_id, datos.fecha_cita, datos.hora_inicio, datos.hora_fin):
            return {
                "exito": False,
                "mensaje": "El médico no está disponible en ese horario",
                "codigo": "CONFLICTO_HORARIO"
            }
        
        # Crear la cita
        cita = Cita(
            paciente_id=datos.paciente_id,
            medico_id=datos.medico_id,
            fecha_cita=datos.fecha_cita,
            hora_inicio=datos.hora_inicio,
            hora_fin=datos.hora_fin,
            motivo=datos.motivo,
            estado="pendiente",
            notas=datos.notas
        )
        
        cita_creada = self.repositorio.crear(cita)
        
        return {
            "exito": True,
            "mensaje": "Cita agendada exitosamente",
            "cita": cita_creada,
            "codigo": "CITA_CREADA"
        }
    
    def obtener_cita(self, cita_id: str) -> Optional[Cita]:
        return self.repositorio.obtener_por_id(cita_id)
    
    def actualizar_cita(self, cita_id: str, datos: ActualizarCitaRequest) -> dict:
        """Actualiza una cita existente con validaciones"""
        cita = self.repositorio.obtener_por_id(cita_id)
        
        if not cita:
            return {
                "exito": False,
                "mensaje": "Cita no encontrada",
                "codigo": "CITA_NO_ENCONTRADA"
            }
        
        # Si se actualizan horarios, validar
        datos_actualizacion = {}
        
        if datos.fecha_cita:
            if not self.validar_fecha_futura(datos.fecha_cita):
                return {
                    "exito": False,
                    "mensaje": "La fecha de la cita debe ser en el futuro",
                    "codigo": "FECHA_INVALIDA"
                }
            datos_actualizacion["fecha_cita"] = datos.fecha_cita
        
        if datos.hora_inicio or datos.hora_fin:
            hora_inicio = datos.hora_inicio or cita.hora_inicio
            hora_fin = datos.hora_fin or cita.hora_fin
            
            if not self.validar_horarios(hora_inicio, hora_fin):
                return {
                    "exito": False,
                    "mensaje": "La hora de fin debe ser mayor a la hora de inicio",
                    "codigo": "HORARIO_INVALIDO"
                }
            
            fecha_validar = datos.fecha_cita or cita.fecha_cita
            
            if not self.validar_horario_disponible(cita.medico_id, fecha_validar, hora_inicio, hora_fin):
                return {
                    "exito": False,
                    "mensaje": "El médico no está disponible en ese horario",
                    "codigo": "CONFLICTO_HORARIO"
                }
            
            datos_actualizacion["hora_inicio"] = hora_inicio
            datos_actualizacion["hora_fin"] = hora_fin
        
        if datos.motivo:
            datos_actualizacion["motivo"] = datos.motivo
        
        if datos.estado:
            datos_actualizacion["estado"] = datos.estado
        
        if datos.notas is not None:
            datos_actualizacion["notas"] = datos.notas
        
        cita_actualizada = self.repositorio.actualizar(cita_id, datos_actualizacion)
        
        return {
            "exito": True,
            "mensaje": "Cita actualizada exitosamente",
            "cita": cita_actualizada,
            "codigo": "CITA_ACTUALIZADA"
        }
    
    def cancelar_cita(self, cita_id: str, cancelada_por: str, razon: str) -> dict:
        """Cancela una cita"""
        cita = self.repositorio.obtener_por_id(cita_id)
        
        if not cita:
            return {
                "exito": False,
                "mensaje": "Cita no encontrada",
                "codigo": "CITA_NO_ENCONTRADA"
            }
        
        datos_actualizacion = {
            "estado": "cancelada",
            "cancelada_por": cancelada_por,
            "razon_cancelacion": razon
        }
        
        cita_cancelada = self.repositorio.actualizar(cita_id, datos_actualizacion)
        
        return {
            "exito": True,
            "mensaje": "Cita cancelada exitosamente",
            "cita": cita_cancelada,
            "codigo": "CITA_CANCELADA"
        }
    
    def listar_citas(self, limite: int = 50, desplazamiento: int = 0) -> List[Cita]:
        return self.repositorio.obtener_todas(limite, desplazamiento)
    
    def listar_por_paciente(self, paciente_id: str, limite: int = 50) -> List[Cita]:
        return self.repositorio.obtener_por_paciente(paciente_id, limite)
    
    def listar_por_medico(self, medico_id: str, limite: int = 50) -> List[Cita]:
        return self.repositorio.obtener_por_medico(medico_id, limite)
    
    def listar_por_fecha(self, fecha: str) -> List[Cita]:
        return self.repositorio.obtener_por_fecha(fecha)
    
    def contar_total(self) -> int:
        return self.repositorio.contar_total()

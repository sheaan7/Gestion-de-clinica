from sqlalchemy.orm import Session
from datetime import datetime
from servicio_historiales.modelos.historial import Historial
from servicio_historiales.repositorios.repositorio_historial import RepositorioHistorial
from servicio_historiales.esquemas.historial_esquema import CrearHistorialRequest, ActualizarHistorialRequest
from servicio_historiales.utilidades.excepciones import DatosInvalidos
from uuid import uuid4

class ServicioHistoriales:
    def __init__(self, sesion: Session):
        self.sesion = sesion
        self.repositorio = RepositorioHistorial(sesion)
    
    def crear_registro(self, datos: CrearHistorialRequest) -> dict:
        self.validar_datos(datos)
        
        nuevo_historial = Historial(
            id=str(uuid4()),
            paciente_id=datos.paciente_id,
            medico_id=datos.medico_id,
            cita_id=datos.cita_id,
            diagnostico=datos.diagnostico,
            tratamiento=datos.tratamiento,
            medicamentos_prescritos=datos.medicamentos_prescritos,
            observaciones=datos.observaciones,
            estado_paciente=datos.estado_paciente,
            proxima_cita_recomendada=datos.proxima_cita_recomendada,
            resultados_laboratorio=datos.resultados_laboratorio
        )
        
        historial_creado = self.repositorio.crear(nuevo_historial)
        
        return {
            "id": historial_creado.id,
            "paciente_id": historial_creado.paciente_id,
            "medico_id": historial_creado.medico_id,
            "fecha_registro": historial_creado.fecha_registro.isoformat(),
            "estado_paciente": historial_creado.estado_paciente
        }
    
    def obtener_historial(self, historial_id: str) -> dict:
        historial = self.repositorio.obtener_por_id(historial_id)
        return self.formatear_historial(historial)
    
    def actualizar_historial(self, historial_id: str, datos: ActualizarHistorialRequest) -> dict:
        datos_dict = datos.model_dump(exclude_unset=True)
        historial = self.repositorio.actualizar(historial_id, datos_dict)
        return self.formatear_historial(historial)
    
    def eliminar_historial(self, historial_id: str) -> bool:
        return self.repositorio.eliminar(historial_id)
    
    def listar_historiales(self, limite: int = 100, desplazamiento: int = 0) -> dict:
        historiales = self.repositorio.obtener_todos(limite, desplazamiento)
        total = self.repositorio.contar_total()
        
        return {
            "total": total,
            "limite": limite,
            "desplazamiento": desplazamiento,
            "historiales": [self.formatear_historial(h) for h in historiales]
        }
    
    def listar_por_paciente(self, paciente_id: str, limite: int = 100) -> dict:
        historiales = self.repositorio.obtener_por_paciente(paciente_id, limite)
        
        return {
            "paciente_id": paciente_id,
            "total": len(historiales),
            "historiales": [self.formatear_historial(h) for h in historiales]
        }
    
    def listar_por_medico(self, medico_id: str, limite: int = 100) -> dict:
        historiales = self.repositorio.obtener_por_medico(medico_id, limite)
        
        return {
            "medico_id": medico_id,
            "total": len(historiales),
            "historiales": [self.formatear_historial(h) for h in historiales]
        }
    
    def listar_por_fecha(self, fecha_inicio: str, fecha_fin: str) -> dict:
        try:
            inicio = datetime.fromisoformat(fecha_inicio)
            fin = datetime.fromisoformat(fecha_fin)
        except ValueError:
            raise DatosInvalidos("Formato de fecha inválido. Use ISO 8601: YYYY-MM-DDTHH:MM:SS")
        
        historiales = self.repositorio.obtener_por_fecha_rango(inicio, fin)
        
        return {
            "fecha_inicio": fecha_inicio,
            "fecha_fin": fecha_fin,
            "total": len(historiales),
            "historiales": [self.formatear_historial(h) for h in historiales]
        }
    
    def obtener_historial_completo_paciente(self, paciente_id: str) -> dict:
        historiales = self.repositorio.obtener_por_paciente(paciente_id, limite=1000)
        
        return {
            "paciente_id": paciente_id,
            "total_registros": len(historiales),
            "historiales": [self.formatear_historial(h) for h in historiales]
        }
    
    def validar_datos(self, datos: CrearHistorialRequest) -> None:
        if not datos.paciente_id or not datos.medico_id:
            raise DatosInvalidos("paciente_id y medico_id son obligatorios")
        
        if not datos.diagnostico or not datos.tratamiento:
            raise DatosInvalidos("diagnostico y tratamiento son obligatorios")
        
        estados_validos = ["crítico", "grave", "estable", "mejoría"]
        if datos.estado_paciente not in estados_validos:
            raise DatosInvalidos(f"estado_paciente debe ser uno de: {', '.join(estados_validos)}")
    
    @staticmethod
    def formatear_historial(historial: Historial) -> dict:
        return {
            "id": historial.id,
            "paciente_id": historial.paciente_id,
            "medico_id": historial.medico_id,
            "cita_id": historial.cita_id,
            "fecha_registro": historial.fecha_registro.isoformat() if historial.fecha_registro else None,
            "diagnostico": historial.diagnostico,
            "tratamiento": historial.tratamiento,
            "medicamentos_prescritos": historial.medicamentos_prescritos,
            "observaciones": historial.observaciones,
            "estado_paciente": historial.estado_paciente,
            "proxima_cita_recomendada": historial.proxima_cita_recomendada,
            "resultados_laboratorio": historial.resultados_laboratorio,
            "fecha_creacion": historial.fecha_creacion.isoformat() if historial.fecha_creacion else None,
            "fecha_actualizacion": historial.fecha_actualizacion.isoformat() if historial.fecha_actualizacion else None
        }

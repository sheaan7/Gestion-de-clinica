from sqlalchemy.orm import Session
from uuid import uuid4
from servicio_medicos.modelos.medico import Medico
from servicio_medicos.repositorios.repositorio_medico import RepositorioMedico
from servicio_medicos.esquemas.medico_esquema import CrearMedicoRequest, ActualizarMedicoRequest
from servicio_medicos.utilidades.excepciones import DatosInvalidos, EmailYaRegistrado, RecursoNoEncontrado
from servicio_medicos.utilidades.validadores import validar_email, validar_especialidad, validar_licencia_medica, validar_nombre

class ServicioMedicos:
    def __init__(self, sesion: Session):
        self.sesion = sesion
        self.repositorio = RepositorioMedico(sesion)
    
    def crear_medico(self, datos: CrearMedicoRequest) -> dict:
        if not validar_email(datos.email):
            raise DatosInvalidos("Email inválido")
        
        if self.repositorio.existe_email(datos.email):
            raise EmailYaRegistrado()
        
        if not validar_licencia_medica(datos.licencia_medica):
            raise DatosInvalidos("Licencia médica inválida (5-50 caracteres alfanuméricos)")
        
        if self.repositorio.existe_licencia(datos.licencia_medica):
            raise DatosInvalidos("Licencia médica ya registrada")
        
        if not validar_especialidad(datos.especialidad):
            raise DatosInvalidos("Especialidad inválida")
        
        if not validar_nombre(datos.nombre):
            raise DatosInvalidos("Nombre debe tener entre 3 y 100 caracteres")
        
        nuevo_medico = Medico(
            id=str(uuid4()),
            email=datos.email,
            nombre=datos.nombre,
            apellido=datos.apellido,
            telefono=datos.telefono,
            especialidad=datos.especialidad,
            licencia_medica=datos.licencia_medica,
            experiencia_años=datos.experiencia_años,
            biografia=datos.biografia,
            horario_inicio=datos.horario_inicio,
            horario_fin=datos.horario_fin,
            dias_laborales=datos.dias_laborales,
            foto_perfil=datos.foto_perfil
        )
        
        medico_creado = self.repositorio.crear(nuevo_medico)
        return self._medico_a_dict(medico_creado)
    
    def obtener_medico(self, medico_id: str) -> dict:
        medico = self.repositorio.obtener_por_id(medico_id)
        return self._medico_a_dict(medico)
    
    def actualizar_medico(self, medico_id: str, datos: ActualizarMedicoRequest) -> dict:
        if datos.especialidad and not validar_especialidad(datos.especialidad):
            raise DatosInvalidos("Especialidad inválida")
        
        datos_dict = datos.model_dump(exclude_unset=True)
        medico_actualizado = self.repositorio.actualizar(medico_id, datos_dict)
        return self._medico_a_dict(medico_actualizado)
    
    def eliminar_medico(self, medico_id: str) -> bool:
        return self.repositorio.eliminar(medico_id)
    
    def listar_medicos(self, limite: int = 100, desplazamiento: int = 0) -> dict:
        medicos = self.repositorio.obtener_todos(limite, desplazamiento)
        total = self.repositorio.contar_total()
        
        return {
            "medicos": [self._medico_a_dict(m) for m in medicos],
            "total": total,
            "limite": limite,
            "desplazamiento": desplazamiento
        }
    
    def listar_por_especialidad(self, especialidad: str, limite: int = 100) -> dict:
        if not validar_especialidad(especialidad):
            raise DatosInvalidos("Especialidad inválida")
        
        medicos = self.repositorio.obtener_por_especialidad(especialidad, limite)
        return {
            "especialidad": especialidad,
            "medicos": [self._medico_a_dict(m) for m in medicos],
            "total": len(medicos)
        }
    
    def listar_disponibles(self, especialidad: str = None, limite: int = 100) -> dict:
        if especialidad and not validar_especialidad(especialidad):
            raise DatosInvalidos("Especialidad inválida")
        
        medicos = self.repositorio.obtener_disponibles(especialidad, limite)
        return {
            "especialidad": especialidad,
            "medicos": [self._medico_a_dict(m) for m in medicos],
            "total": len(medicos)
        }
    
    def cambiar_disponibilidad(self, medico_id: str, disponible: bool) -> dict:
        datos = {"disponible": disponible}
        medico_actualizado = self.repositorio.actualizar(medico_id, datos)
        return self._medico_a_dict(medico_actualizado)
    
    def _medico_a_dict(self, medico: Medico) -> dict:
        return {
            "id": medico.id,
            "email": medico.email,
            "nombre": medico.nombre,
            "apellido": medico.apellido,
            "telefono": medico.telefono,
            "especialidad": medico.especialidad,
            "licencia_medica": medico.licencia_medica,
            "experiencia_años": medico.experiencia_años,
            "biografia": medico.biografia,
            "horario_inicio": medico.horario_inicio,
            "horario_fin": medico.horario_fin,
            "dias_laborales": medico.dias_laborales,
            "disponible": medico.disponible,
            "activo": medico.activo,
            "foto_perfil": medico.foto_perfil,
            "fecha_creacion": medico.fecha_creacion.isoformat() if medico.fecha_creacion else None
        }

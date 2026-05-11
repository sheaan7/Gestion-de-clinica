from sqlalchemy.orm import Session
from uuid import uuid4
from servicio_pacientes.modelos.paciente import Paciente
from servicio_pacientes.repositorios.repositorio_paciente import RepositorioPaciente
from servicio_pacientes.esquemas.paciente_esquema import CrearPacienteRequest, ActualizarPacienteRequest
from servicio_pacientes.utilidades.excepciones import DatosInvalidos, EmailYaRegistrado, RecursoNoEncontrado
from servicio_pacientes.utilidades.validadores import validar_email, validar_cedula, validar_nombre

class ServicioPacientes:
    def __init__(self, sesion: Session):
        self.sesion = sesion
        self.repositorio = RepositorioPaciente(sesion)
    
    def crear_paciente(self, datos: CrearPacienteRequest) -> dict:
        if not validar_email(datos.email):
            raise DatosInvalidos("Email inválido")
        
        if not validar_cedula(datos.numero_identidad):
            raise DatosInvalidos("Número de identidad inválido")
        
        if self.repositorio.existe_numero_identidad(datos.numero_identidad):
            raise DatosInvalidos("Número de identidad ya registrado")
        
        if self.repositorio.existe_email(datos.email):
            raise EmailYaRegistrado()
        
        if not validar_nombre(datos.nombre):
            raise DatosInvalidos("Nombre debe tener entre 3 y 100 caracteres")
        
        nuevo_paciente = Paciente(
            id=str(uuid4()),
            numero_identidad=datos.numero_identidad,
            nombre=datos.nombre,
            apellido=datos.apellido,
            email=datos.email,
            telefono=datos.telefono,
            fecha_nacimiento=datos.fecha_nacimiento,
            genero=datos.genero,
            direccion=datos.direccion,
            ciudad=datos.ciudad,
            tipo_sangre=datos.tipo_sangre,
            alergias=datos.alergias,
            condiciones_preexistentes=datos.condiciones_preexistentes,
            medicamentos_actuales=datos.medicamentos_actuales,
            contacto_emergencia_nombre=datos.contacto_emergencia_nombre,
            contacto_emergencia_telefono=datos.contacto_emergencia_telefono,
            contacto_emergencia_relacion=datos.contacto_emergencia_relacion
        )
        
        paciente_creado = self.repositorio.crear(nuevo_paciente)
        return self._paciente_a_dict(paciente_creado)
    
    def obtener_paciente(self, paciente_id: str) -> dict:
        paciente = self.repositorio.obtener_por_id(paciente_id)
        return self._paciente_a_dict(paciente)
    
    def actualizar_paciente(self, paciente_id: str, datos: ActualizarPacienteRequest) -> dict:
        datos_dict = datos.model_dump(exclude_unset=True)
        paciente_actualizado = self.repositorio.actualizar(paciente_id, datos_dict)
        return self._paciente_a_dict(paciente_actualizado)
    
    def eliminar_paciente(self, paciente_id: str) -> bool:
        return self.repositorio.eliminar(paciente_id)
    
    def listar_pacientes(self, limite: int = 100, desplazamiento: int = 0) -> dict:
        pacientes = self.repositorio.obtener_todos(limite, desplazamiento)
        total = self.repositorio.contar_total()
        
        return {
            "pacientes": [self._paciente_a_dict(p) for p in pacientes],
            "total": total,
            "limite": limite,
            "desplazamiento": desplazamiento
        }
    
    def buscar_pacientes(self, termino: str, limite: int = 100) -> dict:
        pacientes = self.repositorio.buscar_por_nombre(termino, limite)
        return {
            "pacientes": [self._paciente_a_dict(p) for p in pacientes],
            "total": len(pacientes),
            "termino_busqueda": termino
        }
    
    def obtener_por_numero_identidad(self, numero_identidad: str) -> dict:
        paciente = self.repositorio.obtener_por_numero_identidad(numero_identidad)
        if not paciente:
            raise RecursoNoEncontrado("Paciente")
        return self._paciente_a_dict(paciente)
    
    def _paciente_a_dict(self, paciente: Paciente) -> dict:
        return {
            "id": paciente.id,
            "numero_identidad": paciente.numero_identidad,
            "nombre": paciente.nombre,
            "apellido": paciente.apellido,
            "email": paciente.email,
            "telefono": paciente.telefono,
            "fecha_nacimiento": paciente.fecha_nacimiento,
            "genero": paciente.genero,
            "direccion": paciente.direccion,
            "ciudad": paciente.ciudad,
            "tipo_sangre": paciente.tipo_sangre,
            "alergias": paciente.alergias,
            "condiciones_preexistentes": paciente.condiciones_preexistentes,
            "medicamentos_actuales": paciente.medicamentos_actuales,
            "contacto_emergencia_nombre": paciente.contacto_emergencia_nombre,
            "contacto_emergencia_telefono": paciente.contacto_emergencia_telefono,
            "contacto_emergencia_relacion": paciente.contacto_emergencia_relacion,
            "activo": paciente.activo,
            "fecha_creacion": paciente.fecha_creacion
        }

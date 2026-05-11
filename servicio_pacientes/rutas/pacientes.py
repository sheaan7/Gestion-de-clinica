from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from servicio_pacientes.base_datos.conexion import obtener_bd
from servicio_pacientes.servicios.servicio_pacientes import ServicioPacientes
from servicio_pacientes.esquemas.paciente_esquema import CrearPacienteRequest, ActualizarPacienteRequest
from servicio_pacientes.utilidades.excepciones import ErrorAplicacion

router = APIRouter(prefix="/pacientes", tags=["pacientes"])

@router.post("")
async def crear_paciente(datos: CrearPacienteRequest, db: Session = Depends(obtener_bd)):
    try:
        servicio = ServicioPacientes(db)
        resultado = servicio.crear_paciente(datos)
        return {"exito": True, "datos": resultado}
    except ErrorAplicacion as e:
        return {"exito": False, "codigo": e.codigo, "mensaje": e.mensaje}
    except Exception:
        return {"exito": False, "codigo": "ERROR_SERVIDOR", "mensaje": "Error en el servidor"}

@router.get("/{paciente_id}")
async def obtener_paciente(paciente_id: str, db: Session = Depends(obtener_bd)):
    try:
        servicio = ServicioPacientes(db)
        resultado = servicio.obtener_paciente(paciente_id)
        return {"exito": True, "datos": resultado}
    except ErrorAplicacion as e:
        return {"exito": False, "codigo": e.codigo, "mensaje": e.mensaje}
    except Exception:
        return {"exito": False, "codigo": "ERROR_SERVIDOR", "mensaje": "Error en el servidor"}

@router.put("/{paciente_id}")
async def actualizar_paciente(paciente_id: str, datos: ActualizarPacienteRequest, db: Session = Depends(obtener_bd)):
    try:
        servicio = ServicioPacientes(db)
        resultado = servicio.actualizar_paciente(paciente_id, datos)
        return {"exito": True, "datos": resultado}
    except ErrorAplicacion as e:
        return {"exito": False, "codigo": e.codigo, "mensaje": e.mensaje}
    except Exception:
        return {"exito": False, "codigo": "ERROR_SERVIDOR", "mensaje": "Error en el servidor"}

@router.delete("/{paciente_id}")
async def eliminar_paciente(paciente_id: str, db: Session = Depends(obtener_bd)):
    try:
        servicio = ServicioPacientes(db)
        servicio.eliminar_paciente(paciente_id)
        return {"exito": True, "mensaje": "Paciente eliminado"}
    except ErrorAplicacion as e:
        return {"exito": False, "codigo": e.codigo, "mensaje": e.mensaje}
    except Exception:
        return {"exito": False, "codigo": "ERROR_SERVIDOR", "mensaje": "Error en el servidor"}

@router.get("")
async def listar_pacientes(limite: int = 100, desplazamiento: int = 0, db: Session = Depends(obtener_bd)):
    try:
        servicio = ServicioPacientes(db)
        resultado = servicio.listar_pacientes(limite, desplazamiento)
        return {"exito": True, "datos": resultado}
    except ErrorAplicacion as e:
        return {"exito": False, "codigo": e.codigo, "mensaje": e.mensaje}
    except Exception:
        return {"exito": False, "codigo": "ERROR_SERVIDOR", "mensaje": "Error en el servidor"}

@router.get("/buscar/{termino}")
async def buscar_pacientes(termino: str, limite: int = 100, db: Session = Depends(obtener_bd)):
    try:
        servicio = ServicioPacientes(db)
        resultado = servicio.buscar_pacientes(termino, limite)
        return {"exito": True, "datos": resultado}
    except ErrorAplicacion as e:
        return {"exito": False, "codigo": e.codigo, "mensaje": e.mensaje}
    except Exception:
        return {"exito": False, "codigo": "ERROR_SERVIDOR", "mensaje": "Error en el servidor"}

@router.get("/identidad/{numero_identidad}")
async def obtener_por_identidad(numero_identidad: str, db: Session = Depends(obtener_bd)):
    try:
        servicio = ServicioPacientes(db)
        resultado = servicio.obtener_por_numero_identidad(numero_identidad)
        return {"exito": True, "datos": resultado}
    except ErrorAplicacion as e:
        return {"exito": False, "codigo": e.codigo, "mensaje": e.mensaje}
    except Exception:
        return {"exito": False, "codigo": "ERROR_SERVIDOR", "mensaje": "Error en el servidor"}

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from servicio_medicos.base_datos.conexion import obtener_bd
from servicio_medicos.servicios.servicio_medicos import ServicioMedicos
from servicio_medicos.esquemas.medico_esquema import CrearMedicoRequest, ActualizarMedicoRequest
from servicio_medicos.utilidades.excepciones import ErrorAplicacion

router = APIRouter(prefix="/medicos", tags=["medicos"])

@router.post("")
async def crear_medico(datos: CrearMedicoRequest, db: Session = Depends(obtener_bd)):
    try:
        servicio = ServicioMedicos(db)
        resultado = servicio.crear_medico(datos)
        return {"exito": True, "datos": resultado}
    except ErrorAplicacion as e:
        return {"exito": False, "codigo": e.codigo, "mensaje": e.mensaje}
    except Exception:
        return {"exito": False, "codigo": "ERROR_SERVIDOR", "mensaje": "Error en el servidor"}

@router.get("/{medico_id}")
async def obtener_medico(medico_id: str, db: Session = Depends(obtener_bd)):
    try:
        servicio = ServicioMedicos(db)
        resultado = servicio.obtener_medico(medico_id)
        return {"exito": True, "datos": resultado}
    except ErrorAplicacion as e:
        return {"exito": False, "codigo": e.codigo, "mensaje": e.mensaje}
    except Exception:
        return {"exito": False, "codigo": "ERROR_SERVIDOR", "mensaje": "Error en el servidor"}

@router.put("/{medico_id}")
async def actualizar_medico(medico_id: str, datos: ActualizarMedicoRequest, db: Session = Depends(obtener_bd)):
    try:
        servicio = ServicioMedicos(db)
        resultado = servicio.actualizar_medico(medico_id, datos)
        return {"exito": True, "datos": resultado}
    except ErrorAplicacion as e:
        return {"exito": False, "codigo": e.codigo, "mensaje": e.mensaje}
    except Exception:
        return {"exito": False, "codigo": "ERROR_SERVIDOR", "mensaje": "Error en el servidor"}

@router.delete("/{medico_id}")
async def eliminar_medico(medico_id: str, db: Session = Depends(obtener_bd)):
    try:
        servicio = ServicioMedicos(db)
        servicio.eliminar_medico(medico_id)
        return {"exito": True, "mensaje": "Médico eliminado"}
    except ErrorAplicacion as e:
        return {"exito": False, "codigo": e.codigo, "mensaje": e.mensaje}
    except Exception:
        return {"exito": False, "codigo": "ERROR_SERVIDOR", "mensaje": "Error en el servidor"}

@router.get("")
async def listar_medicos(limite: int = 100, desplazamiento: int = 0, db: Session = Depends(obtener_bd)):
    try:
        servicio = ServicioMedicos(db)
        resultado = servicio.listar_medicos(limite, desplazamiento)
        return {"exito": True, "datos": resultado}
    except ErrorAplicacion as e:
        return {"exito": False, "codigo": e.codigo, "mensaje": e.mensaje}
    except Exception:
        return {"exito": False, "codigo": "ERROR_SERVIDOR", "mensaje": "Error en el servidor"}

@router.get("/especialidad/{especialidad}")
async def listar_por_especialidad(especialidad: str, limite: int = 100, db: Session = Depends(obtener_bd)):
    try:
        servicio = ServicioMedicos(db)
        resultado = servicio.listar_por_especialidad(especialidad, limite)
        return {"exito": True, "datos": resultado}
    except ErrorAplicacion as e:
        return {"exito": False, "codigo": e.codigo, "mensaje": e.mensaje}
    except Exception:
        return {"exito": False, "codigo": "ERROR_SERVIDOR", "mensaje": "Error en el servidor"}

@router.get("/disponibles/listar")
async def listar_disponibles(especialidad: str = Query(None), limite: int = 100, db: Session = Depends(obtener_bd)):
    try:
        servicio = ServicioMedicos(db)
        resultado = servicio.listar_disponibles(especialidad, limite)
        return {"exito": True, "datos": resultado}
    except ErrorAplicacion as e:
        return {"exito": False, "codigo": e.codigo, "mensaje": e.mensaje}
    except Exception:
        return {"exito": False, "codigo": "ERROR_SERVIDOR", "mensaje": "Error en el servidor"}

@router.patch("/{medico_id}/disponibilidad")
async def cambiar_disponibilidad(medico_id: str, disponible: bool = Query(...), db: Session = Depends(obtener_bd)):
    try:
        servicio = ServicioMedicos(db)
        resultado = servicio.cambiar_disponibilidad(medico_id, disponible)
        return {"exito": True, "datos": resultado}
    except ErrorAplicacion as e:
        return {"exito": False, "codigo": e.codigo, "mensaje": e.mensaje}
    except Exception:
        return {"exito": False, "codigo": "ERROR_SERVIDOR", "mensaje": "Error en el servidor"}

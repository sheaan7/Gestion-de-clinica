from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from servicio_historiales.base_datos.conexion import obtener_bd
from servicio_historiales.servicios.servicio_historiales import ServicioHistoriales
from servicio_historiales.esquemas.historial_esquema import (
    CrearHistorialRequest, ActualizarHistorialRequest, HistorialResponse
)
from servicio_historiales.utilidades.respuestas import RespuestaExito, RespuestaError
from servicio_historiales.utilidades.excepciones import ErrorAplicacion

router = APIRouter(prefix="/historiales", tags=["historiales"])

@router.post("")
async def crear_historial(
    datos: CrearHistorialRequest,
    db: Session = Depends(obtener_bd)
):
    try:
        servicio = ServicioHistoriales(db)
        resultado = servicio.crear_registro(datos)
        respuesta = RespuestaExito(
            datos=resultado,
            mensaje="Historial clínico creado exitosamente",
            codigo="HISTORIAL_CREADO"
        )
        return respuesta.a_dict()
    except ErrorAplicacion as e:
        respuesta = RespuestaError(e.codigo, e.mensaje)
        return respuesta.a_dict()
    except Exception as e:
        respuesta = RespuestaError("ERROR_SERVIDOR", "Error en el servidor")
        return respuesta.a_dict()

@router.get("/{historial_id}")
async def obtener_historial(
    historial_id: str,
    db: Session = Depends(obtener_bd)
):
    try:
        servicio = ServicioHistoriales(db)
        resultado = servicio.obtener_historial(historial_id)
        respuesta = RespuestaExito(
            datos=resultado,
            mensaje="Historial obtenido exitosamente",
            codigo="HISTORIAL_OBTENIDO"
        )
        return respuesta.a_dict()
    except ErrorAplicacion as e:
        respuesta = RespuestaError(e.codigo, e.mensaje)
        return respuesta.a_dict()
    except Exception as e:
        respuesta = RespuestaError("ERROR_SERVIDOR", "Error en el servidor")
        return respuesta.a_dict()

@router.put("/{historial_id}")
async def actualizar_historial(
    historial_id: str,
    datos: ActualizarHistorialRequest,
    db: Session = Depends(obtener_bd)
):
    try:
        servicio = ServicioHistoriales(db)
        resultado = servicio.actualizar_historial(historial_id, datos)
        respuesta = RespuestaExito(
            datos=resultado,
            mensaje="Historial actualizado exitosamente",
            codigo="HISTORIAL_ACTUALIZADO"
        )
        return respuesta.a_dict()
    except ErrorAplicacion as e:
        respuesta = RespuestaError(e.codigo, e.mensaje)
        return respuesta.a_dict()
    except Exception as e:
        respuesta = RespuestaError("ERROR_SERVIDOR", "Error en el servidor")
        return respuesta.a_dict()

@router.delete("/{historial_id}")
async def eliminar_historial(
    historial_id: str,
    db: Session = Depends(obtener_bd)
):
    try:
        servicio = ServicioHistoriales(db)
        servicio.eliminar_historial(historial_id)
        respuesta = RespuestaExito(
            datos={"id": historial_id},
            mensaje="Historial eliminado exitosamente",
            codigo="HISTORIAL_ELIMINADO"
        )
        return respuesta.a_dict()
    except ErrorAplicacion as e:
        respuesta = RespuestaError(e.codigo, e.mensaje)
        return respuesta.a_dict()
    except Exception as e:
        respuesta = RespuestaError("ERROR_SERVIDOR", "Error en el servidor")
        return respuesta.a_dict()

@router.get("")
async def listar_historiales(
    limite: int = 100,
    desplazamiento: int = 0,
    db: Session = Depends(obtener_bd)
):
    try:
        servicio = ServicioHistoriales(db)
        resultado = servicio.listar_historiales(limite, desplazamiento)
        respuesta = RespuestaExito(
            datos=resultado,
            mensaje="Historiales obtenidos exitosamente",
            codigo="HISTORIALES_OBTENIDOS"
        )
        return respuesta.a_dict()
    except ErrorAplicacion as e:
        respuesta = RespuestaError(e.codigo, e.mensaje)
        return respuesta.a_dict()
    except Exception as e:
        respuesta = RespuestaError("ERROR_SERVIDOR", "Error en el servidor")
        return respuesta.a_dict()

@router.get("/paciente/{paciente_id}")
async def listar_por_paciente(
    paciente_id: str,
    limite: int = 100,
    db: Session = Depends(obtener_bd)
):
    try:
        servicio = ServicioHistoriales(db)
        resultado = servicio.listar_por_paciente(paciente_id, limite)
        respuesta = RespuestaExito(
            datos=resultado,
            mensaje="Historiales del paciente obtenidos exitosamente",
            codigo="HISTORIALES_PACIENTE_OBTENIDOS"
        )
        return respuesta.a_dict()
    except ErrorAplicacion as e:
        respuesta = RespuestaError(e.codigo, e.mensaje)
        return respuesta.a_dict()
    except Exception as e:
        respuesta = RespuestaError("ERROR_SERVIDOR", "Error en el servidor")
        return respuesta.a_dict()

@router.get("/medico/{medico_id}")
async def listar_por_medico(
    medico_id: str,
    limite: int = 100,
    db: Session = Depends(obtener_bd)
):
    try:
        servicio = ServicioHistoriales(db)
        resultado = servicio.listar_por_medico(medico_id, limite)
        respuesta = RespuestaExito(
            datos=resultado,
            mensaje="Registros del médico obtenidos exitosamente",
            codigo="REGISTROS_MEDICO_OBTENIDOS"
        )
        return respuesta.a_dict()
    except ErrorAplicacion as e:
        respuesta = RespuestaError(e.codigo, e.mensaje)
        return respuesta.a_dict()
    except Exception as e:
        respuesta = RespuestaError("ERROR_SERVIDOR", "Error en el servidor")
        return respuesta.a_dict()

@router.get("/paciente/{paciente_id}/completo")
async def historial_completo_paciente(
    paciente_id: str,
    db: Session = Depends(obtener_bd)
):
    try:
        servicio = ServicioHistoriales(db)
        resultado = servicio.obtener_historial_completo_paciente(paciente_id)
        respuesta = RespuestaExito(
            datos=resultado,
            mensaje="Historial completo del paciente obtenido exitosamente",
            codigo="HISTORIAL_COMPLETO_OBTENIDO"
        )
        return respuesta.a_dict()
    except ErrorAplicacion as e:
        respuesta = RespuestaError(e.codigo, e.mensaje)
        return respuesta.a_dict()
    except Exception as e:
        respuesta = RespuestaError("ERROR_SERVIDOR", "Error en el servidor")
        return respuesta.a_dict()

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from servicio_citas.base_datos.conexion import obtener_bd
from servicio_citas.servicios.servicio_citas import ServicioCitas
from servicio_citas.esquemas.cita_esquema import (
    CrearCitaRequest, ActualizarCitaRequest, CancelarCitaRequest, CitaResponse
)
from typing import List

router = APIRouter(prefix="/citas", tags=["citas"])

@router.post("", response_model=dict, status_code=status.HTTP_201_CREATED)
def agendar_cita(
    datos: CrearCitaRequest,
    sesion: Session = Depends(obtener_bd)
):
    """
    Agenda una nueva cita.
    Valida conflictos horarios, fechas y horarios.
    """
    servicio = ServicioCitas(sesion)
    resultado = servicio.agendar_cita(datos)
    
    if not resultado["exito"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=resultado["mensaje"]
        )
    
    return {
        "mensaje": resultado["mensaje"],
        "cita": CitaResponse.from_orm(resultado["cita"])
    }

@router.get("/{cita_id}", response_model=CitaResponse)
def obtener_cita(
    cita_id: str,
    sesion: Session = Depends(obtener_bd)
):
    """Obtiene una cita por ID"""
    servicio = ServicioCitas(sesion)
    cita = servicio.obtener_cita(cita_id)
    
    if not cita:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cita no encontrada"
        )
    
    return CitaResponse.from_orm(cita)

@router.put("/{cita_id}", response_model=dict)
def actualizar_cita(
    cita_id: str,
    datos: ActualizarCitaRequest,
    sesion: Session = Depends(obtener_bd)
):
    """
    Actualiza una cita existente.
    Valida conflictos horarios si se actualiza horario.
    """
    servicio = ServicioCitas(sesion)
    resultado = servicio.actualizar_cita(cita_id, datos)
    
    if not resultado["exito"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=resultado["mensaje"]
        )
    
    return {
        "mensaje": resultado["mensaje"],
        "cita": CitaResponse.from_orm(resultado["cita"])
    }

@router.patch("/{cita_id}/cancelar", response_model=dict)
def cancelar_cita(
    cita_id: str,
    datos: CancelarCitaRequest,
    sesion: Session = Depends(obtener_bd)
):
    """Cancela una cita"""
    servicio = ServicioCitas(sesion)
    resultado = servicio.cancelar_cita(cita_id, "sistema", datos.razon_cancelacion)
    
    if not resultado["exito"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=resultado["mensaje"]
        )
    
    return {
        "mensaje": resultado["mensaje"],
        "cita": CitaResponse.from_orm(resultado["cita"])
    }

@router.get("", response_model=dict)
def listar_citas(
    limite: int = 50,
    desplazamiento: int = 0,
    sesion: Session = Depends(obtener_bd)
):
    """Lista todas las citas con paginación"""
    servicio = ServicioCitas(sesion)
    citas = servicio.listar_citas(limite, desplazamiento)
    total = servicio.contar_total()
    
    return {
        "total": total,
        "limite": limite,
        "desplazamiento": desplazamiento,
        "citas": [CitaResponse.from_orm(c) for c in citas]
    }

@router.get("/paciente/{paciente_id}", response_model=dict)
def listar_por_paciente(
    paciente_id: str,
    limite: int = 50,
    sesion: Session = Depends(obtener_bd)
):
    """Lista todas las citas de un paciente"""
    servicio = ServicioCitas(sesion)
    citas = servicio.listar_por_paciente(paciente_id, limite)
    
    return {
        "paciente_id": paciente_id,
        "cantidad": len(citas),
        "citas": [CitaResponse.from_orm(c) for c in citas]
    }

@router.get("/medico/{medico_id}", response_model=dict)
def listar_por_medico(
    medico_id: str,
    limite: int = 50,
    sesion: Session = Depends(obtener_bd)
):
    """Lista todas las citas de un médico"""
    servicio = ServicioCitas(sesion)
    citas = servicio.listar_por_medico(medico_id, limite)
    
    return {
        "medico_id": medico_id,
        "cantidad": len(citas),
        "citas": [CitaResponse.from_orm(c) for c in citas]
    }

@router.get("/fecha/{fecha}", response_model=dict)
def listar_por_fecha(
    fecha: str,
    sesion: Session = Depends(obtener_bd)
):
    """Lista todas las citas de una fecha especificada"""
    servicio = ServicioCitas(sesion)
    citas = servicio.listar_por_fecha(fecha)
    
    return {
        "fecha": fecha,
        "cantidad": len(citas),
        "citas": [CitaResponse.from_orm(c) for c in citas]
    }

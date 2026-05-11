from fastapi import APIRouter, Depends, Header
from sqlalchemy.orm import Session
from servicio_usuarios.base_datos.conexion import obtener_bd
from servicio_usuarios.servicios.servicio_usuarios import ServicioUsuarios
from servicio_usuarios.esquemas.usuario_esquema import CrearUsuarioRequest, ActualizarUsuarioRequest
from servicio_usuarios.utilidades.excepciones import ErrorAplicacion

router = APIRouter(prefix="/usuarios", tags=["usuarios"])

@router.post("")
async def crear_usuario(
    datos: CrearUsuarioRequest,
    db: Session = Depends(obtener_bd)
):
    try:
        servicio = ServicioUsuarios(db)
        resultado = servicio.crear_usuario(datos)
        return {"exito": True, "datos": resultado}
    except ErrorAplicacion as e:
        return {"exito": False, "codigo": e.codigo, "mensaje": e.mensaje}
    except Exception as e:
        return {"exito": False, "codigo": "ERROR_SERVIDOR", "mensaje": "Error en el servidor"}

@router.get("/{usuario_id}")
async def obtener_usuario(
    usuario_id: str,
    db: Session = Depends(obtener_bd)
):
    try:
        servicio = ServicioUsuarios(db)
        resultado = servicio.obtener_usuario(usuario_id)
        return {"exito": True, "datos": resultado}
    except ErrorAplicacion as e:
        return {"exito": False, "codigo": e.codigo, "mensaje": e.mensaje}
    except Exception as e:
        return {"exito": False, "codigo": "ERROR_SERVIDOR", "mensaje": "Error en el servidor"}

@router.put("/{usuario_id}")
async def actualizar_usuario(
    usuario_id: str,
    datos: ActualizarUsuarioRequest,
    db: Session = Depends(obtener_bd)
):
    try:
        servicio = ServicioUsuarios(db)
        resultado = servicio.actualizar_usuario(usuario_id, datos)
        return {"exito": True, "datos": resultado}
    except ErrorAplicacion as e:
        return {"exito": False, "codigo": e.codigo, "mensaje": e.mensaje}
    except Exception as e:
        return {"exito": False, "codigo": "ERROR_SERVIDOR", "mensaje": "Error en el servidor"}

@router.delete("/{usuario_id}")
async def eliminar_usuario(
    usuario_id: str,
    db: Session = Depends(obtener_bd)
):
    try:
        servicio = ServicioUsuarios(db)
        servicio.eliminar_usuario(usuario_id)
        return {"exito": True, "mensaje": "Usuario eliminado"}
    except ErrorAplicacion as e:
        return {"exito": False, "codigo": e.codigo, "mensaje": e.mensaje}
    except Exception as e:
        return {"exito": False, "codigo": "ERROR_SERVIDOR", "mensaje": "Error en el servidor"}

@router.get("")
async def listar_usuarios(
    limite: int = 100,
    desplazamiento: int = 0,
    db: Session = Depends(obtener_bd)
):
    try:
        servicio = ServicioUsuarios(db)
        resultado = servicio.listar_usuarios(limite, desplazamiento)
        return {"exito": True, "datos": resultado}
    except ErrorAplicacion as e:
        return {"exito": False, "codigo": e.codigo, "mensaje": e.mensaje}
    except Exception as e:
        return {"exito": False, "codigo": "ERROR_SERVIDOR", "mensaje": "Error en el servidor"}

@router.get("/rol/{rol}")
async def listar_por_rol(
    rol: str,
    limite: int = 100,
    desplazamiento: int = 0,
    db: Session = Depends(obtener_bd)
):
    try:
        servicio = ServicioUsuarios(db)
        resultado = servicio.listar_por_rol(rol, limite, desplazamiento)
        return {"exito": True, "datos": resultado}
    except ErrorAplicacion as e:
        return {"exito": False, "codigo": e.codigo, "mensaje": e.mensaje}
    except Exception as e:
        return {"exito": False, "codigo": "ERROR_SERVIDOR", "mensaje": "Error en el servidor"}

@router.get("/email/{email}")
async def buscar_por_email(
    email: str,
    db: Session = Depends(obtener_bd)
):
    try:
        servicio = ServicioUsuarios(db)
        resultado = servicio.buscar_por_email(email)
        return {"exito": True, "datos": resultado}
    except ErrorAplicacion as e:
        return {"exito": False, "codigo": e.codigo, "mensaje": e.mensaje}
    except Exception as e:
        return {"exito": False, "codigo": "ERROR_SERVIDOR", "mensaje": "Error en el servidor"}

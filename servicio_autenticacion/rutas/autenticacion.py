from fastapi import APIRouter, Depends, Header
from sqlalchemy.orm import Session
from servicio_autenticacion.base_datos.conexion import obtener_bd
from servicio_autenticacion.servicios.servicio_autenticacion import ServicioAutenticacion
from servicio_autenticacion.esquemas.usuario_esquema import (
    RegistroRequest, LoginRequest, RefreshTokenRequest, UsuarioResponse
)
from servicio_autenticacion.utilidades.respuestas import RespuestaExito, RespuestaError
from servicio_autenticacion.utilidades.excepciones import ErrorAplicacion

router = APIRouter(prefix="/auth", tags=["autenticacion"])

@router.post("/registro")
async def registro(
    datos: RegistroRequest,
    db: Session = Depends(obtener_bd)
):
    try:
        servicio = ServicioAutenticacion(db)
        resultado = servicio.registrar_usuario(datos)
        respuesta = RespuestaExito(
            datos=resultado,
            mensaje="Usuario registrado exitosamente",
            codigo="REGISTRO_EXITOSO"
        )
        return respuesta.a_dict()
    except ErrorAplicacion as e:
        respuesta = RespuestaError(e.codigo, e.mensaje)
        return respuesta.a_dict()
    except Exception as e:
        respuesta = RespuestaError("ERROR_SERVIDOR", "Error en el servidor")
        return respuesta.a_dict()

@router.post("/login")
async def login(
    datos: LoginRequest,
    db: Session = Depends(obtener_bd)
):
    try:
        servicio = ServicioAutenticacion(db)
        resultado = servicio.autenticar_usuario(datos)
        respuesta = RespuestaExito(
            datos=resultado,
            mensaje="Autenticación exitosa",
            codigo="LOGIN_EXITOSO"
        )
        return respuesta.a_dict()
    except ErrorAplicacion as e:
        respuesta = RespuestaError(e.codigo, e.mensaje)
        return respuesta.a_dict()
    except Exception as e:
        respuesta = RespuestaError("ERROR_SERVIDOR", "Error en el servidor")
        return respuesta.a_dict()

@router.post("/refresh")
async def refresh(
    datos: RefreshTokenRequest,
    db: Session = Depends(obtener_bd)
):
    try:
        servicio = ServicioAutenticacion(db)
        resultado = servicio.renovar_token(datos.refresh_token)
        respuesta = RespuestaExito(
            datos=resultado,
            mensaje="Token renovado exitosamente",
            codigo="REFRESH_EXITOSO"
        )
        return respuesta.a_dict()
    except ErrorAplicacion as e:
        respuesta = RespuestaError(e.codigo, e.mensaje)
        return respuesta.a_dict()
    except Exception as e:
        respuesta = RespuestaError("ERROR_SERVIDOR", "Error en el servidor")
        return respuesta.a_dict()

@router.get("/validar")
async def validar(
    authorization: str = Header(None),
    db: Session = Depends(obtener_bd)
):
    try:
        servicio = ServicioAutenticacion(db)
        datos = servicio.validar_token_actual(authorization)
        respuesta = RespuestaExito(
            datos=datos,
            mensaje="Token válido",
            codigo="TOKEN_VALIDO"
        )
        return respuesta.a_dict()
    except ErrorAplicacion as e:
        respuesta = RespuestaError(e.codigo, e.mensaje)
        return respuesta.a_dict()
    except Exception as e:
        respuesta = RespuestaError("ERROR_SERVIDOR", "Error en el servidor")
        return respuesta.a_dict()

@router.get("/usuarios/{usuario_id}")
async def obtener_usuario(
    usuario_id: str,
    authorization: str = Header(None),
    db: Session = Depends(obtener_bd)
):
    try:
        servicio = ServicioAutenticacion(db)
        servicio.validar_token_actual(authorization)
        resultado = servicio.obtener_perfil_usuario(usuario_id)
        respuesta = RespuestaExito(
            datos=resultado,
            mensaje="Perfil obtenido",
            codigo="PERFIL_OBTENIDO"
        )
        return respuesta.a_dict()
    except ErrorAplicacion as e:
        respuesta = RespuestaError(e.codigo, e.mensaje)
        return respuesta.a_dict()
    except Exception as e:
        respuesta = RespuestaError("ERROR_SERVIDOR", "Error en el servidor")
        return respuesta.a_dict()

@router.get("/usuarios")
async def listar_usuarios(
    limite: int = 100,
    desplazamiento: int = 0,
    authorization: str = Header(None),
    db: Session = Depends(obtener_bd)
):
    try:
        servicio = ServicioAutenticacion(db)
        servicio.validar_token_actual(authorization)
        resultado = servicio.listar_usuarios(limite, desplazamiento)
        respuesta = RespuestaExito(
            datos=resultado,
            mensaje="Usuarios listados",
            codigo="USUARIOS_LISTADOS"
        )
        return respuesta.a_dict()
    except ErrorAplicacion as e:
        respuesta = RespuestaError(e.codigo, e.mensaje)
        return respuesta.a_dict()
    except Exception as e:
        respuesta = RespuestaError("ERROR_SERVIDOR", "Error en el servidor")
        return respuesta.a_dict()

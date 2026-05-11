from fastapi import APIRouter, Depends, Header, HTTPException, status
from gateway_api.config.configuracion import configuracion
from gateway_api.utilidades.seguridad import obtener_usuario_actual
from gateway_api.utilidades.cliente_http import ClienteHTTP

router = APIRouter()

@router.post("/auth/registro")
async def registro(request_body: dict):
    cliente = ClienteHTTP(configuracion.servicio_autenticacion_url)
    resultado = await cliente.post("/auth/registro", request_body)
    await cliente.cerrar()
    return resultado

@router.post("/auth/login")
async def login(request_body: dict):
    cliente = ClienteHTTP(configuracion.servicio_autenticacion_url)
    resultado = await cliente.post("/auth/login", request_body)
    await cliente.cerrar()
    return resultado

@router.post("/auth/refresh")
async def refresh(request_body: dict):
    cliente = ClienteHTTP(configuracion.servicio_autenticacion_url)
    resultado = await cliente.post("/auth/refresh", request_body)
    await cliente.cerrar()
    return resultado

@router.get("/auth/validar")
async def validar_token(authorization: str = Header(None)):
    cliente = ClienteHTTP(configuracion.servicio_autenticacion_url)
    headers = {"Authorization": authorization} if authorization else {}
    resultado = await cliente.get("/auth/validar", headers)
    await cliente.cerrar()
    return resultado

@router.get("/usuarios")
async def listar_usuarios(authorization: str = Header(None)):
    usuario = obtener_usuario_actual(authorization)
    cliente = ClienteHTTP(configuracion.servicio_usuarios_url)
    headers = {"Authorization": authorization} if authorization else {}
    resultado = await cliente.get("/usuarios", headers)
    await cliente.cerrar()
    return resultado

@router.get("/usuarios/{usuario_id}")
async def obtener_usuario(usuario_id: str, authorization: str = Header(None)):
    usuario = obtener_usuario_actual(authorization)
    cliente = ClienteHTTP(configuracion.servicio_usuarios_url)
    headers = {"Authorization": authorization} if authorization else {}
    resultado = await cliente.get(f"/usuarios/{usuario_id}", headers)
    await cliente.cerrar()
    return resultado

@router.post("/usuarios")
async def crear_usuario(request_body: dict, authorization: str = Header(None)):
    usuario = obtener_usuario_actual(authorization)
    cliente = ClienteHTTP(configuracion.servicio_usuarios_url)
    headers = {"Authorization": authorization} if authorization else {}
    resultado = await cliente.post("/usuarios", request_body, headers)
    await cliente.cerrar()
    return resultado

@router.put("/usuarios/{usuario_id}")
async def actualizar_usuario(usuario_id: str, request_body: dict, authorization: str = Header(None)):
    usuario = obtener_usuario_actual(authorization)
    cliente = ClienteHTTP(configuracion.servicio_usuarios_url)
    headers = {"Authorization": authorization} if authorization else {}
    resultado = await cliente.put(f"/usuarios/{usuario_id}", request_body, headers)
    await cliente.cerrar()
    return resultado

@router.delete("/usuarios/{usuario_id}")
async def eliminar_usuario(usuario_id: str, authorization: str = Header(None)):
    usuario = obtener_usuario_actual(authorization)
    cliente = ClienteHTTP(configuracion.servicio_usuarios_url)
    headers = {"Authorization": authorization} if authorization else {}
    resultado = await cliente.delete(f"/usuarios/{usuario_id}", headers)
    await cliente.cerrar()
    return resultado

@router.get("/pacientes")
async def listar_pacientes(authorization: str = Header(None)):
    usuario = obtener_usuario_actual(authorization)
    cliente = ClienteHTTP(configuracion.servicio_pacientes_url)
    headers = {"Authorization": authorization} if authorization else {}
    resultado = await cliente.get("/pacientes", headers)
    await cliente.cerrar()
    return resultado

@router.get("/pacientes/{paciente_id}")
async def obtener_paciente(paciente_id: str, authorization: str = Header(None)):
    usuario = obtener_usuario_actual(authorization)
    cliente = ClienteHTTP(configuracion.servicio_pacientes_url)
    headers = {"Authorization": authorization} if authorization else {}
    resultado = await cliente.get(f"/pacientes/{paciente_id}", headers)
    await cliente.cerrar()
    return resultado

@router.post("/pacientes")
async def crear_paciente(request_body: dict, authorization: str = Header(None)):
    usuario = obtener_usuario_actual(authorization)
    cliente = ClienteHTTP(configuracion.servicio_pacientes_url)
    headers = {"Authorization": authorization} if authorization else {}
    resultado = await cliente.post("/pacientes", request_body, headers)
    await cliente.cerrar()
    return resultado

@router.put("/pacientes/{paciente_id}")
async def actualizar_paciente(paciente_id: str, request_body: dict, authorization: str = Header(None)):
    usuario = obtener_usuario_actual(authorization)
    cliente = ClienteHTTP(configuracion.servicio_pacientes_url)
    headers = {"Authorization": authorization} if authorization else {}
    resultado = await cliente.put(f"/pacientes/{paciente_id}", request_body, headers)
    await cliente.cerrar()
    return resultado

@router.delete("/pacientes/{paciente_id}")
async def eliminar_paciente(paciente_id: str, authorization: str = Header(None)):
    usuario = obtener_usuario_actual(authorization)
    cliente = ClienteHTTP(configuracion.servicio_pacientes_url)
    headers = {"Authorization": authorization} if authorization else {}
    resultado = await cliente.delete(f"/pacientes/{paciente_id}", headers)
    await cliente.cerrar()
    return resultado

@router.get("/medicos")
async def listar_medicos(authorization: str = Header(None)):
    usuario = obtener_usuario_actual(authorization)
    cliente = ClienteHTTP(configuracion.servicio_medicos_url)
    headers = {"Authorization": authorization} if authorization else {}
    resultado = await cliente.get("/medicos", headers)
    await cliente.cerrar()
    return resultado

@router.get("/medicos/{medico_id}")
async def obtener_medico(medico_id: str, authorization: str = Header(None)):
    usuario = obtener_usuario_actual(authorization)
    cliente = ClienteHTTP(configuracion.servicio_medicos_url)
    headers = {"Authorization": authorization} if authorization else {}
    resultado = await cliente.get(f"/medicos/{medico_id}", headers)
    await cliente.cerrar()
    return resultado

@router.post("/medicos")
async def crear_medico(request_body: dict, authorization: str = Header(None)):
    usuario = obtener_usuario_actual(authorization)
    cliente = ClienteHTTP(configuracion.servicio_medicos_url)
    headers = {"Authorization": authorization} if authorization else {}
    resultado = await cliente.post("/medicos", request_body, headers)
    await cliente.cerrar()
    return resultado

@router.get("/citas")
async def listar_citas(authorization: str = Header(None)):
    usuario = obtener_usuario_actual(authorization)
    cliente = ClienteHTTP(configuracion.servicio_citas_url)
    headers = {"Authorization": authorization} if authorization else {}
    resultado = await cliente.get("/citas", headers)
    await cliente.cerrar()
    return resultado

@router.post("/citas")
async def crear_cita(request_body: dict, authorization: str = Header(None)):
    usuario = obtener_usuario_actual(authorization)
    cliente = ClienteHTTP(configuracion.servicio_citas_url)
    headers = {"Authorization": authorization} if authorization else {}
    resultado = await cliente.post("/citas", request_body, headers)
    await cliente.cerrar()
    return resultado

@router.get("/historiales/{paciente_id}")
async def obtener_historial(paciente_id: str, authorization: str = Header(None)):
    usuario = obtener_usuario_actual(authorization)
    cliente = ClienteHTTP(configuracion.servicio_historiales_url)
    headers = {"Authorization": authorization} if authorization else {}
    resultado = await cliente.get(f"/historiales/paciente/{paciente_id}", headers)
    await cliente.cerrar()
    return resultado

@router.post("/historiales")
async def crear_historial(request_body: dict, authorization: str = Header(None)):
    usuario = obtener_usuario_actual(authorization)
    cliente = ClienteHTTP(configuracion.servicio_historiales_url)
    headers = {"Authorization": authorization} if authorization else {}
    resultado = await cliente.post("/historiales", request_body, headers)
    await cliente.cerrar()
    return resultado

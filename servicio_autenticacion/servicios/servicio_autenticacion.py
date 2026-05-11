from sqlalchemy.orm import Session
from datetime import datetime
from servicio_autenticacion.modelos.usuario import Usuario
from servicio_autenticacion.repositorios.repositorio_usuario import RepositorioUsuario
from servicio_autenticacion.esquemas.usuario_esquema import RegistroRequest, LoginRequest
from servicio_autenticacion.utilidades.seguridad import (
    hash_contraseña, verificar_contraseña, crear_token_acceso,
    verificar_token, crear_token_refresh, extraer_token_de_encabezado
)
from servicio_autenticacion.utilidades.validadores import (
    validar_email, validar_contraseña as validar_contraseña_fortaleza
)
from servicio_autenticacion.utilidades.excepciones import (
    CredencialesInvalidas, EmailYaRegistrado, ContraseñaDebil,
    TokenInvalido, DatosInvalidos
)
from uuid import uuid4

class ServicioAutenticacion:
    def __init__(self, sesion: Session):
        self.sesion = sesion
        self.repositorio = RepositorioUsuario(sesion)
    
    def registrar_usuario(self, datos_registro: RegistroRequest) -> dict:
        if not validar_email(datos_registro.email):
            raise DatosInvalidos("Email inválido")
        
        if self.repositorio.existe_email(datos_registro.email):
            raise EmailYaRegistrado()
        
        es_valida, mensaje_error = validar_contraseña_fortaleza(datos_registro.contraseña)
        if not es_valida:
            raise ContraseñaDebil()
        
        nuevo_usuario = Usuario(
            id=str(uuid4()),
            email=datos_registro.email,
            nombre=datos_registro.nombre,
            contraseña_hash=hash_contraseña(datos_registro.contraseña),
            rol=datos_registro.rol,
            verificado=True
        )
        
        usuario_creado = self.repositorio.crear(nuevo_usuario)
        
        datos_token = {
            "usuario_id": usuario_creado.id,
            "email": usuario_creado.email,
            "nombre": usuario_creado.nombre,
            "rol": usuario_creado.rol
        }
        
        return {
            "exito": True,
            "usuario_id": usuario_creado.id,
            "token_acceso": crear_token_acceso(datos_token),
            "token_refresh": crear_token_refresh(usuario_creado.id)
        }
    
    def autenticar_usuario(self, datos_login: LoginRequest) -> dict:
        usuario = self.repositorio.obtener_por_email(datos_login.email)
        
        if not usuario or not verificar_contraseña(datos_login.contraseña, usuario.contraseña_hash):
            raise CredencialesInvalidas()
        
        if not usuario.activo:
            raise CredencialesInvalidas()
        
        usuario.fecha_ultimo_acceso = datetime.utcnow()
        self.sesion.commit()
        
        datos_token = {
            "usuario_id": usuario.id,
            "email": usuario.email,
            "nombre": usuario.nombre,
            "rol": usuario.rol
        }
        
        return {
            "exito": True,
            "usuario_id": usuario.id,
            "email": usuario.email,
            "nombre": usuario.nombre,
            "rol": usuario.rol,
            "token_acceso": crear_token_acceso(datos_token),
            "token_refresh": crear_token_refresh(usuario.id)
        }
    
    def renovar_token(self, token_refresh: str) -> dict:
        datos_token = verificar_token(token_refresh)
        usuario = self.repositorio.obtener_por_id(datos_token["usuario_id"])
        
        datos_nuevo_token = {
            "usuario_id": usuario.id,
            "email": usuario.email,
            "nombre": usuario.nombre,
            "rol": usuario.rol
        }
        
        return {
            "exito": True,
            "token_acceso": crear_token_acceso(datos_nuevo_token),
            "token_refresh": crear_token_refresh(usuario.id)
        }
    
    def validar_token_actual(self, encabezado_autorizacion: str) -> dict:
        token = extraer_token_de_encabezado(encabezado_autorizacion)
        if not token:
            raise TokenInvalido()
        
        datos = verificar_token(token)
        return datos
    
    def obtener_perfil_usuario(self, usuario_id: str) -> dict:
        usuario = self.repositorio.obtener_por_id(usuario_id)
        return {
            "id": usuario.id,
            "email": usuario.email,
            "nombre": usuario.nombre,
            "rol": usuario.rol,
            "activo": usuario.activo,
            "verificado": usuario.verificado,
            "fecha_creacion": usuario.fecha_creacion
        }
    
    def listar_usuarios(self, limite: int = 100, desplazamiento: int = 0) -> dict:
        usuarios = self.repositorio.obtener_todos(limite, desplazamiento)
        total = self.repositorio.contar_total()
        
        return {
            "usuarios": [
                {
                    "id": u.id,
                    "email": u.email,
                    "nombre": u.nombre,
                    "rol": u.rol,
                    "activo": u.activo
                }
                for u in usuarios
            ],
            "total": total,
            "limite": limite,
            "desplazamiento": desplazamiento
        }

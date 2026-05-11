from sqlalchemy.orm import Session
from uuid import uuid4
from servicio_usuarios.modelos.usuario import Usuario
from servicio_usuarios.repositorios.repositorio_usuario import RepositorioUsuario
from servicio_usuarios.esquemas.usuario_esquema import CrearUsuarioRequest, ActualizarUsuarioRequest
from servicio_usuarios.utilidades.excepciones import DatosInvalidos, EmailYaRegistrado, RecursoNoEncontrado
from servicio_usuarios.utilidades.validadores import validar_email, validar_cedula, validar_nombre

class ServicioUsuarios:
    def __init__(self, sesion: Session):
        self.sesion = sesion
        self.repositorio = RepositorioUsuario(sesion)
    
    def crear_usuario(self, datos: CrearUsuarioRequest) -> dict:
        if not validar_email(datos.email):
            raise DatosInvalidos("Email inválido")
        
        if self.repositorio.existe_email(datos.email):
            raise EmailYaRegistrado()
        
        if not validar_nombre(datos.nombre):
            raise DatosInvalidos("Nombre debe tener entre 3 y 100 caracteres")
        
        if datos.cedula and self.repositorio.existe_cedula(datos.cedula):
            raise DatosInvalidos("Cédula ya registrada")
        
        if datos.cedula and not validar_cedula(datos.cedula):
            raise DatosInvalidos("Cédula inválida")
        
        nuevo_usuario = Usuario(
            id=str(uuid4()),
            email=datos.email,
            nombre=datos.nombre,
            apellido=datos.apellido,
            telefono=datos.telefono,
            cedula=datos.cedula,
            fecha_nacimiento=datos.fecha_nacimiento,
            direccion=datos.direccion,
            ciudad=datos.ciudad,
            genero=datos.genero,
            rol="usuario",
            verificado=True
        )
        
        usuario_creado = self.repositorio.crear(nuevo_usuario)
        
        return {
            "id": usuario_creado.id,
            "email": usuario_creado.email,
            "nombre": usuario_creado.nombre,
            "apellido": usuario_creado.apellido,
            "rol": usuario_creado.rol
        }
    
    def obtener_usuario(self, usuario_id: str) -> dict:
        usuario = self.repositorio.obtener_por_id(usuario_id)
        return self._usuario_a_dict(usuario)
    
    def actualizar_usuario(self, usuario_id: str, datos: ActualizarUsuarioRequest) -> dict:
        datos_dict = datos.model_dump(exclude_unset=True)
        usuario_actualizado = self.repositorio.actualizar(usuario_id, datos_dict)
        return self._usuario_a_dict(usuario_actualizado)
    
    def eliminar_usuario(self, usuario_id: str) -> bool:
        return self.repositorio.eliminar(usuario_id)
    
    def listar_usuarios(self, limite: int = 100, desplazamiento: int = 0) -> dict:
        usuarios = self.repositorio.obtener_todos(limite, desplazamiento)
        total = self.repositorio.contar_total()
        
        return {
            "usuarios": [self._usuario_a_dict(u) for u in usuarios],
            "total": total,
            "limite": limite,
            "desplazamiento": desplazamiento
        }
    
    def listar_por_rol(self, rol: str, limite: int = 100, desplazamiento: int = 0) -> dict:
        usuarios = self.repositorio.obtener_por_rol(rol, limite, desplazamiento)
        total = self.repositorio.contar_por_rol(rol)
        
        return {
            "usuarios": [self._usuario_a_dict(u) for u in usuarios],
            "total": total,
            "limite": limite,
            "desplazamiento": desplazamiento,
            "rol": rol
        }
    
    def buscar_por_email(self, email: str) -> dict:
        usuario = self.repositorio.obtener_por_email(email)
        if not usuario:
            raise RecursoNoEncontrado("Usuario")
        return self._usuario_a_dict(usuario)
    
    def _usuario_a_dict(self, usuario: Usuario) -> dict:
        return {
            "id": usuario.id,
            "email": usuario.email,
            "nombre": usuario.nombre,
            "apellido": usuario.apellido,
            "telefono": usuario.telefono,
            "cedula": usuario.cedula,
            "fecha_nacimiento": usuario.fecha_nacimiento,
            "direccion": usuario.direccion,
            "ciudad": usuario.ciudad,
            "genero": usuario.genero,
            "rol": usuario.rol,
            "activo": usuario.activo,
            "verificado": usuario.verificado,
            "fecha_creacion": usuario.fecha_creacion
        }

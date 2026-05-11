from sqlalchemy.orm import Session
from servicio_usuarios.modelos.usuario import Usuario
from servicio_usuarios.utilidades.excepciones import UsuarioNoEncontrado
from typing import Optional

class RepositorioUsuario:
    def __init__(self, sesion: Session):
        self.sesion = sesion
    
    def crear(self, usuario: Usuario) -> Usuario:
        self.sesion.add(usuario)
        self.sesion.commit()
        self.sesion.refresh(usuario)
        return usuario
    
    def obtener_por_id(self, usuario_id: str) -> Usuario:
        usuario = self.sesion.query(Usuario).filter(Usuario.id == usuario_id).first()
        if not usuario:
            raise UsuarioNoEncontrado()
        return usuario
    
    def obtener_por_email(self, email: str) -> Optional[Usuario]:
        return self.sesion.query(Usuario).filter(Usuario.email == email).first()
    
    def obtener_por_cedula(self, cedula: str) -> Optional[Usuario]:
        return self.sesion.query(Usuario).filter(Usuario.cedula == cedula).first()
    
    def obtener_todos(self, limite: int = 100, desplazamiento: int = 0) -> list:
        return self.sesion.query(Usuario).limit(limite).offset(desplazamiento).all()
    
    def obtener_por_rol(self, rol: str, limite: int = 100, desplazamiento: int = 0) -> list:
        return self.sesion.query(Usuario).filter(Usuario.rol == rol).limit(limite).offset(desplazamiento).all()
    
    def contar_total(self) -> int:
        return self.sesion.query(Usuario).count()
    
    def contar_por_rol(self, rol: str) -> int:
        return self.sesion.query(Usuario).filter(Usuario.rol == rol).count()
    
    def actualizar(self, usuario_id: str, datos: dict) -> Usuario:
        usuario = self.obtener_por_id(usuario_id)
        for clave, valor in datos.items():
            if hasattr(usuario, clave) and valor is not None:
                setattr(usuario, clave, valor)
        self.sesion.commit()
        self.sesion.refresh(usuario)
        return usuario
    
    def eliminar(self, usuario_id: str) -> bool:
        usuario = self.obtener_por_id(usuario_id)
        self.sesion.delete(usuario)
        self.sesion.commit()
        return True
    
    def existe_email(self, email: str) -> bool:
        return self.sesion.query(Usuario).filter(Usuario.email == email).first() is not None
    
    def existe_cedula(self, cedula: str) -> bool:
        if not cedula:
            return False
        return self.sesion.query(Usuario).filter(Usuario.cedula == cedula).first() is not None

from sqlalchemy.orm import Session
from servicio_autenticacion.modelos.usuario import Usuario
from servicio_autenticacion.utilidades.excepciones import UsuarioNoEncontrado
from typing import Optional
from uuid import UUID

class RepositorioUsuario:
    def __init__(self, sesion: Session):
        self.sesion = sesion
    
    def crear(self, usuario_nueva_instancia: Usuario) -> Usuario:
        self.sesion.add(usuario_nueva_instancia)
        self.sesion.commit()
        self.sesion.refresh(usuario_nueva_instancia)
        return usuario_nueva_instancia
    
    def obtener_por_id(self, usuario_id: str) -> Usuario:
        usuario = self.sesion.query(Usuario).filter(Usuario.id == usuario_id).first()
        if not usuario:
            raise UsuarioNoEncontrado()
        return usuario
    
    def obtener_por_email(self, email: str) -> Optional[Usuario]:
        return self.sesion.query(Usuario).filter(Usuario.email == email).first()
    
    def obtener_todos(self, limite: int = 100, desplazamiento: int = 0) -> list:
        return self.sesion.query(Usuario).limit(limite).offset(desplazamiento).all()
    
    def contar_total(self) -> int:
        return self.sesion.query(Usuario).count()
    
    def actualizar(self, usuario_id: str, datos_actualizacion: dict) -> Usuario:
        usuario = self.obtener_por_id(usuario_id)
        for clave, valor in datos_actualizacion.items():
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

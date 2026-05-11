from pydantic import BaseModel, Field, EmailStr
from typing import Optional
from datetime import datetime

class RegistroRequest(BaseModel):
    email: EmailStr
    nombre: str = Field(..., min_length=3, max_length=100)
    contraseña: str = Field(..., min_length=8, max_length=100)
    rol: str = Field(default="usuario", pattern="^(usuario|medico|recepcionista|admin)$")
    
    class Config:
        json_schema_extra = {
            "example": {
                "email": "usuario@clinica.com",
                "nombre": "Juan Pérez",
                "contraseña": "MiContraseña@2024",
                "rol": "usuario"
            }
        }

class LoginRequest(BaseModel):
    email: EmailStr
    contraseña: str
    
    class Config:
        json_schema_extra = {
            "example": {
                "email": "usuario@clinica.com",
                "contraseña": "MiContraseña@2024"
            }
        }

class RefreshTokenRequest(BaseModel):
    refresh_token: str

class UsuarioResponse(BaseModel):
    id: str
    email: str
    nombre: str
    rol: str
    activo: bool
    verificado: bool
    fecha_creacion: datetime
    
    class Config:
        from_attributes = True

class LoginResponse(BaseModel):
    exito: bool
    token_acceso: str
    token_refresh: str
    usuario: UsuarioResponse
    
    class Config:
        json_schema_extra = {
            "example": {
                "exito": True,
                "token_acceso": "eyJ0eXAiOiJKV1QiLCJhbGc...",
                "token_refresh": "eyJ0eXAiOiJKV1QiLCJhbGc...",
                "usuario": {
                    "id": "uuid",
                    "email": "usuario@clinica.com",
                    "nombre": "Juan Pérez",
                    "rol": "usuario",
                    "activo": True,
                    "verificado": True,
                    "fecha_creacion": "2024-05-08T10:00:00"
                }
            }
        }

class TokenResponse(BaseModel):
    exito: bool
    token_acceso: str
    token_refresh: str

import bcrypt
import jwt
from datetime import datetime, timedelta
from typing import Dict, Optional
from .excepciones import TokenInvalido, TokenExpirado
import os

ALGORITMO_JWT = os.getenv("JWT_ALGORITHM", "HS256")
CLAVE_SECRETA = os.getenv("JWT_SECRET_KEY", "clave-secreta-cambiar-en-produccion")
HORAS_EXPIRACION = int(os.getenv("JWT_EXPIRATION_HOURS", "24"))

def hash_contraseña(contraseña: str) -> str:
    sal = bcrypt.gensalt(rounds=12)
    return bcrypt.hashpw(contraseña.encode('utf-8'), sal).decode('utf-8')

def verificar_contraseña(contraseña: str, hash_almacenado: str) -> bool:
    try:
        return bcrypt.checkpw(contraseña.encode('utf-8'), hash_almacenado.encode('utf-8'))
    except Exception:
        return False

def crear_token_acceso(datos_usuario: Dict) -> str:
    carga = datos_usuario.copy()
    ahora = datetime.utcnow()
    carga["iat"] = ahora
    carga["exp"] = ahora + timedelta(hours=HORAS_EXPIRACION)
    
    token = jwt.encode(carga, CLAVE_SECRETA, algorithm=ALGORITMO_JWT)
    return token

def verificar_token(token: str) -> Dict:
    try:
        carga = jwt.decode(token, CLAVE_SECRETA, algorithms=[ALGORITMO_JWT])
        return carga
    except jwt.ExpiredSignatureError:
        raise TokenExpirado()
    except jwt.InvalidTokenError:
        raise TokenInvalido()

def crear_token_refresh(usuario_id: str) -> str:
    carga = {
        "usuario_id": usuario_id,
        "tipo": "refresh",
        "iat": datetime.utcnow(),
        "exp": datetime.utcnow() + timedelta(days=7)
    }
    token = jwt.encode(carga, CLAVE_SECRETA, algorithm=ALGORITMO_JWT)
    return token

def extraer_token_de_encabezado(encabezado_autorizacion: Optional[str]) -> Optional[str]:
    if not encabezado_autorizacion:
        return None
    
    partes = encabezado_autorizacion.split()
    if len(partes) != 2 or partes[0].lower() != "bearer":
        return None
    
    return partes[1]

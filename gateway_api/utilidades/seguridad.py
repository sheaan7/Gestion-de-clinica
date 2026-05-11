import jwt
from typing import Dict, Optional
from gateway_api.config.configuracion import configuracion
from fastapi import HTTPException, status

def verificar_token(token: Optional[str]) -> Dict:
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token no proporcionado")
    
    try:
        partes = token.split()
        if len(partes) != 2 or partes[0].lower() != "bearer":
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Formato de token inválido")
        
        token_real = partes[1]
        carga = jwt.decode(token_real, configuracion.jwt_clave_secreta, algorithms=[configuracion.jwt_algoritmo])
        return carga
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token expirado")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token inválido")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Error validando token")

def obtener_usuario_actual(authorization: Optional[str] = None) -> Dict:
    if not authorization:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="No autorizado")
    return verificar_token(authorization)

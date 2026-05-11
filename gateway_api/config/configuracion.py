from pydantic_settings import BaseSettings
import os

class Configuracion(BaseSettings):
    jwt_clave_secreta: str = os.getenv("JWT_SECRET_KEY", "clave-secreta-cambiar-en-produccion")
    jwt_algoritmo: str = os.getenv("JWT_ALGORITHM", "HS256")
    
    origen_frontend: str = os.getenv("ORIGEN_FRONTEND", "http://localhost:3000")
    debug: bool = os.getenv("DEBUG", "True").lower() == "true"
    entorno: str = os.getenv("ENVIRONMENT", "development")
    
    servicio_autenticacion_url: str = os.getenv("SERVICIO_AUTENTICACION_URL", "http://localhost:8001")
    servicio_usuarios_url: str = os.getenv("SERVICIO_USUARIOS_URL", "http://localhost:8002")
    servicio_pacientes_url: str = os.getenv("SERVICIO_PACIENTES_URL", "http://localhost:8003")
    servicio_medicos_url: str = os.getenv("SERVICIO_MEDICOS_URL", "http://localhost:8004")
    servicio_citas_url: str = os.getenv("SERVICIO_CITAS_URL", "http://localhost:8005")
    servicio_historiales_url: str = os.getenv("SERVICIO_HISTORIALES_URL", "http://localhost:8006")
    
    class Config:
        env_file = ".env"
        case_sensitive = False

configuracion = Configuracion()

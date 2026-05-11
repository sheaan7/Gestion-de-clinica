from pydantic_settings import BaseSettings
import os

class Configuracion(BaseSettings):
    db_host: str = os.getenv("DB_HOST", "mysql")
    db_puerto: int = int(os.getenv("DB_PORT", "3306"))
    db_usuario: str = os.getenv("DB_USER", "root")
    db_contraseña: str = os.getenv("DB_PASSWORD", "root123")
    db_nombre: str = os.getenv("DB_NAME_AUTENTICACION", "auth_db")
    
    jwt_clave_secreta: str = os.getenv("JWT_SECRET_KEY", "clave-secreta-cambiar-en-produccion")
    jwt_algoritmo: str = os.getenv("JWT_ALGORITHM", "HS256")
    jwt_horas_expiracion: int = int(os.getenv("JWT_EXPIRATION_HOURS", "24"))
    
    origen_frontend: str = os.getenv("ORIGEN_FRONTEND", "http://localhost:3000")
    debug: bool = os.getenv("DEBUG", "True").lower() == "true"
    entorno: str = os.getenv("ENVIRONMENT", "development")
    
    @property
    def url_base_datos(self) -> str:
        return f"mysql+pymysql://{self.db_usuario}:{self.db_contraseña}@{self.db_host}:{self.db_puerto}/{self.db_nombre}"
    
    class Config:
        env_file = ".env"
        case_sensitive = False

configuracion = Configuracion()

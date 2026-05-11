from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from typing import Generator
from servicio_pacientes.config.configuracion import configuracion
import time

Base = declarative_base()

motor = None
SesionLocal = None
intentos_conexion = 0
max_intentos = 5

def crear_conexion_bd():
    global motor, SesionLocal, intentos_conexion
    
    try:
        motor = create_engine(
            configuracion.url_base_datos,
            pool_size=10,
            max_overflow=20,
            pool_pre_ping=True,
            echo=configuracion.debug
        )
        
        SesionLocal = sessionmaker(bind=motor, autocommit=False, autoflush=False)
        Base.metadata.create_all(bind=motor)
        intentos_conexion = 0
        return True
    except Exception as e:
        intentos_conexion += 1
        if intentos_conexion < max_intentos:
            print(f"Intento {intentos_conexion}/{max_intentos} fallido. Reintentando en 2s...")
            time.sleep(2)
            return crear_conexion_bd()
        return False

def obtener_bd() -> Generator:
    sesion = SesionLocal()
    try:
        yield sesion
    finally:
        sesion.close()

def cerrar_conexion_bd():
    if motor:
        motor.dispose()

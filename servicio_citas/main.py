from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from servicio_citas.config.configuracion import configuracion
from servicio_citas.base_datos.conexion import crear_conexion_bd, cerrar_conexion_bd
from servicio_citas.rutas import citas

app = FastAPI(
    title="Servicio de Citas",
    description="Servicio de gestión de citas médicas con validación de conflictos horarios",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[configuracion.origen_frontend],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(citas.router)

@app.on_event("startup")
def startup_event():
    """Inicializa la conexión a la base de datos"""
    if crear_conexion_bd():
        print("✅ Conexión a base de datos exitosa")
    else:
        print("❌ No se pudo conectar a la base de datos")

@app.on_event("shutdown")
def shutdown_event():
    """Cierra la conexión a la base de datos"""
    cerrar_conexion_bd()
    print("✅ Conexión a base de datos cerrada")

@app.get("/")
def root():
    """Endpoint raíz"""
    return {
        "servicio": "Servicio de Citas",
        "versión": "1.0.0",
        "estado": "activo",
        "base_datos": configuracion.db_nombre
    }

@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {
        "estado": "healthy",
        "servicio": "servicio_citas",
        "puerto": 8005
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "servicio_citas.main:app",
        host="0.0.0.0",
        port=8005,
        reload=configuracion.debug
    )

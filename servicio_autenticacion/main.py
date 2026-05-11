from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from servicio_autenticacion.config.configuracion import configuracion
from servicio_autenticacion.base_datos.conexion import crear_conexion_bd, cerrar_conexion_bd
from servicio_autenticacion.rutas.autenticacion import router as router_autenticacion

app = FastAPI(
    title="Servicio de Autenticación",
    description="API de autenticación JWT para la clínica",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[configuracion.origen_frontend],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router_autenticacion)

@app.on_event("startup")
async def startup_event():
    if not crear_conexion_bd():
        print("ERROR: No se pudo conectar a la base de datos")
        exit(1)
    print("Base de datos conectada")

@app.on_event("shutdown")
async def shutdown_event():
    cerrar_conexion_bd()
    print("Base de datos desconectada")

@app.get("/health")
async def health_check():
    return {"estado": "ok", "servicio": "autenticacion"}

if __name__ == "__main__":
    import uvicorn
    crear_conexion_bd()
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8001,
        reload=configuracion.debug
    )

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from servicio_historiales.config.configuracion import configuracion
from servicio_historiales.base_datos.conexion import crear_conexion_bd, cerrar_conexion_bd
from servicio_historiales.rutas.historiales import router as router_historiales

app = FastAPI(
    title="Servicio de Historiales Clínicos",
    description="API de historiales clínicos con diagnósticos, tratamientos y observaciones",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[configuracion.origen_frontend],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router_historiales)

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
    return {"estado": "ok", "servicio": "historiales"}

if __name__ == "__main__":
    import uvicorn
    crear_conexion_bd()
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8006,
        reload=configuracion.debug
    )

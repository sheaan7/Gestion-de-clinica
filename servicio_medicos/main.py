from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from servicio_medicos.config.configuracion import configuracion
from servicio_medicos.base_datos.conexion import crear_conexion_bd, cerrar_conexion_bd
from servicio_medicos.rutas.medicos import router as router_medicos

app = FastAPI(title="Servicio de Médicos", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[configuracion.origen_frontend],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(router_medicos)

@app.on_event("startup")
async def startup_event():
    if not crear_conexion_bd():
        print("ERROR: No se pudo conectar a la base de datos")
        exit(1)

@app.on_event("shutdown")
async def shutdown_event():
    cerrar_conexion_bd()

@app.get("/health")
async def health_check():
    return {"estado": "ok", "servicio": "medicos"}

if __name__ == "__main__":
    import uvicorn
    crear_conexion_bd()
    uvicorn.run(app, host="0.0.0.0", port=8004, reload=configuracion.debug)

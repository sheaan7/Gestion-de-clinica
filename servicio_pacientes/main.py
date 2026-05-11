from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from servicio_pacientes.config.configuracion import configuracion
from servicio_pacientes.base_datos.conexion import crear_conexion_bd, cerrar_conexion_bd
from servicio_pacientes.rutas.pacientes import router as router_pacientes

app = FastAPI(title="Servicio de Pacientes", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[configuracion.origen_frontend],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(router_pacientes)

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
    return {"estado": "ok", "servicio": "pacientes"}

if __name__ == "__main__":
    import uvicorn
    crear_conexion_bd()
    uvicorn.run(app, host="0.0.0.0", port=8003, reload=configuracion.debug)

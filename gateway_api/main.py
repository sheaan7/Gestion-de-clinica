from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from gateway_api.config.configuracion import configuracion
from gateway_api.rutas_gateway import router

app = FastAPI(
    title="Gateway API",
    description="API Gateway centralizado para la clínica",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[configuracion.origen_frontend, "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)

@app.get("/health")
async def health_check():
    return {"estado": "ok", "servicio": "gateway"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        reload=configuracion.debug
    )

import httpx
from typing import Any, Dict, Optional

class ClienteHTTP:
    def __init__(self, url_base: str):
        self.url_base = url_base
        self.cliente = httpx.AsyncClient(timeout=10.0)
    
    async def get(self, ruta: str, headers: Optional[Dict] = None) -> Dict[str, Any]:
        try:
            url = f"{self.url_base}{ruta}"
            respuesta = await self.cliente.get(url, headers=headers)
            return respuesta.json()
        except Exception as e:
            return {"exito": False, "error": str(e)}
    
    async def post(self, ruta: str, datos: Dict, headers: Optional[Dict] = None) -> Dict[str, Any]:
        try:
            url = f"{self.url_base}{ruta}"
            respuesta = await self.cliente.post(url, json=datos, headers=headers)
            return respuesta.json()
        except Exception as e:
            return {"exito": False, "error": str(e)}
    
    async def put(self, ruta: str, datos: Dict, headers: Optional[Dict] = None) -> Dict[str, Any]:
        try:
            url = f"{self.url_base}{ruta}"
            respuesta = await self.cliente.put(url, json=datos, headers=headers)
            return respuesta.json()
        except Exception as e:
            return {"exito": False, "error": str(e)}
    
    async def delete(self, ruta: str, headers: Optional[Dict] = None) -> Dict[str, Any]:
        try:
            url = f"{self.url_base}{ruta}"
            respuesta = await self.cliente.delete(url, headers=headers)
            return respuesta.json()
        except Exception as e:
            return {"exito": False, "error": str(e)}
    
    async def cerrar(self):
        await self.cliente.aclose()

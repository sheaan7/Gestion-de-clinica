from typing import Any, Optional

def respuesta_exitosa(datos: Any = None, mensaje: str = "Operación exitosa") -> dict:
    return {
        "exito": True,
        "mensaje": mensaje,
        "datos": datos
    }

def respuesta_error(codigo: str, mensaje: str, detalles: Optional[Any] = None) -> dict:
    respuesta = {
        "exito": False,
        "codigo": codigo,
        "mensaje": mensaje
    }
    if detalles:
        respuesta["detalles"] = detalles
    return respuesta

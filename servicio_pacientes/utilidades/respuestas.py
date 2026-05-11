from typing import Any, Dict, List, Optional

class RespuestaExito:
    def __init__(self, datos: Any = None, mensaje: str = "Operación exitosa", codigo: str = "EXITO"):
        self.exito = True
        self.codigo = codigo
        self.mensaje = mensaje
        self.datos = datos

    def a_dict(self) -> Dict[str, Any]:
        return {
            "exito": self.exito,
            "codigo": self.codigo,
            "mensaje": self.mensaje,
            "datos": self.datos
        }

class RespuestaError:
    def __init__(self, codigo: str, mensaje: str, detalles: Optional[Dict] = None):
        self.exito = False
        self.codigo = codigo
        self.mensaje = mensaje
        self.detalles = detalles or {}

    def a_dict(self) -> Dict[str, Any]:
        return {
            "exito": False,
            "codigo": self.codigo,
            "mensaje": self.mensaje,
            "detalles": self.detalles if self.detalles else None
        }

class RespuestaPaginada:
    def __init__(self, datos: List, total: int, pagina: int, por_pagina: int):
        self.exito = True
        self.datos = datos
        self.total = total
        self.pagina = pagina
        self.por_pagina = por_pagina
        self.total_paginas = (total + por_pagina - 1) // por_pagina

    def a_dict(self) -> Dict[str, Any]:
        return {
            "exito": True,
            "datos": self.datos,
            "paginacion": {
                "total": self.total,
                "pagina": self.pagina,
                "por_pagina": self.por_pagina,
                "total_paginas": self.total_paginas
            }
        }

class ErrorAplicacion(Exception):
    def __init__(self, codigo: str, mensaje: str, estado_http: int = 400):
        self.codigo = codigo
        self.mensaje = mensaje
        self.estado_http = estado_http
        super().__init__(self.mensaje)

class UsuarioNoEncontrado(ErrorAplicacion):
    def __init__(self):
        super().__init__(
            codigo="USUARIO_NO_ENCONTRADO",
            mensaje="El usuario no fue encontrado",
            estado_http=404
        )

class CredencialesInvalidas(ErrorAplicacion):
    def __init__(self):
        super().__init__(
            codigo="CREDENCIALES_INVALIDAS",
            mensaje="Email o contraseña incorrectos",
            estado_http=401
        )

class TokenInvalido(ErrorAplicacion):
    def __init__(self):
        super().__init__(
            codigo="TOKEN_INVALIDO",
            mensaje="El token es inválido o ha expirado",
            estado_http=401
        )

class TokenExpirado(ErrorAplicacion):
    def __init__(self):
        super().__init__(
            codigo="TOKEN_EXPIRADO",
            mensaje="El token ha expirado",
            estado_http=401
        )

class PermisoDenegado(ErrorAplicacion):
    def __init__(self):
        super().__init__(
            codigo="PERMISO_DENEGADO",
            mensaje="No tienes permiso para realizar esta acción",
            estado_http=403
        )

class EmailYaRegistrado(ErrorAplicacion):
    def __init__(self):
        super().__init__(
            codigo="EMAIL_YA_REGISTRADO",
            mensaje="El email ya está registrado",
            estado_http=400
        )

class ContraseñaDebil(ErrorAplicacion):
    def __init__(self):
        super().__init__(
            codigo="CONTRASEÑA_DEBIL",
            mensaje="La contraseña no cumple con los requisitos de seguridad",
            estado_http=400
        )

class DatosInvalidos(ErrorAplicacion):
    def __init__(self, detalles: str = ""):
        super().__init__(
            codigo="DATOS_INVALIDOS",
            mensaje=f"Los datos proporcionados son inválidos: {detalles}",
            estado_http=400
        )

class RecursoNoEncontrado(ErrorAplicacion):
    def __init__(self, tipo: str = "Recurso"):
        super().__init__(
            codigo="RECURSO_NO_ENCONTRADO",
            mensaje=f"{tipo} no encontrado",
            estado_http=404
        )

class ConflictoOperacion(ErrorAplicacion):
    def __init__(self, mensaje: str = "Conflicto en la operación"):
        super().__init__(
            codigo="CONFLICTO_OPERACION",
            mensaje=mensaje,
            estado_http=409
        )

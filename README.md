# Sistema de Gestión Clínica - Arquitectura Microservicios

Sistema integral de gestión clínica basado en Programación Orientada a Objetos (POO) y arquitectura de microservicios. Diseñado para clínicas pequeñas y medianas con capacidad de escalar a grandes volúmenes.

**Stack Tecnológico:**
- Backend: Python 3.12 + FastAPI
- Frontend: HTML5 + CSS3 + JavaScript Vanilla + Bootstrap 5
- Base de datos: MySQL 8.0
- Orquestación: Docker + Docker Compose

## Tabla de Contenidos

1. [Instalación](#instalación)
2. [Estructura del Proyecto](#estructura-del-proyecto)
3. [Conceptos de POO](#conceptos-de-poo-implementados)
4. [Arquitectura](#arquitectura)
5. [APIs y Endpoints](#apis-y-endpoints)
6. [Variables de Entorno](#variables-de-entorno)
7. [Deployment](#deployment)
8. [Troubleshooting](#troubleshooting)

## Instalación

### Requisitos

- Docker 20.10+
- Docker Compose 2.0+
- Git

### Pasos

```bash
git clone <repo-url>
cd Proyecto_fina_POO
cp .env.example .env
docker-compose up --build
```

**URLs de acceso:**
- Frontend: http://localhost:3000
- API Gateway: http://localhost:8000
- PHPMyAdmin: http://localhost:8080 (root / root123)

---

## Estructura del Proyecto

```
Proyecto_fina_POO/
├── gateway_api/                    # Gateway centralizado
│   ├── main.py
│   ├── config/configuracion.py
│   ├── utilidades/seguridad.py
│   └── rutas_gateway.py
│
├── servicio_autenticacion/         # Autenticación JWT y login
│   ├── main.py
│   ├── modelos/usuario.py
│   ├── esquemas/usuario_esquema.py
│   ├── servicios/servicio_autenticacion.py
│   ├── repositorios/repositorio_usuario.py
│   └── rutas/usuario.py
│
├── servicio_usuarios/              # Gestión de perfiles
├── servicio_pacientes/             # Gestión de pacientes
├── servicio_medicos/               # Gestión de médicos y especialidades
├── servicio_citas/                 # Agendar citas
├── servicio_historiales/           # Historial clínico
│
├── frontend_web/                   # Single Page Application
│   ├── index.html
│   ├── js/app.js
│   ├── js/auth.js
│   ├── js/router.js
│   ├── js/api.js
│   ├── js/modulos/
│   └── css/estilos.css
│
├── docker-compose.yml
├── .env.example
└── README.md
```

---

## Conceptos de POO Implementados

### 1. ENCAPSULAMIENTO (Ocultamiento de Datos)

El encapsulamiento protege datos internos mediante atributos privados y métodos públicos controlados. Es el fundamento de la seguridad en POO. Al ocultar los detalles internos de implementación, se garantiza que los datos solo sean accesibles y modificables a través de interfaces controladas.

**Ejemplo en el proyecto:**

```python
from datetime import datetime

class Usuario:
    def __init__(self, email: str, contraseña: str):
        self.email = email
        self._contraseña_hash = None
        self.establecer_contraseña(contraseña)
        self.fecha_creacion = datetime.utcnow()
    
    def establecer_contraseña(self, contraseña: str):
        from passlib.context import CryptContext
        pwd_context = CryptContext(schemes=["bcrypt"])
        self._contraseña_hash = pwd_context.hash(contraseña)
    
    def verificar_contraseña(self, contraseña: str) -> bool:
        from passlib.context import CryptContext
        pwd_context = CryptContext(schemes=["bcrypt"])
        return pwd_context.verify(contraseña, self._contraseña_hash)
    
    @property
    def contraseña_esta_seteada(self) -> bool:
        return self._contraseña_hash is not None
```

En este ejemplo, el atributo `_contraseña_hash` es privado (prefijo `_`). No se puede acceder directamente como `usuario._contraseña_hash = "algo"` desde fuera de la clase. El único camino es a través del método `establecer_contraseña()` que garantiza el hashing correcto.

**Ventajas prácticas:**
- La contraseña nunca se almacena en texto plano
- El algoritmo de hash es consistente en toda la aplicación
- Si en el futuro necesitamos cambiar de bcrypt a Argon2, solo modificamos `establecer_contraseña()`
- No hay forma de "saltarse" la encriptación
- Los tests pueden validar que la contraseña efectivamente se hasheó

**Real-world scenario:** Un desarrollador nuevo intenta `usuario._contraseña_hash = "micontraseña"`. Esto falla silenciosamente o lanza un error porque necesita usar `usuario.establecer_contraseña()`. Eso es seguridad por diseño.

---

### 2. HERENCIA (Reutilización de Código)

La herencia permite que clases derivadas hereden atributos y comportamientos de una clase base, eliminando duplicación. Esto refleja una jerarquía natural del dominio de negocio: todos los usuarios tienen email y nombre, pero un médico tiene especialidad, un administrador tiene permisos, etc.

**Ejemplo en el proyecto:**

```python
from uuid import UUID, uuid4
from typing import List

class UsuarioBase:
    def __init__(self, id: UUID, email: str, nombre: str, rol: str):
        self.id = id
        self.email = email
        self.nombre = nombre
        self.rol = rol
        self.activo = True
    
    def obtener_nombre_completo(self) -> str:
        return self.nombre
    
    def desactivar(self):
        self.activo = False
    
    def obtener_representacion(self) -> dict:
        return {
            "id": str(self.id),
            "email": self.email,
            "nombre": self.nombre,
            "rol": self.rol,
            "activo": self.activo
        }

class Medico(UsuarioBase):
    def __init__(self, id: UUID, email: str, nombre: str, especialidad: str, licencia: str, horario_inicio: str = "08:00", horario_fin: str = "17:00"):
        super().__init__(id, email, nombre, "medico")
        self.especialidad = especialidad
        self.numero_licencia = licencia
        self.horario_inicio = horario_inicio
        self.horario_fin = horario_fin
        self.pacientes_asignados = []
    
    def agregar_paciente(self, paciente_id: UUID):
        if paciente_id not in self.pacientes_asignados:
            self.pacientes_asignados.append(paciente_id)
    
    def puede_atender(self) -> bool:
        return self.activo and self.numero_licencia is not None

class Administrador(UsuarioBase):
    def __init__(self, id: UUID, email: str, nombre: str, permisos: List[str]):
        super().__init__(id, email, nombre, "admin")
        self.permisos = permisos
    
    def tiene_permiso(self, permiso: str) -> bool:
        return permiso in self.permisos
    
    def agregar_permiso(self, permiso: str):
        if permiso not in self.permisos:
            self.permisos.append(permiso)

class Recepcionista(UsuarioBase):
    def __init__(self, id: UUID, email: str, nombre: str, turno: str = "Mañana"):
        super().__init__(id, email, nombre, "recepcionista")
        self.turno = turno
        self.citas_agendadas_hoy = 0
    
    def puede_agendar_citas(self) -> bool:
        return self.activo
    
    def incrementar_citas(self):
        self.citas_agendadas_hoy += 1
```

**Jerarquía visual:**
```
UsuarioBase (clase padre)
├── Medico (heredas id, email, nombre, rol, activo)
├── Administrador (hereda id, email, nombre, rol, activo)
└── Recepcionista (hereda id, email, nombre, rol, activo)

Métodos comunes heredados por todos:
  - obtener_nombre_completo()
  - desactivar()
  - obtener_representacion()
```

**Ventajas concretas en la práctica:**
- Si necesitamos validar que email es único, se hace UNA sola vez en UsuarioBase, no 3 veces
- El método `desactivar()` funciona para Médicos, Administradores y Recepcionistas sin reescribirse
- Un cambio en `obtener_representacion()` afecta automáticamente a todas las subclases
- Nuevos tipos de usuarios (Psicólogo, Especialista) heredan todo automáticamente
- Se evita duplicación: no necesitas escribir `self.id`, `self.email`, `self.nombre` en cada subclase

---

### 3. POLIMORFISMO (Muchas Formas)

El polimorfismo permite que diferentes tipos de objetos respondan al mismo método de formas distintas, sin necesidad de conocer el tipo específico en tiempo de compilación. Esto facilita extensibilidad sin modificar código existente.

**Ejemplo 1: Verificación de permisos polimórfica**

```python
def puede_ver_historial(usuario: UsuarioBase, paciente_id: UUID) -> bool:
    if isinstance(usuario, Administrador):
        return usuario.tiene_permiso("ver_todos_historiales")
    elif isinstance(usuario, Medico):
        return paciente_id in usuario.pacientes_asignados
    elif isinstance(usuario, Recepcionista):
        return False
    else:
        return False

admin = Administrador(uuid4(), "admin@clinica.com", "Admin Clínica", ["ver_todos_historiales", "crear_usuarios"])
medico = Medico(uuid4(), "doc@clinica.com", "Dr. García", "Cardiología", "LIC-123456")
recepcionista = Recepcionista(uuid4(), "recep@clinica.com", "María", "Mañana")

paciente_id = uuid4()
medico.agregar_paciente(paciente_id)

resultado_admin = puede_ver_historial(admin, paciente_id)
resultado_medico = puede_ver_historial(medico, paciente_id)
resultado_recepcionista = puede_ver_historial(recepcionista, paciente_id)
```

**Ejemplo 2: Serialización polimórfica - retorna diferente información según tipo**

```python
def serializar_usuario(usuario: UsuarioBase) -> dict:
    datos_base = usuario.obtener_representacion()
    
    if isinstance(usuario, Medico):
        datos_base["especialidad"] = usuario.especialidad
        datos_base["licencia"] = usuario.numero_licencia
        datos_base["disponible"] = usuario.puede_atender()
        datos_base["pacientes"] = len(usuario.pacientes_asignados)
        datos_base["horario"] = f"{usuario.horario_inicio}-{usuario.horario_fin}"
    elif isinstance(usuario, Administrador):
        datos_base["permisos"] = usuario.permisos
        datos_base["puede_crear_usuarios"] = "crear_usuarios" in usuario.permisos
        datos_base["puede_ver_reportes"] = "ver_reportes" in usuario.permisos
    elif isinstance(usuario, Recepcionista):
        datos_base["turno"] = usuario.turno
        datos_base["citas_hoy"] = usuario.citas_agendadas_hoy
        datos_base["puede_agendar"] = usuario.puede_agendar_citas()
    
    return datos_base

medico = Medico(uuid4(), "doc@clinica.com", "Dr. García", "Cardiología", "LIC-123456")
admin = Administrador(uuid4(), "admin@clinica.com", "Admin Clínica", ["crear_usuarios", "ver_reportes"])

print(serializar_usuario(medico))
print(serializar_usuario(admin))
```

**Por qué es poderoso:** Mañana necesitas agregar tipo de usuario "Psicólogo". Sin cambiar `serializar_usuario()` o `puede_ver_historial()`, solo creas la clase `Psicólogo(UsuarioBase)` y agregas un `elif` en los métodos existentes. Todo el código que ya existe sigue funcionando. El sistema es extensible sin modificar el código cerrado.

---

### 4. ABSTRACCIÓN (Simplicidad e Interfaz Limpia)

La abstracción oculta la complejidad interna, exponiendo solo las operaciones necesarias. El usuario ve una interfaz simple; los detalles complejos quedan escondidos. Ejemplo: un usuario del microservicio de pacientes no necesita saber que internamente se hace una búsqueda en SQL, se cachean resultados y se audita todo.

**Ejemplo 1: Servicio que abstrae la búsqueda**

```python
class RepositorioPacientes:
    def __init__(self, db: Session):
        self.db = db
    
    def obtener_por_id(self, id: UUID) -> dict:
        query = """
            SELECT id, nombre, email, cedula, fecha_nacimiento, telefono
            FROM pacientes 
            WHERE id = %s AND activo = 1
        """
        resultado = self.db.execute(query, [id])
        return resultado[0] if resultado else None

class ServicioPacientes:
    def __init__(self, repo: RepositorioPacientes):
        self.repo = repo
    
    def obtener_paciente(self, id: UUID) -> dict:
        paciente = self.repo.obtener_por_id(id)
        if not paciente:
            raise PacienteNoEncontrado("Paciente no existe")
        
        return {
            "id": str(paciente["id"]),
            "nombre": paciente["nombre"],
            "email": paciente["email"],
            "tipo_documento": paciente["cedula"][:2],
            "vigencia": self.calcular_vigencia(paciente["fecha_nacimiento"])
        }
    
    def calcular_vigencia(self, fecha_nacimiento: str) -> str:
        from datetime import datetime
        edad = (datetime.now() - datetime.fromisoformat(fecha_nacimiento)).days // 365
        if edad > 65:
            return "requiere_revision_especial"
        return "vigente"

async def obtener_paciente_endpoint(id: UUID, usuario: dict = Depends(validar_token)):
    if not usuario.get("puede_ver_pacientes"):
        raise HTTPException(status_code=403)
    servicio = ServicioPacientes(repo)
    return servicio.obtener_paciente(id)
```

En este código, el endpoint no sabe:
- Cómo se ejecuta la query SQL
- Cómo se conecta a la BD
- Cómo se cachea
- Cómo se calcula la vigencia
Solo llama `servicio.obtener_paciente()` y obtiene un diccionario simplificado.

**Ejemplo 2: Abstracción de validación de citas - encapsula lógica compleja**

```python
class ValidadorCita:
    def __init__(self, repo_medicos, repo_citas, repo_pacientes):
        self.repo_medicos = repo_medicos
        self.repo_citas = repo_citas
        self.repo_pacientes = repo_pacientes
    
    def validar_cita_completa(self, cita_data: dict) -> tuple:
        if not self.existe_medico(cita_data["medico_id"]):
            return False, "Médico no existe"
        
        if not self.existe_paciente(cita_data["paciente_id"]):
            return False, "Paciente no existe"
        
        if not self.horario_valido(cita_data["fecha"], cita_data["hora"]):
            return False, "Horario inválido (fuera de jornada)"
        
        if self.existe_conflicto(cita_data["medico_id"], cita_data["fecha"], cita_data["hora"]):
            return False, "Médico ocupado en ese horario"
        
        if self.paciente_tiene_cita_misma_fecha(cita_data["paciente_id"], cita_data["fecha"]):
            return False, "Paciente ya tiene cita ese día"
        
        return True, "Validación exitosa"
    
    def existe_medico(self, medico_id: UUID) -> bool:
        return self.repo_medicos.obtener_por_id(medico_id) is not None
    
    def existe_paciente(self, paciente_id: UUID) -> bool:
        return self.repo_pacientes.obtener_por_id(paciente_id) is not None
    
    def horario_valido(self, fecha: str, hora: str) -> bool:
        horas = hora.split(":")
        return 8 <= int(horas[0]) <= 17
    
    def existe_conflicto(self, medico_id: UUID, fecha: str, hora: str) -> bool:
        return self.repo_citas.obtener_por_medico_fecha_hora(medico_id, fecha, hora) is not None
    
    def paciente_tiene_cita_misma_fecha(self, paciente_id: UUID, fecha: str) -> bool:
        return len(self.repo_citas.obtener_por_paciente_fecha(paciente_id, fecha)) > 0
```

El que usa esta clase solo hace: `es_valida, mensaje = validador.validar_cita_completa(cita_data)`. No necesita saber que internamente hace 5 validaciones diferentes complejas. La abstracción proporciona una interfaz limpia.

---

## Patrones de Diseño

### Repository Pattern
Centraliza el acceso a datos. Cambiar de MySQL a PostgreSQL afecta solo RepositorioPacientes, no el resto.

```python
class RepositorioPacientes:
    def crear(self, paciente: dict) -> UUID:
        pass
    
    def obtener_por_id(self, id: UUID) -> dict:
        pass
    
    def obtener_todos(self, limite: int = 100) -> list:
        pass
    
    def actualizar(self, id: UUID, datos: dict) -> bool:
        pass
    
    def eliminar(self, id: UUID) -> bool:
        pass
```

### Service Layer Pattern
Toda lógica de negocio en una capa. Facilita testing y mantenimiento.

```python
class ServicioCitas:
    def __init__(self, repo: RepositorioCitas):
        self.repo = repo
    
    def agendar_cita(self, medico_id: UUID, paciente_id: UUID, fecha: str) -> dict:
        if not self.validar_disponibilidad(medico_id, fecha):
            raise NoDisponible("Horario ocupado")
        if not self.existe_medico(medico_id):
            raise MedicoNoExiste("Médico no existe")
        cita = self.repo.crear(medico_id, paciente_id, fecha)
        return {"id": cita.id, "estado": "confirmada"}
```

### Dependency Injection
FastAPI inyecta dependencias automáticamente.

```python
from fastapi import Depends, HTTPException

def obtener_usuario_actual(token: str = Header(...)) -> dict:
    usuario = validar_jwt(token)
    if not usuario:
        raise HTTPException(status_code=401)
    return usuario

@router.post("/citas")
async def agendar_cita(
    datos: EsquemaCita,
    usuario: dict = Depends(obtener_usuario_actual),
    db: Session = Depends(obtener_sesion_db)
):
    servicio = ServicioCitas(RepositorioCitas(db))
    return servicio.agendar_cita(datos.medico_id, datos.paciente_id, datos.fecha)
```

---

## Arquitectura

### Microservicios Independientes

Cada servicio:
- Tiene su propia BD MySQL
- Implementa su dominio (Pacientes, Médicos, Citas)
- Expone APIs REST
- Puede escalarse independientemente
- Se puede desplegar por separado

### Comunicación

- **Gateway → Servicios:** REST HTTP
- **Frontend → Gateway:** REST HTTP
- **Autenticación:** JWT token validado en el gateway

### Seguridad

- JWT tokens con rol en payload
- Contraseñas hasheadas con bcrypt
- CORS configurado para frontend
- Validación en cada endpoint

---

## APIs y Endpoints

### Autenticación (servicio_autenticacion:8001)

```
POST   /auth/registro          Registrar nuevo usuario
POST   /auth/login             Iniciar sesión (retorna JWT)
POST   /auth/refresh           Renovar token JWT
```

### Usuarios (servicio_usuarios:8002)

```
GET    /usuarios               Listar usuarios
GET    /usuarios/{id}          Obtener usuario
POST   /usuarios               Crear usuario
PUT    /usuarios/{id}          Actualizar usuario
DELETE /usuarios/{id}          Eliminar usuario
```

### Pacientes (servicio_pacientes:8003)

```
GET    /pacientes              Listar pacientes
GET    /pacientes/{id}         Obtener paciente
POST   /pacientes              Registrar paciente
PUT    /pacientes/{id}         Actualizar paciente
DELETE /pacientes/{id}         Eliminar paciente
GET    /pacientes/buscar       Buscar por nombre/cédula
```

### Médicos (servicio_medicos:8004)

```
GET    /medicos                Listar médicos
GET    /medicos/{id}           Obtener médico
POST   /medicos                Registrar médico
PUT    /medicos/{id}           Actualizar médico
DELETE /medicos/{id}           Eliminar médico
GET    /medicos/especialidad   Listar por especialidad
```

### Citas (servicio_citas:8005)

```
GET    /citas                  Listar citas
GET    /citas/{id}             Obtener cita
POST   /citas                  Agendar cita
PUT    /citas/{id}             Modificar cita
DELETE /citas/{id}             Cancelar cita
GET    /citas/disponibilidad   Horarios disponibles
```

### Historiales (servicio_historiales:8006)

```
GET    /historiales/{paciente} Obtener historial
POST   /historiales/{paciente} Crear registro clínico
PUT    /historiales/{id}       Actualizar registro
DELETE /historiales/{id}       Eliminar registro
```

---

## Variables de Entorno

Copiar `.env.example` a `.env` y configurar:

```env
DB_HOST=mysql
DB_PORT=3306
DB_USER=root
DB_PASSWORD=root123
DB_NAME_AUTENTICACION=auth_db
DB_NAME_USUARIOS=usuarios_db
DB_NAME_PACIENTES=pacientes_db
DB_NAME_MEDICOS=medicos_db
DB_NAME_CITAS=citas_db
DB_NAME_HISTORIALES=historiales_db

JWT_SECRET_KEY=clave-secreta-cambiar-en-produccion
JWT_ALGORITHM=HS256
JWT_EXPIRATION_HOURS=24

ORIGEN_FRONTEND=http://localhost:3000

DEBUG=True
ENVIRONMENT=development
```

**Producción:** Cambiar `JWT_SECRET_KEY`, `DB_PASSWORD` y `ENVIRONMENT=production`.

---

## Deployment

### Local (Docker Compose)

```bash
docker-compose up --build
```

Servicios disponibles:
- Frontend: http://localhost:3000
- Gateway: http://localhost:8000
- PHPMyAdmin: http://localhost:8080

### Producción (VPS/Ubuntu)

1. **Instalar Docker:**
```bash
curl -fsSL https://get.docker.com | sh
sudo usermod -aG docker $USER
```

2. **Clonar repositorio:**
```bash
git clone <repo-url>
cd Proyecto_fina_POO
```

3. **Configurar variables:**
```bash
cp .env.example .env
nano .env
```

Cambiar:
- `JWT_SECRET_KEY` (generar con `openssl rand -hex 32`)
- `DB_PASSWORD` (contraseña fuerte)
- `ENVIRONMENT=production`
- `DEBUG=False`
- `ORIGEN_FRONTEND` (dominio real)

4. **Ejecutar:**
```bash
docker-compose -f docker-compose.yml up -d
```

5. **Verificar:**
```bash
docker-compose ps
docker-compose logs -f gateway_api
```

### En Render / Railway

1. Conectar repositorio Git
2. Crear servicio Web
3. Configurar variables de entorno en panel
4. Deploy automático en cada push

---

## Troubleshooting

### Error: "Connection refused" (MySQL)

**Causa:** MySQL no está listo  
**Solución:**
```bash
docker-compose ps
docker-compose logs mysql
docker-compose restart mysql
```

### Error: "CORS policy blocked"

**Causa:** `ORIGEN_FRONTEND` no coincide con URL del navegador  
**Solución:** Verificar `.env`:
```env
ORIGEN_FRONTEND=http://tudominio.com
```

### Error: "JWT expired"

**Causa:** Token vencido (24h por defecto)  
**Solución:** Frontend debe llamar a `POST /auth/refresh`

### Error: "Invalid credentials"

**Causa:** Usuario/contraseña incorrectos  
**Solución:** Verificar en PHPMyAdmin (http://localhost:8080)

### Servicio no inicia

```bash
docker-compose logs servicio_pacientes
docker-compose build --no-cache servicio_pacientes
docker-compose up servicio_pacientes
```

### Base de datos no se crea

```bash
docker-compose exec mysql mysql -uroot -proot123 -e "SHOW DATABASES;"
docker-compose restart mysql
```

---

## Mantenimiento

### Ver logs

```bash
docker-compose logs servicio_pacientes
docker-compose logs -f gateway_api
docker-compose logs -f frontend_web
```

### Detener servicios

```bash
docker-compose down
```

### Reiniciar servicio

```bash
docker-compose restart servicio_pacientes
```

### Eliminar volúmenes (borra datos)

```bash
docker-compose down -v
```

### Escalar servicio

```bash
docker-compose up -d --scale servicio_pacientes=3
```

---

## Contribución

1. Fork el repositorio
2. Crear rama: `git checkout -b feature/mi-feature`
3. Commit: `git commit -am "Agregar feature"`
4. Push: `git push origin feature/mi-feature`
5. Pull Request

---

## Licencia

MIT - Ver LICENSE

---


**Versión:** 2.0.0  
**Autor:** Jean Pierre Pérez Gomez

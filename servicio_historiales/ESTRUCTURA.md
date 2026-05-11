# Servicio de Historiales Clínicos

## Ubicación
`/home/shean/Documentos/Codigos/Uni_xd/POO/Proyecto_fina_POO/servicio_historiales`

## Configuración
- **Puerto**: 8006
- **Base de Datos**: historiales_db
- **Estructura**: Idéntica a Task 3

## Archivos Python (21 total)

### Configuración (2)
- `config/configuracion.py` - Configuración de puerto, BD y JWT
- `config/__init__.py`

### Base de Datos (2)
- `base_datos/conexion.py` - Conexión SQLAlchemy
- `base_datos/__init__.py`

### Modelos (2)
- `modelos/historial.py` - Modelo SQLAlchemy Historial
- `modelos/__init__.py`

### Esquemas (2)
- `esquemas/historial_esquema.py` - Esquemas Pydantic (Create, Update, Response)
- `esquemas/__init__.py`

### Repositorios (2)
- `repositorios/repositorio_historial.py` - Acceso a datos
- `repositorios/__init__.py`

### Servicios (2)
- `servicios/servicio_historiales.py` - Lógica de negocio
- `servicios/__init__.py`

### Rutas (2)
- `rutas/historiales.py` - Endpoints FastAPI
- `rutas/__init__.py`

### Utilidades (5)
- `utilidades/excepciones.py` - Excepciones personalizadas
- `utilidades/respuestas.py` - Formato de respuestas
- `utilidades/seguridad.py` - JWT y hash
- `utilidades/validadores.py` - Validadores
- `utilidades/__init__.py`

### Principal (1)
- `main.py` - Aplicación FastAPI (puerto 8006)

## Campos del Modelo Historial

- `id` - CHAR(36), UUID, Primary Key
- `paciente_id` - String(36), Index, Not Null
- `medico_id` - String(36), Index, Not Null
- `cita_id` - String(36), Nullable
- `fecha_registro` - DateTime, Default Now()
- `diagnostico` - Text, Not Null
- `tratamiento` - Text, Not Null
- `medicamentos_prescritos` - Text, Nullable
- `observaciones` - Text, Nullable
- `estado_paciente` - String(50), Default "estable" (crítico, grave, estable, mejoría)
- `proxima_cita_recomendada` - String(255), Nullable
- `resultados_laboratorio` - Text, Nullable
- `fecha_creacion` - DateTime, Default Now()
- `fecha_actualizacion` - DateTime, Default Now(), OnUpdate Now()

## Métodos del Repositorio (11)

1. `crear(historial)` - Crear nuevo historial
2. `obtener_por_id(id)` - Obtener por ID
3. `obtener_por_paciente(paciente_id, limite)` - Historiales de un paciente
4. `obtener_por_medico(medico_id, limite)` - Registros de un médico
5. `obtener_por_fecha_rango(fecha_inicio, fecha_fin)` - Rango de fechas
6. `obtener_todos(limite, desplazamiento)` - Listar todos
7. `contar_total()` - Contar total
8. `actualizar(id, datos)` - Actualizar
9. `eliminar(id)` - Eliminar
10. `obtener_ultimo_historial_paciente(paciente_id)` - Último registro

## Métodos del Servicio (11)

1. `crear_registro(datos)` - Crear registro clínico
2. `obtener_historial(id)` - Obtener por ID
3. `actualizar_historial(id, datos)` - Actualizar
4. `eliminar_historial(id)` - Eliminar
5. `listar_historiales(limite, desplazamiento)` - Listar
6. `listar_por_paciente(paciente_id, limite)` - Por paciente
7. `listar_por_medico(medico_id, limite)` - Por médico
8. `listar_por_fecha(fecha_inicio, fecha_fin)` - Por rango de fechas
9. `obtener_historial_completo_paciente(paciente_id)` - Historial completo
10. `validar_datos(datos)` - Validar datos
11. `formatear_historial(historial)` - Formatear respuesta

## Endpoints API (8)

### CRUD Básico
- `POST /historiales` - Crear historial
- `GET /historiales/{id}` - Obtener historial
- `PUT /historiales/{id}` - Actualizar historial
- `DELETE /historiales/{id}` - Eliminar historial
- `GET /historiales` - Listar historiales (con paginación)

### Consultas Especializadas
- `GET /historiales/paciente/{paciente_id}` - Historiales del paciente
- `GET /historiales/medico/{medico_id}` - Registros del médico
- `GET /historiales/paciente/{paciente_id}/completo` - Historial completo

## Archivos Adicionales

- `requirements.txt` - Dependencias (idéntico a autenticacion)
- `Dockerfile` - Container (puerto 8006)

## Validaciones

- Estados válidos: `crítico`, `grave`, `estable`, `mejoría`
- paciente_id y medico_id son obligatorios
- diagnostico y tratamiento son obligatorios
- Fechas en formato ISO 8601

## Respuestas

Todas las respuestas siguen el formato:
```json
{
  "exito": true,
  "codigo": "CODIGO_EVENTO",
  "mensaje": "Descripción",
  "datos": {}
}
```

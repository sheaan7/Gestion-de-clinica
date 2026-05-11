import { ClienteAPI } from '../api-cliente.js';

export class Dashboard {
    constructor() {
        this.cliente = new ClienteAPI();
    }

    render() {
        return `
            <div class="main-content">
                <h2>Dashboard</h2>
                <p id="bienvenida-dashboard">Bienvenido al sistema de gestión clínica</p>

                <div class="dashboard-grid">
                    <div class="stat-card">
                        <p>Pacientes</p>
                        <h3 id="stat-pacientes">--</h3>
                    </div>
                    <div class="stat-card">
                        <p>Médicos</p>
                        <h3 id="stat-medicos">--</h3>
                    </div>
                    <div class="stat-card">
                        <p>Citas</p>
                        <h3 id="stat-citas">--</h3>
                    </div>
                    <div class="stat-card">
                        <p>Usuarios</p>
                        <h3 id="stat-usuarios">--</h3>
                    </div>
                </div>

                <div class="card">
                    <div class="card-header">
                        <h5 class="mb-0">Accesos rápidos</h5>
                    </div>
                    <div class="card-body d-flex flex-wrap gap-2">
                        <button class="btn btn-primary" data-nav="/pacientes">Pacientes</button>
                        <button class="btn btn-primary" data-nav="/medicos">Médicos</button>
                        <button class="btn btn-primary" data-nav="/citas">Citas</button>
                        <button class="btn btn-primary" data-nav="/historiales">Historiales</button>
                    </div>
                </div>

                <div class="card">
                    <div class="card-header">
                        <h5 class="mb-0">Actividad reciente (últimas citas)</h5>
                    </div>
                    <div class="card-body">
                        <div class="table-responsive">
                            <table class="table table-sm">
                                <thead>
                                    <tr>
                                        <th>Fecha</th>
                                        <th>Hora</th>
                                        <th>Paciente</th>
                                        <th>Médico</th>
                                        <th>Estado</th>
                                    </tr>
                                </thead>
                                <tbody id="tabla-actividad-reciente">
                                    <tr><td colspan="5" class="text-muted">Cargando...</td></tr>
                                </tbody>
                            </table>
                        </div>
                    </div>
                </div>
            </div>
        `;
    }

    async montar() {
        this.mostrarBienvenida();
        await this.cargarResumen();
    }

    mostrarBienvenida() {
        const usuarioRaw = localStorage.getItem('usuario');
        if (!usuarioRaw) return;

        try {
            const usuario = JSON.parse(usuarioRaw);
            const nombre = usuario?.nombre || 'usuario';
            const bienvenida = document.getElementById('bienvenida-dashboard');
            if (bienvenida) {
                bienvenida.textContent = `Bienvenido, ${nombre}`;
            }
        } catch {
            // ignore invalid localStorage payload
        }
    }

    async cargarResumen() {
        const endpoints = {
            pacientes: '/pacientes',
            medicos: '/medicos',
            citas: '/citas',
            usuarios: '/usuarios'
        };

        const resultados = await Promise.allSettled(
            Object.values(endpoints).map((ruta) => this.cliente.get(ruta))
        );

        Object.keys(endpoints).forEach((clave, idx) => {
            const stat = document.getElementById(`stat-${clave}`);
            if (!stat) return;

            const resultado = resultados[idx];
            if (resultado.status !== 'fulfilled') {
                stat.textContent = '--';
                return;
            }

            stat.textContent = this.extraerTotal(resultado.value);
        });

        const indiceCitas = Object.keys(endpoints).indexOf('citas');
        const resultadoCitas = resultados[indiceCitas];
        if (resultadoCitas?.status === 'fulfilled') {
            this.renderActividadReciente(resultadoCitas.value);
        } else {
            this.renderActividadReciente(null);
        }
    }

    extraerTotal(respuesta) {
        if (!respuesta) return '--';

        // respuesta con wrapper {exito, datos}
        if (respuesta.exito && respuesta.datos) {
            const datos = respuesta.datos;
            if (typeof datos.total === 'number') return String(datos.total);
            if (Array.isArray(datos)) return String(datos.length);
            const colecciones = ['pacientes', 'medicos', 'citas', 'usuarios', 'historiales'];
            for (const key of colecciones) {
                if (Array.isArray(datos[key])) return String(datos[key].length);
            }
        }

        // respuesta directa sin wrapper (ej. /citas)
        if (typeof respuesta.total === 'number') return String(respuesta.total);
        const colecciones = ['pacientes', 'medicos', 'citas', 'usuarios', 'historiales'];
        for (const key of colecciones) {
            if (Array.isArray(respuesta[key])) return String(respuesta[key].length);
        }

        return '--';
    }

    extraerLista(datos, claves) {
        if (!datos) return [];
        if (Array.isArray(datos)) return datos;
        for (const clave of claves) {
            if (Array.isArray(datos[clave])) return datos[clave];
        }
        return [];
    }

    renderActividadReciente(respuestaCitas) {
        const tabla = document.getElementById('tabla-actividad-reciente');
        if (!tabla) return;

        if (!respuestaCitas) {
            tabla.innerHTML = '<tr><td colspan="5" class="text-danger">No disponible</td></tr>';
            return;
        }

        // soporta wrapper {exito, datos} y respuesta directa
        const datosCitas = respuestaCitas.datos || respuestaCitas;
        const citas = this.extraerLista(datosCitas, ['citas']).slice();
        if (citas.length === 0) {
            tabla.innerHTML = '<tr><td colspan="5" class="text-muted">Sin actividad reciente</td></tr>';
            return;
        }

        const obtenerTimestamp = (cita) => {
            const fecha = cita.fecha_creacion || cita.fecha || cita.fecha_cita || cita.created_at;
            if (!fecha) return 0;
            const valor = new Date(fecha).getTime();
            return Number.isNaN(valor) ? 0 : valor;
        };

        const recientes = citas
            .sort((a, b) => obtenerTimestamp(b) - obtenerTimestamp(a))
            .slice(0, 5);

        tabla.innerHTML = recientes.map((cita) => {
            const fecha = cita.fecha || cita.fecha_cita || cita.fecha_creacion || '-';
            const hora = cita.hora || '-';
            const paciente = cita.paciente_nombre || cita.paciente_id || '-';
            const medico = cita.medico_nombre || cita.medico_id || '-';
            const estado = cita.estado || 'pendiente';
            return `
                <tr>
                    <td>${fecha}</td>
                    <td>${hora}</td>
                    <td>${paciente}</td>
                    <td>${medico}</td>
                    <td>${estado}</td>
                </tr>
            `;
        }).join('');
    }
}

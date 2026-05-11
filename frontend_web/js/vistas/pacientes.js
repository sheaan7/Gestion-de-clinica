import { ClienteAPI } from '../api-cliente.js';

export class Pacientes {
    constructor() {
        this.cliente = new ClienteAPI();
    }

    render() {
        return `
            <div class="main-content">
                <div class="d-flex justify-content-between align-items-center mb-3">
                    <h2>Pacientes</h2>
                    <button class="btn btn-success" id="btn-nuevo-paciente">+ Nuevo paciente</button>
                </div>

                <div id="form-paciente" class="card mb-3" style="display:none">
                    <div class="card-body">
                        <h5 class="card-title" id="form-paciente-titulo">Nuevo paciente</h5>
                        <form id="formulario-paciente">
                            <input type="hidden" id="paciente-id">
                            <div class="row g-2">
                                <div class="col-md-4">
                                    <input type="text" class="form-control" id="paciente-numero-identidad" placeholder="Número de identidad" required>
                                </div>
                                <div class="col-md-4">
                                    <input type="text" class="form-control" id="paciente-nombre" placeholder="Nombre completo" required>
                                </div>
                                <div class="col-md-4">
                                    <input type="email" class="form-control" id="paciente-email" placeholder="Email" required>
                                </div>
                            </div>
                            <div class="mt-2 d-flex gap-2">
                                <button type="submit" class="btn btn-primary" id="btn-guardar-paciente">Guardar</button>
                                <button type="button" class="btn btn-secondary" id="btn-cancelar-paciente">Cancelar</button>
                            </div>
                        </form>
                        <p id="paciente-error" class="text-danger mt-2" style="display:none"></p>
                    </div>
                </div>

                <div class="table-responsive">
                    <table class="table table-hover">
                        <thead>
                            <tr><th>Identidad</th><th>Nombre</th><th>Email</th><th>Acciones</th></tr>
                        </thead>
                        <tbody id="tabla-pacientes">
                            <tr><td colspan="4" class="text-muted">Cargando...</td></tr>
                        </tbody>
                    </table>
                </div>
            </div>`;
    }

    async montar() {
        document.getElementById('btn-nuevo-paciente').addEventListener('click', () => this.mostrarFormulario());
        document.getElementById('btn-cancelar-paciente').addEventListener('click', () => this.ocultarFormulario());
        document.getElementById('formulario-paciente').addEventListener('submit', (e) => { e.preventDefault(); this.guardar(); });
        await this.cargarLista();
    }

    mostrarFormulario(paciente = null) {
        document.getElementById('form-paciente').style.display = '';
        document.getElementById('paciente-error').style.display = 'none';
        if (paciente) {
            document.getElementById('form-paciente-titulo').textContent = 'Editar paciente';
            document.getElementById('paciente-id').value = paciente.id || paciente.paciente_id || '';
            document.getElementById('paciente-numero-identidad').value = paciente.numero_identidad || '';
            document.getElementById('paciente-nombre').value = paciente.nombre || '';
            document.getElementById('paciente-email').value = paciente.email || '';
        } else {
            document.getElementById('form-paciente-titulo').textContent = 'Nuevo paciente';
            document.getElementById('paciente-id').value = '';
            document.getElementById('formulario-paciente').reset();
        }
    }

    ocultarFormulario() {
        document.getElementById('form-paciente').style.display = 'none';
    }

    async guardar() {
        const id = document.getElementById('paciente-id').value;
        const datos = {
            numero_identidad: document.getElementById('paciente-numero-identidad').value.trim(),
            nombre: document.getElementById('paciente-nombre').value.trim(),
            email: document.getElementById('paciente-email').value.trim(),
        };
        const errorEl = document.getElementById('paciente-error');
        try {
            const resp = id
                ? await this.cliente.put(`/pacientes/${id}`, datos)
                : await this.cliente.post('/pacientes', datos);
            if (resp.exito || resp.id || resp.paciente_id || resp.datos) {
                this.ocultarFormulario();
                await this.cargarLista();
            } else {
                errorEl.textContent = resp.mensaje || resp.detail || 'Error al guardar';
                errorEl.style.display = '';
            }
        } catch {
            errorEl.textContent = 'Error de conexión';
            errorEl.style.display = '';
        }
    }

    async cargarLista() {
        const tabla = document.getElementById('tabla-pacientes');
        if (!tabla) return;
        try {
            const resp = await this.cliente.get('/pacientes');
            const lista = resp?.datos?.pacientes || resp?.pacientes || [];
            if (lista.length === 0) {
                tabla.innerHTML = '<tr><td colspan="4" class="text-muted">Sin pacientes registrados</td></tr>';
                return;
            }
            tabla.innerHTML = lista.map(p => `
                <tr>
                    <td>${p.numero_identidad || '-'}</td>
                    <td>${p.nombre || '-'}</td>
                    <td>${p.email || '-'}</td>
                    <td>
                        <button class="btn btn-sm btn-outline-primary me-1" data-editar-paciente='${JSON.stringify(p)}'>Editar</button>
                        <button class="btn btn-sm btn-outline-danger" data-eliminar-paciente="${p.id || p.paciente_id}">Eliminar</button>
                    </td>
                </tr>`).join('');

            tabla.querySelectorAll('[data-editar-paciente]').forEach(btn => {
                btn.addEventListener('click', () => this.mostrarFormulario(JSON.parse(btn.dataset.editarPaciente)));
            });
            tabla.querySelectorAll('[data-eliminar-paciente]').forEach(btn => {
                btn.addEventListener('click', () => this.eliminar(btn.dataset.eliminarPaciente));
            });
        } catch {
            tabla.innerHTML = '<tr><td colspan="4" class="text-danger">Error al cargar pacientes</td></tr>';
        }
    }

    async eliminar(id) {
        if (!confirm('¿Eliminar este paciente?')) return;
        await this.cliente.delete(`/pacientes/${id}`);
        await this.cargarLista();
    }
}

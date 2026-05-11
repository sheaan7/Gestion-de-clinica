import { ClienteAPI } from '../api-cliente.js';

export class Citas {
    constructor() {
        this.cliente = new ClienteAPI();
    }

    render() {
        return `
            <div class="main-content">
                <div class="d-flex justify-content-between align-items-center mb-3">
                    <h2>Citas</h2>
                    <button class="btn btn-success" id="btn-nueva-cita">+ Nueva cita</button>
                </div>

                <div id="form-cita" class="card mb-3" style="display:none">
                    <div class="card-body">
                        <h5 class="card-title">Nueva cita</h5>
                        <form id="formulario-cita">
                            <div class="row g-2">
                                <div class="col-md-6">
                                    <input type="text" class="form-control" id="cita-paciente-id" placeholder="ID del paciente" required>
                                </div>
                                <div class="col-md-6">
                                    <input type="text" class="form-control" id="cita-medico-id" placeholder="ID del médico" required>
                                </div>
                                <div class="col-md-4">
                                    <input type="date" class="form-control" id="cita-fecha" required>
                                </div>
                                <div class="col-md-4">
                                    <input type="time" class="form-control" id="cita-hora-inicio" placeholder="Hora inicio" required>
                                </div>
                                <div class="col-md-4">
                                    <input type="time" class="form-control" id="cita-hora-fin" placeholder="Hora fin" required>
                                </div>
                                <div class="col-12">
                                    <input type="text" class="form-control" id="cita-motivo" placeholder="Motivo de la cita" required>
                                </div>
                            </div>
                            <div class="mt-2 d-flex gap-2">
                                <button type="submit" class="btn btn-primary">Guardar</button>
                                <button type="button" class="btn btn-secondary" id="btn-cancelar-cita">Cancelar</button>
                            </div>
                        </form>
                        <p id="cita-error" class="text-danger mt-2" style="display:none"></p>
                    </div>
                </div>

                <div class="table-responsive">
                    <table class="table table-hover">
                        <thead>
                            <tr><th>Fecha</th><th>Hora</th><th>Paciente</th><th>Médico</th><th>Motivo</th><th>Estado</th><th>Acciones</th></tr>
                        </thead>
                        <tbody id="tabla-citas">
                            <tr><td colspan="7" class="text-muted">Cargando...</td></tr>
                        </tbody>
                    </table>
                </div>
            </div>`;
    }

    async montar() {
        document.getElementById('btn-nueva-cita').addEventListener('click', () => this.mostrarFormulario());
        document.getElementById('btn-cancelar-cita').addEventListener('click', () => this.ocultarFormulario());
        document.getElementById('formulario-cita').addEventListener('submit', (e) => { e.preventDefault(); this.guardar(); });
        await this.cargarLista();
    }

    mostrarFormulario() {
        document.getElementById('form-cita').style.display = '';
        document.getElementById('cita-error').style.display = 'none';
        document.getElementById('formulario-cita').reset();
    }

    ocultarFormulario() {
        document.getElementById('form-cita').style.display = 'none';
    }

    async guardar() {
        const datos = {
            paciente_id: document.getElementById('cita-paciente-id').value.trim(),
            medico_id: document.getElementById('cita-medico-id').value.trim(),
            fecha_cita: document.getElementById('cita-fecha').value,
            hora_inicio: document.getElementById('cita-hora-inicio').value,
            hora_fin: document.getElementById('cita-hora-fin').value,
            motivo: document.getElementById('cita-motivo').value.trim(),
        };
        const errorEl = document.getElementById('cita-error');
        try {
            const resp = await this.cliente.post('/citas', datos);
            if (resp.exito || resp.id || resp.cita_id || resp.datos) {
                this.ocultarFormulario();
                await this.cargarLista();
            } else {
                errorEl.textContent = resp.mensaje || (resp.detail && typeof resp.detail === 'string' ? resp.detail : 'Error al guardar');
                errorEl.style.display = '';
            }
        } catch {
            errorEl.textContent = 'Error de conexión';
            errorEl.style.display = '';
        }
    }

    async cargarLista() {
        const tabla = document.getElementById('tabla-citas');
        if (!tabla) return;
        try {
            const resp = await this.cliente.get('/citas');
            const lista = resp?.datos?.citas || resp?.citas || [];
            if (lista.length === 0) {
                tabla.innerHTML = '<tr><td colspan="7" class="text-muted">Sin citas registradas</td></tr>';
                return;
            }
            tabla.innerHTML = lista.map(c => `
                <tr>
                    <td>${c.fecha_cita || c.fecha || '-'}</td>
                    <td>${c.hora_inicio || c.hora || '-'}</td>
                    <td>${c.paciente_nombre || c.paciente_id || '-'}</td>
                    <td>${c.medico_nombre || c.medico_id || '-'}</td>
                    <td>${c.motivo || '-'}</td>
                    <td>${c.estado || 'pendiente'}</td>
                    <td>
                        <button class="btn btn-sm btn-outline-danger" data-eliminar-cita="${c.id || c.cita_id}">Eliminar</button>
                    </td>
                </tr>`).join('');

            tabla.querySelectorAll('[data-eliminar-cita]').forEach(btn => {
                btn.addEventListener('click', () => this.eliminar(btn.dataset.eliminarCita));
            });
        } catch {
            tabla.innerHTML = '<tr><td colspan="7" class="text-danger">Error al cargar citas</td></tr>';
        }
    }

    async eliminar(id) {
        if (!confirm('¿Eliminar esta cita?')) return;
        await this.cliente.delete(`/citas/${id}`);
        await this.cargarLista();
    }
}

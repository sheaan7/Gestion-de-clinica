import { ClienteAPI } from '../api-cliente.js';

export class Historiales {
    constructor() {
        this.cliente = new ClienteAPI();
    }

    render() {
        return `
            <div class="main-content">
                <div class="d-flex justify-content-between align-items-center mb-3">
                    <h2>Historiales</h2>
                    <button class="btn btn-success" id="btn-nuevo-historial">+ Nuevo historial</button>
                </div>

                <div class="card mb-3">
                    <div class="card-body">
                        <form id="form-buscar-historial" class="d-flex gap-2">
                            <input type="text" class="form-control" id="historial-paciente-id" placeholder="ID del paciente" required>
                            <button type="submit" class="btn btn-primary">Buscar</button>
                        </form>
                    </div>
                </div>

                <div id="form-historial" class="card mb-3" style="display:none">
                    <div class="card-body">
                        <h5 class="card-title">Nuevo historial clínico</h5>
                        <form id="formulario-historial">
                            <div class="row g-2">
                                <div class="col-md-6">
                                    <input type="text" class="form-control" id="h-paciente-id" placeholder="ID del paciente" required>
                                </div>
                                <div class="col-md-6">
                                    <input type="text" class="form-control" id="h-medico-id" placeholder="ID del médico" required>
                                </div>
                                <div class="col-12">
                                    <textarea class="form-control" id="h-diagnostico" rows="2" placeholder="Diagnóstico" required></textarea>
                                </div>
                                <div class="col-12">
                                    <textarea class="form-control" id="h-tratamiento" rows="2" placeholder="Tratamiento" required></textarea>
                                </div>
                                <div class="col-md-4">
                                    <select class="form-select" id="h-estado">
                                        <option value="estable">Estable</option>
                                        <option value="mejoría">Mejoría</option>
                                        <option value="grave">Grave</option>
                                        <option value="crítico">Crítico</option>
                                    </select>
                                </div>
                                <div class="col-md-4">
                                    <input type="text" class="form-control" id="h-medicamentos" placeholder="Medicamentos (opcional)">
                                </div>
                                <div class="col-md-4">
                                    <input type="text" class="form-control" id="h-proxima-cita" placeholder="Próxima cita (opcional)">
                                </div>
                                <div class="col-12">
                                    <textarea class="form-control" id="h-observaciones" rows="2" placeholder="Observaciones (opcional)"></textarea>
                                </div>
                            </div>
                            <div class="mt-2 d-flex gap-2">
                                <button type="submit" class="btn btn-primary">Guardar</button>
                                <button type="button" class="btn btn-secondary" id="btn-cancelar-historial">Cancelar</button>
                            </div>
                        </form>
                        <p id="historial-error" class="text-danger mt-2" style="display:none"></p>
                    </div>
                </div>

                <div id="historiales-container">
                    <p class="text-muted">Ingresa el ID de un paciente para ver sus historiales.</p>
                </div>
            </div>`;
    }

    async montar() {
        document.getElementById('btn-nuevo-historial').addEventListener('click', () => this.mostrarFormulario());
        document.getElementById('btn-cancelar-historial').addEventListener('click', () => this.ocultarFormulario());
        document.getElementById('formulario-historial').addEventListener('submit', (e) => { e.preventDefault(); this.guardar(); });
        document.getElementById('form-buscar-historial').addEventListener('submit', (e) => {
            e.preventDefault();
            const id = document.getElementById('historial-paciente-id').value.trim();
            if (id) this.cargarPorPaciente(id);
        });
    }

    mostrarFormulario() {
        document.getElementById('form-historial').style.display = '';
        document.getElementById('historial-error').style.display = 'none';
        document.getElementById('formulario-historial').reset();
    }

    ocultarFormulario() {
        document.getElementById('form-historial').style.display = 'none';
    }

    async guardar() {
        const datos = {
            paciente_id: document.getElementById('h-paciente-id').value.trim(),
            medico_id: document.getElementById('h-medico-id').value.trim(),
            diagnostico: document.getElementById('h-diagnostico').value.trim(),
            tratamiento: document.getElementById('h-tratamiento').value.trim(),
            estado_paciente: document.getElementById('h-estado').value,
        };
        const medicamentos = document.getElementById('h-medicamentos').value.trim();
        const observaciones = document.getElementById('h-observaciones').value.trim();
        const proximaCita = document.getElementById('h-proxima-cita').value.trim();
        if (medicamentos) datos.medicamentos_prescritos = medicamentos;
        if (observaciones) datos.observaciones = observaciones;
        if (proximaCita) datos.proxima_cita_recomendada = proximaCita;

        const errorEl = document.getElementById('historial-error');
        try {
            const resp = await this.cliente.post('/historiales', datos);
            if (resp.exito || resp.datos) {
                this.ocultarFormulario();
                const pacienteId = document.getElementById('historial-paciente-id').value.trim();
                if (pacienteId) await this.cargarPorPaciente(pacienteId);
            } else {
                errorEl.textContent = resp.mensaje || 'Error al guardar';
                errorEl.style.display = '';
            }
        } catch {
            errorEl.textContent = 'Error de conexión';
            errorEl.style.display = '';
        }
    }

    async cargarPorPaciente(pacienteId) {
        const contenedor = document.getElementById('historiales-container');
        contenedor.innerHTML = '<p class="text-muted">Cargando...</p>';
        try {
            const resp = await this.cliente.get(`/historiales/${pacienteId}`);
            const lista = resp?.datos?.historiales || resp?.historiales || [];
            if (lista.length === 0) {
                contenedor.innerHTML = '<p class="text-muted">Sin historiales para este paciente.</p>';
                return;
            }
            contenedor.innerHTML = `<h6 class="text-muted mb-2">Historiales del paciente (${lista.length})</h6>` +
                lista.map(h => `
                    <div class="card mb-2">
                        <div class="card-body">
                            <div class="d-flex justify-content-between">
                                <span class="badge bg-secondary">${h.estado_paciente || 'estable'}</span>
                                <small class="text-muted">${h.fecha_registro || h.fecha_creacion || ''}</small>
                            </div>
                            <p class="mb-1 mt-2"><strong>Diagnóstico:</strong> ${h.diagnostico || '-'}</p>
                            <p class="mb-1"><strong>Tratamiento:</strong> ${h.tratamiento || '-'}</p>
                            ${h.medicamentos_prescritos ? `<p class="mb-1"><strong>Medicamentos:</strong> ${h.medicamentos_prescritos}</p>` : ''}
                            ${h.observaciones ? `<p class="mb-1"><strong>Observaciones:</strong> ${h.observaciones}</p>` : ''}
                            ${h.proxima_cita_recomendada ? `<p class="mb-0"><strong>Próxima cita:</strong> ${h.proxima_cita_recomendada}</p>` : ''}
                        </div>
                    </div>`).join('');
        } catch {
            contenedor.innerHTML = '<p class="text-danger">Error al cargar historiales.</p>';
        }
    }
}

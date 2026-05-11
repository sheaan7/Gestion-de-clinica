import { ClienteAPI } from '../api-cliente.js';

export class Medicos {
    constructor() {
        this.cliente = new ClienteAPI();
    }

    render() {
        return `
            <div class="main-content">
                <div class="d-flex justify-content-between align-items-center mb-3">
                    <h2>Médicos</h2>
                    <button class="btn btn-success" id="btn-nuevo-medico">+ Nuevo médico</button>
                </div>

                <div id="form-medico" class="card mb-3" style="display:none">
                    <div class="card-body">
                        <h5 class="card-title" id="form-medico-titulo">Nuevo médico</h5>
                        <form id="formulario-medico">
                            <input type="hidden" id="medico-id">
                            <div class="row g-2">
                                <div class="col-md-3">
                                    <input type="text" class="form-control" id="medico-nombre" placeholder="Nombre completo" required>
                                </div>
                                <div class="col-md-3">
                                    <input type="email" class="form-control" id="medico-email" placeholder="Email" required>
                                </div>
                                <div class="col-md-3">
                                    <input type="text" class="form-control" id="medico-especialidad" placeholder="Especialidad" required>
                                </div>
                                <div class="col-md-3">
                                    <input type="text" class="form-control" id="medico-licencia" placeholder="Licencia médica" required>
                                </div>
                            </div>
                            <div class="mt-2 d-flex gap-2">
                                <button type="submit" class="btn btn-primary">Guardar</button>
                                <button type="button" class="btn btn-secondary" id="btn-cancelar-medico">Cancelar</button>
                            </div>
                        </form>
                        <p id="medico-error" class="text-danger mt-2" style="display:none"></p>
                    </div>
                </div>

                <div class="table-responsive">
                    <table class="table table-hover">
                        <thead>
                            <tr><th>Nombre</th><th>Email</th><th>Especialidad</th><th>Licencia</th><th>Acciones</th></tr>
                        </thead>
                        <tbody id="tabla-medicos">
                            <tr><td colspan="5" class="text-muted">Cargando...</td></tr>
                        </tbody>
                    </table>
                </div>
            </div>`;
    }

    async montar() {
        document.getElementById('btn-nuevo-medico').addEventListener('click', () => this.mostrarFormulario());
        document.getElementById('btn-cancelar-medico').addEventListener('click', () => this.ocultarFormulario());
        document.getElementById('formulario-medico').addEventListener('submit', (e) => { e.preventDefault(); this.guardar(); });
        await this.cargarLista();
    }

    mostrarFormulario(medico = null) {
        document.getElementById('form-medico').style.display = '';
        document.getElementById('medico-error').style.display = 'none';
        if (medico) {
            document.getElementById('form-medico-titulo').textContent = 'Editar médico';
            document.getElementById('medico-id').value = medico.id || medico.medico_id || '';
            document.getElementById('medico-nombre').value = medico.nombre || '';
            document.getElementById('medico-email').value = medico.email || '';
            document.getElementById('medico-especialidad').value = medico.especialidad || '';
            document.getElementById('medico-licencia').value = medico.licencia_medica || '';
        } else {
            document.getElementById('form-medico-titulo').textContent = 'Nuevo médico';
            document.getElementById('medico-id').value = '';
            document.getElementById('formulario-medico').reset();
        }
    }

    ocultarFormulario() {
        document.getElementById('form-medico').style.display = 'none';
    }

    async guardar() {
        const id = document.getElementById('medico-id').value;
        const datos = {
            nombre: document.getElementById('medico-nombre').value.trim(),
            email: document.getElementById('medico-email').value.trim(),
            especialidad: document.getElementById('medico-especialidad').value.trim(),
            licencia_medica: document.getElementById('medico-licencia').value.trim(),
        };
        const errorEl = document.getElementById('medico-error');
        try {
            const resp = id
                ? await this.cliente.put(`/medicos/${id}`, datos)
                : await this.cliente.post('/medicos', datos);
            if (resp.exito || resp.id || resp.medico_id || resp.datos) {
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
        const tabla = document.getElementById('tabla-medicos');
        if (!tabla) return;
        try {
            const resp = await this.cliente.get('/medicos');
            const lista = resp?.datos?.medicos || resp?.medicos || [];
            if (lista.length === 0) {
                tabla.innerHTML = '<tr><td colspan="5" class="text-muted">Sin médicos registrados</td></tr>';
                return;
            }
            tabla.innerHTML = lista.map(m => `
                <tr>
                    <td>${m.nombre || '-'}</td>
                    <td>${m.email || '-'}</td>
                    <td>${m.especialidad || '-'}</td>
                    <td>${m.licencia_medica || '-'}</td>
                    <td>
                        <button class="btn btn-sm btn-outline-primary me-1" data-editar-medico='${JSON.stringify(m)}'>Editar</button>
                        <button class="btn btn-sm btn-outline-danger" data-eliminar-medico="${m.id || m.medico_id}">Eliminar</button>
                    </td>
                </tr>`).join('');

            tabla.querySelectorAll('[data-editar-medico]').forEach(btn => {
                btn.addEventListener('click', () => this.mostrarFormulario(JSON.parse(btn.dataset.editarMedico)));
            });
            tabla.querySelectorAll('[data-eliminar-medico]').forEach(btn => {
                btn.addEventListener('click', () => this.eliminar(btn.dataset.eliminarMedico));
            });
        } catch {
            tabla.innerHTML = '<tr><td colspan="5" class="text-danger">Error al cargar médicos</td></tr>';
        }
    }

    async eliminar(id) {
        if (!confirm('¿Eliminar este médico?')) return;
        await this.cliente.delete(`/medicos/${id}`);
        await this.cargarLista();
    }
}

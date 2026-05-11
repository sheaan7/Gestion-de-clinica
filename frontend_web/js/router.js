import { Login } from './vistas/login.js';
import { Dashboard } from './vistas/dashboard.js';
import { Pacientes } from './vistas/pacientes.js';
import { Medicos } from './vistas/medicos.js';
import { Citas } from './vistas/citas.js';
import { Historiales } from './vistas/historiales.js';

export class Router {
    constructor() {
        this.vistas = {
            '/': new Login(),
            '/login': new Login(),
            '/dashboard': new Dashboard(),
            '/pacientes': new Pacientes(),
            '/medicos': new Medicos(),
            '/citas': new Citas(),
            '/historiales': new Historiales()
        };
    }

    navegar(ruta) {
        const vista = this.vistas[ruta];
        if (vista) {
            const app = document.getElementById('app');
            app.innerHTML = vista.render();
            vista.montar();
            window.history.pushState({}, '', ruta);
        }
    }
}

import { Login } from './vistas/login.js';
import { Dashboard } from './vistas/dashboard.js';
import { Pacientes } from './vistas/pacientes.js';
import { Medicos } from './vistas/medicos.js';
import { Citas } from './vistas/citas.js';
import { Historiales } from './vistas/historiales.js';

const FABRICAS = {
    '/': () => new Login(),
    '/login': () => new Login(),
    '/dashboard': () => new Dashboard(),
    '/pacientes': () => new Pacientes(),
    '/medicos': () => new Medicos(),
    '/citas': () => new Citas(),
    '/historiales': () => new Historiales(),
};

export class Router {
    normalizarRuta(ruta) {
        const sinHash = ruta.startsWith('#') ? ruta.slice(1) : ruta;
        if (!sinHash || sinHash === '') return '/';
        return sinHash.startsWith('/') ? sinHash : `/${sinHash}`;
    }

    obtenerRutaActual() {
        const rutaHash = this.normalizarRuta(window.location.hash);
        if (rutaHash !== '/') return rutaHash;
        return this.normalizarRuta(window.location.pathname);
    }

    navegar(ruta) {
        const rutaNormalizada = this.normalizarRuta(ruta);
        const fabrica = FABRICAS[rutaNormalizada];
        if (fabrica) {
            const vista = fabrica();
            const app = document.getElementById('app');
            app.innerHTML = vista.render();
            vista.montar();
            window.location.hash = rutaNormalizada;
        }
    }
}

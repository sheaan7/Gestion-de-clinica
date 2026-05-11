import { Router } from './router.js';
import { Autenticacion } from './autenticacion.js';
import { Utils } from './utils.js';

class App {
    constructor() {
        this.router = new Router();
        this.autenticacion = new Autenticacion();
        this.inicializar();
    }

    inicializar() {
        this.autenticacion.verificarSesion();
        this.configurarEventos();
        this.router.navegar(this.router.obtenerRutaActual());
    }

    configurarEventos() {
        window.addEventListener('hashchange', () => {
            this.router.navegar(this.router.obtenerRutaActual());
        });

        document.addEventListener('click', (e) => {
            if (e.target.matches('[data-nav]')) {
                e.preventDefault();
                const ruta = e.target.dataset.nav;
                this.router.navegar(ruta);
            }
        });

        const btnTema = document.querySelector('#btn-tema');
        if (btnTema) {
            btnTema.addEventListener('click', () => this.cambiarTema());
        }

        const btnSalir = document.querySelector('#btn-salir');
        if (btnSalir) {
            btnSalir.addEventListener('click', () => this.autenticacion.cerrarSesion());
        }
    }

    cambiarTema() {
        document.body.classList.toggle('dark-mode');
        localStorage.setItem('tema', document.body.classList.contains('dark-mode') ? 'oscuro' : 'claro');
    }
}

document.addEventListener('DOMContentLoaded', () => new App());

import { ClienteAPI } from './api-cliente.js';
import { Utils } from './utils.js';

export class Autenticacion {
    constructor() {
        this.cliente = new ClienteAPI();
        this.token = localStorage.getItem('token');
    }

    async login(email, contraseña) {
        try {
            const respuesta = await this.cliente.post('/auth/login', {
                email,
                contraseña
            });

            if (respuesta.exito) {
                localStorage.setItem('token', respuesta.datos.token_acceso);
                localStorage.setItem('usuario', JSON.stringify(respuesta.datos.usuario));
                this.token = respuesta.datos.token_acceso;
                window.location.hash = '/dashboard';
            } else {
                Utils.mostrarError(respuesta.mensaje);
            }
        } catch (error) {
            Utils.mostrarError('Error en el servidor');
        }
    }

    async registro(datos) {
        try {
            const respuesta = await this.cliente.post('/auth/registro', datos);
            if (respuesta.exito) {
                Utils.mostrarExito('Usuario registrado exitosamente');
                return true;
            } else {
                Utils.mostrarError(respuesta.mensaje);
                return false;
            }
        } catch (error) {
            Utils.mostrarError('Error en el registro');
            return false;
        }
    }

    verificarSesion() {
        const token = localStorage.getItem('token');
        const rutaActual = (window.location.hash || '#/').replace('#', '');
        if (token && (rutaActual === '/login' || rutaActual === '/')) {
            window.location.hash = '/dashboard';
            return;
        }
        if (!token && rutaActual !== '/login' && rutaActual !== '/') {
            window.location.hash = '/login';
        }
    }

    cerrarSesion() {
        localStorage.removeItem('token');
        localStorage.removeItem('usuario');
        window.location.hash = '/login';
    }

    obtenerUsuarioActual() {
        const usuarioJson = localStorage.getItem('usuario');
        return usuarioJson ? JSON.parse(usuarioJson) : null;
    }

    tieneRol(rol) {
        const usuario = this.obtenerUsuarioActual();
        return usuario && usuario.rol === rol;
    }
}

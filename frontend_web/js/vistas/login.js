import { Autenticacion } from '../autenticacion.js';
import { Utils } from '../utils.js';

export class Login {
    constructor() {
        this.autenticacion = new Autenticacion();
        this.modoRegistro = false;
    }

    render() {
        return `
            <div class="container mt-5">
                <div class="row justify-content-center">
                    <div class="col-md-6">
                        <div class="card">
                            <div class="card-header text-center">
                                <h3>${this.modoRegistro ? 'Registrarse' : 'Iniciar Sesión'}</h3>
                            </div>
                            <div class="card-body">
                                ${this.modoRegistro ? this.formularioRegistro() : this.formularioLogin()}
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        `;
    }

    formularioLogin() {
        return `
            <form id="form-login">
                <div class="mb-3">
                    <label for="email" class="form-label">Email</label>
                    <input type="email" class="form-control" id="email" required>
                </div>
                <div class="mb-3">
                    <label for="password" class="form-label">Contraseña</label>
                    <input type="password" class="form-control" id="password" required>
                </div>
                <button type="submit" class="btn btn-primary w-100">Ingresar</button>
                <p class="text-center mt-3">
                    ¿No tienes cuenta? <a href="#" id="link-registro">Registrarse</a>
                </p>
            </form>
        `;
    }

    formularioRegistro() {
        return `
            <form id="form-registro">
                <div class="mb-3">
                    <label for="email" class="form-label">Email</label>
                    <input type="email" class="form-control" id="email" required>
                </div>
                <div class="mb-3">
                    <label for="nombre" class="form-label">Nombre</label>
                    <input type="text" class="form-control" id="nombre" required>
                </div>
                <div class="mb-3">
                    <label for="password" class="form-label">Contraseña</label>
                    <input type="password" class="form-control" id="password" required>
                </div>
                <button type="submit" class="btn btn-primary w-100">Registrarse</button>
                <p class="text-center mt-3">
                    ¿Ya tienes cuenta? <a href="#" id="link-login">Inicia sesión</a>
                </p>
            </form>
        `;
    }

    montar() {
        if (this.modoRegistro) {
            document.querySelector('#form-registro').addEventListener('submit', (e) => this.handleRegistro(e));
            document.querySelector('#link-login').addEventListener('click', (e) => {
                e.preventDefault();
                this.modoRegistro = false;
                document.querySelector('.container').innerHTML = this.render();
                this.montar();
            });
        } else {
            document.querySelector('#form-login').addEventListener('submit', (e) => this.handleLogin(e));
            document.querySelector('#link-registro').addEventListener('click', (e) => {
                e.preventDefault();
                this.modoRegistro = true;
                document.querySelector('.container').innerHTML = this.render();
                this.montar();
            });
        }
    }

    async handleLogin(e) {
        e.preventDefault();
        const email = document.querySelector('#email').value;
        const contraseña = document.querySelector('#password').value;
        await this.autenticacion.login(email, contraseña);
    }

    async handleRegistro(e) {
        e.preventDefault();
        const email = document.querySelector('#email').value;
        const nombre = document.querySelector('#nombre').value;
        const contraseña = document.querySelector('#password').value;

        if (contraseña.length < 8) {
            Utils.mostrarError('La contraseña debe tener al menos 8 caracteres');
            return;
        }

        const resultado = await this.autenticacion.registro({ email, nombre, contraseña, rol: 'usuario' });
        if (resultado) {
            this.modoRegistro = false;
            document.querySelector('.container').innerHTML = this.render();
            this.montar();
        }
    }
}

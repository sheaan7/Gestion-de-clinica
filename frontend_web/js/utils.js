export class Utils {
    static mostrarExito(mensaje) {
        this.mostrarAlerta(mensaje, 'success');
    }

    static mostrarError(mensaje) {
        this.mostrarAlerta(mensaje, 'danger');
    }

    static mostrarAlerta(mensaje, tipo = 'info') {
        const alertaDiv = document.createElement('div');
        alertaDiv.className = `alert alert-${tipo} alert-dismissible fade show`;
        alertaDiv.innerHTML = `
            ${mensaje}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        `;
        
        const contenedor = document.querySelector('.main-content') || document.body;
        contenedor.insertBefore(alertaDiv, contenedor.firstChild);

        setTimeout(() => alertaDiv.remove(), 5000);
    }

    static formatearFecha(fecha) {
        return new Date(fecha).toLocaleDateString('es-ES');
    }

    static formatearHora(hora) {
        return hora.substring(0, 5);
    }

    static validarEmail(email) {
        const patron = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return patron.test(email);
    }
}

export class ClienteAPI {
    constructor() {
        this.urlBase = 'http://localhost:8000';
    }

    async peticion(metodo, ruta, datos = null) {
        const opciones = {
            method: metodo,
            headers: {
                'Content-Type': 'application/json'
            }
        };

        const token = localStorage.getItem('token');
        if (token) {
            opciones.headers['Authorization'] = `Bearer ${token}`;
        }

        if (datos) {
            opciones.body = JSON.stringify(datos);
        }

        try {
            const respuesta = await fetch(`${this.urlBase}${ruta}`, opciones);
            return await respuesta.json();
        } catch (error) {
            console.error('Error en petición API:', error);
            throw error;
        }
    }

    get(ruta) {
        return this.peticion('GET', ruta);
    }

    post(ruta, datos) {
        return this.peticion('POST', ruta, datos);
    }

    put(ruta, datos) {
        return this.peticion('PUT', ruta, datos);
    }

    delete(ruta) {
        return this.peticion('DELETE', ruta);
    }
}

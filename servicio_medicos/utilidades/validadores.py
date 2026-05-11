import re
from typing import Tuple
from .excepciones import ContraseñaDebil, DatosInvalidos

def validar_email(email: str) -> bool:
    patron = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(patron, email) is not None

def validar_contraseña(contraseña: str) -> Tuple[bool, str]:
    if len(contraseña) < 8:
        return False, "Mínimo 8 caracteres"
    
    if not re.search(r'[a-z]', contraseña):
        return False, "Debe contener letras minúsculas"
    
    if not re.search(r'[A-Z]', contraseña):
        return False, "Debe contener letras mayúsculas"
    
    if not re.search(r'[0-9]', contraseña):
        return False, "Debe contener números"
    
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', contraseña):
        return False, "Debe contener caracteres especiales"
    
    return True, "Contraseña válida"

def validar_nombre(nombre: str) -> bool:
    return len(nombre.strip()) >= 3 and len(nombre) <= 100

def validar_telefono(telefono: str) -> bool:
    patron = r'^[\d\s\-\+\(\)]{10,}$'
    return re.match(patron, telefono) is not None

def validar_fecha_nacimiento(fecha: str) -> bool:
    patron = r'^\d{4}-\d{2}-\d{2}$'
    return re.match(patron, fecha) is not None

def validar_cedula(cedula: str) -> bool:
    return cedula.isdigit() and 8 <= len(cedula) <= 12

def validar_especialidad(especialidad: str) -> bool:
    especialidades_validas = {
        "Cardiología", "Dermatología", "Oftalmología", "Pediatría",
        "Neurología", "Psiquiatría", "Cirugía General", "Urología",
        "Otorrinolaringología", "Traumatología"
    }
    return especialidad in especialidades_validas

def validar_hora_cita(hora: str) -> bool:
    patron = r'^([0-1][0-9]|2[0-3]):[0-5][0-9]$'
    return re.match(patron, hora) is not None

def validar_licencia_medica(licencia: str) -> bool:
    return len(licencia) >= 5 and len(licencia) <= 50 and licencia.isalnum()

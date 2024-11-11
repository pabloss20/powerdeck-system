from Model.GeneradorLlave import generar_llave
from Model.Usuario import Usuario
from Model.JsonHandler import JsonHandler
from Model.GestorHash import encriptar

import base64

import re

class Administrador(Usuario):
    def __init__(self, nombre, apellido, correo, contrasena, rol_administrador):
        super().__init__(nombre, apellido, correo, contrasena)

        self.validar_datos(nombre, apellido, correo, contrasena)

        self.rol_administrador = rol_administrador
        self.id = generar_llave("U", "R")

        self.jsonhandler = JsonHandler('../../Files/usuarios.json')
        self.registrar_usuario()

    def validar_datos(self, nombre, apellido, correo, contrasena):
        if not all([nombre, apellido, correo, contrasena]):
            raise ValueError("Complete todos los campos.")

        regex_correo = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
        if not re.match(regex_correo, correo):
            raise ValueError("El formato del correo electrónico es inválido.")

        if not (6 <= len(contrasena) <= 16):
            raise ValueError("La contraseña debe tener entre 6 y 16 caracteres.")

        if not any(char.isdigit() for char in contrasena):
            raise ValueError("La contraseña debe incluir al menos un número.")

        if not any(char.isalpha() for char in contrasena):
            raise ValueError("La contraseña debe incluir al menos una letra.")

    def registrar_usuario(self):

        # Verificar si el servidor está disponible antes de registrar
        if not self.verificar_servidor():
            raise ValueError("No se puede registrar el administrador. El servidor no está disponible.")

        contrasena_encriptada = encriptar(self.contrasena)

        # Se convierte bytes a base64
        contrasena_base64 = base64.b64encode(contrasena_encriptada).decode('utf-8')

        info_administrador = {
            "id": self.id,
            "nombre": self.nombre,
            "apellido": self.apellido,
            "correo": self.correo,
            "contrasena": contrasena_base64,
            "tipo_usuario": "administrador",
            "rol_administrador": self.rol_administrador
        }
        try:
            self.jsonhandler.agregar_info(info_administrador)
        except ValueError as e:
            raise e
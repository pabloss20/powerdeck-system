import string
import random
from datetime import datetime
from  JsonHandler import JsonHandler

class Jugador:
    def __init__(self, nombre, apellido, correo, contrasena, confirmar_contrasena, edad, imagen_perfil, pais, nombre_usuario):
        self.validar_datos(nombre, apellido, correo, contrasena, confirmar_contrasena, edad, nombre_usuario)

        self.nombre = nombre
        self.apellido = apellido
        self.correo = correo
        self.contrasena = contrasena
        self.edad = edad
        self.fecha_registro = datetime.now().strftime('%d.%m.%Y %H:%M:%S')
        self.imagen_perfil = imagen_perfil
        self.pais = pais
        self.nombre_usuario = nombre_usuario
        self.id = self.generar_id()

        # Inicializar JsonHandler aquí
        self.jsonhandler = JsonHandler('../Files/jugadores.json')
        self.registrar_jugador()

    def validar_datos(self, nombre, apellido, correo, contrasena, confirmar_contrasena, edad, nombre_usuario):

        if not all([nombre, apellido, correo, contrasena, confirmar_contrasena, edad, nombre_usuario]):
            raise ValueError("Complete todos los campos.")

        if not (contrasena == confirmar_contrasena):
            raise ValueError("Las contraseñas ingresadas no coinciden.")

        regex_correo = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
        if not re.match(regex_correo, correo):
            raise ValueError("El formato del correo electrónico es inválido.")

        if not (6 <= len(contrasena) <= 16):
            raise ValueError("La contraseña debe tener entre 6 y 16 caracteres.")

    def generar_id(self):
        id_jugador_u = ''.join(random.choices(string.ascii_letters + string.digits, k=12))
        id_jugador_a = ''.join(random.choices(string.ascii_letters + string.digits, k=12))
        return f"U-{id_jugador_u}-A-{id_jugador_a}"

    def registrar_jugador(self):
        info_jugador = {
            "id": self.id,
            "nombre_usuario": self.nombre_usuario,
            "nombre": self.nombre,
            "apellido": self.apellido,
            "correo": self.correo,
            "contrasena": self.contrasena,
            "edad": self.edad,
            "fecha_registro": self.fecha_registro,
            "imagen_perfil": self.imagen_perfil,
            "pais": self.pais
        }
        try:
            self.jsonhandler.agregar_info(info_jugador)
        except ValueError as e:
            raise e

    def iniciar_sesion(self, correo, contrasena):
        jugadores = self.jsonhandler.cargar_info()

        for jugador in jugadores:
            if jugador['correo'] == correo and jugador['contrasena'] == contrasena:
                return jugador

        raise ValueError("Credenciales incorrectas.")
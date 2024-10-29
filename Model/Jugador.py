import string
import random
from datetime import datetime
from  JsonHandler import JsonHandler

class Jugador:
    def __init__(self, nombre, apellido, correo, contrasena, fecha_nacimiento, imagen_perfil, pais, nombre_usuario):
        self.validar_datos(nombre, apellido, correo, contrasena, nombre_usuario)

        self.nombre = nombre
        self.apellido = apellido
        self.correo = correo
        self.contrasena = contrasena
        self.fecha_nacimiento = fecha_nacimiento
        self.fecha_registro = datetime.now().strftime('%d.%m.%Y %H:%M:%S')
        self.imagen_perfil = imagen_perfil
        self.pais = pais
        self.nombre_usuario = nombre_usuario
        self.id = self.generar_id()

        # Inicializar JsonHandler aquí
        self.jsonhandler = JsonHandler('../Files/jugadores.json')
        self.registrar_jugador()

    def validar_datos(self, nombre, apellido, correo, contrasena, nombre_usuario):
        if not all([nombre, apellido, correo, contrasena, nombre_usuario]):
            raise ValueError("Complete todos los campos.")

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
            "fecha_nacimiento": self.fecha_nacimiento,
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
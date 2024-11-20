import string
import random
from datetime import datetime
from Model.JsonHandler import JsonHandler
from Model.GeneradorLlave import generar_llave

import re
from enum import Enum

import base64

from Model.Usuario import Usuario

class EstadoJugador(Enum):
    INACTIVO = "Inactivo"
    BUSCANDO_BATALLA = "Buscando Batalla"
    EN_BATALLA = "En Batalla"

# Probabilidades de cada tipo de carta
PROBABILIDADES = {
    "Ultrarara": 0.05,
    "Muy rara": 0.12,
    "Rara": 0.18,
    "Normal": 0.25,
    "Basica": 0.40
}

class Jugador(Usuario):
    def __init__(self, nombre, apellido, correo, contrasena, confirmar_contrasena, nombre_usuario, pais):
        super().__init__(nombre, apellido, correo, contrasena)

        self.validar_datos(nombre, apellido, correo, contrasena, confirmar_contrasena, nombre_usuario, pais)

        self.nombre = nombre
        self.apellido = apellido
        self.correo = correo
        self.contrasena = contrasena
        self.fecha_registro = datetime.now().strftime('%d.%m.%Y %H:%M:%S')
        self.nombre_usuario = nombre_usuario
        self.id = generar_llave("U", "A")
        self.cartas = self.seleccionar_cartas()
        self.estado = EstadoJugador.INACTIVO
        self.pais = pais

        # Inicializar JsonHandler aquí
        self.jsonhandler = JsonHandler('../../Files/usuarios.json')

        contrasena_base64 = self.encriptar_contrasena();

        self.registrar_usuario
        (
        {
            "id": self.id,
            "nombre_usuario": self.nombre_usuario,
            "nombre": self.nombre,
            "apellido": self.apellido,
            "correo": self.correo,
            "contrasena": contrasena_base64,
            "fecha_registro": self.fecha_registro,
            "pais": self.pais,
            "cartas": self.cartas,
            "tipo_usuario": "jugador"
        }
        )

    def validar_datos(self, nombre, apellido, correo, contrasena, confirmar_contrasena, nombre_usuario, pais):
        if not all([nombre, apellido, correo, contrasena, confirmar_contrasena, nombre_usuario, pais]):
            raise ValueError("Complete todos los campos.")

        if not (contrasena == confirmar_contrasena):
            raise ValueError("Las contraseñas ingresadas no coinciden.")

        regex_correo = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
        if not re.match(regex_correo, correo):
            raise ValueError("El formato del correo electrónico es inválido.")

        if not (6 <= len(contrasena) <= 16):
            raise ValueError("La contraseña debe tener entre 6 y 16 caracteres.")

        if not any(char.isdigit() for char in contrasena):
            raise ValueError("La contraseña debe incluir al menos un número.")

        if not any(char.isalpha() for char in contrasena):
            raise ValueError("La contraseña debe incluir al menos una letra.")

    # Actualiza el estado del jugador durante el juego
    def actualizar_estado(self, estado: EstadoJugador):
        if isinstance(estado, EstadoJugador):
            self.estado = estado
            print(f"Estado del jugador '{self.nombre}' actualizado a: {self.estado.value}")
        else:
            raise ValueError("El nuevo estado debe ser una instancia de EstadoJugador.")

    # Método para seleccionar cartas basado en las probabilidades definidas
    def seleccionar_cartas(self, cantidad = 3, archivo_json='../../Files/cartas.json'):
        # Cargar las cartas desde el archivo JSON
        json_handler = JsonHandler(archivo_json)
        cartas = json_handler.cargar_cartas()

        seleccionadas = []
        cartas_disponibles = cartas.copy()  # Se copian las cartas para evitar repeticiones

        while len(seleccionadas) < cantidad and cartas_disponibles:
            carta = random.choices(
                cartas_disponibles,
                weights=[PROBABILIDADES.get(carta["tipo_carta"], 0) for carta in cartas_disponibles],
                k=1
            )[0]

            seleccionadas.append(carta)
            cartas_disponibles.remove(carta)  # Eliminar la carta seleccionada para evitar repeticiones

        return seleccionadas

    # Método para mostrar el resultado de las cartas seleccionadas
    def mostrar_cartas_seleccionadas(self):
        print("Cartas seleccionadas y sus rarezas con probabilidades:")
        for carta in self.cartas:
            rareza = carta['tipo_carta']
            probabilidad = PROBABILIDADES.get(rareza, 0) * 100
            print(f"{carta['nombre_personaje']} - Rareza: {rareza} - Probabilidad: {probabilidad:.2f}%")
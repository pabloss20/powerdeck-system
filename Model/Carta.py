import random
import string
import json
from datetime import datetime
import os
from enum import Enum

class Raza(Enum):
    """
    Enum class `Raza` represents various races within a fantasy setting.

    Attributes:
        HUMANO: Represents the human race.
        ELFICO: Represents the elvish race.
        ENANO: Represents the dwarvish race.
        ORCO: Represents the orc race.
        DRAGÓN: Represents the dragon race.
        MÁGICO: Represents magical beings.
        BESTIA: Represents beast-like creatures.
        DEMONIO: Represents the demon race.
    """
    HUMANO = "Humano"
    ELFICO = "Élfico"
    ENANO = "Enano"
    ORCO = "Orco"
    DRAGÓN = "Dragón"
    MÁGICO = "Mágico"
    BESTIA = "Bestia"
    DEMONIO = "Demonio"
class Tipo_de_Carta(Enum):
    ULTRA_RARA = "Ultra-Rara"
    MUY_RARA = "Muy-Rara"
    RARA = "Rara"
    NORMAL = "Normal"
    BASICA = "Basica"

class Atributos:
    """
        Clase Atributos

        Representa una colección de atributos con valores validados entre -100 y 100.

        Métodos
        -------
        __init__(self, poder, velocidad, magia, defensa, inteligencia, altura,
                 fuerza, agilidad, salto, resistencia, flexibilidad, explosividad,
                 carisma, habilidad, balance, sabiduría, suerte, coordinacion,
                 amabilidad, lealtad, disciplina, liderazgo, prudencia,
                 confianza, percepcion, valentía)
            Inicializa una instancia de la clase Atributos.

        poder_total(self)
            Devuelve la suma de todos los atributos.
    """
    def __init__(self, poder, velocidad, magia, defensa, inteligencia, altura,
                 fuerza, agilidad, salto, resistencia, flexibilidad, explosividad,
                 carisma, habilidad, balance, sabiduría, suerte, coordinacion,
                 amabilidad, lealtad, disciplina, liderazgo, prudencia,
                 confianza, percepcion, valentía):
        # Validación de atributos
        for attr in [poder, velocidad, magia, defensa, inteligencia, altura,
                     fuerza, agilidad, salto, resistencia, flexibilidad,
                     explosividad, carisma, habilidad, balance, sabiduría,
                     suerte, coordinacion, amabilidad, lealtad, disciplina,
                     liderazgo, prudencia, confianza, percepcion, valentía]:
            if not (-100 <= attr <= 100):
                raise ValueError("Los atributos deben estar entre -100 y 100.")

        self.poder = poder
        self.velocidad = velocidad
        self.magia = magia
        self.defensa = defensa
        self.inteligencia = inteligencia
        self.altura = altura
        self.fuerza = fuerza
        self.agilidad = agilidad
        self.salto = salto
        self.resistencia = resistencia
        self.flexibilidad = flexibilidad
        self.explosividad = explosividad
        self.carisma = carisma
        self.habilidad = habilidad
        self.balance = balance
        self.sabiduría = sabiduría
        self.suerte = suerte
        self.coordinacion = coordinacion
        self.amabilidad = amabilidad
        self.lealtad = lealtad
        self.disciplina = disciplina
        self.liderazgo = liderazgo
        self.prudencia = prudencia
        self.confianza = confianza
        self.percepcion = percepcion
        self.valentía = valentía

    @property
    def poder_total(self):
        return sum(vars(self).values())


class Carta:
    """
    class Carta:
        """
    def __init__(self, nombre_personaje, descripcion, nombre_variante, raza, imagen, tipo_carta,
                 turno_poder, bonus_poder, atributos, archivo_json='cartas.json'):
        """
        :param nombre_personaje: Nombre del personaje asociado a la carta.
        :param descripcion: Descripción de la carta y del personaje.
        :param nombre_variante: Nombre de la variante de la carta, si existe.
        :param raza: Raza del personaje.
        :param tipo_carta: Tipo de la carta (e.g., común, rara, legendaria).
        :param turno_poder: Turno en el que se puede usar el poder especial de la carta.
        :param bonus_poder: Bonus de poder especial que otorga la carta.
        :param atributos: Atributos detallados de la carta.
        :param archivo_json: Nombre del archivo JSON donde se almacenan las cartas (por defecto 'cartas.json').
        """
        # Inicializar el archivo JSON
        self.archivo_json = archivo_json
        self.cartas = self.cargar_cartas()

        # Validación de datos
        self.validar_datos(nombre_personaje, descripcion, nombre_variante, raza, tipo_carta,
                           turno_poder, bonus_poder, atributos)

        # Inicialización de atributos
        self.nombre_personaje = nombre_personaje
        self.descripcion = descripcion
        self.nombre_variante = nombre_variante
        self.fecha_creacion = datetime.now()
        self.fecha_modificacion = self.fecha_creacion
        self.raza = raza.value
        self.imagen = imagen  # Asignar imagen en el futuro
        self.tipo_carta = tipo_carta.value
        self.activa_en_juego = True
        self.activa_en_sobres = True
        self.turno_poder = turno_poder
        self.bonus_poder = bonus_poder
        self.atributos = atributos
        self.es_variante = self.determine_variation()
        self.llave = self.generar_llave()

        # Agregar la nueva carta al JSON
        self.agregar_carta()

    def cargar_cartas(self):
        """
        Loads cards from a JSON file if it exists and contains data.

        :return: A list of cards loaded from the JSON file, or an empty list if the file doesn't exist or is empty.
        """
        if os.path.exists(self.archivo_json):
            with open(self.archivo_json, 'r') as f:
                contenido = f.read()
                if contenido:  # Verifica que el contenido no esté vacío
                    return json.loads(contenido)
        return []

    def validar_datos(self, nombre_personaje, descripcion, nombre_variante, raza, tipo_carta,
                      turno_poder, bonus_poder, atributos):
        """
        :param nombre_personaje: Nombre del personaje de la carta.
        :param descripcion: Descripción de la carta.
        :param nombre_variante: Variante del nombre del personaje de la carta.
        :param raza: Raza del personaje de la carta.
        :param tipo_carta: Tipo de la carta.
        :param turno_poder: Turno en el que se puede usar el poder especial.
        :param bonus_poder: Bonus adicional del poder especial.
        :param atributos: Conjunto de atributos del personaje de la carta.
        :return: No devuelve ningún valor, pero puede lanzar ValueError si la validación falla.
        """
        # Comprobar si todos los datos están presentes
        if not all([nombre_personaje, descripcion, nombre_variante, raza.value, tipo_carta, atributos]):
            raise ValueError("Todos los datos son requeridos. Por favor, ingrese toda la información e intente de nuevo.")

        # Comprobar si la combinación de nombre de variante y nombre de personaje ya existe
        for carta in self.cartas:
            if (carta['nombre_personaje'] == nombre_personaje and
                carta['nombre_variante'] == nombre_variante):
                raise ValueError("No se puede crear una carta duplicada con el mismo nombre de personaje y variante.")

        # Validar datos numéricos
        for attr in atributos.__dict__.values():
            if not (-100 <= attr <= 100):
                raise ValueError("Los atributos deben estar entre -100 y 100.")

        if not (0 <= turno_poder <= 100):
            raise ValueError("El Turno de Poder debe estar entre 0 y 100.")
        if not (0 <= bonus_poder <= 100):
            raise ValueError("El Bonus de Poder debe estar entre 0 y 100.")

        # Validación de nombre y descripción
        if not (5 <= len(nombre_personaje) <= 30):
            raise ValueError("El nombre del personaje debe tener entre 5 y 30 caracteres.")
        if not (5 <= len(nombre_variante) <= 30):
            raise ValueError("El nombre de variante debe tener entre 5 y 30 caracteres.")
        if len(descripcion) > 1000:
            raise ValueError("La descripción no puede exceder los 1000 caracteres.")

    def determine_variation(self):
        """
        :return: True if any card in the list has the same 'nombre_personaje' as the object's 'nombre_personaje', otherwise False
        """
        return any(carta['nombre_personaje'] == self.nombre_personaje for carta in self.cartas)

    def generar_llave(self):
        """
        Generates a unique key composed of two parts: a card identifier and a variant identifier.

        Each identifier is a random combination of 12 alphanumeric characters.

        :return: A string in the format "C-<card_identifier>-V-<variant_identifier>"
        """
        identificador_carta = ''.join(random.choices(string.ascii_letters + string.digits, k=12))
        identificador_variante = ''.join(random.choices(string.ascii_letters + string.digits, k=12))
        return f"C-{identificador_carta}-V-{identificador_variante}"

    def agregar_carta(self):
        """
        Agrega una nueva carta a la lista de cartas y actualiza el archivo JSON con la información.

        :return: None
        """
        nueva_carta = {
            'nombre_personaje': self.nombre_personaje,
            'descripcion': self.descripcion,
            'nombre_variante': self.nombre_variante,
            'fecha_creacion': self.fecha_creacion.isoformat(),
            'fecha_modificacion': self.fecha_modificacion.isoformat(),
            'raza': self.raza,
            'imagen': self.imagen,
            'tipo_carta': self.tipo_carta,
            'activa_en_juego': self.activa_en_juego,
            'activa_en_sobres': self.activa_en_sobres,
            'turno_poder': self.turno_poder,
            'bonus_poder': self.bonus_poder,
            'atributos': vars(self.atributos),
            'llave': self.llave,
            'es_variante': self.es_variante
        }
        self.cartas.append(nueva_carta)
        with open(self.archivo_json, 'w') as f:
            json.dump(self.cartas, f, indent=4)


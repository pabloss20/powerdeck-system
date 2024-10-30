import datetime
import random
import string
import json
import os
from collections import Counter

class Mazo:
    def __init__(self, nombre, max_cartas=15, filepath="../../Files/mazo.json", fileCartas="../../Files/cartas.json"):
        # Validación de longitud del nombre
        if not (5 <= len(nombre) <= 30):
            raise ValueError("El nombre del mazo debe tener entre 5 y 30 caracteres.")

        # Verificar si el nombre ya existe en el archivo JSON
        if self._nombre_mazo_existe(nombre, filepath):
            raise ValueError(f"Ya existe un mazo con el nombre '{nombre}', no se puede duplicar.")

        self.nombre = nombre
        self.fecha_creacion = datetime.datetime.now()
        self.fecha_modificacion = self.fecha_creacion
        self.cartas = set()
        self.max_cartas = max_cartas
        self.keyid = self._generate_unique_key()
        self.filepath = filepath
        self.fileCartas = fileCartas

    def _generate_unique_key(self):
        key = f"D-{''.join(random.choices(string.ascii_letters + string.digits, k=12))}"
        return key

    def _nombre_mazo_existe(self, nombre, filepath):
        if os.path.exists(filepath):
            with open(filepath, "r") as file:
                mazos = json.load(file)
                return any(mazo["nombre"] == nombre for mazo in mazos)
        return False

    def agregar_carta(self, carta_id):
        if len(self.cartas) >= self.max_cartas:
            raise ValueError("El mazo ya contiene el número máximo de cartas permitido.")
        if carta_id in self.cartas:
            raise ValueError("No se pueden agregar cartas repetidas al mazo.")

        self.cartas.add(carta_id)
        self.fecha_modificacion = datetime.datetime.now()

    def verificar_rareza(self):
        # Cargar las cartas del archivo JSON
        with open(self.fileCartas, "r") as file:
            cartas_data = json.load(file)

        # Crear un diccionario con rarezas solo de las cartas en el mazo
        rarezas = {carta["llave"]: carta["tipo_carta"] for carta in cartas_data if carta["llave"] in self.cartas}

        # Contar rarezas de las cartas en el mazo
        rareza_contador = Counter(rarezas.values())
        total_cartas = len(self.cartas)

        # Definir límites por rareza
        limites = {
            "Ultra rara": 0.15,
            "Rara": 0.20,
            "Normal": 0.60,
            "Básica": 1.00
        }

        # Verificar que cada rareza cumpla con su límite
        for rareza, limite in limites.items():
            max_cartas = int(total_cartas * limite)
            if rareza_contador[rareza] > max_cartas:
                raise ValueError(f"El mazo excede el límite de cartas para rareza '{rareza}' ({limite * 100}%).")

        return True

    def es_valido(self):
        if len(self.cartas) != self.max_cartas:
            raise ValueError("El mazo debe contener exactamente 15 cartas únicas.")
        return True

    def to_dict(self):
        # Convierte los datos del mazo a un diccionario
        return {
            "nombre": self.nombre,
            "fecha_creacion": self.fecha_creacion.isoformat(),
            "fecha_modificacion": self.fecha_modificacion.isoformat(),
            "cartas": list(self.cartas),
            "max_cartas": self.max_cartas,
            "keyid": self.keyid
        }

    def guardar_en_json(self):
        data = self.to_dict()
        if os.path.exists(self.filepath):
            # Si el archivo ya existe, cargar el contenido existente y agregar el nuevo mazo
            with open(self.filepath, "r") as file:
                all_data = json.load(file)
        else:
            all_data = []

        all_data.append(data)

        with open(self.filepath, "w") as file:
            json.dump(all_data, file, indent=4)

# Ejemplo de uso
try:
    mi_mazo = Mazo("MazoEjemplo")
    # Agregar cartas con ids simulados
    for i in range(15):
        mi_mazo.agregar_carta(f"carta-{i}")
    mi_mazo.es_valido()
    mi_mazo.guardar_en_json()
    mi_mazo.verificar_rareza()
    print("Mazo creado y guardado en JSON correctamente:", mi_mazo.keyid)
except ValueError as e:
    print("Error al crear el mazo:", e)

import json
import os
from Model import GestorHash


class JsonHandler:
    def __init__(self, archivo):
        self.archivo = archivo
        if not os.path.exists(self.archivo):
            with open(self.archivo, 'w') as file:
                json.dump([], file)

    def guardar_info(self, info):
        """Guardar la información actualizada en el archivo JSON."""
        with open(self.archivo, 'w') as file:
            json.dump(info, file, indent=4)

    def cargar_cartas(self):
        if not os.path.exists(self.archivo) or os.path.getsize(self.archivo) == 0:
            return []

        with open(self.archivo, 'r') as file:
            try:
                return json.load(file)
            except json.JSONDecodeError:
                return []

    def cargar_info(self):
        """Cargar la información del archivo JSON, asegurándose de que sea la estructura correcta."""
        if not os.path.exists(self.archivo) or os.path.getsize(self.archivo) == 0:
            return {"administradores": [], "jugadores": []}

        with open(self.archivo, 'r') as file:
            try:
                data = json.load(file)
                return data if isinstance(data, dict) else {"administradores": [], "jugadores": []}
            except json.JSONDecodeError:
                return {"administradores": [], "jugadores": []}

    def agregar_info(self, info):
        data_json = self.cargar_info()

        # Se agrega un nuevo usuario
        if 'nombre_usuario' in info:  # Solo los jugadores tienen un nombre de usuario

            if any(jugador['correo'] == info.get('correo') for jugador in data_json["jugadores"]):
                raise ValueError('El correo ingresado se encuentra registrado.')

            if any(jugador['nombre_usuario'] == info.get('nombre_usuario') for jugador in data_json["jugadores"]):
                raise ValueError('El nombre de usuario ingresado se encuentra registrado.')

            data_json["jugadores"].append(info)

        else:
            if any(admin['correo'] == info.get('correo') for admin in data_json["administradores"]):
                raise ValueError('El correo ingresado se encuentra registrado.')
            data_json["administradores"].append(info)

        self.guardar_info(data_json)

    def obtener_cartas_de_jugador(self, identificador, por_id=True):
        """
        Retorna las cartas de un jugador específico.

        Args:
        - identificador (str): El ID o nombre de usuario del jugador.
        - por_id (bool): True para buscar por ID, False para buscar por nombre de usuario.

        Returns:
        - list: Lista de cartas del jugador. Si no se encuentra, retorna una lista vacía.
        """
        data = self.cargar_info()
        for jugador in data.get("jugadores", []):
            if (por_id and jugador["id"] == identificador) or (not por_id and jugador["nombre_usuario"] == identificador):
                return jugador.get("cartas", [])
        return []

    def cargar_datos(self):
        """
        Carga la lista de mazos desde el archivo JSON.
        """
        if not os.path.exists(self.archivo) or os.path.getsize(self.archivo) == 0:
            return []

        with open(self.archivo, 'r') as file:
            try:
                data = json.load(file)
                return data if isinstance(data, list) else []
            except json.JSONDecodeError:
                return []

    def obtener_id_por_correo_y_contrasena(self, correo):
        """
        Retorna el ID de un jugador si el correo y la contraseña coinciden.

        Args:
        - correo (str): El correo del jugador.
        - contrasena (str): La contraseña en texto plano para verificar.

        Returns:
        - str: ID del jugador si se encuentra y las credenciales son correctas.
        - None: Si no se encuentra o las credenciales no coinciden.
        """
        data = self.cargar_info()

        for jugador in data.get("jugadores", []):
            if jugador["correo"] == correo:
                return jugador["id"]
        return None

    def obtener_mazos_de_jugador(self, id_jugador):
        """
        Retorna los mazos de un jugador específico.

        Args:
        - id_jugador (str): El ID del jugador.

        Returns:
        - list: Lista de mazos asociados al jugador. Si no se encuentran mazos, retorna una lista vacía.
        """
        data = self.cargar_datos()

        # Buscar los mazos asociados al ID del jugador
        mazos_jugador = [mazo for mazo in data if mazo.get("jugador") == id_jugador]

        return mazos_jugador
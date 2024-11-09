import json
import os

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

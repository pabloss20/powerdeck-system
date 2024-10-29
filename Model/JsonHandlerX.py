import json
import os

class JsonHandlerX:
    def __init__(self, archivo):
        self.archivo = archivo
        if not os.path.exists(self.archivo):
            with open(self.archivo, 'w') as file:
                json.dump([], file)

    def guardar_info(self, info):
        with open(self.archivo, 'w') as file:
            json.dump(info, file)

    def cargar_info(self):
        if not os.path.exists(self.archivo) or os.path.getsize(self.archivo) == 0:
            return []

        with open(self.archivo, 'r') as file:
            try:
                return json.load(file)
            except json.JSONDecodeError:
                return []

    def agregar_info(self, info):
        info_json = self.cargar_info()

        if any(entry['correo'] == info.get('correo') for entry in info_json):
            raise ValueError('El correo ingresado se encuentra registrado')

        if any(entry['nombre_usuario'] == info.get('nombre_usuario') for entry in info_json):
            raise ValueError('El nombre de usuario se encuentra en uso')

        info_json.append(info)
        self.guardar_info(info_json)
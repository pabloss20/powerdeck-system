from Model.GestorHash import verificar
from Model.JsonHandler import JsonHandler
import base64

class Usuario:

    def __init__(self, nombre, apellido, correo, contrasena):
        self.nombre = nombre
        self.apellido = apellido
        self.correo = correo
        self.contrasena = contrasena

    def registrar_usuario(self):
        raise NotImplementedError("Este método debe ser sobrescrito en las subclases.")

    def validar_usuario(self):
        raise NotImplementedError("Este método debe ser sobrescrito en las subclases.")

    def validar_datos(self):
        raise NotImplementedError("Este método debe ser sobrescrito en las subclases.")

    @staticmethod
    def iniciar_sesion(correo, contrasena):
        if not all([correo, contrasena]):
            raise ValueError("Complete todos los campos.")

        # Se carga el archivo de usuarios
        jsonhandler = JsonHandler('../../Files/usuarios.json')
        usuarios = jsonhandler.cargar_info()

        # Se busca al usuario por correo en administradores y jugadores
        usuario = next((u for u in usuarios["administradores"] if u['correo'] == correo), None)

        if not usuario:
            usuario = next((u for u in usuarios["jugadores"] if u['correo'] == correo), None)

        if not usuario:
            return "Usuario no encontrado"

        # Se obtiene el hash de la contraseña en formato base64
        contrasena_base64 = usuario['contrasena']

        # Se decodifica el hash de base64 a bytes
        contrasena_hash = base64.b64decode(contrasena_base64)

        # Se verifica la contraseña
        if verificar(contrasena, contrasena_hash):  # Contrasena_hash es de tipo bytes
            if usuario['tipo_usuario'] == 'administrador':
                if usuario['rol_administrador'] == 'juego':
                    return 2
                elif usuario['rol_administrador'] == 'reportes':
                    return 3
            return 1  # Jugador
        else:
            return "Contraseña incorrecta"


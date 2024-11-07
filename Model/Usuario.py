from Model.GestorHash import verificar  # Importa la función de verificación
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
        # Cargar el archivo de usuarios
        jsonhandler = JsonHandler('../Files/usuarios.json')
        usuarios = jsonhandler.cargar_info()

        # Buscar al usuario por correo
        usuario = next((u for u in usuarios if u['correo'] == correo), None)
        if not usuario:
            return "Usuario no encontrado"

        # Decodificar el hash de la contraseña desde base64
        contrasena_hash_base64 = usuario['contrasena']
        contrasena_hash = base64.b64decode(contrasena_hash_base64.encode('utf-8'))

        # Verificar la contraseña
        if verificar(contrasena, contrasena_hash):
            if usuario['tipo_usuario'] == 'administrador':
                if usuario['rol_administrador'] == 'juego':
                    return 2
                elif usuario['rol_administrador'] == 'reportes':
                    return 3
            return 1
        else:
            return "Contraseña incorrecta"

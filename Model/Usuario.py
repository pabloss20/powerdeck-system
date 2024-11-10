from Model.GestorHash import verificar
from Model.JsonHandler import JsonHandler
import base64
import socket
import json

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

    def conectar_servidor(self, host='127.0.0.1', puerto=12345):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as conexion:
                conexion.connect((host, puerto))
                print("Conexión exitosa con el servidor.")

                # Envía un mensaje de notificación de conexión exitosa
                mensaje = json.dumps({"accion": "inicio_sesion_exitoso", "correo": self.correo})
                conexion.sendall(mensaje.encode('utf-8'))

                # Espera la respuesta del servidor
                respuesta = conexion.recv(1024).decode('utf-8')
                datos = json.loads(respuesta)

                if datos.get("estado") == "confirmado":
                    print("Servidor ha confirmado el inicio de sesión exitoso.")
                    return True
                else:
                    print("El servidor no pudo confirmar el inicio de sesión.")
                    return False
        except ConnectionRefusedError:
            # Se lanza una excepción pero no se detiene la ejecución
            raise RuntimeError("No se pudo conectar al servidor. Verifique que esté iniciado.")
        except Exception as e:
            # Captura otras excepciones y lanza un error controlado sin detener el flujo
            raise RuntimeError(f"Ocurrió un error al intentar conectarse: {e}")

    # Método para verificar si el servidor está activo antes de registrar
    def verificar_servidor(self):
        try:
            return self.conectar_servidor()
        except RuntimeError:
            print("No se puede registrar el usuario. El servidor no está disponible.")
            return False

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
            usuario_obj = Usuario(usuario["nombre"], usuario["apellido"], correo, contrasena)
            try:
                if usuario_obj.conectar_servidor():
                    if usuario['tipo_usuario'] == 'administrador':
                        if usuario['rol_administrador'] == 'juego':
                            return 2
                        elif usuario['rol_administrador'] == 'reportes':
                            return 3
                    return 1
            except RuntimeError:
                raise ValueError("Servidor no iniciado o sistema caido. Inténtalo más tarde.")
        else:
            return "Contraseña incorrecta"


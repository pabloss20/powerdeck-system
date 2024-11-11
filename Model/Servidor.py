import socket
import threading
import json

class Servidor:
    def __init__(self, host='127.0.0.1', puerto=12345):
        self.host = host
        self.puerto = puerto
        self.servidor_iniciado = False
        self.server_socket = None

    def iniciar_servidor(self):
        # Configuración del socket
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.puerto))
        self.server_socket.listen()

        # Flag de inicio
        print(f"Servidor iniciado en {self.host} : {self.puerto}")
        self.servidor_iniciado = True

        # Bucle principal para aceptar conexiones
        while True:
            conexion, direccion = self.server_socket.accept()
            print(f"Conectado por {direccion}")
            hilo = threading.Thread(target=self.manejar_cliente, args=(conexion, direccion))
            hilo.start()

    def manejar_cliente(self, conexion, direccion):
        while True:
            try:
                datos = conexion.recv(1024)
                if not datos:
                    break

                # Procesa el mensaje JSON recibido
                mensaje = json.loads(datos.decode('utf-8'))
                if mensaje["accion"] == "inicio_sesion_exitoso":
                    print(f"Inicio de sesión exitoso para el usuario: {mensaje['correo']}")
                    respuesta = {"estado": "confirmado"}
                    conexion.sendall(json.dumps(respuesta).encode('utf-8'))
            except:
                break

        # Cierra la conexión con el cliente
        conexion.close()

    def detener_servidor(self):
        if self.server_socket:
            self.server_socket.close()
            print("Servidor detenido.")
        self.servidor_iniciado = False

if __name__ == "__main__":
    servidor = Servidor()
    try:
        servidor.iniciar_servidor()
    except KeyboardInterrupt:
        print("\nDeteniendo el servidor...")
        servidor.detener_servidor()
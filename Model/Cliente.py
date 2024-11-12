import socket
import threading
import json


class Cliente:
    def __init__(self, host='18.216.53.39', puerto=12345):
        self.host = host
        self.puerto = puerto
        self.cliente_socket = None

    def conectar(self):
        try:
            self.cliente_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.cliente_socket.connect((self.host, self.puerto))
            print(f"Conectado al servidor en {self.host}:{self.puerto}")

            # Inicia un hilo para recibir mensajes
            threading.Thread(target=self.recibir_mensajes).start()

        except Exception as e:
            print(f"Error al conectar: {e}")

    def enviar_mensaje(self, mensaje):
        try:
            self.cliente_socket.sendall(json.dumps(mensaje).encode('utf-8'))
        except Exception as e:
            print(f"Error al enviar el mensaje: {e}")

    def recibir_mensajes(self):
        while True:
            try:
                datos = self.cliente_socket.recv(1024).decode('utf-8')
                if datos:
                    print(f"Mensaje recibido: {datos}")
            except Exception as e:
                print(f"Error al recibir mensaje: {e}")
                break

    def cerrar_conexion(self):
        if self.cliente_socket:
            self.cliente_socket.close()
            print("Conexión cerrada.")


if __name__ == "__main__":
    cliente = Cliente(host='18.216.53.39', puerto=12345)
    cliente.conectar()

    # Enviar un mensaje de ejemplo
    mensaje = {
        "accion": "mensaje",
        "contenido": "Hola desde el cliente"
    }
    cliente.enviar_mensaje(mensaje)

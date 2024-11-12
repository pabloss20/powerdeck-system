import socket
import threading
import json

class Servidor:
    def __init__(self, host='0.0.0.0', puerto=12345):
        self.host = host
        self.puerto = puerto
        self.servidor_iniciado = False
        self.server_socket = None
        self.clientes = []  # Lista para almacenar las conexiones de los clientes

    def iniciar_servidor(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.puerto))
        self.server_socket.listen()

        print(f"Servidor iniciado en {self.host} : {self.puerto}")
        self.servidor_iniciado = True

        while True:
            conexion, direccion = self.server_socket.accept()
            print(f"Conectado por {direccion}")
            self.clientes.append(conexion)
            hilo = threading.Thread(target=self.manejar_cliente, args=(conexion, direccion))
            hilo.start()

    def manejar_cliente(self, conexion, direccion):
        while True:
            try:
                datos = conexion.recv(1024)
                if not datos:
                    break

                mensaje = json.loads(datos.decode('utf-8'))
                print(f"Mensaje recibido de {direccion}: {mensaje}")

                if mensaje["accion"] == "inicio_sesion_exitoso":
                    print(f"Inicio de sesión exitoso para el usuario: {mensaje['correo']}")
                    respuesta = {"estado": "confirmado"}
                    conexion.sendall(json.dumps(respuesta).encode('utf-8'))

                # Reenvía el mensaje a otros clientes
                for cliente in self.clientes:
                    if cliente != conexion:  # No enviar al mismo cliente
                        try:
                            cliente.sendall(json.dumps(mensaje).encode('utf-8'))
                        except:
                            self.clientes.remove(cliente)
                            cliente.close()

            except Exception as e:
                print(f"Error manejando cliente {direccion}: {e}")
                break

        conexion.close()
        self.clientes.remove(conexion)
        print(f"Cliente {direccion} desconectado")

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
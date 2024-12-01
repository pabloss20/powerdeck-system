import socket
import threading
import json

class Servidor:
    def __init__(self, host='127.0.0.1', puerto=54321):
        self.host = host
        self.puerto = puerto
        self.servidor_iniciado = False
        self.server_socket = None
        self.clientes = []  # Lista para almacenar las conexiones de los clientes
        self.esperando_partida = []  # Lista para los clientes que buscan partida

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
            conexion, _ = self.server_socket.accept()
            print(f"Cliente conectado")
            hilo = threading.Thread(target=self.manejar_cliente, args=(conexion,))
            hilo.start()

    def manejar_cliente(self, conexion):
        while True:
            try:
                datos = conexion.recv(1024)
                if not datos:
                    break

                # Decodificar los datos recibidos en formato JSON
                mensaje = json.loads(datos.decode('utf-8'))
                print(f"Mensaje recibido: {mensaje}")

                # Acción de inicio de sesión
                if mensaje["accion"] == "inicio_sesion_exitoso":
                    print(f"Inicio de sesión exitoso para el usuario: {mensaje['correo']}")
                    respuesta = {"estado": "confirmado"}
                    conexion.sendall(json.dumps(respuesta).encode('utf-8'))

                # Acción de buscar partida
                if mensaje["accion"] == "buscar_partida":
                    id_jugador = mensaje["id_jugador"]  # Recibir la ID del jugador
                    print(f"Cliente {id_jugador} está buscando partida.")

                    # Agregar cliente a la lista de esperando
                    self.esperando_partida.append((conexion, id_jugador))

                    # Verificar si hay otro cliente esperando para emparejar
                    if len(self.esperando_partida) >= 2:
                        # Emparejar los dos primeros clientes
                        cliente1, id_jugador1 = self.esperando_partida.pop(0)
                        cliente2, id_jugador2 = self.esperando_partida.pop(0)

                        # Asegurarse de que no se emparejan dos clientes iguales
                        if id_jugador1 != id_jugador2:
                            # Enviar mensaje de emparejamiento a ambos clientes
                            mensaje_emparejamiento1 = {
                                "accion": "emparejados",
                                "mensaje": "¡Partida encontrada!",
                                "oponente_id": id_jugador2
                            }
                            mensaje_emparejamiento2 = {
                                "accion": "emparejados",
                                "mensaje": "¡Partida encontrada!",
                                "oponente_id": id_jugador1
                            }
                            cliente1.sendall(json.dumps(mensaje_emparejamiento1).encode('utf-8'))
                            cliente2.sendall(json.dumps(mensaje_emparejamiento2).encode('utf-8'))

                            # Actualizar la lista de clientes emparejados
                            print(f"Clientes emparejados: {id_jugador1} y {id_jugador2}")
                        else:
                            # Si los dos jugadores son el mismo, se agregan de vuelta a la lista de espera
                            print("Intento de emparejamiento con el mismo cliente, esperando otro.")
                            self.esperando_partida.append((cliente1, id_jugador1))

            except Exception as e:
                print(f"Error manejando cliente: {e}")
                break

        conexion.close()

    def detener_servidor(self):
        if self.server_socket:
            self.server_socket.close()
            print("Servidor detenido.")
        self.servidor_iniciado = False

# Ejecución del servidor
if __name__ == "__main__":
    servidor = Servidor()
    try:
        servidor.iniciar_servidor()
    except KeyboardInterrupt:
        print("\nDeteniendo el servidor...")
        servidor.detener_servidor()

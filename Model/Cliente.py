import socket
import threading
import json

class Cliente:
    def __init__(self, host="127.0.0.1", puerto=54321):
        self.host = host
        self.puerto = puerto
        self.cliente_socket = None
        self.respuesta_partida = None  # Almacena la respuesta de buscar partida

    def conectar(self):
        try:
            self.cliente_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.cliente_socket.connect((self.host, self.puerto))
            print(f"Conectado al servidor en {self.host}:{self.puerto}")

            # Inicia un hilo para recibir mensajes
            threading.Thread(target=self.recibir_mensajes).start()

        except Exception as e:
            print(f"Error al conectar: {e}")
            return e

    def enviar_mensaje(self, mensaje):
        try:
            self.cliente_socket.sendall(json.dumps(mensaje).encode('utf-8'))
        except Exception as e:
            print(f"Error al enviar el mensaje: {e}")
            return e

    def buscar_partida(self, id_jugador, n_mazo):
        # Enviar la solicitud de buscar partida con la ID del jugador
        mensaje = {
            "accion": "buscar_partida",
            "id_jugador": id_jugador,
            "mazo_rival" : n_mazo
        }

        self.enviar_mensaje(mensaje)
        print("Buscando partida...")

        # Aquí crearás un hilo para recibir la respuesta
        threading.Thread(target=self.recibir_mensajes).start()
    def seleccionar_carta(self, id_jugador, n_carta):
        mensaje = {
            "accion": "seleccionando_cartas",
            "id_jugador": id_jugador,
            "carta_seleccionada": n_carta
        }
        self.enviar_mensaje(mensaje)
        print("Seleccionando carta...")
        threading.Thread(target=self.recibir_mensajes).start()

    def recibir_mensajes(self):
        while True:
            try:
                datos = self.cliente_socket.recv(1024).decode('utf-8')
                if datos:
                    mensaje = json.loads(datos)
                    print(f"Mensaje recibido: {mensaje}")

                    if mensaje.get("accion") == "emparejados":
                        self.respuesta_partida = mensaje
                        print(f"Partida encontrada: {mensaje['mensaje']}")
                        break
                    if mensaje.get("accion") == "cartas_seleccionadas":
                        self.respuesta_partida = mensaje
                        print(f"evaluando ganador")
                        break

            except Exception as e:
                print(f"Error al recibir mensaje: {e}")
                break

    def cerrar_conexion(self):
        if self.cliente_socket:
            self.cliente_socket.close()
            print("Conexión cerrada.")


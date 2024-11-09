import socket
import threading
import json

servidor_iniciado = False

def manejar_cliente(conexion, direccion):

    # Flag
    print(f"Conectado por {direccion}")

    while True:
        try:
            datos = conexion.recv(1024)

            if not datos:
                break
            mensaje = json.loads(datos.decode('utf-8'))

            if mensaje["accion"] == "buscar_partida":
                respuesta = {"estado": "encontrado"}
                conexion.sendall(json.dumps(respuesta).encode('utf-8'))
        except:
            break

    conexion.close()

def iniciar_servidor(host = '127.0.0.1', puerto = 12345):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, puerto))
    server.listen()

    #Flag
    print(f"Servidor iniciado en {host} : {puerto}")

    servidor_iniciado = True

    while True:
        conexion, direccion = server.accept()
        hilo = threading.Thread(target=manejar_cliente, args=(conexion, direccion))
        hilo.start()
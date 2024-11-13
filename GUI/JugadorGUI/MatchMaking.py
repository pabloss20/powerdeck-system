import pygame
import sys
from Model.Cliente import Cliente
import threading
import CrearMazo
import time
import math  # Importamos el módulo math

buscando_partida = False
oponente_id = ""
pantalla_actual = ""

def main(id_jugador):
    global buscando_partida, oponente_id, pantalla_actual

    # Inicializar pygame
    pygame.init()

    # Colores
    NEGRO = (0, 0, 0)
    BLANCO = (255, 255, 255)
    AZUL_CLARO = (100, 149, 237)

    # Dimensiones de la ventana
    ANCHO = 1820  # Cambiado a 1820
    ALTO = 900  # Cambiado a 900

    # Crear la ventana
    ventana = pygame.display.set_mode((ANCHO, ALTO), pygame.RESIZABLE)
    pygame.display.set_caption('Power Deck App')

    # Fuentes
    fuente_texto = pygame.font.Font(None, 50)

    # Variables de estado
    pantalla_actual = "principal"

    # Variables para controlar el estado de la animación y el juego
    buscando_partida = False  # Para saber si estamos esperando una respuesta
    mensaje = None  # Almacena el mensaje de respuesta

    # Función para mostrar la pantalla de "Rival encontrado"
    def pantalla_rival_encontrado(ventana, oponente_id):
        ventana.fill(NEGRO)  # Limpiar la pantalla
        texto = f"¡Rival encontrado! Jugador: {oponente_id}"
        renderizado_texto = fuente_texto.render(texto, True, BLANCO)
        rect_texto = renderizado_texto.get_rect(center=(ANCHO // 2, ALTO // 2))
        ventana.blit(renderizado_texto, rect_texto)
        pygame.display.update()

    # Función para mostrar el círculo giratorio
    def mostrar_animacion_giratoria(ventana):
        """ Dibuja un círculo giratorio en el centro de la pantalla """
        clock = pygame.time.Clock()  # Para controlar la velocidad de la animación
        tiempo_inicial = time.time()

        while buscando_partida:
            ventana.fill(NEGRO)  # Limpiar la pantalla
            tiempo_transcurrido = time.time() - tiempo_inicial

            # Calcular el ángulo de rotación
            angulo = (tiempo_transcurrido * 100) % 360  # Girar continuamente
            centro = (ANCHO // 2, ALTO // 2)

            # Dibujar el círculo giratorio (simulando la animación)
            pygame.draw.circle(ventana, BLANCO, centro, 50, 5)  # Círculo estático en el centro

            # Dibujar la línea que girará
            longitud = 40  # Longitud de la línea
            radianes = math.radians(angulo)  # Usar math.radians() para convertir grados a radianes
            x_final = centro[0] + longitud * math.cos(radianes)
            y_final = centro[1] + longitud * math.sin(radianes)

            # Dibuja la línea giratoria
            pygame.draw.line(ventana, BLANCO, centro, (x_final, y_final), 5)

            pygame.display.update()  # Actualizar pantalla
            clock.tick(60)  # Controlar la velocidad de la animación

    # Función para dibujar un botón
    def dibujar_boton(texto, x, y, ancho, alto, color_borde, color_fondo, ventana):
        pygame.draw.rect(ventana, color_fondo, (x, y, ancho, alto))
        pygame.draw.rect(ventana, color_borde, (x, y, ancho, alto), 5)
        ventana.blit(texto, (x + (ancho - texto.get_width()) // 2, y + (alto - texto.get_height()) // 2))

    # Función para mostrar la pantalla principal
    def pantalla_principal():
        # Dibujar título
        titulo = fuente_texto.render('POWER DECK', True, BLANCO)
        subtitulo = fuente_texto.render('EMPAREJAMIENTO', True, BLANCO)
        ventana.blit(titulo, ((ANCHO - titulo.get_width()) // 2, 50))
        ventana.blit(subtitulo, ((ANCHO - subtitulo.get_width()) // 2, 130))

        # Dibujar botones
        dibujar_boton(fuente_texto.render('Album', True, BLANCO),
                      ANCHO // 2 - 150, ALTO // 2 - 100, 300, 100, AZUL_CLARO, NEGRO, ventana)

        dibujar_boton(fuente_texto.render('Buscar Partida', True, BLANCO),
                      ANCHO // 2 - 150, ALTO // 2 + 50, 300, 100, AZUL_CLARO, NEGRO, ventana)

    # Llamada desde el bucle principal
    def buscar_partida_thread(id_jugador):
        global buscando_partida, pantalla_actual, oponente_id
        buscando_partida = True  # Activamos la animación
        cliente = Cliente(host='18.216.53.39', puerto=12345)
        cliente.conectar()
        cliente.buscar_partida(id_jugador)

        while cliente.respuesta_partida is None:  # Esperamos la respuesta del servidor
            pygame.event.pump()  # Procesamos eventos de pygame para evitar bloqueo
            time.sleep(0.1)  # Reducimos la carga de la CPU con una pequeña pausa

        buscando_partida = False  # Detenemos la animación una vez que recibimos la respuesta
        if cliente.respuesta_partida and cliente.respuesta_partida.get("accion") == "emparejados":
            print(f"¡Partida encontrada! Oponente ID: {cliente.respuesta_partida.get('oponente_id')}")
            oponente_id = cliente.respuesta_partida.get('oponente_id')
            pantalla_actual = "rival_encontrado"


    # Bucle principal de Pygame
    while True:
        flag = True
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if pantalla_actual == "principal":
                if evento.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    # Verificar si se ha hecho clic en el botón "Crear Carta"
                    if ANCHO // 2 - 150 <= mouse_pos[0] <= ANCHO // 2 + 150 and ALTO // 2 - 100 <= mouse_pos[
                        1] <= ALTO // 2:
                        CrearMazo.iniciar_crear_mazo(pj_id=id_jugador)
                    # Verificar si se ha hecho clic en el botón "Buscar Partida"
                    if ANCHO // 2 - 150 <= mouse_pos[0] <= ANCHO // 2 + 150 and ALTO // 2 + 50 <= mouse_pos[
                        1] <= ALTO // 2 + 150:
                        if not buscando_partida:  # Evitar iniciar un nuevo hilo si ya estamos buscando
                            try:
                                threading.Thread(target=buscar_partida_thread, args=(id_jugador,),
                                                 daemon=True).start()
                            except Exception as e:
                                print(f"Error al conectar: {e}")
                                buscando_partida = False  # Reinicia el estado en caso de error

        # Mostrar animación mientras buscamos partida
        if buscando_partida:
            mostrar_animacion_giratoria(ventana)

        # Rellenar la pantalla de negro
        ventana.fill(NEGRO)

        # Dibujar la pantalla correspondiente
        if pantalla_actual == "principal":
            pantalla_principal()

        elif pantalla_actual == "rival_encontrado":
            pantalla_rival_encontrado(ventana,oponente_id)

        # Actualizar la pantalla
        pygame.display.update()


if __name__ == "__main__":
    main("U-g21FInBATQQx-A-7ns2eMPbIaQZ")

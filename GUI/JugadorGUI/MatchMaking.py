import pygame
import sys
import pygame_gui
from Model.Cliente import Cliente
import threading
import CrearMazo
import time
import math  # Importamos el módulo math

buscando_partida = False
oponente_id = ""
pantalla_actual = ""
dialogo_exito = None  # Variable global para el diálogo
mostrando_botones = True  # Variable para controlar si se muestran los botones

def main(id_jugador, mazo_seleccionado=None):
    global buscando_partida, oponente_id, pantalla_actual, dialogo_exito, mostrando_botones

    # Inicializar pygame
    pygame.init()

    # Colores
    NEGRO = (0, 0, 0)
    BLANCO = (255, 255, 255)
    AZUL_CLARO = (100, 149, 237)

    # Dimensiones de la ventana
    ANCHO = 1820
    ALTO = 900
    # Configuración de la interfaz de usuario de pygame_gui
    manager = pygame_gui.UIManager((ANCHO, ALTO))
    window_surface = pygame.display.set_mode((ANCHO, ALTO))
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

    # Función para mostrar el círculo giratorio y el temporizador
    def mostrar_animacion_giratoria(ventana, tiempo_transcurrido, tiempo_restante):
        """Dibuja un círculo giratorio y muestra el temporizador en el centro de la pantalla."""
        # Calcular el ángulo de rotación
        angulo = (tiempo_transcurrido * 100) % 360
        centro = (ANCHO // 2, ALTO // 2)

        # Dibujar el círculo giratorio (simulando la animación)
        pygame.draw.circle(ventana, BLANCO, centro, 50, 5)

        # Dibujar la línea que girará
        longitud = 40
        radianes = math.radians(angulo)
        x_final = centro[0] + longitud * math.cos(radianes)
        y_final = centro[1] + longitud * math.sin(radianes)

        # Dibujar la línea giratoria
        pygame.draw.line(ventana, BLANCO, centro, (x_final, y_final), 5)

        # Mostrar el tiempo restante en la pantalla
        fuente = pygame.font.Font(None, 36)  # Puedes ajustar el tamaño de la fuente aquí
        texto_tiempo = fuente.render(f"Tiempo restante: {int(tiempo_restante)} s", True, BLANCO)
        ventana.blit(texto_tiempo, (centro[0] - texto_tiempo.get_width() // 2, centro[1] + 60))
        dibujar_boton(fuente_texto.render("CANCELAR", True,BLANCO),ANCHO//2 - 150,ALTO // 2 + 200, 300, 100, BLANCO, NEGRO, ventana)

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

        # Dibujar botones si están habilitados
        if mostrando_botones:
            dibujar_boton(fuente_texto.render('Album', True, BLANCO),
                          ANCHO // 2 - 150, ALTO // 2 - 100, 300, 100, AZUL_CLARO, NEGRO, ventana)

            dibujar_boton(fuente_texto.render('Buscar Partida', True, BLANCO),
                          ANCHO // 2 - 150, ALTO // 2 + 50, 300, 100, AZUL_CLARO, NEGRO, ventana)

    # Llamada desde el bucle principal
    def buscar_partida_thread(id_jugador):
        global buscando_partida, pantalla_actual, oponente_id, mostrando_botones
        buscando_partida = True  # Activamos la animación
        mostrando_botones = False  # Ocultamos los botones
        cliente = Cliente(puerto=12345)
        cliente.conectar()
        cliente.buscar_partida(id_jugador)
        while cliente.respuesta_partida is None:  # Esperamos la respuesta del servidor
            pygame.event.pump()  # Procesamos eventos de pygame para evitar bloqueo
            time.sleep(0.1)  # Reducimos la carga de la CPU con una pequeña pausa
            if not buscando_partida:
                cliente.cerrar_conexion()
                break

        buscando_partida = False  # Detenemos la animación una vez que recibimos la respuesta
        mostrando_botones = True  # Volvemos a mostrar los botones
        if cliente.respuesta_partida and cliente.respuesta_partida.get("accion") == "emparejados":
            print(f"¡Partida encontrada! Oponente ID: {cliente.respuesta_partida.get('oponente_id')}")
            oponente_id = cliente.respuesta_partida.get('oponente_id')
            pantalla_actual = "rival_encontrado"
    def mostrar_dialogo(mensaje, ventana):
        # Fondo del diálogo
        cuadro_dialogo = pygame.Surface((400, 200))
        cuadro_dialogo.fill((0, 0, 0))
        ventana.blit(cuadro_dialogo, (ANCHO // 2 - 200, ALTO // 2 - 100))

        # Texto del mensaje
        texto = fuente_texto.render(mensaje, True, (255, 255, 255))
        ventana.blit(texto, (ANCHO // 2 - texto.get_width() // 2, ALTO // 2 - 30))

        # Botón de aceptar
        boton_texto = fuente_texto.render("Aceptar", True, (255, 255, 255))
        pygame.draw.rect(ventana, AZUL_CLARO, (ANCHO // 2 - 100, ALTO // 2 + 50, 200, 50))
        ventana.blit(boton_texto, (ANCHO // 2 - boton_texto.get_width() // 2, ALTO // 2 + 60))
        pygame.display.update()

        # Coordenadas del botón "Aceptar"
        cuadro_dialogo_rect = pygame.Rect(ANCHO // 2 - 100, ALTO // 2 + 50, 200, 50)

        # Esperar hasta que el jugador haga clic en "Aceptar"
        esperando = True
        while esperando:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if evento.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    if cuadro_dialogo_rect.collidepoint(mouse_pos):
                        esperando = False  # Salir del bucle cuando el jugador haga clic en "Aceptar"

            # Actualizar la pantalla
            pygame.display.update()

    clock = pygame.time.Clock()
    tiempo_inicial = time.time()
    tiempo_limite = 60  # Tiempo límite en segundos
    while True:
        time_delta = clock.tick(60) / 1000.0
        tiempo_transcurrido = time.time() - tiempo_inicial
        tiempo_restante = max(0, tiempo_limite - tiempo_transcurrido)

        for evento in pygame.event.get():
            manager.process_events(evento)
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if pantalla_actual == "Buscando":
                if evento.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    if ANCHO // 2 - 150 <= mouse_pos[0] <= ANCHO // 2 + 150 and ALTO // 2 + 200 <= mouse_pos[1] <= ALTO // 2 + 300:
                        buscando_partida = False
                        pantalla_actual = "principal"
                        mostrando_botones = True

            if pantalla_actual == "principal":
                if evento.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    # Verificar si se ha hecho clic en el botón "Crear Carta"
                    if ANCHO // 2 - 150 <= mouse_pos[0] <= ANCHO // 2 + 150 and ALTO // 2 - 100 <= mouse_pos[
                        1] <= ALTO // 2 and pantalla_actual == "principal":
                        CrearMazo.iniciar_crear_mazo(pj_id=id_jugador)
                    # Verificar si se ha hecho clic en el botón "Buscar Partida"
                    if ANCHO // 2 - 150 <= mouse_pos[0] <= ANCHO // 2 + 150 and ALTO // 2 + 50 <= mouse_pos[
                        1] <= ALTO // 2 + 150 and pantalla_actual == "principal":
                        if mazo_seleccionado is None:
                            mostrar_dialogo("¡El mazo no ha sido seleccionado!", ventana)

                        if not buscando_partida and mazo_seleccionado is not None:
                            try:
                                pantalla_actual = "Buscando"
                                tiempo_inicial = time.time()  # Reinicia el temporizador cada vez que comienza la búsqueda
                                threading.Thread(target=buscar_partida_thread, args=(id_jugador,), daemon=True).start()
                            except Exception as e:
                                buscando_partida = False  # Reinicia el estado en caso de error

        ventana.fill(NEGRO)

        if buscando_partida:
            # Llama a la función de animación y muestra el temporizador
            mostrar_animacion_giratoria(ventana, tiempo_transcurrido, tiempo_restante)
            if tiempo_restante <= 0:
                mostrando_botones = True
                pantalla_actual = "principal"
                buscando_partida = False  # Detener la búsqueda cuando el tiempo se agota


        if pantalla_actual == "principal":
            pantalla_principal()
        elif pantalla_actual == "rival_encontrado":
            pantalla_rival_encontrado(ventana, oponente_id)

        pygame.display.update()
        manager.draw_ui(window_surface)
        manager.update(time_delta)

if __name__ == "__main__":
    main("U-g21FInBATQQx-A-7ns2eMPbIaQZ")

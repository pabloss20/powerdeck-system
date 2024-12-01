import pygame
import sys
import os
import pygame_gui
from Model.Cliente import Cliente
import threading
import CrearMazo
import time
import math  # Importamos el módulo math
from Model.JsonHandler import JsonHandler
from multiprocessing import Process
import random

jsonhandler = JsonHandler('../../Files/usuarios.json')

buscando_partida = False
selecciono_carta = False
oponente_id = ""
cartas_jugador = []
cartas_oponente = []
pantalla_actual = ""
mazo_rival = ""
carta_rival = ""
carta_seleccionada = ""
shuffle = False
puntos_rival = 0
puntos = 0
dialogo_exito = None  # Variable global para el diálogo
mostrando_botones = True  # Variable para controlar si se muestran los botones'
turno_actual = 0
cartas_seleccionadas = []
cartas_no_seleccionadas = []
hitbox = []
cartas_listas = False
def main(id_jugador, mazo_seleccionado=None):
    global buscando_partida, oponente_id, pantalla_actual, dialogo_exito, mostrando_botones, mazo_rival, turno_actual, carta_rival, selecciono_carta, carta_seleccionada, shuffle, puntos, puntos_rival, cartas_listas

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
    shuffle = False
    pantalla_actual = "principal"
    turno_actual = 0
    puntos_rival = 0
    puntos = 0
    cartas_listas = False


    # Variables para controlar el estado de la animación y el juego
    buscando_partida = False  # Para saber si estamos esperando una respuesta
    selecciono_carta = False
    mensaje = None  # Almacena el mensaje de respuesta

    def obtener_cartas(idmazo ,identificador):
        """
        Obtiene las cartas del mazo de un jugador dado su identificador (ID).
        Esta función usa 'jsonhandler.obtener_mazo_de_jugador' para obtener el mazo.
        """
        return jsonhandler.obtener_cartas_de_mazo(idmazo,identificador)  # Suponiendo que devuelve un listado de cartas

    def pantalla_rival_encontrado(ventana, jugador_id, oponente_id, mazo_id, mazo_rival, AMARILLO=(255, 255, 0)):
        global cartas_jugador, turno_actual, cartas_oponente, puntos_rival, puntos, shuffle, cartas_seleccionadas, cartas_no_seleccionadas, hitbox, carta_seleccionada, cartas_listas
        fuente_texto = pygame.font.Font(None, 36)  # Ajusta el tamaño según lo necesario

        """
        Muestra la pantalla cuando se encuentra un oponente, incluyendo las cartas de ambos jugadores y administra turnos.
        """
        ventana.fill(NEGRO)  # Limpiar la pantalla

        cartas_jugador = obtener_cartas(mazo_id, jugador_id)
        cartas_oponente = obtener_cartas(mazo_rival, oponente_id)

        # Selecciona 3 cartas aleatorias
        if len(cartas_jugador) >= 3 and not shuffle:
            cartas_seleccionadas = random.sample(cartas_jugador, 3)
            shuffle = True
            cartas_no_seleccionadas = [carta for carta in cartas_jugador if carta not in cartas_seleccionadas]
        # Mostrar IDs y estado del turno
        texto_jugador = f"Jugador: {jugador_id}"
        renderizado_jugador = fuente_texto.render(texto_jugador, True, BLANCO)
        ventana.blit(renderizado_jugador, (150, ALTO - 50))

        texto_oponente = f"Oponente: {oponente_id}"
        renderizado_oponente = fuente_texto.render(texto_oponente, True, BLANCO)
        ventana.blit(renderizado_oponente, (150, 20))

        puntosR = f"Puntos:  {puntos_rival}"
        renderizado_turno = fuente_texto.render(puntosR, True, AMARILLO)
        ventana.blit(renderizado_turno, (ANCHO // 2 - 100, 20))

        puntosA = f"Puntos: {puntos}"
        renderizado_p = fuente_texto.render(puntosA, True, AMARILLO)
        ventana.blit(renderizado_p, (ANCHO // 2 - 100, ALTO - 50))

        dibujar_cartas(cartas_seleccionadas, oponente_id, ventana, 250, ALTO // 4, ocultar=True)

        # Dibujar cartas y obtener sus áreas
        if turno_actual == 1 and len(cartas_no_seleccionadas) >= 2 and not cartas_listas:
            cartas_seleccionadas.append(cartas_no_seleccionadas.pop(0))
        elif turno_actual == 2 and len(cartas_no_seleccionadas) >= 1 and not cartas_listas:
            cartas_seleccionadas.append(cartas_no_seleccionadas.pop(0))
        if carta_seleccionada in cartas_seleccionadas and not cartas_listas:
            cartas_seleccionadas.remove(carta_seleccionada)
        hitbox = dibujar_cartas(cartas_seleccionadas, oponente_id, ventana, 250, ALTO // 2)
        if cartas_seleccionadas == [] or turno_actual >= 5 and not cartas_listas:
            carta_seleccionada = ""
            pantalla_final(ventana, puntos, puntos_rival)

        return hitbox

    def pantalla_final(ventana, puntos, puntos_rival, BLANCO=(255, 255, 255), NEGRO=(0, 0, 0), ROJO=(255, 0, 0)):
        global pantalla_actual
        pantalla_actual = "final"
        """
        Pantalla final que muestra al ganador y un botón para finalizar.
        """
        # Limpiar la pantalla y definir fuente
        ventana.fill(NEGRO)
        fuente_titulo = pygame.font.Font(None, 80)  # Fuente grande para el título
        fuente_texto = pygame.font.Font(None, 50)  # Fuente para otros textos

        # Determinar ganador
        if puntos > puntos_rival:
            texto_ganador = "¡Ganaste!"
            color_ganador = BLANCO
        elif puntos < puntos_rival:
            texto_ganador = "¡Perdiste!"
            color_ganador = ROJO
        else:
            texto_ganador = "¡Empate!"
            color_ganador = BLANCO

        # Renderizar texto del ganador
        renderizado_titulo = fuente_titulo.render(texto_ganador, True, color_ganador)
        ventana.blit(renderizado_titulo, (ANCHO // 2 - renderizado_titulo.get_width() // 2, ALTO // 3))

        # Mostrar puntos
        texto_puntos = f"Tus puntos: {puntos} - Puntos rival: {puntos_rival}"
        renderizado_puntos = fuente_texto.render(texto_puntos, True, BLANCO)
        ventana.blit(renderizado_puntos, (ANCHO // 2 - renderizado_puntos.get_width() // 2, ALTO // 2))

        # Dibujar botón "Finalizar"
        boton_rect = pygame.Rect(ANCHO // 2 - 100, ALTO - 150, 200, 50)  # Posición y tamaño del botón
        pygame.draw.rect(ventana, BLANCO, boton_rect)
        texto_boton = fuente_texto.render("Finalizar", True, NEGRO)
        ventana.blit(texto_boton, (boton_rect.x + 30, boton_rect.y + 10))

        pygame.display.flip()  # Actualizar pantalla

    def determinar_ganador(carta, cartaR):
        if carta["bonus_poder"] > cartaR["bonus_poder"]:
            return 1
        elif carta["bonus_poder"] < cartaR["bonus_poder"]:
            return 2
        elif carta["bonus_poder"] == cartaR["bonus_poder"]:
            return 3
    def dibujar_cartas(cartas, id_jugador, ventana, x_inicial, y_inicial, ocultar=False):
        hitboxes_cartas = []
        fuente_texto = pygame.font.Font(None, 36)  # Ajusta el tamaño según lo necesario

        espaciado = 120  # Espaciado entre cartas
        tamaño_carta_jugador = (100, 150)  # Tamaño deseado para las cartas del jugador
        tamaño_carta_oculta = (100, 150)  # Tamaño deseado para las cartas ocultas

        for i, carta in enumerate(cartas):
            x = x_inicial + i * espaciado
            y = y_inicial

            if ocultar:
                # Dibuja un rectángulo gris para la carta oculta
                pygame.draw.rect(ventana, (150, 150, 150), (x, y, tamaño_carta_oculta[0], tamaño_carta_oculta[1]))
            else:
                # Mostrar la carta del jugador redimensionada
                imagen_carta = pygame.image.load(carta["imagen"])
                imagen_carta = pygame.transform.scale(imagen_carta, tamaño_carta_jugador)
                ventana.blit(imagen_carta, (x, y))
                puntosR = f" {carta["bonus_poder"]}"
                renderizado_turno = fuente_texto.render(puntosR, True, BLANCO)
                ventana.blit(renderizado_turno, (x, y + 170))

                # Guardar la hitbox de la carta actual
                hitboxes_cartas.append({"rect": pygame.Rect(x, y, tamaño_carta_jugador[0], tamaño_carta_jugador[1]),
                                        "carta": carta})
        return hitboxes_cartas

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
    def cargar_cartas_Select(carta1, carta2,ventana):
        fuente_texto = pygame.font.Font(None, 36)  # Ajusta el tamaño según lo necesario
        x1 = 1200
        y1 = ALTO // 4 + 200
        x2 = 1200
        y2 = ALTO // 4 - 200

        tamaño_carta_jugador = (200, 300)  # Tamaño deseado para las cartas del jugador

        # Mostrar la carta del jugador redimensionada
        imagen_carta = pygame.image.load(carta1["imagen"])
        imagen_carta = pygame.transform.scale(imagen_carta, tamaño_carta_jugador)
        ventana.blit(imagen_carta, (x1, y1))
        puntosR = f" {carta1["bonus_poder"]}"
        renderizado_turno = fuente_texto.render(puntosR, True, BLANCO)
        ventana.blit(renderizado_turno, (x1, y1 + 310))

        # Mostrar la carta del jugador redimensionada
        imagen_carta2 = pygame.image.load(carta2["imagen"])
        imagen_carta2 = pygame.transform.scale(imagen_carta2, tamaño_carta_jugador)
        ventana.blit(imagen_carta2, (x2, y2))
        puntosA = f" {carta2["bonus_poder"]}"
        renderizado_turno2 = fuente_texto.render(puntosA, True, BLANCO)
        ventana.blit(renderizado_turno2, (x2, y2 + 310))


    # Llamada desde el bucle principal
    def buscar_partida_thread(id_jugador, n_mazo):
        global buscando_partida, pantalla_actual, oponente_id, mostrando_botones, mazo_rival
        buscando_partida = True  # Activamos la animación
        mostrando_botones = False  # Ocultamos los botones
        cliente = Cliente()
        cliente.conectar()
        cliente.buscar_partida(id_jugador, n_mazo)
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
            mazo_rival = cliente.respuesta_partida.get('mazo_rival')
            pantalla_actual = "rival_encontrado"

    # Llamada desde el bucle principal
    def cartavs(id_jugador, n_carta):
        global pantalla_actual, oponente_id, carta_rival, puntos_rival, puntos, selecciono_carta, turno_actual, cartas_listas
        cliente = Cliente()
        cliente.conectar()
        cliente.seleccionar_carta(id_jugador, n_carta)
        while cliente.respuesta_partida is None:  # Esperamos la respuesta del servidor
            pygame.event.pump()  # Procesamos eventos de pygame para evitar bloqueo
            time.sleep(0.1)  # Reducimos la carga de la CPU con una pequeña pausa
        if cliente.respuesta_partida and cliente.respuesta_partida.get("accion") == "cartas_seleccionadas":
            print(f"¡Evaluando ganador! Oponente ID: {cliente.respuesta_partida.get('oponente_id')} vs {id_jugador}")
            oponente_id = cliente.respuesta_partida.get('oponente_id')
            carta_rival = cliente.respuesta_partida.get('carta_rival')
            selecciono_carta = True
            cartas_listas = False
            res = determinar_ganador(n_carta, carta_rival)
            if res == 1:
                puntos += 1
            elif res == 2:
                puntos_rival += 1
            turno_actual += 1
            return carta_rival

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
    hitboxes_cartas = []
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
                                threading.Thread(target=buscar_partida_thread, args=(id_jugador, mazo_seleccionado,), daemon=True).start()
                            except Exception as e:
                                buscando_partida = False  # Reinicia el estado en caso de error
            if pantalla_actual == "rival_encontrado":
                if evento.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    for hitbox in hitboxes_cartas:
                        if hitbox["rect"].collidepoint(mouse_pos) and not cartas_listas:
                            cartas_listas = True
                            carta_seleccionada = hitbox["carta"]
                            print(f"Carta seleccionada: {carta_seleccionada}")
                            carta_rival = threading.Thread(target= cartavs, args=(id_jugador, carta_seleccionada,), daemon=True).start()


            elif pantalla_actual == "final":
                if evento.type == pygame.MOUSEBUTTONDOWN:
                    boton_rect = pygame.Rect(ANCHO // 2 - 100, ALTO - 150, 200, 50)
                    if boton_rect.collidepoint(evento.pos):  # Detectar clic en el botón
                        pantalla_actual = "principal"
                        puntos = 0
                        puntos_rival = 0
                        shuffle = False
                        turno_actual = 0
                        pantalla_principal()
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
        elif pantalla_actual == "rival_encontrado" or pantalla_actual == "final":
            hitboxes_cartas = pantalla_rival_encontrado(ventana,  jugador_id= id_jugador,oponente_id= oponente_id,mazo_id = mazo_seleccionado, mazo_rival=mazo_rival)
            if not carta_seleccionada == "":
                if not carta_rival is None:
                    cargar_cartas_Select(carta_seleccionada, carta_rival, ventana)
        pygame.display.update()
        manager.draw_ui(window_surface)
        manager.update(time_delta)

if __name__ == "__main__":
    proceso_1 = Process(target=main, args=("U-DKYT7TUCV4jN-A-ZYm6wvR6DMHz",))
    proceso_2 = Process(target=main, args=("U-mc5QqCgaDbgr-A-dDveHD79sZIo",))

    proceso_1.start()
    proceso_2.start()

    proceso_1.join()
    proceso_2.join()
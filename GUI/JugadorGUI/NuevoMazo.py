import pygame
import pygame_gui
import json
import os
from Model.Mazo import Mazo
import CrearMazo

# Inicializar Pygame y Pygame GUI
pygame.init()
window_size = (1820, 900)
pygame.display.set_caption('PowerDeck')
window_surface = pygame.display.set_mode(window_size)
background = pygame.Surface(window_size)
background.fill(pygame.Color('#ffffff'))

# Variable global para controlar el estado del diálogo de éxito
dialogo_exito_abierto = False


# Configuración de la interfaz de usuario de pygame_gui
manager = pygame_gui.UIManager(window_size)

# Definir la ruta base para la carpeta de imágenes
BASE_DIR = "../.."

# Variables para almacenar el nombre del mazo y las cartas seleccionadas
nombre_del_mazo = ""
cartas_del_mazo = []
id_cartas_del_mazo = []

# Función para cargar cartas desde el JSON de jugadores
def cargar_cartas():
    try:
        with open("../../Files/jugadores.json", "r") as file:
            jugadores_data = json.load(file)

        # Extrae las cartas de cada jugador
        cartas_data = []
        for jugador in jugadores_data:
            if "cartas" in jugador:
                cartas_data.extend(jugador["cartas"])  # Agrega todas las cartas del jugador a la lista

        return cartas_data
    except FileNotFoundError:
        print("El archivo 'jugadores.json' no se encontró.")
        return []
def nuevo_mazo(event):
    global nombre_del_mazo, cartas_del_mazo, id_cartas_del_mazo,dialogo_exito_abierto
    cartas = cargar_cartas()

    cartas_imagenes = []
    for carta in cartas:
        imagen_rel_path = carta.get("imagen")
        imagen_path = os.path.join(BASE_DIR, imagen_rel_path)
        if imagen_rel_path and os.path.exists(imagen_path):
            imagen = pygame.image.load(imagen_path)
            imagen = pygame.transform.scale(imagen, (150, 200))
            cartas_imagenes.append(imagen)
        else:
            print(f"No se encontró la imagen en el path: {imagen_path}")
            carta_placeholder = pygame.Surface((150, 200))
            carta_placeholder.fill((200, 200, 200))  # Color gris para las cartas sin imagen
            cartas_imagenes.append(carta_placeholder)

    # Configuración de fuente
    font = pygame.font.SysFont("Arial", 36)

    # Título "Mis Cartas"
    titulo_texto = font.render("Mis Cartas", True, pygame.Color('#000000'))
    titulo_pos = (window_size[0] * 0.4, 20)

    # Tamaños y posiciones adaptativas
    boton_ancho, boton_alto = 140, 50
    panel_derecha_x = window_size[0] * 0.8
    panel_derecha_ancho = window_size[0] * 0.18
    panel_derecha_alto = window_size[1] * 0.7

    # Botón "Atrás" y "Listo"
    boton_atras = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((panel_derecha_x + 20, window_size[1] - 80), (boton_ancho, boton_alto)),
        text='Atrás',
        manager=manager
    )
    boton_listo = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((panel_derecha_x + 20, window_size[1] - 150), (boton_ancho, boton_alto)),
        text='Listo',
        manager=manager
    )

    # Campo de entrada para el nombre del mazo
    input_nombre_mazo = pygame_gui.elements.UITextEntryLine(
        relative_rect=pygame.Rect((panel_derecha_x + 10, 50), (panel_derecha_ancho - 20, 40)),
        manager=manager
    )
    input_nombre_mazo.set_text("Nombre del Mazo")

    # Contenedor para las cartas en la derecha, con scrollbar
    contenedor_cartas_derecha = pygame_gui.elements.UIScrollingContainer(
        relative_rect=pygame.Rect((panel_derecha_x + 10, 100), (panel_derecha_ancho - 20, panel_derecha_alto)),
        manager=manager
    )

    # Función para actualizar el contenedor derecho con los nombres de cartas en cartas_del_mazo
    def actualizar_contenedor_derecho():
        # Limpiar el contenedor antes de agregar las cartas
        contenedor_cartas_derecha.get_container().kill()
        contenedor_cartas_derecha.set_container(
            pygame_gui.core.ui_container.UIContainer(relative_rect=contenedor_cartas_derecha.relative_rect,
                                                     manager=manager)
        )

        # Ajustar la posición de cada carta dentro del contenedor y calcular la altura total
        altura_total = len(cartas_del_mazo) * 40  # Ajusta el tamaño vertical basado en el número de cartas

        for idx, nombre_carta in enumerate(cartas_del_mazo):
            carta_texto = pygame_gui.elements.UIButton(
                relative_rect=pygame.Rect((10, idx * 40), (panel_derecha_ancho - 40, 30)),
                text=nombre_carta,
                manager=manager,
                container=contenedor_cartas_derecha.get_container()
            )

        # Si la altura total es mayor que el contenedor, activa el scroll
        contenedor_cartas_derecha.set_scrollable_area_dimensions((panel_derecha_ancho - 40, altura_total))

    # Contenedor para cartas en el lado izquierdo
    contenedor_cartas_izquierda = pygame_gui.elements.UIScrollingContainer(
        relative_rect=pygame.Rect((300, 150), (700, 650)),
        manager=manager
    )
    start_x, start_y = 10, 10
    espacio_x, espacio_y = 120, 160
    columnas = 4

    # Diccionario para asociar cada UIImage con su llave y nombre
    cartas_ui = {}
    cartas_data = cargar_cartas()

    for i, carta in enumerate(cartas_data):
        pos_x = start_x + (i % columnas) * espacio_x
        pos_y = start_y + (i // columnas) * espacio_y

        carta_imagen = pygame_gui.elements.UIImage(
            relative_rect=pygame.Rect((pos_x, pos_y), (100, 150)),
            image_surface=cartas_imagenes[i],
            manager=manager,
            container=contenedor_cartas_izquierda.get_container()
        )

        # Asocia la carta con su llave y nombre en el diccionario
        cartas_ui[carta_imagen] = {"llave": carta["llave"], "nombre": carta["nombre_personaje"], "rareza": carta["tipo_carta"]}
        print(f"Asociando carta con llave: {carta['llave']} y nombre: {carta['nombre_personaje']}")


    # Define el cuadro de diálogo y el evento de confirmación.
    def mostrar_confirmacion_exito():
        # Crear cuadro de diálogo de confirmación
        dialogo_exito = pygame_gui.windows.UIConfirmationDialog(
            rect=pygame.Rect((window_size[0] // 2 - 150, window_size[1] // 2 - 50), (300, 100)),
            manager=manager,
            window_title="Éxito",
            action_long_desc="Mazo creado con éxito!",
            action_short_name="OK",
            blocking=True
        )
        return dialogo_exito  # Devolver la referencia para usar en el bucle de evento

    def btn_listo(nombre_mazo, lista_cartas):
        global dialogo_exito_abierto
        try:
            # Crear una instancia de la clase Mazo con el nombre proporcionado
            mi_mazo = Mazo(nombre_mazo)

            # Agregar cada carta de la lista al mazo usando su ID
            for carta_id in lista_cartas:
                mi_mazo.agregar_carta(carta_id)

            # Verificar si el mazo cumple con los requisitos de validez
            mi_mazo.es_valido()

            # Verificar la rareza de las cartas en el mazo
            mi_mazo.verificar_rareza()

            # Guardar el mazo en un archivo JSON
            mi_mazo.guardar_en_json()

            # Mostrar confirmación al usuario
            dialogo_exito_abierto = True
            dialogo_exito = mostrar_confirmacion_exito()

        except ValueError as e:
            dialogo_exito_abierto = False
            print("Error al crear el mazo:", e)

            # Crear un cuadro de diálogo para mostrar el error al usuario
            pygame_gui.windows.UIConfirmationDialog(
                rect=pygame.Rect((window_size[0] // 2 - 150, window_size[1] // 2 - 50), (300, 100)),
                manager=manager,
                window_title="Error",
                action_long_desc=str(e),
                action_short_name="OK",
                blocking=True
            )

    # Loop principal
    clock = pygame.time.Clock()
    is_running = True
    while is_running:
        time_delta = clock.tick(60) / 1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_running = False

            manager.process_events(event)

            if event.type == pygame.USEREVENT:
                if event.user_type == pygame_gui.UI_CONFIRMATION_DIALOG_CONFIRMED and dialogo_exito_abierto:
                    # Llama a la función iniciar_crear_mazo al hacer clic en "OK"
                    CrearMazo.iniciar_crear_mazo()
                    dialogo_exito_abierto = False

                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == boton_atras:
                        CrearMazo.iniciar_crear_mazo()
                    elif event.ui_element == boton_listo:
                        nombre_del_mazo = input_nombre_mazo.get_text()
                        print("Nombre del mazo guardado:", nombre_del_mazo)
                        print("Cartas seleccionadas:", cartas_del_mazo)
                        btn_listo(nombre_del_mazo, id_cartas_del_mazo)
                    elif event.ui_element in contenedor_cartas_derecha:
                        # Eliminar carta al hacer clic en su nombre en el contenedor derecho
                        carta_texto = event.ui_element.text
                        # Buscar el índice de la carta en cartas_del_mazo
                        if carta_texto in cartas_del_mazo:
                            indice = cartas_del_mazo.index(carta_texto)
                            # Eliminar tanto de cartas_del_mazo como de id_cartas_del_mazo
                            cartas_del_mazo.pop(indice)
                            id_cartas_del_mazo.pop(indice)
                            actualizar_contenedor_derecho()
                            print(f"Carta '{carta_texto}' eliminada de cartas_del_mazo y su ID de id_cartas_del_mazo")

        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:  # 1 es el botón izquierdo del ratón
                mouse_pos = pygame.mouse.get_pos()
                for carta_imagen, datos_carta in cartas_ui.items():
                    if carta_imagen.rect.collidepoint(mouse_pos):
                        # Añadir la carta si no está en la lista
                        if datos_carta["llave"] not in id_cartas_del_mazo:
                            cartas_del_mazo.append(datos_carta["nombre"] +"r:" + datos_carta["rareza"])
                            id_cartas_del_mazo.append(datos_carta["llave"])
                            actualizar_contenedor_derecho()
                            print("Nombre de la carta añadida:", datos_carta["nombre"])

        window_surface.blit(background, (0, 0))
        window_surface.blit(titulo_texto, titulo_pos)
        manager.update(time_delta)

        # Actualizar la interfaz de usuario
        contenedor_cartas_derecha.update(time_delta)
        contenedor_cartas_izquierda.update(time_delta)
        manager.draw_ui(window_surface)
        pygame.display.update()

    pygame.quit()

if __name__ == "__main__":
    nuevo_mazo()

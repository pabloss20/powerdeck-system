import pygame
import pygame_gui
import json
import os
import NuevoMazo

# Inicializar Pygame y Pygame GUI
pygame.init()
window_size = (1820, 900)
pygame.display.set_caption('PowerDeck')
window_surface = pygame.display.set_mode(window_size)
background = pygame.Surface(window_size)
background.fill(pygame.Color('#ffffff'))

# Configuración de la interfaz de usuario de pygame_gui
manager = pygame_gui.UIManager(window_size)

# Definir la ruta base para la carpeta de imágenes
BASE_DIR = "..\.."


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

# Función para cargar nombres de mazos desde el JSON
def cargar_nombres_mazos():
    nombres_mazos = []
    try:
        with open("../../Files/mazo.json", "r") as file:
            mazos_data = json.load(file)
            # Obtener el atributo "nombre" de cada mazo
            nombres_mazos = [mazo.get("nombre", "Mazo sin nombre") for mazo in mazos_data]
    except FileNotFoundError:
        print("El archivo 'mazo.json' no se encontró.")
    return nombres_mazos

def iniciar_crear_mazo():
    # Cargar cartas desde el JSON
    cartas = cargar_cartas()

    # Cargar imágenes de las cartas
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
            cartas_imagenes.append(pygame.Surface((150, 200)))
            cartas_imagenes[-1].fill((200, 200, 200))  # Color gris para las cartas sin imagen

    # Asegúrate de que el número de cartas y la cantidad de imágenes coincidan
    if len(cartas_imagenes) < len(cartas):
        cartas_imagenes += [pygame.Surface((150, 200))] * (len(cartas) - len(cartas_imagenes))

    # Configuración de fuente
    font = pygame.font.SysFont("Arial", 36)

    # Título "Mis Cartas"
    titulo_texto = font.render("Mis Cartas", True, pygame.Color('#000000'))
    titulo_pos = (window_size[0] * 0.4, 20)

    # Tamaños y posiciones adaptativas
    boton_ancho, boton_alto = 140, 50
    panel_derecha_x = window_size[0] * 0.8  # Posición del panel derecho
    panel_derecha_ancho = window_size[0] * 0.18
    panel_derecha_alto = window_size[1] * 0.7

    # Botón "Atrás" y "Mazo Nuevo"
    boton_atras = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((panel_derecha_x + 20, window_size[1] - 80),
                                                                         (boton_ancho, boton_alto)),
                                               text='Atrás',
                                               manager=manager)
    boton_nuevo_mazo = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((panel_derecha_x + 20, window_size[1] - 150),
                                  (boton_ancho, boton_alto)),
        text='Mazo Nuevo',
        manager=manager)

    # Cargar los nombres de los mazos y mostrarlos en la lista
    nombres_mazos = cargar_nombres_mazos()
    lista_mazos = pygame_gui.elements.UISelectionList(relative_rect=pygame.Rect((panel_derecha_x + 10, 100),
                                                                                (panel_derecha_ancho - 20,
                                                                                 panel_derecha_alto)),
                                                      item_list=nombres_mazos,
                                                      manager=manager)
    # Tamaño del contenedor para las cartas
    contenedor_cartas = pygame_gui.elements.UIScrollingContainer(
        relative_rect=pygame.Rect((300, 150), (700, 650)),  # Ajusta la posición y tamaño según tu diseño
        manager=manager
    )
    start_x, start_y = 10, 10  # Posición inicial de las cartas dentro del contenedor
    espacio_x, espacio_y = 120, 160  # Espaciado entre las cartas
    columnas = 4  # Número de columnas en la cuadrícula


    # Diccionario para asociar cada UIImage con su llave
    cartas_ui = {}
    cartas_data = cargar_cartas()

    # Crear cada carta y asociarla a su llave
    for i, carta in enumerate(cartas_data):
        pos_x = start_x + (i % columnas) * espacio_x
        pos_y = start_y + (i // columnas) * espacio_y

        carta_imagen = pygame_gui.elements.UIImage(
            relative_rect=pygame.Rect((pos_x, pos_y), (100, 150)),
            image_surface=cartas_imagenes[i],
            manager=manager,
            container=contenedor_cartas.get_container()
        )

        # Asocia la carta con su llave en el diccionario
        cartas_ui[carta_imagen] = carta["llave"]
        print(f"Asociando carta con llave: {carta['llave']}")  # Para verificar la asociación

    # Loop principal
    clock = pygame.time.Clock()
    is_running = True
    while is_running:
        time_delta = clock.tick(60) / 1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_running = False
            manager.process_events(event)  # Mueve esto aquí para procesar todos los eventos primero

            if event.type == pygame.USEREVENT:
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    print("Evento de botón presionado:", event.ui_element)  # Para verificar el evento
                    if event.ui_element == boton_atras:
                        is_running = False  # Cierra la ventana
                    elif event.ui_element == boton_nuevo_mazo:
                        NuevoMazo.nuevo_mazo()
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:  # 1 es el botón izquierdo del ratón
                mouse_pos = pygame.mouse.get_pos()
                for carta_imagen, llave in cartas_ui.items():
                    if carta_imagen.rect.collidepoint(mouse_pos):
                        print("Llave de la carta clickeada:", llave)

            manager.process_events(event)

        # Dibujar elementos en pantalla
        window_surface.blit(background, (0, 0))
        window_surface.blit(titulo_texto, titulo_pos)
        manager.update(time_delta)

        # Actualizar la interfaz de usuario
        contenedor_cartas.update(time_delta)
        manager.draw_ui(window_surface)
        pygame.display.update()

    pygame.quit()


if __name__ == "__main__":
    iniciar_crear_mazo()

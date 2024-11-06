import pygame
import pygame_gui
import json
import pygame_gui.elements
import os

# Inicializar Pygame y Pygame GUI
pygame.init()
window_size = (1820, 900)
pygame.display.set_caption('PowerDeck')
window_surface = pygame.display.set_mode(window_size)
background = pygame.Surface(window_size)
background.fill(pygame.Color('#ffffff'))

# Configuración de la interfaz de usuario de pygame_gui
manager = pygame_gui.UIManager(window_size)



# Función para cargar cartas desde el JSON
def cargar_cartas():
    try:
        with open("../../Files/cartas.json", "r") as file:
            cartas_data = json.load(file)
        return sorted(cartas_data, key=lambda c: (c["nombre_personaje"], c.get("nombre_variante", "")))
    except FileNotFoundError:
        print("Error: El archivo 'cartas.json' no se encontró.")
        return []
    except json.JSONDecodeError:
        print("Error al cargar las cartas. Intente más tarde.")
        return []


# Función para filtrar cartas
def filtrar_cartas(cartas, mostrar_principales):
    alb = []
    if mostrar_principales:
        for carta in cartas:
            if not carta.get("es_variante"):
                alb.append(carta)
    else:
        alb = cartas
    return alb


    print(cartas)
    return cartas


def iniciar_galeria():
    # Tamaños y posiciones adaptativas
    boton_ancho, boton_alto = 140, 50
    panel_derecha_x = window_size[0] * 0.8
    panel_derecha_ancho = window_size[0] * 0.18
    panel_derecha_alto = window_size[1] * 0.7

    # Cargar cartas
    try:
        cartas = cargar_cartas()
    except ValueError as e:
        cartas = []
    con_filtro = False
    if not cartas:
        pygame_gui.windows.UIConfirmationDialog(
            rect=pygame.Rect((window_size[0] // 2 - 150, window_size[1] // 2 - 50), (300, 100)),
            manager=manager,
            window_title="Error",
            action_long_desc=str("No existe ninguna carta creada en el juego"),
            action_short_name="OK",
            blocking=True
        )

    # Configuración de fuente
    font = pygame.font.SysFont("Arial", 24)
    titulo_texto = font.render("Galería POWER DECK", True, pygame.Color('#000000'))
    titulo_pos = (window_size[0] * 0.4, 20)

    # Botón "Atrás" y "Filtro"
    boton_atras = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((panel_derecha_x + 20, window_size[1] - 80), (boton_ancho, boton_alto)),
        text='Atrás',
        manager=manager
    )
    boton_filtro = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((panel_derecha_x + 200, window_size[1] - 80), (boton_ancho, boton_alto)),
        text='Filtrar Variantes',
        manager=manager
    )

    # Contenedor de cartas
    contenedor_cartas = pygame_gui.elements.UIScrollingContainer(
        relative_rect=pygame.Rect((100, 100), (1600, 700)),
        manager=manager
    )

    def actualizar_contenido():

        # Eliminar contenido existente
        for element in contenedor_cartas.get_container().elements:
            element.hide()

        # Aplicar filtro
        cartas_mostradas = filtrar_cartas(cartas, mostrar_principales=con_filtro)
        start_x, start_y = 10, 10
        espacio_x, espacio_y = 200, 300
        columnas = 7

        for i, carta in enumerate(cartas_mostradas):
            pos_x = start_x + (i % columnas) * espacio_x
            pos_y = start_y + (i // columnas) * espacio_y

            # Cargar imagen o marcador de posición
            imagen_rel_path = carta.get("imagen")
            imagen_path = os.path.join(imagen_rel_path)
            if imagen_rel_path and os.path.exists(imagen_path):
                imagen = pygame.image.load(imagen_path)
                imagen = pygame.transform.scale(imagen, (100, 150))
            else:
                imagen = pygame.Surface((100, 150))
                imagen.fill((200, 200, 200))

            carta_imagen = pygame_gui.elements.UIImage(
                relative_rect=pygame.Rect((pos_x, pos_y), (100, 150)),
                image_surface=imagen,
                manager=manager,
                container=contenedor_cartas.get_container()
            )

            # Mostrar los atributos de la carta
            info_text = f"{carta['nombre_personaje']}\n{carta.get('nombre_variante', '')}\n{carta['raza']}\n{carta['tipo_carta']}\n" \
                        f"Activa en Juego: {'Sí' if carta.get('activa_en_juego', False) else 'No'}\n" \
                        f"Activa en Sobres: {'Sí' if carta.get('activa_en_sobres', False) else 'No'}\n" \
                        f"Llave unica: {carta['llave']}\n" \
                        f"Fecha Modificación: {carta['fecha_modificacion']}"

            pygame_gui.elements.UITextBox(
                relative_rect=pygame.Rect((pos_x, pos_y + 160), (180, 120)),
                html_text=info_text,
                manager=manager,
                container=contenedor_cartas.get_container()
            )

    actualizar_contenido()

    clock = pygame.time.Clock()
    is_running = True
    while is_running:
        time_delta = clock.tick(60) / 1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_running = False
            manager.process_events(event)

            if event.type == pygame.USEREVENT:
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == boton_atras:
                        is_running = False
                    if event.ui_element == boton_filtro:
                        con_filtro = not con_filtro
                        actualizar_contenido()

        window_surface.blit(background, (0, 0))
        window_surface.blit(titulo_texto, titulo_pos)
        manager.update(time_delta)
        manager.draw_ui(window_surface)
        pygame.display.update()

    pygame.quit()


if __name__ == "__main__":
    iniciar_galeria()

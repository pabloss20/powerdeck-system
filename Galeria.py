import pygame
import pygame.freetype
import json
import os

# Inicializar Pygame
pygame.init()

# Dimensiones de la ventana
ANCHO_VENTANA = 1400
ALTO_VENTANA = 800
FONDO_COLOR = (200, 200, 200)  # Fondo gris claro
RADIO_ESQUINA = 20  # Radio para las esquinas redondeadas

# Crear ventana
ventana = pygame.display.set_mode((ANCHO_VENTANA, ALTO_VENTANA), pygame.RESIZABLE)
pygame.display.set_caption("Power Deck - Galería de Cartas")

# Cargar la imagen del título y reducir su tamaño en un 25%
titulo_imagen = pygame.image.load("imgs/titulo_crearcarta.png").convert_alpha()
titulo_imagen = pygame.transform.scale(titulo_imagen, (300, 150))  # Tamaño reducido

# Cargar la imagen de la lupa y reducir su tamaño en un 90%
lupa_imagen = pygame.image.load("imgs/lupa.png").convert_alpha()
nuevo_ancho_lupa = int(lupa_imagen.get_width() * 0.03)
nuevo_alto_lupa = int(lupa_imagen.get_height() * 0.03)
lupa_imagen = pygame.transform.scale(lupa_imagen, (nuevo_ancho_lupa, nuevo_alto_lupa))

# Crear fuente
fuente = pygame.freetype.SysFont("Comic Sans MS", 24)
fuente_nombre = pygame.freetype.SysFont("Comic Sans MS", 18)

# Elementos de la interfaz
barra_busqueda = pygame.Rect(100, 220, 400, 40)
filtros_menu = pygame.Rect(570, 220, 150, 40)
boton_refrescar = pygame.Rect(780, 220, 150, 40)
boton_regresar = pygame.Rect(990, 220, 330, 40)

# Cuadrado blanco en el centro
cuadrado_blanco = pygame.Rect((ANCHO_VENTANA - 1300) // 2, 195, 1300, 550)

# Variables de estado
texto_busqueda = ""
mostrar_filtros = False
cartas = []  # Lista para almacenar las imágenes de las cartas y sus nombres
cartas_originales = []  # Lista para almacenar el orden original de las cartas
filtro_seleccionado = "Filtros"

# Función para cargar las cartas desde el archivo JSON
def cargar_cartas():
    global cartas, cartas_originales
    cartas = []  # Reiniciar la lista de cartas
    cartas_originales = []  # Reiniciar la lista de cartas originales
    with open('cartas.json', 'r') as archivo:
        datos = json.load(archivo)
        for carta in datos:
            # Cargar la imagen de la carta y el nombre del personaje
            ruta_imagen = carta["imagen"]
            nombre_personaje = carta.get("nombre_personaje", "Sin Nombre")
            if os.path.exists(ruta_imagen):  # Verificar si la imagen existe
                imagen_carta = pygame.image.load(ruta_imagen).convert_alpha()
                imagen_carta = pygame.transform.scale(imagen_carta, (120, 170))  # Redimensionar la imagen si es necesario
                cartas.append((imagen_carta, nombre_personaje))
                cartas_originales.append((imagen_carta, nombre_personaje))  # Guardar el orden original

# Función para dibujar las cartas en la ventana
def dibujar_cartas():
    x_offset = 50  # Espacio horizontal entre cartas
    y_offset = 50  # Espacio vertical entre cartas
    cartas_por_fila = 5  # Cambiar a 4 cartas por fila después de la cuarta
    for i, (imagen_carta, nombre_personaje) in enumerate(cartas):
        fila = i // cartas_por_fila
        columna = i % cartas_por_fila
        x_pos = 150 + columna * (200 + x_offset)
        y_pos = 300 + fila * (200 + y_offset)
        ventana.blit(imagen_carta, (x_pos, y_pos))
        # Dibujar el nombre del personaje sobre la carta
        nombre_rect = pygame.Rect(x_pos, y_pos - 25, 120, 25)
        centrar_texto(ventana, nombre_personaje, nombre_rect, font_color=(0, 0, 0))

# Función para dibujar rectángulos con esquinas redondeadas
def rect_redondeado(surface, color, rect, radio):
    pygame.draw.rect(surface, (0, 0, 0), rect.inflate(6, 6), border_radius=radio)  # Borde negro
    pygame.draw.rect(surface, color, rect, border_radius=radio)  # Relleno blanco

# Función para dibujar rectángulos sin esquinas redondeadas
def rect_sin_redondear(surface, color_fondo, rect):
    pygame.draw.rect(surface, (0, 0, 0), rect, 0)  # Borde negro
    pygame.draw.rect(surface, color_fondo, rect.inflate(-6, -6))  # Relleno blanco

# Función para centrar el texto en un rectángulo
def centrar_texto(surface, text, rect, font_color=(0, 0, 0)):
    text_surface, text_rect = fuente.render(text, font_color)
    text_rect.center = rect.center
    surface.blit(text_surface, text_rect)

# Función para colocar texto dentro del rectángulo sin desbordar
def texto_derecha(surface, text, rect, offset=10, font_color=(0, 0, 0)):
    text_surface, text_rect = fuente.render(text, font_color)
    text_rect.midleft = (rect.x + offset, rect.centery)
    surface.blit(text_surface, text_rect)

# Función para ordenar las cartas alfabéticamente por nombre de personaje
def ordenar_cartas_alfabeticamente():
    global cartas
    cartas.sort(key=lambda carta: carta[1])

# Función para eliminar filtros y restaurar el orden original
def eliminar_filtro():
    global cartas, filtro_seleccionado
    cartas = cartas_originales.copy()  # Restaurar cartas originales
    filtro_seleccionado = "Filtros"  # Cambiar texto del filtro a por defecto

# Cargar las cartas al iniciar
cargar_cartas()

# Bucle principal
corriendo = True
while corriendo:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            corriendo = False

        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_RETURN:
                print("Texto de búsqueda:", texto_busqueda)

        if evento.type == pygame.MOUSEBUTTONDOWN:
            if filtros_menu.collidepoint(evento.pos):
                mostrar_filtros = not mostrar_filtros
            if boton_refrescar.collidepoint(evento.pos):
                print("Botón refrescar presionado")
                cargar_cartas()  # Cargar cartas al presionar refrescar
                if filtro_seleccionado == "Alfabético":
                    ordenar_cartas_alfabeticamente()
                elif filtro_seleccionado == "Filtros":
                    eliminar_filtro()  # Restaurar el orden original

            if boton_regresar.collidepoint(evento.pos):
                print("Botón regresar presionado")
            if mostrar_filtros:
                opcion_filtros_rect = pygame.Rect(filtros_menu.x, filtros_menu.y + 40, filtros_menu.width, 40)
                if opcion_filtros_rect.collidepoint(evento.pos):
                    filtro_seleccionado = "Alfabético"
                    mostrar_filtros = False
                    print("Filtro seleccionado: Alfabético")
                    ordenar_cartas_alfabeticamente()
                elif filtros_menu.y + 80 < evento.pos[1] < filtros_menu.y + 120:  # Opción de eliminar filtros
                    eliminar_filtro()
                    mostrar_filtros = False
                    print("Filtro eliminado, se ha restaurado el orden original")

        if evento.type == pygame.TEXTINPUT:
            texto_busqueda += evento.text
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_BACKSPACE:
                texto_busqueda = texto_busqueda[:-1]

    # Dibujar el fondo
    ventana.fill(FONDO_COLOR)

    # Dibujar el cuadrado blanco en el centro sin esquinas redondeadas
    rect_sin_redondear(ventana, (255, 255, 255), cuadrado_blanco)

    # Dibujar título
    ventana.blit(titulo_imagen, (ANCHO_VENTANA // 2 - titulo_imagen.get_width() // 2, 20))

    # Dibujar barra de búsqueda con esquinas redondeadas
    rect_redondeado(ventana, (255, 255, 255), barra_busqueda, RADIO_ESQUINA)
    texto_derecha(ventana, texto_busqueda, barra_busqueda)

    # Dibujar la imagen de la lupa en la barra de búsqueda
    ventana.blit(lupa_imagen, (110, 225))

    # Dibujar las cartas
    dibujar_cartas()

    # Dibujar menú de filtros
    rect_redondeado(ventana, (255, 255, 255), filtros_menu, RADIO_ESQUINA)
    centrar_texto(ventana, filtro_seleccionado, filtros_menu)

    # Si se están mostrando los filtros, dibujar la opción de "Alfabético" y "Eliminar Filtros"
    if mostrar_filtros:
        # Opción "Alfabético"
        opcion_filtros_rect = pygame.Rect(filtros_menu.x, filtros_menu.y + 40, filtros_menu.width, 40)
        rect_sin_redondear(ventana, (255, 255, 255), opcion_filtros_rect)
        centrar_texto(ventana, "Alfabético", opcion_filtros_rect)

        # Opción "Eliminar Filtros"
        opcion_eliminar_filtros_rect = pygame.Rect(filtros_menu.x, filtros_menu.y + 80, filtros_menu.width, 40)
        rect_sin_redondear(ventana, (255, 255, 255), opcion_eliminar_filtros_rect)
        centrar_texto(ventana, "Eliminar Filtros", opcion_eliminar_filtros_rect)

    # Dibujar botones
    rect_redondeado(ventana, (255, 255, 255), boton_refrescar, RADIO_ESQUINA)
    centrar_texto(ventana, "Refrescar", boton_refrescar)

    rect_redondeado(ventana, (255, 255, 255), boton_regresar, RADIO_ESQUINA)
    centrar_texto(ventana, "Regresar al menú principal", boton_regresar)

    # Actualizar pantalla
    pygame.display.flip()

# Salir de Pygame
pygame.quit()

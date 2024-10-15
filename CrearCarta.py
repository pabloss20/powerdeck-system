import pygame
import os
import tkinter as tk
from tkinter import filedialog
from PIL import Image
import shutil
import pygame_gui
from pygame_gui.core import ObjectID

# Inicializar Pygame
pygame.init()

clock = pygame.time.Clock()
# Definir colores
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
FONDO_COLOR = (240, 240, 240)

# Definir el tamaño inicial de la ventana
ANCHO_VENTANA = 1820
ALTO_VENTANA = 900
ventana = pygame.display.set_mode((ANCHO_VENTANA, ALTO_VENTANA), pygame.RESIZABLE)
pygame.display.set_caption('Power Deck - Herramienta de Cartas')

# Ruta de las imágenes
ruta_imagenes = os.path.join('imgs')
ruta_guardar_imagenes = os.path.join('Cartas')  # Carpeta para guardar las imágenes

# Crear la carpeta de destino si no existe
if not os.path.exists(ruta_guardar_imagenes):
    os.makedirs(ruta_guardar_imagenes)

# Cargar las imágenes
titulo_crear_carta = pygame.image.load(os.path.join(ruta_imagenes, 'titulo_crearcarta.png'))
inputboxes_img = pygame.image.load(os.path.join(ruta_imagenes, 'inputboxes.png'))
arrastrar_imagen = pygame.image.load(os.path.join(ruta_imagenes, 'ArrastrarImagen.png'))
info = pygame.image.load(os.path.join(ruta_imagenes, 'info.png'))

# Fuente para el texto
fuente = pygame.font.Font(None, 32)


# Redimensionar imágenes
def redimensionar_imagen(imagen, ancho_maximo):
    ancho_original, alto_original = imagen.get_size()
    proporcion = alto_original / ancho_original
    alto_maximo = int(ancho_maximo * proporcion)
    return pygame.transform.scale(imagen, (ancho_maximo, alto_maximo))


# Función para guardar la imagen seleccionada en una carpeta
def guardar_imagen_seleccionada(ruta_imagen_original):
    # Extraer el nombre del archivo
    nombre_archivo = os.path.basename(ruta_imagen_original)

    # Ruta de destino
    ruta_guardada = os.path.join(ruta_guardar_imagenes, nombre_archivo)

    # Copiar la imagen a la carpeta de destino
    shutil.copy(ruta_imagen_original, ruta_guardada)

    return ruta_guardada  # Devolver la ruta donde se guardó la imagen

# Redimensionar imágenes
titulo_crearcarta = redimensionar_imagen(titulo_crear_carta, 600)
info_bloques = redimensionar_imagen(info, 400)
inputboxes_img = redimensionar_imagen(inputboxes_img, 400)
arrastrar_imagen = redimensionar_imagen(arrastrar_imagen, 455)

# Variable para manejar la imagen actual arrastrar
imagen_actual = arrastrar_imagen
posicion_imagen = (ANCHO_VENTANA * 0.6, ALTO_VENTANA * 0.26)


# Función para abrir un cuadro de diálogo de selección de archivo
def abrir_dialogo_imagen():
    root = tk.Tk()
    root.withdraw()  # Ocultar la ventana principal
    ruta_imagen = filedialog.askopenfilename(title="Seleccionar Imagen",
                                             filetypes=[("Imágenes", "*.png; *webp;")])
    root.destroy()  # Destruir la ventana después de la selección
    return ruta_imagen




MANAGER = pygame_gui.UIManager((ANCHO_VENTANA, ALTO_VENTANA), 'text_entry_box.json')
#MANAGER.get_theme().load_theme('text_entry_line.json')
# Crear instancias de UITextEntryLine en lugar de las cajas de texto tradicionales
text_input_boxes = [
    pygame_gui.elements.UITextEntryLine(
        relative_rect=pygame.Rect((600, ALTO_VENTANA * 0.26, 350, 42)), manager=MANAGER,
        object_id=ObjectID(class_id='@campoTXT',object_id="input1")),
    pygame_gui.elements.UITextEntryBox(
        relative_rect=pygame.Rect((600, ALTO_VENTANA * 0.34, 350, 170)), manager=MANAGER,object_id=ObjectID(class_id='@campoTXT',object_id="input2")),
    pygame_gui.elements.UITextEntryLine(
        relative_rect=pygame.Rect((600, ALTO_VENTANA * 0.55, 350, 42)), manager=MANAGER,
        object_id=ObjectID(class_id='@campoTXT',object_id="input3")),
    pygame_gui.elements.UITextEntryLine(
        relative_rect=pygame.Rect((600, ALTO_VENTANA * 0.62, 350, 42)), manager=MANAGER,
        object_id=ObjectID(class_id='@campoTXT',object_id="input4")),
    pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((600, ALTO_VENTANA * 0.69, 350, 42)),
                                        manager=MANAGER, object_id=ObjectID(class_id='@campoTXT',object_id="input5")),
    pygame_gui.elements.UITextEntryLine(
        relative_rect=pygame.Rect((600, ALTO_VENTANA * 0.77, 350, 42)), manager=MANAGER,
        object_id=ObjectID(class_id='@campoTXT',object_id="input6")),
    pygame_gui.elements.UITextEntryLine(
        relative_rect=pygame.Rect((600, ALTO_VENTANA * 0.83, 350, 42)), manager=MANAGER,
        object_id=ObjectID(class_id='@campoTXT',object_id="input7"))
]
# Añadir el botón de guardar
boton_guardar = pygame_gui.elements.UIButton(
    relative_rect=pygame.Rect((600, ALTO_VENTANA * 0.9, 100, 40)),
    text='Guardar',
    manager=MANAGER
)


# Función para obtener los valores de los campos de texto
def guardar_datos():
    nombre_personaje = text_input_boxes[0].get_text()
    descripcion = text_input_boxes[1].get_text()
    nombre_variante = text_input_boxes[2].get_text()
    indicador = text_input_boxes[3].get_text()
    fecha_creacion = text_input_boxes[4].get_text()
    fecha_modificacion = text_input_boxes[5].get_text()
    raza = text_input_boxes[6].get_text()

    # Aquí puedes hacer lo que necesites con las variables, como imprimirlas o guardarlas en un archivo
    print(f"Nombre del personaje: {nombre_personaje}")
    print(f"Descripción: {descripcion}")
    print(f"Nombre de variante: {nombre_variante}")
    print(f"Indicador: {indicador}")
    print(f"Fecha de creación: {fecha_creacion}")
    print(f"Fecha de modificación: {fecha_modificacion}")
    print(f"Raza: {raza}")


# Función para actualizar pygame_gui
def actualizar_gui(evento):

    MANAGER.process_events(evento)
    MANAGER.update(clock.get_time() / 1000.0)
    MANAGER.draw_ui(ventana)

# Función que dibuja la pantalla general
def dibujar_pantalla_general():
    ventana.fill(FONDO_COLOR)  # Rellenar con el color de fondo

    # Dibujar la imagen del título
    ventana.blit(titulo_crearcarta, (ANCHO_VENTANA // 2 - titulo_crearcarta.get_width() // 2, 20))

    # Dibujar la imagen de los bloques de información
    ventana.blit(info_bloques, (ANCHO_VENTANA * 0.1, ALTO_VENTANA * 0.2))

    # Dibujar la imagen actual
    ventana.blit(imagen_actual, posicion_imagen)





# Loop principal
ejecutando = True
while ejecutando:
    UI_REFRESH_RATE = clock.tick(60) / 1000
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            ejecutando = False


        elif evento.type == pygame.VIDEORESIZE:
            ANCHO_VENTANA, ALTO_VENTANA = evento.w, evento.h
            ventana = pygame.display.set_mode((ANCHO_VENTANA, ALTO_VENTANA), pygame.RESIZABLE)
        # Evento para abrir el diálogo de imagen al hacer clic en la imagen de arrastrar
        elif evento.type == pygame.MOUSEBUTTONDOWN:
            if evento.button == 1:  # Botón izquierdo
                mouse_x, mouse_y = evento.pos
                rect_arrastrar = imagen_actual.get_rect(topleft=posicion_imagen)
                if rect_arrastrar.collidepoint(mouse_x, mouse_y):
                    ruta_imagen = abrir_dialogo_imagen()  # Abre el diálogo para seleccionar una imagen
                    if ruta_imagen:  # Si se seleccionó una imagen
                        ruta_guardada = guardar_imagen_seleccionada(ruta_imagen)  # Guardar la imagen en la carpeta

                        # Cargar la imagen guardada
                        imagen_cargada = Image.open(ruta_guardada)
                        imagen_cargada = imagen_cargada.convert("RGBA")  # Convertir a RGBA para Pygame
                        imagen_cargada = pygame.image.fromstring(imagen_cargada.tobytes(), imagen_cargada.size,
                                                                 imagen_cargada.mode)
                        imagen_actual = redimensionar_imagen(imagen_cargada, 455)  # Redimensionar la nueva imagen
            MANAGER.process_events(evento)
        # Verificar si el botón "Guardar" fue presionado
        if evento.type == pygame_gui.UI_BUTTON_PRESSED:
            if evento.ui_element == boton_guardar:
                guardar_datos()  # Llamar a la función para guardar los datos

    actualizar_gui(evento)

    dibujar_pantalla_general()

    MANAGER.draw_ui(ventana)

    pygame.display.update()

pygame.quit()

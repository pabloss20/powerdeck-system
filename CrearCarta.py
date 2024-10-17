import pygame
import os
import tkinter as tk
from tkinter import filedialog
from PIL import Image
import shutil
import pygame_gui
from commctrl import UPDOWN_CLASS
from pygame_gui.core import ObjectID
from Model.Carta import Carta, Atributos, Raza, Tipo_de_Carta

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
pantalla = 0
imagen_seleccionada = ''

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
info2 = pygame.image.load(os.path.join(ruta_imagenes, 'info2.png'))
info3 = pygame.image.load(os.path.join(ruta_imagenes, 'info3.png'))
info4 = pygame.image.load(os.path.join(ruta_imagenes, 'info4.png'))
info5 = pygame.image.load(os.path.join(ruta_imagenes, 'info5.png'))

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
info_second = redimensionar_imagen(info2, 400)
info_third = redimensionar_imagen(info3, 400)
info_fourth = redimensionar_imagen(info4, 400)
info_fifth = redimensionar_imagen(info5, 400)

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
    pygame_gui.elements.UIDropDownMenu(
        starting_option="Humano",
        options_list=["Humano", "Élfico", "Enano", "Orco", "Bestia"],
        relative_rect=pygame.Rect((600, ALTO_VENTANA * 0.83, 350, 42)), manager=MANAGER,
        object_id=ObjectID(class_id='@campoTXT',object_id="input7"))
]
select_boxes = [
    pygame_gui.elements.UIDropDownMenu(
        options_list=["Ultra-Rara", "Muy-Rara", "Rara", "Normal", "Básica"],
        starting_option="Normal",
        relative_rect=pygame.Rect((600, ALTO_VENTANA * 0.26, 350, 42)),
        manager=MANAGER,
        object_id=ObjectID(class_id='@campoTXT', object_id="select1")
    ),
    pygame_gui.elements.UIDropDownMenu(
        options_list=["Activa", "Inactiva"],
        starting_option="Activa",
        relative_rect=pygame.Rect((600, ALTO_VENTANA * 0.41, 350, 42)),
        manager=MANAGER,
        object_id=ObjectID(class_id='@campoTXT', object_id="select2")
    ),
    pygame_gui.elements.UIDropDownMenu(
        options_list=["Activa", "Inactiva"],
        starting_option="Activa",
        relative_rect=pygame.Rect((600, ALTO_VENTANA * 0.58, 350, 42)),
        manager=MANAGER,
        object_id=ObjectID(class_id='@campoTXT', object_id="select3")
    ),
    pygame_gui.elements.UITextEntryLine(
        relative_rect=pygame.Rect((600, ALTO_VENTANA * 0.69, 350, 42)), manager=MANAGER,
        object_id=ObjectID(class_id='@campoTXT',object_id="input8")),
    pygame_gui.elements.UITextEntryLine(
        relative_rect=pygame.Rect((600, ALTO_VENTANA * 0.77, 350, 42)), manager=MANAGER,
        object_id=ObjectID(class_id='@campoTXT',object_id="input9"))
]
# Crear instancias de UITextEntryLine en lugar de las cajas de texto tradicionales
text_input_p3 = [
    pygame_gui.elements.UITextEntryLine(
        relative_rect=pygame.Rect((600, ALTO_VENTANA * 0.26, 350, 42)), manager=MANAGER,
        object_id=ObjectID(class_id='@campoTXT',object_id="input1")),
    pygame_gui.elements.UITextEntryBox(
        relative_rect=pygame.Rect((600, ALTO_VENTANA * 0.34, 350, 42)), manager=MANAGER,object_id=ObjectID(class_id='@campoTXT',object_id="input2")),
    pygame_gui.elements.UITextEntryBox(
            relative_rect=pygame.Rect((600, ALTO_VENTANA * 0.41, 350, 42)), manager=MANAGER,
            object_id=ObjectID(class_id='@campoTXT', object_id="input2")),
    pygame_gui.elements.UITextEntryBox(
        relative_rect=pygame.Rect((600, ALTO_VENTANA * 0.48, 350, 42)), manager=MANAGER,
        object_id=ObjectID(class_id='@campoTXT', object_id="input17")),
    pygame_gui.elements.UITextEntryLine(
        relative_rect=pygame.Rect((600, ALTO_VENTANA * 0.55, 350, 42)), manager=MANAGER,
        object_id=ObjectID(class_id='@campoTXT',object_id="input18")),
    pygame_gui.elements.UITextEntryLine(
        relative_rect=pygame.Rect((600, ALTO_VENTANA * 0.62, 350, 42)), manager=MANAGER,
        object_id=ObjectID(class_id='@campoTXT',object_id="input4")),
    pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((600, ALTO_VENTANA * 0.69, 350, 42)),
                                        manager=MANAGER, object_id=ObjectID(class_id='@campoTXT',object_id="input5")),
    pygame_gui.elements.UITextEntryLine(
        relative_rect=pygame.Rect((600, ALTO_VENTANA * 0.76, 350, 42)), manager=MANAGER,
        object_id=ObjectID(class_id='@campoTXT',object_id="input6")),
    pygame_gui.elements.UITextEntryLine(
        relative_rect=pygame.Rect((600, ALTO_VENTANA * 0.83, 350, 42)), manager=MANAGER,
        object_id=ObjectID(class_id='@campoTXT',object_id="input7"))
]
# Crear instancias de UITextEntryLine en lugar de las cajas de texto tradicionales
text_input_p4 = [
    pygame_gui.elements.UITextEntryLine(
        relative_rect=pygame.Rect((600, ALTO_VENTANA * 0.26, 350, 42)), manager=MANAGER,
        object_id=ObjectID(class_id='@campoTXT',object_id="input8")),
    pygame_gui.elements.UITextEntryBox(
        relative_rect=pygame.Rect((600, ALTO_VENTANA * 0.34, 350, 42)), manager=MANAGER,object_id=ObjectID(class_id='@campoTXT',object_id="input2")),
    pygame_gui.elements.UITextEntryBox(
            relative_rect=pygame.Rect((600, ALTO_VENTANA * 0.41, 350, 42)), manager=MANAGER,object_id=ObjectID(class_id='@campoTXT',object_id="input19")),
    pygame_gui.elements.UITextEntryBox(
            relative_rect=pygame.Rect((600, ALTO_VENTANA * 0.48, 350, 42)), manager=MANAGER,object_id=ObjectID(class_id='@campoTXT',object_id="input20")),
    pygame_gui.elements.UITextEntryLine(
        relative_rect=pygame.Rect((600, ALTO_VENTANA * 0.55, 350, 42)), manager=MANAGER,
        object_id=ObjectID(class_id='@campoTXT',object_id="input9")),
    pygame_gui.elements.UITextEntryLine(
        relative_rect=pygame.Rect((600, ALTO_VENTANA * 0.62, 350, 42)), manager=MANAGER,
        object_id=ObjectID(class_id='@campoTXT',object_id="input10")),
    pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((600, ALTO_VENTANA * 0.69, 350, 42)),
                                        manager=MANAGER, object_id=ObjectID(class_id='@campoTXT',object_id="input5")),
    pygame_gui.elements.UITextEntryLine(
        relative_rect=pygame.Rect((600, ALTO_VENTANA * 0.76, 350, 42)), manager=MANAGER,
        object_id=ObjectID(class_id='@campoTXT',object_id="input11")),
    pygame_gui.elements.UITextEntryLine(
        relative_rect=pygame.Rect((600, ALTO_VENTANA * 0.83, 350, 42)), manager=MANAGER,
        object_id=ObjectID(class_id='@campoTXT',object_id="input12"))
]
# Crear instancias de UITextEntryLine en lugar de las cajas de texto tradicionales
text_input_p5 = [
    pygame_gui.elements.UITextEntryLine(
        relative_rect=pygame.Rect((600, ALTO_VENTANA * 0.26, 350, 42)), manager=MANAGER,
        object_id=ObjectID(class_id='@campoTXT',object_id="input13")),
    pygame_gui.elements.UITextEntryBox(
        relative_rect=pygame.Rect((600, ALTO_VENTANA * 0.34, 350, 42)), manager=MANAGER,object_id=ObjectID(class_id='@campoTXT',object_id="input2")),
    pygame_gui.elements.UITextEntryBox(
        relative_rect=pygame.Rect((600, ALTO_VENTANA * 0.41, 350, 42)), manager=MANAGER,
        object_id=ObjectID(class_id='@campoTXT', object_id="input21")),
    pygame_gui.elements.UITextEntryBox(
        relative_rect=pygame.Rect((600, ALTO_VENTANA * 0.48, 350, 42)), manager=MANAGER,
        object_id=ObjectID(class_id='@campoTXT', object_id="input22")),

    pygame_gui.elements.UITextEntryLine(
        relative_rect=pygame.Rect((600, ALTO_VENTANA * 0.55, 350, 42)), manager=MANAGER,
        object_id=ObjectID(class_id='@campoTXT',object_id="input14")),
    pygame_gui.elements.UITextEntryLine(
        relative_rect=pygame.Rect((600, ALTO_VENTANA * 0.62, 350, 42)), manager=MANAGER,
        object_id=ObjectID(class_id='@campoTXT',object_id="input15")),
    pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((600, ALTO_VENTANA * 0.69, 350, 42)),
                                        manager=MANAGER, object_id=ObjectID(class_id='@campoTXT',object_id="input5")),
    pygame_gui.elements.UITextEntryLine(
        relative_rect=pygame.Rect((600, ALTO_VENTANA * 0.76, 350, 42)), manager=MANAGER,
        object_id=ObjectID(class_id='@campoTXT',object_id="input16")),
]

# Añadir el botón de guardar
boton_guardar = pygame_gui.elements.UIButton(
    relative_rect=pygame.Rect((500, ALTO_VENTANA * 0.9, 100, 40)),
    text='Guardar',
    manager=MANAGER
)
boton_siguiente = pygame_gui.elements.UIButton(
    relative_rect=pygame.Rect((700, ALTO_VENTANA * 0.9, 100, 40)),
    text='Siguiente',
    manager=MANAGER
)
boton_atras = pygame_gui.elements.UIButton(
    relative_rect=pygame.Rect((600, ALTO_VENTANA * 0.9, 100, 40)),
    text='Atras',
    manager=MANAGER
)
def hideshow():
    if pantalla == 4:
        boton_siguiente.hide()
    elif pantalla == 0:
        boton_atras.hide()
    else:
        boton_siguiente.show()
        boton_atras.show()
def guardar_datos():
    try:
        # Obtener los valores de los campos de texto
        nombre_personaje = text_input_boxes[0].get_text()
        descripcion = text_input_boxes[1].get_text()
        nombre_variante = text_input_boxes[2].get_text()
        raza_str = text_input_boxes[6].selected_option[0]
        tipo_carta_str = select_boxes[0].selected_option[0]  # Tipo de carta
        turno_poder = int(select_boxes[3].get_text())  # Convertir a entero
        bonus_poder = int(select_boxes[4].get_text())  # Convertir a entero

        # Atributos
        atributos = Atributos(
            poder=int(text_input_p3[0].get_text()),
            velocidad=int(text_input_p3[1].get_text()),
            magia=int(text_input_p3[2].get_text()),
            defensa=int(text_input_p3[3].get_text()),
            inteligencia=int(text_input_p3[4].get_text()),
            altura=int(text_input_p3[5].get_text()),
            fuerza=int(text_input_p3[6].get_text()),
            agilidad=int(text_input_p3[7].get_text()),
            salto=int(text_input_p3[8].get_text()),
            resistencia=int(text_input_p4[0].get_text()),
            flexibilidad=int(text_input_p4[1].get_text()),
            explosividad=int(text_input_p4[2].get_text()),
            carisma=int(text_input_p4[3].get_text()),
            habilidad=int(text_input_p4[4].get_text()),
            balance=int(text_input_p4[5].get_text()),
            sabiduría=int(text_input_p4[6].get_text()),
            suerte=int(text_input_p4[7].get_text()),
            coordinacion=int(text_input_p4[8].get_text()),
            amabilidad=int(text_input_p5[0].get_text()),
            lealtad=int(text_input_p5[1].get_text()),
            disciplina=int(text_input_p5[2].get_text()),
            liderazgo=int(text_input_p5[3].get_text()),
            prudencia=int(text_input_p5[4].get_text()),
            confianza=int(text_input_p5[5].get_text()),
            percepcion=int(text_input_p5[6].get_text()),
            valentía=int(text_input_p5[7].get_text())
        )

        # Convertir el string de raza y tipo de carta a los correspondientes enums
        raza = Raza[raza_str.upper()]  # Asegúrate que coincida con los nombres en el Enum
        tipo_carta = Tipo_de_Carta[tipo_carta_str.replace('-', '_').upper()]

        # Crear una nueva instancia de la clase Carta
        nueva_carta = Carta(
            nombre_personaje=nombre_personaje,
            descripcion=descripcion,
            nombre_variante=nombre_variante,
            raza=raza,
            imagen=imagen_seleccionada,  # Aquí deberías poner el path de la imagen que seleccionas
            tipo_carta=tipo_carta,
            turno_poder=turno_poder,
            bonus_poder=bonus_poder,
            atributos=atributos
        )

        # Confirmación de que la carta fue creada
        print(f"Carta creada: {nueva_carta.nombre_personaje}, {nueva_carta.llave}")
    except Exception as e:
        print(e)




# Función para actualizar pygame_gui
def actualizar_gui(evento):
    MANAGER.process_events(evento)
    MANAGER.update(clock.get_time() / 1000.0)

# Función que dibuja la pantalla general
def dibujar_pantalla_general():

    ventana.fill(FONDO_COLOR)  # Rellenar con el color de fondo

    # Dibujar la imagen del título
    ventana.blit(titulo_crearcarta, (ANCHO_VENTANA // 2 - titulo_crearcarta.get_width() // 2, 20))

    # Dibujar la imagen de los bloques de información
    if pantalla == 0:
        ventana.blit(info_bloques, (ANCHO_VENTANA * 0.1, ALTO_VENTANA * 0.2))
    elif pantalla == 1:
        # Dibujar la imagen de los bloques de información
        ventana.blit(info_second, (ANCHO_VENTANA * 0.1, ALTO_VENTANA * 0.2))
    elif pantalla == 2:
        ventana.blit(info_third, (ANCHO_VENTANA * 0.1, ALTO_VENTANA * 0.2))
    elif pantalla == 3:
        ventana.blit(info_fourth, (ANCHO_VENTANA * 0.1, ALTO_VENTANA * 0.2))
    elif pantalla == 4:
        ventana.blit(info_fifth, (ANCHO_VENTANA * 0.1, ALTO_VENTANA * 0.2))

    # Dibujar la imagen actual
    ventana.blit(imagen_actual, posicion_imagen)


# Función para activar o desactivar los inputboxes según la pantalla
def cambiar_visibilidad_inputboxes():
    for inputbox in text_input_boxes:
        if pantalla == 0:
            inputbox.show()
        else:
            inputbox.hide()
    for select in select_boxes:
        if pantalla == 1:
            select.show()
        else:
            select.hide()
    for inputbox in text_input_p3:
        if pantalla == 2:
            inputbox.show()
        else:
            inputbox.hide()
    for inputbox in text_input_p4:
        if pantalla == 3:
            inputbox.show()
        else:
            inputbox.hide()
    for inputbox in text_input_p5:
        if pantalla == 4:
            inputbox.show()
        else:
            inputbox.hide()




# Loop principal
ejecutando = True
while ejecutando:
    UI_REFRESH_RATE = clock.tick(60) / 1000
    for evento in pygame.event.get():
        actualizar_gui(evento)
        if evento.type == pygame.QUIT:
            ejecutando = False

        elif evento.type == pygame.VIDEORESIZE:
            ANCHO_VENTANA, ALTO_VENTANA = evento.w, evento.h
            ventana = pygame.display.set_mode((ANCHO_VENTANA, ALTO_VENTANA), pygame.RESIZABLE)

        elif evento.type == pygame.MOUSEBUTTONDOWN:
            if evento.button == 1:  # Botón izquierdo
                mouse_x, mouse_y = evento.pos
                rect_arrastrar = imagen_actual.get_rect(topleft=posicion_imagen)
                if rect_arrastrar.collidepoint(mouse_x, mouse_y):
                    ruta_imagen = abrir_dialogo_imagen()  # Abre el diálogo para seleccionar una imagen
                    if ruta_imagen:  # Si se seleccionó una imagen
                        ruta_guardada = guardar_imagen_seleccionada(ruta_imagen)  # Guardar la imagen en la carpeta
                        imagen_seleccionada = ruta_guardada
                        # Cargar y redimensionar la nueva imagen
                        imagen_cargada = Image.open(ruta_guardada)
                        imagen_cargada = imagen_cargada.convert("RGBA")  # Convertir a RGBA para Pygame
                        imagen_cargada = pygame.image.fromstring(imagen_cargada.tobytes(), imagen_cargada.size, imagen_cargada.mode)
                        imagen_actual = redimensionar_imagen(imagen_cargada, 455)  # Redimensionar la nueva imagen

        if evento.type == pygame_gui.UI_BUTTON_PRESSED:
            if evento.ui_element == boton_guardar:
                guardar_datos()  # Llamar a la función para guardar los datos
            elif evento.ui_element == boton_siguiente:
                pantalla += 1
            elif evento.ui_element == boton_atras:
                pantalla -= 1



    hideshow()
    ventana.fill(FONDO_COLOR)  # Rellenar con el color de fondo
    cambiar_visibilidad_inputboxes()
    dibujar_pantalla_general()





    # Solo dibujar los inputboxes si mostrar_inputboxes es True
    MANAGER.draw_ui(ventana)

    pygame.display.update()

pygame.quit()

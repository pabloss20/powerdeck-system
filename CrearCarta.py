import pygame
import pygame_textinput

# Inicializar Pygame
pygame.init()

# Definir colores
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
GRIS_CLARO = (200, 200, 200)
AZUL_CLARO = (173, 216, 230)

# Definir el tamaño inicial de la ventana
ANCHO_VENTANA = 800
ALTO_VENTANA = 600
ventana = pygame.display.set_mode((ANCHO_VENTANA, ALTO_VENTANA), pygame.RESIZABLE)
pygame.display.set_caption('Power Deck - Herramienta de Cartas')

# Fuentes
FUENTE_MEDIANA = pygame.font.Font(None, 40)
FUENTE_PEQUEÑA = pygame.font.Font(None, 30)

# Crear una clase para manejar los inputs de texto
class InputBox:
    def __init__(self, x, y, w, h, text=''):
        self.rect = pygame.Rect(x, y, w, h)
        self.color_inactive = GRIS_CLARO
        self.color_active = AZUL_CLARO
        self.color = self.color_inactive
        self.text = text
        self.txt_surface = FUENTE_MEDIANA.render(text, True, NEGRO)
        self.active = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Si el usuario hace clic en el input
            if self.rect.collidepoint(event.pos):
                self.active = not self.active
            else:
                self.active = False
            # Cambia el color del campo según si está activo
            self.color = self.color_active if self.active else self.color_inactive

        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    print(self.text)  # Puedes manejar el envío aquí
                    self.text = ''
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                # Renderizar de nuevo la superficie del texto
                self.txt_surface = FUENTE_MEDIANA.render(self.text, True, NEGRO)


def dibujar_boton(texto, x, y, ancho, alto, color_fondo, color_texto):
    pygame.draw.rect(ventana, color_fondo, [x, y, ancho, alto])
    texto_boton = FUENTE_MEDIANA.render(texto, True, color_texto)
    ventana.blit(texto_boton, (x + (ancho - texto_boton.get_width()) // 2, y + (alto - texto_boton.get_height()) // 2))


def dibujar_input(texto, x, y, ancho, alto):
    pygame.draw.rect(ventana, GRIS_CLARO, [x, y, ancho, alto], 2)
    texto_input = FUENTE_PEQUEÑA.render(texto, True, NEGRO)
    ventana.blit(texto_input, (x + 5, y + 5))


def dibujar_area_imagen(x, y, ancho, alto):
    pygame.draw.rect(ventana, GRIS_CLARO, [x, y, ancho, alto], 2)
    texto_imagen = FUENTE_PEQUEÑA.render("Arrastrar imagen aquí", True, NEGRO)
    ventana.blit(texto_imagen, (x + 20, y + 20))


def dibujar_pantalla_general(titulo_texto, campos, ancho_ventana, alto_ventana):
    ventana.fill(BLANCO)

    # Proporciones y posiciones relativas
    margen_x = int(ancho_ventana * 0.05)
    margen_y = int(alto_ventana * 0.1)
    ancho_columna = int(ancho_ventana * 0.4)  # Ancho total para las dos columnas de campos
    ancho_subcolumna = int(ancho_columna * 0.45)  # Sub-columna para etiquetas e inputs
    alto_input = int(alto_ventana * 0.07)
    espacio_entre_campos = int(alto_ventana * 0.03)

    # Título
    titulo = FUENTE_MEDIANA.render(titulo_texto, True, NEGRO)
    ventana.blit(titulo, (ancho_ventana // 2 - titulo.get_width() // 2, margen_y - 60))

    # Dibujar los campos de texto en dos sub-columnas
    for i, campo in enumerate(campos):
        fila = i  # Usamos el índice directamente como fila
        x_label = margen_x  # Columna izquierda (etiquetas)
        x_input = margen_x + ancho_subcolumna + 10  # Columna derecha (inputs)
        y = margen_y + fila * (alto_input + espacio_entre_campos)

        # Dibujar la etiqueta (izquierda)
        dibujar_input(campo["label"], x_label, y, ancho_subcolumna, alto_input)

        # Dibujar el input (derecha)
        dibujar_input(campo["input"], x_input, y, ancho_subcolumna, alto_input)

    # Área de imagen en la segunda columna (derecha)
    x_area_imagen = int(ancho_ventana * 0.55)  # Comienza la segunda columna principal
    y_area_imagen = margen_y
    ancho_area_imagen = int(ancho_ventana * 0.35)
    alto_area_imagen = int(alto_ventana * 0.6)
    dibujar_area_imagen(x_area_imagen, y_area_imagen, ancho_area_imagen, alto_area_imagen)

    # Botón "Subir" debajo del área de imagen
    ancho_boton_subir = int(ancho_ventana * 0.15)
    alto_boton_subir = int(alto_ventana * 0.07)
    x_boton_subir = x_area_imagen + (ancho_area_imagen - ancho_boton_subir) // 2
    y_boton_subir = y_area_imagen + alto_area_imagen + 20
    dibujar_boton("Subir", x_boton_subir, y_boton_subir, ancho_boton_subir, alto_boton_subir, GRIS_CLARO, NEGRO)

    # Dibujar el botón "Siguiente"
    ancho_boton = int(ancho_ventana * 0.2)
    alto_boton = int(alto_ventana * 0.08)
    x_boton = int(ancho_ventana * 0.3)
    y_boton = int(alto_ventana * 0.85)
    dibujar_boton("Siguiente", x_boton, y_boton, ancho_boton, alto_boton, AZUL_CLARO, NEGRO)


def pantalla_1(ancho_ventana, alto_ventana):
    # Estructura de campos corregida con diccionarios que tienen 'label' e 'input'
    campos = [
        {"label": "Nombre del personaje:", "input": "Input"},
        {"label": "Descripción:", "input": "Input"},
        {"label": "Nombre de Variante:", "input": "Input"},
        {"label": "Indicador:", "input": "auto"},
        {"label": "Fecha de creación:", "input": "2024/09/02"},
        {"label": "Fecha de modificación:", "input": "2024/09/02"},
        {"label": "Raza:", "input": "Input"}
    ]

    # Llamada a la función de dibujar la pantalla con los campos correctamente formateados
    dibujar_pantalla_general("Pantalla 1 - Información Principal", campos, ancho_ventana, alto_ventana)



def pantalla_2(ancho_ventana, alto_ventana):
    # Estructura de campos corregida con diccionarios que tienen 'label' e 'input'
    campos = [
        {"label": "Rareza de carta:", "input": "Input"},
        {"label": "Descripción:", "input": "Input"},
        {"label": "Nombre de Variante:", "input": "Input"},
        {"label": "Indicador:", "input": "auto"},
        {"label": "Fecha de creación:", "input": "2024/09/02"},
        {"label": "Fecha de modificación:", "input": "2024/09/02"},
        {"label": "Raza:", "input": "Input"}
    ]

    # Llamada a la función de dibujar la pantalla con los campos correctamente formateados
    dibujar_pantalla_general("Pantalla 1 - Información Principal", campos, ancho_ventana, alto_ventana)

def pantalla_3():
    campos = ["Poder", "Velocidad", "Magia", "Defensa", "Fuerza", "Agilidad",
              "Resistencia", "Inteligencia", "Altura", "Salto", "Flexibilidad", "Carisma"]
    dibujar_pantalla_general("Pantalla 3 - Atributos de la Carta", campos, "Siguiente")


def pantalla_4():
    campos = ["Sabiduria", "Suerte", "Coordinacion", "Amabilidad", "Lealtad", "Disciplina",
              "Liderazgo", "Prudencia", "Confianza", "Percepcion", "Valentia", "PoderTotal"]
    dibujar_pantalla_general("Pantalla 4 - Atributos", campos, "Subir", GRIS_CLARO)


# Loop principal
pantalla_actual = 1
ejecutando = True
while ejecutando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            ejecutando = False
        elif evento.type == pygame.VIDEORESIZE:  # Detecta cuando se redimensiona la ventana
            ANCHO_VENTANA, ALTO_VENTANA = evento.w, evento.h
            ventana = pygame.display.set_mode((ANCHO_VENTANA, ALTO_VENTANA), pygame.RESIZABLE)
        elif evento.type == pygame.MOUSEBUTTONDOWN:
            # Obtener la posición del clic
            pos = pygame.mouse.get_pos()
            # Comprobar si se ha hecho clic en el botón "Siguiente"
            ancho_boton = int(ANCHO_VENTANA * 0.2)
            alto_boton = int(ALTO_VENTANA * 0.08)
            x_boton = int(ANCHO_VENTANA * 0.7)
            y_boton = int(ALTO_VENTANA * 0.85)
            if x_boton <= pos[0] <= x_boton + ancho_boton and y_boton <= pos[1] <= y_boton + alto_boton:
                pantalla_actual = 1 if pantalla_actual >= 4 else pantalla_actual + 1
    # Dibujar la pantalla actual
    if pantalla_actual == 1:
        pantalla_1(ANCHO_VENTANA, ALTO_VENTANA)
    elif pantalla_actual == 2:
        pantalla_2()
    elif pantalla_actual == 3:
        pantalla_3()
    elif pantalla_actual == 4:
        pantalla_4()
    pygame.display.update()

# Salir de Pygame
pygame.quit()
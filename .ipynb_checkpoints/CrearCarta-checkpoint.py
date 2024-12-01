import pygame

# Inicializar Pygame
pygame.init()

# Definir colores
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
GRIS_CLARO = (200, 200, 200)
AZUL_CLARO = (173, 216, 230)

# Definir el tamaño de la ventana
ANCHO_VENTANA = 800
ALTO_VENTANA = 600
ventana = pygame.display.set_mode((ANCHO_VENTANA, ALTO_VENTANA), pygame.RESIZABLE)
pygame.display.set_caption('Power Deck - Herramienta de Cartas')

# Fuentes
FUENTE_MEDIANA = pygame.font.Font(None, 40)
FUENTE_PEQUEÑA = pygame.font.Font(None, 30)

# Constantes de posición de botones
POS_BOTON_X = 600
POS_BOTON_Y = 500
ANCHO_BOTON = 150
ALTO_BOTON = 50


# Clase para los campos de texto
class CampoTexto:
    def __init__(self, x, y, ancho, alto, texto=''):
        self.rect = pygame.Rect(x, y, ancho, alto)
        self.color = GRIS_CLARO
        self.texto = texto
        self.texto_mostrado = FUENTE_PEQUEÑA.render(self.texto, True, NEGRO)
        self.activo = False

    def dibujar(self):
        # Dibujar el cuadro del campo de texto
        pygame.draw.rect(ventana, self.color, self.rect, 2)
        # Mostrar el texto dentro del cuadro
        ventana.blit(self.texto_mostrado, (self.rect.x + 5, self.rect.y + 5))

    def manejar_evento(self, evento):
        if evento.type == pygame.MOUSEBUTTONDOWN:
            # Detectar si se ha hecho clic en el campo
            if self.rect.collidepoint(evento.pos):
                self.activo = True
                self.color = AZUL_CLARO
            else:
                self.activo = False
                self.color = GRIS_CLARO
        if evento.type == pygame.KEYDOWN:
            if self.activo:
                if evento.key == pygame.K_BACKSPACE:
                    # Borrar el último carácter
                    self.texto = self.texto[:-1]
                else:
                    # Agregar el nuevo carácter al texto
                    self.texto += evento.unicode
                # Actualizar el texto mostrado
                self.texto_mostrado = FUENTE_PEQUEÑA.render(self.texto, True, NEGRO)


# Función para dibujar los campos y los inputs
def dibujar_pantalla_general(titulo_texto, etiquetas, campos_input, atributo_boton, color_boton=AZUL_CLARO):
    ventana.fill(BLANCO)

    # Título
    titulo = FUENTE_MEDIANA.render(titulo_texto, True, NEGRO)
    ventana.blit(titulo, (ANCHO_VENTANA // 2 - titulo.get_width() // 2, 50))

    # Dibujar etiquetas y cuadros de entrada en dos columnas
    for i, etiqueta in enumerate(etiquetas):
        y_pos = 150 + i * 50  # Posición vertical (incrementa para cada fila)

        # Columna izquierda: etiquetas
        etiqueta_texto = FUENTE_PEQUEÑA.render(etiqueta, True, NEGRO)
        ventana.blit(etiqueta_texto, (50, y_pos))  # Etiqueta en la izquierda (columna 1)

        # Columna central: cuadros de texto
        campos_input[i].dibujar()

    # Dibujar botón "Siguiente"
    dibujar_boton(atributo_boton, POS_BOTON_X, POS_BOTON_Y, ANCHO_BOTON, ALTO_BOTON, color_boton, NEGRO)


# Crear las pantallas con etiquetas y campos de texto interactivos
def pantalla_1():
    etiquetas = [
        "Nombre del personaje:", "Descripción:", "Nombre de variante:", "Indicador:",
        "Fecha de creación:", "Fecha de modificación:", "Raza:"
    ]
    campos_input = [
        CampoTexto(300, 150, 300, 40),  # Posición de la columna central (columna 2)
        CampoTexto(300, 200, 300, 80),
        CampoTexto(300, 250, 300, 40),
        CampoTexto(300, 300, 300, 40),
        CampoTexto(300, 350, 300, 40),
        CampoTexto(300, 400, 300, 40),
        CampoTexto(300, 450, 300, 40),
    ]
    return etiquetas, campos_input


def pantalla_2():
    etiquetas = [
        "Raridad de la carta:", "Atributo de Activa/Inactiva en juego:", "Activa/Inactiva en sobres:",
        "Turno de Poder:", "Bonus de Poder:"
    ]
    campos_input = [
        CampoTexto(300, 150, 300, 40),  # Inputs en la columna del medio
        CampoTexto(300, 200, 300, 40),
        CampoTexto(300, 250, 300, 40),
        CampoTexto(300, 300, 300, 40),
        CampoTexto(300, 350, 300, 40),
    ]
    return etiquetas, campos_input


def pantalla_3():
    etiquetas = [
        "Poder:", "Velocidad:", "Magia:", "Defensa:", "Fuerza:", "Agilidad:"
    ]
    campos_input = [
        CampoTexto(300, 150, 300, 40),
        CampoTexto(300, 200, 300, 40),
        CampoTexto(300, 250, 300, 40),
        CampoTexto(300, 300, 300, 40),
        CampoTexto(300, 350, 300, 40),
        CampoTexto(300, 400, 300, 40),
    ]
    return etiquetas, campos_input


# Dibujar botón
def dibujar_boton(texto, x, y, ancho, alto, color_fondo, color_texto):
    pygame.draw.rect(ventana, color_fondo, [x, y, ancho, alto])
    texto_boton = FUENTE_MEDIANA.render(texto, True, color_texto)
    ventana.blit(texto_boton, (x + (ancho - texto_boton.get_width()) // 2, y + (alto - texto_boton.get_height()) // 2))


# Loop principal
pantalla_actual = 1
etiquetas, campos_input = pantalla_1()
ejecutando = True

while ejecutando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            ejecutando = False
        for campo in campos_input:
            campo.manejar_evento(evento)
        if evento.type == pygame.MOUSEBUTTONDOWN:
            # Obtener la posición del clic
            pos = pygame.mouse.get_pos()
            # Comprobar si se ha hecho clic en el botón "Siguiente"
            if POS_BOTON_X <= pos[0] <= POS_BOTON_X + ANCHO_BOTON and POS_BOTON_Y <= pos[1] <= POS_BOTON_Y + ALTO_BOTON:
                if pantalla_actual == 1:
                    pantalla_actual = 2
                    etiquetas, campos_input = pantalla_2()
                elif pantalla_actual == 2:
                    pantalla_actual = 3
                    etiquetas, campos_input = pantalla_3()
                else:
                    pantalla_actual = 1
                    etiquetas, campos_input = pantalla_1()

    # Dibujar la pantalla actual
    dibujar_pantalla_general(f"Pantalla {pantalla_actual}", etiquetas, campos_input, "Siguiente")

    pygame.display.update()

# Salir de Pygame
pygame.quit()

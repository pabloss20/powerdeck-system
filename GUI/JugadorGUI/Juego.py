import pygame
import sys

def main():

    pygame.init()

    # Colores
    NEGRO = (0, 0, 0)
    BLANCO = (255, 255, 255)
    AZUL_CLARO = (100, 149, 237)

    ANCHO = 1820
    ALTO = 900

    # Crear la ventana
    ventana = pygame.display.set_mode((ANCHO, ALTO), pygame.RESIZABLE)
    pygame.display.set_caption('PowerDeck App')

    # Fuentes
    fuente_texto = pygame.font.Font(None, 50)

    # Variables de estado
    pantalla_actual = "principal"

    # Función para dibujar un botón
    def dibujar_boton(texto, x, y, ancho, alto, color_borde, color_fondo, ventana):
        pygame.draw.rect(ventana, color_fondo, (x, y, ancho, alto))
        pygame.draw.rect(ventana, color_borde, (x, y, ancho, alto), 5)
        ventana.blit(texto, (x + (ancho - texto.get_width()) // 2, y + (alto - texto.get_height()) // 2))

    # Función para mostrar la pantalla principal
    def pantalla_principal():
        # Dibujar título
        titulo = fuente_texto.render('POWER DECK', True, BLANCO)
        subtitulo = fuente_texto.render('HERRAMIENTA DE CARTAS', True, BLANCO)
        ventana.blit(titulo, ((ANCHO - titulo.get_width()) // 2, 50))
        ventana.blit(subtitulo, ((ANCHO - subtitulo.get_width()) // 2, 130))

        # Dibujar botones
        dibujar_boton(fuente_texto.render('Registrarse', True, BLANCO),
                      ANCHO // 2 - 150, ALTO // 2 - 100, 300, 100, AZUL_CLARO, NEGRO, ventana)

        dibujar_boton(fuente_texto.render('Iniciar Sesión', True, BLANCO),
                      ANCHO // 2 - 150, ALTO // 2 + 50, 300, 100, AZUL_CLARO, NEGRO, ventana)

    # Bucle principal
    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # Manejar eventos de la pantalla actual
            if pantalla_actual == "principal":
                if evento.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    # Verificar si se ha hecho clic en el botón "Crear Carta"
                    if ANCHO // 2 - 150 <= mouse_pos[0] <= ANCHO // 2 + 150 and ALTO // 2 - 100 <= mouse_pos[1] <= ALTO // 2:
                        pantalla_actual = "crear_carta"  # Cambiar a la pantalla de creación de cartas
                    # Verificar si se ha hecho clic en el botón "Ver Álbum"
                    elif ANCHO // 2 - 150 <= mouse_pos[0] <= ANCHO // 2 + 150 and ALTO // 2 + 50 <= mouse_pos[1] <= ALTO // 2 + 150:
                        pantalla_actual = "ver_album"  # Cambiar a la pantalla del álbum
            elif pantalla_actual == "crear_carta":
                pass
            elif pantalla_actual == "ver_album":
                pass

        # Rellenar la pantalla de negro
        ventana.fill(NEGRO)

        # Dibujar la pantalla correspondiente
        if pantalla_actual == "principal":
            pantalla_principal()
        elif pantalla_actual == "crear_carta":
           pass
        elif pantalla_actual == "ver_album":

            pass

        # Actualizar la pantalla
        pygame.display.update()

if __name__ == "__main__":
    main()
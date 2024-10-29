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
    campos_texto = {
        "nombre": "",
        "apellido": "",
        "correo": "",
        "contrasena": "",
        "confirmar_contrasena": "",
        "edad": "",
        "usuario": ""
    }
    cursor_visible = True
    reloj = pygame.time.Clock()

    # Función para dibujar un botón
    def dibujar_boton(texto, x, y, ancho, alto, color_borde, color_fondo):
        pygame.draw.rect(ventana, color_fondo, (x, y, ancho, alto))
        pygame.draw.rect(ventana, color_borde, (x, y, ancho, alto), 5)
        ventana.blit(texto, (x + (ancho - texto.get_width()) // 2, y + (alto - texto.get_height()) // 2))

    # Funciones para mostrar cada pantalla
    def pantalla_principal():
        ventana.fill(NEGRO)
        titulo = fuente_texto.render('POWER DECK', True, BLANCO)
        subtitulo = fuente_texto.render('HERRAMIENTA DE CARTAS', True, BLANCO)
        ventana.blit(titulo, ((ANCHO - titulo.get_width()) // 2, 50))
        ventana.blit(subtitulo, ((ANCHO - subtitulo.get_width()) // 2, 130))

        dibujar_boton(fuente_texto.render('Registrarse', True, BLANCO), ANCHO // 2 - 150, ALTO // 2 - 100, 300, 100, AZUL_CLARO, NEGRO)
        dibujar_boton(fuente_texto.render('Iniciar Sesión', True, BLANCO), ANCHO // 2 - 150, ALTO // 2 + 50, 300, 100, AZUL_CLARO, NEGRO)
        dibujar_boton(fuente_texto.render('Salir', True, BLANCO), ANCHO // 2 - 150, ALTO // 2 + 200, 300, 100, AZUL_CLARO, NEGRO)

    def pantalla_registrar():
        ventana.fill(NEGRO)
        titulo = fuente_texto.render('Registro de Usuario', True, BLANCO)
        ventana.blit(titulo, ((ANCHO - titulo.get_width()) // 2, 50))

        # Dibujar campos de texto
        y_offset = 150
        for campo, valor in campos_texto.items():
            texto_campo = fuente_texto.render(f'{campo.capitalize()}: {valor}', True, BLANCO)
            ventana.blit(texto_campo, (ANCHO // 2 - 200, y_offset))
            y_offset += 50

        # Dibujar botones
        dibujar_boton(fuente_texto.render('Confirmar Registro', True, BLANCO), ANCHO // 2 - 150, ALTO // 2 + 100, 300, 100, AZUL_CLARO, NEGRO)
        dibujar_boton(fuente_texto.render('Regresar', True, BLANCO), ANCHO // 2 - 150, ALTO // 2 + 250, 300, 100, AZUL_CLARO, NEGRO)

    def pantalla_cartas_iniciales():
        ventana.fill(NEGRO)
        titulo = fuente_texto.render('Cartas Iniciales', True, BLANCO)
        ventana.blit(titulo, ((ANCHO - titulo.get_width()) // 2, 50))
        dibujar_boton(fuente_texto.render('Ingresar', True, BLANCO), ANCHO // 2 - 150, ALTO // 2, 300, 100, AZUL_CLARO, NEGRO)

    def pantalla_ingresar():
        ventana.fill(NEGRO)
        titulo = fuente_texto.render('Iniciar Sesión', True, BLANCO)
        ventana.blit(titulo, ((ANCHO - titulo.get_width()) // 2, 50))
        dibujar_boton(fuente_texto.render('Confirmar', True, BLANCO), ANCHO // 2 - 150, ALTO // 2, 300, 100, AZUL_CLARO, NEGRO)
        dibujar_boton(fuente_texto.render('Regresar', True, BLANCO), ANCHO // 2 - 150, ALTO // 2 + 150, 300, 100, AZUL_CLARO, NEGRO)

    # Bucle principal
    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if evento.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()

                if pantalla_actual == "principal":
                    if ANCHO // 2 - 150 <= mouse_pos[0] <= ANCHO // 2 + 150:
                        if ALTO // 2 - 100 <= mouse_pos[1] <= ALTO // 2:
                            pantalla_actual = "registrar"
                        elif ALTO // 2 + 50 <= mouse_pos[1] <= ALTO // 2 + 150:
                            pantalla_actual = "ingresar"
                        elif ALTO // 2 + 200 <= mouse_pos[1] <= ALTO // 2 + 300:
                            pygame.quit()
                            sys.exit()

                elif pantalla_actual == "registrar":
                    if ANCHO // 2 - 150 <= mouse_pos[0] <= ANCHO // 2 + 150:
                        if ALTO // 2 + 100 <= mouse_pos[1] <= ALTO // 2 + 200:

                            pantalla_actual = "cartas_iniciales"
                        elif ALTO // 2 + 250 <= mouse_pos[1] <= ALTO // 2 + 350:
                            pantalla_actual = "principal"

                elif pantalla_actual == "cartas_iniciales":
                    if ANCHO // 2 - 150 <= mouse_pos[0] <= ANCHO // 2 + 150 and ALTO // 2 <= mouse_pos[1] <= ALTO // 2 + 100:
                        pantalla_actual = "ingresar"

                elif pantalla_actual == "ingresar":
                    if ANCHO // 2 - 150 <= mouse_pos[0] <= ANCHO // 2 + 150:
                        if ALTO // 2 <= mouse_pos[1] <= ALTO // 2 + 100:
                            pantalla_actual = "menu"
                        elif ALTO // 2 + 150 <= mouse_pos[1] <= ALTO // 2 + 250:
                            pantalla_actual = "principal"

            if evento.type == pygame.KEYDOWN:
                if pantalla_actual == "registrar":

                    for campo in campos_texto.keys():
                        if evento.unicode.isprintable() and len(campos_texto[campo]) < 20:
                            campos_texto[campo] += evento.unicode
                        elif evento.key == pygame.K_BACKSPACE:
                            campos_texto[campo] = campos_texto[campo][:-1]

        ventana.fill(NEGRO)

        if pantalla_actual == "principal":
            pantalla_principal()
        elif pantalla_actual == "registrar":
            pantalla_registrar()
        elif pantalla_actual == "cartas_iniciales":
            pantalla_cartas_iniciales()
        elif pantalla_actual == "ingresar":
            pantalla_ingresar()

        pygame.display.update()

if __name__ == "__main__":
    main()

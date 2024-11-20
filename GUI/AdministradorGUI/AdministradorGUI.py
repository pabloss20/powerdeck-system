import pygame
import sys
from GUI.AdministradorGUI import CrearCarta
import Galeria

def main():
    # Inicializar pygame
    pygame.init()

    # Colores
    NEGRO = (0, 0, 0)
    BLANCO = (255, 255, 255)
    AZUL_CLARO = (100, 149, 237)

    # Dimensiones de la ventana
    ANCHO = 1820  # Cambiado a 1820
    ALTO = 900    # Cambiado a 900

    # Crear la ventana
    ventana = pygame.display.set_mode((ANCHO, ALTO), pygame.RESIZABLE)
    pygame.display.set_caption('Power Deck App')

    # Fuentes
    fuente_texto = pygame.font.Font(None, 50)

    # Variables de estado
    pantalla_actual = "principal"

    campos_texto = {
        "nombre": "",
        "apellido": "",
        "correo": "",
        "contrasena": ""
    }

    text_inputs = {
        "nombre": pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect(860, 150, 350, 42), manager=manager, object_id=ObjectID(class_id='@campoTXT', object_id="input1")),
        "apellido": pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect(860, 200, 350, 42), manager=manager, object_id=ObjectID(class_id='@campoTXT', object_id="input2")),
        "correo": pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect(860, 250, 350, 42), manager=manager, object_id=ObjectID(class_id='@campoTXT', object_id="input3")),
        "contrasena": pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect(860, 300, 350, 42), manager=manager, object_id=ObjectID(class_id='@campoTXT', object_id="input4"))
    }

    # Ocultar los campos inicialmente
    for text_input in text_inputs.values():
        text_input.hide()

    # Agregar el UIDropDownMenu para seleccionar el rol
    dropdown_rol = pygame_gui.elements.UIDropDownMenu(
        options_list=["juego", "reportes"],
        starting_option="juego",
        relative_rect=pygame.Rect(860, 350, 350, 42),
        manager=manager,
        object_id=ObjectID(class_id='@dropdown', object_id="dropdown1")
    )
    dropdown_rol.hide()

    def cambiar_visibilidad_inputboxes(pantalla):
        if pantalla == "registrar":
            for text_input in text_inputs.values():
                text_input.show()
            dropdown_rol.show()
        else:
            for text_input in text_inputs.values():
                text_input.hide()
            dropdown_rol.hide()

    def pantalla_registrar():
        ventana.fill(NEGRO)
        titulo = fuente_texto.render('Registro de Administrador', True, BLANCO)
        ventana.blit(titulo, ((ANCHO - titulo.get_width()) // 2, 50))

        y_offset = 150
        for campo, valor in campos_texto.items():
            texto_campo = fuente_texto.render(f'{campo.capitalize()}: {valor}', True, BLANCO)
            ventana.blit(texto_campo, (ANCHO // 2 - 200, y_offset))
            y_offset += 50

        dibujar_boton(fuente_texto.render('Confirmar Registro', True, BLANCO), ANCHO // 2 - 150, ALTO_VENTANA // 2 + 100, 300, 100, AZUL_CLARO, NEGRO)
        dibujar_boton(fuente_texto.render('Regresar', True, BLANCO), ANCHO // 2 - 150, ALTO_VENTANA // 2 + 250, 300, 100, AZUL_CLARO, NEGRO)


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
        dibujar_boton(fuente_texto.render('CREAR CARTA', True, BLANCO),
                      ANCHO // 2 - 150, ALTO // 2 - 100, 300, 100, AZUL_CLARO, NEGRO, ventana)

        dibujar_boton(fuente_texto.render('VER ALBUM', True, BLANCO),
                      ANCHO // 2 - 150, ALTO // 2 + 50, 300, 100, AZUL_CLARO, NEGRO, ventana)

        dibujar_boton(fuente_texto.render('REGISTRAR ADMINISTRADOR', True, BLANCO),
                      ANCHO // 2 - 150, ALTO // 2 + 125, 300, 100, AZUL_CLARO, NEGRO, ventana)


    def btn_listo():
        global pantalla_actual
        try:
            text_input = {
                "nombre": text_inputs["nombre"].get_text(),
                "apellido": text_inputs["apellido"].get_text(),
                "correo": text_inputs["correo"].get_text(),
                "contrasena": text_inputs["contrasena"].get_text(),
            }

            rol_seleccionado = dropdown_rol.selected_option[0]  # Solo toma el primer valor de la tupla

            if rol_seleccionado == "":
                raise ValueError("Debe seleccionar un rol")

            nuevo_admin = Administrador(
                nombre=text_input["nombre"],
                apellido=text_input["apellido"],
                correo=text_input["correo"],
                contrasena=text_input["contrasena"],
                rol_administrador=rol_seleccionado
            )

            pygame_gui.windows.UIConfirmationDialog(
                rect=pygame.Rect((ALTO_VENTANA // 2, ANCHO // 2 - 600), (300, 100)),
                manager=manager,
                window_title="Exito!",
                action_long_desc=str("Usuario creado con éxito"),
                action_short_name="OK",
                blocking=True
            )
        except ValueError as e:
            pygame_gui.windows.UIConfirmationDialog(
                rect=pygame.Rect((ALTO_VENTANA // 2, ANCHO // 2 - 600), (300, 100)),
                manager=manager,
                window_title="Error",
                action_long_desc=str(e),
                action_short_name="OK",
                blocking=True
            )

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
                    elif ANCHO // 2 - 150 <= mouse_pos[0] <= ANCHO // 2 + 150 and ALTO // 2 + 125 <= mouse_pos[1] <= ALTO // 2 + 150:
                        pantalla_actual = "registrar"  # Cambiar a la pantalla a registro


            elif pantalla_actual == "crear_carta":
                CrearCarta.iniciar_crear_carta()
            elif pantalla_actual == "ver_album":
                Galeria.iniciar_galeria()  # Llamar a la función de galería desde el archivo correspondiente
            elif pantalla_actual == "registrar":
                if ANCHO // 2 - 150 <= mouse_pos[0] <= ANCHO // 2 + 150:
                    if ALTO_VENTANA // 2 + 100 <= mouse_pos[1] <= ALTO_VENTANA // 2 + 200:
                        btn_listo()
                    elif ALTO_VENTANA // 2 + 250 <= mouse_pos[1] <= ALTO_VENTANA // 2 + 350:
                        pantalla_actual = "principal"
                        cambiar_visibilidad_inputboxes("principal")

        # Rellenar la pantalla de negro
        ventana.fill(NEGRO)

        # Dibujar la pantalla correspondiente
        if pantalla_actual == "principal":
            pantalla_principal()
        elif pantalla_actual == "crear_carta":
            CrearCarta.iniciar_crear_carta()
        elif pantalla_actual == "ver_album":
            #Galeria.iniciar_galeria()
            pass
        elif pantalla_actual == "registrar":
            pantalla_registrar()

        # Actualizar la pantalla
        pygame.display.update()

if __name__ == "__main__":
    main()
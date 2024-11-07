import pygame
import pygame_gui
import sys
from pygame_gui.core import ObjectID
from Model.Administrador import Administrador

def iniciar_reportes_gui():
    pygame.init()

    # Colores y constantes de la ventana
    global Ingreso
    Ingreso = False
    NEGRO = (0, 0, 0)
    BLANCO = (255, 255, 255)
    AZUL_CLARO = (100, 149, 237)
    ANCHO = 1820
    ALTO_VENTANA = 900

    ventana = pygame.display.set_mode((ANCHO, ALTO_VENTANA), pygame.RESIZABLE)
    pygame.display.set_caption('PowerDeck App')
    manager = pygame_gui.UIManager((ANCHO, ALTO_VENTANA), '../../Files/text_entry_box.json')

    fuente_texto = pygame.font.Font(None, 50)

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

    def dibujar_boton(texto, x, y, ancho, alto, color_borde, color_fondo):
        pygame.draw.rect(ventana, color_fondo, (x, y, ancho, alto))
        pygame.draw.rect(ventana, color_borde, (x, y, ancho, alto), 5)
        ventana.blit(texto, (x + (ancho - texto.get_width()) // 2, y + (alto - texto.get_height()) // 2))

    def pantalla_principal():
        ventana.fill(NEGRO)
        titulo = fuente_texto.render('POWER DECK', True, BLANCO)
        subtitulo = fuente_texto.render('SISTEMA ADMINISTRADOR DE REPORTES', True, BLANCO)
        ventana.blit(titulo, ((ANCHO - titulo.get_width()) // 2, 50))
        ventana.blit(subtitulo, ((ANCHO - subtitulo.get_width()) // 2, 130))

        dibujar_boton(fuente_texto.render('Registrar Administrador', True, BLANCO), ANCHO // 2 - 150, ALTO_VENTANA // 2 - 100, 300, 100, AZUL_CLARO, NEGRO)
        dibujar_boton(fuente_texto.render('Visualizar Reportes', True, BLANCO), ANCHO // 2 - 150, ALTO_VENTANA // 2 + 50, 300, 100, AZUL_CLARO, NEGRO)
        dibujar_boton(fuente_texto.render('Salir', True, BLANCO), ANCHO // 2 - 150, ALTO_VENTANA // 2 + 200, 300, 100, AZUL_CLARO, NEGRO)

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

    def btn_listo():
        global pantalla_actual
        try:
            text_input = {
                "nombre": text_inputs["nombre"].get_text(),
                "apellido": text_inputs["apellido"].get_text(),
                "correo": text_inputs["correo"].get_text(),
                "contrasena": text_inputs["contrasena"].get_text(),
            }

            rol_seleccionado = dropdown_rol.selected_option  # Obtiene el rol seleccionado
            if rol_seleccionado == "Seleccionar rol":
                raise ValueError("Debe seleccionar un rol.")

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

    reloj = pygame.time.Clock()
    while True:
        time_delta = reloj.tick(60) / 1000.0
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            manager.process_events(evento)
            if evento.type == pygame.MOUSEBUTTONUP:
                mouse_pos = pygame.mouse.get_pos()
                if pantalla_actual == "principal":
                    if ANCHO // 2 - 150 <= mouse_pos[0] <= ANCHO // 2 + 150:
                        if ALTO_VENTANA // 2 - 100 <= mouse_pos[1] <= ALTO_VENTANA // 2:
                            pantalla_actual = "registrar"
                            cambiar_visibilidad_inputboxes("registrar")

                        elif ALTO_VENTANA // 2 + 200 <= mouse_pos[1] <= ALTO_VENTANA // 2 + 300:
                            pygame.quit()
                            sys.exit()
                elif pantalla_actual == "registrar":
                    if ANCHO // 2 - 150 <= mouse_pos[0] <= ANCHO // 2 + 150:
                        if ALTO_VENTANA // 2 + 100 <= mouse_pos[1] <= ALTO_VENTANA // 2 + 200:
                            btn_listo()
                        elif ALTO_VENTANA // 2 + 250 <= mouse_pos[1] <= ALTO_VENTANA // 2 + 350:
                            pantalla_actual = "principal"
                            cambiar_visibilidad_inputboxes("principal")

        ventana.fill(NEGRO)
        if pantalla_actual == "principal":
            pantalla_principal()
        elif pantalla_actual == "registrar":
            pantalla_registrar()

        manager.update(time_delta)
        manager.draw_ui(ventana)
        pygame.display.update()

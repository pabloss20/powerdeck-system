import pygame
import pygame_gui
import sys
from pygame_gui.core import ObjectID
from Model.Jugador import Jugador
from Model.Administrador import Administrador
from Model.Usuario import Usuario
import AdminReportesGUI
import AdministradorGUI

def main():
    pygame.init()

    # Colores
    global Ingreso
    Ingreso = False
    NEGRO = (0, 0, 0)
    BLANCO = (255, 255, 255)
    AZUL_CLARO = (100, 149, 237)

    ANCHO = 1820
    ALTO_VENTANA = 900

    # Crear ventana y manager de UI
    ventana = pygame.display.set_mode((ANCHO, ALTO_VENTANA), pygame.RESIZABLE)
    pygame.display.set_caption('PowerDeck App')
    manager = pygame_gui.UIManager((ANCHO, ALTO_VENTANA), '../../Files/text_entry_box.json')

    # Fuentes
    fuente_texto = pygame.font.Font(None, 50)

    # Variables de estado
    pantalla_actual = "principal"

    campos_texto_login = {
        "correo": "",
        "contrasena": ""
    }

    # Crear instancias de UITextEntryLine solo una vez para la pantalla de inicio de sesion
    text_inputs_login = {

        "correo": pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect(860, 150, 350, 42),
                                                      manager=manager,
                                                      object_id=ObjectID(class_id='@campoTXT', object_id="input3")),
        "contrasena": pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect(920, 200, 350, 42),
                                                          manager=manager,
                                                          object_id=ObjectID(class_id='@campoTXT', object_id="input4"))
    }

    # Variables para mostrar/ocultar campos de texto
    for text_input_login in text_inputs_login.values():
        text_input_login.hide()

    # Función para dibujar un botón
    def dibujar_boton(texto, x, y, ancho, alto, color_borde, color_fondo):
        pygame.draw.rect(ventana, color_fondo, (x, y, ancho, alto))
        pygame.draw.rect(ventana, color_borde, (x, y, ancho, alto), 5)
        ventana.blit(texto, (x + (ancho - texto.get_width()) // 2, y + (alto - texto.get_height()) // 2))

    # Funciones para mostrar cada pantalla
    def pantalla_principal():
        ventana.fill(NEGRO)
        titulo = fuente_texto.render('POWER DECK', True, BLANCO)
        subtitulo = fuente_texto.render('SISTEMA PARA ADMINISTRADOR', True, BLANCO)
        ventana.blit(titulo, ((ANCHO - titulo.get_width()) // 2, 50))
        ventana.blit(subtitulo, ((ANCHO - subtitulo.get_width()) // 2, 130))

        dibujar_boton(fuente_texto.render('Iniciar Sesión', True, BLANCO), ANCHO // 2 - 150, ALTO_VENTANA // 2 + 50,
                      300, 100, AZUL_CLARO, NEGRO)
        dibujar_boton(fuente_texto.render('Salir', True, BLANCO), ANCHO // 2 - 150, ALTO_VENTANA // 2 + 200, 300, 100,
                      AZUL_CLARO, NEGRO)

    # Función para activar o desactivar los inputboxes según la pantalla
    def cambiar_visibilidad_inputboxes_login(pantalla):
        for input_login in text_inputs_login.values():
            if pantalla == 0:
                input_login.show()
            else:
                input_login.hide()

    # Nueva función para manejar el inicio de sesión
    def iniciar_sesion(log):
        global Ingreso
        try:
            correo = log[0]
            contrasena = log[1]
            print(log)

            # Llamamos al método iniciar_sesion de Usuario
            resultado = Usuario.iniciar_sesion(correo, contrasena)

            if resultado == 1:
                # Usuario autenticado, pero no es administrador
                print("Usuario autenticado, pero no es administrador")
                pygame_gui.windows.UIConfirmationDialog(
                    rect=pygame.Rect((ALTO_VENTANA // 2, ANCHO // 2 - 600), (300, 100)),
                    manager=manager,
                    window_title="Advertencia",
                    action_long_desc="Usuario autenticado, pero no es administrador.",
                    action_short_name="OK",
                    blocking=True
                )
                Ingreso = 1

            elif resultado == 2:
                # Usuario autenticado como administrador de juego
                print("Inicio de sesión exitoso - Administrador de juego")
                pygame_gui.windows.UIConfirmationDialog(
                    rect=pygame.Rect((ALTO_VENTANA // 2, ANCHO // 2 - 600), (300, 100)),
                    manager=manager,
                    window_title="Éxito",
                    action_long_desc="Bienvenido, Administrador de juego.",
                    action_short_name="OK",
                    blocking=True
                )
                Ingreso = 3

            elif resultado == 3:
                # Usuario autenticado como administrador de reportes
                print("Inicio de sesión exitoso - Administrador de reportes")
                pygame_gui.windows.UIConfirmationDialog(
                    rect=pygame.Rect((ALTO_VENTANA // 2, ANCHO // 2 - 600), (300, 100)),
                    manager=manager,
                    window_title="Éxito",
                    action_long_desc="Bienvenido, Administrador de reportes.",
                    action_short_name="OK",
                    blocking=True
                )
                Ingreso = 2

            else:
                # Caso en el que el resultado es "Usuario no encontrado" o "Contraseña incorrecta"
                print("Error de credenciales")
                pygame_gui.windows.UIConfirmationDialog(
                    rect=pygame.Rect((ALTO_VENTANA // 2, ANCHO // 2 - 600), (300, 100)),
                    manager=manager,
                    window_title="Error",
                    action_long_desc=str(resultado),
                    action_short_name="OK",
                    blocking=True
                )

        except ValueError as e:
            print("Error al iniciar sesión:", e)
            pygame_gui.windows.UIConfirmationDialog(
                rect=pygame.Rect((ALTO_VENTANA // 2, ANCHO // 2 - 600), (300, 100)),
                manager=manager,
                window_title="Error",
                action_long_desc=str(e),
                action_short_name="OK",
                blocking=True
            )

    def pantalla_ingresar():
        ventana.fill(NEGRO)
        # Dibujar campos de texto
        y_offset = 150
        for campo, valor in campos_texto_login.items():
            texto_campo = fuente_texto.render(f'{campo.capitalize()}: {valor}', True, BLANCO)
            ventana.blit(texto_campo, (ANCHO // 2 - 200, y_offset))
            y_offset += 50
        titulo = fuente_texto.render('Inicio de Sesion', True, BLANCO)
        ventana.blit(titulo, ((ANCHO - titulo.get_width()) // 2, 50))

        for text_input in text_inputs_login.values():
            text_input.show()

        # Dibujar botones
        dibujar_boton(fuente_texto.render('Confirmar', True, BLANCO), ANCHO // 2 - 150, ALTO_VENTANA // 2 + 100,
                      300, 100, AZUL_CLARO, NEGRO)
        dibujar_boton(fuente_texto.render('Regresar', True, BLANCO), ANCHO // 2 - 150, ALTO_VENTANA // 2 + 250, 300, 100,
                      AZUL_CLARO, NEGRO)
    # Bucle principal
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
                        if ALTO_VENTANA // 2 + 50 <= mouse_pos[1] <= ALTO_VENTANA // 2 + 150:
                            pantalla_actual = "ingresar"
                            for text_input in text_inputs_login.values():
                                text_input_login.show()
                        elif ALTO_VENTANA // 2 + 200 <= mouse_pos[1] <= ALTO_VENTANA // 2 + 300:
                            pygame.quit()
                            sys.exit()

                elif pantalla_actual == "ingresar":
                    if ANCHO // 2 - 150 <= mouse_pos[0] <= ANCHO // 2 + 150:
                        if ALTO_VENTANA // 2 + 100 <= mouse_pos[1] <= ALTO_VENTANA // 2 + 200:
                            log = []
                            for campo, text_input in text_inputs_login.items():
                                print(f"{campo}: {text_input.get_text()}")  # Aquí puedes guardar los datos.
                                log.append(text_input.get_text())
                            iniciar_sesion(log)
                            if Ingreso == 2:
                                AdminReportesGUI.iniciar_reportes_gui()
                            elif Ingreso == 3:
                                AdministradorGUI.main()


                        elif ALTO_VENTANA // 2 + 250 <= mouse_pos[1] <= ALTO_VENTANA // 2 + 350:
                            pantalla_actual = "principal"
                            cambiar_visibilidad_inputboxes_login(1)

        ventana.fill(NEGRO)

        if pantalla_actual == "principal":
            pantalla_principal()
        elif pantalla_actual == "ingresar":
            pantalla_ingresar()

        manager.update(time_delta)
        manager.draw_ui(ventana)
        pygame.display.update()

if __name__ == "__main__":
    main()
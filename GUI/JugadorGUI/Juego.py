import pygame
import pygame_gui
import sys
from pygame_gui.core import ObjectID
from Model.Jugador import Jugador
from Model.JsonHandler import JsonHandler
import CrearMazo
from Model import Servidor
from Model.Usuario import Usuario
import MatchMaking

def main():
    pygame.init()
    jsonhandler = JsonHandler('../../Files/usuarios.json')

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

    # Lista de países de la ONU (solo algunos como ejemplo)
    paises_onu = ["Afganistán", "Albania", "Alemania", "Andorra", "Angola", "Antigua y Barbuda", "Arabia Saudita", "Argelia", "Argentina", "Australia", "Costa Rica"]

    # Variables de estado
    pantalla_actual = "principal"
    campos_texto = {
        "nombre": "",
        "apellido": "",
        "correo": "",
        "contrasena": "",
        "confirmar_contrasena": "",
        "usuario": ""
    }

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

    # Crear instancias de UITextEntryLine solo una vez para la pantalla de registro
    text_inputs = {
        "nombre": pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect(860, 150, 350, 42),
                                                      manager=manager,
                                                      object_id=ObjectID(class_id='@campoTXT', object_id="input1")),
        "apellido": pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect(860, 200, 350, 42),
                                                        manager=manager,
                                                        object_id=ObjectID(class_id='@campoTXT', object_id="input2")),
        "correo": pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect(860, 250, 350, 42),
                                                      manager=manager,
                                                      object_id=ObjectID(class_id='@campoTXT', object_id="input3")),
        "contrasena": pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect(930, 300, 350, 42),
                                                          manager=manager,
                                                          object_id=ObjectID(class_id='@campoTXT', object_id="input4")),
        "confirmar_contrasena": pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect(1100, 350, 350, 42),
                                                          manager=manager,
                                                          object_id=ObjectID(class_id='@campoTXT', object_id="input4")),
        "usuario": pygame_gui.elements.UITextEntryLine(
            relative_rect=pygame.Rect(860, 400, 350, 42), manager=manager,
            object_id=ObjectID(class_id='@campoTXT', object_id="input5"))
    }

    # Agregar el UIDropDownMenu para seleccionar el país
    dropdown_pais = pygame_gui.elements.UIDropDownMenu(
        options_list=["Australia", "Costa Rica"],  # Lista de países de la ONU
        starting_option="Australia",  # Opción predeterminada
        relative_rect=pygame.Rect(860, 450, 350, 42),
        manager=manager,
        object_id=ObjectID(class_id='@dropdown', object_id="dropdown_pais")
    )
    dropdown_pais.hide()  # Inicialmente oculto

    # Variables para mostrar/ocultar campos de texto
    for text_input in text_inputs.values():
        text_input.hide()

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
        subtitulo = fuente_texto.render('HERRAMIENTA DE CARTAS', True, BLANCO)
        ventana.blit(titulo, ((ANCHO - titulo.get_width()) // 2, 50))
        ventana.blit(subtitulo, ((ANCHO - subtitulo.get_width()) // 2, 130))

        dibujar_boton(fuente_texto.render('Registrarse', True, BLANCO), ANCHO // 2 - 150, ALTO_VENTANA // 2 - 100, 300,
                      100, AZUL_CLARO, NEGRO)
        dibujar_boton(fuente_texto.render('Iniciar Sesión', True, BLANCO), ANCHO // 2 - 150, ALTO_VENTANA // 2 + 50,
                      300, 100, AZUL_CLARO, NEGRO)
        dibujar_boton(fuente_texto.render('Salir', True, BLANCO), ANCHO // 2 - 150, ALTO_VENTANA // 2 + 200, 300, 100,
                      AZUL_CLARO, NEGRO)

    # Función para activar o desactivar los inputboxes según la pantalla
    def cambiar_visibilidad_inputboxes(pantalla):
        for inputbox in text_inputs:
            if pantalla == 0:
                # Variables para mostrar/ocultar campos de texto
                for text_input in text_inputs.values():
                    text_input.show()
                dropdown_pais.show()

            else:
                # Variables para mostrar/ocultar campos de texto
                for text_input in text_inputs.values():
                    text_input.hide()
                dropdown_pais.hide()

    # Función para activar o desactivar los inputboxes según la pantalla
    def cambiar_visibilidad_inputboxes_login(pantalla):
        for input_login in text_inputs_login.values():
            if pantalla == 0:
                input_login.show()
            else:
                input_login.hide()

    def pantalla_registrar():
        ventana.fill(NEGRO)
        # Dibujar campos de texto
        y_offset = 150
        for campo, valor in campos_texto.items():
            texto_campo = fuente_texto.render(f'{campo.capitalize()}: {valor}', True, BLANCO)
            ventana.blit(texto_campo, (ANCHO // 2 - 200, y_offset))
            y_offset += 50
        titulo = fuente_texto.render('Registro de Usuario', True, BLANCO)
        ventana.blit(titulo, ((ANCHO - titulo.get_width()) // 2, 50))

        for text_input in text_inputs.values():
            text_input.show()

        dropdown_pais.show()

        # Dibujar botones
        dibujar_boton(fuente_texto.render('Confirmar Registro', True, BLANCO), ANCHO // 2 - 150, ALTO_VENTANA // 2 + 100,
                      300, 100, AZUL_CLARO, NEGRO)
        dibujar_boton(fuente_texto.render('Regresar', True, BLANCO), ANCHO // 2 - 150, ALTO_VENTANA // 2 + 250, 300, 100,
                      AZUL_CLARO, NEGRO)

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
                print("Inicio de sesión exitoso -Jugador")
                pygame_gui.windows.UIConfirmationDialog(
                    rect=pygame.Rect((ALTO_VENTANA // 2, ANCHO // 2 - 600), (300, 100)),
                    manager=manager,
                    window_title="Éxito",
                    action_long_desc="Bienvenido, Jugador.",
                    action_short_name="OK",
                    blocking=True
                )
                Ingreso = 1

            elif resultado == 2:
                print("Usuario autenticado, pero no es jugador.")
                pygame_gui.windows.UIConfirmationDialog(
                    rect=pygame.Rect((ALTO_VENTANA // 2, ANCHO // 2 - 600), (300, 100)),
                    manager=manager,
                    window_title="Advertencia",
                    action_long_desc="Usuario autenticado, pero no es jugador.",
                    action_short_name="OK",
                    blocking=True
                )
                Ingreso = 2

            elif resultado == 3:
                print("Usuario autenticado, pero no es jugador.")
                pygame_gui.windows.UIConfirmationDialog(
                    rect=pygame.Rect((ALTO_VENTANA // 2, ANCHO // 2 - 600), (300, 100)),
                    manager=manager,
                    window_title="Advertencia",
                    action_long_desc="Usuario autenticado, pero no es jugador.",
                    action_short_name="OK",
                    blocking=True
                )
                Ingreso = 3

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

    def btn_listo(contra,confirmar):
        global pantalla_actual
        try:
            # Extraer los valores de cada campo en text_inputs
            text_input = {
                "nombre": text_inputs["nombre"].get_text(),
                "apellido": text_inputs["apellido"].get_text(),
                "correo": text_inputs["correo"].get_text(),
                "contrasena": contra,
                "confirmar_contrasena": confirmar,
                "nombre_usuario": text_inputs["usuario"].get_text()
            }

            pais_seleccionado = dropdown_pais.selected_option[0]  # Solo toma el primer valor de la tupla

            # Crear una instancia de la clase Mazo con el nombre proporcionado
            nuevo_jugador = Jugador(
                nombre = text_input["nombre"],
                apellido= text_input["apellido"],
                correo = text_input["correo"],
                contrasena= text_input["contrasena"],
                confirmar_contrasena= text_input["confirmar_contrasena"],
                pais= pais_seleccionado,
                nombre_usuario= text_input["nombre_usuario"]
            )

            # Limpiar campos de texto
            for campo in campos_texto.keys():
                campos_texto[campo] = ""  # Limpiar los valores del diccionario de campos de texto

            # Limpiar las cajas de texto en la interfaz gráfica
            for key, text_input in text_inputs.items():
                text_input.set_text("")  # Limpiar cada input en la interfaz

            # Crear un cuadro de diálogo para mostrar el error al usuario
            pygame_gui.windows.UIConfirmationDialog(
                rect=pygame.Rect((ALTO_VENTANA // 2, ANCHO // 2 - 600), (300, 100)),
                manager=manager,
                window_title="Exito!",
                action_long_desc=str("Usuario creado con exito"),
                action_short_name="OK",
                blocking=True
            )

            # Mostrar confirmación al usuario

        except ValueError as e:
            dialogo_exito_abierto = False
            print("Error al registrar jugador:", e)

            # Crear un cuadro de diálogo para mostrar el error al usuario
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

    def verificar_servidor():
        if not Servidor.servidor_iniciado:
            pygame_gui.windows.UIConfirmationDialog(
                rect=pygame.Rect((ALTO_VENTANA // 2, ANCHO // 2 - 600), (300, 100)),
                manager=manager,
                window_title="Error",
                action_long_desc="El servidor no está en funcionamiento.",
                action_short_name="OK",
                blocking=True
            )
            return False
        return True

    #Variable para almacenar el texto real de la contraseña
    texto_real_contrasena = ""
    texto_real_confirmar_contrasena = ""
    # Bucle principal
    reloj = pygame.time.Clock()
    while True:
        time_delta = reloj.tick(60) / 1000.0

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            # Detectar eventos de texto en `UITextEntryLine`
            if evento.type == pygame.USEREVENT and evento.user_type == pygame_gui.UI_TEXT_ENTRY_CHANGED:
                for key in text_inputs_login:
                    if evento.ui_element == text_inputs_login[key]:
                        if key == "contrasena":  # Campo de contraseña
                            texto_actual = text_inputs_login[key].get_text()
                            if len(texto_actual) > len(texto_real_contrasena):
                                texto_real_contrasena += texto_actual[-1]  # Agregar el último carácter ingresado
                            elif len(texto_actual) < len(texto_real_contrasena):
                                texto_real_contrasena = texto_real_contrasena[
                                                        :-1]  # Eliminar el último carácter si se borró
                            # Mostrar solo asteriscos en el campo
                            text_inputs_login[key].set_text('*' * len(texto_real_contrasena))

                for key in text_inputs:
                    if evento.ui_element == text_inputs[key]:
                        if key == "confirmar_contrasena":  # Campo de confirmación de contraseña
                            texto_actual_c = text_inputs[key].get_text()
                            if len(texto_actual_c) > len(texto_real_confirmar_contrasena):
                                texto_real_confirmar_contrasena += texto_actual_c[
                                    -1]  # Agregar el último carácter ingresado
                            elif len(texto_actual_c) < len(texto_real_confirmar_contrasena):
                                texto_real_confirmar_contrasena = texto_real_confirmar_contrasena[
                                                                  :-1]  # Eliminar el último carácter si se borró

                            # Mostrar solo asteriscos en el campo
                            text_inputs[key].set_text('*' * len(texto_real_confirmar_contrasena))

                        elif key == "contrasena":  # Campo de contraseña
                            texto_actual = text_inputs[key].get_text()
                            if len(texto_actual) > len(texto_real_contrasena):
                                texto_real_contrasena += texto_actual[-1]  # Agregar el último carácter ingresado
                            elif len(texto_actual) < len(texto_real_contrasena):
                                texto_real_contrasena = texto_real_contrasena[
                                                        :-1]  # Eliminar el último carácter si se borró

                            # Mostrar solo asteriscos en el campo
                            text_inputs[key].set_text('*' * len(texto_real_contrasena))

            manager.process_events(evento)
            if evento.type == pygame.MOUSEBUTTONUP:
                mouse_pos = pygame.mouse.get_pos()
                if pantalla_actual == "principal":
                    if ANCHO // 2 - 150 <= mouse_pos[0] <= ANCHO // 2 + 150:
                        if ALTO_VENTANA // 2 - 100 <= mouse_pos[1] <= ALTO_VENTANA // 2:
                            pantalla_actual = "registrar"
                            for text_input in text_inputs.values():
                                text_input.show()

                        elif ALTO_VENTANA // 2 + 50 <= mouse_pos[1] <= ALTO_VENTANA // 2 + 150:
                            pantalla_actual = "ingresar"
                            for text_input in text_inputs_login.values():
                                text_input_login.show()
                        elif ALTO_VENTANA // 2 + 200 <= mouse_pos[1] <= ALTO_VENTANA // 2 + 300:
                            pygame.quit()
                            sys.exit()
                elif pantalla_actual == "registrar":
                    if ANCHO // 2 - 150 <= mouse_pos[0] <= ANCHO // 2 + 150:
                        if ALTO_VENTANA // 2 + 100 <= mouse_pos[1] <= ALTO_VENTANA // 2 + 200:
                            for campo, text_input in text_inputs.items():
                                print(f"{campo}: {text_input.get_text()}")  # Aquí puedes guardar los datos.
                            btn_listo(texto_real_contrasena,texto_real_confirmar_contrasena)

                        elif ALTO_VENTANA // 2 + 250 <= mouse_pos[1] <= ALTO_VENTANA // 2 + 350:
                            pantalla_actual = "principal"
                            cambiar_visibilidad_inputboxes(1)

                elif pantalla_actual == "cartas_iniciales":
                    if ANCHO // 2 - 150 <= mouse_pos[0] <= ANCHO // 2 + 150 and ALTO_VENTANA // 2 <= mouse_pos[1] <= ALTO_VENTANA // 2 + 100:
                        pantalla_actual = "ingresar"

                elif pantalla_actual == "ingresar":
                    if ANCHO // 2 - 150 <= mouse_pos[0] <= ANCHO // 2 + 150:
                        if ALTO_VENTANA // 2 + 100 <= mouse_pos[1] <= ALTO_VENTANA // 2 + 200:
                            log = []
                            for campo, text_input in text_inputs_login.items():
                                if campo == "contrasena":
                                    # Usar el texto real de la contraseña
                                    log.append(texto_real_contrasena)
                                    print(f"{campo}: {texto_real_contrasena}")
                                else:
                                    log.append(text_input.get_text())
                                    print(f"{campo}: {text_input.get_text()}")
                            iniciar_sesion(log)
                            if Ingreso == 1:
                                MatchMaking.main(jsonhandler.obtener_id_por_correo_y_contrasena(correo=log[0]))

                        elif ALTO_VENTANA // 2 + 250 <= mouse_pos[1] <= ALTO_VENTANA // 2 + 350:
                            pantalla_actual = "principal"
                            cambiar_visibilidad_inputboxes_login(1)

        ventana.fill(NEGRO)

        if pantalla_actual == "principal":
            pantalla_principal()
        elif pantalla_actual == "registrar":
            pantalla_registrar()
        elif pantalla_actual == "ingresar":
            pantalla_ingresar()

        manager.update(time_delta)
        manager.draw_ui(ventana)
        pygame.display.update()

if __name__ == "__main__":

    main()

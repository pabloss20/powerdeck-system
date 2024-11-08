from Model.Administrador import Administrador
from Model.Usuario import Usuario
from Model.GestorHash import verificar
from Model.JsonHandler import JsonHandler


def main():
    # Datos para probar el registro y login
    nombre = "Juan"
    apellido = "Perez"
    correo = "juan.perez@ejemplo.com"
    contrasena = "Contraseña123"
    rol_administrador = "juego"  # Solo para administrador, puede ser 'juego' o 'reportes'

    # Probar el registro de un nuevo Administrador
    print("Registro de Administrador:")
    try:
        # Crear un nuevo administrador
        nuevo_administrador = Administrador(nombre, apellido, correo, contrasena, rol_administrador)
        print(f"Administrador {nombre} {apellido} registrado exitosamente.")
    except ValueError as e:
        print(f"Error al registrar el administrador: {e}")

    # Intentar iniciar sesión con las credenciales correctas
    print("\nIniciar sesión con las credenciales correctas:")
    resultado = Usuario.iniciar_sesion(correo, contrasena)

    if resultado == 1:
        print("Inicio de sesión exitoso como Jugador.")
    elif resultado == 2:
        print("Inicio de sesión exitoso como Administrador de Juego.")
    elif resultado == 3:
        print("Inicio de sesión exitoso como Administrador de Reportes.")
    elif isinstance(resultado, str):
        print(f"Error en el inicio de sesión: {resultado}")
    else:
        print("Credenciales incorrectas o no encontradas.")

    # Intentar iniciar sesión con una contraseña incorrecta
    print("\nIniciar sesión con la contraseña incorrecta:")
    resultado_incorrecto = Usuario.iniciar_sesion(correo, "ContraseñaIncorrecta")

    if isinstance(resultado_incorrecto, str):
        print(f"Error en el inicio de sesión: {resultado_incorrecto}")
    else:
        print("Sesión iniciada exitosamente (esto no debería suceder).")


if __name__ == "__main__":
    main()

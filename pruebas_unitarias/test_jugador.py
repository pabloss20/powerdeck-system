import os
import json
import pytest
from datetime import datetime
from Model.Jugador import Jugador

@pytest.fixture
def jugador_temporal():
    """Fixture para crear un jugador temporal para pruebas."""
    json_path = 'jugadores.json'
    if os.path.exists(json_path):
        os.remove(json_path)

    jugador = Jugador(
        nombre="Juan",
        apellido="Pérez",
        correo="juan.perez@example.com",
        contrasena="contrasena123",
        fecha_nacimiento="1990-01-01",
        imagen_perfil="ruta/a/imagen.png",
        pais="Costa Rica",
        nombre_usuario="juanperez"
    )
    return jugador

def test_crear_jugador(jugador_temporal):
    """Prueba que un jugador se crea correctamente."""
    assert jugador_temporal.nombre == "Juan"
    assert jugador_temporal.apellido == "Pérez"
    assert jugador_temporal.correo == "juan.perez@example.com"
    assert jugador_temporal.nombre_usuario == "juanperez"
    assert isinstance(jugador_temporal.fecha_registro, str)
    assert len(jugador_temporal.id) == 29

def test_validar_datos_faltantes():
    """Prueba que se lance ValueError si faltan datos requeridos."""
    with pytest.raises(ValueError):
        Jugador(
            nombre="",
            apellido="Pérez",
            correo="juan.perez@example.com",
            contrasena="contrasena123",
            fecha_nacimiento="1990-01-01",
            imagen_perfil="ruta/a/imagen.png",
            pais="Costa Rica",
            nombre_usuario="juanperez"
        )

def test_registrar_jugador(jugador_temporal):
    """Prueba que el jugador se registra correctamente en el JSON."""
    with open('jugadores.json', 'r') as f:
        jugadores = json.load(f)

    assert len(jugadores) == 1
    assert jugadores[0]['nombre_usuario'] == "juanperez"
    assert jugadores[0]['correo'] == "juan.perez@example.com"

def test_generar_id_unico(jugador_temporal):
    """Prueba que la ID generada es única."""
    id_original = jugador_temporal.id
    nuevo_jugador = Jugador(
        nombre="Maria",
        apellido="Gómez",
        correo="maria.gomez@example.com",
        contrasena="contrasena123",
        fecha_nacimiento="1995-01-01",
        imagen_perfil="ruta/a/imagen2.png",
        pais="Costa Rica",
        nombre_usuario="mariagomez"
    )
    assert nuevo_jugador.id != id_original

if __name__ == "__main__":
    pytest.main()

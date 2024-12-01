# test_cartas.py

import os
import json
import pytest
from datetime import datetime
from Model.Carta import Raza, Tipo_de_Carta, Atributos, Carta, cargar_cartas, es_variante

@pytest.fixture
def atributos():
    """Fixture para crear atributos de prueba."""
    return Atributos(
        poder=10, velocidad=20, magia=30, defensa=40, inteligencia=50,
        altura=60, fuerza=70, agilidad=80, salto=90, resistencia=100,
        flexibilidad=50, explosividad=50, carisma=50, habilidad=50,
        balance=50, sabiduría=50, suerte=50, coordinacion=50,
        amabilidad=50, lealtad=50, disciplina=50, liderazgo=50,
        prudencia=50, confianza=50, percepcion=50, valentia=50
    )

@pytest.fixture
def carta_temporal(atributos):
    """Fixture para crear una carta temporal para pruebas."""
    # Asegúrate de que el archivo JSON no exista antes de la prueba
    json_path = 'cartas.json'
    if os.path.exists(json_path):
        os.remove(json_path)

    carta = Carta(
        nombre_personaje="Heroe",
        descripcion="Un héroe valiente.",
        nombre_variante="Heroe Feroz",
        raza=Raza.HUMANO,
        imagen="ruta/a/imagen.png",
        tipo_carta=Tipo_de_Carta.NORMAL,
        turno_poder=1,
        bonus_poder=5,
        atributos=atributos
    )
    return carta

def test_crear_carta(carta_temporal):
    """Prueba que una carta se crea correctamente."""
    assert carta_temporal.nombre_personaje == "Heroe"
    assert carta_temporal.descripcion == "Un héroe valiente."
    assert carta_temporal.raza == Raza.HUMANO.value
    assert carta_temporal.tipo_carta == Tipo_de_Carta.NORMAL.value
    assert carta_temporal.turno_poder == 1
    assert carta_temporal.bonus_poder == 5
    assert carta_temporal.atributos.poder_total == 1350  # Verifica la suma de atributos

def test_validar_datos_faltantes(carta_temporal):
    """Prueba que se lance ValueError si faltan datos requeridos."""
    with pytest.raises(ValueError):
        Carta(
            nombre_personaje="",
            descripcion="Falta el nombre.",
            nombre_variante="Variante",
            raza=Raza.HUMANO,
            imagen="ruta/a/imagen.png",
            tipo_carta=Tipo_de_Carta.NORMAL,
            turno_poder=1,
            bonus_poder=5,
            atributos=carta_temporal.atributos
        )

def test_generar_llave(carta_temporal):
    """Prueba que la llave generada es única."""
    llave_original = carta_temporal.llave
    nueva_carta = Carta(
        nombre_personaje="Villano",
        descripcion="Un villano malvado.",
        nombre_variante="Villano Astuto",
        raza=Raza.ORCO,
        imagen="ruta/a/imagen_villano.png",
        tipo_carta=Tipo_de_Carta.ULTRA_RARA,
        turno_poder=2,
        bonus_poder=10,
        atributos=carta_temporal.atributos
    )
    assert nueva_carta.llave != llave_original

def test_cargar_cartas():
    """Prueba que se carguen las cartas desde el archivo JSON."""
    # Asegúrate de que el archivo JSON exista y contenga datos
    with open('cartas.json', 'w') as f:
        json.dump([{
            'nombre_personaje': "Heroe",
            'descripcion': "Un héroe valiente.",
            'nombre_variante': "Heroe Feroz",
            'fecha_creacion': datetime.now().isoformat(),
            'raza': Raza.HUMANO.value,
            'imagen': "ruta/a/imagen.png",
            'tipo_carta': Tipo_de_Carta.NORMAL.value,
            'activa_en_juego': True,
            'activa_en_sobres': True,
            'turno_poder': 1,
            'bonus_poder': 5,
            'atributos': vars(Atributos(10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50)),
            'llave': "C-XYZ-V-123",
            'es_variante': False
        }], f, indent=4)

    cartas = cargar_cartas()
    assert len(cartas) > 0
    assert cartas[0]['nombre_personaje'] == "Heroe"

def test_es_variante():
    """Prueba que se determine correctamente si una carta es variante."""
    # Asegúrate de que el archivo JSON tenga una carta para probar
    with open('cartas.json', 'w') as f:
        json.dump([{
            'nombre_personaje': "Heroe",
            'nombre_variante': "Heroe Feroz"
        }], f, indent=4)

    resultado = es_variante("Heroe", "Heroe1")
    assert resultado == "Variante"

    resultado_no_variante = es_variante("Herowe", "Heroe Normal")
    assert resultado_no_variante == "No Variante"

# Ejecutar pytest para que se ejecute la prueba
if __name__ == "__main__":
    pytest.main()

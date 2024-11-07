import pytest
from Model.GeneradorLlave import generar_llave

@pytest.fixture
def categorias_ua():
    """Fixture para proporcionar categorías U y A."""
    return "U", "A"


@pytest.fixture
def categorias_ur():
    """Fixture para proporcionar categorías U y R."""
    return "U", "R"


def test_generar_llave_ua(categorias_ua):
    """Prueba que generar_llave genera una llave correctamente con categorías U y A."""
    categoria_principal, categoria_secundaria = categorias_ua
    llave_generada = generar_llave(categoria_principal, categoria_secundaria)

    assert isinstance(llave_generada, str)  # La llave debe ser de tipo str
    assert llave_generada.startswith("U-") and "-A" in llave_generada  # Verifica formato correcto
    assert len(llave_generada.split("-")) == 4  # Debe tener 4 partes


def test_generar_llave_ur(categorias_ur):
    """Prueba que generar_llave genera una llave correctamente con categorías U y R."""
    categoria_principal, categoria_secundaria = categorias_ur
    llave_generada = generar_llave(categoria_principal, categoria_secundaria)

    assert isinstance(llave_generada, str)  # La llave debe ser de tipo str
    assert llave_generada.startswith("U-") and "-R" in llave_generada  # Verifica formato correcto
    assert len(llave_generada.split("-")) == 4  # Debe tener 4 partes


if __name__ == "__main__":
    pytest.main()

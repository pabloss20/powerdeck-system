
import pytest
from Model.GestorHash import encriptar, verificar

@pytest.fixture
def contraseña():
    """Fixture para proporcionar una contraseña de prueba."""
    return "mi_contrasena_segura"

def test_encriptar(contraseña):
    """Prueba que el hash de la contraseña se genere correctamente."""
    hash_generado = encriptar(contraseña)
    assert isinstance(hash_generado, bytes)  # El hash debe ser de tipo bytes
    assert hash_generado != contraseña.encode('utf-8')  # Asegura que no es la contraseña en texto plano

def test_verificar_contraseña_correcta(contraseña):
    """Prueba que verificar confirme correctamente la contraseña original."""
    hash_generado = encriptar(contraseña)
    assert verificar(contraseña, hash_generado)  # La contraseña debe coincidir con el hash

def test_verificar_contraseña_incorrecta(contraseña):
    """Prueba que verificar falle con una contraseña incorrecta."""
    hash_generado = encriptar(contraseña)
    assert not verificar("contrasena_incorrecta", hash_generado)  # La contraseña incorrecta no debe coincidir

if __name__ == "__main__":
    pytest.main()

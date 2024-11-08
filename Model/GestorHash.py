import bcrypt

def encriptar(password: str) -> bytes:
    """
    Genera un hash seguro de la contraseña utilizando bcrypt.

    Args:
        password (str): La contraseña a encriptar.

    Returns:
        bytes: El hash de la contraseña.
    """

    hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    return hashed

def verificar(password: str, hashed: bytes) -> bool:
    """
    Verifica si una contraseña coincide con su hash.

    Args:
        password (str): La contraseña a verificar.
        hashed (bytes): El hash de la contraseña original.

    Returns:
        bool: True si la contraseña es correcta, False de lo contrario.
    """

    return bcrypt.checkpw(password.encode('utf-8'), hashed)

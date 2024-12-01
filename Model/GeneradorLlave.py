
import random
import string

def generar_llave(categoria_principal, categoria_secundaria):
    codigo_primario = ''.join(random.choices(string.ascii_letters + string.digits, k=12))
    codigo_secundario = ''.join(random.choices(string.ascii_letters + string.digits, k=12))
    return f"{categoria_principal}-{codigo_primario}-{categoria_secundaria}-{codigo_secundario}"
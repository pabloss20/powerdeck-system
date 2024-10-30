# CartaSelector.py
import random
from JsonHandlerX import JsonHandlerX

class CartaSelector:
    PROBABILIDADES = {
        "Ultrarara": 0.05,
        "Muy rara": 0.12,
        "Rara": 0.18,
        "Normal": 0.25,
        "Basica": 0.40
    }

    def __init__(self):
        self.json_handler = JsonHandlerX('../Files/cartasx.json')
        self.cartas = self.json_handler.cargar_info()

    def seleccionar_cartas(self, cantidad):
        seleccionadas = []
        cartas_disponibles = self.cartas.copy()  # Se copian las cartas para poder eliminarlas (para evitar repeticiones)

        while len(seleccionadas) < cantidad and cartas_disponibles:
            carta = random.choices(     # azar con pesos (probabilidades)
                cartas_disponibles,
                weights=[self.PROBABILIDADES.get(carta["tipo_carta"], 0) for carta in cartas_disponibles], # probabilidades ya definidas
                k=1
            )[0]

            seleccionadas.append(carta)
            cartas_disponibles.remove(carta)  # Se elimina la carta seleccionada de la lista disponible (para evitar repeticiones)

        return seleccionadas

    def mostrar_resultados(self, seleccionadas):
        print("Cartas seleccionadas y sus rarezas con probabilidades:")
        for carta in seleccionadas:
            rareza = carta['tipo_carta']
            probabilidad = self.PROBABILIDADES.get(rareza, 0) * 100
            print(f"{carta['nombre_personaje']} - Rareza: {rareza} - Probabilidad: {probabilidad:.2f}%")


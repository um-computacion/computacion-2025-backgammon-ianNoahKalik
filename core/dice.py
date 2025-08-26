# core/dice.py

import random

class Dado:
    """
    Representa un dado de Backgammon.
    Permite lanzar y obtener valores entre 1 y 6.
    """

    def __init__(self):
        self.valor = None

    def lanzar(self):
        """Lanza el dado y guarda el valor obtenido."""
        self.valor = random.randint(1, 6)
        return self.valor
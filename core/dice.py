

import random

class Dado:
    """
    Representa un dado de Backgammon.
    Permite lanzar y obtener valores entre 1 y 6.
    """

    VALORES_VALIDOS = [1, 2, 3, 4, 5, 6]

    def __init__(self):
        self.valor = None
        self.lanzado = False

    def lanzar(self):
        """Lanza el dado y guarda el valor obtenido."""
        self.valor = random.randint(1, 6)
        self.lanzado = True
        return self.valor

    def obtener_valor(self):
        """
        Devuelve el valor actual del dado.
        Lanza excepción si aún no fue lanzado.
        """
        if not self.lanzado:
            raise ValueError("El dado aún no fue lanzado")
        return self.valor

    def reiniciar(self):
        """Reinicia el estado del dado (sin valor)."""
        self.valor = None
        self.lanzado = False

    def __str__(self):
        """Representación textual del dado."""
        return f"[{self.valor if self.lanzado else '-'}]"
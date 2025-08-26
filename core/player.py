# core/player.py

class Jugador:
    """
    Representa a un jugador del juego.
    Tiene un color (blanco o negro) y sus fichas.
    """

    def __init__(self, nombre: str, color: int):
        self.nombre = nombre
        self.color = color
        self.fichas_capturadas = 0
        self.fichas_salidas = 0
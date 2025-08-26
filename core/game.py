# core/game.py

from core.board import Tablero
from core.player import Jugador
from core.dice import Dado

class JuegoBackgammon:
    """
    Clase principal que gestiona el flujo del juego.
    Controla el tablero, los jugadores y los turnos.
    """

    def __init__(self, nombre_blanco="Jugador 1", nombre_negro="Jugador 2"):
        self.tablero = Tablero()
        self.jugador_blanco = Jugador(nombre_blanco, Tablero.BLANCO)
        self.jugador_negro = Jugador(nombre_negro, Tablero.NEGRO)
        self.dado1 = Dado()
        self.dado2 = Dado()
        self.turno_actual = self.jugador_blanco
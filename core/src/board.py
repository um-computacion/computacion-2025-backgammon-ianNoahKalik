class TableroError(Exception):
    pass


class Tablero:
    """
    Representa el tablero de Backgammon con 24 puntos, la barra y el borne off.
    Cada punto se modela con un entero:
      >0: fichas blancas
      <0: fichas negras
    """

    BLANCO = 1
    NEGRO = -1
    PUNTOS_CONTADOS = 24 

    def __init__(self):
        self.reset()

    def reset(self):
        """Inicializa el tablero en la posición estándar y limpia la barra."""
        # Lista de 24 puntos inicializados a cero
        self.puntos = [0] * self.PUNTOS_CONTADOS

        # Colocación estándar de fichas blancas
        self.puntos[0]  = 2 * self.BLANCO
        self.puntos[11] = 5 * self.BLANCO
        self.puntos[16] = 3 * self.BLANCO
        self.puntos[18] = 5 * self.BLANCO

        # Colocación estándar de fichas negras
        self.puntos[23] = 2 * self.NEGRO
        self.puntos[12] = 5 * self.NEGRO
        self.puntos[7]  = 3 * self.NEGRO
        self.puntos[5]  = 5 * self.NEGRO

        # Barra de fichas capturadas pendientes de reingreso
        self.barra = { self.BLANCO: 0, self.NEGRO: 0 }
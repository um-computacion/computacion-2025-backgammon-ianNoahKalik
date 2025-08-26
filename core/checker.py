# core/checker.py

class Ficha:
    """
    Representa una ficha individual de Backgammon.
    Puede pertenecer al jugador blanco o negro.
    """

    def __init__(self, color: int):
        """
        color: 1 para blanco, -1 para negro
        """
        self.color = color
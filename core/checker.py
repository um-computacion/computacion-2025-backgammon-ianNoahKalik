class Ficha:
    """
    Representa una ficha individual de Backgammon.
    Puede pertenecer al jugador blanco (1) o negro (-1).
    """

    def __init__(self, color: int):
        if color not in (1, -1):
            raise ValueError("El color debe ser 1 (blanco) o -1 (negro)")
        self.color = color
        self.capturada = False

    def capturar(self):
        self.capturada = True

    def liberar(self):
        self.capturada = False

    def es_blanca(self) -> bool:
        return self.color == 1

    def es_negra(self) -> bool:
        return self.color == -1

    def esta_capturada(self) -> bool:
        return self.capturada

    def __str__(self):
        estado = "Capturada" if self.capturada else "Activa"
        color_str = "Blanca" if self.color == 1 else "Negra"
        return f"Ficha {color_str} ({estado})"
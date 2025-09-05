class Ficha:
    """
    Representa una ficha individual de Backgammon.
    Puede pertenecer al jugador blanco (1) o negro (-1).
    """

    def __init__(self, color: int):
        """
        color: 1 para blanco, -1 para negro
        """
        if color not in (1, -1):
            raise ValueError("El color debe ser 1 (blanco) o -1 (negro)")
        self.color = color
        self.capturada = False  # Estado de captura

    def capturar(self):
        """Marca la ficha como capturada."""
        self.capturada = True

    def liberar(self):
        """Libera la ficha capturada."""
        self.capturada = False

    def es_blanca(self) -> bool:
        """Retorna True si la ficha es blanca."""
        return self.color == 1

    def es_negra(self) -> bool:
        """Retorna True si la ficha es negra."""
        return self.color == -1

    def esta_capturada(self) -> bool:
        """Retorna True si la ficha está capturada."""
        return self.capturada

    def __str__(self):
        estado = "Capturada" if self.capturada else "Activa"
        color_str = "Blanca" if self.color == 1 else "Negra"
        return f"Ficha {color_str} ({estado})"
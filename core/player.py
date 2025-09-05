from core.dice import Dado
class Jugador:
    """
    Representa a un jugador de Backgammon.
    Tiene nombre, color, fichas capturadas/salidas, y su dado.
    """

    def __init__(self, nombre: str, color: int):
        self.nombre = nombre
        self.color = color  # 0 = blanco, 1 = negro
        self.fichas_capturadas = 0
        self.fichas_salidas = 0
        self.dado = Dado()
        self.fichas_en_tablero = 15  # Valor inicial estándar
        self.movimientos_disponibles = []  # Se actualiza tras lanzar el dado

    def jugar_turno(self):
        """
        Lanza el dado y guarda los movimientos disponibles.
        """
        valor = self.dado.lanzar()
        self.movimientos_disponibles = [valor]  # Se puede extender a dobles
        print(f"{self.nombre} lanzó el dado y obtuvo: {valor}")
        return valor

    def capturar_ficha(self):
        """
        Incrementa el contador de fichas capturadas.
        """
        self.fichas_capturadas += 1
        print(f"{self.nombre} capturó una ficha. Total: {self.fichas_capturadas}")

    def sacar_ficha(self):
        """
        Incrementa el contador de fichas salidas.
        """
        if self.fichas_en_tablero > 0:
            self.fichas_salidas += 1
            self.fichas_en_tablero -= 1
            print(f"{self.nombre} sacó una ficha. Total salidas: {self.fichas_salidas}")
        else:
            print(f"{self.nombre} no tiene fichas en el tablero.")

    def reiniciar_turno(self):
        """
        Reinicia el dado y los movimientos disponibles.
        """
        self.dado.reiniciar()
        self.movimientos_disponibles = []

    def __str__(self):
        return (f"Jugador: {self.nombre} | Color: {'Blanco' if self.color == 0 else 'Negro'} | "
                f"Capturadas: {self.fichas_capturadas} | Salidas: {self.fichas_salidas} | "
                f"En tablero: {self.fichas_en_tablero}")
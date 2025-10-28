from core.dice import Dado

class Jugador:
    def __init__(self, nombre: str, color: str):
        self.nombre = nombre
        self.color = color  # "Blancas" o "Negras"
        self.dado = Dado()
        self.fichas_capturadas = 0
        self.fichas_salidas = 0
        self.fichas_en_tablero = 15
        self.movimientos_disponibles = []

    def color_str(self):
        return self.color

    def jugar_turno(self):
        valor = self.dado.lanzar()
        self.movimientos_disponibles = [valor]
        print(f"{self.nombre} lanzó el dado y obtuvo: {valor}")
        return valor

    def capturar_ficha(self):
        self.fichas_capturadas += 1
        print(f"{self.nombre} capturó una ficha. Total: {self.fichas_capturadas}")

    def sacar_ficha(self):
        if self.fichas_en_tablero > 0:
            self.fichas_salidas += 1
            self.fichas_en_tablero -= 1
            print(f"{self.nombre} sacó una ficha. Total salidas: {self.fichas_salidas}")
        else:
            print(f"{self.nombre} no tiene fichas en el tablero.")

    def reiniciar_turno(self):
        self.dado.reiniciar()
        self.movimientos_disponibles = []

    def __str__(self):
        return (f"Jugador: {self.nombre} | Color: {self.color} | "
                f"Capturadas: {self.fichas_capturadas} | Salidas: {self.fichas_salidas} | "
                f"En tablero: {self.fichas_en_tablero}")
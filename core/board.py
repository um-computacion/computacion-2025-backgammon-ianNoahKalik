class TableroError(Exception):
    pass

class Tablero:

    BLANCO = 1
    NEGRO = -1
    TOTAL_PUNTOS = 24

    def __init__(self):
        self.reset()

    def reset(self):
        """Inicializa el tablero en la posición estándar y limpia la barra."""
        self.puntos = [0] * self.TOTAL_PUNTOS

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

        self.barra = { self.BLANCO: 0, self.NEGRO: 0 }
        self.borne_off = { self.BLANCO: 0, self.NEGRO: 0 }

    def _validar_jugador(self, jugador: int):
        if jugador not in (self.BLANCO, self.NEGRO):
            raise TableroError("Jugador inválido")

    def obtener_punto(self, indice: int) -> int:
        if not (0 <= indice < self.TOTAL_PUNTOS):
            raise TableroError(f"Índice de punto fuera de rango: {indice}")
        return self.puntos[indice]

    def punto_disponible(self, indice: int, jugador: int) -> bool:
        ocupacion = self.obtener_punto(indice)
        if ocupacion == 0:
            return True
        if ocupacion * jugador > 0:
            return True
        if abs(ocupacion) == 1:
            return True
        return False

    def mover_pieza(self, jugador: int, origen: int, destino: int):
        self._validar_jugador(jugador)

        if not (0 <= origen < self.TOTAL_PUNTOS):
            raise TableroError(f"Origen fuera de rango: {origen}")
        if not (0 <= destino < self.TOTAL_PUNTOS):
            raise TableroError(f"Destino fuera de rango: {destino}")

        if self.puntos[origen] * jugador <= 0:
            raise TableroError("No hay ficha propia en el punto de origen")

        if not self.punto_disponible(destino, jugador):
            raise TableroError("Destino bloqueado por 2 o más fichas enemigas")

        self.puntos[origen] -= jugador

        if self.puntos[destino] * jugador < 0:
            self.barra[-jugador] += 1
            self.puntos[destino] = 0

        self.puntos[destino] += jugador

    def hay_en_barra(self, jugador: int) -> bool:
        """Indica si el jugador tiene fichas en la barra."""
        self._validar_jugador(jugador)
        return self.barra[jugador] > 0

    def reingresar_desde_barra(self, jugador: int, destino: int):
        """Reingresa una ficha del jugador desde la barra al punto destino."""
        self._validar_jugador(jugador)

        if self.barra[jugador] == 0:
            raise TableroError("No hay fichas en la barra para reingresar")

        if not (0 <= destino < self.TOTAL_PUNTOS):
            raise TableroError(f"Destino fuera de rango: {destino}")

        if not self.punto_disponible(destino, jugador):
            raise TableroError("Destino bloqueado para reingreso")

        self.barra[jugador] -= 1

        if self.puntos[destino] * jugador < 0:
            self.barra[-jugador] += 1
            self.puntos[destino] = 0

        self.puntos[destino] += jugador

    def agregar_a_fuera(self, jugador: int):
        """Agrega una ficha del jugador a la zona de borne-off."""
        self._validar_jugador(jugador)
        self.borne_off[jugador] += 1

    def obtener_fuera(self, jugador: int) -> int:
        """Devuelve la cantidad de fichas borneadas por el jugador."""
        self._validar_jugador(jugador)
        return self.borne_off[jugador]


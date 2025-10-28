from core.excepciones import (
    MovimientoInvalido,
    PosicionFueraDeRango,
    OrigenSinFicha,
    DestinoBloqueado,
    NoPuedeReingresar,
    NoPuedeSacarFicha
)

class Tablero:
    BLANCO = "Blancas"
    NEGRO = "Negras"

    def __init__(self):
        self._tablero = [[] for _ in range(24)]
        self._piezas_comidas = {self.BLANCO: 0, self.NEGRO: 0}
        self._barra = {self.BLANCO: 0, self.NEGRO: 0}

    def inicializar_piezas(self):
        self._tablero = [[] for _ in range(24)]
        self._tablero[0] = [self.BLANCO] * 2
        self._tablero[5] = [self.NEGRO] * 5
        self._tablero[7] = [self.NEGRO] * 3
        self._tablero[11] = [self.BLANCO] * 5
        self._tablero[12] = [self.NEGRO] * 5
        self._tablero[16] = [self.BLANCO] * 3
        self._tablero[18] = [self.BLANCO] * 5
        self._tablero[23] = [self.NEGRO] * 2
        self._barra = {self.BLANCO: 0, self.NEGRO: 0}
        self._piezas_comidas = {self.BLANCO: 0, self.NEGRO: 0}

    def mostrar_tablero(self):
        return self._tablero

    def mostrar_tablero_visual(self):
        visual = "\n🟫 Tablero de Backgammon 🟫\n\n"
        visual += "↘️ Puntos 12 a 1 (lado superior)\n"
        for i in reversed(range(12)):
            punto = self._tablero[i]
            contenido = "".join("⚪" if ficha == self.BLANCO else "⚫" for ficha in punto)
            visual += f"{i:02d}: {contenido:<6}  "
        visual += "\n\n↗️ Puntos 13 a 24 (lado inferior)\n"
        for i in range(12, 24):
            punto = self._tablero[i]
            contenido = "".join("⚪" if ficha == self.BLANCO else "⚫" for ficha in punto)
            visual += f"{i:02d}: {contenido:<6}  "
        visual += "\n"
        return visual

    def piezas_comidas(self):
        return self._piezas_comidas

    def fichas_en_barra(self, color: str):
        return self._barra[color]

    def sacar_pieza(self, posicion: int):
        if posicion < 0 or posicion > 23:
            raise PosicionFueraDeRango(f"La posición {posicion} está fuera del tablero (0-23).")
        if self._tablero[posicion]:
            return self._tablero[posicion].pop()
        else:
            raise OrigenSinFicha(f"No hay fichas en la posición {posicion}.")

    def colocar_pieza(self, posicion: int, color: str):
        if posicion < 0 or posicion > 23:
            raise PosicionFueraDeRango(f"La posición {posicion} está fuera del tablero (0-23).")
        self._tablero[posicion].append(color)

    def mover_pieza(self, origen: int, destino: int):
        if not self._tablero[origen]:
            raise OrigenSinFicha(f"No hay fichas en la posición {origen}.")
        color = self._tablero[origen][-1]
        self.validar_movimiento(origen, destino, color)

        pieza = self.sacar_pieza(origen)

        if (self._tablero[destino] and
            self._tablero[destino][-1] != color and
            len(self._tablero[destino]) == 1):
            color_comido = self._tablero[destino].pop()
            self._piezas_comidas[color_comido] += 1
            self._barra[color_comido] += 1

        self.colocar_pieza(destino, pieza)

    def validar_movimiento(self, origen: int, destino: int, color: str):
        if origen < 0 or origen > 23 or destino < 0 or destino > 23:
            raise PosicionFueraDeRango("Las posiciones deben estar entre 0 y 23.")
        if not self._tablero[origen]:
            raise OrigenSinFicha(f"No hay fichas en la posición {origen}.")
        if self._tablero[origen][-1] != color:
            raise MovimientoInvalido(f"La ficha en posición {origen} no pertenece al jugador {color}.")
        if (self._tablero[destino] and
            self._tablero[destino][-1] != color and
            len(self._tablero[destino]) > 1):
            raise DestinoBloqueado(f"La posición {destino} está bloqueada por fichas enemigas.")
        return True

    def reingresar_desde_barra(self, color: str, destino: int):
        if destino < 0 or destino > 23:
            raise PosicionFueraDeRango(f"La posición {destino} está fuera del tablero (0-23).")
        if self._barra[color] <= 0:
            raise NoPuedeReingresar(f"No hay fichas de color {color} en la barra para reingresar.")
        if (self._tablero[destino] and
            self._tablero[destino][-1] != color and
            len(self._tablero[destino]) > 1):
            raise DestinoBloqueado(f"No se puede reingresar en posición {destino}: está bloqueada.")
        if (self._tablero[destino] and
            self._tablero[destino][-1] != color and
            len(self._tablero[destino]) == 1):
            color_comido = self._tablero[destino].pop()
            self._piezas_comidas[color_comido] += 1
            self._barra[color_comido] += 1
        self._tablero[destino].append(color)
        self._barra[color] -= 1
        return True

    def puede_reingresar(self, color: str, dados: list):
        if self._barra[color] == 0:
            return False
        posiciones = [dado - 1 if color == self.BLANCO else 24 - dado for dado in dados]
        for pos in posiciones:
            if 0 <= pos <= 23:
                if (not self._tablero[pos] or
                    self._tablero[pos][-1] == color or
                    len(self._tablero[pos]) == 1):
                    return True
        return False

    def todas_en_home(self, color: str):
        home = range(18, 24) if color == self.BLANCO else range(0, 6)
        for i, punto in enumerate(self._tablero):
            if punto and punto[0] == color and i not in home:
                return False
        return self._barra[color] == 0

    def sacar_ficha_fuera(self, color: str, origen: int):
        if origen < 0 or origen > 23:
            raise PosicionFueraDeRango(f"La posición {origen} está fuera del tablero (0-23).")
        if not self._tablero[origen]:
            raise OrigenSinFicha(f"No hay fichas en la posición {origen} para sacar.")
        if self._tablero[origen][-1] != color:
            raise MovimientoInvalido(f"La ficha en posición {origen} no pertenece al jugador {color}.")
        if not self.todas_en_home(color):
            raise NoPuedeSacarFicha(f"No se puede sacar fichas: no todas las fichas de {color} están en el home.")
        self._tablero[origen].pop()
        return True
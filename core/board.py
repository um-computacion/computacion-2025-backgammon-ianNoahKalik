from core.excepciones import (
    MovimientoInvalido,
    PosicionFueraDeRango,
    OrigenSinFicha,
    DestinoBloqueado,
    NoPuedeReingresar,
    NoPuedeSacarFicha
)
from core.checker import Ficha

class Tablero:
    BLANCO = "Blancas"
    NEGRO = "Negras"

    def __init__(self):
        self._tablero = [[] for _ in range(24)]
        self._piezas_comidas = {self.BLANCO: 0, self.NEGRO: 0}
        self._barra = {self.BLANCO: [], self.NEGRO: []}
        self._fichas_fuera = {self.BLANCO: [], self.NEGRO: []}

    def inicializar_piezas(self):
        self._tablero = [[] for _ in range(24)]
        self._tablero[0] = [Ficha(1) for _ in range(2)]
        self._tablero[5] = [Ficha(-1) for _ in range(5)]
        self._tablero[7] = [Ficha(-1) for _ in range(3)]
        self._tablero[11] = [Ficha(1) for _ in range(5)]
        self._tablero[12] = [Ficha(-1) for _ in range(5)]
        self._tablero[16] = [Ficha(1) for _ in range(3)]
        self._tablero[18] = [Ficha(1) for _ in range(5)]
        self._tablero[23] = [Ficha(-1) for _ in range(2)]
        self._barra = {self.BLANCO: [], self.NEGRO: []}
        self._piezas_comidas = {self.BLANCO: 0, self.NEGRO: 0}
        self._fichas_fuera = {self.BLANCO: [], self.NEGRO: []}

    def mostrar_tablero(self):
        return self._tablero

    def mostrar_tablero_visual(self):
        visual = "\n Tablero de Backgammon \n\n"
        visual += "↘ Puntos 12 a 1 (lado superior)\n"
        for i in reversed(range(12)):
            punto = self._tablero[i]
            contenido = "".join("⚪" if ficha.es_blanca() else "⚫" for ficha in punto)
            visual += f"{i:02d}: {contenido:<6}  "
        visual += "\n\n↗ Puntos 13 a 24 (lado inferior)\n"
        for i in range(12, 24):
            punto = self._tablero[i]
            contenido = "".join("⚪" if ficha.es_blanca() else "⚫" for ficha in punto)
            visual += f"{i:02d}: {contenido:<6}  "
        visual += "\n"
        return visual

    def piezas_comidas(self):
        return self._piezas_comidas

    def fichas_en_barra(self, color: str):
        return len(self._barra[color])

    def fichas_fuera(self, color: str):
        return self._fichas_fuera[color]

    def sacar_pieza(self, posicion: int):
        if posicion < 0 or posicion > 23:
            raise PosicionFueraDeRango(f"La posición {posicion} está fuera del tablero (0-23).")
        if self._tablero[posicion]:
            return self._tablero[posicion].pop()
        else:
            raise OrigenSinFicha(f"No hay fichas en la posición {posicion}.")

    def colocar_pieza(self, posicion: int, ficha: Ficha):
        if posicion < 0 or posicion > 23:
            raise PosicionFueraDeRango(f"La posición {posicion} está fuera del tablero (0-23).")
        self._tablero[posicion].append(ficha)

    def mover_pieza(self, origen: int, destino: int):
        if not self._tablero[origen]:
            raise OrigenSinFicha(f"No hay fichas en la posición {origen}.")
        ficha = self._tablero[origen][-1]
        color = self.BLANCO if ficha.es_blanca() else self.NEGRO
        self.validar_movimiento(origen, destino, color)

        ficha = self.sacar_pieza(origen)

        if (self._tablero[destino] and
            self._tablero[destino][-1].color != ficha.color and
            len(self._tablero[destino]) == 1):
            ficha_comida = self._tablero[destino].pop()
            ficha_comida.capturar()
            color_comido = self.BLANCO if ficha_comida.es_blanca() else self.NEGRO
            self._piezas_comidas[color_comido] += 1
            self._barra[color_comido].append(ficha_comida)

        self.colocar_pieza(destino, ficha)

    def validar_movimiento(self, origen: int, destino: int, color: str):
        if origen < 0 or origen > 23 or destino < 0 or destino > 23:
            raise PosicionFueraDeRango("Las posiciones deben estar entre 0 y 23.")
        if not self._tablero[origen]:
            raise OrigenSinFicha(f"No hay fichas en la posición {origen}.")
        ficha = self._tablero[origen][-1]
        if (color == self.BLANCO and not ficha.es_blanca()) or (color == self.NEGRO and not ficha.es_negra()):
            raise MovimientoInvalido(f"La ficha en posición {origen} no pertenece al jugador {color}.")
        if (self._tablero[destino] and
            self._tablero[destino][-1].color != ficha.color and
            len(self._tablero[destino]) > 1):
            raise DestinoBloqueado(f"La posición {destino} está bloqueada por fichas enemigas.")
        return True

    def reingresar_desde_barra(self, color: str, destino: int):
        if destino < 0 or destino > 23:
            raise PosicionFueraDeRango(f"La posición {destino} está fuera del tablero (0-23).")
        if not self._barra[color]:
            raise NoPuedeReingresar(f"No hay fichas de color {color} en la barra para reingresar.")
        ficha = self._barra[color].pop()
        if (self._tablero[destino] and
            self._tablero[destino][-1].color != ficha.color and
            len(self._tablero[destino]) > 1):
            raise DestinoBloqueado(f"No se puede reingresar en posición {destino}: está bloqueada.")
        if (self._tablero[destino] and
            self._tablero[destino][-1].color != ficha.color and
            len(self._tablero[destino]) == 1):
            ficha_comida = self._tablero[destino].pop()
            ficha_comida.capturar()
            color_comido = self.BLANCO if ficha_comida.es_blanca() else self.NEGRO
            self._piezas_comidas[color_comido] += 1
            self._barra[color_comido].append(ficha_comida)
        self._tablero[destino].append(ficha)
        return True

    def puede_reingresar(self, color: str, dados: list):
        if not self._barra[color]:
            return False
        posiciones = [dado - 1 if color == self.BLANCO else 24 - dado for dado in dados]
        for pos in posiciones:
            if 0 <= pos <= 23:
                if (not self._tablero[pos] or
                    self._tablero[pos][-1].color == (1 if color == self.BLANCO else -1) or
                    len(self._tablero[pos]) == 1):
                    return True
        return False

    def todas_en_home(self, color: str):
        home = range(18, 24) if color == self.BLANCO else range(0, 6)
        for i, punto in enumerate(self._tablero):
            if punto and ((color == self.BLANCO and punto[0].es_blanca()) or
                          (color == self.NEGRO and punto[0].es_negra())) and i not in home:
                return False
        return not self._barra[color]

    def sacar_ficha_fuera(self, color: str, origen: int):
        if origen < 0 or origen > 23:
            raise PosicionFueraDeRango(f"La posición {origen} está fuera del tablero (0-23).")
        if not self._tablero[origen]:
            raise OrigenSinFicha(f"No hay fichas en la posición {origen} para sacar.")
    
        ficha = self._tablero[origen][-1]
    
        if (color == self.BLANCO and not ficha.es_blanca()) or (color == self.NEGRO and not ficha.es_negra()):
            raise MovimientoInvalido(f"La ficha en posición {origen} no pertenece al jugador {color}.")
    
        if not self.todas_en_home(color):
            raise NoPuedeSacarFicha(f"No se puede sacar fichas: no todas las fichas de {color} están en el home.")
    
        ficha = self._tablero[origen].pop()
        self._fichas_fuera[color].append(ficha)
        return True
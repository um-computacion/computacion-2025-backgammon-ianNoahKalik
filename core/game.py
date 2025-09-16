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

    def lanzar_dados(self):
        self.dado1.lanzar()
        self.dado2.lanzar()
        return self.dado1.valor, self.dado2.valor

    def cambiar_turno(self):
        self.turno_actual = (
            self.jugador_negro if self.turno_actual == self.jugador_blanco
            else self.jugador_blanco
        )

    def obtener_jugador_actual(self):
        return self.turno_actual

    def jugar_turno(self):
        jugador = self.obtener_jugador_actual()
        dado1, dado2 = self.lanzar_dados()

        print(f"{jugador.nombre} lanzó los dados: {dado1} y {dado2}")

        movimientos = [dado1, dado2] if dado1 != dado2 else [dado1] * 4
        jugador.movimientos_disponibles = movimientos

        for movimiento in movimientos:
            if self.tablero.hay_en_barra(jugador.color):
                destino = self.calcular_destino_reingreso(jugador.color, movimiento)
                try:
                    self.tablero.reingresar_desde_barra(jugador.color, destino)
                    print(f"{jugador.nombre} reingresó una ficha desde la barra al punto {destino}")
                except Exception as e:
                    print(f"No se pudo reingresar: {e}")
                    continue
            else:
                origen, destino = self.calcular_movimiento(jugador.color, movimiento)
                try:
                    self.tablero.mover_pieza(jugador.color, origen, destino)
                    print(f"{jugador.nombre} movió ficha de {origen} a {destino}")
                except Exception as e:
                    print(f"No se pudo mover ficha: {e}")
                    continue

            if self.puede_bornear(jugador.color):
                self.tablero.agregar_a_fuera(jugador.color)
                jugador.sacar_ficha()

        self.cambiar_turno()

    def juego_terminado(self):
        return (
            self.tablero.obtener_fuera(self.jugador_blanco.color) == 15 or
            self.tablero.obtener_fuera(self.jugador_negro.color) == 15
        )

    def simular_partida(self):
        while not self.juego_terminado():
            self.jugar_turno()
        ganador = (
            self.jugador_blanco if self.tablero.obtener_fuera(self.jugador_blanco.color) == 15
            else self.jugador_negro
        )
        print(f"¡{ganador.nombre} ha ganado la partida!")

    def obtener_ganador(self):
        if self.tablero.obtener_fuera(self.jugador_blanco.color) == 15:
            return self.jugador_blanco
        elif self.tablero.obtener_fuera(self.jugador_negro.color) == 15:
            return self.jugador_negro
        return None
    
    def reiniciar_partida(self):
        self.tablero.reset()
        for jugador in [self.jugador_blanco, self.jugador_negro]:
            jugador.fichas_capturadas = 0
            jugador.fichas_salidas = 0
            jugador.fichas_en_tablero = 15
            jugador.movimientos_disponibles = []
        self.turno_actual = self.jugador_blanco

    def calcular_destino_reingreso(self, color, movimiento):
        return movimiento - 1 if color == Tablero.BLANCO else Tablero.TOTAL_PUNTOS - movimiento

    def calcular_movimiento(self, color, movimiento):
        # Movimiento ficticio: busca la primera ficha del jugador y la mueve
        puntos = range(Tablero.TOTAL_PUNTOS) if color == Tablero.BLANCO else reversed(range(Tablero.TOTAL_PUNTOS))
        for origen in puntos:
            if self.tablero.obtener_punto(origen) * color > 0:
                destino = origen + movimiento if color == Tablero.BLANCO else origen - movimiento
                if 0 <= destino < Tablero.TOTAL_PUNTOS:
                    return origen, destino
        raise Exception("No se encontró movimiento válido")

    def puede_bornear(self, color):
        # Simulación: si el jugador tiene fichas en el punto final, puede bornear
        extremos = range(18, 24) if color == Tablero.BLANCO else range(0, 6)
        total = sum(abs(self.tablero.obtener_punto(i)) for i in extremos if self.tablero.obtener_punto(i) * color > 0)
        return total > 0
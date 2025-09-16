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
        
        # Acá podrías integrar lógica de movimiento, reingreso, etc.
        # Por ejemplo:
        # self.tablero.mover_pieza(jugador.color, origen, destino)

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
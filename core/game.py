from core.board import Tablero
from core.player import Jugador
from core.dice import Dado
from core.excepciones import (
    PosicionFueraDeRango,
    OrigenSinFicha,
    DestinoBloqueado,
    NoPuedeReingresar,
    NoPuedeSacarFicha,
    MovimientoInvalido
)

class JuegoBackgammon:
    def __init__(self, nombre_blanco="Jugador 1", nombre_negro="Jugador 2"):
        if not nombre_blanco or not nombre_negro:
            raise ValueError("Los nombres de los jugadores no pueden estar vacíos.")
        self.tablero = Tablero()
        self.tablero.inicializar_piezas()
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

    def juego_terminado(self):
        return (
            self.jugador_blanco.fichas_salidas == 15 or
            self.jugador_negro.fichas_salidas == 15
        )

    def obtener_ganador(self):
        if self.jugador_blanco.fichas_salidas == 15:
            return self.jugador_blanco
        elif self.jugador_negro.fichas_salidas == 15:
            return self.jugador_negro
        return None

    def reiniciar_partida(self):
        self.tablero.inicializar_piezas()
        for jugador in [self.jugador_blanco, self.jugador_negro]:
            jugador.fichas_capturadas = 0
            jugador.fichas_salidas = 0
            jugador.fichas_en_tablero = 15
            jugador.movimientos_disponibles = []
        self.turno_actual = self.jugador_blanco

    def calcular_destino_reingreso(self, color, movimiento):
        if movimiento < 1 or movimiento > 6:
            raise ValueError(f"Movimiento inválido para reingreso: {movimiento}")
        return movimiento - 1 if color == Tablero.BLANCO else 24 - movimiento

    def calcular_movimiento(self, color, movimiento):
        puntos = range(24) if color == Tablero.BLANCO else reversed(range(24))
        for origen in puntos:
            try:
                punto = self.tablero.mostrar_tablero()[origen]
                if punto and punto[-1] == color:
                    destino = origen + movimiento if color == Tablero.BLANCO else origen - movimiento
                    if 0 <= destino < 24:
                        return origen, destino
            except (PosicionFueraDeRango, OrigenSinFicha):
                continue
        raise MovimientoInvalido("No se encontró movimiento válido para el jugador.")

    def puede_bornear(self, color):
        extremos = range(18, 24) if color == Tablero.BLANCO else range(0, 6)
        for i in extremos:
            punto = self.tablero.mostrar_tablero()[i]
            if punto and punto[-1] == color:
                return True
        return False

    def jugar_partida_interactiva(self):
        while not self.juego_terminado():
            jugador = self.obtener_jugador_actual()
            print(f"\n🎯 Turno de {jugador.nombre} ({'Blanco' if jugador.color == Tablero.BLANCO else 'Negro'})")
            input("Presioná Enter para lanzar los dados...")
            dado1, dado2 = self.lanzar_dados()
            print(f"{jugador.nombre} lanzó: {dado1} y {dado2}")

            movimientos = [dado1, dado2] if dado1 != dado2 else [dado1] * 4
            jugador.movimientos_disponibles = movimientos

            for movimiento in movimientos:
                print(f"\n➡️ Movimiento disponible: {movimiento}")
                print(self.tablero.mostrar_tablero_visual())

                movimiento_realizado = False
                intentos = 0

                while not movimiento_realizado and intentos < 10:
                    intentos += 1

                    if self.tablero.fichas_en_barra(jugador.color):
                        try:
                            destino = int(input("Tenés fichas en la barra. Elegí destino para reingresar: "))
                            self.tablero.reingresar_desde_barra(jugador.color, destino)
                            print(f"{jugador.nombre} reingresó una ficha al punto {destino}")
                            movimiento_realizado = True
                        except (ValueError, PosicionFueraDeRango, OrigenSinFicha, DestinoBloqueado, NoPuedeReingresar) as e:
                            print(f"⚠️ Error al reingresar: {e}")
                    else:
                        try:
                            origen = int(input("Elegí punto de origen: "))
                            destino = int(input("Elegí punto de destino: "))
                            self.tablero.mover_pieza(origen, destino)
                            print(f"{jugador.nombre} movió ficha de {origen} a {destino}")

                            if self.puede_bornear(jugador.color):
                                punto = self.tablero.mostrar_tablero()[destino]
                                if punto and punto[-1] == jugador.color:
                                    try:
                                        self.tablero.sacar_ficha_fuera(jugador.color, destino)
                                        jugador.sacar_ficha()
                                    except NoPuedeSacarFicha as e:
                                        print(f"⚠️ No se pudo sacar ficha: {e}")
                            movimiento_realizado = True
                        except (ValueError, PosicionFueraDeRango, OrigenSinFicha, DestinoBloqueado, MovimientoInvalido) as e:
                            print(f"⚠️ Movimiento inválido: {e}")

                if not movimiento_realizado:
                    print(f"⏭️ No se pudo realizar el movimiento {movimiento}. Se pierde ese dado.")

            self.cambiar_turno()

        ganador = self.obtener_ganador()
        print(f"\n🏁 ¡{ganador.nombre} ha ganado la partida!")

    def simular_partida(self):
        while not self.juego_terminado():
            jugador = self.obtener_jugador_actual()
            print(f"\n🎯 Turno de {jugador.nombre} ({'Blanco' if jugador.color == Tablero.BLANCO else 'Negro'})")
            dado1, dado2 = self.lanzar_dados()
            print(f"{jugador.nombre} lanzó: {dado1} y {dado2}")

            movimientos = [dado1, dado2] if dado1 != dado2 else [dado1] * 4
            jugador.movimientos_disponibles = movimientos

            for movimiento in movimientos:
                print(f"\n➡️ Movimiento automático: {movimiento}")
                print(self.tablero.mostrar_tablero_visual())

                if self.tablero.fichas_en_barra(jugador.color):
                    destino = self.calcular_destino_reingreso(jugador.color, movimiento)
                    try:
                        self.tablero.reingresar_desde_barra(jugador.color, destino)
                        print(f"{jugador.nombre} reingresó una ficha al punto {destino}")
                    except Exception as e:
                        print(f"⚠️ Error al reingresar: {e}")
                    continue

                try:
                    origen, destino = self.calcular_movimiento(jugador.color, movimiento)
                    self.tablero.mover_pieza(origen, destino)
                    print(f"{jugador.nombre} movió ficha de {origen} a {destino}")

                    if self.puede_bornear(jugador.color):
                        punto = self.tablero.mostrar_tablero()[destino]
                        if punto and punto[-1] == jugador.color:
                            try:
                                self.tablero.sacar_ficha_fuera(jugador.color, destino)
                                jugador.sacar_ficha()
                            except Exception as e:
                                print(f"⚠️ No se pudo sacar ficha: {e}")
                except Exception as e:
                    print(f"⚠️ Movimiento inválido: {e}")

            self.cambiar_turno()

        ganador = self.obtener_ganador()
        print(f"\n🏁 ¡{ganador.nombre} ha ganado la partida!")

if __name__ == "__main__":
    print("🎲 Bienvenido a Backgammon")
    print("Seleccioná el modo de juego:")
    print("1. Modo interactivo (jugás vos)")
    print("2. Modo automático (simulación completa)")

    opcion = input("Ingresá 1 o 2: ").strip()

    if opcion == "1":
        nombre1 = input("Ingresá tu nombre (jugador blanco): ").strip()
        nombre2 = input("Ingresá el nombre del rival (jugador negro): ").strip()
        juego = JuegoBackgammon(nombre1 or "Jugador 1", nombre2 or "Jugador 2")
        juego.jugar_partida_interactiva()
    elif opcion == "2":
        juego = JuegoBackgammon("Jugador 1", "Jugador 2")
        juego.simular_partida()
    else:
        print("❌ Opción inválida. Cerrando el juego.")
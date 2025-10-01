import unittest
from core.game import JuegoBackgammon
from core.board import Tablero

class TestJuegoBackgammon(unittest.TestCase):

    def setUp(self):
        self.juego = JuegoBackgammon("Ian", "Bot")

    def test_inicializacion_juego(self):
        self.assertEqual(self.juego.jugador_blanco.nombre, "Ian")
        self.assertEqual(self.juego.jugador_negro.nombre, "Bot")
        self.assertEqual(self.juego.turno_actual, self.juego.jugador_blanco)
        self.assertIsInstance(self.juego.tablero, Tablero)

    def test_lanzar_dados_valores_validos(self):
        dado1, dado2 = self.juego.lanzar_dados()
        self.assertIn(dado1, range(1, 7))
        self.assertIn(dado2, range(1, 7))

    def test_cambiar_turno(self):
        jugador_inicial = self.juego.obtener_jugador_actual()
        self.juego.cambiar_turno()
        jugador_nuevo = self.juego.obtener_jugador_actual()
        self.assertNotEqual(jugador_inicial, jugador_nuevo)

    def test_juego_terminado_false_por_defecto(self):
        self.assertFalse(self.juego.juego_terminado())

    def test_juego_terminado_true_blanco_gana(self):
        self.juego.tablero.fuera[self.juego.jugador_blanco.color] = 15
        self.assertTrue(self.juego.juego_terminado())

    def test_juego_terminado_true_negro_gana(self):
        self.juego.tablero.fuera[self.juego.jugador_negro.color] = 15
        self.assertTrue(self.juego.juego_terminado())

    def test_simular_partida_mockeada(self):
        # Forzamos condición de victoria para evitar bucle
        self.juego.tablero.fuera[self.juego.jugador_blanco.color] = 15
        self.juego.simular_partida()  # Solo debería imprimir el ganador

    def test_obtener_ganador_blanco(self):
        self.juego.tablero.fuera[self.juego.jugador_blanco.color] = 15
        ganador = self.juego.obtener_ganador()
        self.assertEqual(ganador, self.juego.jugador_blanco)

    def test_obtener_ganador_negro(self):
        self.juego.tablero.fuera[self.juego.jugador_negro.color] = 15
        ganador = self.juego.obtener_ganador()
        self.assertEqual(ganador, self.juego.jugador_negro)

    def test_obtener_ganador_none(self):
        ganador = self.juego.obtener_ganador()
        self.assertIsNone(ganador)

    def test_reiniciar_partida(self):
        self.juego.tablero.fuera[self.juego.jugador_blanco.color] = 15
        self.juego.jugador_blanco.fichas_capturadas = 5
        self.juego.jugador_blanco.fichas_salidas = 10
        self.juego.jugador_blanco.fichas_en_tablero = 0
        self.juego.turno_actual = self.juego.jugador_negro

        self.juego.reiniciar_partida()

        self.assertEqual(self.juego.jugador_blanco.fichas_capturadas, 0)
        self.assertEqual(self.juego.jugador_blanco.fichas_salidas, 0)
        self.assertEqual(self.juego.jugador_blanco.fichas_en_tablero, 15)
        self.assertEqual(self.juego.turno_actual, self.juego.jugador_blanco)
        self.assertEqual(self.juego.tablero.obtener_fuera(self.juego.jugador_blanco.color), 0)        

    def test_movimiento_basico(self):
        # Colocamos una ficha blanca en el punto 0
        self.juego.tablero.puntos[0] = 1  # 1 ficha blanca
        self.juego.jugador_blanco.movimientos_disponibles = [3]
        origen, destino = self.juego.calcular_movimiento(self.juego.jugador_blanco.color, 3)
        self.assertEqual(origen, 0)
        self.assertEqual(destino, 3)

    def test_reingreso_desde_barra(self):
        self.juego.tablero.barra[self.juego.jugador_blanco.color] = 1
        destino = self.juego.calcular_destino_reingreso(self.juego.jugador_blanco.color, 4)
        self.assertEqual(destino, 3)

    def test_puede_bornear_true(self):
        # Colocamos fichas blancas en zona de borneo
        for i in range(18, 24):
            self.juego.tablero.puntos[i] = 1
        self.assertTrue(self.juego.puede_bornear(self.juego.jugador_blanco.color))

    def test_puede_bornear_false(self):
        for i in range(18, 24):
            self.juego.tablero.puntos[i] = 0
        self.assertFalse(self.juego.puede_bornear(self.juego.jugador_blanco.color)) 

    
    def test_turno_con_dobles(self):
        # Aseguramos que haya fichas blancas en el tablero
        self.juego.tablero.puntos[0] = 1  # 1 ficha blanca en punto 0

        # Reemplazamos los métodos lanzar() de los dados por funciones que devuelven 5
        self.juego.dado1.valor = 5
        self.juego.dado2.valor = 5
        self.juego.lanzar_dados = lambda: (5, 5)

        self.juego.jugar_turno()

        movimientos = self.juego.jugador_blanco.movimientos_disponibles
        self.assertEqual(movimientos, [5, 5, 5, 5])


    def test_calcular_movimiento_blanco(self):
        self.juego.tablero.puntos[0] = 1  # ficha blanca
        origen, destino = self.juego.calcular_movimiento(Tablero.BLANCO, 3)
        self.assertEqual(origen, 0)
        self.assertEqual(destino, 3)

    def test_calcular_movimiento_negro(self):
        self.juego.tablero.puntos[23] = -1  # ficha negra
        origen, destino = self.juego.calcular_movimiento(Tablero.NEGRO, 4)
        self.assertEqual(origen, 23)
        self.assertEqual(destino, 19)

    def test_calcular_movimiento_sin_fichas(self):
        for i in range(Tablero.TOTAL_PUNTOS):
            self.juego.tablero.puntos[i] = 0
        with self.assertRaises(Exception):
            self.juego.calcular_movimiento(Tablero.BLANCO, 2)

    def test_calcular_destino_reingreso_blanco(self):
        destino = self.juego.calcular_destino_reingreso(Tablero.BLANCO, 5)
        self.assertEqual(destino, 4)

    def test_calcular_destino_reingreso_negro(self):
        destino = self.juego.calcular_destino_reingreso(Tablero.NEGRO, 2)
        self.assertEqual(destino, 22)

    def test_puede_bornear_true_blanco(self):
        self.juego.tablero.puntos[18] = 1
        self.assertTrue(self.juego.puede_bornear(Tablero.BLANCO))

    def test_puede_bornear_false_blanco(self):
        for i in range(18, 24):
            self.juego.tablero.puntos[i] = 0
        self.assertFalse(self.juego.puede_bornear(Tablero.BLANCO))

    def test_jugar_turno_valido(self):
        self.juego.tablero.puntos[0] = 1
        self.juego.dado1.valor = 2
        self.juego.dado2.valor = 3
        self.juego.lanzar_dados = lambda: (2, 3)
        self.juego.jugar_turno()
        self.assertEqual(self.juego.turno_actual, self.juego.jugador_negro)

    def test_turno_con_dobles(self):
        self.juego.tablero.puntos[0] = 1
        self.juego.dado1.valor = 5
        self.juego.dado2.valor = 5
        self.juego.lanzar_dados = lambda: (5, 5)
        self.juego.jugar_turno()
        movimientos = self.juego.jugador_blanco.movimientos_disponibles
        self.assertEqual(movimientos, [5, 5, 5, 5])


    def test_reingreso_bloqueado(self):
        self.juego.tablero.barra[Tablero.BLANCO] = 1
        self.juego.tablero.puntos[3] = -2  # bloqueado por negras
        self.juego.lanzar_dados = lambda: (4, 4)
        self.juego.jugar_turno()
        self.assertEqual(self.juego.tablero.barra[Tablero.BLANCO], 1)  # sigue en barra


    def test_borneo_automatico(self):
        self.juego.tablero.puntos[18] = 1
        self.juego.jugador_blanco.fichas_en_tablero = 1
        self.juego.lanzar_dados = lambda: (6, 6)
        self.juego.jugar_turno()
        self.assertEqual(self.juego.jugador_blanco.fichas_salidas, 1)


    def test_jugador_sin_fichas_en_tablero(self):
        self.juego.jugador_blanco.fichas_en_tablero = 0
        self.juego.lanzar_dados = lambda: (2, 3)
        self.juego.jugar_turno()
        self.assertEqual(self.juego.turno_actual, self.juego.jugador_negro)


    def test_mover_a_destino_invalido(self):
        self.juego.tablero.puntos[0] = 1
        self.juego.tablero.puntos[5] = -2  # bloqueado
        self.juego.lanzar_dados = lambda: (5, 5)
        self.juego.jugar_turno()
        self.assertEqual(self.juego.tablero.puntos[0], 1)  # no se movió


    def test_cambio_turno_tras_fallo(self):
        self.juego.tablero.puntos[0] = 1
        self.juego.tablero.puntos[5] = -2
        self.juego.lanzar_dados = lambda: (5, 5)
        turno_inicial = self.juego.turno_actual
        self.juego.jugar_turno()
        self.assertNotEqual(self.juego.turno_actual, turno_inicial)




if __name__ == "__main__":
    unittest.main()
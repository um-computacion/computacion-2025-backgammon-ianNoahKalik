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

if __name__ == "__main__":
    unittest.main()
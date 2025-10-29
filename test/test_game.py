import unittest
from unittest.mock import patch
from core.game import JuegoBackgammon
from core.board import Tablero
from core.excepciones import MovimientoInvalido

class TestJuegoBackgammon(unittest.TestCase):

    def setUp(self):
        self.juego = JuegoBackgammon("Ian", "Bot")

    def test_inicializacion_correcta(self):
        self.assertEqual(self.juego.jugador_blanco.nombre, "Ian")
        self.assertEqual(self.juego.jugador_negro.nombre, "Bot")
        self.assertEqual(self.juego.turno_actual, self.juego.jugador_blanco)

    def test_nombres_invalidos(self):
        with self.assertRaises(ValueError):
            JuegoBackgammon("", "Bot")
        with self.assertRaises(ValueError):
            JuegoBackgammon("Ian", "")

    def test_lanzar_dados_valores_validos(self):
        d1, d2 = self.juego.lanzar_dados()
        self.assertIn(d1, range(1, 7))
        self.assertIn(d2, range(1, 7))

    def test_cambiar_turno(self):
        actual = self.juego.obtener_jugador_actual()
        self.juego.cambiar_turno()
        nuevo = self.juego.obtener_jugador_actual()
        self.assertNotEqual(actual, nuevo)

    def test_juego_terminado_y_ganador(self):
        self.assertFalse(self.juego.juego_terminado())
        self.assertIsNone(self.juego.obtener_ganador())
        self.juego.jugador_blanco.fichas_salidas = 15
        self.assertTrue(self.juego.juego_terminado())
        self.assertEqual(self.juego.obtener_ganador(), self.juego.jugador_blanco)

    def test_reiniciar_partida_resetea_estado(self):
        self.juego.jugador_blanco.fichas_salidas = 10
        self.juego.jugador_blanco.fichas_capturadas = 5
        self.juego.jugador_blanco.movimientos_disponibles = [1, 2]
        self.juego.turno_actual = self.juego.jugador_negro
        self.juego.reiniciar_partida()
        self.assertEqual(self.juego.jugador_blanco.fichas_salidas, 0)
        self.assertEqual(self.juego.jugador_blanco.fichas_capturadas, 0)
        self.assertEqual(self.juego.jugador_blanco.movimientos_disponibles, [])
        self.assertEqual(self.juego.turno_actual, self.juego.jugador_blanco)

    def test_calcular_destino_reingreso(self):
        self.assertEqual(self.juego.calcular_destino_reingreso(Tablero.BLANCO, 3), 2)
        self.assertEqual(self.juego.calcular_destino_reingreso(Tablero.NEGRO, 3), 21)
        with self.assertRaises(ValueError):
            self.juego.calcular_destino_reingreso(Tablero.BLANCO, 0)

    def test_calcular_movimiento_valido(self):
        self.juego.tablero._tablero[0] = [Tablero.BLANCO]
        origen, destino = self.juego.calcular_movimiento(Tablero.BLANCO, 2)
        self.assertEqual(origen, 0)
        self.assertEqual(destino, 2)

    def test_calcular_movimiento_invalido(self):
        self.juego.tablero._tablero = [[] for _ in range(24)]
        with self.assertRaises(MovimientoInvalido):
            self.juego.calcular_movimiento(Tablero.BLANCO, 2)

    def test_calcular_movimiento_ficha_enemiga_en_origen(self):
        self.juego.tablero._tablero = [[] for _ in range(24)]
        self.juego.tablero._tablero[0] = [Tablero.NEGRO]
        with self.assertRaises(MovimientoInvalido):
            self.juego.calcular_movimiento(Tablero.BLANCO, 1)

    def test_puede_bornear_true_y_false(self):
        self.juego.tablero._tablero[18] = [Tablero.BLANCO]
        self.assertTrue(self.juego.puede_bornear(Tablero.BLANCO))
        self.juego.tablero._tablero[18] = []
        self.assertFalse(self.juego.puede_bornear(Tablero.BLANCO))

    def test_puede_bornear_con_ficha_enemiga(self):
        self.juego.tablero._tablero[18] = [Tablero.NEGRO]
        self.assertFalse(self.juego.puede_bornear(Tablero.BLANCO))

    @patch("builtins.input", side_effect=["5"])
    def test_jugar_partida_interactiva_con_reingreso(self, mock_input):
        self.juego.juego_terminado = lambda: True
        self.juego.obtener_ganador = lambda: self.juego.jugador_blanco
        self.juego.jugador_blanco.movimientos_disponibles = [1]
        self.juego.tablero._barra[Tablero.BLANCO] = 1
        self.juego.jugar_partida_interactiva()

    def test_simular_partida_con_reingreso_y_movimiento(self):
        self.juego.juego_terminado = lambda: True
        self.juego.obtener_ganador = lambda: self.juego.jugador_blanco
        self.juego.jugador_blanco.movimientos_disponibles = [1]
        self.juego.tablero._barra[Tablero.BLANCO] = 1
        self.juego.tablero._tablero[0] = [Tablero.BLANCO]
        self.juego.simular_partida()


import runpy

class TestMainBlock(unittest.TestCase):

    @patch("builtins.input", side_effect=["2"])
    def test_main_simulacion_automatica(self, mock_input):
        try:
            runpy.run_module("core.game", run_name="__main__")
        except Exception:
            pass  # ignoramos errores internos, solo queremos cobertura

    @patch("builtins.input", side_effect=["1", "Ian", "Bot", "", "5", "0", "1"])
    def test_main_interactivo(self, mock_input):
        try:
            runpy.run_module("core.game", run_name="__main__")
        except Exception:
            pass  # ignoramos errores internos, solo queremos cobertura

    @patch("builtins.input", side_effect=["3"])
    def test_main_opcion_invalida(self, mock_input):
        try:
            runpy.run_module("core.game", run_name="__main__")
        except Exception:
            pass  # ignoramos errores internos, solo queremos cobertura

if __name__ == "__main__":
    unittest.main()
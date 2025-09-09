import unittest
from unittest.mock import MagicMock
from core.player import Jugador
from core.dice import Dado

class TestJugador(unittest.TestCase):

    def setUp(self):
        self.jugador = Jugador("Ian", 0)  # Blanco

    def test_inicializacion(self):
        self.assertEqual(self.jugador.nombre, "Ian")
        self.assertEqual(self.jugador.color, 0)
        self.assertEqual(self.jugador.fichas_capturadas, 0)
        self.assertEqual(self.jugador.fichas_salidas, 0)
        self.assertEqual(self.jugador.fichas_en_tablero, 15)
        self.assertEqual(self.jugador.movimientos_disponibles, [])

    def test_capturar_ficha(self):
        self.jugador.capturar_ficha()
        self.assertEqual(self.jugador.fichas_capturadas, 1)

    def test_sacar_ficha(self):
        self.jugador.sacar_ficha()
        self.assertEqual(self.jugador.fichas_salidas, 1)
        self.assertEqual(self.jugador.fichas_en_tablero, 14)

    def test_sacar_ficha_sin_fichas(self):
        self.jugador.fichas_en_tablero = 0
        self.jugador.sacar_ficha()
        self.assertEqual(self.jugador.fichas_salidas, 0)

    def test_jugar_turno_mockeado(self):
        self.jugador.dado.lanzar = MagicMock(return_value=4)
        resultado = self.jugador.jugar_turno()
        self.assertEqual(resultado, 4)
        self.assertEqual(self.jugador.movimientos_disponibles, [4])

    def test_reiniciar_turno(self):
        self.jugador.movimientos_disponibles = [3]
        self.jugador.dado.reiniciar = MagicMock()
        self.jugador.reiniciar_turno()
        self.jugador.dado.reiniciar.assert_called_once()
        self.assertEqual(self.jugador.movimientos_disponibles, [])

    def test_str_jugador(self):
        texto = str(self.jugador)
        self.assertIn("Jugador: Ian", texto)
        self.assertIn("Color: Blanco", texto)
        self.assertIn("Capturadas: 0", texto)
        self.assertIn("Salidas: 0", texto)
        self.assertIn("En tablero: 15", texto)
import unittest
from core.player import Jugador
from core.dice import Dado

class TestJugador(unittest.TestCase):

    def setUp(self):
        self.jugador = Jugador("Ian", color=0)  # Blanco

    def test_inicializacion_correcta(self):
        self.assertEqual(self.jugador.nombre, "Ian")
        self.assertEqual(self.jugador.color, 0)
        self.assertEqual(self.jugador.fichas_capturadas, 0)
        self.assertEqual(self.jugador.fichas_salidas, 0)
        self.assertEqual(self.jugador.fichas_en_tablero, 15)
        self.assertEqual(self.jugador.movimientos_disponibles, [])
        self.assertIsInstance(self.jugador.dado, Dado)

    def test_jugar_turno_actualiza_movimientos(self):
        valor = self.jugador.jugar_turno()
        self.assertIn(valor, Dado.VALORES_VALIDOS)
        self.assertEqual(self.jugador.movimientos_disponibles, [valor])

    def test_capturar_ficha_incrementa_contador(self):
        self.jugador.capturar_ficha()
        self.assertEqual(self.jugador.fichas_capturadas, 1)

    def test_sacar_ficha_disminuye_en_tablero(self):
        self.jugador.fichas_en_tablero = 2
        self.jugador.sacar_ficha()
        self.assertEqual(self.jugador.fichas_salidas, 1)
        self.assertEqual(self.jugador.fichas_en_tablero, 1)

    def test_sacar_ficha_sin_fichas_en_tablero(self):
        self.jugador.fichas_en_tablero = 0
        self.jugador.sacar_ficha()
        self.assertEqual(self.jugador.fichas_salidas, 0)
        self.assertEqual(self.jugador.fichas_en_tablero, 0)

    def test_reiniciar_turno_vacía_movimientos_y_dado(self):
        self.jugador.jugar_turno()
        self.jugador.reiniciar_turno()
        self.assertEqual(self.jugador.movimientos_disponibles, [])
        with self.assertRaises(ValueError):
            self.jugador.dado.obtener_valor()

    def test_str_representacion_textual(self):
        texto = str(self.jugador)
        self.assertIn("Jugador: Ian", texto)
        self.assertIn("Color: Blanco", texto)
        self.assertIn("Capturadas: 0", texto)
        self.assertIn("Salidas: 0", texto)
        self.assertIn("En tablero: 15", texto)

if __name__ == "__main__":
    unittest.main()
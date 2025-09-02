import unittest
from core.dice import Dado # Ajustá el import según tu estructura

class TestDado(unittest.TestCase):

    def setUp(self):
        self.dado = Dado()

    def test_estado_inicial(self):
        self.assertIsNone(self.dado.valor)
        self.assertFalse(self.dado.lanzado)

    def test_lanzar_dado_valor_valido(self):
        valor = self.dado.lanzar()
        self.assertTrue(self.dado.lanzado)
        self.assertIn(valor, Dado.VALORES_VALIDOS)

    def test_obtener_valor_sin_lanzar(self):
        with self.assertRaises(ValueError):
            self.dado.obtener_valor()

    def test_obtener_valor_despues_de_lanzar(self):
        valor_lanzado = self.dado.lanzar()
        valor_obtenido = self.dado.obtener_valor()
        self.assertEqual(valor_lanzado, valor_obtenido)

    def test_reiniciar_dado(self):
        self.dado.lanzar()
        self.dado.reiniciar()
        self.assertIsNone(self.dado.valor)
        self.assertFalse(self.dado.lanzado)

    def test_str_sin_lanzar(self):
        self.assertEqual(str(self.dado), "[-]")

    def test_str_despues_de_lanzar(self):
        self.dado.lanzar()
        self.assertEqual(str(self.dado), f"[{self.dado.valor}]")

    def test_valores_validos_constantes(self):
        self.assertEqual(Dado.VALORES_VALIDOS, [1, 2, 3, 4, 5, 6])

if __name__ == "__main__":
    unittest.main()
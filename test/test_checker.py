import unittest
from core.checker import Ficha

class TestFicha(unittest.TestCase):

    def test_inicializacion_blanca(self):
        ficha = Ficha(1)
        self.assertEqual(ficha.color, 1)
        self.assertFalse(ficha.esta_capturada())
        self.assertTrue(ficha.es_blanca())
        self.assertFalse(ficha.es_negra())

    def test_inicializacion_negra(self):
        ficha = Ficha(-1)
        self.assertEqual(ficha.color, -1)
        self.assertFalse(ficha.esta_capturada())
        self.assertFalse(ficha.es_blanca())
        self.assertTrue(ficha.es_negra())

    def test_color_invalido_lanza_excepcion(self):
        with self.assertRaises(ValueError):
            Ficha(0)

    def test_capturar_y_liberar_ficha(self):
        ficha = Ficha(1)
        ficha.capturar()
        self.assertTrue(ficha.esta_capturada())
        ficha.liberar()
        self.assertFalse(ficha.esta_capturada())

    def test_str_ficha_blanca_activa(self):
        ficha = Ficha(1)
        self.assertEqual(str(ficha), "Ficha Blanca (Activa)")

    def test_str_ficha_negra_capturada(self):
        ficha = Ficha(-1)
        ficha.capturar()
        self.assertEqual(str(ficha), "Ficha Negra (Capturada)")

if __name__ == "__main__":
    unittest.main()
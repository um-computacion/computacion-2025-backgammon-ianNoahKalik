import unittest
from core.board import Tablero
from core.excepciones import (
    MovimientoInvalido,
    PosicionFueraDeRango,
    OrigenSinFicha,
    DestinoBloqueado,
    NoPuedeReingresar,
    NoPuedeSacarFicha
)

class TestTablero(unittest.TestCase):

    def setUp(self):
        self.tablero = Tablero()
        self.tablero.inicializar_piezas()

    def test_inicializar_piezas_estado_correcto(self):
        self.assertEqual(self.tablero._tablero[0], [Tablero.BLANCO] * 2)
        self.assertEqual(self.tablero._tablero[5], [Tablero.NEGRO] * 5)
        self.assertEqual(self.tablero._barra[Tablero.BLANCO], 0)
        self.assertEqual(self.tablero._piezas_comidas[Tablero.NEGRO], 0)

    def test_mostrar_tablero_devuelve_lista_de_24(self):
        tablero = self.tablero.mostrar_tablero()
        self.assertIsInstance(tablero, list)
        self.assertEqual(len(tablero), 24)

    def test_mostrar_tablero_visual_formato(self):
        visual = self.tablero.mostrar_tablero_visual()
        self.assertIsInstance(visual, str)
        self.assertIn("🟫 Tablero de Backgammon 🟫", visual)

    def test_fichas_en_barra(self):
        self.assertEqual(self.tablero.fichas_en_barra(Tablero.BLANCO), 0)
        self.tablero._barra[Tablero.BLANCO] = 2
        self.assertEqual(self.tablero.fichas_en_barra(Tablero.BLANCO), 2)

    def test_sacar_pieza_excepciones(self):
        with self.assertRaises(PosicionFueraDeRango):
            self.tablero.sacar_pieza(-1)
        with self.assertRaises(PosicionFueraDeRango):
            self.tablero.sacar_pieza(24)
        self.tablero._tablero[3] = []
        with self.assertRaises(OrigenSinFicha):
            self.tablero.sacar_pieza(3)

    def test_colocar_pieza_excepciones(self):
        with self.assertRaises(PosicionFueraDeRango):
            self.tablero.colocar_pieza(25, Tablero.BLANCO)

    def test_mover_pieza_valida_con_captura(self):
        self.tablero._tablero[1] = [Tablero.BLANCO]
        self.tablero._tablero[2] = [Tablero.NEGRO]
        self.tablero.mover_pieza(1, 2)
        self.assertEqual(self.tablero._tablero[2], [Tablero.BLANCO])
        self.assertEqual(self.tablero._barra[Tablero.NEGRO], 1)
        self.assertEqual(self.tablero._piezas_comidas[Tablero.NEGRO], 1)

    def test_mover_pieza_bloqueada(self):
        self.tablero._tablero[1] = [Tablero.BLANCO]
        self.tablero._tablero[2] = [Tablero.NEGRO, Tablero.NEGRO]
        with self.assertRaises(DestinoBloqueado):
            self.tablero.mover_pieza(1, 2)

    def test_validar_movimiento_excepciones(self):
        with self.assertRaises(PosicionFueraDeRango):
            self.tablero.validar_movimiento(-1, 2, Tablero.BLANCO)
        with self.assertRaises(OrigenSinFicha):
            self.tablero.validar_movimiento(3, 2, Tablero.BLANCO)
        self.tablero._tablero[4] = [Tablero.NEGRO]
        with self.assertRaises(MovimientoInvalido):
            self.tablero.validar_movimiento(4, 5, Tablero.BLANCO)

    def test_reingresar_desde_barra_excepciones(self):
        with self.assertRaises(PosicionFueraDeRango):
            self.tablero.reingresar_desde_barra(Tablero.BLANCO, 24)
        with self.assertRaises(NoPuedeReingresar):
            self.tablero.reingresar_desde_barra(Tablero.BLANCO, 5)
        self.tablero._barra[Tablero.BLANCO] = 1
        self.tablero._tablero[5] = [Tablero.NEGRO, Tablero.NEGRO]
        with self.assertRaises(DestinoBloqueado):
            self.tablero.reingresar_desde_barra(Tablero.BLANCO, 5)

    def test_reingreso_valido_con_captura(self):
        self.tablero._barra[Tablero.BLANCO] = 1
        self.tablero._tablero[5] = [Tablero.NEGRO]
        self.tablero.reingresar_desde_barra(Tablero.BLANCO, 5)
        self.assertEqual(self.tablero._tablero[5], [Tablero.BLANCO])
        self.assertEqual(self.tablero._barra[Tablero.NEGRO], 1)

    def test_puede_reingresar_true_y_false(self):
        self.tablero._barra[Tablero.BLANCO] = 1
        self.tablero._tablero[0] = []
        self.assertTrue(self.tablero.puede_reingresar(Tablero.BLANCO, [1]))
        self.tablero._tablero[0] = [Tablero.NEGRO, Tablero.NEGRO]
        self.assertFalse(self.tablero.puede_reingresar(Tablero.BLANCO, [1]))

    def test_todas_en_home_true_y_false(self):
        self.tablero._tablero = [[] for _ in range(24)]
        self.tablero._tablero[18] = [Tablero.BLANCO]
        self.assertTrue(self.tablero.todas_en_home(Tablero.BLANCO))
        self.tablero._tablero[10] = [Tablero.BLANCO]
        self.assertFalse(self.tablero.todas_en_home(Tablero.BLANCO))
        self.tablero._barra[Tablero.BLANCO] = 1
        self.assertFalse(self.tablero.todas_en_home(Tablero.BLANCO))

    def test_sacar_ficha_fuera_excepciones(self):
        with self.assertRaises(PosicionFueraDeRango):
            self.tablero.sacar_ficha_fuera(Tablero.BLANCO, -1)
        with self.assertRaises(OrigenSinFicha):
            self.tablero.sacar_ficha_fuera(Tablero.BLANCO, 3)
        self.tablero._tablero[18] = [Tablero.NEGRO]
        with self.assertRaises(MovimientoInvalido):
            self.tablero.sacar_ficha_fuera(Tablero.BLANCO, 18)
        self.tablero._tablero[10] = [Tablero.BLANCO]
        with self.assertRaises(NoPuedeSacarFicha):
            self.tablero.sacar_ficha_fuera(Tablero.BLANCO, 10)

    def test_sacar_ficha_fuera_valida(self):
        self.tablero._tablero = [[] for _ in range(24)]
        self.tablero._tablero[18] = [Tablero.BLANCO]
        self.assertTrue(self.tablero.sacar_ficha_fuera(Tablero.BLANCO, 18))
        self.assertEqual(self.tablero._tablero[18], [])

    def test_validar_movimiento_valido(self):
        self.tablero._tablero[1] = [Tablero.BLANCO]
        self.tablero._tablero[2] = []
        resultado = self.tablero.validar_movimiento(1, 2, Tablero.BLANCO)
        self.assertTrue(resultado)

    def test_reingresar_desde_barra_exito_sin_captura(self):
        self.tablero._barra[Tablero.BLANCO] = 1
        self.tablero._tablero[3] = []
        resultado = self.tablero.reingresar_desde_barra(Tablero.BLANCO, 3)
        self.assertTrue(resultado)
        self.assertEqual(self.tablero._barra[Tablero.BLANCO], 0)
        self.assertEqual(self.tablero._tablero[3], [Tablero.BLANCO])

    def test_sacar_ficha_fuera_exito(self):
        self.tablero._tablero = [[] for _ in range(24)]
        self.tablero._tablero[18] = [Tablero.BLANCO]
        self.assertTrue(self.tablero.todas_en_home(Tablero.BLANCO))
        resultado = self.tablero.sacar_ficha_fuera(Tablero.BLANCO, 18)
        self.assertTrue(resultado)
        self.assertEqual(self.tablero._tablero[18], [])

if __name__ == "__main__":
    unittest.main()
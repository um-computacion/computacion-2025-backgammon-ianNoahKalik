import unittest
from core.board import Tablero, TableroError

class TestTableroInicializacion(unittest.TestCase):
    def test_reset_inicializa_correctamente(self):
        t = Tablero()
        t.reset()
        total = sum(abs(t.obtener_punto(i)) for i in range(t.TOTAL_PUNTOS))
        self.assertEqual(total, 30)
        self.assertEqual(t.obtener_punto(0), 2)
        self.assertEqual(t.obtener_punto(23), -2)

    def test_barra_inicial_vacia(self):
        t = Tablero()
        self.assertEqual(t.barra[t.BLANCO], 0)
        self.assertEqual(t.barra[t.NEGRO], 0)

    def test_borne_off_inicializado(self):
        t = Tablero()
        self.assertEqual(t.obtener_fuera(t.BLANCO), 0)
        self.assertEqual(t.obtener_fuera(t.NEGRO), 0)

class TestTableroValidaciones(unittest.TestCase):
    def test_obtener_punto_fuera_de_rango(self):
        t = Tablero()
        with self.assertRaises(TableroError):
            t.obtener_punto(-1)
        with self.assertRaises(TableroError):
            t.obtener_punto(24)

    def test_mover_pieza_jugador_invalido(self):
        t = Tablero()
        with self.assertRaises(TableroError):
            t.mover_pieza(0, 0, 1)

    def test_mover_pieza_origen_sin_ficha_propia(self):
        t = Tablero()
        with self.assertRaises(TableroError):
            t.mover_pieza(t.BLANCO, 5, 6)

class TestTableroMovimientos(unittest.TestCase):
    def test_mover_pieza_valida_sin_captura(self):
        t = Tablero()
        t.puntos[0] = 1
        t.puntos[1] = 0
        t.mover_pieza(t.BLANCO, 0, 1)
        self.assertEqual(t.obtener_punto(0), 0)
        self.assertEqual(t.obtener_punto(1), 1)

    def test_mover_pieza_con_captura(self):
        t = Tablero()
        t.puntos[0] = 1
        t.puntos[1] = -1
        t.mover_pieza(t.BLANCO, 0, 1)
        self.assertEqual(t.obtener_punto(0), 0)
        self.assertEqual(t.obtener_punto(1), 1)
        self.assertEqual(t.barra[t.NEGRO], 1)

    def test_mover_pieza_destino_bloqueado(self):
        t = Tablero()
        t.puntos[0] = 1
        t.puntos[1] = -2
        with self.assertRaises(TableroError):
            t.mover_pieza(t.BLANCO, 0, 1)

class TestTableroReingreso(unittest.TestCase):
    def test_hay_en_barra_true_false(self):
        t = Tablero()
        t.barra[t.BLANCO] = 1
        self.assertTrue(t.hay_en_barra(t.BLANCO))
        t.barra[t.BLANCO] = 0
        self.assertFalse(t.hay_en_barra(t.BLANCO))

    def test_reingreso_valido_sin_captura(self):
        t = Tablero()
        t.barra[t.BLANCO] = 1
        t.puntos[5] = 0
        t.reingresar_desde_barra(t.BLANCO, 5)
        self.assertEqual(t.obtener_punto(5), 1)
        self.assertEqual(t.barra[t.BLANCO], 0)

    def test_reingreso_con_captura(self):
        t = Tablero()
        t.barra[t.BLANCO] = 1
        t.puntos[5] = -1
        t.reingresar_desde_barra(t.BLANCO, 5)
        self.assertEqual(t.obtener_punto(5), 1)
        self.assertEqual(t.barra[t.NEGRO], 1)

    def test_reingreso_sin_fichas_en_barra(self):
        t = Tablero()
        with self.assertRaises(TableroError):
            t.reingresar_desde_barra(t.BLANCO, 5)

    def test_reingreso_en_destino_bloqueado(self):
        t = Tablero()
        t.barra[t.BLANCO] = 1
        t.puntos[5] = -2
        with self.assertRaises(TableroError):
            t.reingresar_desde_barra(t.BLANCO, 5)

class TestTableroFuera(unittest.TestCase):
    def test_agregar_y_obtener_fuera(self):
        t = Tablero()
        t.agregar_a_fuera(t.BLANCO)
        t.agregar_a_fuera(t.BLANCO)
        self.assertEqual(t.obtener_fuera(t.BLANCO), 2)
        self.assertEqual(t.obtener_fuera(t.NEGRO), 0)

if __name__ == "_main_":
    unittest.main()









class TestTableroCoberturaExtra(unittest.TestCase):
    def test_validar_jugador_invalido_directamente(self):
        t = Tablero()
        with self.assertRaises(TableroError):
            t._validar_jugador(99)

    def test_punto_disponible_ocupacion_vacia(self):
        t = Tablero()
        t.puntos[3] = 0
        self.assertTrue(t.punto_disponible(3, t.BLANCO))

    def test_punto_disponible_ocupado_por_mismo_color(self):
        t = Tablero()
        t.puntos[4] = 2 * t.BLANCO
        self.assertTrue(t.punto_disponible(4, t.BLANCO))

    def test_punto_disponible_con_un_enemigo(self):
        t = Tablero()
        t.puntos[5] = -1
        self.assertTrue(t.punto_disponible(5, t.BLANCO))

    def test_punto_disponible_bloqueado_por_2_enemigos(self):
        t = Tablero()
        t.puntos[6] = -2
        self.assertFalse(t.punto_disponible(6, t.BLANCO))



if __name__ == "__main__":
    unittest.main()
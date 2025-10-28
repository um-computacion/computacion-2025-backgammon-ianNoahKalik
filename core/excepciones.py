# core/excepciones.py

class MovimientoInvalido(Exception): pass
class PosicionFueraDeRango(Exception): pass
class OrigenSinFicha(Exception): pass
class DestinoBloqueado(Exception): pass
class NoPuedeReingresar(Exception): pass
class NoPuedeSacarFicha(Exception): pass
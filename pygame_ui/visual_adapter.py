def adaptar_tablero(tablero):
    """
    Convierte tablero._tablero (listas de fichas) en formato visual:
    lista de 24 elementos tipo ('white'|'black', cantidad)
    """
    pos = []
    for punto in tablero.mostrar_tablero():
        if not punto:
            pos.append(None)
        else:
            color = punto[0]
            cantidad = len(punto)
            if color == "Blancas":
                color_str = 'white'
            elif color == "Negras":
                color_str = 'black'
            else:
                color_str = 'gray'  # fallback visual si hay error
            pos.append((color_str, cantidad))
    return pos
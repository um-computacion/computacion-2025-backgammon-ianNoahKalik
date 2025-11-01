import argparse
from core.game import JuegoBackgammon
# from pygame_ui.main import iniciar_interfaz  # si tenés interfaz gráfica

def main():
    parser = argparse.ArgumentParser(
        description=" Backgammon CLI - Ejecutá el juego desde consola"
    )
    parser.add_argument("--modo", choices=["interactivo", "simulado", "grafico"], default="interactivo",
                        help="Modo de juego: interactivo, simulado o grafico")
    parser.add_argument("--jugador1", default="Jugador 1", help="Nombre del jugador blanco")
    parser.add_argument("--jugador2", default="Jugador 2", help="Nombre del jugador negro")
    args = parser.parse_args()

    print(f"\n Iniciando Backgammon en modo: {args.modo.upper()}")
    print(f" Blanco: {args.jugador1} |  Negro: {args.jugador2}\n")

    juego = JuegoBackgammon(args.jugador1, args.jugador2)

    if args.modo == "interactivo":
        juego.jugar_partida_interactiva()
    elif args.modo == "simulado":
        juego.simular_partida()
    elif args.modo == "grafico":
        print(" Modo gráfico aún no implementado.")
        # iniciar_interfaz(juego)

if __name__ == "__main__":
    main()
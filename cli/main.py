import argparse
from core.game import JuegoBackgammon
# from pygame_ui.main import iniciar_interfaz  # si ya tenés pygame

def main():
    parser = argparse.ArgumentParser(description="Backgammon CLI")
    parser.add_argument("--modo", choices=["interactivo", "simulado", "grafico"], default="interactivo")
    args = parser.parse_args()

    juego = JuegoBackgammon("Ian", "Noah")

    if args.modo == "interactivo":
        juego.jugar_partida_interactiva()
    elif args.modo == "simulado":
        juego.simular_partida()
    elif args.modo == "grafico":
        print("Modo gráfico aún no implementado.")
        # iniciar_interfaz(juego)

if __name__ == "__main__":
    main()
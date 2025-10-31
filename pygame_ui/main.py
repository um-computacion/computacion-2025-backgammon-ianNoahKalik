import pygame
import sys
from core.game import JuegoBackgammon
from core.excepciones import MovimientoInvalido, DestinoBloqueado
from pygame_ui.render import render_board, hit_test, render_barra
from pygame_ui.visual_adapter import adaptar_tablero

def pantalla_inicio(screen, font):
    input_boxes = []
    clock = pygame.time.Clock()
    input_blanco = pygame.Rect(400, 250, 200, 40)
    input_negro = pygame.Rect(400, 320, 200, 40)
    color_inactive = pygame.Color('lightskyblue3')
    color_active = pygame.Color('dodgerblue2')
    active_blanco = False
    active_negro = False
    texto_blanco = ''
    texto_negro = ''
    boton_jugar = pygame.Rect(420, 400, 160, 50)
    jugando = False

    while not jugando:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if input_blanco.collidepoint(event.pos):
                    active_blanco = True
                    active_negro = False
                elif input_negro.collidepoint(event.pos):
                    active_negro = True
                    active_blanco = False
                else:
                    active_blanco = active_negro = False

                if boton_jugar.collidepoint(event.pos):
                    if texto_blanco.strip() and texto_negro.strip():
                        return texto_blanco.strip(), texto_negro.strip()

            elif event.type == pygame.KEYDOWN:
                if active_blanco:
                    if event.key == pygame.K_RETURN:
                        active_blanco = False
                    elif event.key == pygame.K_BACKSPACE:
                        texto_blanco = texto_blanco[:-1]
                    else:
                        texto_blanco += event.unicode
                elif active_negro:
                    if event.key == pygame.K_RETURN:
                        active_negro = False
                    elif event.key == pygame.K_BACKSPACE:
                        texto_negro = texto_negro[:-1]
                    else:
                        texto_negro += event.unicode

        screen.fill((240, 230, 210))
        titulo = font.render("Backgammon", True, (20, 20, 20))
        screen.blit(titulo, (420, 100))

        pygame.draw.rect(screen, color_active if active_blanco else color_inactive, input_blanco, 2)
        pygame.draw.rect(screen, color_active if active_negro else color_inactive, input_negro, 2)

        txt1 = font.render("Jugador Blanco:", True, (20, 20, 20))
        txt2 = font.render("Jugador Negro:", True, (20, 20, 20))
        screen.blit(txt1, (280, 260))
        screen.blit(txt2, (280, 330))

        nombre1 = font.render(texto_blanco, True, (20, 20, 20))
        nombre2 = font.render(texto_negro, True, (20, 20, 20))
        screen.blit(nombre1, (input_blanco.x + 5, input_blanco.y + 8))
        screen.blit(nombre2, (input_negro.x + 5, input_negro.y + 8))

        pygame.draw.rect(screen, (100, 180, 100), boton_jugar)
        jugar_txt = font.render("Comenzar partida", True, (255, 255, 255))
        screen.blit(jugar_txt, (boton_jugar.x + 10, boton_jugar.y + 15))

        pygame.display.flip()
        clock.tick(30)

def main():
    pygame.init()
    pygame.display.set_caption("Backgammon")
    screen = pygame.display.set_mode((1000, 700))
    font = pygame.font.SysFont(None, 24)

    nombre1, nombre2 = pantalla_inicio(screen, font)

    # Acá continúa tu loop principal del juego como ya lo tenías
    # Reutilizá el main que ya tenés desde este punto en adelante
    # Usá nombre1 y nombre2 como jugadores

    # Por ejemplo:
    from pygame_ui.main_juego import ejecutar_juego
    ejecutar_juego(screen, font, nombre1, nombre2)

if __name__ == "__main__":
    main()
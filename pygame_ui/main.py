import pygame
import sys
from pygame_ui.main_juego import ejecutar_juego

def pantalla_inicio(screen, font_titulo, font_texto):
    clock = pygame.time.Clock()

    input_blanco = pygame.Rect(480, 250, 200, 40)
    input_negro = pygame.Rect(480, 320, 200, 40)

    color_inactive = pygame.Color('saddlebrown')
    color_active = pygame.Color('peru')
    active_blanco = False
    active_negro = False
    texto_blanco = ''
    texto_negro = ''
    boton_jugar = pygame.Rect(420, 400, 160, 50)
    mensaje_error = ""

    while True:
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
                        print(f"[Inicio] Jugador Blanco: {texto_blanco.strip()} | Jugador Negro: {texto_negro.strip()}")
                        return texto_blanco.strip(), texto_negro.strip()
                    else:
                        mensaje_error = "⚠️ Completá ambos nombres antes de comenzar"

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

        screen.fill((230, 220, 200))  # Marrón claro

        # Título grande centrado
        titulo = font_titulo.render("Backgammon", True, (60, 40, 20))
        rect_titulo = titulo.get_rect(center=(500, 100))
        screen.blit(titulo, rect_titulo)

        # Etiquetas alineadas con campos
        txt1 = font_texto.render("Jugador Blanco:", True, (20, 20, 20))
        txt2 = font_texto.render("Jugador Negro:", True, (20, 20, 20))
        screen.blit(txt1, (280, input_blanco.y + 8))
        screen.blit(txt2, (280, input_negro.y + 8))

        # Campos de texto
        pygame.draw.rect(screen, color_active if active_blanco else color_inactive, input_blanco, 2)
        pygame.draw.rect(screen, color_active if active_negro else color_inactive, input_negro, 2)

        nombre1 = font_texto.render(texto_blanco, True, (20, 20, 20))
        nombre2 = font_texto.render(texto_negro, True, (20, 20, 20))
        screen.blit(nombre1, (input_blanco.x + 5, input_blanco.y + 8))
        screen.blit(nombre2, (input_negro.x + 5, input_negro.y + 8))

        # Botón jugar
        pygame.draw.rect(screen, (100, 180, 100), boton_jugar)
        jugar_txt = font_texto.render("Comenzar partida", True, (255, 255, 255))
        screen.blit(jugar_txt, (boton_jugar.x + 10, boton_jugar.y + 15))

        # Mensaje de error si falta algún nombre
        if mensaje_error:
            error_txt = font_texto.render(mensaje_error, True, (200, 0, 0))
            screen.blit(error_txt, (360, 470))

        pygame.display.flip()
        clock.tick(30)

def main():
    pygame.init()
    pygame.display.set_caption("Backgammon")
    screen = pygame.display.set_mode((1000, 700))
    font_titulo = pygame.font.SysFont(None, 140)
    font_texto = pygame.font.SysFont(None, 24)

    nombre1, nombre2 = pantalla_inicio(screen, font_titulo, font_texto)
    ejecutar_juego(screen, font_texto, nombre1, nombre2)

if __name__ == "__main__":
    main()
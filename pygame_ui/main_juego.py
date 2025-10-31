import pygame
import sys
from core.game import JuegoBackgammon
from core.excepciones import MovimientoInvalido, DestinoBloqueado
from pygame_ui.render import render_board, hit_test, render_barra
from pygame_ui.visual_adapter import adaptar_tablero

def ejecutar_juego(screen, font, nombre1, nombre2):
    clock = pygame.time.Clock()

    juego = JuegoBackgammon(nombre1, nombre2)

    hitmap = {}
    seleccionado = None
    dados = []
    dados_lanzados = False
    mensaje = ""
    mostrar_bloqueo = False

    running = True
    while running:
        for e in pygame.event.get():
            if e.type == pygame.QUIT or (e.type == pygame.KEYDOWN and e.key in (pygame.K_ESCAPE, pygame.K_q)):
                running = False

            elif e.type == pygame.KEYDOWN and e.key == pygame.K_SPACE:
                if not dados_lanzados:
                    dados = list(juego.lanzar_dados())
                    juego.obtener_jugador_actual().movimientos_disponibles = dados.copy()
                    mensaje = f"{juego.obtener_jugador_actual().nombre} lanzó: {dados}"
                    dados_lanzados = True
                else:
                    mensaje = "Ya lanzaste los dados este turno"

            elif e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                idx = hit_test(hitmap, e.pos)
                if idx is not None:
                    jugador = juego.obtener_jugador_actual()
                    color = jugador.color

                    if seleccionado is None:
                        punto = juego.tablero.mostrar_tablero()[idx]
                        if punto and punto[0] == color:
                            seleccionado = idx
                            mensaje = f"Origen seleccionado: {idx}"
                        else:
                            mensaje = "Solo podés mover tus propias fichas"
                    else:
                        distancia = abs(seleccionado - idx)
                        sentido_valido = (
                            color == "Blancas" and idx < seleccionado or
                            color == "Negras" and idx > seleccionado
                        )

                        if sentido_valido:
                            if distancia in jugador.movimientos_disponibles:
                                try:
                                    juego.tablero.mover_pieza(seleccionado, idx)
                                    jugador.movimientos_disponibles.remove(distancia)
                                    mensaje = f"Movimiento: {seleccionado} → {idx} (usó {distancia})"

                                    if juego.tablero.todas_en_home(color):
                                        restantes = sum(
                                            len(p) for p in juego.tablero.mostrar_tablero()
                                            if p and p[0] == color
                                        )
                                        if restantes == 0:
                                            mensaje = f"🎉 {jugador.nombre} ha ganado la partida 🎉"
                                            running = False

                                    if not jugador.movimientos_disponibles:
                                        juego.cambiar_turno()
                                        dados_lanzados = False

                                    seleccionado = None
                                except (MovimientoInvalido, DestinoBloqueado) as err:
                                    mensaje = f"Movimiento inválido: {err}"
                                    seleccionado = None
                            else:
                                mensaje = f"Distancia {distancia} no está en los dados disponibles: {jugador.movimientos_disponibles}"
                                seleccionado = None
                        else:
                            mensaje = "Sentido de movimiento inválido para tu color"
                            seleccionado = None

        jugador = juego.obtener_jugador_actual()
        color = jugador.color
        mostrar_bloqueo = False
        if dados_lanzados and jugador.movimientos_disponibles and juego.tablero.fichas_en_barra(color) > 0:
            posibles = [dado - 1 if color == "Blancas" else 24 - dado for dado in jugador.movimientos_disponibles]
            reingresado = False
            for pos in posibles:
                try:
                    juego.tablero.reingresar_desde_barra(color, pos)
                    jugador.movimientos_disponibles.remove(24 - pos if color == "Negras" else pos + 1)
                    mensaje = f"Reingresó ficha en {pos}"
                    reingresado = True
                    break
                except:
                    continue
            if not reingresado:
                mensaje = "No puede reingresar ninguna ficha. Turno salteado."
                juego.cambiar_turno()
                dados_lanzados = False
                seleccionado = None
                mostrar_bloqueo = True

        juego_visual = type("VisualGame", (), {})()
        juego_visual.board = type("VisualBoard", (), {})()
        juego_visual.board.pos = adaptar_tablero(juego.tablero)

        hitmap = render_board(screen, juego_visual, font)

        if seleccionado is not None:
            if seleccionado in hitmap and hitmap[seleccionado]:
                cx, cy, r = hitmap[seleccionado][0]
                pygame.draw.circle(screen, (200, 0, 0), (cx, cy), r + 4, 2)

        turno = juego.obtener_jugador_actual().nombre
        txt_turno = font.render(f"Turno: {turno}", True, (20, 20, 20))
        txt_msg = font.render(mensaje, True, (20, 20, 20))
        txt_dados = font.render(f"Dados: {jugador.movimientos_disponibles}", True, (20, 20, 20))
        screen.blit(txt_turno, (40, 10))
        screen.blit(txt_msg, (200, 10))
        screen.blit(txt_dados, (40, 30))

        barra_blancas = juego.tablero.fichas_en_barra("Blancas")
        barra_negras = juego.tablero.fichas_en_barra("Negras")
        comidas = juego.tablero.piezas_comidas()
        fuera_blancas = juego.tablero.fichas_fuera("Blancas")
        fuera_negras = juego.tablero.fichas_fuera("Negras")

        txt_barra = font.render(f"Barra ⚪: {barra_blancas}   ⚫: {barra_negras}", True, (20, 20, 20))
        txt_comidas = font.render(f"Comidas ⚪: {comidas['Blancas']}   ⚫: {comidas['Negras']}", True, (20, 20, 20))
        txt_fuera = font.render(f"Fuera ⚪: {fuera_blancas}   ⚫: {fuera_negras}", True, (20, 20, 20))
        screen.blit(txt_barra, (40, 50))
        screen.blit(txt_comidas, (40, 70))
        screen.blit(txt_fuera, (40, 90))

        render_barra(screen, font, barra_blancas, barra_negras)

        if mostrar_bloqueo:
            txt_bloqueo = font.render("⛔ Debés reingresar antes de mover otras fichas", True, (200, 0, 0))
            screen.blit(txt_bloqueo, (40, 110))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()
import pygame
import sys
from core.game import JuegoBackgammon
from core.excepciones import MovimientoInvalido, DestinoBloqueado
from pygame_ui.render import (
    render_board, hit_test, render_barra,
    render_fuera, render_dados
)

class VisualBoard:
    def __init__(self, tablero):
        self.pos = tablero.mostrar_tablero()

class VisualGame:
    def __init__(self, tablero):
        self.board = VisualBoard(tablero)

def ejecutar_juego(screen, font, nombre1, nombre2):
    clock = pygame.time.Clock()
    juego = JuegoBackgammon(nombre1, nombre2)

    hitmap = {}
    seleccionado = None
    dados = []
    dados_lanzados = False
    mensaje = ""
    mostrar_bloqueo = False
    destinos_validos = []

    print(f"[Inicio partida] Jugador Blanco: {nombre1} | Jugador Negro: {nombre2}")

    running = True
    while running:
        for e in pygame.event.get():
            if e.type == pygame.QUIT or (e.type == pygame.KEYDOWN and e.key in (pygame.K_ESCAPE, pygame.K_q)):
                running = False

            elif e.type == pygame.KEYDOWN and e.key == pygame.K_SPACE:
                if not dados_lanzados:
                    dados = list(juego.lanzar_dados())
                    jugador = juego.obtener_jugador_actual()
                    jugador.movimientos_disponibles = dados.copy()
                    mensaje = f"{jugador.nombre} lanzó: {dados}"
                    dados_lanzados = True
                    print(f"[Dados] {jugador.nombre} lanzó: {dados}")
                else:
                    mensaje = "Ya lanzaste los dados este turno"

            elif e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                idx = hit_test(hitmap, e.pos)
                if idx is not None:
                    jugador = juego.obtener_jugador_actual()

                    if seleccionado is None:
                        punto = juego.tablero.mostrar_tablero()[idx]
                        if punto and punto[-1].color == jugador.color_numerico:
                            seleccionado = idx
                            mensaje = f"Origen seleccionado: {idx}"
                            destinos_validos = []
                            for dado in jugador.movimientos_disponibles:
                                destino = idx - dado if jugador.color_numerico == 1 else idx + dado
                                if 0 <= destino < 24:
                                    destinos_validos.append(destino)
                        else:
                            mensaje = "Solo podés mover tus propias fichas"
                    else:
                        distancia = abs(seleccionado - idx)
                        sentido_valido = (
                            jugador.color_numerico == 1 and idx < seleccionado or
                            jugador.color_numerico == -1 and idx > seleccionado
                        )

                        if sentido_valido:
                            if distancia in jugador.movimientos_disponibles:
                                try:
                                    juego.tablero.mover_pieza(seleccionado, idx)
                                    jugador.movimientos_disponibles.remove(distancia)
                                    mensaje = f"Movimiento: {seleccionado} → {idx} (usó {distancia})"
                                    print(f"[Movimiento] {jugador.nombre} movió de {seleccionado} a {idx} usando {distancia}")

                                    if juego.tablero.todas_en_home(jugador.color):
                                        restantes = sum(
                                            len(p) for p in juego.tablero.mostrar_tablero()
                                            if p and ((jugador.color_numerico == 1 and p[-1].es_blanca()) or
                                                      (jugador.color_numerico == -1 and p[-1].es_negra()))
                                        )
                                        if restantes == 0:
                                            mensaje = f"🎉 {jugador.nombre} ha ganado la partida 🎉"
                                            print(f"[Victoria] {jugador.nombre} ha ganado la partida")
                                            running = False

                                    if not jugador.movimientos_disponibles:
                                        juego.cambiar_turno()
                                        dados_lanzados = False

                                    seleccionado = None
                                    destinos_validos = []
                                except (MovimientoInvalido, DestinoBloqueado) as err:
                                    mensaje = f"Movimiento inválido: {err}"
                                    print(f"[Error] Movimiento inválido: {err}")
                                    seleccionado = None
                                    destinos_validos = []
                            else:
                                mensaje = f"Distancia {distancia} no está en los dados disponibles: {jugador.movimientos_disponibles}"
                                print(f"[Error] Distancia inválida: {distancia}")
                                seleccionado = None
                                destinos_validos = []
                        else:
                            mensaje = "Sentido de movimiento inválido para tu color"
                            print(f"[Error] Sentido inválido para {jugador.nombre}")
                            seleccionado = None
                            destinos_validos = []

        jugador = juego.obtener_jugador_actual()
        mostrar_bloqueo = False
        if dados_lanzados and jugador.movimientos_disponibles and juego.tablero.fichas_en_barra(jugador.color) > 0:
            posibles = [dado - 1 if jugador.color_numerico == 1 else 24 - dado for dado in jugador.movimientos_disponibles]
            reingresado = False
            for pos in posibles:
                try:
                    juego.tablero.reingresar_desde_barra(jugador.color, pos)
                    jugador.movimientos_disponibles.remove(24 - pos if jugador.color_numerico == -1 else pos + 1)
                    mensaje = f"Reingresó ficha en {pos}"
                    print(f"[Reingreso] {jugador.nombre} reingresó ficha en {pos}")
                    reingresado = True
                    break
                except:
                    continue
            if not reingresado:
                mensaje = "No puede reingresar ninguna ficha. Turno salteado."
                print(f"[Bloqueo] {jugador.nombre} no pudo reingresar ninguna ficha")
                juego.cambiar_turno()
                dados_lanzados = False
                seleccionado = None
                destinos_validos = []
                mostrar_bloqueo = True

        hitmap = render_board(screen, VisualGame(juego.tablero), font, destinos_validos)

        if seleccionado is not None:
            if seleccionado in hitmap and hitmap[seleccionado]:
                cx, cy, r = hitmap[seleccionado][0]
                pygame.draw.circle(screen, (200, 0, 0), (cx, cy), r + 4, 2)

        txt_turno = font.render(f"Turno: {jugador.nombre}", True, (20, 20, 20))
        txt_msg = font.render(mensaje, True, (20, 20, 20))
        screen.blit(txt_turno, (40, 10))
        screen.blit(txt_msg, (200, 10))

        render_dados(screen, font, jugador.movimientos_disponibles)
        render_barra(screen, font, juego.tablero._barra["Blancas"], juego.tablero._barra["Negras"])
        render_fuera(screen, font, juego.tablero.fichas_fuera("Blancas"), juego.tablero.fichas_fuera("Negras"))

        if mostrar_bloqueo:
            txt_bloqueo = font.render("⛔ Debés reingresar antes de mover otras fichas", True, (200, 0, 0))
            screen.blit(txt_bloqueo, (40, 110))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()
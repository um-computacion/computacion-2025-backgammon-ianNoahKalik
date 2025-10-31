import pygame

# ------------------ Config visual ------------------
WIDTH, HEIGHT = 1000, 700
MARGIN_X, MARGIN_Y = 40, 40
BG_COLOR = (230, 220, 200)  # Marrón claro
BOARD_COLOR = (210, 200, 180)
TRI_A = (170, 120, 90)
TRI_B = (210, 170, 130)
LINE = (60, 60, 60)
WHITE = (245, 245, 245)
BLACK = (30, 30, 30)
TEXT = (25, 25, 25)
HIGHLIGHT = (0, 180, 0)

MAX_VISIBLE_STACK = 5

def point_index_to_display(idx):
    if 0 <= idx <= 11:
        return 'top', 11 - idx
    else:
        return 'bottom', idx - 12

def draw_triangle(surface, board_rect, col_vis, row, color):
    x0 = board_rect.left + col_vis * (board_rect.width / 12.0)
    x1 = x0 + (board_rect.width / 12.0)
    x_mid = (x0 + x1) / 2.0

    if row == 'top':
        tip_y = board_rect.top + board_rect.height * 0.42
        pts = [(x0, board_rect.top), (x1, board_rect.top), (x_mid, tip_y)]
    else:
        tip_y = board_rect.bottom - board_rect.height * 0.42
        pts = [(x0, board_rect.bottom), (x1, board_rect.bottom), (x_mid, tip_y)]
    pygame.draw.polygon(surface, color, pts)

def draw_checker(surface, center, radius, color_rgb, label=None, font=None):
    pygame.draw.circle(surface, color_rgb, center, radius)
    pygame.draw.circle(surface, LINE, center, radius, 1)
    if label and font:
        txt = font.render(str(label), True, LINE if color_rgb == WHITE else WHITE)
        rect = txt.get_rect(center=center)
        surface.blit(txt, rect)

def render_board(surface, game, font, destinos_validos=None):
    surface.fill(BG_COLOR)

    board_rect = pygame.Rect(
        MARGIN_X,
        MARGIN_Y + 20,
        WIDTH - 2 * MARGIN_X - 120,  # espacio para columnas laterales
        HEIGHT - 2 * MARGIN_Y - 40
    )
    pygame.draw.rect(surface, BOARD_COLOR, board_rect, border_radius=12)
    pygame.draw.rect(surface, LINE, board_rect, 2, border_radius=12)

    for col_vis in range(12):
        draw_triangle(surface, board_rect, col_vis, 'top', TRI_A if col_vis % 2 == 0 else TRI_B)
        draw_triangle(surface, board_rect, col_vis, 'bottom', TRI_B if col_vis % 2 == 0 else TRI_A)

    tri_w = board_rect.width / 12.0
    radius = int(tri_w * 0.38)
    radius = max(12, min(radius, 22))
    vgap = 4
    step = radius * 2 + vgap

    hitmap = {i: [] for i in range(24)}

    for idx in range(24):
        cell = game.board.pos[idx]
        row, col_vis = point_index_to_display(idx)
        cx = int(board_rect.left + col_vis * tri_w + tri_w / 2)

        if row == 'top':
            cy = int(board_rect.top + radius + 6)
        else:
            cy = int(board_rect.bottom - radius - 6)

        if destinos_validos and idx in destinos_validos:
            pygame.draw.circle(surface, HIGHLIGHT, (cx, cy), radius + 4, 2)

        if not cell:
            hitmap[idx].append((cx, cy, radius))
            continue

        visibles = min(len(cell), MAX_VISIBLE_STACK)
        extras = max(0, len(cell) - (MAX_VISIBLE_STACK - 1)) if len(cell) > MAX_VISIBLE_STACK else 0

        for i in range(visibles):
            cy_offset = i * step if row == 'top' else -i * step
            cy_i = cy + cy_offset
            label = extras if (extras and i == visibles - 1) else None
            ficha = cell[i]
            color_rgb = WHITE if ficha.es_blanca() else BLACK
            draw_checker(surface, (cx, cy_i), radius, color_rgb, label, font)
            hitmap[idx].append((cx, cy_i, radius))

    return hitmap

def hit_test(hitmap, pos):
    mx, my = pos
    for idx, circles in hitmap.items():
        for (cx, cy, r) in circles:
            dx, dy = mx - cx, my - cy
            if dx*dx + dy*dy <= r*r:
                return idx
    return None

def render_barra(surface, font, barra_blancas, barra_negras):
    x_base = WIDTH - 100
    y_base = 120
    radius = 14
    vgap = 6

    for i, ficha in enumerate(barra_blancas):
        cy = y_base + i * (radius * 2 + vgap)
        color = WHITE if ficha.es_blanca() else BLACK
        pygame.draw.circle(surface, color, (x_base, cy), radius)
        pygame.draw.circle(surface, LINE, (x_base, cy), radius, 1)

    for i, ficha in enumerate(barra_negras):
        cy = y_base + i * (radius * 2 + vgap)
        color = WHITE if ficha.es_blanca() else BLACK
        pygame.draw.circle(surface, color, (x_base + 40, cy), radius)
        pygame.draw.circle(surface, LINE, (x_base + 40, cy), radius, 1)

    txt = font.render("Barra ⚪⚫", True, TEXT)
    surface.blit(txt, (x_base, y_base - 24))

def render_fuera(surface, font, fuera_blancas, fuera_negras):
    x_base = WIDTH - 100
    y_base = 500
    radius = 14
    vgap = 6

    for i, ficha in enumerate(fuera_blancas):
        cy = y_base + i * (radius * 2 + vgap)
        color = WHITE if ficha.es_blanca() else BLACK
        pygame.draw.circle(surface, color, (x_base, cy), radius)
        pygame.draw.circle(surface, LINE, (x_base, cy), radius, 1)

    for i, ficha in enumerate(fuera_negras):
        cy = y_base + i * (radius * 2 + vgap)
        color = WHITE if ficha.es_blanca() else BLACK
        pygame.draw.circle(surface, color, (x_base + 40, cy), radius)
        pygame.draw.circle(surface, LINE, (x_base + 40, cy), radius, 1)

    txt = font.render("Fuera ⚪⚫", True, TEXT)
    surface.blit(txt, (x_base, y_base - 24))

def render_dados(surface, font, dados):
    x_base = WIDTH - 100
    y_base = 40
    radius = 18
    for i, valor in enumerate(dados):
        cx = x_base + i * 40
        pygame.draw.circle(surface, (200, 200, 200), (cx, y_base), radius)
        pygame.draw.circle(surface, LINE, (cx, y_base), radius, 2)
        txt = font.render(str(valor), True, LINE)
        rect = txt.get_rect(center=(cx, y_base))
        surface.blit(txt, rect)
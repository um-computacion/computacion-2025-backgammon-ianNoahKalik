import pygame

# ------------------ Config visual ------------------
WIDTH, HEIGHT = 1000, 700
MARGIN_X, MARGIN_Y = 40, 40
BG_COLOR = (245, 239, 230)
BOARD_COLOR = (230, 220, 200)
TRI_A = (170, 120, 90)
TRI_B = (210, 170, 130)
LINE = (60, 60, 60)
WHITE = (245, 245, 245)
BLACK = (30, 30, 30)
TEXT = (25, 25, 25)

MAX_VISIBLE_STACK = 5

def point_index_to_display(idx):
    if 0 <= idx <= 11:
        return 'top', 11 - idx  # puntos 0–11 van arriba
    else:
        return 'bottom', idx - 12  # puntos 12–23 van abajo

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

def render_board(surface, game, font):
    surface.fill(BG_COLOR)

    board_rect = pygame.Rect(
        MARGIN_X,
        MARGIN_Y + 20,
        WIDTH - 2 * MARGIN_X,
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

    top_labels = [str(i) for i in range(12, 0, -1)]
    for col_vis, lbl in enumerate(top_labels):
        x = int(board_rect.left + col_vis * tri_w + tri_w / 2)
        y = board_rect.top - 14
        img = font.render(lbl, True, TEXT)
        rect = img.get_rect(center=(x, y))
        surface.blit(img, rect)

    bottom_labels = [str(i) for i in range(13, 25)]
    for col_vis, lbl in enumerate(bottom_labels):
        x = int(board_rect.left + col_vis * tri_w + tri_w / 2)
        y = board_rect.bottom + 14
        img = font.render(lbl, True, TEXT)
        rect = img.get_rect(center=(x, y))
        surface.blit(img, rect)

    pygame.draw.line(surface, LINE, (board_rect.left, board_rect.centery),
                     (board_rect.right, board_rect.centery), 1)

    hitmap = {i: [] for i in range(24)}

    for idx in range(24):
        cell = game.board.pos[idx]
        row, col_vis = point_index_to_display(idx)
        cx = int(board_rect.left + col_vis * tri_w + tri_w / 2)

        if row == 'top':
            cy = int(board_rect.top + radius + 6)
        else:
            cy = int(board_rect.bottom - radius - 6)

        if not cell:
            hitmap[idx].append((cx, cy, radius))
            continue

        color_name, count = cell
        visibles = min(count, MAX_VISIBLE_STACK)
        extras = max(0, count - (MAX_VISIBLE_STACK - 1)) if count > MAX_VISIBLE_STACK else 0

        for i in range(visibles):
            cy_offset = i * step if row == 'top' else -i * step
            cy_i = cy + cy_offset
            label = extras if (extras and i == visibles - 1) else None
            draw_checker(surface, (cx, cy_i), radius, BLACK if color_name == 'white' else WHITE, label, font)
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
    x_base = 860
    y_base = 120
    radius = 14
    vgap = 6

    for i in range(barra_blancas):
        cy = y_base + i * (radius * 2 + vgap)
        pygame.draw.circle(surface, (245, 245, 245), (x_base, cy), radius)
        pygame.draw.circle(surface, (60, 60, 60), (x_base, cy), radius, 1)

    for i in range(barra_negras):
        cy = y_base + i * (radius * 2 + vgap)
        pygame.draw.circle(surface, (30, 30, 30), (x_base + 40, cy), radius)
        pygame.draw.circle(surface, (60, 60, 60), (x_base + 40, cy), radius, 1)

    txt = font.render("Barra ⚪⚫", True, (20, 20, 20))
    surface.blit(txt, (x_base, y_base - 24))
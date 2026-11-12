import random, math, json
from PIL import Image
from pxl import *
from facade import CAL, STONE, BRICK, IRON, MOSS, TELHA, GLASS

VW, VH = 480, 270
VM, DM = 24, 16                    # vertical 24 px/m ; profundidade do piso 16 px/m (3/4 oblíquo)
X0, X1 = 72, 408                   # paredes internas (14 m)
CAP, YT, YB, YF = 28, 36, 132, 236 # topo do corte, topo da parede, base da parede de fundo, borda da frente (6,5 m)
def fy(d): return YB + int(round(d * DM))

WOOD  = ramp(165, 0.20, (0.13, 0.21, 0.31, 0.41, 0.52))     # esquadrias verde-musgo
TIMB  = ramp(28, 0.38, (0.14, 0.22, 0.32, 0.42, 0.54))       # madeira escura
BARRA = ramp(168, 0.22, (0.22, 0.30, 0.40, 0.50, 0.60))
FLOOR = ramp(22, 0.27, (0.31, 0.37, 0.43, 0.49, 0.56))
LEAF  = ramp(120, 0.38, (0.16, 0.24, 0.33, 0.43, 0.55))
STRAW = ramp(40, 0.45, (0.30, 0.42, 0.54, 0.66, 0.78))
BREAD = ramp(32, 0.55, (0.28, 0.40, 0.52, 0.64, 0.76))
CLAY  = ramp(18, 0.48, (0.26, 0.36, 0.46, 0.56, 0.66))
RED   = ramp(4, 0.42, (0.30, 0.40, 0.50, 0.60, 0.70))
FILT  = ramp(15, 0.52, (0.17, 0.26, 0.35, 0.45, 0.56))
SACK  = ramp(44, 0.18, (0.60, 0.70, 0.80, 0.88, 0.94))
VOID  = (22, 16, 19)

# ---------------------------------------------------------------- utilidades
def arch_mask(x, w, y_floor, h):
    r = w / 2.0; cx = x + r; spring = y_floor - h + r
    def m(px, py):
        if px < x or px >= x + w or py >= y_floor: return False
        if py >= spring: return True
        dx = px + 0.5 - cx
        return dx * dx + (py + 0.5 - spring) ** 2 <= r * r
    return m
def fill_mask(c, mask, bbox, col):
    x0, y0, x1, y1 = bbox
    for y in range(y0, y1):
        for x in range(x0, x1):
            if mask(x, y): c.pset(x, y, col(x, y) if callable(col) else col)
def ell(c, cx, cy, rx, ry, col):
    for y in range(int(cy - ry) - 1, int(cy + ry) + 2):
        for x in range(int(cx - rx) - 1, int(cx + rx) + 2):
            if ((x + .5 - cx) / rx) ** 2 + ((y + .5 - cy) / ry) ** 2 <= 1: c.pset(x, y, col)
def SKY_V(y, h):
    cols = [(150, 190, 218), (176, 206, 224), (206, 222, 224), (232, 230, 212)]
    return cols[min(3, int(y / float(h) * 4))]

TINY = {
 'F': ["###", "#..", "##.", "#..", "#.."], 'I': ["###", ".#.", ".#.", ".#.", "###"], 'A': [".#.", "#.#", "###", "#.#", "#.#"],
 'D': ["##.", "#.#", "#.#", "#.#", "##."], 'O': [".#.", "#.#", "#.#", "#.#", ".#."], 'T': ["###", ".#.", ".#.", ".#.", ".#."],
 'E': ["###", "#..", "##.", "#..", "###"], 'S': [".##", "#..", ".#.", "..#", "##."], 'X': ["#.#", "#.#", ".#.", "#.#", "#.#"],
 'R': ["##.", "#.#", "##.", "#.#", "#.#"], ' ': ["..", "..", "..", "..", ".."],
}
def tiny(c, x, y, s, col):
    for ch in s:
        if ch == 'É':
            g = TINY['E']; c.pset(x + 1, y - 2, col)
        else: g = TINY[ch]
        for j, row in enumerate(g):
            for i, v in enumerate(row):
                if v == '#': c.pset(x + i, y + j, col)
        x += len(g[0]) + 1

# ---------------------------------------------------------------- base: arquitetura + móveis encostados na parede
def build_base(seed=5):
    rng = random.Random(seed)
    c = C(VW, VH, VOID + (255,))
    # piso: ladrilho 0,5 m = 12x8 px
    for ty in range((YF - YB) // 8 + 1):
        for tx in range((X1 - X0) // 12):
            col = rng.choice([FLOOR[2]] * 5 + [FLOOR[3]] * 3 + [mix(FLOOR[2], FLOOR[1], 0.5)] * 2)
            x, y = X0 + tx * 12, YB + ty * 8
            c.rect(x, y, 12, 8, col)
            c.hline(x, y, 12, mix(col, (255, 230, 190), 0.07)); c.vline(x, y, 8, mix(col, (255, 230, 190), 0.05))
            c.hline(x, y + 7, 12, mix(col, (30, 20, 40), 0.20)); c.vline(x + 11, y, 8, mix(col, (30, 20, 40), 0.14))
    c.rect(X0, YF, X1 - X0, 12, VOID + (255,))
    # trilho de uso: porta -> balcão (tom um pouco mais claro)
    for ty in range(((YF - 60) - YB) // 8, (YF - YB) // 8):
        for tx in range(13, 18):
            x, y = X0 + tx * 12, YB + ty * 8
            for yy in range(y, y + 8):
                for xx in range(x, x + 12):
                    r, g, b, a = c.get(xx, yy)
                    if yy < YF: c.pset(xx, yy, mix((r, g, b), (236, 200, 160), 0.09))
    c.shade(X0, YB, 7, YF - YB, SH1); c.shade(X1 - 7, YB, 7, YF - YB, SH1)
    c.shade(X0, YB, 3, YF - YB, SH2); c.shade(X1 - 3, YB, 3, YF - YB, SH2)
    c.shade(X0, YB, X1 - X0, 2, SH3); c.shade(X0, YB + 2, X1 - X0, 3, SH2); c.shade(X0, YB + 5, X1 - X0, 3, SH1)
    # parede de fundo
    c.rect(X0, YT, X1 - X0, YB - YT, CAL[3])
    c.rect(X0, YT, X1 - X0, 8, CAL[2]); c.shade(X0, YT + 8, X1 - X0, 6, SH1)
    by = YB - 31
    c.rect(X0, by, X1 - X0, 31, BARRA[2]); c.hline(X0, by, X1 - X0, BARRA[4]); c.hline(X0, by + 1, X1 - X0, BARRA[3]); c.hline(X0, by + 2, X1 - X0, BARRA[1]); c.hline(X0, by - 1, X1 - X0, CAL[1])
    c.rect(X0, YB - 6, X1 - X0, 6, STONE[2]); c.hline(X0, YB - 6, X1 - X0, STONE[4]); c.hline(X0, YB - 5, X1 - X0, STONE[3]); c.hline(X0, YB - 1, X1 - X0, STONE[1])
    def damp(xa, wa, ha):
        for i in range(wa):
            hh = ha + int(3 * math.sin(i / 5.0 + xa) + rng.randint(-1, 1))
            for j in range(hh):
                x, y = xa + i, by - 2 - j
                r, g, b, a = c.get(x, y)
                c.pset(x, y, tuple(round(v * f) for v, f in zip((r, g, b), SH1 if j < hh - 1 else SH2)))
    damp(X0 + 4, 40, 8); damp(X1 - 56, 48, 7)
    c.line(X0 + 292, YT + 14, X0 + 296, YT + 30, CAL[1]); c.line(X0 + 296, YT + 30, X0 + 294, YT + 40, CAL[1])
    c.rect(X0, YT, X1 - X0, 6, TIMB[2]); c.hline(X0, YT, X1 - X0, TIMB[4]); c.hline(X0, YT + 1, X1 - X0, TIMB[3]); c.hline(X0, YT + 5, X1 - X0, TIMB[1])
    for x in range(X0 + 6, X1, 19): c.vline(x, YT + 2, 3, TIMB[1])
    c.shade(X0, YT + 6, X1 - X0, 2, SH3)
    c.shade(X0, YT + 8, 6, YB - YT - 8, SH1); c.shade(X1 - 6, YT + 8, 6, YB - YT - 8, SH1)

    # ---- vão para os fundos (cozinha): canto esquerdo
    ax, aw, ah = 80, 36, 72
    mo = arch_mask(ax - 3, aw + 6, YB - 6, ah + 3); m = arch_mask(ax, aw, YB - 6, ah)
    fill_mask(c, mo, (ax - 3, YB - 6 - ah - 3, ax + aw + 3, YB - 6), CAL[4])
    fill_mask(c, m, (ax, YB - 6 - ah, ax + aw, YB - 6), (40, 32, 36))
    for y in range(YB - 34, YB - 6):
        for x in range(ax, ax + aw):
            if m(x, y): c.pset(x, y, mix(FLOOR[1], (20, 14, 22), 0.55))
    for y in range(YB - 6 - ah, YB - 6):
        for x in range(ax, ax + aw):
            if m(x, y) and (y < YB - 6 - ah + 10 or x < ax + 3): c.pset(x, y, tuple(round(v * 0.7) for v in c.get(x, y)[:3]))
    c.vline(ax - 3, YB - 6 - ah // 2, ah // 2, CAL[4]); c.vline(ax + aw + 2, YB - 6 - ah // 2, ah // 2, CAL[1])

    # ---- forno de lenha (alvenaria + chaminé)
    ox, ow, depth = 122, 80, 16
    top_front = YB + depth - 48
    for y in range(YT + 6, top_front - depth + 2):
        t = (y - (YT + 6)) / float(top_front - depth - YT - 4); w = int(26 + 26 * t); cx_ = ox + ow // 2
        c.hline(cx_ - w // 2, y, w, BRICK[2]); c.pset(cx_ - w // 2, y, BRICK[3]); c.pset(cx_ + w // 2 - 1, y, BRICK[1])
        if (y // 4) % 2 == 0:
            for xx in range(cx_ - w // 2 + 1, cx_ + w // 2 - 1, 9): c.pset(xx, y, BRICK[1])
    c.shade(ox + ow // 2 - 13, YT + 6, 26, 3, SH2)
    c.rect(ox - 2, top_front - depth, ow + 4, depth, CAL[3]); c.hline(ox - 2, top_front - depth, ow + 4, CAL[4])
    c.vline(ox - 2, top_front - depth, depth, CAL[4]); c.vline(ox + ow + 1, top_front - depth, depth, CAL[2])
    c.shade(ox + ow // 2 - 13, top_front - depth, 26, 5, SH1)
    c.rect(ox, top_front, ow, 48, BRICK[2])
    for r, y in enumerate(range(top_front, top_front + 48, 4)):
        c.hline(ox, y + 3, ow, BRICK[1]); off = (r % 2) * 5
        for x in range(ox + off, ox + ow, 10):
            if x > ox: c.vline(x, y, 3, BRICK[1])
            col = rng.choice([BRICK[2], BRICK[2], BRICK[3], BRICK[1]])
            for i in range(1, 9):
                if x + i < ox + ow:
                    for j in range(3): c.pset(x + i, y + j, col)
    c.hline(ox, top_front, ow, BRICK[4]); c.vline(ox, top_front, 48, BRICK[3]); c.vline(ox + ow - 1, top_front, 48, BRICK[1])
    c.hline(ox - 2, top_front, ow + 4, CAL[3]); c.hline(ox - 2, top_front + 1, ow + 4, CAL[2]); c.hline(ox - 2, top_front + 2, ow + 4, CAL[1])
    mx, mw, mh = ox + ow // 2 - 17, 34, 25; my = top_front + 48 - 9
    fill_mask(c, arch_mask(mx - 2, mw + 4, my, mh + 2), (mx - 2, my - mh - 2, mx + mw + 2, my), IRON[2])
    fill_mask(c, arch_mask(mx, mw, my, mh), (mx, my - mh, mx + mw, my), (24, 18, 20))
    mm = arch_mask(mx, mw, my, mh)
    for y in range(my - 7, my):
        for x in range(mx + 5, mx + mw - 4):
            if mm(x, y): c.pset(x, y, (50, 30, 26))
    c.rect(mx - 6, my, mw + 12, 3, STONE[4]); c.hline(mx - 6, my + 2, mw + 12, STONE[1])
    c.rect(ox, top_front + 48 - 6, ow, 6, STONE[2]); c.hline(ox, top_front + 48 - 6, ow, STONE[4]); c.hline(ox, top_front + 47, ow, STONE[1])
    c.shade(ox + 1, top_front + 48, ow + 3, 6, SH3); c.shade(ox + 4, top_front + 54, ow + 3, 4, SH2)

    # ---- pilha de lenha ao lado do forno (chão)
    lx, ly = 203, YB + 14
    for (dx, dy) in [(0, 0), (6, 0), (12, 0), (3, -5), (9, -5), (6, -10)]:
        ell(c, lx + dx + 3, ly + dy - 3, 3.2, 3.0, TIMB[2]); ell(c, lx + dx + 3, ly + dy - 3, 2, 1.9, TIMB[4]); c.pset(lx + dx + 3, ly + dy - 3, TIMB[3])
    c.shade(lx - 1, ly, 20, 3, SH2)

    # ---- bancada de trabalho encostada na parede (massa, tabuleiros) + janela do quintal acima
    bx0, bw = 224, 78
    # janela
    wx, wy, ww, wh = 238, YB - 29 - 41, 36, 41
    c.rect(wx - 3, wy - 3, ww + 6, wh + 6, CAL[4]); c.rect(wx + ww + 1, wy - 3, 2, wh + 6, CAL[2]); c.hline(wx - 3, wy + wh + 2, ww + 6, CAL[1])
    for y in range(wy, wy + wh):
        for x in range(wx, wx + ww): c.pset(x, y, SKY_V(y - wy, wh))
    c.rect(wx, wy + 24, ww, 17, mix((200, 190, 170), (214, 222, 222), 0.3)); c.hline(wx, wy + 24, ww, (222, 214, 196))
    for (cx_, cy_, rr) in [(wx + 8, wy + 30, 11), (wx + 23, wy + 27, 13), (wx + 32, wy + 34, 9), (wx + 14, wy + 38, 10)]:
        for dy in range(-rr, rr):
            for dx in range(-rr, rr + 1):
                if dx * dx + dy * dy <= rr * rr and wx <= cx_ + dx < wx + ww and wy <= cy_ + dy < wy + wh:
                    t = (dy / rr + dx / rr) * 0.5
                    c.pset(cx_ + dx, cy_ + dy, LEAF[3] if t < -0.35 else (LEAF[2] if t < 0.15 else LEAF[1]))
    for _ in range(12):
        px_, py_ = wx + rng.randint(2, ww - 4), wy + rng.randint(22, 38); c.rect(px_, py_, 2, 1, LEAF[4]); c.pset(px_ + 1, py_ + 1, LEAF[1])
    c.rect(wx, wy, ww, 2, WOOD[3]); c.rect(wx, wy, 2, wh, WOOD[3]); c.rect(wx + ww - 2, wy, 2, wh, WOOD[1]); c.rect(wx, wy + wh - 2, ww, 2, WOOD[1])
    c.vline(wx + ww // 2 - 1, wy, wh, WOOD[2]); c.vline(wx + ww // 2, wy, wh, WOOD[1]); c.hline(wx, wy + 15, ww, WOOD[2]); c.hline(wx, wy + 16, ww, WOOD[1])
    c.poly([(wx + 3, wy + 13), (wx + 9, wy + 3), (wx + 12, wy + 3), (wx + 6, wy + 13)], (236, 242, 244))
    c.shade(wx + 2, wy + 2, ww - 4, 3, SH1); c.shade(wx + 2, wy + 2, 3, wh - 4, SH1)
    c.rect(wx - 5, wy + wh + 2, ww + 10, 3, STONE[4]); c.hline(wx - 5, wy + wh + 4, ww + 10, STONE[1]); c.shade(wx - 4, wy + wh + 5, ww + 8, 3, SH2)
    # bancada: tampo (0,9 m) + frente com prateleira aberta
    bh = 22; btop_b = YB - bh; btop_f = YB + 13 - bh
    c.rect(bx0, btop_b, bw, 13, TIMB[3]); c.hline(bx0, btop_b, bw, TIMB[4]); c.vline(bx0, btop_b, 13, TIMB[4]); c.vline(bx0 + bw - 1, btop_b, 13, TIMB[2])
    for i in range(3): c.line(bx0 + 6 + i * 24, btop_b + 3 + i, bx0 + 20 + i * 24, btop_b + 4 + i, TIMB[2])
    c.rect(bx0, btop_f, bw, 3, TIMB[2]); c.hline(bx0, btop_f, bw, TIMB[4]); c.hline(bx0, btop_f + 2, bw, TIMB[1])
    c.rect(bx0 + 1, btop_f + 3, bw - 2, YB + 13 - (btop_f + 3), TIMB[1])               # vão da prateleira (sombra)
    c.shade(bx0 + 1, btop_f + 3, bw - 2, 5, SH2)
    c.rect(bx0, btop_f + 3, 3, YB + 13 - btop_f - 3, TIMB[2]); c.rect(bx0 + bw - 3, btop_f + 3, 3, YB + 13 - btop_f - 3, TIMB[2]); c.rect(bx0 + 38, btop_f + 3, 2, YB + 13 - btop_f - 3, TIMB[2])
    c.hline(bx0 + 3, YB + 7, bw - 6, TIMB[3]); c.hline(bx0 + 3, YB + 8, bw - 6, TIMB[0])
    # sacos de farinha e cesto na prateleira
    for sx in (bx0 + 8, bx0 + 22):
        c.rect(sx, YB - 2, 11, 12, SACK[3]); c.rect(sx + 3, YB - 4, 5, 3, SACK[3]); c.hline(sx + 3, YB - 4, 5, SACK[4]); c.hline(sx + 3, YB - 2, 5, SACK[1])
        c.vline(sx, YB - 2, 12, SACK[4]); c.vline(sx + 10, YB - 2, 12, SACK[2]); c.hline(sx + 2, YB + 3, 7, RED[2]); c.hline(sx + 2, YB + 4, 7, RED[2])
    ell(c, bx0 + 54, YB + 4, 8, 4, STRAW[2]); c.rect(bx0 + 46, YB + 4, 17, 5, STRAW[2]); c.hline(bx0 + 46, YB + 4, 17, STRAW[4]); c.hline(bx0 + 46, YB + 8, 17, STRAW[1])
    for k in range(4): c.vline(bx0 + 48 + k * 4, YB + 5, 4, STRAW[1])
    c.shade(bx0 + 1, YB + 13, bw + 3, 3, SH3); c.shade(bx0 + 3, YB + 16, bw + 2, 3, SH2)
    # objetos sobre a bancada: tabuleiro com pães, tigela com massa, rolo
    def tray(x, y):
        c.rect(x, y, 26, 9, IRON[3]); c.hline(x, y, 26, IRON[4]); c.hline(x, y + 8, 26, IRON[1]); c.vline(x, y, 9, IRON[4]); c.vline(x + 25, y, 9, IRON[2])
        for k in range(4):
            px_ = x + 2 + k * 6; ell(c, px_ + 3, y + 4, 3.2, 2.2, BREAD[3]); c.hline(px_ + 1, y + 3, 4, BREAD[4]); c.pset(px_ + 2, y + 5, BREAD[1]); c.pset(px_ + 4, y + 5, BREAD[1])
    tray(bx0 + 3, btop_b + 2)
    ell(c, bx0 + 42, btop_b + 6, 7, 3.6, CAL[2]); ell(c, bx0 + 42, btop_b + 5, 6, 2.8, CAL[4]); c.pset(bx0 + 39, btop_b + 4, CAL[4])
    c.rect(bx0 + 54, btop_b + 6, 16, 2, TIMB[4]); c.hline(bx0 + 54, btop_b + 8, 16, TIMB[1]); c.rect(bx0 + 52, btop_b + 5, 2, 4, TIMB[3]); c.rect(bx0 + 70, btop_b + 5, 2, 4, TIMB[3])

    # ---- lousa do cardápio (Fiado até sexta) entre a chaminé e a janela
    lx0, ly0, lw, lh = 208, 58, 22, 25
    c.rect(lx0 - 2, ly0 - 2, lw + 4, lh + 4, TIMB[3]); c.hline(lx0 - 2, ly0 - 2, lw + 4, TIMB[4]); c.rect(lx0 + lw, ly0 - 2, 2, lh + 4, TIMB[1]); c.hline(lx0 - 2, ly0 + lh + 1, lw + 4, TIMB[1])
    c.rect(lx0, ly0, lw, lh, (30, 42, 38)); c.shade(lx0, ly0, lw, 2, SH1)
    CH = (226, 226, 214)
    tiny(c, lx0 + 1, ly0 + 4, "FIADO", CH); tiny(c, lx0 + 5, ly0 + 12, "ATÉ", CH); tiny(c, lx0 + 1, ly0 + 18, "SEXTA", CH)
    c.rect(lx0 + 15, ly0 + lh - 2, 4, 1, mix(CH, (30, 42, 38), 0.35))
    # ---- calendário
    kx, ky = 282, YB - 62
    c.rect(kx, ky, 15, 20, CAL[4]); c.rect(kx, ky, 15, 5, RED[2]); c.vline(kx + 14, ky, 20, CAL[2]); c.hline(kx, ky + 19, 15, CAL[2])
    for r in range(3):
        for q in range(4): c.pset(kx + 2 + q * 3, ky + 8 + r * 3, IRON[2])
    c.pset(kx + 7, ky - 1, IRON[2])
    # ---- estante (armazenamento) + rádio de pilha
    ex, ew, eh = 308, 38, 60
    y0 = YB - eh
    c.rect(ex, y0, ew, eh, TIMB[2]); c.hline(ex, y0, ew, TIMB[4]); c.vline(ex, y0, eh, TIMB[3]); c.vline(ex + ew - 1, y0, eh, TIMB[1])
    c.rect(ex - 1, y0 - 5, ew + 2, 5, TIMB[3]); c.hline(ex - 1, y0 - 5, ew + 2, TIMB[4])
    cbs = []
    for k in range(4):
        ct = y0 + 2 + k * 14; cb = ct + 12; cbs.append(cb)          # compartimento 12 px; tábua de 2 px
        c.rect(ex + 2, ct, ew - 4, 12, TIMB[0]); c.shade(ex + 2, ct, ew - 4, 3, SH2)
        c.rect(ex + 2, cb, ew - 4, 2, TIMB[3]); c.hline(ex + 2, cb, ew - 4, TIMB[4])
    # 1) rádio de pilha (antena recolhida) + caixa de bolo + lata
    cb = cbs[0]
    c.rect(ex + 4, cb - 8, 13, 8, IRON[2]); c.hline(ex + 4, cb - 8, 13, IRON[4]); c.rect(ex + 6, cb - 6, 5, 4, STRAW[3]); c.pset(ex + 14, cb - 6, STRAW[4]); c.pset(ex + 14, cb - 3, RED[3])
    c.line(ex + 15, cb - 8, ex + 17, cb - 10, IRON[4])
    c.rect(ex + 20, cb - 7, 10, 7, CAL[4]); c.hline(ex + 20, cb - 7, 10, CAL[4]); c.hline(ex + 20, cb - 1, 10, CAL[1]); c.hline(ex + 21, cb - 4, 8, CAL[2])
    c.rect(ex + 32, cb - 5, 4, 5, RED[2]); c.hline(ex + 32, cb - 5, 4, CAL[4])
    # 2) potes de vidro
    cb = cbs[1]
    for k, col in enumerate([RED[3], STRAW[3], SACK[3], BREAD[3], RED[2]]):
        px_ = ex + 4 + k * 6; c.rect(px_, cb - 9, 5, 9, mix(col, (200, 220, 224), 0.28)); c.rect(px_, cb - 9, 5, 2, TIMB[4]); c.vline(px_, cb - 7, 7, mix(col, (255, 255, 255), 0.4))
    # 3) latas de café
    cb = cbs[2]
    for k in range(4):
        px_ = ex + 4 + k * 8; c.rect(px_, cb - 10, 7, 10, [RED[2], BREAD[2], STRAW[2], RED[2]][k]); c.hline(px_, cb - 10, 7, CAL[4]); c.hline(px_, cb - 6, 7, CAL[3])
    # 4) cestos de pão
    cb = cbs[3]
    for k in range(2):
        px_ = ex + 3 + k * 17; c.rect(px_, cb - 6, 15, 6, STRAW[2]); c.hline(px_, cb - 6, 15, STRAW[4]); c.hline(px_, cb - 1, 15, STRAW[1])
        for q in range(3): ell(c, px_ + 4 + q * 4, cb - 7, 2.6, 2, BREAD[3])
    c.shade(ex + 1, YB, ew + 3, 3, SH3); c.shade(ex + 3, YB + 3, ew + 2, 3, SH2)

    # ---- altar de São Jorge: nicho com imagem central, vela, copo d'água, flores, fitinhas
    nx, nw, nh = 353, 22, 44; nb = YB - 31 - 6
    mn = arch_mask(nx, nw, nb, nh)
    fill_mask(c, arch_mask(nx - 3, nw + 6, nb + 3, nh + 3), (nx - 3, nb - nh - 3, nx + nw + 3, nb + 3), CAL[4])
    BG = (92, 122, 146)
    def inner(x, y):
        k = 0.78 if (x < nx + 3 or y < nb - nh + 5) else 1.0
        return tuple(round(v * k) for v in BG)
    fill_mask(c, mn, (nx, nb - nh, nx + nw, nb), inner)
    # halo da vela acesa
    for y in range(nb - 20, nb):
        for x in range(nx, nx + nw):
            d2 = (x - (nx + 3)) ** 2 + (y - (nb - 10)) ** 2
            if mn(x, y) and d2 <= 25:
                r_, g_, b_, a_ = c.get(x, y); c.pset(x, y, mix((r_, g_, b_), (255, 206, 140), 0.16 if d2 <= 9 else 0.08))
    # imagem emoldurada (São Jorge a cavalo, lança no dragão)
    fx, fy_, fw, fh = nx + 6, nb - 33, 10, 19
    c.rect(fx, fy_, fw, fh, TIMB[2]); c.hline(fx, fy_, fw, TIMB[4]); c.vline(fx, fy_, fh, TIMB[3]); c.hline(fx, fy_ + fh - 1, fw, TIMB[0]); c.vline(fx + fw - 1, fy_, fh, TIMB[1])
    c.rect(fx + 1, fy_ + 1, 8, 17, (178, 198, 214)); c.rect(fx + 7, fy_ + 2, 2, 2, (238, 232, 200))
    c.rect(fx + 1, fy_ + 14, 8, 4, (92, 112, 82))
    c.rect(fx + 1, fy_ + 15, 4, 2, LEAF[2]); c.pset(fx + 1, fy_ + 14, LEAF[3])                       # dragão
    ell(c, fx + 5.5, fy_ + 10, 3, 2, SACK[4]); c.rect(fx + 7, fy_ + 6, 2, 3, SACK[4]); c.pset(fx + 8, fy_ + 6, SACK[3])  # cavalo
    c.vline(fx + 3, fy_ + 11, 3, SACK[2]); c.vline(fx + 7, fy_ + 11, 3, SACK[2])
    c.rect(fx + 4, fy_ + 5, 2, 4, RED[2]); c.pset(fx + 4, fy_ + 4, (200, 150, 112))                      # cavaleiro e capa
    c.line(fx + 6, fy_ + 3, fx + 3, fy_ + 14, IRON[4])                                                    # lança
    # fitinhas penduradas
    for xx, col in [(nx + 2, (70, 130, 170)), (nx + 3, (214, 170, 60)), (nx + 18, (180, 70, 66)), (nx + 19, (226, 226, 214))]:
        c.pset(xx, nb - 31, IRON[3]); c.vline(xx, nb - 30, 11, col)
    # prateleira de pedra
    c.rect(nx - 5, nb, nw + 8, 3, STONE[4]); c.hline(nx - 5, nb + 2, nw + 8, STONE[1]); c.shade(nx - 4, nb + 3, nw + 6, 3, SH2)
    # vela acesa
    c.rect(nx + 2, nb - 8, 3, 8, SACK[3]); c.vline(nx + 2, nb - 8, 8, SACK[4]); c.vline(nx + 4, nb - 8, 8, SACK[1])
    c.pset(nx + 3, nb - 9, IRON[1]); c.pset(nx + 3, nb - 10, (255, 150, 60)); c.pset(nx + 3, nb - 11, (255, 218, 120))
    # copo d'água
    c.rect(nx + 9, nb - 5, 4, 5, (210, 226, 232)); c.hline(nx + 9, nb - 5, 4, (240, 246, 248)); c.rect(nx + 10, nb - 3, 2, 3, (150, 190, 214)); c.hline(nx + 9, nb - 1, 4, (180, 200, 210))
    # vasinho com flores
    c.rect(nx + 16, nb - 6, 5, 6, CLAY[2]); c.hline(nx + 16, nb - 6, 5, CLAY[4]); c.vline(nx + 20, nb - 6, 6, CLAY[1]); c.hline(nx + 16, nb - 1, 5, CLAY[1])
    for xx, hh in [(nx + 17, 5), (nx + 18, 7), (nx + 19, 6)]: c.vline(xx, nb - 6 - hh, hh, LEAF[2])
    for (xx, yy, col) in [(nx + 16, nb - 12, RED[3]), (nx + 18, nb - 14 + 1, SACK[4]), (nx + 20, nb - 11, RED[3]), (nx + 19, nb - 13, SACK[3])]:
        c.rect(xx, yy, 2, 2, col)

    # ---- porta da escada
    dx, dw, dh = 382, 22, 60
    c.rect(dx - 3, YB - dh - 3, dw + 6, dh + 3, CAL[4]); c.vline(dx + dw + 2, YB - dh - 3, dh + 3, CAL[1])
    c.rect(dx, YB - dh, dw, dh - 6, WOOD[2])
    for bx in range(dx + 3, dx + dw - 2, 5): c.vline(bx, YB - dh + 11, dh - 17, WOOD[1]); c.vline(bx + 1, YB - dh + 11, dh - 17, WOOD[3])
    c.rect(dx, YB - dh, dw, 10, (30, 24, 28))
    for bx in range(dx + 2, dx + dw, 4): c.vline(bx, YB - dh, 10, IRON[3])
    c.hline(dx, YB - dh + 10, dw, WOOD[0])
    c.rect(dx + 3, YB - dh + 16, dw - 6, 14, WOOD[1]); c.hline(dx + 3, YB - dh + 16, dw - 6, WOOD[0])
    c.rect(dx + 3, YB - dh + 34, dw - 6, 14, WOOD[1]); c.hline(dx + 3, YB - dh + 34, dw - 6, WOOD[0])
    c.rect(dx + dw - 6, YB - dh + 28, 2, 3, IRON[4]); c.shade(dx, YB - dh, dw, 2, SH2)
    c.rect(dx - 4, YB - 6, dw + 8, 3, STONE[4]); c.hline(dx - 4, YB - 4, dw + 8, STONE[1])
    return c

def light_pass(c):
    wx, ww = 238, 36
    for band, (amt, sh) in enumerate([(0.17, 26), (0.12, 0)]):
        pts = [(wx + 4 + sh, YB + 18), (wx + ww - 2 + sh, YB + 18), (wx + ww - 22 + sh, YB + 52 - sh // 2), (wx - 18 + sh, YB + 52 - sh // 2)]
        t = C(VW, VH); t.poly(pts, (255, 255, 255, 255))
        for y in range(YB + 16, YB + 54):
            for x in range(wx - 24, wx + ww + 40):
                if t.p[x, y][3]:
                    r, g, b, a = c.p[x, y]; c.p[x, y] = (*mix((r, g, b), (255, 238, 190), amt), a)
    dxc = VW // 2
    t = C(VW, VH); t.poly([(dxc - 26, YF - 1), (dxc + 26, YF - 1), (dxc + 40, YF - 38), (dxc - 12, YF - 38)], (255, 255, 255, 255))
    for y in range(YF - 40, YF):
        for x in range(dxc - 30, dxc + 46):
            if t.p[x, y][3]:
                r, g, b, a = c.p[x, y]; c.p[x, y] = (*mix((r, g, b), (255, 226, 170), 0.20 if y > YF - 20 else 0.11), a)

def frame_room(c):
    L0, L1, R0, R1 = 60, 72, 408, 420
    endb = YF + 10
    for (xa, xb, light) in [(L0, L1, True), (R0, R1, False)]:
        c.rect(xa, CAP, xb - xa, endb - CAP, CAL[2] if light else CAL[1])
        c.rect(xa, CAP, xb - xa, YF - 96 - CAP, CAL[3] if light else CAL[2])
        c.hline(xa, YF - 96, xb - xa, CAL[1] if light else CAL[0])
        c.vline(xa, CAP, endb - CAP, CAL[4] if light else CAL[2]); c.vline(xb - 1, CAP, endb - CAP, CAL[1] if light else CAL[0])
        c.rect(xa, YF - 14, xb - xa, 24, STONE[2]); c.hline(xa, YF - 14, xb - xa, STONE[3])
    c.rect(L0, CAP, R1 - L0, 8, CAL[3]); c.hline(L0, CAP, R1 - L0, CAL[4]); c.hline(L0, CAP + 7, R1 - L0, CAL[1])
    door0, door1 = VW // 2 - 26, VW // 2 + 26
    for (xa, xb) in [(L1, door0), (door1, R0)]:
        c.rect(xa, YF, xb - xa, 10, STONE[2]); c.hline(xa, YF, xb - xa, STONE[4]); c.hline(xa, YF + 1, xb - xa, STONE[3]); c.hline(xa, YF + 9, xb - xa, STONE[0])
        for x in range(xa, xb, 17): c.vline(x, YF + 2, 7, STONE[1])
    c.rect(door0 - 1, YF, door1 - door0 + 2, 6, STONE[4]); c.hline(door0 - 1, YF + 5, door1 - door0 + 2, STONE[1])
    c.vline(door0 - 1, YF, 10, STONE[1]); c.vline(door1, YF, 10, STONE[1])
    c.shade(L1, YF + 10, R0 - L1, 4, SH3)

# ---------------------------------------------------------------- props (ordenados por profundidade)
def new(): return C(VW, VH)

def prop_counter():
    c = new()
    cx0, cx1 = X0, 252
    f1 = fy(3.3); f0 = f1 - 24; t0 = f0 - 13           # frente 1,0 m ; tampo 0,8 m de profundidade
    for y in range(f1, f1 + 5):
        for x in range(cx0, cx1 + 3): c.pset(x, y, (20, 12, 30, 120 if y < f1 + 3 else 70))
    c.rect(cx0, t0, cx1 - cx0, 13, CAL[3]); c.hline(cx0, t0, cx1 - cx0, CAL[4]); c.hline(cx0, f0 - 4, cx1 - cx0, CAL[4])
    c.rect(cx0, f0 - 3, cx1 - cx0, 3, CAL[2]); c.hline(cx0, f0 - 1, cx1 - cx0, CAL[1]); c.vline(cx1 - 1, t0, 13, CAL[2])
    rng = random.Random(3)
    for k in range(6):
        x = cx0 + rng.randint(8, cx1 - cx0 - 30); y = t0 + rng.randint(2, 9); c.line(x, y, x + rng.randint(10, 22), y + rng.randint(-1, 1), CAL[2])
    c.rect(cx0, f0, cx1 - cx0, 24, WOOD[2]); c.hline(cx0, f0, cx1 - cx0, WOOD[4]); c.hline(cx0, f0 + 1, cx1 - cx0, WOOD[3])
    for x in range(cx0 + 6, cx1 - 14, 36):
        c.rect(x, f0 + 4, 32, 14, WOOD[1]); c.hline(x, f0 + 4, 32, WOOD[0]); c.vline(x, f0 + 4, 14, WOOD[0]); c.hline(x + 1, f0 + 18, 31, WOOD[3]); c.vline(x + 31, f0 + 4, 14, WOOD[3])
    c.rect(cx0, f1 - 4, cx1 - cx0, 4, WOOD[0]); c.vline(cx1 - 1, f0, 24, WOOD[1])
    c.rect(190, f0 + 8, 5, 3, IRON[4]); c.hline(190, f0 + 11, 5, IRON[1])                     # puxador da gaveta
    c.shade(cx0, f0 + 2, cx1 - cx0, 2, SH1)
    # vitrine de vidro com pães e bolos (sobre o tampo, lado esquerdo)
    vx, vw = 88, 64; vb = f0 - 4; vt = vb - 26
    c.rect(vx, vb - 3, vw, 3, TIMB[2]); c.hline(vx, vb - 3, vw, TIMB[4]); c.hline(vx, vb - 1, vw, TIMB[0])
    for sh_y, kind in [(vb - 10, 'pao'), (vb - 20, 'bolo')]:
        c.rect(vx + 2, sh_y, vw - 4, 2, CAL[2]); c.hline(vx + 2, sh_y, vw - 4, CAL[4])
        for k in range(8 if kind == 'pao' else 3):
            if kind == 'pao':
                px_ = vx + 5 + k * 7; ell(c, px_ + 3, sh_y - 3, 3.4, 2.6, BREAD[3]); c.hline(px_ + 1, sh_y - 4, 4, BREAD[4]); c.pset(px_ + 2, sh_y - 2, BREAD[1])
            else:
                px_ = vx + 6 + k * 19; c.rect(px_, sh_y - 6, 15, 6, CAL[3]); c.rect(px_, sh_y - 8, 15, 3, BREAD[3]); c.hline(px_, sh_y - 8, 15, BREAD[4]); c.pset(px_ + 4, sh_y - 9, RED[3]); c.pset(px_ + 9, sh_y - 9, RED[3])
    c.rect(vx + 2, vt, vw - 4, vb - 3 - vt, (225, 240, 246, 46))
    c.rect(vx, vt, vw, 2, TIMB[3]); c.rect(vx, vt, 2, vb - vt, TIMB[3]); c.rect(vx + vw - 2, vt, 2, vb - vt, TIMB[1]); c.hline(vx, vt, vw, TIMB[4])
    c.poly([(vx + 6, vb - 6), (vx + 12, vt + 3), (vx + 15, vt + 3), (vx + 9, vb - 6)], (255, 255, 255, 70))
    # cesto de pães
    ell(c, 170, f0 - 8, 8, 4, STRAW[2]); c.rect(162, f0 - 8, 17, 5, STRAW[2]); c.hline(162, f0 - 8, 17, STRAW[4]); c.hline(162, f0 - 4, 17, STRAW[1])
    for k in range(3): ell(c, 165 + k * 5, f0 - 10, 3, 2.2, BREAD[3])
    # caixa registradora + caderneta do fiado + garrafa térmica e xícaras
    c.rect(206, f0 - 12, 22, 9, IRON[2]); c.hline(206, f0 - 12, 22, IRON[4]); c.rect(208, f0 - 18, 14, 7, IRON[1]); c.rect(209, f0 - 17, 12, 4, STRAW[3]); c.pset(214, f0 - 15, IRON[0])
    for k in range(4): c.pset(209 + k * 3, f0 - 9, CAL[4])
    c.rect(231, f0 - 8, 11, 6, RED[2]); c.hline(231, f0 - 8, 11, RED[4]); c.vline(231, f0 - 8, 6, RED[3]); c.hline(231, f0 - 3, 11, RED[0]); c.line(233, f0 - 6, 240, f0 - 6, CAL[4])
    c.rect(243, f0 - 16, 5, 13, CAL[3]); c.vline(243, f0 - 16, 13, CAL[4]); c.rect(243, f0 - 18, 5, 3, RED[2]); c.hline(243, f0 - 4, 5, CAL[1])
    for k in range(2): c.rect(236 + k * 0, f0 - 3 - k, 0, 0, CAL[3])
    c.rect(149, f0 - 4, 3, 3, CAL[4]); c.hline(149, f0 - 2, 3, CAL[1]); c.rect(153, f0 - 4, 3, 3, CAL[4]); c.hline(153, f0 - 2, 3, CAL[1])
    return c, dict(base=f1, solid=[cx0, f1 - 15, cx1 + 4, f1 + 2])

def chair(c, x, y, view, flip=False):
    """Cadeira de madeira pintada. view: front (de frente p/ a câmera), back (de costas), side (perfil; flip = olha p/ a esquerda)."""
    W_ = WOOD; S = TIMB
    if view == 'front':
        c.rect(x - 5, y - 28, 10, 12, S[2]); c.vline(x - 5, y - 28, 12, S[3]); c.vline(x + 4, y - 28, 12, S[1]); c.hline(x - 5, y - 28, 10, S[4])
        c.hline(x - 4, y - 24, 8, S[0]); c.hline(x - 4, y - 21, 8, S[0])
        c.rect(x - 5, y - 17, 10, 6, S[3]); c.hline(x - 5, y - 17, 10, S[4])
        c.rect(x - 5, y - 11, 10, 2, S[2]); c.hline(x - 5, y - 10, 10, S[1])
        c.rect(x - 5, y - 9, 2, 9, S[2]); c.rect(x + 3, y - 9, 2, 9, S[1])
    elif view == 'back':
        c.rect(x - 5, y - 23, 10, 13, S[2]); c.vline(x - 5, y - 23, 13, S[3]); c.vline(x + 4, y - 23, 13, S[1]); c.hline(x - 5, y - 23, 10, S[4])
        c.hline(x - 4, y - 18, 8, S[0]); c.hline(x - 4, y - 14, 8, S[0])
        c.rect(x - 5, y - 10, 10, 2, S[1]); c.rect(x - 5, y - 8, 2, 8, S[2]); c.rect(x + 3, y - 8, 2, 8, S[1])
    else:
        d = -1 if flip else 1                      # direção em que a cadeira olha
        bx = x - 5 * d
        c.rect(min(bx, bx + d * 2) if d < 0 else bx - 1, y - 28, 3, 20, S[2])
        for q in range(3): c.hline(bx - 1 if d > 0 else bx - 1, y - 26 + q * 7, 3, S[0])
        c.rect(x - 6, y - 16, 12, 6, S[3]); c.hline(x - 6, y - 16, 12, S[4])
        c.rect(x - 6, y - 10, 12, 2, S[2]); c.hline(x - 6, y - 9, 12, S[1])
        c.rect(x - 6, y - 8, 2, 8, S[2]); c.rect(x + 4, y - 8, 2, 8, S[1])
    for yy in range(2): c.hline(x - 6, y + yy, 12, (18, 10, 28, 70))

def prop_table(cx, yb, cloth=False):
    c = new()
    for yy in range(3): c.hline(cx - 6, yb + yy - 1, 12, (18, 10, 28, 80))
    ell(c, cx, yb - 1, 7, 3, TIMB[1]); c.rect(cx - 2, yb - 17, 4, 15, TIMB[2]); c.vline(cx - 2, yb - 17, 15, TIMB[3]); c.vline(cx + 1, yb - 17, 15, TIMB[1])
    ell(c, cx, yb - 17 + 2, 12, 6.5, TIMB[1])           # espessura
    ell(c, cx, yb - 18, 12, 6.5, TIMB[3] if not cloth else CAL[4])
    if cloth:
        for j in range(-7, 8):
            for i in range(-12, 13):
                if ((i + 12) // 4 + (j + 7) // 3) % 2 == 0 and (i / 12.0) ** 2 + (j / 6.5) ** 2 <= 0.96: c.pset(cx + i, yb - 18 + j, RED[3])
        for i in range(-12, 13):
            if abs(i) < 12: c.pset(cx + i, yb - 14 + int(1 + 2 * math.sqrt(max(0, 1 - (i / 12.0) ** 2))), RED[1])
    else:
        c.line(cx - 8, yb - 19, cx + 6, yb - 17, TIMB[2]); c.line(cx - 4, yb - 21, cx + 8, yb - 19, TIMB[2])
    # xícara e açucareiro
    c.rect(cx - 5, yb - 22, 4, 3, CAL[4]); c.pset(cx - 4, yb - 22, (60, 38, 30)); c.hline(cx - 5, yb - 19, 4, CAL[2]); c.pset(cx - 1, yb - 21, CAL[3])
    c.rect(cx + 3, yb - 23, 4, 4, CAL[3]); c.hline(cx + 3, yb - 23, 4, CAL[4]); c.hline(cx + 3, yb - 20, 4, CAL[1])
    return c

def prop_filter(cx, cy):
    """Filtro de barro em 3/4: suporte de madeira de 3 pes; corpo inferior (agua filtrada) com torneira de latao saindo
    para a direita; corpo superior com aro elíptico visivel, faixa vitrificada, tampa em cupula e botao. (cx, cy) = centro da base no piso."""
    c = new(); rng = random.Random(11)
    F = FILT
    def shade_idx(u): return 4 if u < -0.55 else (3 if u < -0.12 else (2 if u < 0.42 else (1 if u < 0.8 else 0)))
    def cyl(rows, y_bot, ry):
        y_top = y_bot - len(rows) + 1
        for k, w in enumerate(rows):
            for x in range(-w, w + 1): c.pset(cx + x, y_top + k, F[shade_idx(x / float(w))])
        w = rows[-1]
        for x in range(-w, w + 1):
            u = x / float(w); extra = int(round(ry * math.sqrt(max(0.0, 1 - u * u))))
            for q in range(1, extra + 1): c.pset(cx + x, y_bot + q, F[shade_idx(u)])
        return y_top
    # suporte de madeira escura: tampo elíptico + 3 pes (o de tras fica oculto pelo corpo)
    sy = cy - 7
    for (lx, ll) in [(cx - 7, 8), (cx + 7, 8), (cx, 10)]:
        c.rect(lx - 1, sy + 1, 2, ll, TIMB[1]); c.vline(lx - 1, sy + 1, ll, TIMB[2]); c.pset(lx, sy + ll, TIMB[0])
    ell(c, cx, sy + 2, 10.5, 3.8, TIMB[0]); ell(c, cx, sy + 1, 10.5, 3.8, TIMB[2]); ell(c, cx, sy, 10.5, 3.8, TIMB[3])
    ell(c, cx, sy, 8.2, 2.7, TIMB[2]); c.hline(cx - 6, sy - 3, 10, TIMB[4])
    # corpo inferior (bojo)
    low = [6, 7, 8, 8, 8, 8, 8, 7, 7, 6]
    y_low_bot = sy - 3
    y_low_top = cyl(low, y_low_bot, 3)
    # torneira de latao (lateral): flange no bojo, cano, cotovelo p/ baixo, registro, gota
    ty = y_low_top + 6
    c.rect(cx + 7, ty - 2, 2, 5, STRAW[1]); c.vline(cx + 7, ty - 2, 5, STRAW[3]); c.hline(cx + 7, ty - 2, 2, STRAW[4])
    c.rect(cx + 9, ty - 1, 5, 2, STRAW[3]); c.hline(cx + 9, ty - 1, 5, STRAW[4]); c.hline(cx + 9, ty, 5, STRAW[1])
    c.rect(cx + 13, ty + 1, 2, 4, STRAW[2]); c.pset(cx + 13, ty + 1, STRAW[4]); c.vline(cx + 14, ty + 1, 4, STRAW[1])
    c.rect(cx + 10, ty - 4, 1, 3, STRAW[2]); c.rect(cx + 9, ty - 5, 3, 1, STRAW[4])
    c.pset(cx + 14, ty + 6, (176, 208, 228))
    # sombra do corpo de cima sobre o de baixo + aro/ressalto
    for x in range(-8, 9):
        r_, g_, b_, a_ = c.get(cx + x, y_low_top + 1)
        if a_: c.pset(cx + x, y_low_top + 1, tuple(round(v * 0.62) for v in (r_, g_, b_)))
    up = [8, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9]
    y_up_bot = y_low_top
    ell(c, cx, y_up_bot - 1, 9.6, 3.3, F[0]); ell(c, cx, y_up_bot - 2, 9.6, 3.3, F[4] if False else F[3])
    c.hline(cx - 7, y_up_bot - 4, 10, F[4])
    y_up_top = cyl(up, y_up_bot - 3, 3)
    # faixa vitrificada (sob o aro) e frisos de torno: so em trechos, como marcas de uso e nao listras
    for k, (yy, a, b) in enumerate([(y_up_top + 3, -8, 8), (y_up_top + 4, -8, 8), (y_up_top + 5, -8, 8)]):
        for x in range(a, b + 1):
            u = x / 9.0
            c.pset(cx + x, yy, mix(F[shade_idx(u)], (40, 18, 18), 0.55 if k == 1 else 0.30))
    for yy, a, b in [(y_up_top + 8, -6, 1), (y_up_top + 9, -1, 6), (y_low_top + 4, -6, 0), (y_low_top + 7, 1, 6)]:
        for x in range(a, b + 1):
            r_, g_, b_, a_ = c.get(cx + x, yy); c.pset(cx + x, yy, tuple(round(v * 0.80) for v in (r_, g_, b_)))
    for _ in range(16):                                                                                  # pontos de queima / engobo irregular
        x = cx + rng.randint(-7, 7); y = rng.randint(y_up_top + 6, y_low_top + 8)
        r_, g_, b_, a_ = c.get(x, y)
        if a_: c.pset(x, y, mix((r_, g_, b_), (36, 18, 16), .45) if rng.random() < .55 else mix((r_, g_, b_), (214, 150, 120), .35))
    # boca (aro elíptico) + tampa em cupula + botao
    ell(c, cx, y_up_top, 9.6, 3.3, F[4]); ell(c, cx, y_up_top + .3, 8.2, 2.6, F[1]); ell(c, cx, y_up_top + .6, 7, 1.9, F[0])
    for dy, w in [(0, 7), (-1, 7), (-2, 6), (-3, 4), (-4, 3)]:
        for x in range(-w, w + 1):
            u = x / float(w); c.pset(cx + x, y_up_top - 1 + dy, F[min(4, shade_idx(u) + 0)] if u < 0.5 else F[1])
    c.hline(cx - 6, y_up_top - 1, 11, F[0]); c.hline(cx - 5, y_up_top - 3, 3, F[4])
    c.rect(cx - 1, y_up_top - 7, 3, 3, F[3]); c.hline(cx - 1, y_up_top - 7, 3, F[4]); c.pset(cx + 1, y_up_top - 5, F[0])
    return c, cy

def prop_aparador(x0=74, x1=100, yb=None):
    """Aparador baixo no canto frontal esquerdo, com o filtro e um copo em cima. Encostado na parede esquerda."""
    yb = yb or fy(6.4)
    c = new(); w = x1 - x0; h, d = 18, 10
    top_f = yb - h; top_b = top_f - d
    for yy in range(3): c.hline(x0, yb + yy, w + 3, (18, 10, 28, 90 - yy * 20))
    c.vline(x1, top_b + 6, h + d - 6, (18, 10, 28, 60))
    c.rect(x0, top_b, w, d, TIMB[3]); c.hline(x0, top_b, w, TIMB[4]); c.vline(x1 - 1, top_b, d, TIMB[2])
    for yy in (top_b + 4, top_b + 8): c.line(x0 + 2, yy, x1 - 4, yy, TIMB[2])
    c.rect(x0, top_f, w, 2, TIMB[4]); c.hline(x0, top_f + 1, w, TIMB[3])
    c.rect(x0, top_f + 2, w, h - 2, TIMB[2]); c.vline(x0, top_f + 2, h - 2, TIMB[3]); c.vline(x1 - 1, top_f + 2, h - 2, TIMB[1])
    for dx in (x0 + 2, x0 + 14):
        c.rect(dx, top_f + 3, 10, h - 8, TIMB[1]); c.hline(dx, top_f + 4, 10, TIMB[0]); c.vline(dx, top_f + 4, h - 9, TIMB[0]); c.hline(dx + 1, top_f + h - 6, 9, TIMB[3]); c.vline(dx + 9, top_f + 4, h - 9, TIMB[3])
    c.pset(x0 + 11, top_f + 9, IRON[4]); c.pset(x0 + 14, top_f + 9, IRON[4])
    c.rect(x0, yb - 3, w, 3, TIMB[0]); c.hline(x0, yb - 3, w, TIMB[1])
    cy = top_b + d // 2 + 2
    fcx = x0 + 11
    f, _ = prop_filter(fcx, cy)
    c.im.alpha_composite(f.im)
    # copo ao lado do filtro
    gx = fcx + 11                                                       # copo sob a torneira
    c.rect(gx - 1, cy + 1, 3, 5, (210, 226, 232)); c.hline(gx - 1, cy + 1, 3, (240, 246, 248)); c.rect(gx, cy + 3, 1, 3, (150, 190, 214)); c.hline(gx - 1, cy + 5, 3, (160, 188, 204))
    return c, dict(base=yb + 1, solid=[x0 - 1, top_b, x1 + 3, yb + 3])

def build_props():
    props = []
    def add(name, c, base, solid=None):
        im = c.im; bb = im.getbbox()
        crop = im.crop(bb); crop.save(f'../assets/prop_{name}.png')
        props.append(dict(name=name, x=bb[0], y=bb[1], base=base, solid=solid))
    cc, info = prop_counter(); add('counter', cc, info['base'], info['solid'])
    tA = (312, fy(3.9)); tB = (376, fy(5.0))
    def seat(name, view, x, y, flip=False):
        c = new(); chair(c, x, y, view, flip); add(name, c, y, [x - 6, y - 3, x + 6, y + 2])
    seat('chair_a_back', 'front', tA[0], tA[1] - 8)
    seat('chair_b_back', 'front', tB[0], tB[1] - 8)
    add('table_a', prop_table(tA[0], tA[1]), tA[1] + 1, [tA[0] - 12, tA[1] - 6, tA[0] + 12, tA[1] + 5])
    add('table_b', prop_table(tB[0], tB[1], cloth=True), tB[1] + 1, [tB[0] - 12, tB[1] - 6, tB[0] + 12, tB[1] + 5])
    seat('chair_a_l', 'side', tA[0] - 19, tA[1] + 4, False)
    seat('chair_a_r', 'side', tA[0] + 19, tA[1] + 4, True)
    seat('chair_b_l', 'side', tB[0] - 19, tB[1] + 4, False)
    seat('chair_b_f', 'back', tB[0], tB[1] + 17)
    ca, ia = prop_aparador(); add('aparador', ca, ia['base'], ia['solid'])
    return props

if __name__ == '__main__':
    base = build_base(); light_pass(base); frame_room(base)
    base.save('../assets/bakery_interior_base.png')
    props = build_props()
    # solidos de arquitetura (pés)
    solids = [
        [118, YB, 208, YB + 20],          # forno
        [204, YB, 226, YB + 15],          # lenha
        [222, YB, 304, YB + 17],          # bancada
        [306, YB, 348, YB + 11],          # estante
    ] + [p['solid'] for p in props if p['solid']]
    layout = dict(X0=X0, X1=X1, YB=YB, YF=YF, EXIT_X=240, props=[{k: p[k] for k in ('name', 'x', 'y', 'base')} for p in props], solids=solids,
                  gap=[252, 284], counter_back=fy(2.5))
    json.dump(layout, open('../assets/layout.json', 'w'))
    comp = base.im.copy()
    for p in sorted(props, key=lambda p: p['base']):
        comp.alpha_composite(Image.open(f"../assets/prop_{p['name']}.png"), (p['x'], p['y']))
    comp.save('../preview/interior_raw.png')
    comp.resize((VW * 2, VH * 2), Image.NEAREST).save('../preview/interior_x2.png')
    print(len(props), 'props')

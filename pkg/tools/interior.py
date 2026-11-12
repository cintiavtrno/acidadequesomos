import random, math
from pxl import *
from facade import CAL, STONE, BRICK, IRON, MOSS, TELHA, GLASS

VW, VH = 480, 270
# --- câmera 3/4 oblíqua: vertical 24 px/m, profundidade do piso 16 px/m (frente + topo visíveis) ---
VM, DM = 24, 16
X0, X1 = 72, 408           # paredes internas (14 m)
YT, YB = 28, 124           # topo e base da parede de fundo (4 m)
YF = 252                   # beira da frente do piso (8 m de profundidade)
def floor_y(depth_m): return YB + int(round(depth_m * DM))

WOOD  = ramp(165, 0.20, (0.13, 0.21, 0.31, 0.41, 0.52))     # esquadrias verde-musgo (mesma da fachada)
TIMB  = ramp(28, 0.38, (0.14, 0.22, 0.32, 0.42, 0.54))       # madeira escura
BARRA = ramp(168, 0.22, (0.22, 0.30, 0.40, 0.50, 0.60))      # barra pintada
FLOOR = ramp(22, 0.27, (0.31, 0.37, 0.43, 0.49, 0.56))
LEAF  = ramp(120, 0.38, (0.16, 0.24, 0.33, 0.43, 0.55))
VOID  = (22, 16, 19)

def arch_mask(x, w, y_floor, h):
    r = w / 2.0
    cx = x + r
    spring = y_floor - h + r
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

def build_base(seed=5):
    rng = random.Random(seed)
    c = C(VW, VH, VOID + (255,))
    # ---------------------------------------------------------------- piso (ladrilho 0,5 m = 12x8 px)
    tones = [FLOOR[1], FLOOR[2], FLOOR[2], FLOOR[3]]
    for ty in range((YF - YB) // 8):
        for tx in range((X1 - X0) // 12):
            col = rng.choice([FLOOR[2]] * 5 + [FLOOR[3]] * 3 + [mix(FLOOR[2], FLOOR[1], 0.5)] * 2)
            x, y = X0 + tx * 12, YB + ty * 8
            c.rect(x, y, 12, 8, col)
            c.hline(x, y, 12, mix(col, (255, 230, 190), 0.07))       # aresta iluminada (topo)
            c.vline(x, y, 8, mix(col, (255, 230, 190), 0.05))
            c.hline(x, y + 7, 12, mix(col, (30, 20, 40), 0.20))      # rejunte
            c.vline(x + 11, y, 8, mix(col, (30, 20, 40), 0.14))
    # desgaste: trilho mais claro entre porta e balcão (uso), 2 tons de gasto
    for ty in range(14, (YF - YB) // 8):
        for tx in range(13, 18):
            x, y = X0 + tx * 12, YB + ty * 8
            for yy in range(y, y + 8):
                for xx in range(x, x + 12):
                    r, g, b, a = c.get(xx, yy)
                    c.pset(xx, yy, mix((r, g, b), (236, 200, 160), 0.10))
    # oclusão ambiente: cantos junto às paredes laterais e à frente
    c.shade(X0, YB, 7, YF - YB, SH1); c.shade(X1 - 7, YB, 7, YF - YB, SH1)
    c.shade(X0, YB, 3, YF - YB, SH2); c.shade(X1 - 3, YB, 3, YF - YB, SH2)
    # sombra de contato no pé da parede de fundo
    c.shade(X0, YB, X1 - X0, 2, SH3); c.shade(X0, YB + 2, X1 - X0, 3, SH2); c.shade(X0, YB + 5, X1 - X0, 3, SH1)
    # ---------------------------------------------------------------- parede de fundo
    c.rect(X0, YT, X1 - X0, YB - YT, CAL[3])
    c.rect(X0, YT, X1 - X0, 8, CAL[2])                                  # sombra do frechal
    c.shade(X0, YT + 8, X1 - X0, 6, SH1)
    # barra pintada (1,3 m) com filete
    by = YB - 31
    c.rect(X0, by, X1 - X0, 31, BARRA[2]); c.hline(X0, by, X1 - X0, BARRA[4]); c.hline(X0, by + 1, X1 - X0, BARRA[3])
    c.hline(X0, by + 2, X1 - X0, BARRA[1]); c.hline(X0, by - 1, X1 - X0, CAL[1])
    for x in range(X0, X1, 7): c.vline(x, by + 4, 20, BARRA[1]) if rng.random() < 0.0 else None
    # rodapé
    c.rect(X0, YB - 6, X1 - X0, 6, STONE[2]); c.hline(X0, YB - 6, X1 - X0, STONE[4]); c.hline(X0, YB - 5, X1 - X0, STONE[3]); c.hline(X0, YB - 1, X1 - X0, STONE[1])
    # umidade ascendente / descascado (localizado, perto dos cantos e sob a janela)
    def damp(xa, wa, ha):
        for i in range(wa):
            hh = ha + int(3 * math.sin(i / 5.0 + xa) + rng.randint(-1, 1))
            for j in range(hh):
                x, y = xa + i, by - 2 - j
                r, g, b, a = c.get(x, y)
                c.pset(x, y, tuple(round(v * f) for v, f in zip((r, g, b), SH1 if j < hh - 1 else SH2)))
    damp(X0 + 6, 54, 9); damp(X1 - 70, 60, 7)
    patch(c, X0 + 32, by - 7, 12, 4, mix(CAL[2], CAL[3], 0.5), rng, jag=0.35)
    patch(c, X1 - 40, by - 6, 10, 4, mix(CAL[2], CAL[3], 0.5), rng, jag=0.35)
    # rachadura sutil
    c.line(X0 + 244, YT + 14, X0 + 248, YT + 30, CAL[1]); c.line(X0 + 248, YT + 30, X0 + 246, YT + 40, CAL[1])
    # frechal (viga) no topo e cantos
    c.rect(X0, YT, X1 - X0, 6, TIMB[2]); c.hline(X0, YT, X1 - X0, TIMB[4]); c.hline(X0, YT + 1, X1 - X0, TIMB[3]); c.hline(X0, YT + 5, X1 - X0, TIMB[1])
    for x in range(X0 + 6, X1, 19): c.vline(x, YT + 2, 3, TIMB[1])
    c.shade(X0, YT + 6, X1 - X0, 2, SH3)
    # ambient occlusion nos cantos laterais
    c.shade(X0, YT + 8, 6, YB - YT - 8, SH1); c.shade(X1 - 6, YT + 8, 6, YB - YT - 8, SH1)
    # ---------------------------------------------------------------- vão para os fundos (cozinha), arco pleno
    ax, aw, ah = 84, 36, 72
    m = arch_mask(ax, aw, YB - 6, ah)
    # moldura
    mo = arch_mask(ax - 3, aw + 6, YB - 6, ah + 3)
    fill_mask(c, mo, (ax - 3, YB - 6 - ah - 3, ax + aw + 3, YB - 6), CAL[4])
    fill_mask(c, m, (ax, YB - 6 - ah, ax + aw, YB - 6), lambda x, y: (40, 32, 36) if y < YB - 34 else mix(FLOOR[0], (20, 14, 20), 0.35))
    for y in range(YB - 34, YB - 6):                              # piso da cozinha ao fundo (mais escuro)
        for x in range(ax, ax + aw):
            if m(x, y): c.pset(x, y, mix(FLOOR[1], (20, 14, 22), 0.55))
    for y in range(YB - 6 - ah, YB - 6):
        for x in range(ax, ax + aw):
            if m(x, y) and (y < YB - 6 - ah + 10 or x < ax + 3): c.pset(x, y, tuple(round(v * 0.7) for v in c.get(x, y)[:3]))
    c.vline(ax - 3, YB - 6 - ah // 2, ah // 2, CAL[4]); c.vline(ax + aw + 2, YB - 6 - ah // 2, ah // 2, CAL[1])
    # ---------------------------------------------------------------- janela para o quintal
    wx, wy, ww, wh = 252, YB - 29 - 41, 38, 41
    c.rect(wx - 3, wy - 3, ww + 6, wh + 6, CAL[4]); c.rect(wx + ww + 1, wy - 3, 2, wh + 6, CAL[2]); c.hline(wx - 3, wy + wh + 2, ww + 6, CAL[1])
    # vista: céu + muro ao longe + copa de mangueira
    for y in range(wy, wy + wh):
        for x in range(wx, wx + ww):
            c.pset(x, y, SKY_V(y - wy, wh))
    c.rect(wx, wy + 24, ww, 17, mix((200, 190, 170), (214, 222, 222), 0.3))        # muro vizinho em névoa
    c.hline(wx, wy + 24, ww, (222, 214, 196))
    for (cx_, cy_, rr) in [(wx + 8, wy + 30, 11), (wx + 24, wy + 27, 13), (wx + 34, wy + 34, 9), (wx + 14, wy + 38, 10)]:
        for dy in range(-rr, rr):
            for dx in range(-rr, rr + 1):
                if dx * dx + dy * dy <= rr * rr and wx <= cx_ + dx < wx + ww and wy <= cy_ + dy < wy + wh:
                    t = (dy / rr + dx / rr) * 0.5
                    c.pset(cx_ + dx, cy_ + dy, LEAF[3] if t < -0.35 else (LEAF[2] if t < 0.15 else LEAF[1]))
    for _ in range(14):                                                               # folhas isoladas na borda
        px_, py_ = wx + rng.randint(2, ww - 4), wy + rng.randint(22, 38)
        c.rect(px_, py_, 2, 1, LEAF[4]); c.pset(px_ + 1, py_ + 1, LEAF[1])
    # caixilho e vidros
    c.rect(wx, wy, ww, 2, WOOD[3]); c.rect(wx, wy, 2, wh, WOOD[3]); c.rect(wx + ww - 2, wy, 2, wh, WOOD[1]); c.rect(wx, wy + wh - 2, ww, 2, WOOD[1])
    c.vline(wx + ww // 2 - 1, wy, wh, WOOD[2]); c.vline(wx + ww // 2, wy, wh, WOOD[1])
    c.hline(wx, wy + 15, ww, WOOD[2]); c.hline(wx, wy + 16, ww, WOOD[1])
    c.poly([(wx + 3, wy + 13), (wx + 9, wy + 3), (wx + 12, wy + 3), (wx + 6, wy + 13)], (236, 242, 244))   # reflexo no vidro
    c.shade(wx + 2, wy + 2, ww - 4, 3, SH1); c.shade(wx + 2, wy + 2, 3, wh - 4, SH1)
    # peitoril de pedra e verga
    c.rect(wx - 5, wy + wh + 2, ww + 10, 3, STONE[4]); c.hline(wx - 5, wy + wh + 4, ww + 10, STONE[1])
    c.shade(wx - 4, wy + wh + 5, ww + 8, 3, SH2)
    # ---------------------------------------------------------------- nicho (arco pleno), vazio
    nx, nw, nh = 302, 26, 40
    nb = YB - 31 - 6
    mn = arch_mask(nx, nw, nb, nh)
    fill_mask(c, arch_mask(nx - 3, nw + 6, nb + 3, nh + 3), (nx - 3, nb - nh - 3, nx + nw + 3, nb + 3), CAL[4])
    fill_mask(c, mn, (nx, nb - nh, nx + nw, nb), CAL[2])
    for y in range(nb - nh, nb):
        for x in range(nx, nx + nw):
            if mn(x, y) and (x < nx + 3 or y < nb - nh + 6): c.pset(x, y, CAL[1])
    for y in range(nb - 6, nb):
        for x in range(nx, nx + nw): c.pset(x, y, CAL[1])
    c.rect(nx - 4, nb, nw + 8, 3, STONE[4]); c.hline(nx - 4, nb + 2, nw + 8, STONE[1]); c.shade(nx - 3, nb + 3, nw + 6, 3, SH2)
    # ---------------------------------------------------------------- porta para a escada (parede da direita)
    dx, dw, dh = 350, 30, 62
    y_f = YB - 6
    c.rect(dx - 3, YB - dh - 3 - 6 + 6, dw + 6, dh + 3, CAL[4]); c.vline(dx + dw + 2, YB - dh - 3, dh + 3 - 6 + 6, CAL[1])
    c.rect(dx, YB - dh - 6 + 6 - 0, dw, dh - 6 + 0, WOOD[2])
    for bx in range(dx + 3, dx + dw - 2, 5):
        c.vline(bx, YB - dh + 11, dh - 17, WOOD[1]); c.vline(bx + 1, YB - dh + 11, dh - 17, WOOD[3])
    c.rect(dx, YB - dh, dw, 10, (30, 24, 28))                              # bandeira escura
    for bx in range(dx + 2, dx + dw, 4): c.vline(bx, YB - dh, 10, IRON[3])
    c.hline(dx, YB - dh + 10, dw, WOOD[0])
    c.rect(dx + 3, YB - dh + 16, dw - 6, 16, WOOD[1]); c.hline(dx + 3, YB - dh + 16, dw - 6, WOOD[0]); c.vline(dx + 3, YB - dh + 16, 16, WOOD[0])
    c.rect(dx + 3, YB - dh + 36, dw - 6, 14, WOOD[1]); c.hline(dx + 3, YB - dh + 36, dw - 6, WOOD[0]); c.vline(dx + 3, YB - dh + 36, 14, WOOD[0])
    c.rect(dx + dw - 6, YB - dh + 30, 2, 3, IRON[4])
    c.shade(dx, YB - dh, dw, 2, SH2)
    c.rect(dx - 4, YB - 6, dw + 8, 3, STONE[4]); c.hline(dx - 4, YB - 4, dw + 8, STONE[1])
    # ---------------------------------------------------------------- forno de lenha embutido (massa de alvenaria + chaminé)
    ox, ow = 140, 82
    depth = 16
    top_front = YB + depth - 48            # frente 2,0 m
    # chaminé (afunila)
    for y in range(YT + 6, top_front - depth + 2):
        t = (y - (YT + 6)) / float(top_front - depth - YT - 4)
        w = int(26 + 26 * t)
        cx_ = ox + ow // 2
        c.hline(cx_ - w // 2, y, w, BRICK[2]); c.pset(cx_ - w // 2, y, BRICK[3]); c.pset(cx_ + w // 2 - 1, y, BRICK[1])
        if (y // 4) % 2 == 0:
            for xx in range(cx_ - w // 2 + 1, cx_ + w // 2 - 1, 9): c.pset(xx, y, BRICK[1])
    c.shade(ox + ow // 2 - 13, YT + 6, 26, 3, SH2)
    # face superior (laje de alvenaria)
    c.rect(ox - 2, top_front - depth, ow + 4, depth, CAL[3]); c.hline(ox - 2, top_front - depth, ow + 4, CAL[4])
    c.vline(ox - 2, top_front - depth, depth, CAL[4]); c.vline(ox + ow + 1, top_front - depth, depth, CAL[2])
    c.shade(ox + ow // 2 - 13, top_front - depth, 26, 5, SH1)
    # frente em tijolo aparente (fiadas de 4 px)
    c.rect(ox, top_front, ow, 48, BRICK[2])
    for r, y in enumerate(range(top_front, top_front + 48, 4)):
        c.hline(ox, y + 3, ow, BRICK[1])
        off = (r % 2) * 5
        for x in range(ox + off, ox + ow, 10):
            if x > ox: c.vline(x, y, 3, BRICK[1])
            col = rng.choice([BRICK[2], BRICK[2], BRICK[3], BRICK[1]])
            for i in range(1, 9):
                if x + i < ox + ow and c.get(x + i, y)[3]: 
                    for j in range(3): c.pset(x + i, y + j, col)
    c.hline(ox, top_front, ow, BRICK[4]); c.vline(ox, top_front, 48, BRICK[3]); c.vline(ox + ow - 1, top_front, 48, BRICK[1])
    c.hline(ox - 2, top_front, ow + 4, CAL[3]); c.hline(ox - 2, top_front + 1, ow + 4, CAL[2]); c.hline(ox - 2, top_front + 2, ow + 4, CAL[1])
    # boca do forno (arco) com aro de ferro
    mx, mw, mh = ox + ow // 2 - 17, 34, 25
    my = top_front + 48 - 9
    fill_mask(c, arch_mask(mx - 2, mw + 4, my, mh + 2), (mx - 2, my - mh - 2, mx + mw + 2, my), IRON[2])
    fill_mask(c, arch_mask(mx, mw, my, mh), (mx, my - mh, mx + mw, my), (24, 18, 20))
    for y in range(my - mh, my):
        for x in range(mx, mx + mw):
            if arch_mask(mx, mw, my, mh)(x, y) and y > my - 7 and 4 < x - mx < mw - 4: c.pset(x, y, (46, 28, 24))   # brasa apagada
    # soleira do forno (lábio de pedra) e base
    c.rect(mx - 6, my, mw + 12, 3, STONE[4]); c.hline(mx - 6, my + 2, mw + 12, STONE[1])
    c.rect(ox, top_front + 48 - 6, ow, 6, STONE[2]); c.hline(ox, top_front + 48 - 6, ow, STONE[4]); c.hline(ox, top_front + 47, ow, STONE[1])
    c.shade(ox + 1, top_front + 48, ow + 3, 6, SH3)          # sombra de contato no piso
    c.shade(ox + 4, top_front + 54, ow + 3, 4, SH2)
    return c, dict(oven=(ox - 2, top_front + 40, ow + 4, 14), mouth=(mx, my))

def SKY_V(y, h):
    t = y / float(h)
    cols = [(150, 190, 218), (176, 206, 224), (206, 222, 224), (232, 230, 212)]
    return cols[min(3, int(t * 4))]

def light_pass(c):
    """Luz que entra: janela de fundo (feixe no piso) e porta da frente (mancha quente)."""
    # feixe da janela (paralelogramo inclinado para a frente/esquerda), em duas faixas
    wx, ww = 252, 38
    for band, (amt, sh) in enumerate([(0.17, 26), (0.12, 0)]):
        pts = [(wx + 4 + sh, YB), (wx + ww - 2 + sh, YB), (wx + ww - 22 + sh, YB + 52 - sh // 2), (wx - 18 + sh, YB + 52 - sh // 2)]
        # só aplica sobre pixels de piso
        t = C(VW, VH); t.poly(pts, (255, 255, 255, 255))
        for y in range(YB, YB + 54):
            for x in range(wx - 24, wx + ww + 40):
                if t.p[x, y][3] and (band == 0 or True):
                    r, g, b, a = c.p[x, y]
                    inside2 = band == 1 and False
                    c.p[x, y] = (*mix((r, g, b), (255, 238, 190), amt + (0.06 if (x + y) % 2 == 0 and abs(x - (wx + 21)) > 17 and False else 0)), a)
    # mancha de luz da porta da frente (quente), junto à soleira
    dxc = (VW // 2)
    t = C(VW, VH); t.poly([(dxc - 26, YF - 1), (dxc + 26, YF - 1), (dxc + 40, YF - 38), (dxc - 12, YF - 38)], (255, 255, 255, 255))
    for y in range(YF - 40, YF):
        for x in range(dxc - 30, dxc + 46):
            if t.p[x, y][3]:
                r, g, b, a = c.p[x, y]
                amt = 0.20 if y > YF - 20 else 0.11
                c.p[x, y] = (*mix((r, g, b), (255, 226, 170), amt), a)

def frame_room(c):
    # paredes laterais em corte (topo + face da ponta) e topo da parede de fundo
    L0, L1 = 60, 72; R0, R1 = 408, 420
    for (xa, xb, light) in [(L0, L1, True), (R0, R1, False)]:
        c.rect(xa, 20, xb - xa, 237 - 0, CAL[2] if light else CAL[1])
        c.rect(xa, 20, xb - xa, 136, CAL[3] if light else CAL[2])             # topo (frechal visto de cima)
        c.hline(xa, 156, xb - xa, CAL[1] if light else CAL[0])
        c.vline(xa, 20, 237, CAL[4] if light else CAL[2]); c.vline(xb - 1, 20, 237, CAL[1] if light else CAL[0])
        # base de pedra na ponta
        c.rect(xa, 232, xb - xa, 25, STONE[2]); c.hline(xa, 232, xb - xa, STONE[3])
    c.rect(L0, 20, R1 - L0, 8, CAL[3]); c.hline(L0, 20, R1 - L0, CAL[4]); c.hline(L0, 27, R1 - L0, CAL[1])
    # embasamento frontal baixo com vão da porta (52 px = 2,2 m)
    door0, door1 = VW // 2 - 26, VW // 2 + 26
    for (xa, xb) in [(L1, door0), (door1, R0)]:
        c.rect(xa, YF, xb - xa, 10, STONE[2]); c.hline(xa, YF, xb - xa, STONE[4]); c.hline(xa, YF + 1, xb - xa, STONE[3]); c.hline(xa, YF + 9, xb - xa, STONE[0])
        for x in range(xa, xb, 17): c.vline(x, YF + 2, 7, STONE[1])
    # soleira
    c.rect(door0 - 1, YF, door1 - door0 + 2, 6, STONE[4]); c.hline(door0 - 1, YF + 5, door1 - door0 + 2, STONE[1])
    c.vline(door0 - 1, YF, 10, STONE[1]); c.vline(door1, YF, 10, STONE[1])
    c.shade(L1, YF + 10, R0 - L1, 4, SH3)

def build_counter():
    """Balcão em L (frente + retorno à direita) como camada própria: personagem passa atrás ou na frente."""
    c = C(VW, VH)
    cx0, cx1 = 132, 312; rx1 = 334        # frente 7,5 m + retorno de 0,9 m
    front_y0, front_y1 = 156, 180          # face frontal (1,0 m)
    top_y0 = 142                           # aresta de trás do tampo (profundidade 0,9 m = 14 px)
    # sombra projetada no piso (alfa)
    for y in range(front_y1, front_y1 + 5):
        for x in range(cx0 + 2, rx1 + 3): c.pset(x, y, (20, 12, 30, 120 if y < front_y1 + 3 else 70))
    # retorno: tampo em faixa vertical até a parede de fundo
    c.rect(cx1, 100, rx1 - cx1, front_y0 - 104, CAL[3]); c.vline(cx1, 100, front_y0 - 104, CAL[4]); c.vline(rx1 - 1, 100, front_y0 - 104, CAL[2]); c.hline(cx1, 100, rx1 - cx1, CAL[4])
    # tampo (mármore claro com bordas)
    c.rect(cx0, top_y0, rx1 - cx0, front_y0 - top_y0, CAL[3])
    c.hline(cx0, top_y0, rx1 - cx0, CAL[4]); c.hline(cx0, front_y0 - 4, rx1 - cx0, CAL[4])
    c.rect(cx0, front_y0 - 3, rx1 - cx0, 3, CAL[2]); c.hline(cx0, front_y0 - 1, rx1 - cx0, CAL[1])
    c.vline(cx0, top_y0, front_y0 - top_y0, CAL[4])
    rng = random.Random(3)
    for k in range(6):                                          # veios de mármore
        x = cx0 + rng.randint(8, rx1 - cx0 - 30); y = top_y0 + rng.randint(3, 10)
        c.line(x, y, x + rng.randint(10, 22), y + rng.randint(-2, 2), CAL[2])
    # frente de madeira pintada com almofadas
    c.rect(cx0, front_y0, rx1 - cx0, front_y1 - front_y0, WOOD[2])
    c.hline(cx0, front_y0, rx1 - cx0, WOOD[4]); c.hline(cx0, front_y0 + 1, rx1 - cx0, WOOD[3])
    for x in range(cx0 + 4, rx1 - 12, 36):
        c.rect(x, front_y0 + 4, 32, 14, WOOD[1]); c.hline(x, front_y0 + 4, 32, WOOD[0]); c.vline(x, front_y0 + 4, 14, WOOD[0])
        c.hline(x + 1, front_y0 + 18, 31, WOOD[3]); c.vline(x + 31, front_y0 + 4, 14, WOOD[3])
    c.rect(cx0, front_y1 - 4, rx1 - cx0, 4, WOOD[0])             # rodapé do balcão
    c.vline(cx0, front_y0, front_y1 - front_y0, WOOD[3]); c.vline(rx1 - 1, front_y0, front_y1 - front_y0, WOOD[1])
    c.shade(cx0 + 1, front_y0 + 2, rx1 - cx0 - 2, 2, SH1)        # sombra sob a quina do tampo
    return c

if __name__ == '__main__':
    base, info = build_base()
    light_pass(base); frame_room(base)
    base.save('../assets/bakery_interior_base.png')
    cn = build_counter(); cn.save('../assets/bakery_counter.png')
    comp = base.im.copy(); comp.alpha_composite(cn.im)
    comp.save('../preview/interior_raw.png')
    comp.resize((VW * 2, VH * 2), Image.NEAREST).save('../preview/interior_x2.png') if False else None
    from PIL import Image
    comp.resize((VW * 2, VH * 2), Image.NEAREST).save('../preview/interior_x2.png')
    print(info)

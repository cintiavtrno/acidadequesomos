"""Casa de Seu Raimundo (Etapa 5 · Fase A) — sala-cozinha-quarto do sobrado amarelo, câmera 3/4 (1 m = 24 px; piso 16 px/m).
Gera: assets/casa_interior_base.png, assets/objects/casa_objetos.png, assets/objects/catalog_casa.json, assets/objects/scene_casa.json."""
import json, math, random
from PIL import Image
from pxl import *
from facade import CAL, STONE, BRICK, IRON
from interior import (VW, VH, X0, X1, CAP, YT, YB, YF, TIMB, WOOD, LEAF, STRAW, BREAD, CLAY, RED, SACK, VOID, BARRA, arch_mask, fill_mask, ell, SKY_V, frame_room)
import objlib as O
from objlib import shadow, CELL, AXY, new, ALU, ENAM

OUT = '../assets/objects/'
AMAR = ramp(46, 0.58, (0.36, 0.48, 0.60, 0.71, 0.80))        # reboco amarelo envelhecido (a casa amarela)
AZUL = ramp(196, 0.24, (0.30, 0.38, 0.47, 0.56, 0.66))       # barra desbotada
ASSO = ramp(26, 0.36, (0.27, 0.33, 0.40, 0.47, 0.54))        # assoalho de tábua corrida
RUG = [(138, 74, 62), (192, 156, 92), (104, 124, 112), (206, 198, 176), (84, 104, 128), (164, 112, 82)]

# ------------------------------------------------------------------ cenário-base
def build_base(seed=11):
    rng = random.Random(seed); c = C(VW, VH, VOID + (255,))
    # assoalho: tábuas de 0,25 m (4 px) correndo no sentido da largura, juntas escalonadas
    for ty in range((YF - YB) // 4 + 1):
        y = YB + ty * 4; x = X0 - rng.randint(0, 30)
        while x < X1:
            w = rng.choice((38, 46, 54, 62)); col = rng.choice([ASSO[2]] * 6 + [ASSO[3]] * 2 + [mix(ASSO[2], ASSO[1], .5)] * 2)
            xa, xb = max(x, X0), min(x + w, X1)
            if xb > xa:
                c.rect(xa, y, xb - xa, 4, col); c.hline(xa, y, xb - xa, mix(col, (255, 232, 190), .10)); c.hline(xa, y + 3, xb - xa, mix(col, (24, 14, 34), .30))
                if x >= X0: c.vline(x, y, 4, mix(col, (24, 14, 34), .38))
                for _ in range(rng.randint(0, 2)): c.hline(xa + rng.randint(2, max(3, xb - xa - 8)), y + 1, rng.randint(3, 7), mix(col, (24, 14, 34), .10))   # veio da madeira
            x += w
    c.rect(X0, YF, X1 - X0, 12, VOID + (255,))
    draw_rug(c, 130, 170, 202, 58)                                  # tapete têxtil sob a mesa de convivência
    # trilho de uso: porta -> fogão/mesa (tábuas mais claras pelo gasto)
    for yy in range(YF - 70, YF):
        for xx in range(214, 270):
            r, g, b, a = c.get(xx, yy)
            if a and yy < YF: c.pset(xx, yy, mix((r, g, b), (240, 206, 160), .07))
    c.shade(X0, YB, 7, YF - YB, SH1); c.shade(X1 - 7, YB, 7, YF - YB, SH1); c.shade(X0, YB, 3, YF - YB, SH2); c.shade(X1 - 3, YB, 3, YF - YB, SH2)
    c.shade(X0, YB, X1 - X0, 2, SH3); c.shade(X0, YB + 2, X1 - X0, 3, SH2); c.shade(X0, YB + 5, X1 - X0, 3, SH1)
    # parede de fundo: reboco amarelo, barra azul desbotada, rodapé de madeira, viga no alto
    c.rect(X0, YT, X1 - X0, YB - YT, AMAR[3]); c.rect(X0, YT, X1 - X0, 8, AMAR[2]); c.shade(X0, YT + 8, X1 - X0, 6, SH1)
    by = YB - 30
    c.rect(X0, by, X1 - X0, 24, AZUL[2]); c.hline(X0, by, X1 - X0, AZUL[4]); c.hline(X0, by + 1, X1 - X0, AZUL[3]); c.hline(X0, by + 2, X1 - X0, AZUL[1]); c.hline(X0, by - 1, X1 - X0, AMAR[1])
    c.rect(X0, YB - 6, X1 - X0, 6, TIMB[2]); c.hline(X0, YB - 6, X1 - X0, TIMB[4]); c.hline(X0, YB - 5, X1 - X0, TIMB[3]); c.hline(X0, YB - 1, X1 - X0, TIMB[0])
    # desgaste localizado: reboco caído perto do telhado (mostra o tijolo) e umidade na barra
    for (px, py, rx, ry) in ((100, YT + 17, 6, 4), (396, YT + 24, 4, 6)):
        patch(c, px, py, rx, ry, mix(BRICK[2], AMAR[2], .5), rng, clip=lambda x, y: YT + 8 <= y < by - 4)
        patch(c, px - 1, py - 1, rx - 2, ry - 2, mix(BRICK[3], AMAR[3], .45), rng, clip=lambda x, y: YT + 8 <= y < by - 4)
    def damp(xa, wa, ha):
        for i in range(wa):
            hh = ha + int(3 * math.sin(i / 5.0 + xa) + rng.randint(-1, 1))
            for j in range(hh):
                x, y = xa + i, by - 2 - j; r, g, b, a = c.get(x, y); c.pset(x, y, tuple(round(v * f) for v, f in zip((r, g, b), SH1 if j < hh - 1 else SH2)))
    damp(X0 + 6, 30, 7); damp(214, 20, 5)
    c.rect(X0, YT, X1 - X0, 6, TIMB[2]); c.hline(X0, YT, X1 - X0, TIMB[4]); c.hline(X0, YT + 1, X1 - X0, TIMB[3]); c.hline(X0, YT + 5, X1 - X0, TIMB[1])
    for x in range(X0 + 9, X1, 23): c.vline(x, YT + 2, 3, TIMB[1])
    c.shade(X0, YT + 6, X1 - X0, 2, SH3); c.shade(X0, YT + 8, 6, YB - YT - 8, SH1); c.shade(X1 - 6, YT + 8, 6, YB - YT - 8, SH1)

    # ---- porta-janela da sacada (duas folhas de veneziana verde-musgo, uma entreaberta) e vista da rua
    wx, ww, wt, wb = 224, 64, 46, YB - 6; wh = wb - wt
    c.rect(wx - 4, wt - 4, ww + 8, wh + 4, AMAR[4]); c.rect(wx + ww + 2, wt - 4, 2, wh + 4, AMAR[2]); c.hline(wx - 4, wt - 4, ww + 8, AMAR[4])
    for y in range(wt, wb):
        for x in range(wx, wx + ww): c.pset(x, y, SKY_V(y - wt, wh))
    # fachada em frente (rosa) com telhado, vista de relance
    c.rect(wx, wt + 26, ww, wh - 26, mix((214, 150, 140), (236, 214, 200), .1)); c.rect(wx, wt + 20, ww, 6, (176, 84, 58)); c.hline(wx, wt + 20, ww, (210, 120, 78)); c.hline(wx, wt + 25, ww, (120, 54, 44))
    for fx in (wx + 8, wx + 34, wx + 52):
        c.rect(fx, wt + 32, 7, 13, (70, 96, 90)); c.hline(fx, wt + 32, 7, (232, 226, 210)); c.vline(fx + 3, wt + 32, 13, (46, 66, 62))
    # folhas: esquerda fechada (veneziana), direita entreaberta (vista de perfil, estreita)
    lw = ww // 2
    c.rect(wx, wt, lw - 1, wh, WOOD[2]); c.rect(wx, wt, 2, wh, WOOD[3]); c.rect(wx + lw - 3, wt, 2, wh, WOOD[1])
    for y in range(wt + 4, wb - 4, 3):
        c.hline(wx + 3, y, lw - 7, WOOD[3]); c.hline(wx + 3, y + 1, lw - 7, WOOD[1])
    c.rect(wx, wt + wh // 2 - 1, lw - 1, 3, WOOD[2]); c.hline(wx, wt + wh // 2 - 1, lw - 1, WOOD[4])
    c.poly([(wx + ww - 10, wt), (wx + ww, wt + 4), (wx + ww, wb), (wx + ww - 10, wb - 5)], WOOD[1])
    c.vline(wx + ww - 10, wt, wh - 4, WOOD[3]); c.vline(wx + ww - 1, wt + 4, wh - 4, WOOD[0])
    for y in range(wt + 6, wb - 8, 4): c.line(wx + ww - 9, y, wx + ww - 1, y + 3, WOOD[0])
    c.vline(wx + lw - 1, wt, wh, WOOD[0]); c.rect(wx + lw - 5, wt + wh // 2 + 2, 2, 5, IRON[4])
    # guarda-corpo de ferro da sacada (por dentro da porta aberta, na frente do vão)
    for gx in range(wx + lw + 1, wx + ww - 9, 4): c.vline(gx, wb - 22, 22, IRON[1]); c.pset(gx, wb - 23, IRON[4])
    c.hline(wx + lw + 1, wb - 22, ww - lw - 10, IRON[3]); c.hline(wx + lw + 1, wb - 8, ww - lw - 10, IRON[2])
    c.shade(wx, wt, ww, 3, SH1); c.rect(wx - 6, wb, ww + 12, 4, STONE[4]); c.hline(wx - 6, wb + 3, ww + 12, STONE[1]); c.shade(wx - 4, wb + 4, ww + 8, 3, SH2)
    # vaso de samambaia pendurado no batente
    c.vline(wx - 3, wt, 14, IRON[3]); ell(c, wx - 3, wt + 16, 5, 3, CLAY[2]); c.hline(wx - 8, wt + 14, 10, CLAY[4])
    for k in range(7):
        a = math.radians(-80 + k * 26); L = 8 + (k % 3) * 2; c.line(wx - 3, wt + 15, wx - 3 + int(math.sin(a) * L), wt + 15 + int(abs(math.cos(a)) * L * .9) + 3, LEAF[2 + k % 3])
    # lâmpada nua pendurada do forro (luz de uso diário)
    lx = 176; c.vline(lx, YT + 6, 14, IRON[1]); c.rect(lx - 1, YT + 20, 3, 3, IRON[3]); ell(c, lx, YT + 25, 3, 3.4, (252, 232, 170)); c.pset(lx - 1, YT + 24, (255, 252, 226))
    for r_, a_ in ((7, .10), (12, .06)):
        for y in range(YT + 8, YT + 44):
            for x in range(lx - 14, lx + 15):
                if (x - lx) ** 2 + (y - (YT + 25)) ** 2 <= r_ * r_ and c.get(x, y)[3]:
                    rr, gg, bb, aa = c.get(x, y); c.pset(x, y, mix((rr, gg, bb), (255, 232, 170), a_))
    # prego da sacola e do chapéu marcado na parede (os objetos são sprites)
    return c

def light_pass(c):
    wx, ww = 224, 64
    for band, (amt, sh) in enumerate([(0.19, 30), (0.12, 0)]):
        pts = [(wx + 6 + sh, YB + 18), (wx + ww - 6 + sh, YB + 18), (wx + ww - 30 + sh, YB + 62 - sh // 2), (wx - 20 + sh, YB + 62 - sh // 2)]
        t = C(VW, VH); t.poly(pts, (255, 255, 255, 255))
        for y in range(YB + 16, YB + 64):
            for x in range(wx - 30, wx + ww + 60):
                if t.p[x, y][3]:
                    r, g, b, a = c.p[x, y]; c.p[x, y] = (*mix((r, g, b), (255, 238, 190), amt), a)
    dxc = VW // 2; t = C(VW, VH); t.poly([(dxc - 26, YF - 1), (dxc + 26, YF - 1), (dxc + 40, YF - 38), (dxc - 12, YF - 38)], (255, 255, 255, 255))
    for y in range(YF - 40, YF):
        for x in range(dxc - 30, dxc + 46):
            if t.p[x, y][3]:
                r, g, b, a = c.p[x, y]; c.p[x, y] = (*mix((r, g, b), (255, 226, 170), 0.20 if y > YF - 20 else 0.11), a)

# ------------------------------------------------------------------ objetos (âncora = pés, centro do contato com o chão)
def box(c, x0, y0, w, h, cols, side=0):
    c.rect(x0, y0, w, h, cols[2]); c.hline(x0, y0, w, cols[4]); c.vline(x0, y0, h, cols[3]); c.vline(x0 + w - 1, y0, h, cols[1]); c.hline(x0, y0 + h - 1, w, cols[1])

def d_mesa(c, x, y):      # mesa quadrada 1,25 x 0,8 m com toalha de crochê; y = frente do pé
    w = 30; x0 = x - w // 2; shadow(c, x, y + 1, w + 2)
    for lx in (x0 + 1, x0 + w - 3): c.rect(lx, y - 14, 2, 14, TIMB[2]); c.vline(lx, y - 14, 14, TIMB[3])
    for lx in (x0 + 4, x0 + w - 6): c.rect(lx, y - 20, 2, 7, TIMB[1])                       # pés de trás
    c.rect(x0, y - 31, w, 13, TIMB[3]); c.hline(x0, y - 31, w, TIMB[4]); c.vline(x0, y - 31, 13, TIMB[4]); c.vline(x0 + w - 1, y - 31, 13, TIMB[2])
    c.rect(x0, y - 18, w, 3, TIMB[2]); c.hline(x0, y - 18, w, TIMB[4]); c.hline(x0, y - 16, w, TIMB[1])
    # toalha branca com barrado azul; caída na frente
    c.rect(x0 + 1, y - 30, w - 2, 12, SACK[3]); c.hline(x0 + 1, y - 30, w - 2, SACK[4])
    c.rect(x0 + 1, y - 19, w - 2, 5, SACK[3]); c.hline(x0 + 1, y - 15, w - 2, WOOD[3])
    for k in range(x0 + 2, x0 + w - 2, 3): c.pset(k, y - 14, SACK[3]); c.pset(k, y - 13, SACK[2])
    for k in range(x0 + 3, x0 + w - 3, 4): c.pset(k, y - 17, WOOD[3]); c.pset(k + 1, y - 17, WOOD[2])
    c.hline(x0 + 1, y - 29, w - 2, mix(SACK[3], WOOD[3], .55)); c.vline(x0 + 1, y - 29, 11, SACK[2]); c.vline(x0 + w - 2, y - 29, 11, SACK[1])
    c.shade(x0 + 1, y - 14, w - 2, 3, SH1)

def d_caixa_domino(c, x, y):   # y = tampo
    c.rect(x - 5, y - 4, 10, 4, TIMB[2]); c.hline(x - 5, y - 4, 10, TIMB[4]); c.vline(x - 5, y - 4, 4, TIMB[3]); c.vline(x + 4, y - 4, 4, TIMB[1])
    c.rect(x - 4, y - 6, 8, 2, TIMB[3]); c.hline(x - 4, y - 6, 8, TIMB[4]); c.pset(x, y - 3, (214, 190, 120))
    for k, (dx, dy) in enumerate(((7, -1), (9, -2), (8, 0))): c.rect(x + dx, y + dy - 2, 3, 2, SACK[4]); c.pset(x + dx, y + dy - 2, IRON[1]); c.pset(x + dx + 2, y + dy - 2, IRON[1])

def d_cesto_pao(c, x, y):
    ell(c, x, y - 3, 7, 3, STRAW[2]); c.rect(x - 7, y - 4, 15, 4, STRAW[2]); c.hline(x - 7, y - 4, 15, STRAW[4]); c.hline(x - 7, y - 1, 15, STRAW[1])
    c.rect(x - 6, y - 7, 13, 4, SACK[3]); c.hline(x - 6, y - 7, 13, SACK[4]); c.pset(x - 3, y - 5, RED[3]); c.pset(x + 2, y - 5, RED[3])
    c.line(x - 6, y - 7, x - 7, y - 4, SACK[2]); c.line(x + 6, y - 7, x + 7, y - 4, SACK[2]); ell(c, x + 1, y - 8, 4, 1.6, BREAD[3]); c.hline(x - 2, y - 9, 4, BREAD[4])

def d_cadeira_balanco(c, x, y):    # vista de costas (encosto de palhinha) voltada para a janela
    w = 22; x0 = x - w // 2; shadow(c, x, y, w + 4)
    for lx in (x0 + 2, x0 + w - 5): c.rect(lx, y - 14, 3, 14, TIMB[2]); c.vline(lx, y - 14, 14, TIMB[3])
    c.rect(x0 - 1, y - 12, w + 2, 3, TIMB[2]); c.hline(x0 - 1, y - 12, w + 2, TIMB[4])           # braços
    c.rect(x0 + 1, y - 40, w - 2, 28, TIMB[2]); c.hline(x0 + 1, y - 40, w - 2, TIMB[4]); c.vline(x0 + 1, y - 40, 28, TIMB[3]); c.vline(x0 + w - 2, y - 40, 28, TIMB[1])
    c.rect(x0 + 4, y - 36, w - 8, 20, STRAW[2]); c.hline(x0 + 4, y - 36, w - 8, STRAW[4])
    for k in range(0, 20, 2): c.hline(x0 + 4, y - 35 + k, w - 8, STRAW[3] if k % 4 == 0 else STRAW[1])
    for k in range(0, w - 8, 2): c.vline(x0 + 4 + k, y - 36, 20, STRAW[1] if k % 4 == 0 else STRAW[3])
    c.rect(x0 + 3, y - 15, w - 6, 3, TIMB[1])
    c.line(x0 - 3, y - 1, x0 + 4, y + 2, TIMB[3]); c.hline(x0 + 4, y + 2, w - 8, TIMB[3]); c.line(x0 + w - 5, y + 2, x0 + w + 2, y - 1, TIMB[3])   # balanços (patins)
    c.hline(x0 + 4, y + 3, w - 8, TIMB[0]); c.pset(x0 + w - 6, y + 3, TIMB[0])
    c.rect(x0 + 5, y - 3, 3, 3, TIMB[1]); c.rect(x0 + w - 8, y - 3, 3, 3, TIMB[1])

def d_armario(c, x, y):    # guarda-roupa de duas portas, espelho na porta esquerda
    w, h = 34, 54; x0 = x - w // 2; shadow(c, x, y, w + 3)
    c.rect(x0 + 2, y - 3, 3, 3, TIMB[1]); c.rect(x0 + w - 5, y - 3, 3, 3, TIMB[1])
    c.rect(x0, y - h, w, h - 3, TIMB[2]); c.hline(x0, y - h, w, TIMB[4]); c.vline(x0, y - h, h - 3, TIMB[3]); c.vline(x0 + w - 1, y - h, h - 3, TIMB[1])
    c.rect(x0 - 1, y - h - 3, w + 2, 4, TIMB[3]); c.hline(x0 - 1, y - h - 3, w + 2, TIMB[4]); c.hline(x0 - 1, y - h, w + 2, TIMB[0])
    for dx0 in (x0 + 2, x0 + w // 2 + 1):
        c.rect(dx0, y - h + 4, w // 2 - 3, h - 11, TIMB[1]); c.rect(dx0 + 1, y - h + 5, w // 2 - 5, h - 13, TIMB[3]); c.hline(dx0 + 1, y - h + 5, w // 2 - 5, TIMB[4])
    # espelho
    mx, my, mw, mh = x0 + 4, y - h + 7, w // 2 - 7, 22
    c.rect(mx, my, mw, mh, (150, 180, 196)); c.poly([(mx + 1, my + mh - 2), (mx + 6, my + 1), (mx + 8, my + 1), (mx + 3, my + mh - 2)], (200, 224, 232)); c.hline(mx, my, mw, (112, 138, 156))
    c.rect(x0 + w // 2 - 1, y - h + 4, 2, h - 11, TIMB[0]); c.rect(x0 + w // 2 - 3, y - h // 2 + 2, 1, 4, BREAD[3]); c.rect(x0 + w // 2 + 2, y - h // 2 + 2, 1, 4, BREAD[3])
    c.shade(x0, y - 3 - 4, w, 4, SH1)

def d_cama(c, x, y):       # cama de solteiro, cabeceira na parede de fundo; y = frente do pé
    w, dep = 28, 33; x0 = x - w // 2; shadow(c, x + 1, y, w + 4)
    top = y - 12                                                     # altura do colchão (0,5 m)
    c.rect(x0, top - dep - 20, w, 22, TIMB[2]); c.hline(x0, top - dep - 20, w, TIMB[4]); c.vline(x0, top - dep - 20, 22, TIMB[3]); c.vline(x0 + w - 1, top - dep - 20, 22, TIMB[1])
    for k in range(3): c.vline(x0 + 4 + k * 9, top - dep - 17, 14, TIMB[1])                      # balaústres da cabeceira
    c.rect(x0, top - dep, w, dep, SACK[2])                                                         # lençol (plano do colchão)
    c.rect(x0 + 3, top - dep + 1, w - 6, 8, SACK[4]); c.hline(x0 + 3, top - dep + 1, w - 6, (255, 252, 240)); c.hline(x0 + 3, top - dep + 8, w - 6, SACK[2])   # travesseiro
    # colcha de retalhos: quadrados 6x6 em tons pastel envelhecidos
    k = 0                                                            # colcha: 4 colunas de retalhos de 6 px, recuadas 2 px; as laterais caem sobre a cama (sem vazar da borda)
    for gy in range(top - dep + 11, top - 1, 5):
        hh = min(5, top - 1 - gy)
        for gx in range(x0 + 2, x0 + w - 2, 6):
            col = RUG[(k * 5 + k // 3) % len(RUG)]; col = mix(col, (236, 224, 200), .25); k += 1
            c.rect(gx, gy, 6, hh, col); c.hline(gx, gy, 6, mix(col, (255, 244, 220), .18))
            if hh == 5: c.hline(gx, gy + 4, 6, mix(col, (30, 20, 40), .28))
            c.vline(gx + 5, gy, hh, mix(col, (30, 20, 40), .22))
    for gy in range(top - dep + 11, top - 1):                        # queda lateral da colcha (dobra sombreada) e barra de pano
        c.pset(x0, gy, mix(RUG[(gy // 5) % len(RUG)], (60, 44, 52), .45)); c.pset(x0 + 1, gy, mix(RUG[(gy // 5) % len(RUG)], (120, 100, 96), .3))
        c.pset(x0 + w - 1, gy, mix(RUG[(gy // 5 + 2) % len(RUG)], (30, 20, 40), .55)); c.pset(x0 + w - 2, gy, mix(RUG[(gy // 5 + 2) % len(RUG)], (60, 44, 52), .35))
    c.hline(x0 + 2, top - dep + 10, w - 4, SACK[2])                  # dobra do lençol sob a colcha
    c.rect(x0, top - 1, w, 3, TIMB[3]); c.hline(x0, top - 1, w, TIMB[4])                          # beira da colcha/estrado
    c.rect(x0 - 1, top + 2, w + 2, 10, TIMB[2]); c.hline(x0 - 1, top + 2, w + 2, TIMB[4]); c.hline(x0 - 1, y - 1, w + 2, TIMB[0])           # peseira
    for lx in (x0, x0 + w - 3): c.rect(lx, y - 12, 3, 12, TIMB[2]); c.vline(lx, y - 12, 12, TIMB[3])
    c.shade(x0 + 1, top + 4, w - 2, 3, SH1)

def d_criado(c, x, y):     # criado-mudo com rádio de pilha e óculos
    w = 13; x0 = x - w // 2; shadow(c, x, y, w + 3)
    c.rect(x0 + 1, y - 3, 2, 3, TIMB[1]); c.rect(x0 + w - 3, y - 3, 2, 3, TIMB[1])
    c.rect(x0, y - 17, w, 14, TIMB[2]); c.hline(x0, y - 17, w, TIMB[4]); c.vline(x0, y - 17, 14, TIMB[3]); c.vline(x0 + w - 1, y - 17, 14, TIMB[1])
    c.rect(x0 + 2, y - 14, w - 4, 5, TIMB[3]); c.hline(x0 + 2, y - 14, w - 4, TIMB[4]); c.pset(x, y - 12, BREAD[3])
    c.rect(x0 + 2, y - 8, w - 4, 4, TIMB[1])
    c.rect(x0 + 1, y - 24, 9, 7, IRON[2]); c.hline(x0 + 1, y - 24, 9, IRON[4]); c.rect(x0 + 2, y - 22, 4, 3, STRAW[3]); c.pset(x0 + 8, y - 22, STRAW[4]); c.line(x0 + 8, y - 24, x0 + 10, y - 27, IRON[4])
    c.rect(x0 + 10, y - 19, 2, 1, IRON[4]); c.pset(x0 + 11, y - 18, IRON[4])      # óculos dobrados

def d_talha(c, x, y):      # talha de barro com tampa de madeira e caneca esmaltada
    shadow(c, x, y, 18)
    for dx in (-5, 5): c.line(x + dx, y, x + dx // 2, y - 8, TIMB[2])
    c.hline(x - 6, y - 8, 12, TIMB[3])
    c.poly([(x - 7, y - 24), (x + 7, y - 24), (x + 8, y - 15), (x + 5, y - 8), (x - 5, y - 8), (x - 8, y - 15)], CLAY[2])
    c.vline(x - 7, y - 22, 12, CLAY[4]); c.vline(x - 6, y - 21, 10, CLAY[3]); c.vline(x + 7, y - 22, 11, CLAY[1]); c.hline(x - 6, y - 15, 13, CLAY[3]); c.hline(x - 5, y - 9, 11, CLAY[1])
    c.rect(x - 7, y - 26, 14, 3, CLAY[3]); c.hline(x - 7, y - 26, 14, CLAY[4]); c.rect(x - 5, y - 29, 10, 3, TIMB[3]); c.hline(x - 5, y - 29, 10, TIMB[4]); c.pset(x, y - 30, TIMB[1])
    c.rect(x + 8, y - 12, 4, 5, ENAM[3]); c.hline(x + 8, y - 12, 4, ENAM[4]); c.pset(x + 12, y - 11, ENAM[3]); c.pset(x + 12, y - 9, ENAM[3])

def d_oratorio(c, x, y):   # y = base do oratório (parede); porta aberta, imagem do Bonfim, fitas
    w, h = 24, 36; x0 = x - w // 2
    box(c, x0, y - h, w, h, TIMB); c.rect(x0 - 1, y - h - 2, w + 2, 3, TIMB[3]); c.hline(x0 - 1, y - h - 2, w + 2, TIMB[4])
    c.rect(x0 + 2, y - h + 3, w - 4, h - 12, (88, 112, 128)); c.shade(x0 + 2, y - h + 3, w - 4, 3, SH2); c.shade(x0 + 2, y - h + 3, 3, h - 12, SH1)
    fx, fy_ = x0 + 7, y - h + 5                                       # estampa: figura de manto e braços abertos sobre fundo claro
    c.rect(fx, fy_, 10, 15, (216, 200, 160)); c.hline(fx, fy_, 10, TIMB[4]); c.rect(fx - 1, fy_ - 1, 12, 17, TIMB[1]); c.rect(fx, fy_, 10, 15, (216, 200, 160))
    c.rect(fx + 3, fy_ + 2, 4, 3, (200, 150, 112)); c.poly([(fx + 5, fy_ + 5), (fx + 1, fy_ + 14), (fx + 9, fy_ + 14)], (92, 124, 168)); c.rect(fx + 4, fy_ + 6, 2, 3, (232, 226, 210)); c.pset(fx + 4, fy_ + 1, (226, 190, 80)); c.pset(fx + 5, fy_ + 1, (226, 190, 80))
    c.rect(x0 + 2, y - 10, w - 4, 2, TIMB[3]); c.hline(x0 + 2, y - 10, w - 4, TIMB[4])
    c.poly([(x0 - 7, y - h + 2), (x0 + 1, y - h + 4), (x0 + 1, y - 8), (x0 - 7, y - 6)], TIMB[1]); c.line(x0 - 7, y - h + 2, x0 - 7, y - 6, TIMB[3])   # porta aberta (vista de lado)
    # fitas do Bonfim penduradas na porta
    for k, col in enumerate(((70, 130, 170), (214, 170, 60), (180, 70, 66), (226, 226, 214), (96, 150, 110))):
        c.vline(x0 - 6 + (k % 2), y - h + 6 + k, 9 + (k % 3) * 2, col)
    # prateleirinha com flor
    c.rect(x0 - 1, y - 8, w + 2, 3, TIMB[3]); c.hline(x0 - 1, y - 8, w + 2, TIMB[4]); c.hline(x0 - 1, y - 6, w + 2, TIMB[0]); c.shade(x0, y - 5, w + 2, 3, SH2)
    c.rect(x0 + w - 8, y - 14, 5, 6, CLAY[2]); c.hline(x0 + w - 8, y - 14, 5, CLAY[4]); c.vline(x0 + w - 6, y - 19, 5, LEAF[2]); c.rect(x0 + w - 7, y - 21, 2, 2, SACK[4]); c.rect(x0 + w - 5, y - 20, 2, 2, RED[3])

def d_vela_oratorio(c, x, y, f):   # x,y = ponta do pavio
    c.pset(x, y, (255, 150, 60) if f == 0 else (255, 120, 50)); c.pset(x, y - 1, (255, 222, 130)); c.pset(x + (f), y - 2, (255, 190, 90)) if f else c.pset(x, y - 2, (255, 190, 90))
    c.rect(x - 1, y + 1, 3, 6, SACK[3]); c.vline(x - 1, y + 1, 6, SACK[4]); c.vline(x + 1, y + 1, 6, SACK[1]); c.pset(x, y, IRON[1]) if False else None

def d_retrato_mae(c, x, y):   # moldura oval sépia: a mãe, de lenço branco na cabeça; y = base
    w, h = 16, 21; x0 = x - w // 2
    ell(c, x, y - h // 2, w / 2 + 1, h / 2 + 1, TIMB[2]); ell(c, x, y - h // 2, w / 2 - 1, h / 2 - 1, TIMB[4]); ell(c, x, y - h // 2, w / 2 - 2, h / 2 - 2, (196, 170, 128))
    ell(c, x, y - h // 2 - 2, 3.5, 4, (172, 128, 96)); ell(c, x, y - h // 2 - 4, 5, 3.5, (236, 228, 208)); c.hline(x - 5, y - h // 2 - 2, 10, (214, 202, 178))      # rosto e lenço
    c.poly([(x - 7, y - 2), (x - 4, y - h // 2 + 2), (x + 4, y - h // 2 + 2), (x + 7, y - 2)], (104, 86, 90)); c.hline(x - 3, y - h // 2 + 2, 6, (226, 214, 190))
    c.pset(x - 1, y - h // 2 - 2, (60, 40, 36)); c.pset(x + 1, y - h // 2 - 2, (60, 40, 36)); c.pset(x, y - h // 2, (150, 80, 70))
    c.pset(x, y - h - 1, IRON[3])

def d_foto_forno(c, x, y):    # fotografia pequena: a boca do forno de lenha e uma figura de avental na porta
    w, h = 15, 11; x0 = x - w // 2
    c.rect(x0 - 1, y - h - 1, w + 2, h + 2, TIMB[2]); c.hline(x0 - 1, y - h - 1, w + 2, TIMB[4]); c.rect(x0, y - h, w, h, (190, 170, 138))
    c.rect(x0 + 1, y - h + 1, w - 2, h - 2, (214, 194, 156)); c.poly([(x0 + 3, y - 2), (x0 + 3, y - 7), (x0 + 6, y - 9), (x0 + 9, y - 7), (x0 + 9, y - 2)], (74, 54, 46))
    c.rect(x0 + 10, y - 8, 2, 2, (150, 112, 90)); c.rect(x0 + 10, y - 6, 3, 4, (230, 224, 204)); c.hline(x0 + 1, y - 2, w - 2, (120, 96, 80))
    c.pset(x, y - h - 2, IRON[3])

def d_sacola_prego(c, x, y):  # sacola de pano pendurada e chapéu de palha no mesmo prego; y = prego
    c.rect(x - 1, y, 2, 2, IRON[4]); c.pset(x, y + 2, IRON[2])
    c.line(x - 4, y + 2, x - 2, y + 7, SACK[2]); c.line(x + 4, y + 2, x + 2, y + 7, SACK[2])        # alças
    BG_ = [mix(v, (190, 160, 110), .55) for v in SACK]; c.rect(x - 6, y + 7, 12, 14, BG_[3]); c.hline(x - 6, y + 7, 12, BG_[4]); c.vline(x - 6, y + 7, 14, BG_[4]); c.vline(x + 5, y + 7, 14, BG_[1]); c.hline(x - 6, y + 20, 12, BG_[1])
    c.rect(x - 3, y + 11, 6, 5, mix(RED[2], SACK[3], .35)); c.hline(x - 3, y + 11, 6, RED[3]); c.hline(x - 5, y + 14, 1, SACK[1]); c.pset(x + 4, y + 17, SACK[1])               # remendo
    ell(c, x - 12, y + 6, 7, 2.5, STRAW[3]); ell(c, x - 12, y + 3, 4, 3, STRAW[2]); c.hline(x - 15, y + 4, 7, RED[2]); c.hline(x - 18, y + 6, 12, STRAW[4])

def d_planta2(c, x, y): O.d_planta(c, x, y)
from casa_v2 import d_mesa, d_cadeira_balanco, d_armario, d_talha, d_planta_casa, d_cad_f, d_cad_b, d_cad_s, draw_rug

# ------------------------------------------------------------------ catálogo
def A(id, nome, classe, tipo, draw, size_m, layer='floor', collide=None, stand=None, face='up', anim='interact', zoom=2, desc='', frames=1, states=None, png=None, cat='casa', supports=None):
    return dict(id=id, nome=nome, categoria=cat, classe=classe, interacao=tipo, draw=draw, size_m=size_m, collide=collide, stand=stand, face=face, anim=anim, layer=layer, zoom=zoom, desc=desc, frames=frames, states=states, png=png, supports=supports)

ASSETS = [
 A('mesa_casa', 'Mesa de jantar com toalha', 'UTILIZAVEL', 'usar', d_mesa, (2.4, 1.3, 0.75), collide=[-30, -17, 30, 0], stand=[0, 14], zoom=2, desc='Mesa grande, com toalha de crochê branca de barrado azul e xícaras postas. Cabem seis.'),
 A('cadeira_c_frente', 'Cadeira (de frente)', 'UTILIZAVEL', 'usar', d_cad_f, (0.45, 0.45, 0.95), collide=[-5, -4, 5, 0]),
 A('cadeira_c_costas', 'Cadeira (de costas)', 'UTILIZAVEL', 'usar', d_cad_b, (0.45, 0.45, 0.95), collide=[-5, -4, 5, 0]),
 A('cadeira_c_dir', 'Cadeira (perfil direito)', 'UTILIZAVEL', 'usar', lambda c, x, y: d_cad_s(c, x, y, 'right'), (0.45, 0.45, 0.95), collide=[-5, -4, 5, 0]),
 A('cadeira_c_esq', 'Cadeira (perfil esquerdo)', 'UTILIZAVEL', 'usar', lambda c, x, y: d_cad_s(c, x, y, 'left'), (0.45, 0.45, 0.95), collide=[-5, -4, 5, 0]),
 A('balanco', 'Cadeira de balanço', 'UTILIZAVEL', 'usar', d_cadeira_balanco, (0.75, 0.9, 1.25), collide=[-11, -9, 11, 0], stand=[0, 11], zoom=2, desc='Cadeira de balanço de madeira escura, braços, encosto de palhinha e patins curvos, ao lado da janela e virada para dentro de casa.'),
 A('armario_casa', 'Guarda-roupa com espelho', 'EXAMINAVEL', 'examinar', d_armario, (1.5, 0.55, 2.3), collide=[-18, -9, 18, 0], stand=[0, 11], zoom=2, desc='Guarda-roupa de duas portas, uma com espelho.'),
 A('cama_casa', 'Cama de solteiro com colcha de retalhos', 'EXAMINAVEL', 'examinar', d_cama, (1.1, 2.0, 0.5), collide=[-14, -33, 14, 0], stand=[-20, -6], zoom=2, desc='Cama de solteiro com cabeceira de madeira e colcha de retalhos.'),
 A('criado_radio', 'Criado-mudo com rádio', 'EXAMINAVEL', 'examinar', d_criado, (0.5, 0.4, 0.7), collide=[-7, -5, 7, 0], stand=[0, 10], zoom=3, desc='Criado-mudo com rádio de pilha e óculos.'),
 A('talha_barro', 'Filtro de barro', 'EXAMINAVEL', 'examinar', d_talha, (0.9, 0.45, 1.5), collide=[-11, -7, 11, 0], stand=[0, 10], zoom=2, desc='Filtro de barro com tampa de madeira e torneira, sobre um suporte de madeira encostado na parede, com uma caneca esmaltada.'),
 A('oratorio', 'Oratório', 'EXAMINAVEL', 'examinar', d_oratorio, (0.9, 0.2, 1.5), layer='wall', zoom=3, desc='Oratório de madeira com porta aberta, estampa e fitas.'),
 A('retrato_mae', 'Retrato da mãe', 'EXAMINAVEL', 'examinar', d_retrato_mae, (0.6, 0.05, 0.85), layer='wall', zoom=3, desc='Moldura oval sépia com uma senhora de lenço branco.'),
 A('foto_forno', 'Fotografia do forno', 'EXAMINAVEL', 'examinar', d_foto_forno, (0.55, 0.05, 0.4), layer='wall', zoom=3, desc='Fotografia pequena de um forno de lenha e uma mulher de avental.'),
 A('sacola_prego', 'Sacola de pano e chapéu', 'EXAMINAVEL', 'examinar', d_sacola_prego, (0.5, 0.1, 0.9), layer='wall', zoom=3, desc='Sacola de pano remendada e chapéu de palha no prego.'),
 A('caixa_domino', 'Caixa de dominó', 'EXAMINAVEL', 'examinar', d_caixa_domino, (0.2, 0.15, 0.1), layer='on', zoom=3, desc='Caixa de madeira de dominó com algumas pedras fora.'),
 A('cesto_pao', 'Cesto de pão com pano', 'DECORATIVO', 'nenhum', d_cesto_pao, (0.3, 0.3, 0.2), layer='on'),
 A('planta_casa', 'Vaso de folhagem', 'DECORATIVO', 'nenhum', d_planta_casa, (0.8, 0.4, 1.2), collide=[-6, -4, 6, 0], desc='Folhagem em vaso de barro.'),
 A('prateleira_casa', 'Prateleira de louças', 'DECORATIVO', 'nenhum', O.d_prateleira, (1.4, 0.2, 0.35), layer='wall'),
 A('fogao_casa', 'Fogão de quatro bocas', 'FUNCIONAL', 'examinar', O.d_fogao, (0.8, 0.6, 1.2), collide=[-10, -9, 10, 0], stand=[0, 9], zoom=2, states=['desligado', 'ligado'], desc='Fogão a gás de quatro bocas, com forno.', supports=[dict(nome='boca_esq', dx=-5, dy=-28), dict(nome='boca_dir', dx=5, dy=-28)]),
 A('panela_casa', 'Panela de alumínio', 'DECORATIVO', 'nenhum', O.d_panela, (0.28, 0.28, 0.2), layer='on'),
 A('cafeteira_casa', 'Cafeteira esmaltada', 'DECORATIVO', 'nenhum', O.d_cafeteira, (0.2, 0.2, 0.3), layer='on'),
 A('chama_casa', 'Chama do fogão', 'DECORATIVO', 'nenhum', lambda c, x, y: O.d_chama(c, x, y, 0), (0.1, 0.1, 0.1), layer='on', frames=2),
 A('vapor_casa', 'Vapor da panela', 'DECORATIVO', 'nenhum', lambda c, x, y: O.d_vapor(c, x, y, 0), (0.1, 0.1, 0.1), layer='on', frames=2),
 A('vela_oratorio', 'Vela do oratório', 'DECORATIVO', 'nenhum', lambda c, x, y: d_vela_oratorio(c, x, y, 0), (0.05, 0.05, 0.2), layer='wall', frames=2),
]

def render(a):
    out = []
    if a['png']:
        out.append((a['id'], Image.open(f"../assets/{a['png']}.png"), None)); return out
    for f in range(a['frames']):
        c = new(); d = a['draw']
        if a['id'] == 'chama_casa': O.d_chama(c, *AXY, f)
        elif a['id'] == 'vapor_casa': O.d_vapor(c, *AXY, f)
        elif a['id'] == 'vela_oratorio': d_vela_oratorio(c, *AXY, f)
        else: d(c, *AXY)
        bb = c.im.getbbox(); out.append((a['id'] + (f'#{f}' if a['frames'] > 1 else ''), c.im.crop(bb), (AXY[0] - bb[0], AXY[1] - bb[1])))
    return out

# ------------------------------------------------------------------ cena
FX, FY = 112, 141                       # fogão (base); a parede termina em y=132 — móveis encostados têm a frente a ~9 px dela
TX, TY = 231, 208                       # mesa (frente do pé) — conjunto de convivência
SCENE = [
 dict(inst='fogao_1', asset='fogao_casa', x=FX, y=FY, stand_abs=[FX, FY + 10]),
 dict(inst='panela_1', asset='panela_casa', sobre='fogao_1', suporte='boca_esq', visivel_se=['fogao_1', 1]),
 dict(inst='chama_1', asset='chama_casa', sobre='fogao_1', suporte='boca_esq', visivel_se=['fogao_1', 1], off=[0, 0]),
 dict(inst='vapor_1', asset='vapor_casa', sobre='fogao_1', suporte='boca_esq', off=[0, -9], visivel_se=['fogao_1', 1]),
 dict(inst='cafeteira_1', asset='cafeteira_casa', sobre='fogao_1', suporte='boca_dir'),
 dict(inst='prateleira_1', asset='prateleira_casa', x=146, y=62),
 dict(inst='foto_forno_1', asset='foto_forno', x=84, y=84, stand_abs=[100, 152], anim='interact_high'),
 dict(inst='talha_1', asset='talha_barro', x=148, y=141),
 dict(inst='sacola_1', asset='sacola_prego', x=207, y=70, stand_abs=[200, 162], anim='interact_high'),
 dict(inst='planta_1', asset='planta_casa', x=87, y=143),
 dict(inst='balanco_1', asset='balanco', x=207, y=147),
 dict(inst='oratorio_1', asset='oratorio', x=316, y=104, stand_abs=[316, 152], anim='interact_high'),
 dict(inst='vela_1', asset='vela_oratorio', x=316, y=80, visivel_se=['oratorio_1', 1]),
 dict(inst='retrato_1', asset='retrato_mae', x=346, y=70, stand_abs=[346, 152], anim='interact_high'),
 dict(inst='armario_1', asset='armario_casa', x=346, y=141),
 dict(inst='criado_1', asset='criado_radio', x=372, y=141),
 dict(inst='cama_1', asset='cama_casa', x=392, y=174),
 dict(inst='mesa_1', asset='mesa_casa', x=TX, y=TY, stand_abs=[TX + 46, TY + 10]),
 dict(inst='cesto_1', asset='cesto_pao', sobre_abs=[TX + 16, TY - 30]),
 dict(inst='domino_1', asset='caixa_domino', sobre_abs=[TX - 10, TY - 30], stand_abs=[TX - 46, TY + 10]),
 dict(inst='cad_frente', asset='cadeira_c_frente', x=TX - 15, y=TY - 27, base=TY - 27, stand_abs=[TX - 31, TY - 22]),
 dict(inst='cad_frente2', asset='cadeira_c_frente', x=TX + 15, y=TY - 27, base=TY - 27, stand_abs=[TX + 31, TY - 22]),
 dict(inst='cad_esq', asset='cadeira_c_esq', x=TX - 39, y=TY - 5, base=TY - 5, stand_abs=[TX - 44, TY + 6]),
 dict(inst='cad_dir', asset='cadeira_c_dir', x=TX + 39, y=TY - 5, base=TY - 5, stand_abs=[TX + 44, TY + 6]),
 dict(inst='cad_sul', asset='cadeira_c_costas', x=TX - 15, y=TY + 18, base=TY + 18, stand_abs=[TX - 1, TY + 19]),
 dict(inst='cad_sul2', asset='cadeira_c_costas', x=TX + 15, y=TY + 18, base=TY + 18, stand_abs=[TX + 29, TY + 19]),
]

def build():
    cats = {}
    for a in ASSETS:
        for key, im, anc in render(a): cats.setdefault('casa', []).append((key, im, anc, a))
    sheet, pos = O.pack([(k, im) for k, im, _, _ in cats['casa']]); sheet.save(OUT + 'casa_objetos.png')
    entries = []
    for key, im, anc, a in cats['casa']:
        e = {k: a[k] for k in ('id', 'nome', 'categoria', 'classe', 'interacao', 'size_m', 'layer', 'states', 'supports', 'zoom', 'desc', 'frames', 'anim', 'face') if k in a}
        e.update(sprite=key, folha='objects/casa_objetos.png', rect=list(pos[key]), perspectiva='3/4 interior', dim_px=[im.width, im.height], ancora=list(anc) if anc else None, collide=a['collide'], stand=a['stand'])
        entries.append(e)
    json.dump(dict(unidade='1 m = 24 px (altura); piso 16 px/m; âncora = pés', camera='3/4 oblíqua', cena='casa_raimundo', assets=entries), open(OUT + 'catalog_casa.json', 'w'), indent=1, ensure_ascii=False)
    return entries

def build_scene(entries):
    by = {}
    for e in entries: by.setdefault(e['id'], []).append(e)
    A_ = {a['id']: a for a in ASSETS}; inst = []; inter = []; placed = {}
    for s in SCENE:
        e = by[s['asset']][0]; a = A_[s['asset']]; anc = e['ancora']
        if 'sobre' in s:
            host = placed[s['sobre']]; sup = next(q for q in by[host['asset']][0]['supports'] if q['nome'] == s['suporte']); ox, oy = s.get('off', [0, 0])
            x, y = host['x'] + sup['dx'] + ox, host['y'] + sup['dy'] + oy; sort = host['y'] + .2
        elif 'sobre_abs' in s:
            x, y = s['sobre_abs']; sort = TY + .2
        else:
            x, y = s['x'], s['y']; sort = y
        placed[s['inst']] = dict(asset=s['asset'], x=x, y=y)
        sx, sy = x - anc[0], y - anc[1]; col = None
        if e['collide']: c0 = e['collide']; col = [x + c0[0], y + c0[1], x + c0[2], y + c0[3]]
        if 'base' in s: sort = s['base']
        rec = dict(inst=s['inst'], asset=s['asset'], sprite=e['sprite'], sx=sx, sy=sy, base=sort, layer=e['layer'], collide=col, frames=e['frames'])
        if e['states']: rec['states'] = e['states']
        if s.get('visivel_se'): rec['visivel_se'] = s['visivel_se']
        if e['frames'] > 1: rec['fps'] = 6
        inst.append(rec)
        if e['interacao'] != 'nenhum' and (e['layer'] != 'on' or s['inst'] == 'domino_1'):
            st = e['stand']; stand = s.get('stand_abs') or ([x + st[0], y + st[1]] if st else [x, y + 10])
            inter.append(dict(id=s['inst'], asset=s['asset'], nome=e['nome'], classe=e['classe'], tipo=e['interacao'], rect=[sx, sy, e['dim_px'][0], e['dim_px'][1]], stand=stand,
                              face=s.get('face', e['face']), anim=s.get('anim', e['anim']), zoom=e['zoom'], desc=e['desc'], **({'states': e['states']} if e['states'] else {})))
    # interativos fixos do cenário-base
    inter += [
      dict(id='janela_sacada', asset='janela', nome='Porta-janela da sacada', classe='EXAMINAVEL', tipo='examinar', rect=[220, 42, 72, 84], stand=[256, 152], face='up', anim='interact_high', zoom=2, desc='Porta-janela de veneziana com sacada de ferro.'),
      dict(id='lampada', asset='lampada', nome='Lâmpada nua', classe='DECORATIVO', tipo='nenhum', rect=[198, 56, 12, 14], stand=[204, 160], face='up', anim='interact_high', zoom=2, desc=''),
    ]
    inter = [i for i in inter if i['tipo'] != 'nenhum']
    seats = [
      dict(id='cad_frente', x=TX - 15, y=TY - 30, face='down', sort='after', base=TY - 23, mesa='M', stand=[TX - 31, TY - 22]),
      dict(id='cad_frente2', x=TX + 15, y=TY - 30, face='down', sort='after', base=TY - 23, mesa='M', stand=[TX + 31, TY - 22]),
      dict(id='cad_esq', x=TX - 39, y=TY - 8, face='right', sort='after', base=TY - 3, mesa='M', stand=[TX - 44, TY + 6]),
      dict(id='cad_dir', x=TX + 39, y=TY - 8, face='left', sort='after', base=TY - 3, mesa='M', stand=[TX + 44, TY + 6]),
      dict(id='cad_sul', x=TX - 15, y=TY + 12, face='up', sort='before', base=TY + 18, mesa='M', stand=[TX - 1, TY + 19]),
      dict(id='cad_sul2', x=TX + 15, y=TY + 12, face='up', sort='before', base=TY + 18, mesa='M', stand=[TX + 29, TY + 19]),
      dict(id='balanco_1', x=207, y=150, face='down_right', sort='after', base=148, mesa='janela', stand=[207, 160]),
    ]
    solids = [[72, 0, 408, 135]]                                    # parede de fundo (o fundo já bloqueia por YB; mantido para depuração)
    pontos = dict(porta=[240, 231], fogao=[FX, FY + 10], mesa_cafe=[TX + 8, TY + 24], talha=[148, 151], planta=[93, 153], janela=[207, 158], oratorio=[316, 152], armario=[346, 152],
                  cama=[364, 174], radio=[372, 152], retrato=[346, 152], foto=[100, 152], sacola=[200, 162], sala=[290, 205], tapete=[TX + 70, TY + 14], entrada=[240, 222], mesa_dom=[TX + 48, TY + 14])
    scene = dict(cena='casa_raimundo', seats=seats, pontos=pontos, instancias=inst, interativos=inter, colisao_arquitetura=[])
    json.dump(scene, open(OUT + 'scene_casa.json', 'w'), indent=1, ensure_ascii=False)
    return scene

if __name__ == '__main__':
    base = build_base(); frame_room(base); light_pass(base); base.save('../assets/casa_interior_base.png')
    e = build(); sc = build_scene(e); print(len(e), 'sprites', len(sc['instancias']), 'instâncias', len(sc['interativos']), 'interativos')

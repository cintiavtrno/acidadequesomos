"""Arte do quintal (Etapa 8.6b) no mesmo fluxo dos outros mundos: pxl + rampas de cor + luz do alto/esquerda.
Saídas em ../assets/quintal/: quintal_base.png (720x270), mangueira_copa.png, folhas (mobiliario/equipamentos/decorativos/itens).png,
catalog_quintal.json (posição em px do mundo de cada sprite) e quintal_preview.png. 1 m = 24 px (X e altura), 16 px/m (profundidade)."""
import json, math, random
from PIL import Image
from pxl import *
from facade import CAL, STONE, BRICK, IRON, MOSS, TELHA, GLASS
from interior import TIMB, WOOD, LEAF, STRAW, CLAY, RED, SACK, BREAD
D = json.load(open('../quintal/qdata.json')); OUT = '../assets/quintal/'
SX = lambda X: round(24 + 24 * X)
SY = lambda Y, Z=0: round(124 + 16 * Y - 24 * Z)
W, H = 720, 270
SKIN = ramp(24, 0.40, (0.30, 0.40, 0.50, 0.60, 0.70)); BLUE = ramp(215, 0.40, (0.22, 0.32, 0.42, 0.52, 0.62)); YEL = ramp(44, 0.65, (0.34, 0.46, 0.58, 0.70, 0.82))
BARK = ramp(30, 0.22, (0.14, 0.22, 0.31, 0.40, 0.50)); ALU = ramp(210, 0.07, (0.28, 0.40, 0.54, 0.68, 0.82)); ENAM = ramp(200, 0.40, (0.20, 0.30, 0.42, 0.54, 0.66))
DEND = ramp(24, 0.80, (0.28, 0.38, 0.48, 0.58, 0.68)); CHITA = ramp(350, 0.50, (0.35, 0.47, 0.60, 0.72, 0.84))
def shadow(c, x0, x1, yb, a=70):
    for k, al in enumerate((a + 10, a - 20)): c.hline(x0 - 1 + k, yb + k, x1 - x0 + 2 - 2 * k, (18, 10, 28, al))
def box(c, x, y, w, d, h, R, grain=0, cap=True):
    """caixa 3/4: (x,y) = canto de trás/esquerda do tampo; luz do alto/esquerda."""
    c.rect(x, y + d, w, h, R[2]); c.vline(x, y + d, h, R[3]); c.vline(x + w - 1, y + d, h, R[1]); c.hline(x, y + d + h - 1, w, R[0]); c.hline(x, y + d, w, R[4])
    c.rect(x, y, w, d, R[3]); c.hline(x, y, w, R[4]); c.vline(x, y, d, R[4]); c.vline(x + w - 1, y, d, R[2]); c.hline(x, y + d - 1, w, R[2])
    if grain:
        rg = random.Random(w * 7 + d)
        for k in range(1, d - 1, 3): c.hline(x + 1, y + k, w - 2, R[2] if k % 6 else R[3])
        for k in range(grain): xx = x + rg.randint(2, w - 6); c.hline(xx, y + rg.randint(1, max(1, d - 2)), rg.randint(3, 8), R[2])
def leg(c, x, y, h, R, w=2): c.rect(x, y, w, h, R[2]); c.vline(x, y, h, R[3]); c.vline(x + w - 1, y, h, R[1]); c.hline(x, y + h - 1, w, R[0])
def ell(c, cx, cy, rx, ry, col):
    for yy in range(int(cy - ry) - 1, int(cy + ry) + 2):
        for xx in range(int(cx - rx) - 1, int(cx + rx) + 2):
            if ((xx - cx) / max(rx, .5)) ** 2 + ((yy - cy) / max(ry, .5)) ** 2 <= 1: c.pset(xx, yy, col)

# ============================================================ OBJETOS (cada função desenha em canvas c; retorna (x, y) do tampo/ancora)
def d_table(c, x, y, w, d, h, R, t=2, apron=3):       # mesa de madeira: tampo com espessura, aventais e pernas
    top = h - t
    for lx in (x + 1, x + w - 3): leg(c, lx, y + d + t, top, R)
    for lx in (x + 2, x + w - 4): leg(c, lx, y + t, h - t, [R[0], R[1], R[1], R[2], R[3]])
    c.rect(x + 3, y + d + t, w - 6, apron, R[1]); c.hline(x + 3, y + d + t, w - 6, R[2])
    box(c, x, y, w, d, t, R, grain=4)
def d_chair(c, x, y, face, R=TIMB):                   # pegada 12×8 px (0,5×0,5 m); assento a 11 px, encosto até 22 px; âncora = base dos pés da frente
    w, yb = 12, y + 22
    def seatp(): box(c, x, yb - 11, w, 8, 2, R); c.hline(x + 1, yb - 10, w - 2, R[4])
    def legs(front=True, back=True):
        if back:
            for lx in (x + 1, x + w - 3): leg(c, lx, yb - 3, 4, [R[0], R[1], R[1], R[2], R[3]])
        if front:
            for lx in (x + 1, x + w - 3): leg(c, lx, yb - 1, 9, R)
    if face == 'down':
        legs(front=False); box(c, x + 1, yb - 22, w - 2, 2, 11, R); c.rect(x + 3, yb - 18, w - 6, 6, R[1]); [c.vline(x + 3 + i * 2, yb - 18, 6, R[2]) for i in range(4)]
        seatp(); legs(back=False)
    elif face == 'up':
        legs(front=False); seatp(); legs(back=False)
        box(c, x + 1, yb - 16, w - 2, 2, 15, R); c.rect(x + 3, yb - 12, w - 6, 7, R[1]); [c.vline(x + 3 + i * 2, yb - 12, 7, R[2]) for i in range(4)]
    else:
        bx = x if face == 'right' else x + w - 3
        legs(front=False); seatp(); box(c, bx, yb - 22, 3, 8, 11, R); legs(back=False)
        c.rect(bx + 1 if face == 'right' else bx, yb - 12, 2, 8, R[1])
def d_stool(c, w, d, h, R=TIMB):
    box(c, 0, 0, w, d, 2, R); leg(c, 1, d + 2, h - 2, R); leg(c, w - 3, d + 2, h - 2, R)
def d_bench(c, w, d, h, R=TIMB):
    for lx in (2, w - 4): c.rect(lx, d + 1, 3, h - 2, R[2]); c.vline(lx, d + 1, h - 2, R[3]); c.vline(lx + 2, d + 1, h - 2, R[1])
    c.rect(4, d + h - 5, w - 8, 1, R[1]); box(c, 0, 0, w, d, 2, R, grain=3)
def d_pano(c, x, y, w, d, h, R):       # toalha branca caindo pelos lados
    c.rect(x, y, w, d, SACK[3]); c.hline(x, y, w, SACK[4]); c.hline(x, y + d - 1, w, SACK[2])
    c.rect(x, y + d, w, h, SACK[3])
    for k in range(0, w, 6): c.vline(x + k, y + d + 1, h - 2, SACK[2]); c.vline(x + k + 1, y + d + 1, h - 2, SACK[4])
    for k in range(1, w, 2): c.pset(x + k, y + d + h - 1, SACK[1] if k % 4 else SACK[2])
    for k in range(0, w, 4): c.pset(x + k, y + d + h, SACK[0])
    c.vline(x, y, d + h, SACK[4]); c.vline(x + w - 1, y, d + h, SACK[1])
    for k in range(3, w - 3, 8): c.hline(x + k, y + 2, 3, SACK[2])      # bordado
def d_mesa_longa(c, w, d, h):
    for lx in (3, w - 5): leg(c, lx, d + 6, h - 6, TIMB); leg(c, lx, 2, h - 8, [TIMB[0], TIMB[1], TIMB[1], TIMB[2], TIMB[3]])
    d_pano(c, 0, 0, w, d, h - 5, TIMB)
def d_tronco(c, w, h):
    rg = random.Random(3)
    for y in range(h):
        flare = max(0, (y - (h - 14))) * 0.55; x0 = int(-flare); x1 = int(w + flare)
        for x in range(x0, x1): c.pset(x + 6, y, BARK[2])
    for y in range(h):
        flare = max(0, (y - (h - 14))) * 0.55; x0 = int(-flare); x1 = int(w + flare)
        c.pset(x0 + 6, y, BARK[3]); c.pset(x0 + 7, y, BARK[3]); c.pset(x1 + 5, y, BARK[1]); c.pset(x1 + 4, y, BARK[1]); c.pset(x1 + 3, y, BARK[1] if y % 2 else BARK[2])
    for k in range(34):
        x = 6 + rg.randint(1, w - 2); y = rg.randint(0, h - 4); L = rg.randint(3, 9); c.vline(x, y, L, BARK[1] if rg.random() < .6 else BARK[3])
    for k in range(6): ell(c, 6 + rg.randint(2, w - 3), rg.randint(6, h - 18), 1.5, 2, BARK[0]); c.pset(6 + rg.randint(2, w - 3), rg.randint(4, h - 10), MOSS[2])
    for k in range(5): c.pset(6 + w - 2, h - 20 + k * 3, MOSS[1]); c.pset(6 + w - 3, h - 19 + k * 3, MOSS[2])
    c.hline(2, h - 1, w + 8, BARK[0]); c.hline(3, h - 2, w + 6, BARK[1])
def d_stone_curb(c, w, d, h):
    box(c, 0, 0, w, d, h, STONE)
    for x in range(8, w, 11): c.vline(x, d, h, STONE[1]); c.vline(x, 0, d, STONE[2])
    rg = random.Random(5)
    for k in range(10): c.pset(rg.randint(1, w - 2), d + rg.randint(1, h - 2), STONE[4] if k % 2 else STONE[1])
    for k in range(5): c.hline(rg.randint(1, w - 6), 0, 3, MOSS[2]); c.pset(rg.randint(1, w - 2), d + h - 2, MOSS[1])
def d_fogao(c, w, d, h):          # fogão a gás esmaltado: tampo preto com bocas, painel, forno com visor
    box(c, 0, 0, w, d, 3, SACK); c.rect(2, 2, w - 4, d - 3, IRON[1])
    for bx in (6, w - 7):
        ell(c, bx, 4, 3, 1.4, IRON[0]); ell(c, bx, 4, 1.6, .8, IRON[3]); ell(c, bx, 7, 3, 1.4, IRON[0]); ell(c, bx, 7, 1.6, .8, IRON[3])
    c.rect(0, d + 3, w, 4, SACK[4]); c.hline(0, d + 3, w, SACK[4]);
    for k in range(4): c.rect(3 + k * ((w - 8) // 3), d + 4, 2, 2, IRON[2]); c.pset(3 + k * ((w - 8) // 3), d + 4, IRON[4])
    c.rect(0, d + 7, w, h - 7 - 2, SACK[3]); c.vline(0, d + 7, h - 9, SACK[4]); c.vline(w - 1, d + 7, h - 9, SACK[1])
    c.rect(2, d + 9, w - 4, h - 13, SACK[2]); c.rect(4, d + 11, w - 8, h - 17, IRON[1]); c.hline(4, d + 11, w - 8, IRON[2]); c.hline(3, d + 9, w - 6, SACK[4])
    c.hline(2, d + 8, w - 4, IRON[4])
    c.rect(1, d + h - 2, 3, 2, IRON[1]); c.rect(w - 4, d + h - 2, 3, 2, IRON[1]); c.hline(0, d + h - 3, w, SACK[1])
def d_trempe(c, w, d, f):         # 3 pedras/ferro + panelão de alumínio com dendê fervendo + fogo (2 quadros)
    cx = w // 2
    for k, (dx, dy) in enumerate(((-9, 12), (9, 12), (0, 7))): c.rect(cx + dx - 2, dy, 4, 12, STONE[2]); c.vline(cx + dx - 2, dy, 12, STONE[3]); c.vline(cx + dx + 1, dy, 12, STONE[1]); c.hline(cx + dx - 2, dy, 4, STONE[4])
    # fogo
    for i, (fx, fh) in enumerate(((cx - 5, 9), (cx - 1, 12), (cx + 4, 8))):
        fh2 = fh + (2 if (i + f) % 2 else 0)
        for k in range(fh2): ww = max(1, 3 - k * 3 // fh2); c.hline(fx - ww // 2, 22 - k, ww + 1, (226, 112, 38) if k < fh2 * .55 else (246, 196, 74))
        c.pset(fx, 22, (255, 232, 140))
    for k in range(6): c.pset(cx - 9 + k * 3, 23, (60, 30, 24))
    # panelão
    ell(c, cx, 6, 15, 6, ALU[3]); ell(c, cx, 6, 13, 5, ALU[1]); ell(c, cx, 6, 11, 4, DEND[2]); ell(c, cx - 3, 5, 5, 2, DEND[3]); ell(c, cx + 4, 7, 3, 1.3, DEND[1])
    c.rect(cx - 15, 7, 31, 12, ALU[2]); c.vline(cx - 15, 7, 12, ALU[4]); c.vline(cx + 15, 7, 12, ALU[1]); c.hline(cx - 14, 19, 29, ALU[1]); c.hline(cx - 14, 20, 27, ALU[0])
    c.vline(cx - 11, 8, 10, ALU[3]); c.vline(cx - 10, 8, 10, ALU[4])
    ell(c, cx, 6, 15, 6, ALU[3]) if False else None
    for dx in (-18, 18): c.rect(cx + dx - 2, 8, 4, 2, ALU[1]); c.pset(cx + dx - 2, 8, ALU[3])
    c.hline(cx - 14, 6, 29, ALU[4]) if False else None
def d_bancada(c, w, d, h):
    d_table(c, 0, 0, w, d, h, TIMB, t=3, apron=2)
    c.hline(2, d + 10, w - 4, TIMB[1]); box(c, 3, d + 12, w - 6, 3, 2, TIMB)
def d_tanque(c, w, d, h):          # tanque de pedra/cimento com torneira e água
    box(c, 0, 0, w, d, h - 2, STONE); c.rect(2, 2, w - 4, d - 3, STONE[1]); c.rect(3, 3, w - 6, d - 5, GLASS[2]); c.hline(3, 3, w - 6, GLASS[3]); c.hline(4, 5, 6, GLASS[4])
    c.rect(w // 2 - 1, -5, 2, 7, IRON[3]); c.hline(w // 2 - 1, -5, 5, IRON[3]); c.pset(w // 2 + 4, -4, IRON[4]); c.vline(w // 2 + 4, -3, 2, GLASS[4])
    for k in range(3): c.pset(3 + k * 4, d + h - 5, MOSS[2])
    for k in range(2): c.rect(2 + k * (w - 6), d + h - 2, 3, 2, STONE[1])
def d_talha(c, w, d, h):           # talha de barro sobre suporte de madeira, com tampa e caneca
    cx = w // 2
    for k in range(3): c.rect(cx - 6 + k * 5, 24 - 0, 2, 0, TIMB[2])
    c.rect(cx - 5, 18, 2, 8, TIMB[2]); c.rect(cx + 3, 18, 2, 8, TIMB[1]); c.hline(cx - 5, 17, 11, TIMB[3]); c.hline(cx - 5, 25, 11, TIMB[0])
    for y in range(0, 17):
        r = 5.5 - abs(y - 9) * 0.28 if y > 2 else 3 + y; ell(c, cx, y + 1, r, 0.8, CLAY[2])
    for y in range(0, 17):
        r = 5.5 - abs(y - 9) * 0.28 if y > 2 else 3 + y
        c.hline(int(cx - r), y + 1, 2, CLAY[4]); c.hline(int(cx + r - 2), y + 1, 2, CLAY[1])
    c.hline(cx - 4, 0, 8, CLAY[3]); c.hline(cx - 3, -1, 6, CLAY[4]); c.rect(cx - 1, -3, 3, 2, CLAY[2]); c.pset(cx, -4, CLAY[3])
    c.hline(cx - 5, 8, 11, CLAY[1]); c.rect(cx + 6, 10, 3, 3, ENAM[3]); c.pset(cx + 7, 10, ENAM[4])
def d_lavatorio(c, w, d, h):
    cx = w // 2; c.rect(cx - 4, 14, 2, 8, TIMB[2]); c.rect(cx + 2, 14, 2, 8, TIMB[1]); c.hline(cx - 5, 13, 11, TIMB[3]); c.rect(cx - 5, 20, 11, 1, TIMB[1])
    ell(c, cx, 9, 6, 2.5, ENAM[3]); ell(c, cx, 9, 4.5, 1.6, GLASS[3]); c.hline(cx - 4, 8, 3, GLASS[4]); c.rect(cx - 6, 10, 13, 3, ENAM[2]); c.vline(cx - 6, 10, 3, ENAM[4]); c.vline(cx + 6, 10, 3, ENAM[1])
    ell(c, cx + 8, 8, 2, 1, ENAM[4]); c.rect(cx + 7, 8, 3, 3, ENAM[3])
def d_pilao(c, w, d, h):
    cx = w // 2; ell(c, cx, 4, 5, 2, TIMB[4]); ell(c, cx, 4, 3.5, 1.3, TIMB[0]); c.rect(cx - 5, 4, 11, 8, TIMB[2]); c.vline(cx - 5, 4, 8, TIMB[3]); c.vline(cx + 5, 4, 8, TIMB[1]); c.hline(cx - 4, 12, 9, TIMB[0]); c.hline(cx - 4, 7, 9, TIMB[1])
    c.line(cx + 1, 3, cx + 5, -12, TIMB[3]); c.line(cx + 2, 3, cx + 6, -12, TIMB[2]); c.rect(cx + 4, -13, 3, 3, TIMB[3])
def d_lenha(c, w, d, h):           # pilha de lenha: troncos vistos de cima (deitados) e as pontas na frente
    box(c, 0, 0, w, d, h, TIMB); rg = random.Random(9)
    for k in range(1, w - 1, 3): c.vline(k, 1, d - 2, TIMB[4]); c.vline(k + 1, 1, d - 2, TIMB[2]); c.vline(k + 2, 1, d - 2, TIMB[1])
    for k in range(0, w - 3, 4):
        for j in range(0, h - 2, 4): ell(c, k + 3, d + j + 3, 2, 2, TIMB[4] if (k + j) % 8 else CLAY[3]); c.pset(k + 3, d + j + 3, TIMB[1]); c.pset(k + 2, d + j + 4, TIMB[0])
def d_tabuleiro(c, w, d, h):       # tabuleiro de Nena: mesa com pano e tacho
    d_table(c, 0, 0, w, d, h, TIMB, t=2, apron=1); c.rect(0, 0, w, d, SACK[3]); c.hline(0, 0, w, SACK[4]); c.hline(0, d - 1, w, SACK[2]); c.rect(0, d, w, 3, SACK[3]); c.hline(0, d + 2, w, SACK[1])
    for k in range(0, w, 4): c.pset(k, d + 2, SACK[2])
def d_vaso(c, w, d, h):            # planta em lata pintada
    cx = w // 2; c.rect(cx - 4, 6, 9, 7, ALU[2]); c.vline(cx - 4, 6, 7, ALU[4]); c.vline(cx + 4, 6, 7, ALU[1]); c.hline(cx - 4, 12, 9, ALU[0]); c.hline(cx - 5, 5, 11, ALU[3]); c.hline(cx - 5, 5, 11, ALU[4])
    c.rect(cx - 3, 8, 7, 2, RED[2]); c.rect(cx - 3, 10, 7, 1, STRAW[3]); c.hline(cx - 3, 4, 7, CLAY[0])
    rg = random.Random(w + 4)
    for k in range(9):
        a = math.radians(-70 + k * 17 + rg.uniform(-4, 4)); L = rg.randint(8, 13); tx, ty = cx + math.sin(a) * L, 4 - math.cos(a) * L
        c.poly([(cx - 1, 4), ((cx + tx) / 2 + 1, (4 + ty) / 2), (tx, ty), ((cx + tx) / 2 - 1, (4 + ty) / 2 + 1)], LEAF[2 + k % 3]); c.line(cx, 4, tx, ty, LEAF[4] if k % 2 else LEAF[1])
def d_banner(c, w, h):
    px = c.pset
    c.rect(0, 5, w, 3, TIMB[2]); c.hline(0, 5, w, TIMB[4]); c.rect(0, h + 5, w, 3, TIMB[2]); c.hline(0, h + 7, w, TIMB[0]); c.rect(-1 if False else 0, 3, 1, 4, TIMB[1]); c.rect(w - 1, 3, 1, 4, TIMB[1])
    c.vline(w // 2 - 4, 0, 5, TIMB[1]); c.vline(w // 2 + 4, 0, 5, TIMB[1]); c.hline(w // 2 - 4, 0, 9, TIMB[1])
    y0 = 8; hh = h - 3; cloth = ramp(172, 0.30, (0.26, 0.34, 0.42, 0.50, 0.58))
    c.rect(0, y0, w, hh, cloth[2]); c.vline(0, y0, hh, cloth[1]); c.vline(1, y0, hh, cloth[1]); c.vline(w - 1, y0, hh, cloth[0]); c.vline(w - 2, y0, hh, cloth[1])
    for x in range(4, w - 2, 5): c.vline(x, y0, hh, cloth[3])
    c.rect(2, y0 + 2, w - 4, 1, STRAW[3]); c.rect(2, y0 + hh - 3, w - 4, 1, STRAW[3]); c.vline(2, y0 + 2, hh - 4, STRAW[3]); c.vline(w - 3, y0 + 2, hh - 4, STRAW[3])
    c.rect(4, y0 + 4, w - 8, 1, RED[2]); c.rect(4, y0 + hh - 5, w - 8, 1, RED[2])
    for x in range(1, w - 1, 2): c.vline(x, y0 + hh, 4, STRAW[3] if x % 4 else STRAW[2])
    cx = w // 2; px(cx, y0 + 7, STRAW[4]); px(cx - 1, y0 + 8, STRAW[3]); px(cx + 1, y0 + 8, STRAW[3]); px(cx, y0 + 9, STRAW[3])
    def santo(sx0, rb, sk):
        top = y0 + 12
        for r in (7, 6): ell(c, sx0, top + 5, r, r - 1.5, STRAW[3] if r == 7 else cloth[2])
        c.hline(sx0 - 3, top + 1, 7, BARK[0]); c.rect(sx0 - 3, top + 2, 7, 3, BARK[0]); c.pset(sx0 - 4, top + 4, BARK[0]); c.pset(sx0 + 4, top + 4, BARK[0])
        c.rect(sx0 - 3, top + 4, 7, 6, sk[2]); c.vline(sx0 - 3, top + 4, 6, sk[3]); c.vline(sx0 + 3, top + 4, 6, sk[1])
        c.pset(sx0 - 2, top + 6, (30, 18, 16)); c.pset(sx0 + 1, top + 6, (30, 18, 16)); c.pset(sx0 - 1, top + 8, sk[1]); c.pset(sx0, top + 8, sk[1])
        c.rect(sx0 - 1, top + 10, 3, 2, sk[1])
        for i in range(22):
            hf = 3 + i * 2 // 9; c.hline(sx0 - hf - 1, top + 12 + i, 2 * hf + 3, rb[2]); c.pset(sx0 - hf - 1, top + 12 + i, rb[3]); c.pset(sx0 - hf, top + 12 + i, rb[3]); c.pset(sx0 + hf + 1, top + 12 + i, rb[1])
            if i % 7 == 6: c.hline(sx0 - hf, top + 12 + i, 2 * hf + 2, rb[1])
        c.rect(sx0 - 4, top + 12, 9, 3, rb[3]); c.hline(sx0 - 4, top + 12, 9, rb[4]); c.hline(sx0 - 3, top + 22, 8, STRAW[3]); c.hline(sx0 - 3, top + 23, 8, STRAW[1])
        c.rect(sx0 - 3, top + 34, 3, 2, sk[1]); c.rect(sx0 + 1, top + 34, 3, 2, sk[1])
    santo(cx - 8, RED, SKIN); santo(cx + 8, BLUE, ramp(22, 0.38, (0.26, 0.34, 0.43, 0.52, 0.62)))
    c.rect(cx - 3, y0 + 34, 6, 3, SKIN[3]); c.hline(cx - 3, y0 + 34, 6, SKIN[4])
    for i, x in enumerate(range(5, w - 7, (w - 12) // 5)): c.rect(x, y0 + hh - 10 + (i % 2), 3, 2, LEAF[3] if i % 2 else RED[3]); c.pset(x + 1, y0 + hh - 11 + (i % 2), STRAW[3])
def d_toalha(c, w, d):             # chita no chão: fundo rosado, flores pequenas, barra
    c.rect(0, 0, w, d, CHITA[3]); rg = random.Random(2)
    for y in range(0, d, 4):
        for x in range((y // 4 % 2) * 4, w, 8): c.pset(x, y, CHITA[1]); c.pset(x + 1, y, CHITA[4]); c.pset(x, y + 1, LEAF[2]); c.pset(x - 1, y, STRAW[3]); c.pset(x + 1, y + 1, STRAW[3])
    c.rect(0, 0, w, 2, CHITA[1]); c.rect(0, d - 2, w, 2, CHITA[1]); c.rect(0, 0, 2, d, CHITA[1]); c.rect(w - 2, 0, 2, d, CHITA[1]); c.hline(2, 2, w - 4, CHITA[4]); c.hline(2, d - 3, w - 4, STRAW[3])
    c.hline(0, 0, w, CHITA[2]); c.hline(0, d - 1, w, CHITA[0]); c.vline(w - 1, 0, d, CHITA[0])
    for k in range(4): c.hline(rg.randint(6, w - 12), rg.randint(4, d - 5), rg.randint(3, 7), CHITA[2])
    c.pset(0, 0, (0, 0, 0, 0)); c.pset(w - 1, d - 1, (0, 0, 0, 0))

# ---- itens pequenos (por nome → desenho em canvas c, w,h em px; âncora = base)
def i_bacia(c, w, h, col, fill=None):
    ell(c, w / 2, 1.5, w / 2, 1.8, col[4]); ell(c, w / 2, 2, w / 2 - 1, 1.2, fill or col[1]) if fill else None
    c.rect(0, 2, w, h - 2, col[2]); c.vline(0, 2, h - 2, col[3]); c.vline(w - 1, 2, h - 2, col[1]); c.hline(1, h - 1, w - 2, col[0])
def i_prato(c, w, h, col=SACK, fill=None):
    ell(c, w / 2, h / 2, w / 2, max(1.5, h / 2), col[3]); c.hline(1, h // 2, w - 2, col[4]) if w > 4 else None
    if fill: ell(c, w / 2, h / 2, max(1, w / 2 - 2), max(.8, h / 2 - 1), fill)
def draw_item(n, w, h, t):
    """devolve Image do item pelo nome."""
    n = n.lower(); w, h, t = round(w), round(h), round(t); c = C(max(w, 4) + 12, max(h, 3) + 14); ox = 2; oy = 10
    cv = C(c.w, c.h); cc = cv
    def sub(fn, *a, **k): s = C(c.w, c.h); fn(s, *a, **k); cv.im.alpha_composite(s.im, (0, 0))
    W_, H_ = max(3, round(w)), max(2, round(h))
    if 'toalha' in n: return None
    if re.search(r'bacia|caçarola|panela|tacho|balde', n): 
        s = C(c.w, c.h); col = ALU if re.search(r'panela|caçarola|tacho', n) else (ENAM if 'balde' in n else CLAY)
        fill = DEND[2] if re.search(r'vatap|caruru|camar|dendê', n) else (LEAF[2] if 'quiabo' in n else (SACK[3] if 'massa' in n else None))
        s2 = C(c.w, c.h); s2.im.alpha_composite(Image.new('RGBA', (1, 1)), (0, 0)); i_bacia(s2, W_, max(4, round(t)) if t else 4, col, fill); cv.im.alpha_composite(s2.im, (ox, oy + 2 - 2))
        if 'massa' in n: cv.rect(ox, oy, W_, 2, SACK[4])
        if 'balde' in n: cv.hline(ox + 1, oy - 2, W_ - 2, IRON[3])
    elif re.search(r'travessa|bandeja|prato|pratos|cocada|pratinho|doces|santos', n):
        fill = (DEND[3] if re.search(r'vatap', n) else DEND[2] if 'caruru' in n else STRAW[3] if re.search(r'arroz|farofa', n) else YEL[2] if re.search(r'doces|cocada', n) else None)
        s = C(c.w, c.h); i_prato(s, W_, max(3, H_), CLAY if 'pratinho' in n else SACK, fill); cv.im.alpha_composite(s.im, (ox, oy))
        if 'santos' in n: cv.pset(ox + 3, oy + 1, RED[2]); cv.pset(ox + 4, oy + 1, RED[3])
        if 'travessa' in n and 'arroz' in n: cv.rect(ox + 1, oy, W_ // 2, 2, SACK[4])
    elif 'pilha' in n:
        for k in range(3): s = C(c.w, c.h); i_prato(s, W_, 3, SACK); cv.im.alpha_composite(s.im, (ox, oy - k * 2))
    elif 'vela' in n:
        s = C(c.w, c.h); i_prato(s, 6, 3, CLAY); cv.im.alpha_composite(s.im, (ox - 1, oy)); cv.rect(ox + 1, oy - 3, 2, 3, SACK[4]); cv.pset(ox + 1, oy - 4, STRAW[4]); cv.pset(ox + 1, oy - 5, YEL[3])
    elif 'vasinho' in n:
        cv.rect(ox, oy - 2, 4, 3, CLAY[2]); cv.pset(ox, oy - 2, CLAY[4]); cv.vline(ox + 1, oy - 7, 5, LEAF[2]); cv.vline(ox + 2, oy - 6, 4, LEAF[3]); cv.pset(ox, oy - 8, SACK[4]); cv.pset(ox + 2, oy - 7, SACK[4]); cv.pset(ox + 3, oy - 5, SACK[4]); cv.pset(ox + 1, oy - 9, SACK[3])
    elif 'jarra' in n:
        col = GLASS if 'água' in n else ENAM; fill = GLASS[3] if 'água' in n else YEL[2]
        cv.rect(ox, oy - 5, 5, 6, col[2]); cv.vline(ox, oy - 5, 6, col[4]); cv.vline(ox + 4, oy - 5, 6, col[1]); cv.rect(ox + 1, oy - 4, 3, 4, fill); cv.hline(ox, oy - 6, 5, col[3]); cv.pset(ox + 5, oy - 4, col[3]); cv.pset(ox + 5, oy - 2, col[3])
    elif re.search(r'copos|copinhos', n):
        for k in range(min(6, max(1, W_ // 2))): cv.rect(ox + k * 2, oy - 2, 1, 3, GLASS[4]); cv.pset(ox + k * 2, oy - 2, SACK[4])
        if 'sete' in n: cv.rect(ox, oy - 1, 2, 2, GLASS[4])
    elif re.search(r'cesto', n):
        s = C(c.w, c.h); i_bacia(s, W_, max(4, round(t)), STRAW, None); cv.im.alpha_composite(s.im, (ox, oy - 2))
        for k in range(0, W_ - 2, 2): cv.pset(ox + 1 + k, oy - 1 + (k // 2 % 2), STRAW[1])
        cols = [RED[2], (200, 140, 50), LEAF[3]] if 'temperos' in n else [YEL[3], DEND[3]]
        for k in range(min(4, W_ // 2)): cv.pset(ox + 1 + k * 2, oy - 3, cols[k % len(cols)]); cv.pset(ox + 1 + k * 2, oy - 2, cols[k % len(cols)])
    elif re.search(r'tábua', n):
        cv.rect(ox, oy, W_, 3, TIMB[3]); cv.hline(ox, oy, W_, TIMB[4]); cv.hline(ox, oy + 2, W_, TIMB[1]); cv.pset(ox + W_ - 2, oy + 1, TIMB[0]); cv.hline(ox + 2, oy - 1, 4, LEAF[3])
    elif re.search(r'colher|faca|conchas|talheres|cuia', n):
        if 'cuia' in n: cv.rect(ox, oy - 3, 5, 4, TIMB[3]); cv.hline(ox, oy - 3, 5, TIMB[4]); [cv.vline(ox + 1 + k, oy - 6, 3, ALU[4 - k % 2]) for k in range(3)]
        else:
            cv.hline(ox, oy, W_, TIMB[3]); cv.pset(ox + W_, oy, TIMB[2]); cv.pset(ox + W_ + 1, oy, TIMB[3]); cv.hline(ox, oy - 1, max(2, W_ // 2), ALU[4]) if 'faca' in n else None
            if 'conchas' in n: cv.hline(ox + 1, oy - 1, W_ - 2, TIMB[4])
    elif 'dominó' in n:
        for k in range(4): cv.rect(ox + k * 3, oy - 1, 2, 2, SACK[4]); cv.pset(ox + k * 3, oy, IRON[1])
    else:
        cv.rect(ox, oy - 2, W_, 3, STRAW[3]); cv.hline(ox, oy - 2, W_, STRAW[4])
    return cv.im
import re

# ============================================================ montagem: sprites, folhas, catálogo
from PIL import ImageDraw
class T(C):
    """canvas com origem deslocada: os desenhos usam (0,0) = canto de trás/esquerda do tampo e podem sair para valores negativos"""
    def __init__(s, w, h, ox, oy): super().__init__(w, h); s.ox, s.oy = ox, oy
    def pset(s, x, y, c): super().pset(x + s.ox, y + s.oy, c)
    def line(s, x0, y0, x1, y1, c): super().line(x0 + s.ox, y0 + s.oy, x1 + s.ox, y1 + s.oy, c)
    def poly(s, pts, c): super().poly([(x + s.ox, y + s.oy) for x, y in pts], c)
    def shade(s, *a, **k): pass
OBJ = {o[0]: o for o in D['OBJ']}
SEAT = dict(M06='right', M07='left', M02='down', M03='down', M04='down', M05='down', M08='up', M10='right', M11='right', M12='left', M13='left', M15='down', M16='up', M17='right', M18='left', M19='down', M20='down', M21='down', M23='down', M24='down')
def px(o): return round(24 * o[5]), round(16 * o[6]), round(24 * o[7])
def sprite(fn, size=(160, 110), org=(24, 40)):
    c = T(size[0], size[1], org[0], org[1]); fn(c); im = c.im; bb = im.getbbox(); return im, bb, org
SPR = []     # (sheet, id, nome, Image, anchor(ax, ay_bottom_excl), world dict)
def add(sheet, id, nome, fn, w, d, h, wx, wy, wz=0, frames=1, size=(170, 120), org=(24, 44), shadow_on=True, layer='obj', extra=None):
    for f in range(frames):
        c = T(size[0], size[1], org[0], org[1]); fn(c, f) if frames > 1 else fn(c)
        bb = c.im.getbbox(); im = c.im.crop(bb); ax, ay = org[0] - bb[0], bb[3] - 0
        if shadow_on:
            sh = C(im.width + 6, im.height + 4); sh.im.alpha_composite(im, (3, 0)); shadow(sh, 3 + 1, 3 + im.width - 1, im.height, 70); im = sh.im; ax += 3
        SPR.append(dict(sheet=sheet, id=id + (f'#{f}' if frames > 1 else ''), nome=nome, im=im, pos=[SX(wx) - ax, SY(wy + d / 16 if False else wy, wz) if False else None], ax=ax, h_im=im.height, wx=wx, wy=wy, wz=wz, d=d, layer=layer, w=w, h=h, extra=extra or {}))
def build_objs():
    for o in D['OBJ']:
        id, nome, cat, x, y, wm, dm, hm = o[:8]; w, d, h = px(o)
        if id in ('F01', 'F02', 'F03', 'F04'): continue
        if id == 'F05' or id == 'F06': add('decorativos', id, nome, lambda c, w=w, h=h: (box(c, 0, 0, w, 5, h, TIMB), c.rect(-1, h - 2, w + 2, 4, TIMB[3]), c.hline(-1, h - 2, w + 2, TIMB[4]), c.rect(-1, 0, w + 2, 2, TIMB[3]), c.rect(w // 2 - 1, 8, 1, 3, TIMB[0]), c.rect(0, 20, w, 1, TIMB[1])), w, 5, h, x, y); continue
        if id == 'F07': add('equipamentos', id, nome, lambda c, f: d_trempe(c, w, d, f), w, d, h, x, y, frames=2, org=(30, 44)); continue
        if id == 'F08': add('equipamentos', id, nome, lambda c, w=w, d=d, h=h: d_fogao(c, w, d, h), w, d, h, x, y); continue
        if id == 'F09': add('mobiliario', id, nome, lambda c, w=w, d=d, h=h: d_bancada(c, w, d, h), w, d, h, x, y); continue
        if id == 'F10': add('equipamentos', id, nome, lambda c, w=w, d=d, h=h: d_tanque(c, w, d, h), w, d, h, x, y); continue
        if id == 'F11': add('equipamentos', id, nome, lambda c, w=w, d=d, h=h: d_talha(c, w, d, h), w, d, h, x, y); continue
        if id == 'F12': add('mobiliario', id, nome, lambda c, w=w, d=d, h=h: d_table(c, 0, 0, w, d, h, TIMB, t=3, apron=2), w, d, h, x, y); continue
        if id == 'F13': add('mobiliario', id, nome, lambda c, w=w, d=d, h=h: d_table(c, 0, 0, w, d, h, TIMB, t=2, apron=1), w, d, h, x, y); continue
        if id == 'F14': add('decorativos', id, nome, lambda c, w=w, h=h: d_tronco(c, w, h + 22), w, d, h, x, y, org=(30, 100), size=(100, 160)); continue
        if id == 'F15': add('decorativos', id, nome, lambda c, w=w, d=d, h=h: d_stone_curb(c, w, d, h), w, d, h, x, y); continue
        if id == 'M01': add('mobiliario', id, nome, lambda c, w=w, d=d, h=h: d_mesa_longa(c, w, d, h), w, d, h, x, y); continue
        if id in ('M02', 'M03', 'M04', 'M05', 'M06', 'M07', 'M15', 'M16', 'M17', 'M18', 'M20'): add('mobiliario', id, nome, lambda c, f=SEAT[id], R=(TIMB if id != 'M20' else TIMB): d_chair(c, 0, 0, f), w, d, h, x, y, org=(16, 40)); continue
        if id in ('M08', 'M19', 'M21'): add('mobiliario', id, nome, lambda c, w=w, d=d, h=h: d_bench(c, w, d, h), w, d, h, x, y); continue
        if id in ('M10', 'M11', 'M12', 'M13', 'M23', 'M24'): add('mobiliario', id, nome, lambda c, w=w, d=d, h=h: d_stool(c, w, d, h), w, d, h, x, y); continue
        if id == 'M09': add('mobiliario', id, nome, lambda c, w=w, d=d, h=h: d_table(c, 0, 0, w, d, h, TIMB, t=2, apron=1), w, d, h, x, y); continue
        if id == 'M14': add('mobiliario', id, nome, lambda c, w=w, d=d, h=h: (d_table(c, 0, 0, w, d, h, TIMB, t=2, apron=2), c.rect(3, 2, w - 6, d - 4, MOSS[1]), c.hline(3, 2, w - 6, MOSS[2]), c.hline(3, d - 3, w - 6, MOSS[0])), w, d, h, x, y); continue
        if id == 'M22': add('equipamentos', id, nome, lambda c, w=w, d=d, h=h: d_lavatorio(c, w, d, h), w, d, h, x, y); continue
        if id == 'M25': add('equipamentos', id, nome, lambda c, w=w, d=d, h=h: d_pilao(c, w, d, h), w, d, h, x, y); continue
        if id == 'M26': add('equipamentos', id, nome, lambda c, w=w, d=d, h=h: d_lenha(c, w, d, h), w, d, h, x, y); continue
        if id == 'M27': add('equipamentos', id, nome, lambda c, w=w, d=d, h=h: d_tabuleiro(c, w, d, h), w, d, h, x, y); continue
        if id.startswith('D'): add('decorativos', id, nome, lambda c, w=w, d=d, h=h: d_vaso(c, w, d, h), w, d, h, x, y); continue
    B = D['BANDEIRA']; bw, bh = round((B['x1'] - B['x0']) * 24), round((B['z1'] - B['z0']) * 24)
    add('decorativos', 'B01', B['nome'], lambda c: d_banner(c, bw, bh), bw, 0, bh, B['x0'], 0, wz=B['z1'], org=(10, 12), size=(80, 100), shadow_on=False, layer='parede', extra={'z_topo': B['z1']})
    T_ = D['TOALHA']; tw, td = round(2.2 * 24), round(2.2 * 16)
    add('decorativos', 'E01', 'Toalha de chita dos sete meninos', lambda c: d_toalha(c, tw, td), tw, td, 0, T_['x0'] + .55 - 0.0, T_['y0'] + .55, org=(4, 4), size=(80, 60), shadow_on=False, layer='chao')
    for it in D['ITENS']:
        sid, nome, zona, sup, x, y, wm, dm, hm, z = it[:10]
        if sid in ('S22', 'E01') or 'toalha' in nome.lower(): continue
        im = draw_item(nome, wm * 24, dm * 16, hm * 24)
        if im is None: continue
        bb = im.getbbox(); im = im.crop(bb)
        SPR.append(dict(sheet='itens', id=sid, nome=nome, im=im, ax=2 - bb[0], h_im=im.height, wx=x, wy=y, wz=z, d=dm * 16, layer='item', w=wm * 24, h=hm * 24, extra=dict(sup=sup, zona=zona), ay_off=bb[3] - 6))
def finalize():
    for s in SPR:
        im = s['im']; L = s['layer']
        if L == 'parede': pos = [SX(s['wx']) - 10, SY(0, s['wz']) - 12]
        elif L == 'chao': pos = [SX(s['wx']) - 4, SY(s['wy'], 0) - 4]
        elif L == 'item': pos = [round(SX(s['wx']) - s['ax']), round(SY(s['wy'] + s['d'] / 16, s['wz']) - im.height)]
        else: pos = [round(SX(s['wx']) - s['ax']), round(SY(s['wy'] + s['d'] / 16, 0) - im.height + 4)]
        s['pos'] = pos
    return SPR

def pack(items, w=512):
    x = y = 2; rowh = 0; pos = {}
    for key, im in items:
        if x + im.width + 2 > w: x = 2; y += rowh + 2; rowh = 0
        pos[key] = (x, y, im.width, im.height); x += im.width + 2; rowh = max(rowh, im.height)
    sheet = Image.new('RGBA', (w, y + rowh + 2), (0, 0, 0, 0))
    for key, im in items: sheet.alpha_composite(im, pos[key][:2])
    return sheet, pos

def stain(c, cx, cy, rx, ry, f, rg, clip=None, n=11):
    """mancha suave: multiplica a cor que já existe (sem recortes duros de cor)"""
    m = Image.new('L', (c.w, c.h), 0); pts = [(cx + math.cos(i / n * math.tau) * rx * (1 + rg.uniform(-.3, .3)), cy + math.sin(i / n * math.tau) * ry * (1 + rg.uniform(-.3, .3))) for i in range(n)]
    ImageDraw.Draw(m).polygon(pts, fill=255); mp = m.load()
    for y in range(max(0, int(cy - ry * 1.4)), min(c.h, int(cy + ry * 1.4) + 1)):
        for x in range(max(0, int(cx - rx * 1.4)), min(c.w, int(cx + rx * 1.4) + 1)):
            if mp[x, y] and (clip is None or clip(x, y)):
                r, g, b, a = c.p[x, y]; c.p[x, y] = (min(255, round(r * f)), min(255, round(g * f)), min(255, round(b * f)), a)
# ============================================================ BASE 720×270
def build_base():
    c = C(W, H); rg = random.Random(11); P = lambda X, Y, Z=0: (SX(X), SY(Y, Z))
    def rect3(X0, Z0, X1, Z1, col, Y=0): a = P(X0, Y, Z1); b = P(X1, Y, Z0); c.rect(a[0], a[1], b[0] - a[0], b[1] - a[1], col)
    # céu e nuvens
    SKY = ramp(200, 0.38, (0.58, 0.64, 0.70, 0.76, 0.82))
    for y in range(0, 150): c.hline(0, y, W, SKY[min(4, y // 32)] if y < 128 else SKY[4])
    for cx, cy, w in ((120, 30, 40), (330, 18, 54), (560, 42, 44)):
        for k, (dx, dy, rw, rh) in enumerate(((0, 0, w, 5), (-w // 3, 2, w // 2, 4), (w // 3, 3, w // 2, 4))): ell(c, cx + dx, cy + dy, rw / 2, rh, SACK[4]); ell(c, cx + dx, cy + dy + 2, rw / 2 - 1, rh - 2, SACK[3])
    # casa de Rita (atrás do muro): parede, telhado de telha, dano com lona azul e balde
    Rt = D['RITA']; bx0, bx1 = SX(Rt['x0']), SX(Rt['x1']); by = SY(Rt['y_beiral'], Rt['z_beiral']); cy = SY(Rt['y_cume'], Rt['z_cume'])
    rect3(Rt['x0'], 0, Rt['x1'], Rt['z_beiral'], CAL[2], Y=Rt['y_beiral']); c.rect(bx0, by - 2, bx1 - bx0, 3, CAL[1])
    for k, y in enumerate(range(cy, by - 2, 3)):
        for x in range(bx0, bx1):
            c.pset(x, y, TELHA[3] if k % 2 else TELHA[2]); c.pset(x, y + 1, TELHA[2] if k % 2 else TELHA[1]); c.pset(x, y + 2, TELHA[1] if k % 2 else TELHA[0])
        for x in range(bx0 + (k % 2) * 4, bx1, 8): c.pset(x, y + 2, TELHA[0]); c.pset(x + 1, y + 1, TELHA[0]); c.pset(x + 2, y, TELHA[3])
    c.rect(bx0, cy - 2, bx1 - bx0, 3, TELHA[3]); c.hline(bx0, cy - 2, bx1 - bx0, TELHA[4]); c.hline(bx0, cy + 1, bx1 - bx0, TELHA[0])
    a, b = SX(Rt['dano_x0']), SX(Rt['dano_x1']); ty = by - 25
    c.poly([(a, ty + 3), (b, ty), (b, by - 3), (a, by - 3)], GLASS[2])
    for k in range(a + 2, b, 6): c.vline(k, ty + 2, by - ty - 5, GLASS[1])
    c.line(a, ty + 3, b, ty, GLASS[4]); c.hline(a, by - 3, b - a, GLASS[0])
    for k in range(4): c.pset(a + 3 + k * 7, ty + 8 + k, SACK[3])
    c.rect(a + 5, ty - 6, 6, 6, STONE[3]); c.hline(a + 5, ty - 6, 6, STONE[4]); c.vline(a + 10, ty - 6, 6, STONE[1]); c.hline(a + 5, ty - 1, 6, STONE[0])
    # parede da casa de Zefa: reboco em manchas, umidade, falha de reboco com tijolo, cornija e rodapé
    rect3(0, 0, 11, 4, CAL[2]); wall = lambda x, y: SX(0) <= x < SX(11) and SY(0, 4) <= y < SY(0, 0)
    for k in range(16):
        stain(c, rg.uniform(SX(0), SX(11)), rg.uniform(SY(0, 3.6), SY(0, 0.8)), rg.uniform(14, 34), rg.uniform(6, 14), 1.04 if k % 2 else 0.95, rg, clip=wall)
    for x in range(SX(0), SX(11)):
        hh = int(13 + 6 * math.sin(x * 0.11) + 3 * math.sin(x * 0.37))
        for k in range(hh): 
            if (x + k) % 3 or k > hh - 5: c.pset(x, SY(0, 0.28) - k, CAL[1] if k > hh - 3 else CAL[2])
    pa = (SX(9.6), SY(0, 1.35)); pb = (SX(11), SY(0, 0.28)); c.poly([(pa[0] + 2, pa[1] + 4), (pa[0] + 14, pa[1]), (pb[0], pa[1] + 6), (pb[0], pb[1]), (pa[0] - 2, pb[1])], BRICK[2])
    for row in range(0, 10):
        for col in range(0, 9):
            x = pa[0] + 1 + col * 5 + (row % 2) * 2; y = pa[1] + 3 + row * 4
            if x < pb[0] and y < pb[1] - 1: c.rect(x, y, 4, 3, BRICK[2 + (row * 7 + col * 3) % 3 % 2 + (1 if (row + col) % 5 == 0 else 0)]); c.hline(x, y, 4, BRICK[3]); c.hline(x, y + 3, 4, BRICK[0])
    for k in range(14): c.pset(pa[0] + k, pa[1] + 2 + (k % 3), CAL[3])
    rect3(0, 0, 11, 0.28, STONE[2]); rect3(0, 0.26, 11, 0.3, STONE[3]); c.hline(SX(0), SY(0, 0.3), SX(11) - SX(0), STONE[4]); c.hline(SX(0), SY(0, 0), SX(11) - SX(0), STONE[0])
    rect3(0, 3.8, 11, 4, CAL[4]); rect3(0, 3.74, 11, 3.8, CAL[1]); c.hline(SX(0), SY(0, 3.74), SX(11) - SX(0), CAL[0])
    for x in range(SX(0), SX(11), 5): c.pset(x, SY(0, 3.8) + 1, CAL[3])
    # muro de divisa com chapim de pedra
    rect3(11, 0, 28, 2.4, CAL[3]); mur = lambda x, y: SX(11) <= x < SX(28) and SY(0, 2.4) <= y < SY(0, 0)
    for k in range(18): stain(c, rg.uniform(SX(11), SX(28)), rg.uniform(SY(0, 2.2), SY(0, 0.2)), rg.uniform(10, 26), rg.uniform(5, 10), 1.03 if k % 2 else 0.95, rg, clip=mur)
    for x in range(SX(11), SX(28)):
        hh = int(7 + 4 * math.sin(x * 0.07) + 2 * math.sin(x * 0.29)); [c.pset(x, SY(0, 0.0) - k, CAL[2]) for k in range(hh) if (x + k) % 3]
    rect3(11, 2.28, 28, 2.4, STONE[3]); c.hline(SX(11), SY(0, 2.4), SX(28) - SX(11), STONE[4]); c.hline(SX(11), SY(0, 2.28), SX(28) - SX(11), STONE[1])
    for x in range(SX(11), SX(28), 13): c.vline(x, SY(0, 2.4), 3, STONE[1])
    rect3(11, 0, 28, 0.22, CAL[1]); c.hline(SX(11), SY(0, 0.22), SX(28) - SX(11), CAL[0])
    for k in range(3): patch(c, rg.uniform(SX(14), SX(26)), SY(0, 0.1), 8, 2, MOSS[1], rg, clip=mur)
    for xx in (SX(0) - 7, SX(28)): c.rect(xx, SY(0, 2.4), 7, SY(8, 0) - SY(0, 2.4), CAL[1]); c.rect(xx, SY(0, 2.4), 7, 2, STONE[3])
    c.rect(0, SY(0, 2.4), SX(0) - 7, SY(8, 0) - SY(0, 2.4), CAL[1]); c.rect(SX(28) + 7, SY(0, 2.4), W - SX(28) - 7, SY(8, 0) - SY(0, 2.4), CAL[1])
    # janela da cozinha
    o = D['OPEN']['janela']
    rect3(o['x0'] - .1, o['z0'] - .1, o['x1'] + .1, o['z1'] + .1, TIMB[1]); rect3(o['x0'], o['z0'], o['x1'], o['z1'], GLASS[3]); rect3(o['x0'], o['z1'] - .45, o['x1'], o['z1'], GLASS[4])
    rect3(o['x0'] + .58, o['z0'], o['x0'] + .62, o['z1'], TIMB[2]); rect3(o['x0'], o['z0'] + .5, o['x1'], o['z0'] + .54, TIMB[2])
    ax = P(o['x0'] + .1, 0, o['z1'] - .1); [c.line(ax[0] + k * 4, ax[1] + 8, ax[0] + k * 4 + 8, ax[1], GLASS[4]) for k in range(0, 3)]
    for sgn in (-1, 1):
        xa, xb = (o['x0'] - .32, o['x0']) if sgn < 0 else (o['x1'], o['x1'] + .32); rect3(xa, o['z0'], xb, o['z1'], WOOD[2])
        for z in range(int(o['z0'] * 24) + 2, int(o['z1'] * 24), 3): c.hline(SX(xa) + 1, SY(0, 0) - z, SX(xb) - SX(xa) - 2, WOOD[1] if (z // 3) % 2 else WOOD[3])
        c.vline(SX(xa), SY(0, o['z1']), int((o['z1'] - o['z0']) * 24), WOOD[4]); c.vline(SX(xb) - 1, SY(0, o['z1']), int((o['z1'] - o['z0']) * 24), WOOD[0])
    rect3(o['x0'] - .15, o['z0'] - .1, o['x1'] + .15, o['z0'] - .03, STONE[4]); rect3(o['x0'] - .15, o['z0'] - .13, o['x1'] + .15, o['z0'] - .1, STONE[1])
    # porta de serviço
    o = D['OPEN']['servico']
    rect3(o['x0'] - .1, 0, o['x1'] + .1, o['h'] + .1, TIMB[1]); rect3(o['x0'], 0, o['x1'], o['h'], WOOD[2]); rect3(o['x0'], 0, o['x0'] + .05, o['h'], WOOD[4]); rect3(o['x1'] - .05, 0, o['x1'], o['h'], WOOD[0])
    for za, zb in ((.18, 1.05), (1.2, o['h'] - .14)):
        rect3(o['x0'] + .14, za, o['x1'] - .14, zb, WOOD[1]); rect3(o['x0'] + .17, za + .03, o['x1'] - .17, zb - .03, WOOD[3]); rect3(o['x0'] + .17, zb - .06, o['x1'] - .17, zb - .03, WOOD[4])
    rect3(o['x1'] - .27, 1.0, o['x1'] - .17, 1.1, STRAW[2]); c.pset(SX(o['x1'] - .24), SY(0, 1.07), STRAW[4]); rect3(o['x0'] - .12, 0, o['x1'] + .12, .06, STONE[4])
    # portão de Rita (de perfil à direita)
    o = D['OPEN']['portao']; c.poly([(SX(28) + 7, SY(o['y0'], 0)), (SX(28) + 7, SY(o['y0'], 1.8)), (SX(28) + 7, SY(o['y1'], 1.8)), (SX(28) + 7, SY(o['y1'], 0))], TIMB[2])
    # piso: lajes de cimento queimado com bisel, juntas, manchas largas, desgaste e trincas
    f0, f1 = P(0, 0), P(28, 8); floor = IRON  # noqa
    FL = ramp(34, 0.13, (0.45, 0.50, 0.55, 0.60, 0.66))
    for X in [i * 1.4 for i in range(20)]:
        for Y in range(8):
            a = P(X, Y); b = P(min(28, X + 1.4), Y + 1); t = rg.random(); col = FL[1] if t < .3 else FL[2] if t < .7 else FL[3]
            c.rect(a[0], a[1], b[0] - a[0], b[1] - a[1], col); c.hline(a[0], a[1], b[0] - a[0], FL[4]); c.vline(a[0], a[1], b[1] - a[1], FL[3] if col != FL[3] else FL[4]); c.hline(a[0], b[1] - 1, b[0] - a[0], FL[0]); c.vline(b[0] - 1, a[1], b[1] - a[1], FL[0])
    flo = lambda x, y: f0[0] <= x < f1[0] and f0[1] <= y < f1[1]
    for k in range(16): stain(c, rg.uniform(f0[0], f1[0]), rg.uniform(f0[1], f1[1]), rg.uniform(16, 40), rg.uniform(4, 9), 1.04 if k % 2 else 0.93, rg, clip=flo)
    for k in range(6):
        x = rg.uniform(f0[0] + 10, f1[0] - 40); y = rg.uniform(f0[1] + 14, f1[1] - 10)
        for i in range(5): nx, ny = x + rg.randint(3, 7), y + rg.randint(-2, 2); c.line(int(x), int(y), int(nx), int(ny), FL[0]); x, y = nx, ny
    # soleira (corredor da rua): faixa mais clara
    s_ = D['OPEN']['soleira']; a = P(s_['x0'], 4.6); b = P(s_['x1'], 8); c.shade(a[0], a[1], b[0] - a[0], b[1] - a[1], (0.95, 0.94, 0.97), mask=None)
    # sombra da mangueira (projetada no chão)
    m = D['MANGA']; cx, cy = P(m['copa_c'][0] + .3, m['copa_c'][1] + 1.0)
    for r, f in ((70, .90), (58, .88), (44, .88)):
        for y in range(cy - 36, cy + 36):
            for x in range(cx - 74, cx + 74):
                if ((x - cx) / r) ** 2 + ((y - cy) / (r * 0.48)) ** 2 <= 1 and 0 <= x < W and 0 <= y < H and y > SY(0, 0):
                    rr, g, bl, al = c.p[x, y]; c.p[x, y] = (round(rr * f), round(g * f), round(bl * f * 1.03), 255)
    # calçada de pedra
    for y in range(f1[1], H): c.hline(0, y, W, STONE[2])
    for r, y in enumerate(range(f1[1], H, 7)):
        c.hline(0, y, W, STONE[1])
        for x in range((r % 2) * 14, W, 28): c.vline(x, y, 7, STONE[1])
        for x in range(0, W, 28): c.hline(x + (r % 2) * 14 + 1, y + 1, 12, STONE[3])
    c.hline(0, f1[1], W, STONE[4])
    c.rect(SX(s_['x0']), f1[1] - 3, SX(s_['x1']) - SX(s_['x0']), 8, STONE[4]); c.hline(SX(s_['x0']), f1[1] - 3, SX(s_['x1']) - SX(s_['x0']), SACK[4]); c.hline(SX(s_['x0']), f1[1] + 4, SX(s_['x1']) - SX(s_['x0']), STONE[2]); c.vline(SX(s_['x0']), f1[1] - 3, 8, STONE[3]); c.vline(SX(s_['x1']) - 1, f1[1] - 3, 8, STONE[2])
    return c

def build_copa():
    c = C(W, H); rg = random.Random(5); HL = D['HULL']; mask = Image.new('L', (W, H), 0); ImageDraw.Draw(mask).polygon([tuple(p) for p in HL], fill=255); mp = mask.load()
    xs = [p[0] for p in HL]; ys = [p[1] for p in HL]; x0, x1, y0, y1 = min(xs), max(xs), min(ys), max(ys)
    cl = sorted([(rg.uniform(x0, x1), rg.uniform(y0, y1), rg.uniform(6, 12)) for _ in range(170)], key=lambda t: t[1])
    for x in range(int(x0), int(x1) + 1):
        for y in range(int(y0), int(y1) + 1):
            if mp[x, y]: c.pset(x, y, LEAF[1])
    for (x, y, r) in cl:
        lit = 0.5 * (1 - (y - y0) / (y1 - y0)) + 0.5 * (1 - (x - x0) / (x1 - x0))
        for (dy, rr, col) in ((2, r, LEAF[0]), (0, r, LEAF[3] if lit > .62 else LEAF[2] if lit > .36 else LEAF[1]), (-r * .28, r * .45, LEAF[4] if lit > .5 else LEAF[3])):
            for yy in range(int(y + dy - rr * .7), int(y + dy + rr * .7) + 1):
                for xx in range(int(x - rr), int(x + rr) + 1):
                    if 0 <= xx < W and 0 <= yy < H and mp[xx, yy] and ((xx - x) / rr) ** 2 + ((yy - y - dy) / (rr * .7)) ** 2 <= 1: c.pset(xx, yy, col)
    for k in range(60): 
        x, y = int(rg.uniform(x0, x1)), int(rg.uniform(y0, y1))
        if mp[x, y]: c.hline(x, y, 3, LEAF[0])
    for k in range(9):
        x, y = int(rg.uniform(x0 + 14, x1 - 14)), int(rg.uniform(y0 + (y1 - y0) * .5, y1 - 6))
        if mp[x, y]: c.rect(x, y, 3, 4, STRAW[2]); c.vline(x, y, 4, STRAW[3]); c.hline(x, y + 3, 3, STRAW[1]); c.pset(x + 1, y - 1, LEAF[2])
    for y in range(int(y0), int(y1) + 1):          # contorno escuro só onde falta vizinho
        for x in range(int(x0), int(x1) + 1):
            if mp[x, y] and (not mp[x - 1, y] or not mp[x + 1, y] or not mp[x, y - 1] or not mp[x, y + 1]): c.pset(x, y, LEAF[0])
    return c

def main():
    build_objs(); finalize()
    build_base().save(OUT + 'quintal_base.png'); build_copa().save(OUT + 'mangueira_copa.png')
    cat = {}; 
    for sheet in ('mobiliario', 'equipamentos', 'decorativos', 'itens'):
        lst = [s for s in SPR if s['sheet'] == sheet]; im, pos = pack([(s['id'], s['im']) for s in lst], 512 if sheet != 'mobiliario' else 640); im.save(OUT + sheet + '.png')
        for s in lst: cat[s['id']] = dict(folha=sheet + '.png', rect=list(pos[s['id']]), pos_px=s['pos'], mundo=dict(x=s['wx'], y=s['wy'], z=s['wz']), layer=s['layer'], nome=s['nome'], **s['extra'])
    json.dump(dict(unidade='1 m = 24 px (X e altura); 16 px/m (profundidade). pos_px = canto superior esquerdo do sprite em px do mundo (720x270). Ordem de desenho: pela base (y + profundidade).', camera='3/4 oblíqua', base='quintal_base.png', copa='mangueira_copa.png', sprites=cat),
              open(OUT + 'catalog_quintal.json', 'w'), indent=1, ensure_ascii=False)
    return cat

if __name__ == '__main__':
    cat = main(); print(len(cat), 'sprites')

def preview(fase='C'):
    """composição estática: base + objetos ordenados pela base + itens + Lia (escala) + copa. Fase C = adultos à mesa (sem toalha dos meninos)."""
    cat = json.load(open(OUT + 'catalog_quintal.json'))['sprites']; base = Image.open(OUT + 'quintal_base.png').convert('RGBA'); sheets = {n: Image.open(OUT + n + '.png').convert('RGBA') for n in ('mobiliario', 'equipamentos', 'decorativos', 'itens')}
    lst = []
    for k, v in cat.items():
        if k.endswith('#1') or (k == 'M27' and False): continue
        if k.startswith('E') and k != 'E01' and fase != 'C1': continue
        if k == 'E01' and fase != 'C1': continue
        x, y, w, h = v['rect']; im = sheets[v['folha'][:-4]].crop((x, y, x + w, y + h))
        o = next((q for q in D['OBJ'] if q[0] == k.split('#')[0]), None)
        key = (o[4] + o[6]) if o else (v['mundo']['y'] + 0.01 + (0 if v['layer'] != 'item' else 0.5)); 
        if v['layer'] == 'item':
            sup = next((q for q in D['OBJ'] if q[0] == v.get('sup')), None); key = (sup[4] + sup[6] + 0.002) if sup else v['mundo']['y'] + .5
        if v['layer'] == 'parede': key = 0.0
        if v['layer'] == 'chao': key = -0.5
        lst.append((key, v['pos_px'], im))
    # Lia (escala 1,50 m) em frente à mesa e um adulto de 1,75 m
    a = json.load(open('../assets/chars/lia_tq.json')); li = Image.open('../assets/chars/lia_tq.png').convert('RGBA'); cw, ch = a['cell']; r = a['rows']['idle/down']; pd = a['pad']
    fr = li.crop((pd, pd + r['row'] * (ch + 2 * pd) if False else pd + r['row'] * (ch + pd), pd + cw, pd + r['row'] * (ch + pd) + ch)) if False else None
    lst.sort(key=lambda t: t[0])
    for _, p, im in lst: base.alpha_composite(im, (max(0, p[0]), max(0, p[1])))
    base.alpha_composite(Image.open(OUT + 'mangueira_copa.png').convert('RGBA'), (0, 0))
    return base
if __name__ == '__main__':
    for f in ('C', 'C1'): preview(f).resize((1440, 540), Image.NEAREST).save(OUT + f'quintal_preview_{f}.png')

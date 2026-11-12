"""Etapa 6 — rua: fachadas (as mesmas da Etapa 1), chão novo (calçada funda, meio-fio, paralelepípedo variado),
elementos fixos das fachadas (letreiros, lampiões, vasos, trepadeiras, varal) e camada da frente (fios)."""
import random, math, json, sys
from pxl import *
from facade import *
import street as ST
from rua6_art import *
from rua6_font import text, width

W = 1130; VW, VH = 480, 270
def yw(x): return 212 + int(max(0, x)) // 70          # contato parede/calçada (a rua desce à direita, mais suave que na Etapa 1)
SW = 22; CB = 4; GT = 2                               # calçada 22 px (~1,4 m), meio-fio 4, sarjeta 2
def walk_top(x): return yw(x) + 8                     # primeiro y onde os pés pisam (encostado na parede)
def walk_bot(x): return VH - 3

S = STONE
def ground6(rng):
    h = 70; s = C(W, h)
    # --- calçada: duas fiadas de lajes de cantaria desencontradas
    rows = [(2, 11), (12, SW - 1)]
    for (ya, yb) in rows:
        x = -rng.randint(0, 20) - (12 if ya > 5 else 0)
        while x < W:
            lw = rng.randint(26, 46); tone = rng.choice([S[3], S[3], S[3], S[2], mix(S[3], (150, 140, 120), .25)])
            for xx in range(max(0, x), min(W, x + lw)):
                for y in range(ya, yb + 1): s.pset(xx, y, tone)
                s.pset(xx, ya, S[4] if tone != S[2] else S[3])               # face de cima iluminada
                s.pset(xx, yb, S[1])                                         # junta inferior
            if 0 <= x + lw - 1 < W:
                for y in range(ya, yb + 1): s.pset(x + lw - 1, y, S[1])
            # pequenas variações: lasca e rachadura curta
            if rng.random() < 0.28 and lw > 30:
                cx = x + rng.randint(6, lw - 8); cy = rng.randint(ya + 2, yb - 2)
                for k in range(rng.randint(3, 6)): s.pset(cx + k // 2, cy + k, S[1])
            x += lw
    for xx in range(W): s.pset(xx, 0, S[0]); s.pset(xx, 1, S[1])             # contato com a parede
    # --- meio-fio de granito
    y = SW
    for xx in range(W):
        s.pset(xx, y, S[4]); s.pset(xx, y + 1, mix(S[4], S[3], .5)); s.pset(xx, y + 2, S[2]); s.pset(xx, y + 3, S[1])
    x = 0
    while x < W:
        x += rng.randint(40, 70)
        for j in range(4): s.pset(min(W - 1, x), y + j, S[0])
    for xx in range(W): s.pset(xx, y + 4, S[0]); s.pset(xx, y + 5, S[1])   # sarjeta
    # --- paralelepípedo
    COB = [S[1], S[2], S[2], S[3], mix(S[2], (120, 100, 96), .35), mix(S[1], (96, 82, 84), .4)]
    JOINT = mix(S[0], (50, 40, 40), .5)
    y0 = y + 6
    for yy in range(y0, h):
        for xx in range(W): s.pset(xx, yy, JOINT)
    yy = y0
    while yy < h:
        rh = rng.choice([6, 6, 7]); xx = -rng.randint(0, 9)
        while xx < W:
            sw = rng.randint(8, 12); col = rng.choice(COB)
            for j in range(rh - 1):
                for i in range(sw - 1):
                    if (j in (0, rh - 2)) and (i in (0, sw - 2)): continue
                    s.pset(xx + i, yy + j, col)
            for i in range(1, sw - 3): s.pset(xx + i, yy, mix(col, (230, 220, 210), .22))
            for i in range(1, sw - 2): s.pset(xx + i, yy + rh - 2, mix(col, (30, 26, 40), .35))
            xx += sw
        yy += rh
    return s

def compose(seed=1991):
    rng = random.Random(seed)
    world = C(W, VH); placed = []
    for i, (name, x0, spec) in enumerate(ST.BUILDINGS):
        b, info = ST.build(name, spec, 100 + i)
        xref = x0 + info.get('door_x', info['w'] // 2)
        ytop = yw(xref) - info['y0']
        world.paste(b, x0, ytop)
        info.update(x0=x0, xref=xref, ytop=ytop, name=name, base=yw(xref)); placed.append(info)
    gs = ground6(rng)
    for x in range(W):
        top = yw(x)
        for y in range(top, VH):
            sy = min(y - top, gs.h - 1); r, g, b, a = gs.p[x, sy]; world.p[x, y] = (r, g, b, 255)
    return world, placed, gs

# ------------------------------------------------------------------ ajudantes de posição em relação ao chão
def put(c, x, sy, col):                    # pixel na faixa do chão: sy = linha dentro da faixa (0 = encosto da parede)
    c.pset(x, yw(x) + sy, col)
def hput(c, x, w, sy, col):
    for xx in range(x, x + w): put(c, xx, sy, col)
def rput(c, x, w, sy0, h, col):
    for k in range(h): hput(c, x, w, sy0 + k, col)

def ground_features(world, rng):
    # 1) ladrilho hidráulico na soleira de três portas (desenho geométrico gasto)
    def ladrilho(xc, w, sy0, h, cA, cB, cC):
        for i in range(w):
            for j in range(h):
                u, v = i % 6, j % 6
                if (u in (0, 5) or v in (0, 5)): col = cC
                elif (u in (1, 4) or v in (1, 4)): col = cA
                else: col = cB
                if (i // 6 + j // 6) % 2: col = cA if col == cB else cB if col == cA else col
                if rng.random() < 0.05: col = mix(col, (150, 140, 120), .5)
                put(world, xc - w // 2 + i, sy0 + j, col)
    ladrilho(164, 36, 3, 12, (138, 74, 58), (222, 208, 176), (58, 52, 60))
    ladrilho(756, 42, 3, 12, (58, 92, 126), (226, 214, 184), (52, 52, 64))
    for xx in range(444, 497): rput(world, xx, 1, 2, 4, mix(S[3], (60, 50, 60), .18)) if False else None
    # soleira de granito da padaria (laje contínua mais clara)
    for xx in range(440, 500):
        for sy in range(2, 8): put(world, xx, sy, S[4] if sy == 2 else S[3] if sy < 7 else S[1])
    # 2) remendos de cimento (restauro) — mais claros e lisos, com borda irregular
    for (xc, w, sy0, h) in [(350, 34, 4, 9), (610, 28, 12, 8), (1010, 40, 3, 11)]:
        for i in range(w):
            for j in range(h):
                if (i in (0, w - 1) and rng.random() < .4): continue
                put(world, xc - w // 2 + i, sy0 + j, mix(S[3], (214, 204, 186), .55) if j else mix(S[4], (230, 222, 206), .5))
        for i in range(2, w - 2, 7): put(world, xc - w // 2 + i, sy0 + h // 2, S[2])
    # 3) mato nas frestas (capim, tufos de trevo) e musgo nas bordas das lajes
    for _ in range(46):
        x = rng.randint(4, W - 4); sy = rng.choice([1, 11, 12, 21, SW + 1])
        if sy in (1, 21, SW + 1) or rng.random() < .3:
            _ = (rng.randint(3, 5), rng.randint(3, 6), rng.choice([LEAF2, LEAF]))   # rev.: sem mato nas frestas da calçada
    # 4) bueiros de ferro na sarjeta e tampa de ferro redonda na rua
    for xc in (562, 905):
        rput(world, xc - 9, 18, SW + 4, 2, S[0])
        for i in range(0, 18, 3): hput(world, xc - 9 + i, 1, SW + 4, FERRO[3]) if False else put(world, xc - 9 + i, SW + 4, FERRO[3])
    xc = 382; yc = yw(xc) + SW + 22
    for yy in range(-4, 5):
        for xx in range(-9, 10):
            if (xx / 9.5) ** 2 + (yy / 4.5) ** 2 <= 1:
                d = (xx / 9.5) ** 2 + (yy / 4.5) ** 2
                col = FERRO[1] if d > .75 else FERRO[2] if (xx + yy) % 4 else FERRO[3]
                world.pset(xc + xx, yc + yy, col)
    for xx in range(-6, 7, 3): world.pset(xc + xx, yc, FERRO[4])
    # 5) remendo de asfalto na rua (reparo de concessionária)
    ax, aw, ay0, ah = 748, 56, 14, 11
    for i in range(aw):
        for j in range(ah):
            u = abs(i - aw / 2) / (aw / 2); v = abs(j - ah / 2) / (ah / 2)
            if u ** 2.4 + v ** 2.4 <= 1 + rng.uniform(-.12, .1):
                x = ax + i; world.pset(x, yw(x) + SW + ay0 + j, (52, 50, 58) if (i + j) % 7 else (62, 60, 68))
    # 6) mancha de umidade na sarjeta (água de lavagem) e casca de laranja / folhas secas pequenas
    for _ in range(26):
        x = rng.randint(6, W - 6); sy = SW + rng.choice([5, 6, 8, 12, 16])
        world.pset(x, yw(x) + sy, rng.choice([(150, 110, 60), (118, 138, 70), (196, 150, 64)]))

# ------------------------------------------------------------------ elementos das fachadas
def wy(b, h):                                  # y do mundo, h px acima do chão da fachada
    return b['base'] - h

def lampiao(c, x, y):
    """Lampião de ferro fixado na parede (vista frontal): braço, caixa de vidro, cúpula."""
    c.rect(x - 3, y - 2, 7, 1, FERRO[2]); c.rect(x - 1, y - 5, 3, 3, FERRO[1]); c.pset(x, y - 1, FERRO[0])        # suporte na parede
    c.rect(x - 3, y, 7, 2, FERRO[3]); c.pset(x - 3, y, FERRO[4])
    for j in range(7):
        c.rect(x - 2, y + 2 + j, 5, 1, (228, 196, 110) if j > 1 else (240, 220, 150))
    c.vline(x - 3, y + 2, 7, FERRO[2]); c.vline(x + 3, y + 2, 7, FERRO[1]); c.vline(x, y + 2, 7, mix((230, 200, 120), FERRO[2], .5))
    c.rect(x - 3, y + 9, 7, 1, FERRO[2]); c.rect(x - 2, y + 10, 5, 1, FERRO[1]); c.pset(x, y + 11, FERRO[1])
    c.rect(x - 4, y - 1, 9, 1, FERRO[3]); c.rect(x - 2, y - 2, 5, 1, FERRO[4])

def placa_pintada(c, x, y, w, h, s, bg, ink, rng, gasto=4):
    """Letreiro pintado à mão sobre tábua: moldura, filete, letras claras e desgaste."""
    c.rect(x, y, w, h, bg[2]); c.hline(x, y, w, bg[3]); c.vline(x, y, h, bg[3]); c.vline(x + w - 1, y, h, bg[1]); c.hline(x, y + h - 1, w, bg[1])
    tx = x + (w - width(s)) // 2
    text(c, tx + 1, y + (h - 7) // 2 + 1, s, bg[0], 1)
    text(c, tx, y + (h - 7) // 2, s, ink, 1)
    for _ in range(gasto): c.pset(x + rng.randint(2, w - 3), y + rng.randint(2, h - 3), bg[2])
    c.shade(x, y + h, w, 2, SH2)

def azulejo_placa(c, x, y, s, rng):
    w = width(s) + 6; h = 11
    c.rect(x, y, w, h, (236, 232, 218)); c.hline(x, y, w, (252, 250, 240)); c.vline(x, y, h, (252, 250, 240)); c.hline(x, y + h - 1, w, (188, 184, 170)); c.vline(x + w - 1, y, h, (188, 184, 170))
    c.rect(x + 1, y + 1, w - 2, 1, (46, 74, 130)); c.rect(x + 1, y + h - 2, w - 2, 1, (46, 74, 130))
    text(c, x + 3, y + 2, s, (30, 52, 104), 1)
    c.pset(x + 2, y + 5, (200, 196, 180)); c.shade(x, y + h, w, 2, SH2)

def gaiola(c, x, y, rng):
    """Gaiola de passarinho pendurada (arame e madeira) com pássaro dentro."""
    c.vline(x, y - 8, 8, FERRO[3]); c.pset(x - 1, y - 8, FERRO[3]); c.pset(x + 1, y - 8, FERRO[3])
    c.rect(x - 4, y, 9, 1, WOOD[3]); c.rect(x - 3, y - 2, 7, 2, FERRO[3]); c.pset(x, y - 3, FERRO[3]); c.pset(x, y - 4, FERRO[4])
    for j in range(1, 9):
        c.pset(x - 4, y + j, FERRO[3]); c.pset(x + 4, y + j, FERRO[1])
        for i in (-2, 0, 2): c.pset(x + i, y + j, mix(FERRO[2], (200, 190, 170), .2) if j % 3 else FERRO[1])
    c.rect(x - 4, y + 9, 9, 2, WOOD[2]); c.hline(x - 4, y + 9, 9, WOOD[4])
    c.rect(x - 1, y + 5, 3, 3, (220, 170, 40)); c.pset(x - 2, y + 5, (230, 190, 60)); c.pset(x + 1, y + 5, (30, 20, 20)); c.pset(x + 2, y + 6, (200, 120, 30))   # canário
    c.hline(x - 3, y + 8, 7, WOOD[4])

def vasos_peitoril(c, x, ysill, rng, kinds):
    """Vasos sobre o peitoril: lata, barro, jardineira (vista frontal)."""
    xx = x
    for k in kinds:
        if k == 'lata':
            can_pot(c, xx, ysill, 6, 6, rng.choice([LATA, LATA2]), rng); fern(c, xx, ysill - 6, 6, 8, rng, LEAF2); xx += 9
        elif k == 'barro':
            pot_clay(c, xx, ysill, 7, 6); leafmass(c, xx, ysill - 11, 5, 5, rng, LEAF, n=8); flower_dots(c, xx, ysill - 11, 5, 4, rng, FLOR_V, 5); xx += 10
        elif k == 'jard':
            c.rect(xx - 9, ysill - 5, 18, 5, WOOD[2]); c.hline(xx - 9, ysill - 5, 18, WOOD[4]); c.hline(xx - 9, ysill - 1, 18, WOOD[0]); c.vline(xx - 9, ysill - 5, 5, WOOD[3])
            leafmass(c, xx, ysill - 9, 9, 5, rng, LEAF, n=18); flower_dots(c, xx, ysill - 10, 8, 4, rng, rng.choice([FLOR_V, FLOR_M, FLOR_A]), 9); xx += 20

def samambaia_pendurada(c, x, y, rng):
    c.vline(x - 3, y - 12, 12, FERRO[3]); c.vline(x + 3, y - 12, 12, FERRO[3]); c.pset(x, y - 13, FERRO[3])
    c.line(x - 3, y - 12, x, y - 13, FERRO[3]); c.line(x + 3, y - 12, x, y - 13, FERRO[3])
    pot_clay(c, x, y + 5, 8, 5)
    fern(c, x, y, 9, 11, rng, LEAF2, droop=True)
    for i in range(-6, 7, 3): c.vline(x + i, y + 1, rng.randint(4, 9), LEAF2[2] if i % 2 else LEAF2[1])

def trepadeira(c, x0, x1, ytop_fn, ybase_fn, rng, ramp_=LEAF, flor=FLOR_M, dens=0.9, clip=None):
    """Planta que sobe pela parede/muro (bougainville): massa irregular + flores."""
    x = x0
    while x < x1:
        top = ytop_fn(x) + rng.randint(-2, 2); base = ybase_fn(x)
        for y in range(int(top), int(base)):
            if clip and not clip(x, y): continue
            if rng.random() < dens * (1 if y - top < 14 else .5):
                k = 3 if rng.random() < .22 else 2 if rng.random() < .6 else 1
                c.pset(x, y, ramp_[k])
        x += 1
    for _ in range(int((x1 - x0) * 0.55)):
        px = rng.randint(x0, x1 - 1); py = ytop_fn(px) + rng.randint(0, 18)
        if clip and not clip(px, py): continue
        if c.get(px, py)[3]:
            c.pset(px, py, flor[3]); c.pset(px + 1, py, flor[2]); c.pset(px, py + 1, flor[1]) if rng.random() < .5 else None
            if rng.random() < .4: c.pset(px - 1, py - 1, flor[4])

def cartaz(c, x, y, w, h, cols, rng):
    c.rect(x, y, w, h, cols[0]); c.hline(x, y, w, cols[1]); c.vline(x + w - 1, y, h, mix(cols[0], (40, 30, 40), .3)); c.hline(x, y + h - 1, w, mix(cols[0], (40, 30, 40), .3))
    for j in range(2, h - 2, 3):
        L = rng.randint(w // 3, w - 4); c.hline(x + 2, y + j, L, cols[2])
    c.pset(x, y, (210, 200, 180))
    c.shade(x + w, y + 1, 1, h, SH2)

def fiacao(front, placed, rng):
    """Camada da frente: postes ligados por fios com catenária, fios que entram nas fachadas, isoladores."""
    wires = []
    def cat(x0, y0, x1, y1, sag, col=(34, 30, 40)):
        n = abs(x1 - x0) + 1
        pts = []
        for i in range(n):
            t = i / max(1, n - 1); x = x0 + (x1 - x0) * t; y = y0 + (y1 - y0) * t + sag * 4 * t * (1 - t)
            pts.append((round(x), round(y)))
        for (px, py) in pts: front.pset(px, py, col)
        for (px, py) in pts[::2]:
            front.pset(px, py - 1, (*col[:3], 90)) if rng.random() < .0 else None
    return cat

def build_world():
    rng = random.Random(1991)
    world, placed, gs = compose()
    ground_features(world, rng)
    B = {p['name']: p for p in placed}
    # ---------- b0 (casa baixa bege): barbearia
    b = B['b0']
    placa_pintada(world, 72 - 29, wy(b, 82), 58, 11, 'BARBEARIA', ramp(150, .30, (.14, .22, .30, .38, .46)), (244, 234, 206), rng)
    lampiao(world, 98, wy(b, 60))
    # hera/trepadeira no parapeito da casa baixa bege (esquerda): pendurada
    trepadeira(world, 6, 40, lambda x: wy(b, 88) + 1, lambda x: wy(b, 88) + 12 + (x * 7) % 5, rng, LEAF, FLOR_B, .75)
    # ---------- sobrado de Seu Raimundo
    b = B['sobrado']
    lampiao(world, 137, wy(b, 62))
    gaiola(world, 190, wy(b, 60), rng)
    azulejo_placa(world, 138, wy(b, 52), 'N 12', rng) if False else None
    vasos_peitoril(world, 233, wy(b, 24), rng, ['lata', 'barro'])
    samambaia_pendurada(world, 164 - 12, wy(b, 108) , rng)             # sacada
    samambaia_pendurada(world, 240 + 10, wy(b, 108), rng)
    # número da casa, em azulejo, ao lado da porta
    c = world; x = 183; y = wy(b, 42)
    c.rect(x, y, 11, 9, (236, 232, 218)); c.rect(x, y, 11, 1, (252, 250, 240)); c.rect(x + 1, y + 1, 9, 7, (232, 226, 210)); text(c, x + 2, y + 1, '2', (30, 52, 104), 1) if False else None
    c.hline(x, y + 8, 11, (180, 176, 160)); c.pset(x + 1, y + 1, (46, 74, 130)); c.pset(x + 9, y + 1, (46, 74, 130)); c.pset(x + 1, y + 7, (46, 74, 130)); c.pset(x + 9, y + 7, (46, 74, 130))
    text(c, x + 3, y + 1, '1', (30, 52, 104), 1) if False else None
    for i, ch in enumerate('12'): text(c, x + 1 + i * 5 - (1 if i else 0), y + 1, ch, (30, 52, 104), 0)
    # ---------- padaria
    b = B['padaria']
    lampiao(world, 437, wy(b, 60)); lampiao(world, 503, wy(b, 60))
    samambaia_pendurada(world, 290 + 108, wy(b, 108), rng)
    samambaia_pendurada(world, 290 + 252, wy(b, 108), rng)
    vasos_peitoril(world, 290 + 99, wy(b, 24), rng, ['lata']) if False else None
    cartaz(world, 556, wy(b, 52), 12, 16, [(214, 84, 66), (240, 120, 100), (252, 232, 200)], rng)    # cartaz de festa (lambe-lambe)
    cartaz(world, 574, wy(b, 50), 11, 14, [(236, 200, 70), (250, 224, 120), (120, 60, 30)], rng)
    # ---------- associação (casa azul)
    b = B['azul']
    placa_pintada(world, 756 - 36, wy(b, 83), 72, 11, 'ASSOCIACAO', ramp(210, .55, (.16, .25, .34, .43, .52)), (244, 234, 206), rng)
    lampiao(world, 726, wy(b, 60))
    azulejo_placa(world, 660, wy(b, 88), 'R. DA PAZ', rng)
    # quadro de avisos fica como objeto (sprite); aqui só a sombra de pregos
    # ---------- casa verde
    b = B['verde']
    vasos_peitoril(world, 810 + 94, wy(b, 24), rng, ['barro', 'lata'])
    lampiao(world, 877, wy(b, 60))
    # ---------- b5 (casa baixa rosa): trepadeira florida no parapeito e plantas nas janelas
    b = B['b5']
    pt = lambda x: wy(b, 88)
    trepadeira(world, 955, 1010, lambda x: wy(b, 88) - 1, lambda x: wy(b, 88) + 8 + (x * 5) % 17, rng, LEAF, FLOR_M, .9)
    vasos_peitoril(world, 950 + 118, wy(b, 26), rng, ['jard'])
    # varal junto à parede da casa rosa (peças dobradas pelo vento: sem animação, só desenho)
    xa, xb, y_l = 1040, 1118, wy(b, 60)
    for x in range(xa, xb): world.pset(x, y_l + (2 if 20 < x - xa < 58 else 1 if 8 < x - xa < 70 else 0), (46, 38, 44))
    world.rect(xa - 1, y_l - 3, 2, 6, FERRO[2]); world.rect(xb, y_l - 3, 2, 6, FERRO[2])
    cloth(world, xa + 6, y_l + 2, 9, 12, ramp(200, .45, (.28, .38, .50, .60, .70)), rng, 'shirt')
    cloth(world, xa + 20, y_l + 3, 8, 14, ramp(352, .50, (.34, .44, .56, .66, .76)), rng, 'towel')
    cloth(world, xa + 34, y_l + 4, 14, 11, ramp(46, .20, (.70, .80, .88, .93, .97)), rng, 'sheet')
    cloth(world, xa + 54, y_l + 2, 9, 12, ramp(46, .70, (.40, .52, .62, .72, .82)), rng, 'shirt')
    cloth(world, xa + 68, y_l + 1, 7, 10, ramp(120, .40, (.24, .34, .46, .56, .66)), rng, 'towel')
    return world, placed, B

if __name__ == '__main__':
    world, placed, B = build_world()
    world.save('/tmp/world6.png')
    print([(p['name'], p['x0'], p['base']) for p in placed])

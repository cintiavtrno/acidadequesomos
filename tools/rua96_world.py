"""Etapa B de 1996 — cenário-base da rua: fachadas em renovação desigual + piso, sem personagens e sem objetos da gravação.
Reaproveita o gerador de 1991 (facade.py, rua6_world.py). A composição (beirais, dois pavimentos, larguras, faixas de calçada/rua) é a aprovada;
muda a conservação, a paleta e os acabamentos. Saída em ../assets/street96/."""
import random, math, json, os, colorsys
from PIL import Image
from pxl import *
import facade as F
import rua6_world as RW
from rua6_art import *
from rua6_font import text, width

W = 1500; VW, VH = 480, 270; SW = 22
SLOPE_BASE, SLOPE_DIV = 212, 110                      # rua mais plana que em 1991 (div 70): o palco de 400 px mantém profundidade
def yw(x): return SLOPE_BASE + int(max(0, x)) // SLOPE_DIV
RW.W = W; RW.yw = yw                                  # o gerador de chão de 1991 lê estas globais

# ------------------------------------------------------------------ paleta (referências do briefing, aplicadas com variação)
HEX = {'rosa_q': '#D58C79', 'amarelo': '#E5C46D', 'salvia': '#8FB9A7', 'azul': '#7D9FBD', 'creme': '#E8DFC9', 'agua': '#9ABCB4', 'rosa_a': '#D18FA5', 'lilas': '#B7A2C6'}
def hexrgb(h): return tuple(int(h[i:i + 2], 16) for i in (1, 3, 5))
def wall_ramp(hx, dl=0.0, ds=1.0):
    r, g, b = [v / 255 for v in hexrgb(hx)]; h, l, s = colorsys.rgb_to_hls(r, g, b)
    l = max(.3, min(.9, l + dl)); s = min(1, s * ds)
    return ramp(h * 360, s, (l - .24, l - .12, l, l + .08, l + .15))
def old_ramp(hx):   # a mesma cor, mais gasta: dessaturada, um pouco mais escura e mais quente
    r, g, b = [v / 255 for v in hexrgb(hx)]; h, l, s = colorsys.rgb_to_hls(r, g, b)
    return ramp(h * 360 + 3, s * .62, (l - .31, l - .19, l - .07, l + .02, l + .10))

TR_NEW = ramp(46, .16, (.58, .70, .82, .91, .97))             # molduras recém-pintadas
TR_CREAM = ramp(46, .20, (.52, .64, .76, .86, .94))
TR_BLUE = ramp(210, .30, (.36, .48, .60, .72, .82))
WD = {'verde': ramp(165, .30, (.13, .21, .31, .41, .52)), 'azul': ramp(208, .50, (.20, .31, .43, .55, .68)), 'marrom': ramp(28, .42, (.16, .25, .36, .47, .58)),
      'ocre': ramp(36, .55, (.22, .33, .45, .57, .68)), 'vinho': ramp(350, .38, (.14, .22, .32, .42, .52)), 'gasto': ramp(26, .22, (.16, .24, .33, .42, .52))}
IRON_NEW = ramp(235, .10, (.06, .10, .16, .24, .34))
TELHA_NEW = ramp(14, .55, (.26, .38, .50, .62, .72))

# ------------------------------------------------------------------ construtor de fachada (parametrizado por estado de conservação)
def build96(name, s, seed):
    rng = random.Random(seed)
    state = s['state']; w = s['w']
    wall = wall_ramp(HEX[s['hex']], dl=s.get('dl', 0)); old = old_ramp(HEX[s['hex']])
    if state == 'gasto': wall = old
    trim = s['trim']; wood = WD[s['wood']]
    F.IRON = IRON_NEW if state != 'gasto' else F.IRON0; F.TELHA = TELHA_NEW if state in ('novo', 'rest') else F.TELHA0
    T = 22; H0 = 94; H1 = 79; y_str = T + H1; y0 = y_str + 3 + H0; fh = y0 + 44
    c = C(w, fh)
    F.make_wall(c, 0, T, w, fh - T, wall, rng)
    inside = lambda x, y: 0 <= x < w and T + 3 <= y < y0 - 10
    if state == 'parcial':      # tinta nova em cima, reboco antigo embaixo, divisa irregular
        cut = F._smooth_heights(0, w, rng, 0, 14, 13)
        base = y0 - s.get('old_h', 60)
        for i in range(w):
            for yy in range(base + cut[i], y0 + 4):
                if inside(i, yy): c.pset(i, yy, old[2])
        c.vline(0, base, y0 - base, old[3]); c.vline(w - 1, base, y0 - base, old[1])
    c.shade(0, y0 - 40, w, 28, (0.97, 0.97, 0.99))
    for (rx, ry, rw, rh) in s.get('repaint', []): F.repaint(c, rx, ry, rw, rh, s.get('rp_light', True), rng, inside)
    if state == 'gasto':
        F.wear_patches(c, 0, T + 10, w, fh, wall, F.CAL, rng, y0 - 2, brick=s.get('brick', False), clip=inside, damp_h=17)
    elif state == 'parcial':
        F.wear_patches(c, 0, T + 10, w, fh, old, F.CAL, rng, y0 - 2, clip=lambda x, y: inside(x, y) and y > y0 - 48, damp_h=11)
    elif state == 'rest':       # restaurada com sinal de uso: pouca umidade rente ao chão
        F.wear_patches(c, 0, T + 10, w, fh, wall, F.CAL, rng, y0 - 2, clip=lambda x, y: inside(x, y) and y > y0 - 30, damp_h=7)
    F.roof(c, 0, 0, w, 17, rng); F.cornice(c, 0, 17, w, trim)
    F.string_course(c, 0, y_str, w, trim)
    if s.get('ashlar'): F.ashlar(c, 0, T + 5, fh - T - 5, 7, trim, rng); F.ashlar(c, w - 7, T + 5, fh - T - 5, 7, trim, rng)
    F.plinth(c, 0, y0 - 12, w, fh - (y0 - 12), rng)
    info = {'y0': y0, 'w': w}
    for (x, kind) in s['ground']:
        if kind == 'gw':   F.window_grade(c, x, y0 - 64, 28, 40, trim, rng)
        elif kind == 'ws': F.window_shut(c, x, y0 - 66, 28, 42, trim, wood, rng)
        elif kind == 'arch': F.door_arch(c, x, y0, 52, 66, trim, wood); info['door_x'] = x
        elif kind == 'flat': F.door_flat(c, x, y0 - 3, 30, 62, trim, wood); info.setdefault('flat', []).append(x)
        elif kind == 'big': F.door_flat(c, x, y0 - 3, 40, 66, trim, wood, iron_bars=False); info['door_x'] = x
    for (x, kind) in s.get('upper', []):
        if kind == 'bd': F.balcony_door(c, x, y_str, 26, 60, trim, wood, rng)
        elif kind == 'ws': F.window_shut(c, x, y_str - 62, 26, 42, trim, wood, rng)
    if state in ('gasto', 'parcial'):
        for (x, kind) in s.get('upper', []):
            if kind == 'bd': F.streaks(c, x, y_str + 9, 3 if state == 'gasto' else 1, rng)
        for (x, kind) in s['ground']:
            if kind in ('gw', 'ws'): F.streaks(c, x, y0 - 18, 2 if state == 'gasto' else 1, rng, 10)
    if s.get('sign'):
        xc = s['sign']; pw, ph = 56, 13; sx, sy = xc - pw // 2, y0 - 90
        c.rect(sx, sy, pw, ph, F.CAL[4]); c.hline(sx, sy, pw, (250, 246, 232)); c.rect(sx, sy, 1, ph, (250, 246, 232)); c.rect(sx + pw - 1, sy, 1, ph, F.CAL[2]); c.hline(sx, sy + ph - 1, pw, F.CAL[2])
        c.hline(sx + 1, sy + 1, pw - 2, wood[3]); c.hline(sx + 1, sy + ph - 2, pw - 2, wood[3])
        text(c, sx + 7, sy + 3, "PADARIA", wood[0], 1); c.shade(sx, sy + ph, pw, 2, SH2)
    F.IRON = F.IRON0; F.TELHA = F.TELHA0
    return c, info
F.IRON0 = F.IRON; F.TELHA0 = F.TELHA

# ------------------------------------------------------------------ elenco de imóveis: mesma composição aprovada, estados diferentes
BUILDINGS = [
 ('casa_salvia', 0, dict(w=170, hex='salvia', state='parcial', old_h=58, trim=TR_NEW, wood='verde', ground=[(40, 'ws'), (118, 'flat')], upper=[(40, 'bd'), (118, 'bd')], repaint=[(100, 40, 44, 30)])),
 ('sobrado', 170, dict(w=160, hex='amarelo', state='novo', trim=TR_NEW, wood='azul', ashlar=True, ground=[(46, 'flat'), (116, 'ws')], upper=[(46, 'bd'), (116, 'bd')])),
 ('padaria', 330, dict(w=360, hex='rosa_q', state='rest', trim=TR_CREAM, wood='verde', ashlar=True, sign=180, rp_light=True,
                       ground=[(36, 'gw'), (108, 'gw'), (180, 'arch'), (252, 'gw'), (324, 'flat')], repaint=[(200, 40, 100, 70), (14, 120, 60, 40)],
                       upper=[(36, 'bd'), (108, 'bd'), (180, 'bd'), (252, 'bd'), (324, 'bd')])),
 ('azul', 690, dict(w=160, hex='azul', state='parcial', old_h=46, trim=TR_NEW, wood='azul', ground=[(38, 'ws'), (106, 'big')], upper=[(38, 'bd'), (106, 'bd')])),
 ('creme', 850, dict(w=150, hex='creme', state='novo', trim=TR_BLUE, wood='vinho', ground=[(30, 'ws'), (94, 'big')], upper=[(30, 'ws'), (94, 'bd')])),
 ('agua', 1000, dict(w=150, hex='agua', state='gasto', brick=True, trim=F.CAL, wood='gasto', ground=[(36, 'flat'), (100, 'ws')], upper=[(36, 'ws'), (100, 'ws')], repaint=[], rp_light=False)),
 ('rosa', 1150, dict(w=180, hex='rosa_a', state='parcial', old_h=54, trim=TR_NEW, wood='marrom', ground=[(40, 'ws'), (120, 'flat')], upper=[(40, 'bd'), (120, 'bd')])),
 ('lilas', 1330, dict(w=170, hex='lilas', state='novo', trim=TR_NEW, wood='ocre', ground=[(40, 'flat'), (110, 'ws')], upper=[(40, 'ws'), (110, 'bd')])),
]

# ------------------------------------------------------------------ chão: calçamento antigo + trechos reformados
S = F.STONE
def calcada_nova(gs, x0, x1, rng):
    """Lajes de granito regulares, mais claras e bem rejuntadas (trecho reformado)."""
    for (ya, yb, off) in ((2, 11, 0), (12, SW - 1, 20)):
        x = x0 - ((x0 + off) % 40)
        while x < x1:
            tone = mix(S[3], (206, 200, 186), .34 if (x // 40) % 3 else .26)
            for xx in range(max(x0, x), min(x1, x + 40)):
                for y in range(ya, yb + 1): gs.pset(xx, y, tone)
                gs.pset(xx, ya, mix(S[4], (230, 224, 210), .4)); gs.pset(xx, yb, S[2])
            if x0 <= x + 39 < x1:
                for y in range(ya, yb + 1): gs.pset(x + 39, y, S[2])
            x += 40
    for xx in range(x0, x1): gs.pset(xx, 0, S[0]); gs.pset(xx, 1, S[1])

def rua_nova(gs, x0, x1, rng, y_from=SW + 6, y_to=70):
    """Paralelepípedo reassentado: fiadas alinhadas, peças mais uniformes e juntas limpas."""
    JOINT = mix(S[0], (50, 40, 40), .5); COB = [S[2], S[2], S[3], mix(S[2], (150, 140, 130), .3)]
    for yy in range(y_from, y_to):
        for xx in range(x0, x1): gs.pset(xx, yy, JOINT)
    yy = y_from; r = 0
    while yy < y_to:
        rh = 6; xx = x0 - (5 if r % 2 else 0)
        while xx < x1:
            sw = 10; col = rng.choice(COB)
            for j in range(rh - 1):
                for i in range(sw - 1):
                    if (j in (0, rh - 2)) and (i in (0, sw - 2)): continue
                    if x0 <= xx + i < x1 and yy + j < y_to: gs.pset(xx + i, yy + j, col)
            for i in range(1, sw - 3):
                if x0 <= xx + i < x1: gs.pset(xx + i, yy, mix(col, (230, 220, 210), .20))
            xx += sw
        yy += rh; r += 1

def ground96(rng):
    gs = RW.ground6(rng)                                                   # base: o mesmo desgaste de 1991
    for (a, b) in ((330, 690), (850, 1000), (1330, 1500)): calcada_nova(gs, a, b, rng)          # calçada reformada em frente ao que foi recuperado
    for (a, b) in ((60, 520), (1180, 1500)): rua_nova(gs, a, b, rng)                             # calçamento refeito nas pontas; o palco fica com o piso antigo
    # meio-fio: trechos refeitos mais claros (mesmos pontos da calçada nova)
    for (a, b) in ((330, 690), (850, 1000), (1330, 1500)):
        for xx in range(a, b):
            gs.pset(xx, SW, mix(S[4], (236, 230, 216), .4)); gs.pset(xx, SW + 1, mix(S[3], (210, 204, 190), .3))
    return gs

def compose96(seed=1996):
    rng = random.Random(seed)
    world = C(W, VH); placed = []
    for i, (name, x0, spec) in enumerate(BUILDINGS):
        b, info = build96(name, spec, 700 + i)
        xref = x0 + info.get('door_x', info['w'] // 2)
        ytop = yw(xref) - info['y0']
        world.paste(b, x0, ytop)
        info.update(x0=x0, xref=xref, ytop=ytop, name=name, base=yw(xref)); placed.append(info)
    gs = ground96(rng)
    for x in range(W):
        top = yw(x)
        for y in range(top, VH):
            sy = min(y - top, gs.h - 1); r, g, b, a = gs.p[x, sy]; world.p[x, y] = (r, g, b, 255)
    return world, placed, rng

def put(c, x, sy, col): c.pset(x, yw(x) + sy, col)
def rput(c, x, w, sy0, h, col):
    for k in range(h):
        for xx in range(x, x + w): put(c, xx, sy0 + k, col)

def ground_features96(world, rng):
    # soleira de granito da padaria (mesma função de 1991, no mesmo eixo da porta: x 510)
    for xx in range(480, 541):
        for sy in range(2, 8): put(world, xx, sy, S[4] if sy == 2 else S[3] if sy < 7 else S[1])
    # remendos de cimento ainda visíveis (reparos antigos) e lajes novas encaixadas no piso velho
    for (xc, w, sy0, h, new) in [(760, 30, 12, 8, False), (905, 34, 5, 9, True), (1060, 26, 4, 10, False), (640, 24, 14, 7, True)]:
        for i in range(w):
            for j in range(h):
                if i in (0, w - 1) and rng.random() < .3 and not new: continue
                base = mix(S[3], (214, 204, 186), .62 if new else .45)
                put(world, xc - w // 2 + i, sy0 + j, base if j else mix(S[4], (236, 228, 212), .5))
    for xc in (612, 1012):     # bueiros de ferro na sarjeta
        rput(world, xc - 9, 18, SW + 4, 2, S[0])
        for i in range(0, 18, 3): put(world, xc - 9 + i, SW + 4, F.IRON[3])
    xc = 862; yc = yw(xc) + SW + 22     # tampa de ferro redonda
    for yy in range(-4, 5):
        for xx in range(-9, 10):
            if (xx / 9.5) ** 2 + (yy / 4.5) ** 2 <= 1:
                d = (xx / 9.5) ** 2 + (yy / 4.5) ** 2
                world.pset(xc + xx, yc + yy, F.IRON[1] if d > .75 else F.IRON[2] if (xx + yy) % 4 else F.IRON[3])
    for xx in range(-6, 7, 3): world.pset(xc + xx, yc, F.IRON[4])
    for _ in range(26):      # poucas folhas secas e cascas
        x = rng.randint(6, W - 6); sy = SW + rng.choice([5, 6, 8, 12, 16])
        world.pset(x, yw(x) + sy, rng.choice([(150, 110, 60), (118, 138, 70), (196, 150, 64)]))

# ------------------------------------------------------------------ acabamentos fixos das fachadas
def wy(b, h): return b['base'] - h
def decorar(world, B, rng):
    RW.yw = yw
    # luminárias conservadas, uma de cada lado das portas principais
    for n, xs in (('casa_salvia', (158,)), ('sobrado', (200, 262)), ('padaria', (477, 543)), ('azul', (792 + 10,)), ('creme', (920, 977)), ('rosa', (1330 - 8,)), ('lilas', (1410,))):
        for x in xs: RW.lampiao(world, x, wy(B[n], 60))
    # letreiros organizados, todos pintados e alinhados na mesma altura
    b = B['casa_salvia']; RW.placa_pintada(world, 118 - 29, wy(b, 84), 58, 11, 'BARBEARIA', ramp(150, .30, (.14, .22, .30, .38, .46)), (248, 240, 214), rng, gasto=1)
    b = B['azul']; RW.placa_pintada(world, 796 - 36, wy(b, 84), 72, 11, 'ASSOCIACAO', ramp(210, .55, (.16, .25, .34, .43, .52)), (248, 240, 214), rng, gasto=1)
    RW.azulejo_placa(world, 690 + 6, wy(b, 85), 'R. DA PAZ', rng)
    # padaria: plaqueta bilíngue ao lado do arco (continuidade de 1994), agora esmaltada e centralizada na parede
    b = B['padaria']; pw = width('BREAD') + 6; x = 330 + 287 - pw // 2; y = wy(b, 52)
    world.rect(x, y, pw, 22, (236, 232, 218)); world.rect(x + 1, y + 1, pw - 2, 20, (46, 92, 140)); world.hline(x + 1, y + 1, pw - 2, (86, 132, 178))
    text(world, x + 3, y + 4, 'BREAD', (244, 240, 226), 1); world.hline(x + 3, y + 11, pw - 6, (216, 178, 74)); text(world, x + (pw - width('PAO')) // 2, y + 14, 'PAO', (244, 240, 226), 1)
    world.shade(x, y + 22, pw, 2, SH2)
    # vasos e floreiras nas fachadas recuperadas; samambaias nas sacadas
    for n, kinds, x in (('sobrado', ['barro', 'lata'], 170 + 108), ('rosa', ['jard'], 1150 + 40), ('lilas', ['barro'], 1330 + 110), ('creme', ['lata', 'barro'], 850 + 22)):
        RW.vasos_peitoril(world, x, wy(B[n], 24), rng, kinds)
    for n, xs in (('sobrado', (170 + 46,)), ('padaria', (330 + 108, 330 + 252)), ('rosa', (1150 + 40,)), ('lilas', (1330 + 110,))):
        for x in xs: RW.samambaia_pendurada(world, x, wy(B[n], 108), rng)
    # trepadeira florida só na fachada ainda sem reforma
    b = B['agua']
    RW.trepadeira(world, 1000 + 4, 1000 + 52, lambda x: wy(b, 90) + 1, lambda x: wy(b, 90) + 10 + (x * 5) % 14, rng, LEAF, FLOR_M, .85)

def build_world96():
    world, placed, rng = compose96()
    ground_features96(world, rng)
    B = {p['name']: p for p in placed}
    decorar(world, B, rng)
    return world, placed, B

if __name__ == '__main__':
    world, placed, B = build_world96(); world.save('/tmp/world96.png'); print([(p['name'], p['x0'], p['base']) for p in placed])

import random, math, sys
from pxl import *
from facade import *

W = 1130           # largura do mundo (px)
VW, VH = 480, 270  # viewport nativa
def f_ground(x):   # altura do "pé" (linha de caminhada) — a rua desce para a direita
    return 222 + int(max(0, x) // 36)
def yw(x):         # contato parede/calçada
    return f_ground(x) - 6

PAL = {
 'padaria': dict(wall=ramp(10, 0.34, (0.36, 0.48, 0.60, 0.70, 0.80)), trim=CAL, wood=ramp(165, 0.20, (0.13, 0.21, 0.31, 0.41, 0.52))),
 'sobrado': dict(wall=ramp(41, 0.56, (0.34, 0.46, 0.58, 0.69, 0.80)), trim=CAL, wood=ramp(208, 0.28, (0.16, 0.25, 0.36, 0.47, 0.58))),
 'azul':    dict(wall=ramp(46, 0.20, (0.60, 0.70, 0.80, 0.88, 0.94)), trim=ramp(46, 0.20, (0.50, 0.62, 0.74, 0.84, 0.92)), wood=ramp(208, 0.50, (0.20, 0.31, 0.43, 0.55, 0.68))),
 'verde':   dict(wall=ramp(158, 0.20, (0.36, 0.48, 0.60, 0.70, 0.80)), trim=CAL, wood=ramp(26, 0.38, (0.14, 0.22, 0.32, 0.42, 0.52))),
 'bege':    dict(wall=ramp(34, 0.16, (0.38, 0.50, 0.62, 0.72, 0.82)), trim=CAL, wood=ramp(190, 0.22, (0.16, 0.25, 0.35, 0.46, 0.57))),
 'rosa':    dict(wall=ramp(352, 0.30, (0.40, 0.52, 0.64, 0.74, 0.83)), trim=CAL, wood=ramp(165, 0.20, (0.13, 0.21, 0.31, 0.41, 0.52))),
}

def build(name, spec, seed):
    rng = random.Random(seed)
    P = PAL[spec['pal']]; wall, trim, wood = P['wall'], P['trim'], P['wood']
    w = spec['w']; two = spec['floors'] == 2
    telha = spec['roof'] == 'telha'
    T = 22 if telha else 5
    H0 = spec.get('H0', 94); H1 = spec.get('H1', 79) if two else 0
    y_str = T + H1
    y0 = y_str + (3 if two else 0) + H0
    fh = y0 + 44
    c = C(w, fh)
    make_wall(c, 0, T, w, fh - T, wall, rng)
    # faixas largas de luz/desgaste (sem ruído): mais claro no alto, levemente mais escuro junto à base
    c.shade(0, y0 - 40, w, 28, (0.97, 0.97, 0.99))
    inside = lambda x, y: 0 <= x < w and T + 3 <= y < y0 - 10
    for (rx, ry, rw, rh) in spec.get('repaint', []):
        repaint(c, rx, ry, rw, rh, spec.get('rp_light', True), rng, inside)
    wear_patches(c, 0, T + 10, w, fh, wall, CAL, rng, y0 - 2, brick=spec.get('brick', False), clip=inside)
    # manchas verticais sob peitoris (escorrimento) — poucas e discretas
    # estrutura
    if telha:
        roof(c, 0, 0, w, 17, rng); cornice(c, 0, 17, w, trim)
    else:
        cornice(c, 0, 0, w, trim)
    if two: string_course(c, 0, y_str, w, trim)
    if spec.get('ashlar'):
        ashlar(c, 0, T + 5, fh - T - 5, 7, trim, rng); ashlar(c, w - 7, T + 5, fh - T - 5, 7, trim, rng)
    plinth(c, 0, y0 - 12, w, fh - (y0 - 12), rng)
    info = {'y0': y0, 'w': w}
    # elementos do térreo
    for (x, kind) in spec['ground']:
        if kind == 'gw':   window_grade(c, x, y0 - 64, 28, 40, trim, rng)
        elif kind == 'ws': window_shut(c, x, y0 - 66, 28, 42, trim, wood, rng)
        elif kind == 'arch':
            door_arch(c, x, y0, 52, 66, trim, wood); info['door_x'] = x
        elif kind == 'flat':
            door_flat(c, x, y0 - 3, 30, 62, trim, wood); info.setdefault('flat', []).append(x)
        elif kind == 'big':
            door_flat(c, x, y0 - 3, 40, 66, trim, wood, iron_bars=False); info['door_x'] = x
    for (x, kind) in spec.get('upper', []):
        if kind == 'bd': balcony_door(c, x, y_str, 26, 60, trim, wood, rng)
        elif kind == 'ws': window_shut(c, x, y_str - 62, 26, 42, trim, wood, rng)
    for (x, kind) in spec.get('upper', []):
        if kind == 'bd': streaks(c, x, y_str + 9, 3, rng)
    for (x, kind) in spec['ground']:
        if kind in ('gw', 'ws'): streaks(c, x, y0 - 18, 2, rng, 10)
    if spec.get('sign'):
        xc = spec['sign']
        pw, ph = 56, 13
        sx, sy = xc - pw // 2, y0 - 90
        c.rect(sx, sy, pw, ph, CAL[3]); c.hline(sx, sy, pw, CAL[4])
        c.rect(sx, sy, 1, ph, CAL[4]); c.rect(sx + pw - 1, sy, 1, ph, CAL[2]); c.hline(sx, sy + ph - 1, pw, CAL[2])
        c.hline(sx + 1, sy + 1, pw - 2, wood[3]); c.hline(sx + 1, sy + ph - 2, pw - 2, wood[3])   # filetes pintados
        text(c, sx + 7, sy + 3, "PADARIA", wood[0], 1)
        c.shade(sx, sy + ph, pw, 2, SH2)
        # desgaste do letreiro
        c.pset(sx + 3, sy + 5, CAL[2]); c.pset(sx + 4, sy + 6, CAL[2]); c.pset(sx + pw - 6, sy + 4, CAL[2])
    return c, info

BUILDINGS = [
 # nome, x0, spec
 ('b0', -40, dict(w=150, pal='bege', floors=1, roof='parapet', H0=86, ground=[(38, 'ws'), (112, 'flat')])),
 ('sobrado', 110, dict(w=180, pal='sobrado', floors=2, roof='telha', ashlar=True, brick=True,
                       ground=[(54, 'flat'), (130, 'ws')], upper=[(54, 'bd'), (130, 'bd')], repaint=[(14, 98, 78, 50)])),
 ('padaria', 290, dict(w=360, pal='padaria', floors=2, roof='telha', ashlar=True, sign=180,
                       ground=[(36, 'gw'), (108, 'gw'), (180, 'arch'), (252, 'gw'), (324, 'flat')], repaint=[(200, 40, 110, 80), (14, 120, 60, 40)], rp_light=False,
                       upper=[(36, 'bd'), (108, 'bd'), (180, 'bd'), (252, 'bd'), (324, 'bd')])),
 ('azul', 650, dict(w=160, pal='azul', floors=2, roof='telha', H1=70,
                    ground=[(38, 'ws'), (106, 'big')], upper=[(38, 'ws'), (106, 'ws')])),
 ('verde', 810, dict(w=140, pal='verde', floors=2, roof='telha', H1=70,
                     ground=[(36, 'flat'), (100, 'ws')], upper=[(36, 'ws'), (100, 'ws')])),
 ('b5', 950, dict(w=210, pal='rosa', floors=1, roof='parapet', H0=88, ground=[(40, 'flat'), (118, 'ws')])),
]

def ground_strip(rng):
    h = 64
    s = C(W, h)
    sw_h, cb_h = 12, 4
    S = STONE
    # calçada: lajes de pedra
    for y in range(sw_h): s.hline(0, y, W, S[3])
    x = 0
    while x < W:
        lw = rng.randint(24, 40)
        tone = rng.choice([S[3], S[3], S[2]])
        for xx in range(x, min(W, x + lw)):
            for y in range(2, sw_h): s.pset(xx, y, tone)
            s.pset(xx, 2, S[4] if tone == S[3] else S[3])
        for y in range(2, sw_h): s.pset(min(W - 1, x + lw - 1), y, S[1])
        x += lw
    for xx in range(W): s.pset(xx, 0, S[0]); s.pset(xx, 1, S[1])         # contato com a parede
    for xx in range(W): s.pset(xx, sw_h - 1, S[1])
    # meio-fio (granito)
    y = sw_h
    for xx in range(W):
        s.pset(xx, y, S[4]); s.pset(xx, y + 1, S[3]); s.pset(xx, y + 2, S[3]); s.pset(xx, y + 3, S[1])
    x = 0
    while x < W:
        x += rng.randint(38, 64); 
        for j in range(3): s.pset(min(W - 1, x), y + j, S[1])
    # sarjeta
    for xx in range(W): s.pset(xx, y + 4, S[0]); s.pset(xx, y + 5, S[1])
    # paralelepípedo
    COB = [S[1], S[2], S[2], S[3], mix(S[2], (120, 100, 96), 0.35), mix(S[1], (96, 82, 84), 0.4)]
    JOINT = mix(S[0], (50, 40, 40), 0.5)
    y0 = y + 6
    for yy in range(y0, h): 
        for xx in range(W): s.pset(xx, yy, JOINT)
    row = 0; yy = y0
    while yy < h:
        rh = rng.choice([6, 6, 7])
        xx = -rng.randint(0, 9)
        while xx < W:
            sw = rng.randint(8, 12)
            col = rng.choice(COB)
            for j in range(rh - 1):
                for i in range(sw - 1):
                    px_, py_ = xx + i, yy + j
                    # cantos arredondados
                    if (j in (0, rh - 2)) and (i in (0, sw - 2)): continue
                    s.pset(px_, py_, col)
            for i in range(1, sw - 3): s.pset(xx + i, yy, mix(col, (230, 220, 210), 0.22))   # brilho no topo
            for i in range(1, sw - 2): s.pset(xx + i, yy + rh - 2, mix(col, (30, 26, 40), 0.35))
            xx += sw
        yy += rh; row += 1
    return s

def compose_street():
    rng = random.Random(1991)
    world = C(W, VH)
    placed = []
    for i, (name, x0, spec) in enumerate(BUILDINGS):
        b, info = build(name, spec, 100 + i)
        xref = x0 + info.get('door_x', info['w'] // 2)
        ytop = yw(xref) - info['y0']
        world.paste(b, x0, ytop)
        info['x0'] = x0; info['xref'] = xref; info['ytop'] = ytop; info['name'] = name
        placed.append(info)
    gs = ground_strip(rng)
    # cola a faixa de chão coluna a coluna, deslocada pela inclinação
    for x in range(W):
        top = yw(x)
        for y in range(top, VH):
            sy = y - top
            if sy >= gs.h: sy = gs.h - 1
            r, g, b, a = gs.p[x, sy]
            world.p[x, y] = (r, g, b, 255)
    # degraus e soleiras na calçada, em projeção frontal
    for info in placed:
        if info['name'] == 'sobrado':
            dx = info['x0'] + 54
            for k, (ww, yy) in enumerate([(30, yw(dx) - 6), (36, yw(dx) - 3)]):
                world.rect(dx - ww // 2, yy, ww, 3, STONE[3]); world.hline(dx - ww // 2, yy, ww, STONE[4])
                world.hline(dx - ww // 2, yy + 2, ww, STONE[1])
    return world, placed

if __name__ == '__main__':
    world, placed = compose_street()
    world.save('../preview/street_raw.png')
    print([(p['name'], p['x0'], p['ytop'], p['y0']) for p in placed])

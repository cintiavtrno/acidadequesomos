"""Ferramentas de desenho da Etapa 6: vegetação, ferro, madeira, tecido (pixel art, luz do alto à esquerda)."""
import random, math
from pxl import *
from facade import STONE, CAL, IRON, BRICK, MOSS, TELHA

LEAF  = ramp(118, 0.40, (0.14, 0.22, 0.31, 0.42, 0.55))      # folhagem verde (escuro -> claro)
LEAF2 = ramp(98, 0.42, (0.16, 0.25, 0.35, 0.46, 0.58))       # verde-amarelado (capim, samambaia nova)
LEAF3 = ramp(150, 0.30, (0.13, 0.21, 0.30, 0.40, 0.50))      # verde frio (espada, babosa)
BARK  = ramp(24, 0.30, (0.14, 0.22, 0.31, 0.41, 0.52))
WOOD  = ramp(28, 0.42, (0.16, 0.25, 0.36, 0.47, 0.58))
WOODD = ramp(20, 0.34, (0.12, 0.19, 0.28, 0.38, 0.48))
CLAYR = ramp(16, 0.52, (0.24, 0.35, 0.46, 0.57, 0.68))        # barro / telha
FLOR_M = ramp(322, 0.60, (0.28, 0.40, 0.52, 0.64, 0.76))     # primavera/bougainville magenta
FLOR_V = ramp(2, 0.62, (0.30, 0.42, 0.54, 0.66, 0.78))       # hibisco vermelho
FLOR_A = ramp(44, 0.80, (0.40, 0.52, 0.62, 0.72, 0.82))      # amarelo (alamanda)
FLOR_B = ramp(46, 0.30, (0.70, 0.78, 0.86, 0.92, 0.97))      # branco
FERRO = IRON
CAL_W = CAL
LATA  = ramp(210, 0.40, (0.20, 0.30, 0.42, 0.54, 0.66))      # lata de tinta azul
LATA2 = ramp(8, 0.45, (0.24, 0.34, 0.45, 0.56, 0.66))        # lata vermelha

def shadow_ell(c, cx, cy, rx, ry, a=70):
    for y in range(-ry, ry + 1):
        for x in range(-rx, rx + 1):
            if (x / rx) ** 2 + (y / ry) ** 2 <= 1:
                px, py = int(cx + x), int(cy + y); r, g, b, aa = c.get(px, py)
                if aa == 0: c.pset(px, py, (24, 18, 40, a))

def blob(c, cx, cy, rx, ry, col):
    for y in range(-ry, ry + 1):
        for x in range(-rx, rx + 1):
            if (x / (rx + .3)) ** 2 + (y / (ry + .3)) ** 2 <= 1: c.pset(cx + x, cy + y, col)

def leafmass(c, cx, cy, rx, ry, rng, ramp_=LEAF, n=None, lightdir=(-0.5, -0.8), cell=(5, 3), hole=0.0):
    """Massa de folhagem por tufos: sombra no fundo/direita, luz no alto/esquerda, bordas irregulares."""
    n = n or int(rx * ry / 5)
    items = []
    for _ in range(n * 3):
        a = rng.uniform(0, math.tau); r = math.sqrt(rng.random())
        x = cx + math.cos(a) * rx * r; y = cy + math.sin(a) * ry * r
        items.append((y, x))
    items.sort()
    for y, x in items[:n * 2]:
        u = ((x - cx) / rx) * lightdir[0] * -1 + ((y - cy) / ry) * lightdir[1] * -1   # >0 = sombra
        t = max(0, min(4, int(2.6 - u * 2.2 + rng.uniform(-0.6, 0.6))))
        w = rng.randint(cell[0] - 1, cell[0] + 1); h = rng.randint(cell[1] - 1, cell[1] + 1)
        blob(c, int(x), int(y), w // 2, max(1, h // 2), ramp_[t])
    # contorno interno suave: pixels de luz no topo esquerdo
    for _ in range(n // 2):
        a = rng.uniform(math.pi * 0.9, math.pi * 1.7); r = rng.uniform(0.55, 0.95)
        x = int(cx + math.cos(a) * rx * r); y = int(cy + math.sin(a) * ry * r)
        if c.get(x, y)[3]: c.hline(x, y, rng.randint(1, 3), ramp_[4])
    if hole:
        for _ in range(int(n * hole)):
            a = rng.uniform(0, math.tau); r = rng.uniform(0.2, 0.9)
            x = int(cx + math.cos(a) * rx * r); y = int(cy + math.sin(a) * ry * r)
            c.pset(x, y, ramp_[0])

def trunk(c, x, y0, y1, w0, w1, rng, col=BARK, lean=0.0):
    h = y0 - y1
    for i in range(h + 1):
        t = i / max(1, h); w = round(w0 + (w1 - w0) * t); xx = x + round(lean * t * 6)
        for k in range(w):
            u = k / max(1, w - 1)
            c.pset(xx - w // 2 + k, y0 - i, col[3 if u < 0.25 else 2 if u < 0.6 else 1])
        if rng.random() < 0.18: c.pset(xx - w // 2 + rng.randint(0, w - 1), y0 - i, col[0])

def pot_clay(c, cx, yb, w, h, col=CLAYR):
    """Vaso de barro (vista frontal)."""
    for j in range(h):
        t = j / max(1, h - 1); ww = round(w * (0.72 + 0.28 * (1 - t))) if j > 3 else w
        for i in range(ww):
            u = i / max(1, ww - 1); k = 3 if u < 0.2 else 2 if u < 0.55 else 1 if u < 0.85 else 0
            c.pset(cx - ww // 2 + i, yb - j - 1, col[k])
    c.hline(cx - w // 2, yb - h, w, col[4]); c.hline(cx - w // 2, yb - h + 1, w, col[3])      # borda do vaso
    c.hline(cx - w // 2, yb - h + 2, w, col[1])

def can_pot(c, cx, yb, w, h, col, rng):
    """Lata de tinta/óleo reaproveitada como vaso (vista frontal): corpo, aro, alça."""
    for j in range(h):
        for i in range(w):
            u = i / max(1, w - 1); k = 4 if u < 0.15 else 3 if u < 0.45 else 2 if u < 0.8 else 1
            c.pset(cx - w // 2 + i, yb - j - 1, col[k])
    c.hline(cx - w // 2, yb - h, w, col[4]); c.hline(cx - w // 2, yb - 2, w, col[1]); c.hline(cx - w // 2, yb - h // 2 - 1, w, col[1])
    for i in range(0, w, 3):
        if rng.random() < 0.5: c.pset(cx - w // 2 + i, yb - h // 2 - 3, col[0])        # respingos / ferrugem
    c.pset(cx - w // 2 + 1, yb - 1, col[0]); c.pset(cx + w // 2 - 1, yb - 1, col[0])

def fern(c, cx, yb, rx, ry, rng, ramp_=LEAF2, droop=False):
    """Samambaia / folhas longas arqueadas: lâminas curvas saindo de um ponto."""
    n = max(7, rx * 2)
    for i in range(n):
        a = -math.pi / 2 + (i / (n - 1) - 0.5) * math.pi * 1.35 + rng.uniform(-0.08, 0.08)
        L = ry * rng.uniform(0.75, 1.1)
        x, y = cx, yb
        px, py = cx, yb
        for s in range(int(L)):
            t = s / L
            ang = a + (0.9 * t * t * (1 if a > -math.pi / 2 else -1)) * (1.2 if droop else 0.6)
            px = cx + math.cos(ang) * s * (rx / ry) * 1.1; py = yb + math.sin(ang) * s
            k = 3 if t < 0.25 else 2 if t < 0.65 else 1
            if a < -math.pi / 2 - 0.35 and t > 0.3: k += 1
            c.pset(round(px), round(py), ramp_[min(4, k)])
            if s % 2 == 0 and 0.2 < t < 0.9:
                c.pset(round(px) + (1 if a > -math.pi / 2 else -1), round(py), ramp_[max(0, k - 1)])

def sword_plant(c, cx, yb, h, rng, n=7):
    """Espada-de-são-jorge: folhas eretas com borda amarela."""
    for i in range(n):
        off = (i - (n - 1) / 2); a = off * 0.17 + rng.uniform(-0.03, 0.03); L = h * (1 - abs(off) * 0.09) * rng.uniform(0.85, 1.0)
        for s in range(int(L)):
            t = s / L; x = cx + math.sin(a) * s + off * 0.8 * (1 - t) * 0.6; y = yb - math.cos(a) * s
            wdt = 2 if t < 0.7 else 1
            for k in range(wdt):
                col = LEAF3[2 + (k == 0 and a < 0)] if t > 0.15 else LEAF3[1]
                c.pset(round(x) + k, round(y), col)
            if wdt == 2 and rng.random() < 0.7: c.pset(round(x) + 2, round(y), FLOR_A[2])   # borda amarela
            c.pset(round(x) - 1, round(y), LEAF3[0]) if t > 0.3 and wdt == 2 and rng.random() < 0.4 else None

def grass_tuft(c, x, y, rng, n=5, h=5, ramp_=LEAF2):
    for i in range(n):
        dx = i - n // 2 + rng.randint(-1, 1); L = rng.randint(h - 2, h)
        for s in range(L):
            c.pset(x + dx + (s * (1 if dx > 0 else -1)) // 3, y - s, ramp_[1 + (s * 3) // L])

def flower_dots(c, cx, cy, rx, ry, rng, ramp_, n=10):
    for _ in range(n):
        a = rng.uniform(0, math.tau); r = math.sqrt(rng.random())
        x = int(cx + math.cos(a) * rx * r); y = int(cy + math.sin(a) * ry * r)
        c.pset(x, y, ramp_[3]); c.pset(x + 1, y, ramp_[2]); c.pset(x, y + 1, ramp_[1]) if rng.random() < 0.6 else None
        if rng.random() < 0.35: c.pset(x - 1, y - 1, ramp_[4])

def whitewash_box(c, x, y, w, h, rng, top=2):
    """Alvenaria caiada (canteiro): frente clara, topo, sombra à direita/embaixo, desgaste localizado."""
    c.rect(x, y, w, h, CAL[3]); c.rect(x, y, w, top, CAL[4]); c.hline(x, y + top, w, CAL[2])
    c.vline(x, y + top, h - top, CAL[4]); c.vline(x + w - 1, y, h, CAL[1]); c.vline(x + w - 2, y + top, h - top, CAL[2])
    c.hline(x, y + h - 1, w, CAL[1]); c.hline(x + 1, y + h - 2, w - 2, CAL[2])
    for _ in range(max(1, w // 24)):
        px = x + rng.randint(3, w - 8); py = y + h - rng.randint(3, 6)
        c.rect(px, py, rng.randint(3, 6), 2, STONE[3]); c.pset(px + 1, py - 1, STONE[3])        # reboco caído mostrando a pedra
    for xx in range(x + 3, x + w - 3, 5):
        c.pset(xx, y + h - 3, mix(CAL[2], (96, 130, 80), 0.35))                                  # limo na base

def iron_post(c, x, y0, y1, w, col=FERRO):
    for yy in range(y1, y0):
        c.pset(x - w // 2, yy, col[3]); c.rect(x - w // 2 + 1, yy, max(1, w - 2), 1, col[2]); c.pset(x + w // 2, yy, col[1])

def cloth(c, x, y, w, h, col, rng, kind='shirt'):
    """Roupa no varal: retângulo com sombra de dobra e pregadores."""
    if kind == 'shirt':
        c.rect(x, y, w, h, col[2]); c.rect(x, y, w, 1, col[3]); c.vline(x + w - 1, y, h, col[1])
        c.rect(x - 2, y, 2, 4, col[2]); c.rect(x + w, y, 2, 4, col[1])                               # mangas
        c.rect(x + w // 2 - 1, y, 3, 1, col[0])                                                       # gola
        c.hline(x + 1, y + h - 1, w - 2, col[1])
    elif kind == 'towel':
        c.rect(x, y, w, h, col[3]); c.rect(x, y, w, 1, col[4]); c.vline(x + w - 1, y, h, col[2])
        for k in range(2, h - 1, 3): c.hline(x + 1, y + k, w - 2, col[2])
        c.hline(x, y + h - 1, w, col[1])
    else:   # lençol/pano largo, ondulado
        for i in range(w):
            hh = h + (1 if (i // 4) % 2 else 0)
            c.rect(x + i, y, 1, hh, col[3] if (i // 4) % 2 == 0 else col[2])
        c.hline(x, y, w, col[4]); c.hline(x, y + h, w, col[1])
    c.pset(x + 1, y - 1, (60, 40, 30)); c.pset(x + w - 2, y - 1, (60, 40, 30))

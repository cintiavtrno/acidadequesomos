"""Helpers mínimos de pixel art (sem antialias, paletas com mudança de matiz)."""
from PIL import Image, ImageDraw
import colorsys, random, math

def hsl(h, s, l):
    r, g, b = colorsys.hls_to_rgb((h % 360) / 360.0, max(0, min(1, l)), max(0, min(1, s)))
    return (round(r * 255), round(g * 255), round(b * 255))

def _toward(h, target, amt):
    d = ((target - h + 180) % 360) - 180
    return h + d * amt

def ramp(h, s, ls=(0.20, 0.34, 0.50, 0.66, 0.80), warm=52, cool=248, k=0.30):
    """Rampa escuro->claro: sombras tendem ao azul/roxo, luzes ao amarelo; saturação maior no meio."""
    n = len(ls); out = []
    for i, l in enumerate(ls):
        t = (i / (n - 1)) * 2 - 1
        hh = _toward(h, warm if t > 0 else cool, abs(t) * k)
        ss = s * (1 - 0.30 * abs(t))
        out.append(hsl(hh, ss, l))
    return out

def mix(a, b, t):
    return tuple(round(a[i] + (b[i] - a[i]) * t) for i in range(3))

SH1 = (0.80, 0.82, 0.93)
SH2 = (0.62, 0.66, 0.86)
SH3 = (0.46, 0.50, 0.76)

class C:
    def __init__(s, w, h, fill=(0, 0, 0, 0)):
        s.w, s.h = w, h
        s.im = Image.new('RGBA', (w, h), fill)
        s.p = s.im.load()
    def get(s, x, y):
        if 0 <= x < s.w and 0 <= y < s.h: return s.p[x, y]
        return (0, 0, 0, 0)
    def pset(s, x, y, c):
        if 0 <= x < s.w and 0 <= y < s.h:
            s.p[x, y] = c if len(c) == 4 else (c[0], c[1], c[2], 255)
    def rect(s, x, y, w, h, c):
        for yy in range(int(y), int(y + h)):
            for xx in range(int(x), int(x + w)):
                s.pset(xx, yy, c)
    def hline(s, x, y, w, c):
        for xx in range(int(x), int(x + w)): s.pset(xx, int(y), c)
    def vline(s, x, y, h, c):
        for yy in range(int(y), int(y + h)): s.pset(int(x), yy, c)
    def line(s, x0, y0, x1, y1, c):
        ImageDraw.Draw(s.im).line([(x0, y0), (x1, y1)], fill=c if len(c) == 4 else (*c, 255))
    def poly(s, pts, c):
        ImageDraw.Draw(s.im).polygon(pts, fill=c if len(c) == 4 else (*c, 255))
    def shade(s, x, y, w, h, f, mask=None):
        """Escurece/tinge pixels existentes (sombra projetada coerente com a paleta)."""
        for yy in range(int(y), int(y + h)):
            for xx in range(int(x), int(x + w)):
                if not (0 <= xx < s.w and 0 <= yy < s.h): continue
                r, g, b, a = s.p[xx, yy]
                if a == 0: continue
                if mask and not mask(xx, yy): continue
                s.p[xx, yy] = (round(r * f[0]), round(g * f[1]), round(b * f[2]), a)
    def lighten(s, x, y, w, h, amt=0.16, tint=(255, 238, 196)):
        for yy in range(int(y), int(y + h)):
            for xx in range(int(x), int(x + w)):
                if not (0 <= xx < s.w and 0 <= yy < s.h): continue
                r, g, b, a = s.p[xx, yy]
                if a == 0: continue
                s.p[xx, yy] = (*mix((r, g, b), tint, amt), a)
    def paste(s, o, x, y):
        s.im.alpha_composite(o.im if isinstance(o, C) else o, (int(x), int(y)))
    def save(s, path): s.im.save(path)

def patch(c, cx, cy, rx, ry, col, rng, n=11, jag=0.35, clip=None):
    """Mancha irregular (desgaste localizado): polígono com raios variados."""
    pts = []
    for i in range(n):
        a = i / n * math.tau
        r = 1 + rng.uniform(-jag, jag)
        pts.append((cx + math.cos(a) * rx * r, cy + math.sin(a) * ry * r))
    if clip is None:
        c.poly(pts, col)
    else:
        t = C(c.w, c.h); t.poly(pts, col)
        for yy in range(c.h):
            for xx in range(c.w):
                if t.p[xx, yy][3] and clip(xx, yy): c.p[xx, yy] = t.p[xx, yy]

FONT = {
 'P': ["####.", "#...#", "#...#", "####.", "#....", "#....", "#...."],
 'A': [".###.", "#...#", "#...#", "#####", "#...#", "#...#", "#...#"],
 'D': ["####.", "#...#", "#...#", "#...#", "#...#", "#...#", "####."],
 'R': ["####.", "#...#", "#...#", "####.", "#.#..", "#..#.", "#...#"],
 'I': [".###.", "..#..", "..#..", "..#..", "..#..", "..#..", ".###."],
}
def text(c, x, y, s, col, gap=1):
    for ch in s:
        g = FONT[ch]
        for j, row in enumerate(g):
            for i, v in enumerate(row):
                if v == '#': c.pset(x + i, y + j, col)
        x += 5 + gap
    return x

"""Camadas do fundo da rua separadas para paralaxe: céu (parado), nuvens (derivam sozinhas), morro e casario com a torre.
Mesmas cores e mesmo estilo de far.py (rampas planas, sem antialias). Cada camada é um PNG com transparência.
Saída: assets/far/<rua>_{sky,clouds,hill,casas}.png. O jogo desenha cada uma com a sua própria velocidade (ver Plx em game/fit.js)."""
import random, math, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pxl import *
from far import SKY, haze

HZ = (206, 216, 220)
H = 270
W_SKY = 64          # tile horizontal do céu (o tracejado de 2 px se repete)
W_CLOUD = 960       # tile das nuvens (dá a volta)
W_FAR = 1000        # morro e casario: cobrem a largura lógica máxima (640) mais o deslocamento da câmera

def sky():
    c = C(W_SKY, H); bh = 30
    for i, col in enumerate(SKY): c.rect(0, i * bh, W_SKY, bh, col)
    for i in range(1, len(SKY)):
        y = i * bh
        for x in range(W_SKY):
            if x % 2 == 0: c.pset(x, y - 1, SKY[i])
            if (x + 1) % 2 == 0: c.pset(x, y, SKY[i - 1])
    c.rect(0, len(SKY) * bh, W_SKY, H - len(SKY) * bh, SKY[-1])
    return c

def clouds(seed):
    rng = random.Random(seed); c = C(W_CLOUD, H)
    def cloud(cx, cy, w):
        for k in range(4):
            ww = int(w * (1 - 0.22 * k)); ox = cx + int(w * 0.08 * k)
            for dx in range(ww):
                t = dx / ww; hh = int(3 + 4 * math.sin(math.pi * t) * (1 - 0.15 * k))
                for dy in range(hh):
                    col = (252, 246, 236) if dy < hh - 2 else (222, 224, 226)
                    c.pset((ox + dx) % W_CLOUD, cy - k * 2 - dy + hh // 2, col)
    # sete nuvens espalhadas pelo tile, alturas e larguras diferentes; as grandes ficam no alto
    xs = [30, 170, 330, 470, 610, 760, 880]
    for x in xs:
        w = rng.choice([30, 36, 44, 52, 60]); y = rng.randint(16, 66)
        cloud(x + rng.randint(-14, 14), y, w)
    return c

def hill(seed):
    c = C(W_FAR, H)
    hl = haze((92, 128, 120), 0.66, HZ); hh = haze((112, 146, 134), 0.66, HZ)
    rng = random.Random(seed); p1, p2 = rng.uniform(0, 6), rng.uniform(0, 6)
    pts = [(0, 300)]; x = 0
    while x <= W_FAR + 20:
        pts.append((x, 150 + int(18 * math.sin(x / 70.0 + p1) + 9 * math.sin(x / 23.0 + p2)))); x += 6
    pts.append((W_FAR + 20, 300)); c.poly(pts, hl)
    for i in range(1, len(pts) - 2):
        x_, y_ = pts[i]
        if i % 2 == 0: c.pset(x_, y_, hh); c.pset(x_ + 1, y_ + 1, hh)
    return c

def casas(seed, torre_x=78):
    rng = random.Random(seed); c = C(W_FAR, H)
    walls = [haze(col, 0.58, HZ) for col in [(206, 170, 130), (200, 150, 140), (190, 190, 170), (210, 188, 120), (160, 176, 186)]]
    rf = haze((176, 108, 90), 0.58, HZ)
    def fila(x0, x1, ybase):
        x = x0
        while x < x1:
            w = rng.randint(18, 32); h = rng.randint(18, 34); col = rng.choice(walls)
            c.rect(x, ybase - h, w, h + 40, col)
            c.rect(x - 1, ybase - h - 4, w + 2, 4, rf); c.hline(x - 1, ybase - h - 4, w + 2, mix(rf, (255, 230, 200), 0.3))
            for wx in range(x + 4, x + w - 4, 8): c.rect(wx, ybase - h + 6, 3, 5, haze((90, 100, 120), 0.4, HZ))
            x += w + rng.randint(0, 3)
    fila(0, W_FAR, 176)
    def torre(x, base=190):
        tw, th = 30, 84
        body = haze((214, 196, 170), 0.52, HZ); body_l = haze((236, 220, 192), 0.52, HZ); body_d = haze((170, 150, 140), 0.52, HZ); dark = haze((92, 96, 112), 0.42, HZ)
        c.rect(x, base - th, tw, th + 40, body); c.vline(x, base - th, th + 40, body_l); c.vline(x + tw - 1, base - th, th + 40, body_d); c.vline(x + tw - 2, base - th, th + 40, body_d)
        c.hline(x - 2, base - th, tw + 4, body_l); c.hline(x - 2, base - th + 1, tw + 4, body_d)
        for yy in (base - th + 16, base - 28): c.hline(x, yy, tw, body_d)
        c.rect(x + 9, base - th + 22, 12, 22, dark)
        for i in range(6): c.hline(x + 9 + i, base - th + 22 - (6 - i) // 3, 12 - 2 * i, dark)
        c.rect(x + 12, base - th + 33, 6, 4, haze((220, 190, 120), 0.45, HZ))
        c.rect(x + 5, base - th - 12, tw - 10, 12, body); c.vline(x + 5, base - th - 12, 12, body_l); c.vline(x + tw - 6, base - th - 12, 12, body_d)
        for i in range(10):
            ww = int((tw - 8) * math.sqrt(max(0, 1 - (i / 10.0) ** 2)))
            c.hline(x + tw // 2 - ww // 2, base - th - 13 - i, ww, haze((150, 120, 110), 0.5, HZ))
        c.vline(x + tw // 2, base - th - 30, 10, dark); c.hline(x + tw // 2 - 2, base - th - 27, 5, dark)
    torre(torre_x)
    fila(520, W_FAR, 182)        # segunda fileira, mais baixa, à direita
    return c

def build(nome, seed, torre_x, outdir):
    os.makedirs(outdir, exist_ok=True)
    sky().save(f'{outdir}/{nome}_sky.png'); clouds(seed).save(f'{outdir}/{nome}_clouds.png')
    hill(seed).save(f'{outdir}/{nome}_hill.png'); casas(seed, torre_x).save(f'{outdir}/{nome}_casas.png')

if __name__ == '__main__':
    A = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'assets') + '/'
    build('rua', 7, 78, A + 'far')
    build('rua96', 11, 78, A + 'far')
    print('ok')

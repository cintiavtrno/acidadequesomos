import random, math
from pxl import *

FAR_W = 707
SKY = [(146, 184, 214), (164, 196, 220), (184, 208, 224), (204, 220, 224), (224, 228, 218), (240, 232, 208)]

def haze(c, k=0.55, sky=(214, 222, 222)): return mix(c, sky, k)

def far_layer():
    rng = random.Random(7)
    c = C(FAR_W, 270)
    # céu em faixas planas; borda entre faixas com tracejado de 2 px (dither mínimo)
    bh = 30
    for i, col in enumerate(SKY):
        c.rect(0, i * bh, FAR_W, bh, col)
    for i in range(1, len(SKY)):
        y = i * bh
        for x in range(FAR_W):
            if (x + 0) % 2 == 0: c.pset(x, y - 1, SKY[i]); 
            if (x + 1) % 2 == 0: c.pset(x, y, SKY[i - 1])
    c.rect(0, len(SKY) * bh, FAR_W, 270 - len(SKY) * bh, SKY[-1])
    # nuvens achatadas, base mais escura, topo iluminado (luz do alto-esq.)
    def cloud(cx, cy, w):
        for k in range(4):
            ww = int(w * (1 - 0.22 * k)); ox = cx + int(w * 0.08 * k)
            for dx in range(ww):
                t = dx / ww
                hh = int(3 + 4 * math.sin(math.pi * t) * (1 - 0.15 * k))
                for dy in range(hh):
                    col = (252, 246, 236) if dy < hh - 2 else (222, 224, 226)
                    c.pset(ox + dx, cy - k * 2 - dy + hh // 2, col)
    cloud(210, 34, 60); cloud(470, 22, 48); cloud(600, 52, 36); cloud(40, 54, 34)
    HZ = (206, 216, 220)
    # colina distante (vegetação) e casario em névoa
    hill = haze((92, 128, 120), 0.62, HZ); hill_hi = haze((112, 146, 134), 0.62, HZ)
    pts = [(0, 300)]
    x = 0
    while x <= FAR_W + 20:
        pts.append((x, 150 + int(18 * math.sin(x / 70.0) + 9 * math.sin(x / 23.0 + 1))))
        x += 6
    pts.append((FAR_W + 20, 300))
    c.poly(pts, hill)
    for i in range(1, len(pts) - 2):                                  # topo iluminado (copas)
        x_, y_ = pts[i]
        if i % 2 == 0: c.pset(x_, y_, hill_hi); c.pset(x_ + 1, y_ + 1, hill_hi)
    # casario baixo ao longe
    walls = [haze(col, 0.58, HZ) for col in [(206, 170, 130), (200, 150, 140), (190, 190, 170), (210, 188, 120), (160, 176, 186)]]
    rf = haze((176, 108, 90), 0.58, HZ)
    def casas(x0, x1, ybase):
        x = x0
        while x < x1:
            w = rng.randint(18, 32); h = rng.randint(18, 34)
            col = rng.choice(walls)
            c.rect(x, ybase - h, w, h + 40, col)
            c.rect(x - 1, ybase - h - 4, w + 2, 4, rf); c.hline(x - 1, ybase - h - 4, w + 2, mix(rf, (255, 230, 200), 0.3))
            for wx in range(x + 4, x + w - 4, 8):
                c.rect(wx, ybase - h + 6, 3, 5, haze((90, 100, 120), 0.4, HZ))
            x += w + rng.randint(0, 3)
    casas(0, FAR_W, 176)
    # torre da igreja (silhueta alta, névoa), com cúpula e cruz pequena
    def torre(x, base=190):
        tw, th = 30, 84
        body = haze((214, 196, 170), 0.52, HZ); body_l = haze((236, 220, 192), 0.52, HZ); body_d = haze((170, 150, 140), 0.52, HZ)
        dark = haze((92, 96, 112), 0.42, HZ)
        c.rect(x, base - th, tw, th + 40, body); c.vline(x, base - th, th + 40, body_l); c.vline(x + tw - 1, base - th, th + 40, body_d); c.vline(x + tw - 2, base - th, th + 40, body_d)
        c.hline(x - 2, base - th, tw + 4, body_l); c.hline(x - 2, base - th + 1, tw + 4, body_d)      # cimalha
        for yy in (base - th + 16, base - 28):
            c.hline(x, yy, tw, body_d)
        # arco do sino
        c.rect(x + 9, base - th + 22, 12, 22, dark)
        for i in range(6): c.hline(x + 9 + i, base - th + 22 - (6 - i) // 3 - 0, 12 - 2 * i, dark)
        c.rect(x + 12, base - th + 33, 6, 4, haze((220, 190, 120), 0.45, HZ))                          # sino
        # tambor + cúpula + lanterna
        c.rect(x + 5, base - th - 12, tw - 10, 12, body); c.vline(x + 5, base - th - 12, 12, body_l); c.vline(x + tw - 6, base - th - 12, 12, body_d)
        for i in range(10):
            ww = int((tw - 8) * math.sqrt(max(0, 1 - (i / 10.0) ** 2)))
            c.hline(x + tw // 2 - ww // 2, base - th - 13 - i, ww, haze((150, 120, 110), 0.5, HZ))
        c.vline(x + tw // 2, base - th - 30, 10, dark); c.hline(x + tw // 2 - 2, base - th - 27, 5, dark)
    torre(78)
    casas(0, 0, 0)
    # segundo conjunto à direita (fim da rua), mais baixo
    casas(520, FAR_W, 182)
    return c

if __name__ == '__main__':
    far_layer().save('../preview/far_raw.png')

import random, math
from pxl import *

# ---- escala: 1 m = 24 px (horizontal e vertical em fachadas) ----
M = 24
STONE = ramp(222, 0.10, (0.16, 0.28, 0.42, 0.56, 0.70))
CAL   = ramp(46, 0.22, (0.50, 0.62, 0.74, 0.84, 0.92))      # cal / reboco claro
TELHA = ramp(14, 0.50, (0.22, 0.34, 0.46, 0.57, 0.68))
MOSS  = ramp(95, 0.25, (0.22, 0.30, 0.38, 0.46, 0.54))
IRON  = ramp(235, 0.14, (0.10, 0.17, 0.26, 0.36, 0.48))
BRICK = ramp(10, 0.45, (0.24, 0.34, 0.44, 0.54, 0.62))
GLASS = ramp(200, 0.22, (0.14, 0.22, 0.32, 0.46, 0.62))
DARKIN = (26, 20, 22)

def make_wall(c, x, y, w, h, col, rng, base_idx=2):
    """Parede pintada: cor base com bandas largas (luz do alto à esquerda) — sem ruído por pixel."""
    c.rect(x, y, w, h, col[base_idx])
    # coluna esquerda iluminada / direita em leve sombra (quina)
    c.vline(x, y, h, col[min(4, base_idx + 1)])
    c.vline(x + w - 1, y, h, col[max(0, base_idx - 1)])
    c.vline(x + w - 2, y, h, col[max(0, base_idx - 1)])

def _smooth_heights(x0, w, rng, lo, hi, step=17):
    pts = [rng.randint(lo, hi) for _ in range(w // step + 3)]
    out = []
    for i in range(w):
        k = i // step; t = (i % step) / step
        t = t * t * (3 - 2 * t)
        out.append(round(pts[k] * (1 - t) + pts[k + 1] * t))
    return out

def wear_patches(c, x, y, w, h, wallcol, plaster, rng, floor_y, brick=False, clip=None, damp_h=15):
    """Desgaste localizado e orgânico: umidade ascendente (mancha escura de contorno irregular)
    e descascados pontuais onde a umidade é maior; cantaria à mostra só onde a história pede."""
    base = floor_y - 10
    hs = _smooth_heights(x, w, rng, 5, damp_h + 3)
    pe = mix(wallcol[3], plaster[2], 0.55)       # camada antiga exposta (não branco puro)
    for i in range(w):
        for j in range(hs[i]):
            px_, py_ = x + i, base - j
            if clip and not clip(px_, py_): continue
            r, g, b, a = c.get(px_, py_)
            if a: c.pset(px_, py_, tuple(round(v * f) for v, f in zip((r, g, b), SH1 if j < hs[i] - 1 else SH2)) )
    # descascados: 1-3 manchas dentro da zona úmida
    for _ in range(max(1, w // 110)):
        cx = x + rng.randint(14, w - 14); ry = rng.randint(3, 6)
        patch(c, cx, base - rng.randint(3, 6), rng.randint(7, 13), ry, pe, rng, jag=0.38, clip=clip)
        patch(c, cx + 2, base - 4, rng.randint(3, 6), 2, mix(pe, wallcol[1], 0.5), rng, jag=0.3, clip=clip)
    if brick:
        bx = x + w - 40; by = floor_y - 52
        patch(c, bx, by, 14, 14, pe, rng, jag=0.34, clip=clip)
        patch(c, bx + 1, by + 2, 6, 7, BRICK[2], rng, jag=0.3, clip=clip)
        patch(c, bx - 2, by + 5, 3, 3, BRICK[1], rng, jag=0.3, clip=clip)
        c.line(bx - 15, by - 14, bx - 10, by - 3, wallcol[0])        # rachadura que nasce da quina do vão
        c.line(bx - 10, by - 3, bx - 12, by + 6, wallcol[0])

def repaint(c, x, y, w, h, light, rng, clip=None):
    """Retoque de pintura antigo: contorno irregular, diferença sutil de tom (não um degrau inteiro da rampa)."""
    top = _smooth_heights(x, w, rng, 0, 3, 11); bot = _smooth_heights(x, w, rng, 0, 3, 13)
    for i in range(w):
        for yy in range(y + top[i], y + h - bot[i]):
            if clip and not clip(x + i, yy): continue
            r, g, b, a = c.get(x + i, yy)
            if not a: continue
            if light: c.pset(x + i, yy, (*mix((r, g, b), (255, 236, 190), 0.10), a))
            else:     c.pset(x + i, yy, (round(r * 0.93), round(g * 0.93), round(b * 0.97), a))

def streaks(c, x, y, n, rng, fmax=14):
    for k in range(n):
        xx = x + rng.randint(-8, 8); L = rng.randint(6, fmax)
        for j in range(L):
            r, g, b, a = c.get(xx, y + j)
            if a: c.pset(xx, y + j, tuple(round(v * f) for v, f in zip((r, g, b), SH1)))

# ------------------------------------------------------------------ partes
def roof(c, x, y, w, h, rng):
    c.rect(x, y, w, h, TELHA[2])
    for i in range(w):
        m = i % 3
        col = TELHA[1] if m == 0 else (TELHA[3] if m == 1 else TELHA[2])
        for j in range(h): c.pset(x + i, y + j, col)
    # fiadas (sobreposição das telhas), alternadas
    for r in range(4, h - 2, 5):
        off = (r // 5) % 2 * 3
        for i in range(w):
            if (i + off) % 6 < 5: c.pset(x + i, y + r, TELHA[1] if i % 3 != 1 else TELHA[2])
    # telhas antigas / substituídas (aglomerados)
    for _ in range(max(2, w // 60)):
        tx = x + rng.randint(2, w - 12); ty = y + rng.randint(3, h - 6)
        col = rng.choice([TELHA[1], TELHA[4], MOSS[1]])
        for i in range(rng.randint(3, 6)):
            for j in range(rng.randint(2, 4)):
                if c.get(tx + i, ty + j)[3]: c.pset(tx + i, ty + j, col if (tx + i) % 3 != 0 else TELHA[0])
    # cumeeira
    c.hline(x, y, w, TELHA[4]); c.hline(x, y + 1, w, TELHA[3]); c.hline(x, y + 2, w, TELHA[1])
    # beiral: pontas das telhas
    for i in range(w):
        c.pset(x + i, y + h - 1, TELHA[0])
        if i % 3 == 1: c.pset(x + i, y + h - 2, TELHA[0])
    c.vline(x, y, h, TELHA[3]); c.vline(x + w - 1, y, h, TELHA[1])

def cornice(c, x, y, w, col, h=5):
    # sombra projetada na parede abaixo (luz do alto à esquerda)
    c.shade(x + 1, y + h, w - 2, 1, SH3)
    c.shade(x + 1, y + h + 1, w - 2, 2, SH2)
    c.shade(x + 1, y + h + 3, w - 2, 2, SH1)
    c.hline(x - 1, y, w + 2, col[4]); c.hline(x - 1, y + 1, w + 2, col[3])
    c.hline(x - 1, y + 2, w + 2, col[3]); c.hline(x - 1, y + 3, w + 2, col[2]); c.hline(x - 1, y + 4, w + 2, col[1])

def string_course(c, x, y, w, col):
    c.shade(x, y + 3, w, 2, SH2); c.shade(x, y + 5, w, 2, SH1)
    c.hline(x, y, w, col[4]); c.hline(x, y + 1, w, col[3]); c.hline(x, y + 2, w, col[1])

def ashlar(c, x, y, h, w, col, rng):
    """Cunhal de cantaria (pilastra de esquina): blocos alternados."""
    c.rect(x, y, w, h, col[3])
    r = 0
    for yy in range(y, y + h, 8):
        c.hline(x, yy, w, col[1])
        k = (r % 2) * (w // 2)
        if r % 2: c.vline(x + w // 2, yy, 8, col[1])
        r += 1
    c.vline(x, y, h, col[4]); c.vline(x + w - 1, y, h, col[2])

def plinth(c, x, y, w, h, rng):
    c.rect(x, y, w, h, STONE[2])
    r = 0
    for yy in range(y + 2, y + h, 7):
        xx = x - rng.randint(0, 10)
        while xx < x + w:
            bw = rng.randint(14, 26)
            for i in range(max(x, xx), min(x + w, xx + bw)):
                c.pset(i, yy, STONE[3]); c.pset(i, yy + 6, STONE[1])
                if rng.random() < 0.08: c.pset(i, yy + 2, STONE[3])
            if x <= xx + bw - 1 < x + w:
                for j in range(7): c.pset(xx + bw - 1, yy + j, STONE[1])
            xx += bw
        r += 1
    c.hline(x, y, w, STONE[4]); c.hline(x, y + 1, w, STONE[3])
    c.shade(x, y + 2, w, 2, SH1)

def frame(c, x, y, w, h, col, t=2):
    c.rect(x, y, w, h, col[3])
    c.rect(x, y, w, t, col[4]); c.rect(x, y, t, h, col[4])
    c.rect(x + w - t, y, t, h, col[2]); c.rect(x, y + h - t, w, t, col[2])
    c.vline(x + w - 1, y, h, col[1]); c.hline(x, y + h - 1, w, col[1])

def lintel(c, xc, y, w, col):
    """Verga reta com pequena cimalha; sombra cai sobre o vão."""
    c.hline(xc - w // 2 - 2, y - 3, w + 4, col[4]); c.hline(xc - w // 2 - 2, y - 2, w + 4, col[3])
    c.hline(xc - w // 2 - 1, y - 1, w + 2, col[2])
    c.shade(xc - w // 2 - 1, y, w + 2, 2, SH2)

def sill(c, xc, y, w, col):
    c.hline(xc - w // 2 - 2, y, w + 4, col[4]); c.hline(xc - w // 2 - 2, y + 1, w + 4, col[3])
    c.hline(xc - w // 2 - 2, y + 2, w + 4, col[1])
    c.shade(xc - w // 2 - 1, y + 3, w + 4, 2, SH2); c.shade(xc - w // 2, y + 5, w + 3, 2, SH1)

def window_grade(c, xc, yt, w, h, trim, rng):
    x = xc - w // 2
    lintel(c, xc, yt, w, trim)
    frame(c, x, yt, w, h, trim, 2)
    ix, iy, iw, ih = x + 2, yt + 2, w - 4, h - 4
    c.rect(ix, iy, iw, ih, (34, 26, 28))
    c.rect(ix, iy + ih - 7, iw, 7, (52, 38, 34))                 # piso/luz refletida lá dentro
    c.rect(ix + 3, iy + 7, iw - 6, 14, (46, 36, 34))
    c.shade(ix, iy, iw, 3, SH2); c.shade(ix, iy, 2, ih, SH2)       # sombra da espessura da parede
    for bx in range(ix + 2, ix + iw, 4):
        c.vline(bx, iy, ih, IRON[3]); c.vline(bx + 1, iy, ih, IRON[1])
    c.hline(ix, iy + 3, iw, IRON[2]); c.hline(ix, iy + ih - 4, iw, IRON[2])
    sill(c, xc, yt + h, w, trim)

def window_shut(c, xc, yt, w, h, trim, wood, rng):
    x = xc - w // 2
    lintel(c, xc, yt, w, trim)
    frame(c, x, yt, w, h, trim, 2)
    ix, iy, iw, ih = x + 2, yt + 2, w - 4, h - 4
    lw = iw // 2
    for k in range(2):
        lx = ix + k * (lw + (iw - 2 * lw))
        c.rect(lx, iy, lw, ih, wood[2])
        c.rect(lx, iy, lw, 1, wood[3]); c.vline(lx, iy, ih, wood[3])
        c.vline(lx + lw - 1, iy, ih, wood[1]); c.hline(lx, iy + ih - 1, lw, wood[1])
        # painéis rebaixados: veneziana embaixo, almofada em cima
        c.rect(lx + 2, iy + 3, lw - 4, ih // 3 - 1, wood[1]); c.hline(lx + 2, iy + 3, lw - 4, wood[0])
        c.rect(lx + 2, iy + 3, 1, ih // 3 - 1, wood[0])
        for ly in range(iy + ih // 3 + 4, iy + ih - 3, 3):
            c.hline(lx + 2, ly, lw - 4, wood[1]); c.hline(lx + 2, ly + 1, lw - 4, wood[3])
    c.shade(ix, iy, iw, 2, SH2)
    c.vline(ix + lw, iy, ih, wood[0])
    sill(c, xc, yt + h, w, trim)

def balcony_door(c, xc, slab_y, w, dh, trim, wood, rng, lights=True):
    x = xc - w // 2
    yt = slab_y - dh
    lintel(c, xc, yt, w, trim)
    frame(c, x, yt, w, dh, trim, 2)
    ix, iy, iw, ih = x + 2, yt + 2, w - 4, dh - 2
    lw = iw // 2
    # bandeira (vidro) no topo
    gh = 10
    c.rect(ix, iy, iw, gh, GLASS[1])
    c.poly([(ix + 2, iy + gh - 1), (ix + 7, iy + 1), (ix + 9, iy + 1), (ix + 4, iy + gh - 1)], GLASS[3])
    c.vline(ix + lw, iy, gh, trim[2]); c.hline(ix, iy + gh, iw, trim[2]); c.hline(ix, iy + gh + 1, iw, wood[0])
    for k in range(2):
        lx = ix + k * (lw + (iw - 2 * lw))
        top = iy + gh + 2
        c.rect(lx, top, lw, ih - gh - 2, wood[2])
        c.vline(lx, top, ih - gh - 2, wood[3]); c.vline(lx + lw - 1, top, ih - gh - 2, wood[1])
        c.rect(lx + 2, top + 2, lw - 4, 10, wood[1]); c.hline(lx + 2, top + 2, lw - 4, wood[0]); c.vline(lx + 2, top + 2, 10, wood[0])
        for ly in range(top + 15, top + ih - gh - 8, 3):
            c.hline(lx + 2, ly, lw - 4, wood[1]); c.hline(lx + 2, ly + 1, lw - 4, wood[3])
    c.vline(ix + lw, iy + gh + 2, ih - gh - 2, wood[0])
    c.shade(ix, iy, iw, 2, SH2)
    # sacada: laje + cachorros + guarda-corpo de ferro
    sw = w + 14; sx = xc - sw // 2
    c.shade(sx + 2, slab_y + 4, sw, 3, SH2); c.shade(sx + 3, slab_y + 7, sw - 1, 3, SH1)
    for cx_ in (sx + 4, sx + sw - 8):
        c.rect(cx_, slab_y + 3, 4, 4, trim[2]); c.rect(cx_, slab_y + 6, 3, 1, trim[1]); c.vline(cx_, slab_y + 3, 4, trim[3])
    c.hline(sx, slab_y, sw, trim[4]); c.hline(sx, slab_y + 1, sw, trim[3]); c.hline(sx, slab_y + 2, sw, trim[1])
    rh = 22
    for bx in range(sx + 2, sx + sw - 1, 3):
        c.vline(bx, slab_y - rh, rh, IRON[1]); c.vline(bx + 1, slab_y - rh, rh, IRON[3])
    c.hline(sx + 1, slab_y - rh, sw - 2, IRON[3]); c.hline(sx + 1, slab_y - rh + 1, sw - 2, IRON[1])
    c.hline(sx + 1, slab_y - 4, sw - 2, IRON[2])
    for px_ in (sx + 1, sx + sw - 3):
        c.vline(px_, slab_y - rh - 2, rh + 1, IRON[2]); c.vline(px_ + 1, slab_y - rh - 2, rh + 1, IRON[3])
        c.pset(px_, slab_y - rh - 3, IRON[4])

def door_arch(c, xc, y_floor, w, h, trim, wood):
    hw = w // 2
    rise = 9
    spring = y_floor - h + rise
    def top(dx):  # arco abatido (elíptico)
        r = max(0.0, 1 - (dx / hw) ** 2)
        return spring - rise * math.sqrt(r)
    # moldura (vão + 4px)
    for dx in range(-hw - 4, hw + 5):
        t = top(max(-hw, min(hw, dx)) if abs(dx) <= hw else (hw if dx > 0 else -hw)) - (4 if abs(dx) <= hw else 0)
        for yy in range(int(round(t)), y_floor):
            c.pset(xc + dx, yy, trim[3])
    # luz na moldura (esquerda/topo claros, direita escura)
    for dx in range(-hw - 4, hw + 5):
        t = top(max(-hw, min(hw, dx))) - 4 if abs(dx) <= hw else spring
        c.pset(xc + dx, int(round(t)), trim[4])
    c.vline(xc - hw - 4, spring, y_floor - spring, trim[4]); c.vline(xc - hw - 3, spring, y_floor - spring, trim[4])
    c.vline(xc + hw + 4, spring, y_floor - spring, trim[1]); c.vline(xc + hw + 3, spring, y_floor - spring, trim[2])
    # vão escuro
    for dx in range(-hw, hw + 1):
        t = int(round(top(dx)))
        for yy in range(t, y_floor):
            c.pset(xc + dx, yy, (30, 23, 24))
    # interior sugerido: clarão quente de janelas ao fundo + piso iluminado
    c.rect(xc - hw + 8, y_floor - 46, 7, 13, (70, 52, 44)); c.rect(xc + hw - 16, y_floor - 46, 7, 13, (70, 52, 44))
    c.rect(xc - hw, y_floor - 7, w + 1, 7, (58, 42, 36)); c.hline(xc - hw, y_floor - 7, w + 1, (74, 54, 44))
    # folhas abertas vistas de borda (dobradiças) e sombra do lintel
    for dx in list(range(-hw, -hw + 3)) + list(range(hw - 2, hw + 1)):
        for yy in range(int(round(top(dx))) + 1, y_floor):
            c.pset(xc + dx, yy, wood[2] if dx < 0 else wood[1])
    for yy in (y_floor - 55, y_floor - 12):
        c.pset(xc - hw + 2, yy, IRON[3]); c.pset(xc + hw - 2, yy, IRON[3])
    for dx in range(-hw + 3, hw - 2):
        t = int(round(top(dx)))
        for k in range(3): c.pset(xc + dx, t + k, (20, 15, 17))
    # fecho do arco (pedra-chave)
    c.rect(xc - 3, int(top(0)) - 7, 7, 6, trim[4]); c.rect(xc - 3, int(top(0)) - 3, 7, 2, trim[2]); c.vline(xc + 3, int(top(0)) - 7, 6, trim[1])
    # soleira
    c.rect(xc - hw - 6, y_floor - 1, w + 13, 4, STONE[3]); c.hline(xc - hw - 6, y_floor - 1, w + 13, STONE[4]); c.hline(xc - hw - 6, y_floor + 2, w + 13, STONE[1])
    return int(top(0)) - 7

def door_flat(c, xc, y_floor, w, h, trim, wood, iron_bars=True):
    x = xc - w // 2
    lintel(c, xc, y_floor - h, w, trim)
    frame(c, x, y_floor - h, w, h, trim, 2)
    ix, iy, iw, ih = x + 2, y_floor - h + 2, w - 4, h - 2
    if iron_bars:
        c.rect(ix, iy, iw, 9, (34, 26, 28))
        for bx in range(ix + 2, ix + iw, 4): c.vline(bx, iy, 9, IRON[3])
        c.hline(ix, iy + 9, iw, wood[0])
    top = iy + (11 if iron_bars else 0)
    c.rect(ix, top, iw, ih - (11 if iron_bars else 0), wood[2])
    for bx in range(ix + 3, ix + iw, 5):       # tábuas verticais
        c.vline(bx, top, y_floor - top, wood[1]); c.vline(bx + 1, top, y_floor - top, wood[3])
    c.rect(ix + 3, top + 4, iw - 6, 18, wood[1]); c.hline(ix + 3, top + 4, iw - 6, wood[0]); c.vline(ix + 3, top + 4, 18, wood[0])
    c.hline(ix + 3, top + 21, iw - 6, wood[3])
    c.rect(ix + 3, top + 26, iw - 6, y_floor - top - 32, wood[1]); c.hline(ix + 3, top + 26, iw - 6, wood[0]); c.vline(ix + 3, top + 26, y_floor - top - 32, wood[0])
    c.rect(ix + iw - 5, top + 24, 2, 2, IRON[4]); c.pset(ix + iw - 5, top + 26, IRON[1])
    c.shade(ix, iy, iw, 2, SH2)
    c.rect(x - 3, y_floor - 1, w + 6, 4, STONE[3]); c.hline(x - 3, y_floor - 1, w + 6, STONE[4]); c.hline(x - 3, y_floor + 2, w + 6, STONE[1])

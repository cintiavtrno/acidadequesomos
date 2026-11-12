"""Renderizador de personagens em pixel art a partir de volumes 3D simples.

Projeção idêntica às câmeras do jogo (Etapa 1):
  tela_x = 24 * x
  tela_y = -24 * y + D * z          D = 0 (rua, side-view ortográfico)  |  D = 16 (interior, 3/4 oblíquo)
y = altura (m), z = para a câmera (m).  1 m = 24 px na vertical; profundidade do piso = 16 px/m.
"""
import math
import numpy as np
from PIL import Image

PPM = 24.0
CW, CH = 40, 52            # célula de cada frame
AX, AY = 20, 46            # âncora: centro dos pés (x) e linha logo abaixo da sola (y) = chão
SS = 2                     # subamostras por pixel (2x2)
LIGHT = np.array([-0.50, 0.72, 0.62]); LIGHT /= np.linalg.norm(LIGHT)   # luz de cima, à esquerda, de frente (igual ao cenário)
OUT = (30, 18, 16)         # contorno (#1e1210 do protótipo anterior)


def hexc(h):
    h = h.lstrip('#'); return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def rotY(a):
    c, s = math.cos(a), math.sin(a)
    return np.array([[c, 0, s], [0, 1, 0], [-s, 0, c]])


def rotX(a):
    c, s = math.cos(a), math.sin(a)
    return np.array([[1, 0, 0], [0, c, -s], [0, s, c]])


def rotZ(a):
    c, s = math.cos(a), math.sin(a)
    return np.array([[c, -s, 0], [s, c, 0], [0, 0, 1]])


# ------------------------------------------------------------------ SDFs
def sd_ell(q, r):
    k0 = np.linalg.norm(q / r, axis=1)
    k1 = np.linalg.norm(q / (r * r), axis=1)
    return k0 * (k0 - 1.0) / np.maximum(k1, 1e-6)


def sd_cone(P, a, b, ra, rb):
    ba = b - a; l2 = float(ba @ ba)
    if l2 < 1e-9: return np.linalg.norm(P - a, axis=1) - max(ra, rb)
    rr = ra - rb; a2 = l2 - rr * rr; il2 = 1.0 / l2
    pa = P - a; y = pa @ ba; z = y - l2
    t = pa * l2 - np.outer(y, ba); x2 = (t * t).sum(1)
    y2 = y * y * l2; z2 = z * z * l2
    k = np.sign(rr) * rr * rr * x2
    d1 = np.sqrt(x2 + z2) * il2 - rb
    d2 = np.sqrt(x2 + y2) * il2 - ra
    d3 = (np.sqrt(np.maximum(x2 * a2 * il2, 0)) + y * rr) * il2 - ra
    return np.where(np.sign(z) * a2 * z2 > k, d1, np.where(np.sign(y) * a2 * y2 < k, d2, d3))


class Prim:
    """kind 'ell' (c, r) ou 'cone' (a, b, ra, rb); coords no referencial local (origin, R, scale).
    grp = grupo p/ linhas internas; mat = id fixo ou função(local_do_personagem)->ids; cut = (n, d): mantém n·q <= d."""
    def __init__(self, kind, origin, R, scale=(1, 1, 1), grp='body', mat=0, cut=None, tex=None, **kw):
        self.kind = kind; self.o = np.asarray(origin, float); self.R = np.asarray(R, float)
        self.s = np.asarray(scale, float); self.grp = grp; self.mat = mat; self.cut = cut; self.tex = tex; self.kw = kw

    def local(self, P):
        return ((P - self.o) @ self.R) / self.s

    def sd(self, P):
        q = ((P - self.o) @ self.R) / self.s
        if self.kind == 'ell': d = sd_ell(q - self.kw['c'], self.kw['r'])
        else: d = sd_cone(q, self.kw['a'], self.kw['b'], self.kw['ra'], self.kw['rb'])
        d = d * float(self.s.min())
        if self.cut is not None:
            n, c = self.cut; d = np.maximum(d, (q @ np.asarray(n, float) - c) * float(self.s.min()))
        return d


def ell(origin, R, c, r, **kw):
    return Prim('ell', origin, R, c=np.asarray(c, float), r=np.asarray(r, float), **kw)


def cone(origin, R, a, b, ra, rb, **kw):
    return Prim('cone', origin, R, a=np.asarray(a, float), b=np.asarray(b, float), ra=ra, rb=rb, **kw)


# ------------------------------------------------------------------ render
def _scene_sd(prims, P):
    d = prims[0].sd(P)
    for p in prims[1:]: d = np.minimum(d, p.sd(P))
    return d


def render(prims, mats, D, cell=(CW, CH)):
    """Retorna Image RGBA (cell). mats: {id: dict(ramp=[...4 cores escuras->claras], tex=..)}"""
    W, H = cell
    n = W * H * SS * SS
    uu = (np.arange(W * SS) + 0.5) / SS; vv = (np.arange(H * SS) + 0.5) / SS
    U, V = np.meshgrid(uu, vv)
    x = (U - AX) / PPM
    y0 = (AY - V) / PPM
    Zs = 1.6
    O = np.stack([x.ravel(), (y0 + D / PPM * Zs).ravel(), np.full(n, Zs)], 1)
    d = np.array([0.0, -D / PPM, -1.0]); dl = np.linalg.norm(d); dn = d / dl
    # só raios que passam perto do personagem (caixa grossa) — acelera
    t = np.zeros(n); active = np.ones(n, bool); hit = np.zeros(n, bool)
    for _ in range(70):
        idx = np.nonzero(active)[0]
        if not len(idx): break
        P = O[idx] + dn * t[idx, None]
        dist = _scene_sd(prims, P)
        h = dist < 0.0025
        hit[idx[h]] = True; active[idx[h]] = False
        step = np.where(h, 0, dist * 0.85)
        t[idx] += step
        active[idx[t[idx] > 4.0]] = False
    hi = np.nonzero(hit)[0]
    img = np.zeros((H * SS, W * SS, 4), np.uint8)
    out = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    if not len(hi): return out
    P = O[hi] + dn * t[hi, None]
    # material por primitiva mais próxima
    dm = np.stack([p.sd(P) for p in prims], 0)
    owner = dm.argmin(0)
    eps = 0.004
    g = np.stack([_scene_sd(prims, P + np.array(e) * eps) - _scene_sd(prims, P - np.array(e) * eps)
                  for e in ((1, 0, 0), (0, 1, 0), (0, 0, 1))], 1)
    nrm = g / np.maximum(np.linalg.norm(g, axis=1, keepdims=True), 1e-9)
    mid = np.zeros(len(hi), int)
    lam = np.clip(nrm @ LIGHT, 0, 1)
    inten = 0.40 + 0.60 * lam
    for k, p in enumerate(prims):
        sel = owner == k
        if not sel.any(): continue
        q = p.local(P[sel])
        mid[sel] = p.mat(q) if callable(p.mat) else p.mat
        if p.tex is not None: inten[sel] = p.tex(q, inten[sel], mid[sel])
    grp = np.array([p.grp for p in prims])[owner]
    # amostra mais próxima por pixel
    ys, xs = np.divmod(hi, W * SS)
    py, px = ys // SS, xs // SS
    pix = py * W + px
    order = np.argsort(-t[hi])                         # do mais longe p/ o mais perto: o último escrito vence
    best_t = np.full(W * H, 9.0); best_i = np.full(W * H, -1)
    cnt = np.zeros(W * H, int)
    np.add.at(cnt, pix, 1)
    for i in order:
        pp = pix[i]
        if t[hi[i]] < best_t[pp]: best_t[pp] = t[hi[i]]; best_i[pp] = i
    cov = cnt >= 2
    res = {'mask': cov.reshape(H, W), 'depth': best_t.reshape(H, W), 'grp': np.full((H, W), '', object)}
    arr = np.zeros((H, W, 4), np.uint8)
    for pp in np.nonzero(cov)[0]:
        i = best_i[pp]
        ramp = mats[mid[i]]['ramp']; I = inten[i]
        thr = mats[mid[i]].get('thr', (0.50, 0.68, 0.88))
        b = 0 if I < thr[0] else (1 if I < thr[1] else (2 if I < thr[2] else 3))
        b = min(b, len(ramp) - 1)
        c = ramp[b]
        yy, xx = divmod(pp, W)
        arr[yy, xx] = (*c, 255); res['grp'][yy, xx] = grp[i]
    res['arr'] = arr; res['loc'] = None
    return res

"""Pós-processamento: linhas internas, rosto, contorno."""
import numpy as np
from PIL import Image
from render import *
from rig import build, MATS

EYE = (30, 18, 16)

def _proj(pt, D):
    return AX + PPM * pt[0], AY - PPM * pt[1] + D * pt[2]

def face(arr, mask, info, D, pose, who):
    H, W = mask.shape
    Rhw = info['Rhw']; c = info['head']; rx, ry, rz = info['rx'], info['ry'], info['rz']
    toc = np.array([0, D / PPM, 1.0]); toc /= np.linalg.norm(toc)          # direção até a câmera
    def surf(x, y):
        z = rz * math.sqrt(max(0.0, 1 - (x / rx) ** 2 - (y / ry) ** 2))
        loc = np.array([x, y, z]); n = np.array([x / rx ** 2, y / ry ** 2, z / rz ** 2]); n /= np.linalg.norm(n)
        return c + Rhw @ loc, Rhw @ n
    def put(x, y, col, thr=0.22, need=True):
        pw, nw = surf(x, y)
        if float(nw @ toc) < thr: return False
        u, v = _proj(pw, D); iu, iv = int(math.floor(u)), int(math.floor(v))
        if 0 <= iu < W and 0 <= iv < H and (mask[iv, iu] or not need):
            arr[iv, iu] = (*col, 255); return True
        return False
    skin = MATS[who][0]['ramp']
    ey = 0.014 if who == 'lia' else 0.010
    ex = 0.050 if who == 'lia' else 0.048
    mouth = pose.get('mouth', 0); eyes = pose.get('eyes', 1)
    SCL = (236, 228, 208)
    for s_ in (+1, -1):
        if eyes:
            ok = put(s_ * ex, ey, EYE)
            if ok: put(s_ * (ex + 0.040), ey, SCL, thr=0.30)           # esclera do lado de fora
        else: put(s_ * ex, ey - 0.006, skin[0]); put(s_ * (ex + 0.040), ey - 0.006, skin[0], thr=0.30)
    # sobrancelha (Lia: reta e fina; Vó: um pouco mais baixa, caída)
    # boca
    my = -0.062 if who == 'lia' else -0.060
    mc = (110, 46, 42) if who == 'lia' else (96, 44, 38)
    if mouth == 0:
        put(-0.012, my, mc); put(0.012, my, mc)
    elif mouth == 1:
        put(-0.010, my, mc); put(0.010, my, mc); put(0.0, my - 0.012, (66, 26, 24))
    else:
        for dx in (-0.010, 0.010):
            put(dx, my, (66, 26, 24)); put(dx, my - 0.012, (66, 26, 24))
    # bochecha / realce do nariz
    put(0.0, -0.030, skin[3], thr=0.45)
    return arr

def finish(res, who, pose, info, D, lines=True):
    arr = res['arr'].copy(); mask = res['mask'].copy(); grp = res['grp']; depth = res['depth']
    H, W = mask.shape
    # linhas internas: onde um grupo diferente e mais próximo cobre o pixel vizinho
    if lines:
        arr2 = arr.copy()
        for y in range(H):
            for x in range(W):
                if not mask[y, x]: continue
                for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    xx, yy = x + dx, y + dy
                    if 0 <= xx < W and 0 <= yy < H and mask[yy, xx] and grp[yy, xx] != grp[y, x] and depth[yy, xx] < depth[y, x] - 0.045:
                        c = arr[y, x, :3].astype(float); arr2[y, x, :3] = (c * 0.55 + np.array(OUT) * 0.45).astype(np.uint8); break
        arr = arr2
    arr = face(arr, mask, info, D, pose, who)
    # contorno externo
    out = np.zeros((H, W, 4), np.uint8); out[:] = arr
    m = mask
    for y in range(H):
        for x in range(W):
            if m[y, x]: continue
            for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                xx, yy = x + dx, y + dy
                if 0 <= xx < W and 0 <= yy < H and m[yy, xx]:
                    out[y, x] = (*OUT, 255); break
    return Image.fromarray(out, 'RGBA')

SCALE = {'lia': 0.89, 'aurea': 1.0, 'raimundo': 1.0, 'dandara': 1.0, 'lucia': 1.0, 'ze': 1.0, 'nonato': 1.0, 'bela': 0.97, 'cicera': 1.0, 'junior': 0.95, 'tonho': 1.0, 'zefa': 0.90, 'nena': 0.89, 'davi': 1.0, 'rita': 0.90, 'caio': 0.92, 'bia': 0.87, 'm1': 0.92, 'm2': 1.0, 'm3': 0.88, 'm4': 0.96, 'm5': 1.03, 'm6': 0.90}          # Lia 1,38 m (33 px) · Vó ~1,60 m: escala de mundo aplicada à geometria inteira
import render as _R
def frame(who, pose, D):
    global PPM
    u = SCALE[who]; old = PPM; PPM = _R.PPM = 24.0 * u; D = D * u
    try:
        prims, info = build(who, pose, D)
        res = render(prims, MATS[who], D)
        return finish(res, who, pose, info, D)
    finally:
        PPM = _R.PPM = old

"""Esqueleto (FK + IK de 2 ossos) e peças de roupa/cabelo de Lia e Vó Áurea.

Referencial local: x = esquerda do personagem, y = para cima, z = para onde ele olha.  Mundo: yaw 0 = olhando para a câmera.
"""
import math
import numpy as np
from render import *

# --------------------------------------------------------------------------- paletas (4 níveis: sombra -> luz)
def R(*hs): return [hexc(h) for h in hs]

MATS = {
 'lia': {
  0: dict(ramp=R('#3b2318', '#5a3624', '#7a4b32', '#9a6444')),            # pele
  1: dict(ramp=R('#1c1210', '#2c1b14', '#43291e', '#5e3b2a')),            # cabelo
  2: dict(ramp=R('#245a5a', '#2f7a76', '#43a193', '#7cc9b2')),            # camiseta verde-água
  3: dict(ramp=R('#7a3028', '#a04334', '#c4604a', '#dc826a')),            # bermuda terracota
  4: dict(ramp=R('#2a4e8a', '#2f5fa8', '#4a7bc4', '#7aa2de')),            # tira azul da chinela
  5: dict(ramp=R('#b9b09c', '#d6cfbf', '#ece7da', '#faf6ec')),            # sola branca
  6: dict(ramp=R('#8a6a1e', '#c49a2a', '#ecc85a', '#f6e08a')),            # amarelo (elástico / lápis)
  7: dict(ramp=R('#7a2a2a', '#a8383a', '#cc5248', '#e07a66')),            # elástico vermelho
  8: dict(ramp=R('#b9a888', '#d6c8a8', '#ebe0c6', '#f7f0de')),            # papel / caderneta
  9: dict(ramp=R('#101010', '#242020', '#3a3434', '#524a4a')),            # grafite / detalhes escuros
 },
 'aurea': {
  0: dict(ramp=R('#35201a', '#4d2f22', '#6a4130', '#87573e')),
  1: dict(ramp=R('#7d7a78', '#a9a6a2', '#cfccc7', '#ebe9e4')),            # cabelo branco
  2: dict(ramp=R('#1d2a47', '#2b3d66', '#3f5a8c', '#6482b0')),            # vestido índigo
  3: dict(ramp=R('#7a4a2a', '#a06838', '#c08a50', '#dcaa70')),            # couro claro das sandálias
  4: dict(ramp=R('#b9a888', '#d6c8a8', '#ebe0c6', '#f7f0de')),            # avental cru
  5: dict(ramp=R('#8a7e66', '#a89c82', '#c2b698', '#d8cdb0')),            # bolso / barra do avental
  6: dict(ramp=R('#8a6a1e', '#c49a2a', '#ecc85a', '#f6e08a')),            # ouro
  7: dict(ramp=R('#a89c82', '#c2b698', '#ebe0c6', '#f7f0de')),            # botões / costura
  8: dict(ramp=R('#20201e', '#343230', '#4c4a46', '#66625c')),            # cordão / óculos
  9: dict(ramp=R('#101010', '#242020', '#3a3434', '#524a4a')),
 },
}

# --------------------------------------------------------------------------- medidas (m)
SPEC = {
 'lia': dict(hip_w=0.072, pelvis_h=0.620, ankle_h=0.063, thigh=0.26, shin=0.26, sh_w=0.122, sh_y=0.335, neck_y=0.380,
             head_dy=0.185, head_r=(0.126, 0.150, 0.120), arm1=0.19, arm2=0.18, torso_len=0.34, stride=0.50),
 'aurea': dict(hip_w=0.085, pelvis_h=0.740, ankle_h=0.063, thigh=0.32, shin=0.32, sh_w=0.138, sh_y=0.370, neck_y=0.415,
               head_dy=0.170, head_r=(0.118, 0.142, 0.114), arm1=0.24, arm2=0.22, torso_len=0.38, stride=0.44),
}


def ik2(a, t, l1, l2, pole):
    """Joelho/cotovelo para articulação a, alvo t, comprimentos l1, l2 e direção de dobra 'pole'."""
    v = t - a; d = float(np.linalg.norm(v)); d = min(max(d, abs(l1 - l2) + 1e-3), l1 + l2 - 1e-4)
    dirv = v / max(np.linalg.norm(v), 1e-9)
    x = (l1 * l1 - l2 * l2 + d * d) / (2 * d); h = math.sqrt(max(l1 * l1 - x * x, 0))
    pv = pole - dirv * float(pole @ dirv); pn = np.linalg.norm(pv)
    pv = pv / pn if pn > 1e-6 else np.array([0, 0, 1.0])
    return a + dirv * x + pv * h, a + dirv * d


# --------------------------------------------------------------------------- texturas procedurais (estáveis: usam coord. local)
def _h3(q, sc, seed=0):
    g = np.floor(q / sc).astype(np.int64)
    n = (g[:, 0] * 73856093) ^ (g[:, 1] * 19349663) ^ (g[:, 2] * 83492791) ^ (seed * 2654435761)
    n = (n ^ (n >> 13)) * 1274126177
    return ((n ^ (n >> 16)) & 0xFFFF) / 65535.0


def tex_curl(q, inten, mid, sc=0.055):
    """Cabelo crespo: grumos de luz/sombra em pequenos aglomerados."""
    h = _h3(q, sc)
    out = inten.copy()
    out[h > 0.80] += 0.30; out[h < 0.20] -= 0.26
    return np.clip(out, 0, 1)


def tex_none(q, inten, mid): return inten


# --------------------------------------------------------------------------- construção do corpo
def build(who, pose, D):
    """Retorna (prims, info) para a pose dada. info: posições para o rosto."""
    if who in ("raimundo", "dandara", "lucia"):
        import rig_npc
        return rig_npc.build_npc(who, pose, D)
    if who in ("ze", "nonato", "bela", "cicera", "junior", "tonho", "zefa", "nena", "davi", "rita", "caio", "bia", "m1", "m2", "m3", "m4", "m5", "m6"):
        import rig_npc2
        return rig_npc2.build_npc2(who, pose, D)
    S = SPEC[who]; p = dict(pose)
    yaw = p.get('yaw', 0.0); Rr = rotY(yaw)
    W = lambda v: Rr @ np.asarray(v, float)                       # local -> mundo (origem no chão sob o personagem)
    bob = p.get('bob', 0.0); sway = p.get('sway', 0.0)
    pel = np.array([sway, S['pelvis_h'] + bob, p.get('pz', 0.0)])
    Rt = rotY(p.get('twist', 0.0)) @ rotX(p.get('lean', 0.0)) @ rotZ(p.get('troll', 0.0))
    Rp = rotY(p.get('ptwist', 0.0)) @ rotZ(p.get('proll', 0.0))
    sh = {s_: pel + Rt @ np.array([s_ * S['sh_w'], S['sh_y'], 0.0]) for s_ in (+1, -1)}      # +1 = esquerda do personagem
    neck = pel + Rt @ np.array([0, S['neck_y'], 0.012 if who == 'aurea' else 0.0])
    Rh = Rt @ rotY(p.get('hyaw', 0.0)) @ rotX(p.get('hpitch', 0.0)) @ rotZ(p.get('hroll', 0.0))
    head = neck + Rh @ np.array([0, S['head_dy'], 0.01])
    prims = []
    O0 = np.zeros(3); I3 = np.eye(3)
    def wc(a, b, ra, rb, **kw): prims.append(cone(O0, I3, W(a), W(b), ra, rb, **kw))
    def we(c, r, Rl=None, **kw): prims.append(ell(W(c), Rr @ (Rl if Rl is not None else I3), (0, 0, 0), r, **kw))

    # ---------------- pernas (IK) ----------------
    feet = {}
    for s_ in (+1, -1):
        f = p.get('foot_l' if s_ > 0 else 'foot_r', {})
        hip = pel + Rp @ np.array([s_ * S['hip_w'], -0.025, 0.0])
        ank = np.array([s_ * S['hip_w'] + f.get('x', 0.0), S['ankle_h'] + f.get('y', 0.0), f.get('z', 0.0)])
        knee, ank = ik2(hip, ank, S['thigh'], S['shin'], np.array([0.12 * s_, 0.0, 1.0]))
        feet[s_] = (hip, knee, ank, f.get('pitch', 0.0))
        if who == 'lia':
            wc(hip, knee, 0.056, 0.046, mat=0, grp=f'leg{s_}')
            wc(hip, hip + (knee - hip) * 0.42, 0.068, 0.064, mat=3, grp=f'leg{s_}')                  # bainha da bermuda
            wc(knee, ank, 0.043, 0.033, mat=0, grp=f'leg{s_}')
        else:
            wc(hip, knee, 0.054, 0.045, mat=0, grp=f'leg{s_}')
            wc(knee, ank, 0.042, 0.032, mat=0, grp=f'leg{s_}')
        # pé calçado (chinela): tira + sola
        Rf = Rr @ rotX(-f.get('pitch', 0.0))
        if who == 'lia':
            def mf(q): return np.where(q[:, 1] < -0.0800, 5, np.where((q[:, 2] > 0.035) & (q[:, 1] > -0.0800), 4, 0))   # sola / tira / pé
        else:
            def mf(q): return np.where(q[:, 1] < -0.0800, 3, np.where(q[:, 2] > 0.02, 3, 0))
        o = Rr @ ank
        pf = cone(o, Rf, (0, -0.0566, -0.030), (0, -0.0566, 0.090), 0.045, 0.040, mat=mf, grp=f'foot{s_}')
        pf.s = np.array([0.85, 0.62, 1.0])                                  # pé achatado: chinela de dedo
        prims.append(pf)
    # ---------------- tronco ----------------
    o_t = pel; Rtt = Rr @ Rt
    if who == 'lia':
        def mt(q): return np.where(q[:, 1] < -0.030, 3, 2)
        prims.append(cone(Rr @ o_t, Rtt, (0, 0.0, 0), (0, 0.34, 0), 0.112, 0.124, scale=(1, 1, 0.80), mat=mt, grp='body'))
        prims.append(ell(Rr @ o_t, Rtt @ Rp, (0, -0.03, 0), (0.118, 0.090, 0.092), mat=mt, grp='body'))
    else:
        # corpete + saia do vestido (saia só com o giro do quadril) + avental por decalque
        def apron(q, top, hem, hw0, hw1):
            t = np.clip((top - q[:, 1]) / max(top - hem, 1e-6), 0, 1); hw = hw0 + (hw1 - hw0) * t
            return (np.abs(q[:, 0]) < hw) & (q[:, 2] > 0.02) & (q[:, 1] < top) & (q[:, 1] > hem)
        def mb(q):
            m = np.full(len(q), 2)
            m[apron(q, 0.31, -0.40, 0.058, 0.060)] = 4                                                 # peitilho do avental
            btn = (np.abs(q[:, 0]) < 0.012) & (q[:, 2] > 0.02) & (q[:, 1] > 0.03) & (((q[:, 1] * 1000).astype(int)) % 56 < 11)
            m[btn & ~apron(q, 0.31, -0.40, 0.058, 0.060)] = 7
            return m
        prims.append(cone(Rr @ o_t, Rtt, (0, -0.02, 0), (0, 0.37, 0), 0.122, 0.126, scale=(1, 1, 0.80), mat=mb, grp='body'))
        def ms(q):
            m = np.full(len(q), 2)
            ap = apron(q, 1.0, 0.50, 0.100, 0.128)
            m[ap] = 4
            m[ap & (q[:, 1] < 0.56) & (q[:, 1] > 0.535)] = 5                                            # barra do avental
            pk = ap & (np.abs(q[:, 0]) < 0.062) & (q[:, 1] < 0.78) & (q[:, 1] > 0.66)
            m[pk] = 5
            m[pk & ((np.abs(q[:, 0]) > 0.052) | (q[:, 1] > 0.77))] = 4
            return m
        # saia: cone no referencial do mundo (origem no chão), só gira com o yaw
        prims.append(cone(np.zeros(3), Rr, (0, S['pelvis_h'] + bob + 0.12, 0.0), (0, 0.470, 0.0), 0.138, 0.186, scale=(1, 1, 0.90), mat=ms, grp='body'))
    # ---------------- pescoço, cabeça, cabelo ----------------
    wc(neck - Rh @ np.array([0, 0.03, 0]), neck + Rh @ np.array([0, 0.09, 0.012]), 0.042, 0.038, mat=0, grp='head')
    rx, ry, rz = S['head_r']
    Rhw = Rr @ Rh
    prims.append(ell(Rr @ head, Rhw, (0, 0, 0), (rx, ry, rz), mat=0, grp='head'))
    prims.append(ell(Rr @ head + Rhw @ np.array([0, -0.012, rz - 0.004]), Rhw, (0, 0, 0), (0.021, 0.024, 0.026), mat=0, grp='head'))   # nariz
    for s_ in (+1, -1):                                                                                                                # orelhas
        prims.append(ell(Rr @ head + Rhw @ np.array([s_ * (rx - 0.004), -0.008, -0.012]), Rhw, (0, 0, 0), (0.020, 0.032, 0.026), mat=0, grp='head'))
    if who == 'lia':
        # dois coques crespos altos + miolo de cabelo preso; elásticos de cores diferentes
        prims.append(ell(Rr @ head, Rhw, (0, 0.022, -0.026), (rx + 0.014, ry - 0.004, rz + 0.012), mat=1, grp='hair', cut=((0, -1, 0), 0.005), tex=tex_curl))
        for s_, em in ((+1, 6), (-1, 7)):
            c0 = np.array([s_ * 0.080, ry + 0.040, -0.030])
            def mp(q, s_=s_, em=em, c0=c0): return np.where(np.abs(q[:, 1] - (c0[1] - 0.052)) < 0.014, em, 1)
            prims.append(ell(Rr @ head, Rhw, c0, (0.066, 0.062, 0.066), mat=mp, grp='hair', tex=lambda q, i, m: np.where(m == 1, tex_curl(q, i, m), i)))
        # lápis amarelo atrás da orelha esquerda do personagem
        pc = cone(Rr @ head, Rhw, (0.112, 0.030, -0.075), (0.112, 0.030, 0.020), 0.012, 0.010, mat=lambda q: np.where(q[:, 2] > 0.012, 9, 6), grp='pencil')
        prims.append(pc)
    else:
        prims.append(ell(Rr @ head, Rhw, (0, 0.020, -0.024), (rx + 0.012, ry - 0.008, rz + 0.010), mat=1, grp='hair', cut=((0, -1, 0), 0.010), tex=lambda q, i, m: tex_curl(q, i, m, 0.05)))
        for s_ in (+1, -1):                                                                                                            # argolinhas douradas
            prims.append(ell(Rr @ head + Rhw @ np.array([s_ * (rx + 0.004), -0.058, -0.004]), Rhw, (0, 0, 0), (0.014, 0.022, 0.014), mat=6, grp='head'))
    # ---------------- braços (IK) ----------------
    hands = {}
    for s_ in (+1, -1):
        a = p.get('arm_l' if s_ > 0 else 'arm_r', {})
        shp = sh[s_]
        if 'tgt' in a: tgt = np.array(a['tgt'], float)
        else:
            sw, ab, ext = a.get('sw', 0.0), a.get('ab', 0.10), a.get('ext', 0.94)
            dirv = np.array([s_ * math.sin(ab), -math.cos(sw) * math.cos(ab), math.sin(sw) * math.cos(ab)])
            tgt = shp + (Rt @ dirv) * (S['arm1'] + S['arm2']) * ext
        pole = Rt @ np.array([s_ * 0.55, -0.9, -0.55])
        el, wr = ik2(shp, tgt, S['arm1'], S['arm2'], pole)
        hands[s_] = (shp, el, wr)
        if who == 'lia':
            wc(shp, el, 0.037, 0.032, mat=0, grp=f'arm{s_}')
            wc(shp, shp + (el - shp) * 0.50, 0.048, 0.045, mat=2, grp=f'arm{s_}')                    # manga curta
            wc(el, wr, 0.031, 0.027, mat=0, grp=f'arm{s_}')
        else:
            wc(shp, el, 0.036, 0.031, mat=0, grp=f'arm{s_}')
            wc(shp, shp + (el - shp) * 0.78, 0.047, 0.043, mat=2, grp=f'arm{s_}')                    # manga até o cotovelo
            wc(el, wr, 0.030, 0.026, mat=0, grp=f'arm{s_}')
            wc(wr - (wr - el) * 0.18, wr - (wr - el) * 0.10, 0.032, 0.032, mat=6, grp=f'arm{s_}')   # pulseira fina
        we(wr + (wr - el) / max(np.linalg.norm(wr - el), 1e-6) * 0.012, (0.032, 0.036, 0.032) if who == 'lia' else (0.034, 0.038, 0.034), mat=0, grp=f'arm{s_}')
    # ---------------- acessórios ----------------
    if who == 'lia':
        # caderneta do fiado no bolso de trás (lado esquerdo do personagem): só aparece de lado/costas
        prims.append(ell(Rr @ o_t, Rtt, (0.074, -0.040, -0.080), (0.034, 0.046, 0.016), mat=lambda q: np.where(q[:, 1] > -0.040 + 0.030, 7, 8), grp='body'))
    else:
        # óculos pendurados no cordão sobre o peito + corrente fina
        prims.append(ell(Rr @ o_t, Rtt, (0.0, 0.215, 0.100), (0.050, 0.014, 0.012), mat=8, grp='body'))
        prims.append(cone(Rr @ o_t, Rtt, (0.044, 0.320, 0.062), (0.0, 0.216, 0.096), 0.006, 0.006, mat=8, grp='body'))
        prims.append(cone(Rr @ o_t, Rtt, (-0.044, 0.320, 0.062), (0.0, 0.216, 0.096), 0.006, 0.006, mat=8, grp='body'))
    info = dict(head=Rr @ head, Rhw=Rhw, rx=rx, ry=ry, rz=rz, who=who, feet=feet, hands=hands, pel=Rr @ pel)
    return prims, info

import rig_npc  # registra paletas e medidas dos clientes

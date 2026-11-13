"""Gravação de 1996 na rua: percussionistas de um bloco afro, o cantor e a equipe de filmagem.
Mesma câmera, escala, esqueleto/IK e renderização dos moradores (rig_npc2): 1 m = 24 px, célula 40x52, contorno e luz iguais.
Acrescenta peças novas (tambores com correia, câmeras, tripé, headset, prancheta, cases) e camisetas estampadas por função de material."""
import math
import numpy as np
from render import *
import rig
from rig import R, ik2, tex_curl
from rig_npc2 import mats, SK, SHOE, SOLE, DARK

RED = ('#5a1616', '#921f20', '#cf3a2a', '#f06a4a'); YEL = ('#8a5e0a', '#c8920e', '#f2c42a', '#fbe47c')
GRN = ('#0a4224', '#116a38', '#22a04e', '#52cf80'); BLK = ('#0c0a0a', '#1c1818', '#302a2a', '#4a4242')
WHT = ('#a8a49c', '#cfcbc2', '#ece8de', '#fbf9f2'); JEAN = ('#1e3050', '#2c4472', '#4562a0', '#6e8cc8'); JEAN2 = ('#2a3c5e', '#3a5280', '#5470a4', '#7c98c8')
KHA = ('#6a5a3a', '#8a7a52', '#aa9a6c', '#cabc8c'); NAVY = ('#14203a', '#1e3058', '#2f4a82', '#4e6eaa'); GRY = ('#3a3a40', '#54545c', '#74747e', '#9a9aa4')
CAM = ('#16161a', '#26262c', '#3c3c44', '#5a5a64')          # corpo da câmera
CASE = ('#2a2a2e', '#3c3c42', '#56565e', '#787882')          # case de transporte (metal escuro)
SKIN = {'a': ('#2c1810', '#442a1c', '#5e3c2a', '#7c5238'), 'b': ('#3a2216', '#58361f', '#7a4c30', '#9a6644'), 'c': ('#4a2c1e', '#6a4230', '#8a5a40', '#a87452'),
        'd': ('#5a3826', '#7a4f36', '#9a6a4a', '#b88460'), 'e': ('#241410', '#3a2218', '#503022', '#6c4430'), 'f': ('#6a4230', '#8a5a40', '#a87452', '#c48e68'),
        'g': ('#7a5238', '#9a6c4c', '#bc8a64', '#d8aa84'), 'h': ('#8a6244', '#aa7c58', '#c89c74', '#e0bc96')}
HAIRC = ('#100a08', '#1e1410', '#2e201a', '#42302a'); HAIRG = ('#6a6a68', '#92928e', '#b8b8b2', '#dcdcd6')


# ---------------------------------------------------------------- camisetas estampadas (material por posição no tronco)
def shirt(kind, c):
    """c = (a, b, c, d): ids de material. Vermelho/amarelo/verde/preto em faixas, blocos, diagonais ou metades."""
    a, b, cc, d = c
    if kind == 'bands':        # faixas horizontais no peito
        return lambda q: np.select([q[:, 1] > 0.30, q[:, 1] > 0.215, q[:, 1] > 0.135, q[:, 1] > 0.06], [a, b, cc, d], a)
    if kind == 'diag':         # faixa diagonal larga, do ombro ao quadril
        def f(q):
            t = q[:, 1] - q[:, 0] * 0.9
            return np.select([t > 0.34, t > 0.25, t > 0.16, t > 0.07], [a, b, cc, d], a)
        return f
    if kind == 'blocks':       # blocos: ombros, peito dividido e barra
        def f(q):
            top = q[:, 1] > 0.29; mid = (q[:, 1] <= 0.29) & (q[:, 1] > 0.12)
            return np.where(top, a, np.where(mid, np.where(q[:, 0] > 0, b, cc), d))
        return f
    if kind == 'vert':         # faixas verticais
        return lambda q: np.select([np.abs(q[:, 0]) < 0.022, np.abs(q[:, 0]) < 0.062, np.abs(q[:, 0]) < 0.092], [b, cc, d], a)
    if kind == 'halves':       # metades, com uma faixa cruzando
        return lambda q: np.where((q[:, 1] > 0.17) & (q[:, 1] < 0.24), cc, np.where(q[:, 0] > 0, a, b))
    if kind == 'chevron':      # V sobre o peito
        def f(q):
            v = q[:, 1] - 0.34 + np.abs(q[:, 0]) * 1.2
            return np.select([v > 0.11, v > 0.0, v > -0.09], [a, b, cc], d)
        return f
    return lambda q: np.full(len(q), a)


def peace_shirt(q):
    """Camiseta branca (2) com símbolo da paz grande em preto (9) e detalhes amarelo (6), vermelho (7) e verde (8); a palavra vira uma linha de letras acima."""
    x, y, z = q[:, 0], q[:, 1], q[:, 2]; fr = z > 0.0
    cx, cy = 0.0, 0.262; dx, dy = x - cx, y - cy; r = np.hypot(dx, dy)
    ring = (r < 0.118) & (r > 0.096)
    vert = (np.abs(dx) < 0.0085) & (dy > -0.118) & (dy < 0.118)
    dl = (np.abs(dx + dy * 0.0 - (-dy) * 1.0) < 0.0100) & (dy < 0.0) & (dx < 0.0) & (r < 0.118)          # diagonal esquerda-baixo
    dr = (np.abs(dx - (-dy) * 1.0) < 0.0100) & (dy < 0.0) & (dx > 0.0) & (r < 0.118)
    inside = (r <= 0.096) & ~vert & ~dl & ~dr
    m = np.full(len(q), 2)
    sector = np.where(dy > 0.0, np.where(dx < 0, 6, 8), np.where(np.abs(dx) < -dy * 1.0, 7, 6))          # amarelo / verde / vermelho
    m = np.where(fr & inside, sector, m)
    m = np.where(fr & (ring | vert | dl | dr), 9, m)
    word = fr & (y > 0.372) & (y < 0.395) & (np.abs(x) < 0.085) & ((np.floor((x + 0.085) / 0.0285).astype(int) % 2) == 0)   # OLODUM: seis traços
    m = np.where(word, np.where((np.floor((x + 0.085) / 0.0285).astype(int) // 2) % 3 == 0, 7, np.where((np.floor((x + 0.085) / 0.0285).astype(int) // 2) % 3 == 1, 6, 9)), m)
    return m


def vest(q):          # colete de fotógrafo (4 = bolsos) por cima da camiseta (2)
    pk = (np.abs(np.abs(q[:, 0]) - 0.065) < 0.032) & (q[:, 2] > 0.0) & (((q[:, 1] > 0.02) & (q[:, 1] < 0.09)) | ((q[:, 1] > 0.15) & (q[:, 1] < 0.22)))
    return np.where(pk, 6, 2)


# ---------------------------------------------------------------- elenco: paletas, medidas e configuração
PERC = {   # 6 percussionistas: pele, cabelo, estilo, medidas, tambor, camiseta, bermuda/calça, ritmo
 'perc1': dict(skin='c', hair='afro', hc=HAIRC, h=1.00, bw=1.04, drum='L', shirt=('bands', (2, 6, 7, 8)), cols=(RED, YEL, GRN, BLK), pants=JEAN, leg='long', style=0, belly=0.02),
 'perc2': dict(skin='a', hair='trancas', hc=HAIRC, h=1.02, bw=0.94, drum='M', shirt=('diag', (2, 6, 7, 8)), cols=(YEL, RED, GRN, BLK), pants=BLK, leg='bermuda', style=1, belly=0.0),
 'perc3': dict(skin='d', hair='cachos', hc=HAIRC, h=0.97, bw=0.90, drum='S', shirt=('blocks', (2, 6, 7, 8)), cols=(GRN, YEL, RED, BLK), pants=KHA, leg='long', style=2, belly=0.0),
 'perc4': dict(skin='b', hair='raspado', hc=HAIRC, h=1.03, bw=1.08, drum='L', shirt=('vert', (2, 6, 7, 8)), cols=(BLK, RED, YEL, GRN), pants=JEAN2, leg='bermuda', style=1, belly=0.03),
 'perc5': dict(skin='f', hair='curto_cacheado', hc=HAIRC, h=0.98, bw=0.92, drum='M', shirt=('halves', (2, 6, 7, 8)), cols=(RED, BLK, YEL, GRN), pants=BLK, leg='long', style=0, belly=0.0),
 'perc6': dict(skin='e', hair='bald', hc=HAIRG, h=1.00, bw=1.00, drum='S', shirt=('chevron', (2, 6, 7, 8)), cols=(YEL, GRN, RED, BLK), pants=JEAN, leg='long', style=2, belly=0.015, hairgray=True),
}
DRUM = {'L': dict(r=0.175, h=0.42, yc=0.015, zc=0.255, tilt=0.30), 'M': dict(r=0.135, h=0.34, yc=0.035, zc=0.225, tilt=0.28), 'S': dict(r=0.102, h=0.25, yc=0.060, zc=0.195, tilt=0.26)}
SHELL = {'perc1': (2, 6, 7), 'perc2': (7, 2, 6), 'perc3': (6, 7, 2), 'perc4': (2, 7, 6), 'perc5': (6, 2, 7), 'perc6': (7, 6, 2)}   # cor de cada tambor (3 faixas)

def _spec(h, bw, belly=0.0):
    k = h
    return dict(hip_w=0.080 * bw, pelvis_h=0.770 * k, ankle_h=0.063, thigh=0.335 * k, shin=0.335 * k, sh_w=0.138 * bw, sh_y=0.385, neck_y=0.425, head_dy=0.170,
                head_r=(0.112, 0.138, 0.110), arm1=0.246 * k, arm2=0.230 * k, torso_len=0.40, stride=0.44)

CFG96 = {}
for n, d in PERC.items():
    cols = d['cols']
    rig.MATS[n] = mats(SKIN[d['skin']], d['hc'], cols[0], d['pants'], hat=cols[2], acc=cols[1], aux=cols[3])
    rig.SPEC[n] = _spec(d['h'], d['bw'])
    CFG96[n] = dict(leg=d['leg'], sleeve=0.50, belly=d['belly'], hair=d['hair'], hat=None, bw=d['bw'], shirt=shirt(d['shirt'][0], d['shirt'][1]), kind='perc', drum=d['drum'], style=d['style'], pk=n)

# cantor: magro e esguio, pele clara, cachos pretos volumosos; camiseta branca com símbolo da paz; jeans e sapato preto
rig.MATS['cantor'] = mats(SKIN['g'], HAIRC, WHT, JEAN, hat=RED, acc=YEL, aux=GRN, shoe=BLK)
rig.SPEC['cantor'] = dict(hip_w=0.066, pelvis_h=0.800, ankle_h=0.063, thigh=0.352, shin=0.352, sh_w=0.118, sh_y=0.385, neck_y=0.425, head_dy=0.172,
                          head_r=(0.100, 0.138, 0.102), arm1=0.250, arm2=0.236, torso_len=0.40, stride=0.40)
CFG96['cantor'] = dict(leg='long', sleeve=0.46, belly=0.0, hair='cachos_cantor', hat=None, bw=0.76, aw=0.80, lw=0.80, shirt=peace_shirt, kind='cantor', shoe_mat=4, pk='cantor')

# equipe de filmagem
rig.MATS['cam1'] = mats(SKIN['b'], HAIRC, NAVY, JEAN, hat=GRY, acc=CAM, aux=CASE, shoe=BLK)
rig.MATS['cam2'] = mats(SKIN['d'], HAIRC, GRN, KHA, hat=GRY, acc=CAM, aux=CASE, shoe=SHOE)
rig.MATS['assist'] = mats(SKIN['f'], HAIRC, WHT, BLK, hat=GRY, acc=CASE, aux=SOLE, shoe=BLK)
rig.MATS['carga'] = mats(SKIN['c'], HAIRC, GRY, KHA, hat=GRY, acc=CASE, aux=CAM, shoe=BLK)
rig.MATS['diretor'] = mats(SKIN['h'], HAIRG, KHA, BLK, hat=KHA, acc=CAM, aux=SOLE, shoe=SHOE)
rig.SPEC['cam1'] = _spec(1.02, 1.04); rig.SPEC['cam2'] = _spec(0.98, 1.0); rig.SPEC['assist'] = _spec(0.95, 0.90); rig.SPEC['carga'] = _spec(1.00, 1.10); rig.SPEC['diretor'] = _spec(1.02, 1.0)
CFG96['cam1'] = dict(leg='long', sleeve=0.50, belly=0.0, hair='short', hat='bone', bw=1.04, kind='cam1', pk='cam1')
CFG96['cam2'] = dict(leg='long', sleeve=0.52, belly=0.01, hair='curto_cacheado', hat=None, bw=1.0, kind='cam2', pk='cam2')
CFG96['assist'] = dict(leg='long', sleeve=0.50, belly=0.0, hair='cachos', hat='headset', bw=0.90, kind='assist', pk='assist')
CFG96['carga'] = dict(leg='long', sleeve=0.44, belly=0.02, hair='raspado', hat=None, bw=1.10, kind='carga', pk='carga')
CFG96['diretor'] = dict(leg='long', sleeve=0.60, belly=0.025, hair='short', hat='bucket', bw=1.0, kind='diretor', glasses=True, shirt=vest, pk='diretor')
# operador de câmera SEM tripé nem câmera no corpo: o equipamento fica no cenário (props tripe_cam_d/e) e o operador se posiciona atrás dele
rig.MATS['cam2o'] = rig.MATS['cam2']; rig.SPEC['cam2o'] = rig.SPEC['cam2']
CFG96['cam2o'] = dict(CFG96['cam2'], kind='cam2o', pk='cam2o')
# segundo operador de câmera e segundo assistente: outros rostos e roupas, mesma animação
rig.MATS['cam3o'] = mats(SKIN['a'], HAIRC, GRY, JEAN, hat=GRY, acc=CAM, aux=CASE, shoe=BLK)
rig.SPEC['cam3o'] = _spec(1.04, 1.06)
CFG96['cam3o'] = dict(CFG96['cam2'], kind='cam2o', hair='short', bw=1.06, pk='cam3o')
rig.MATS['assist2'] = mats(SKIN['c'], HAIRC, NAVY, KHA, hat=GRY, acc=CASE, aux=SOLE, shoe=SHOE)
rig.SPEC['assist2'] = _spec(0.93, 0.95)
CFG96['assist2'] = dict(CFG96['assist'], hair='afro', bw=0.95, pk='assist2')
WHO = tuple(CFG96)
PERCS = tuple(PERC)

import pipeline as _P
for n in WHO: _P.SCALE[n] = 1.0 if n not in ('assist', 'perc3') else 0.96
_P.SCALE['perc3'] = 0.94; _P.SCALE['perc6'] = 0.98; _P.SCALE['cantor'] = 1.03; _P.SCALE['cam1'] = 1.0; _P.SCALE['carga'] = 1.0; _P.SCALE['perc4'] = 1.02


# ---------------------------------------------------------------- construção do corpo
def _R3(p):
    return rotY(p.get('twist', 0.0)) @ rotX(p.get('lean', 0.0)) @ rotZ(p.get('troll', 0.0))


def build96(who, pose, D):
    S = rig.SPEC[who]; C_ = CFG96[who]; p = dict(pose)
    yaw = p.get('yaw', 0.0); Rr = rotY(yaw)
    W = lambda v: Rr @ np.asarray(v, float)
    bob = p.get('bob', 0.0); sway = p.get('sway', 0.0)
    pel = np.array([sway, S['pelvis_h'] + bob, p.get('pz', 0.0)])
    Rt = _R3(p); Rp = rotY(p.get('ptwist', 0.0)) @ rotZ(p.get('proll', 0.0))
    sh = {s_: pel + Rt @ np.array([s_ * S['sh_w'], S['sh_y'], 0.0]) for s_ in (+1, -1)}
    neck = pel + Rt @ np.array([0, S['neck_y'], 0.012])
    Rh = Rt @ rotY(p.get('hyaw', 0.0)) @ rotX(p.get('hpitch', 0.0)) @ rotZ(p.get('hroll', 0.0))
    head = neck + Rh @ np.array([0, S['head_dy'], 0.01])
    prims = []; O0 = np.zeros(3); I3 = np.eye(3)
    def wc(a, b, ra, rb, **kw): prims.append(cone(O0, I3, W(a), W(b), ra, rb, **kw))
    def we(c, r, Rl=None, **kw): prims.append(ell(W(c), Rr @ (Rl if Rl is not None else I3), (0, 0, 0), r, **kw))
    bw = C_.get('bw', 1.0); aw = C_.get('aw', 1.0); lw = C_.get('lw', 1.0); bermuda = C_['leg'] == 'bermuda'
    shoe = C_.get('shoe_mat', 4)
    for s_ in (+1, -1):
        f = p.get('foot_l' if s_ > 0 else 'foot_r', {})
        hip = pel + Rp @ np.array([s_ * S['hip_w'], -0.025, 0.0])
        ank = np.array([s_ * S['hip_w'] + f.get('x', 0.0), S['ankle_h'] + f.get('y', 0.0), f.get('z', 0.0)])
        knee, ank = ik2(hip, ank, S['thigh'], S['shin'], np.array([0.12 * s_, 0.0, 1.0]))
        if bermuda:
            wc(hip, knee, 0.060 * lw, 0.050 * lw, mat=3, grp=f'leg{s_}'); wc(knee, ank, 0.042 * lw, 0.032 * lw, mat=0, grp=f'leg{s_}')
        else:
            wc(hip, knee, 0.060 * lw, 0.050 * lw, mat=3, grp=f'leg{s_}'); wc(knee, ank, 0.048 * lw, 0.040 * lw, mat=3, grp=f'leg{s_}')
        Rf = Rr @ rotX(-f.get('pitch', 0.0)); o = Rr @ ank
        mf = (lambda q: np.where(q[:, 1] < -0.0800, 5, shoe))
        pf = cone(o, Rf, (0, -0.0566, -0.030), (0, -0.0566, 0.095), 0.046 * lw, 0.040 * lw, mat=mf, grp=f'foot{s_}')
        pf.s = np.array([0.88, 0.66, 1.0]); prims.append(pf)
    Rtt = Rr @ Rt; o_t = pel; bl = C_.get('belly', 0.0)
    sf = C_.get('shirt')
    if sf is not None: mt = sf
    else: mt = (lambda q: 2)
    prims.append(cone(Rr @ o_t, Rtt, (0, -0.02, 0), (0, 0.39, 0), (0.118 + bl) * bw, 0.126 * bw, scale=(1, 1, 0.82 + bl * 3), mat=mt, grp='body'))
    prims.append(ell(Rr @ o_t, Rtt @ Rp, (0, -0.03, 0), (0.122 * bw + bl, 0.092, 0.098 + bl * 1.5), mat=3, grp='body'))
    wc(neck - Rh @ np.array([0, 0.03, 0]), neck + Rh @ np.array([0, 0.09, 0.012]), 0.043 * aw, 0.039 * aw, mat=0, grp='head')
    rx, ry, rz = S['head_r']; Rhw = Rr @ Rh
    prims.append(ell(Rr @ head, Rhw, (0, 0, 0), (rx, ry, rz), mat=0, grp='head'))
    prims.append(ell(Rr @ head + Rhw @ np.array([0, -0.012, rz - 0.004]), Rhw, (0, 0, 0), (0.022, 0.025, 0.027), mat=0, grp='head'))
    for s_ in (+1, -1):
        prims.append(ell(Rr @ head + Rhw @ np.array([s_ * (rx - 0.004), -0.008, -0.012]), Rhw, (0, 0, 0), (0.020, 0.032, 0.026), mat=0, grp='head'))
    H = lambda c, r, **kw: prims.append(ell(Rr @ head, Rhw, c, r, **kw))
    h = C_['hair']
    if h == 'short': H((0, 0.014, -0.030), (rx + 0.008, ry - 0.028, rz + 0.004), mat=1, grp='hair', cut=((0, -1, 0), 0.020))
    elif h == 'bald':
        H((0, -0.010, -0.040), (rx + 0.006, ry - 0.060, rz - 0.020), mat=1, grp='hair', cut=((0, -1, 0), 0.010))
        H((0, 0.050, -0.010), (rx - 0.004, 0.020, rz * 0.7), mat=0, grp='head')
    elif h == 'raspado': H((0, 0.010, -0.014), (rx + 0.005, ry - 0.020, rz + 0.003), mat=1, grp='hair', cut=((0, -1, 0), 0.030))
    elif h == 'curto_cacheado': H((0, 0.022, -0.026), (rx + 0.016, ry - 0.002, rz + 0.012), mat=1, grp='hair', cut=((0, -1, 0), 0.005), tex=lambda q, i, m: tex_curl(q, i, m, 0.05))
    elif h == 'afro': H((0, 0.034, -0.022), (rx + 0.052, ry + 0.012, rz + 0.044), mat=1, grp='hair', cut=((0, -1, 0), -0.010), tex=lambda q, i, m: tex_curl(q, i, m, 0.055))
    elif h == 'cachos':
        H((0, 0.026, -0.024), (rx + 0.026, ry + 0.004, rz + 0.020), mat=1, grp='hair', cut=((0, -1, 0), 0.000), tex=lambda q, i, m: tex_curl(q, i, m, 0.045))
    elif h == 'cachos_cantor':      # cachos volumosos de comprimento médio, caindo pelos lados e atrás
        H((0, 0.036, -0.030), (rx + 0.066, ry + 0.016, rz + 0.056), mat=1, grp='hair', cut=((0, -1, 0), -0.030), tex=lambda q, i, m: tex_curl(q, i, m, 0.050))
        for sx in (+1, -1):
            H((sx * (rx + 0.030), -0.040, -0.030), (0.040, 0.058, 0.056), mat=1, grp='hair', tex=lambda q, i, m: tex_curl(q, i, m, 0.045))
        H((0, -0.050, -rz * 0.80), (rx * 0.80, 0.070, 0.050), mat=1, grp='hair', tex=lambda q, i, m: tex_curl(q, i, m, 0.045))
    elif h == 'trancas':
        H((0, 0.012, -0.022), (rx + 0.008, ry - 0.016, rz + 0.006), mat=1, grp='hair', cut=((0, -1, 0), 0.010))
        for k_, sx in enumerate((-0.07, -0.025, 0.025, 0.07)):       # tranças penduradas atrás e ao lado
            a = head + Rh @ np.array([sx, 0.020, -rz * 0.80]); b = head + Rh @ np.array([sx * 1.25, -0.20 - 0.02 * (k_ % 2), -rz * 0.95])
            wc(a, b, 0.021, 0.014, mat=1, grp='hair')
    hat = C_.get('hat')
    if hat == 'bone':
        H((0, ry * 0.58, -0.010), (rx + 0.016, 0.052, rz + 0.016), mat=7, grp='hat')
        H((0, ry * 0.40, rz * 0.82), (0.066, 0.014, 0.050), mat=7, grp='hat')
    elif hat == 'bucket':           # chapéu de pano de aba curta
        H((0, ry * 0.48, -0.004), (rx + 0.024, 0.056, rz + 0.024), mat=7, grp='hat')
        H((0, ry * 0.34, 0.000), (rx + 0.064, 0.014, rz + 0.060), mat=7, grp='hat')
    elif hat == 'headset':          # arco sobre a cabeça, conchas nas orelhas e microfone na boca
        for s_ in (+1, -1):
            a = head + Rh @ np.array([s_ * (rx + 0.008), -0.006, -0.012]); m_ = head + Rh @ np.array([s_ * (rx * 0.66), ry * 0.86, -0.012]); t_ = head + Rh @ np.array([0, ry + 0.010, -0.012])
            wc(a, m_, 0.009, 0.009, mat=9, grp='hat'); wc(m_, t_, 0.009, 0.009, mat=9, grp='hat')
            H((s_ * (rx + 0.012), -0.006, -0.012), (0.024, 0.034, 0.030), mat=9, grp='hat')
        a = head + Rh @ np.array([rx + 0.016, -0.010, 0.0]); m2 = head + Rh @ np.array([rx * 0.8, -0.056, rz * 0.82]); wc(a, m2, 0.006, 0.006, mat=9, grp='hat')
        H((rx * 0.8, -0.056, rz * 0.86), (0.014, 0.012, 0.012), mat=9, grp='hat')
    if C_.get('glasses'): H((0, 0.012, rz - 0.006), (rx - 0.006, 0.014, 0.012), mat=9, grp='head')
    hands = {}; sl = C_['sleeve']
    for s_ in (+1, -1):
        a = p.get('arm_l' if s_ > 0 else 'arm_r', {}); shp = sh[s_]
        if 'tgt' in a: tgt = np.array(a['tgt'], float)
        else:
            sw, ab, ext = a.get('sw', 0.0), a.get('ab', 0.10), a.get('ext', 0.94)
            dirv = np.array([s_ * math.sin(ab), -math.cos(sw) * math.cos(ab), math.sin(sw) * math.cos(ab)])
            tgt = shp + (Rt @ dirv) * (S['arm1'] + S['arm2']) * ext
        pole = Rt @ np.array([s_ * 0.55, -0.9, -0.55])
        el, wr = ik2(shp, tgt, S['arm1'], S['arm2'], pole); hands[s_] = (shp, el, wr)
        wc(shp, el, 0.038 * aw, 0.033 * aw, mat=0, grp=f'arm{s_}')
        wc(shp, shp + (el - shp) * sl, 0.049 * aw, 0.045 * aw, mat=2, grp=f'arm{s_}')
        wc(el, wr, 0.031 * aw, 0.027 * aw, mat=0, grp=f'arm{s_}')
        we(wr + (wr - el) / max(np.linalg.norm(wr - el), 1e-6) * 0.012, (0.034, 0.038, 0.034), mat=0, grp=f'arm{s_}')
    ctx = dict(W=W, Rr=Rr, Rt=Rt, Rtt=Rtt, o_t=o_t, pel=pel, sh=sh, hands=hands, head=head, Rh=Rh, Rhw=Rhw, p=p, S=S, C=C_, wc=wc, we=we, prims=prims, rx=rx, ry=ry, rz=rz, who=who)
    EXTRA[C_['kind']](ctx)
    info = dict(head=Rr @ head, Rhw=Rhw, rx=rx, ry=ry, rz=rz, who=who, feet={}, hands=hands, pel=Rr @ pel)
    return prims, info


# ---------------------------------------------------------------- adereços
def _tl(ctx, v):         # ponto do referencial do tronco -> mundo (pré-giro de yaw)
    return ctx['pel'] + ctx['Rt'] @ np.asarray(v, float)


def x_perc(ctx):
    """Tambor preso por duas correias nos ombros, na frente do corpo; baquetas nas mãos."""
    C_ = ctx['C']; Dm = DRUM[C_['drum']]; W = ctx['W']; Rr, Rtt, Rt = ctx['Rr'], ctx['Rtt'], ctx['Rt']; prims = ctx['prims']
    r, hh, tilt = Dm['r'], Dm['h'] / 2, Dm['tilt']
    cen = np.array([0, Dm['yc'], Dm['zc']])
    org = Rr @ _tl(ctx, cen); Rd = Rtt @ rotX(tilt)
    sc = SHELL[C_['pk']]
    def ms(q): return np.select([q[:, 1] > hh * 0.50, q[:, 1] < -hh * 0.50], [sc[0], sc[2]], sc[1])
    prims.append(cyl(org, Rd, (0, 0, 0), r, hh, rr=0.012, mat=ms, grp='drum'))
    prims.append(cyl(org, Rd, (0, hh - 0.004, 0), r + 0.006, 0.012, rr=0.006, mat=9, grp='drum'))          # aro de metal
    prims.append(cyl(org, Rd, (0, hh + 0.004, 0), r - 0.010, 0.006, rr=0.003, mat=5, grp='drum'))          # pele clara
    prims.append(cyl(org, Rd, (0, -hh + 0.012, 0), r + 0.004, 0.008, rr=0.004, mat=9, grp='drum'))         # aro de baixo
    Rdl = rotX(tilt)
    for s_ in (+1, -1):                                                                                      # correias: ombro -> borda do tambor
        top = _tl(ctx, cen + Rdl @ np.array([s_ * r * 0.80, hh * 0.9, 0.0]))
        wc = ctx['wc']; wc(ctx['sh'][s_] + np.array([0, 0.01, 0]), top, 0.011, 0.011, mat=9, grp='strap')
    # baquetas
    for s_ in (+1, -1):
        shp, el, wr = ctx['hands'][s_]; d = (wr - el) / max(np.linalg.norm(wr - el), 1e-6)
        a = wr - d * 0.035; b = wr + d * 0.20 + np.array([0, -0.045, 0.045])
        ctx['wc'](a, b, 0.0085, 0.0075, mat=5, grp=f'arm{s_}')
        ctx['we'](b + 0.0, (0.014, 0.014, 0.014), mat=5, grp=f'arm{s_}')


def _box(ctx, c, h, mat, R=None, rr=0.008, grp='gear'):
    ctx['prims'].append(box(np.zeros(3), np.eye(3) if R is None else R, c, h, rr=rr, mat=mat, grp=grp))


def x_cam1(ctx):
    """Câmera profissional de ombro (anos 90): corpo, lente com para-sol, visor, bateria e alça."""
    W, Rr = ctx['W'], ctx['Rr']; prims = ctx['prims']; R_ = Rr @ ctx['Rt']
    sh = ctx['sh'][-1]                                            # ombro direito do personagem
    org = Rr @ (sh + ctx['Rt'] @ np.array([0.015, 0.075, 0.07]))
    L = 0.40
    prims.append(box(org, R_, (0, 0, 0.0), (0.072, 0.085, L / 2), rr=0.014, mat=lambda q: np.where(q[:, 1] > 0.045, 9, 6), grp='cam'))      # corpo
    prims.append(box(org, R_, (-0.035, 0.0, -L / 2 - 0.045), (0.050, 0.075, 0.060), rr=0.012, mat=9, grp='cam'))                              # bateria
    prims.append(box(org, R_, (0.088, 0.045, 0.01), (0.030, 0.044, 0.110), rr=0.010, mat=6, grp='cam'))                                       # visor
    Rl = R_ @ rotX(math.pi / 2)
    prims.append(cyl(org, Rl, (0, L / 2 + 0.04, 0.0), 0.058, 0.060, rr=0.010, mat=9, grp='cam'))                                              # lente
    prims.append(cyl(org, Rl, (0, L / 2 + 0.110, 0.0), 0.070, 0.026, rr=0.008, mat=6, grp='cam'))                                             # para-sol
    prims.append(box(org, R_, (0, 0.105, 0.04), (0.012, 0.016, 0.070), rr=0.006, mat=9, grp='cam'))                                           # alça de cima


def x_cam2(ctx):
    """Câmera sobre tripé à frente do operador."""
    prims = ctx['prims']; Rr = ctx['Rr']; W = ctx['W']; wc = ctx['wc']
    z0 = 0.52; ytop = 1.28
    top = np.array([0, ytop, z0])
    for fx, fz in ((0, 0.30), (0.27, -0.16), (-0.27, -0.16)):
        wc(top, np.array([fx, 0.0, z0 + fz]), 0.016, 0.011, mat=9, grp='tripod')
    wc(top + np.array([0, -0.30, 0]), top + np.array([0, 0.02, 0]), 0.014, 0.014, mat=9, grp='tripod')
    org = Rr @ (top + np.array([0, 0.115, 0.0]))
    prims.append(box(org, Rr, (0, 0, 0), (0.075, 0.082, 0.215), rr=0.014, mat=lambda q: np.where(q[:, 1] > 0.045, 9, 6), grp='cam'))
    prims.append(box(org, Rr, (-0.030, 0.0, -0.255), (0.050, 0.072, 0.055), rr=0.012, mat=9, grp='cam'))
    prims.append(box(org, Rr, (0.092, 0.040, -0.02), (0.028, 0.042, 0.100), rr=0.010, mat=6, grp='cam'))
    Rl = Rr @ rotX(math.pi / 2)
    prims.append(cyl(org, Rl, (0, 0.250, 0.0), 0.056, 0.060, rr=0.010, mat=9, grp='cam'))
    prims.append(cyl(org, Rl, (0, 0.320, 0.0), 0.068, 0.024, rr=0.008, mat=6, grp='cam'))
    wc(top + np.array([0.12, 0.03, -0.05]), top + np.array([0.15, -0.05, -0.28]), 0.010, 0.010, mat=9, grp='tripod')      # barra de pan
    wc(top + np.array([0.12, 0.03, -0.05]), top + np.array([0.12, 0.03, 0.04]), 0.010, 0.010, mat=9, grp='tripod')


def x_assist(ctx):
    """Prancheta no antebraço esquerdo (do personagem), rádio comunicador no cinto e lápis."""
    prims = ctx['prims']; Rr = ctx['Rr']; shp, el, wr = ctx['hands'][+1]; wc = ctx['wc']
    d = (wr - el) / max(np.linalg.norm(wr - el), 1e-6); mid = (el + wr) / 2 + d * 0.06
    Rb = Rr @ ctx['Rt']
    nrm = np.cross(d, np.array([1.0, 0, 0])); nrm = nrm / max(np.linalg.norm(nrm), 1e-6)
    ux = np.cross(nrm, d); ux /= max(np.linalg.norm(ux), 1e-6)
    Rcl = np.stack([ux, d, nrm], 1)                              # eixos: x=largura, y=comprimento, z=espessura
    prims.append(box(Rr @ mid, Rr @ Rcl, (0, 0, 0.03), (0.075, 0.105, 0.007), rr=0.004, mat=8, grp='clip'))
    prims.append(box(Rr @ mid, Rr @ Rcl, (0, 0.100, 0.035), (0.030, 0.012, 0.008), rr=0.004, mat=9, grp='clip'))
    prims.append(box(Rr @ _tl(ctx, (0.115, -0.03, 0.0)), Rb, (0, 0, 0), (0.026, 0.050, 0.018), rr=0.008, mat=9, grp='radio'))     # rádio no cinto
    prims.append(cone(Rr @ _tl(ctx, (0.115, 0.02, 0.0)), Rb, (0, 0, 0), (0, 0.075, 0), 0.005, 0.004, mat=9, grp='radio'))


def x_carga(ctx):
    """Case de equipamento na mão direita (do personagem) e rolo de cabo no ombro esquerdo."""
    prims = ctx['prims']; Rr = ctx['Rr']; shp, el, wr = ctx['hands'][-1]
    c = wr + np.array([0.0, -0.17, 0.0])
    prims.append(box(Rr @ c, Rr, (0, 0, 0), (0.060, 0.150, 0.200), rr=0.012, mat=lambda q: np.where(np.abs(q[:, 1]) > 0.12, 9, 8), grp='case'))
    prims.append(box(Rr @ (wr + np.array([0, -0.025, 0])), Rr, (0, 0, 0), (0.014, 0.020, 0.075), rr=0.006, mat=9, grp='case'))     # alça
    Rb = Rr @ ctx['Rt']; cs = _tl(ctx, (0.150, 0.34, 0.0))
    prims.append(ell(Rr @ cs, Rb @ rotZ(0.5), (0, 0, 0), (0.060, 0.092, 0.092), mat=9, grp='cable'))
    prims.append(ell(Rr @ _tl(ctx, (-0.07, 0.18, 0.115)), Rb @ rotZ(-0.6), (0, 0, 0), (0.018, 0.150, 0.018), mat=9, grp='cable'))     # cabo cruzando o peito
    prims.append(box(Rr @ _tl(ctx, (-0.13, 0.00, -0.115)), Rb, (0, 0, 0), (0.040, 0.075, 0.070), rr=0.010, mat=8, grp='case'))          # estojo pequeno nas costas


def x_diretor(ctx):
    """Colete de fotógrafo (material); ao andar leva um roteiro dobrado; observa de braços e queixo."""
    prims = ctx['prims']; Rr = ctx['Rr']
    if ctx['p'].get('script'):
        shp, el, wr = ctx['hands'][+1]
        prims.append(box(Rr @ (wr + np.array([0.0, -0.01, 0.045])), Rr, (0, 0, 0), (0.060, 0.082, 0.010), rr=0.004, mat=8, grp='clip'))


def x_cantor(ctx): pass


EXTRA = {'cam2o': lambda ctx: None, 'perc': x_perc, 'cam1': x_cam1, 'cam2': x_cam2, 'assist': x_assist, 'carga': x_carga, 'diretor': x_diretor, 'cantor': x_cantor}


# ---------------------------------------------------------------- animação
import anim as A
G = lambda **k: dict(dict(T=0.96, step=0.40, lift=0.050, bob=0.011, arm=0.20, lean=0.06, sway=0.010, head=0.02, hand_out=0.10), **k)
A.GAIT.update({
 'perc1': G(T=1.00, step=0.38, lean=-0.03, bob=0.014), 'perc2': G(T=0.92, step=0.42, lean=-0.02, bob=0.016), 'perc3': G(T=0.86, step=0.42, lean=-0.02, bob=0.018),
 'perc4': G(T=1.04, step=0.36, lean=-0.04, bob=0.014), 'perc5': G(T=0.96, step=0.40, lean=-0.02, bob=0.015), 'perc6': G(T=1.08, step=0.34, lean=-0.03, bob=0.012),
 'cantor': G(T=0.90, step=0.30, lift=0.040, bob=0.008, arm=0.12, lean=0.02, sway=0.016, head=0.03),
 'cam1': G(T=1.00, step=0.38, lean=0.04), 'cam2': G(T=1.00, step=0.38, lean=0.05), 'cam2o': G(T=1.00, step=0.38, lean=0.04), 'cam3o': G(T=1.00, step=0.38, lean=0.04), 'assist2': G(T=0.82, step=0.44, arm=0.30, lean=0.04), 'assist': G(T=0.80, step=0.44, arm=0.30, lean=0.04),
 'carga': G(T=1.00, step=0.38, lean=0.02), 'diretor': G(T=1.06, step=0.40, lean=0.04, arm=0.20),
})
A.ANIMS.update({'drum': (4, 6.0, True), 'drumwalk': (8, None, True), 'sway': (4, 4.0, True), 'pose': (4, 2.0, True), 'film': (4, 2.0, True), 'note': (4, 5.0, True),
                'radio': (4, 3.0, True), 'watch': (4, 2.0, True), 'point': (4, 4.0, True), 'carry': (4, 2.0, True), 'carrywalk': (8, None, True), 'camwalk': (8, None, True)})


def _hit(k, off, n=4):                 # 0..1: 1 = braço no alto, 0 = batida
    return 0.5 + 0.5 * math.cos(2 * math.pi * ((k + off) % n) / n)


def _drum_arms(who, k, n=4, style=0, amp=0.11):
    C_ = CFG96[who]; Dm = DRUM[C_['drum']]; S = rig.SPEC[who]
    ytop = S['pelvis_h'] + Dm['yc'] + Dm['h'] / 2 * math.cos(Dm['tilt']) + 0.045; zc = Dm['zc'] + Dm['h'] / 2 * math.sin(Dm['tilt'])
    spread = Dm['r'] * 0.50
    offs = ((0, n // 2), (0, n // 4), (n // 4, n * 3 // 4))[style]
    l = _hit(k, offs[0], n); r = _hit(k, offs[1], n)
    return dict(arm_l=dict(tgt=(spread, ytop + amp * l, zc + 0.02 - 0.03 * l)), arm_r=dict(tgt=(-spread, ytop + amp * r, zc + 0.02 - 0.03 * r)))


def pose96(who, anim, k, yaw):
    C_ = CFG96[who]; kind = C_['kind']; g = A.GAIT[who]
    if anim in ('idle', 'talk', 'wave', 'turn') and kind != 'perc':
        p = {'idle': A.idle_pose, 'talk': A.talk_pose, 'wave': A.wave_pose, 'turn': A.turn_pose}[anim](who, k)
    elif anim == 'walk' or anim == 'drumwalk' or anim == 'camwalk' or anim == 'carrywalk':
        p = A.walk_pose(who, k)
    else:
        p = A.idle_pose(who, k)
    p['yaw'] = yaw
    if kind == 'perc':
        st = C_['style']
        if anim in ('idle', 'talk', 'wave', 'turn', 'sit'):          # tambor em repouso: baquetas apoiadas, corpo balançando de leve
            p = A.idle_pose(who, k); p.update(_drum_arms(who, k, 4, st, 0.03)); p['bob'] = (0, -0.008, 0, -0.008)[k] * (1 + st); p['yaw'] = yaw
            if anim == 'talk': p['mouth'] = (1, 2, 1, 0)[k]
        elif anim == 'drum':
            p = A.idle_pose(who, k); p.update(_drum_arms(who, k, 4, st, 0.13 + 0.02 * st))
            p['bob'] = -0.014 * (1 - _hit(k, 0)) * (1 if st != 2 else 0.5); p['hpitch'] = (0.0, 0.08, 0.0, 0.08)[(k + st) % 4]; p['lean'] = -0.03 + 0.02 * _hit(k, 1)
            p['sway'] = (0.0, 0.010, 0.0, -0.010)[(k + st) % 4]; p['twist'] = (0.05, 0.0, -0.05, 0.0)[(k + st) % 4] * (1 if st == 1 else 0.4)
            p['mouth'] = 1 if st == 1 and k % 2 else 0; p['yaw'] = yaw
        elif anim == 'drumwalk':
            arms = _drum_arms(who, k, 8, st, 0.12); p.update(arms); p['hpitch'] = -0.04 + 0.04 * math.sin(2 * math.pi * (k + st) / 4); p['yaw'] = yaw
            p['twist'] = 0.05 * math.cos(2 * math.pi * k / 8); p['ptwist'] = -0.04 * math.cos(2 * math.pi * k / 8)
    elif kind == 'cantor':
        if anim == 'walk':      # passos curtos, ombros e cabeça discretos
            a = 2 * math.pi * k / 8
            p['arm_l'] = dict(sw=-0.16 * math.cos(a), ab=0.10, ext=0.92); p['arm_r'] = dict(sw=0.16 * math.cos(a), ab=0.10, ext=0.92)
            p['hroll'] = 0.04 * math.sin(a); p['hyaw'] = 0.05 * math.sin(a + 1.2); p['troll'] = 0.035 * math.sin(a); p['yaw'] = yaw
        elif anim == 'wave':    # aceno com uma das mãos
            up = (0.5, 1.0, 0.6, 1.0)[k]; p = A.wave_pose(who, k); p['arm_r'] = dict(tgt=(-0.30 - 0.04 * (k % 2), 1.20 + 0.16 * up, 0.04)); p['hroll'] = 0.07; p['mouth'] = 0; p['yaw'] = yaw
        elif anim == 'sway':    # movimento rítmico de tronco e braços, sem dança contínua
            p = A.idle_pose(who, k); s = (0.0, 0.8, 0.0, -0.8)[k]
            p['troll'] = 0.05 * s; p['proll'] = -0.04 * s; p['sway'] = 0.012 * s; p['hroll'] = -0.05 * s; p['bob'] = (0, -0.01, 0, -0.01)[k]
            p['arm_l'] = dict(tgt=(0.19, 0.84 + 0.05 * s, 0.10)); p['arm_r'] = dict(tgt=(-0.19, 0.84 - 0.05 * s, 0.10)); p['yaw'] = yaw
        elif anim == 'pose':    # breves poses para a gravação
            p = A.idle_pose(who, 0); i = k
            if i == 0: p['arm_l'] = dict(tgt=(0.20, 0.86, -0.02)); p['arm_r'] = dict(tgt=(-0.18, 0.84, 0.10)); p['hroll'] = 0.08
            elif i == 1: p['arm_r'] = dict(tgt=(-0.20, 1.50, 0.10)); p['arm_l'] = dict(tgt=(0.18, 0.80, 0.10)); p['hpitch'] = -0.10; p['lean'] = -0.04
            elif i == 2: p['arm_l'] = dict(tgt=(0.10, 1.12, 0.22)); p['arm_r'] = dict(tgt=(-0.10, 1.12, 0.22)); p['hpitch'] = 0.05
            else: p['arm_r'] = dict(tgt=(-0.30, 1.30, 0.28)); p['arm_l'] = dict(tgt=(0.17, 0.80, 0.10)); p['hroll'] = -0.06; p['mouth'] = 1
            p['yaw'] = yaw
    elif kind in ('cam1', 'cam2', 'cam2o'):
        shp_y = rig.SPEC[who]['pelvis_h']
        if kind == 'cam1':
            cy = rig.SPEC[who]['pelvis_h'] + 0.385 + 0.075 - 0.02                      # altura da câmera no ombro
            def hold(wob=0.0):
                return dict(arm_r=dict(tgt=(-0.15, cy - 0.12 + wob, 0.12)), arm_l=dict(tgt=(0.06, cy - 0.06 + wob, 0.44)))
            if anim in ('idle', 'film', 'camwalk', 'talk', 'turn', 'wave'):
                if anim in ('camwalk', 'walk'): p = A.walk_pose(who, k); p['lean'] = 0.0; p['hpitch'] = 0.04
                else: p = A.idle_pose(who, k)
                p.update(hold(0.004 * (0, 1, 0, -1)[k % 4] if anim != 'camwalk' else 0.0)); p['hroll'] = -0.10; p['hyaw'] = -0.12; p['hpitch'] = p.get('hpitch', 0) + 0.03; p['yaw'] = yaw
                if anim == 'film': p['bob'] = (0, -0.004, 0, -0.002)[k]
            if anim == 'walk': p = A.walk_pose(who, k); p.update(hold()); p['hroll'] = -0.08; p['yaw'] = yaw
        else:   # cam2: opera câmera no tripé (à frente); ao andar carrega o tripé dobrado no ombro
            if anim in ('idle', 'film', 'talk', 'turn', 'wave'):
                p = A.idle_pose(who, k); y = rig.SPEC[who]['pelvis_h'] + 0.34
                p['arm_l'] = dict(tgt=(0.12, 1.28 + 0.004 * (0, 1, 0, -1)[k], 0.40)); p['arm_r'] = dict(tgt=(-0.14, 1.22 + 0.02 * (0, 0, 1, 0)[k], 0.34))
                p['lean'] = 0.07; p['hpitch'] = 0.06; p['hroll'] = 0.06; p['yaw'] = yaw
            elif anim in ('walk', 'camwalk'):
                p = A.walk_pose(who, k); p['yaw'] = yaw
                if kind == 'cam2': p['arm_r'] = dict(tgt=(-0.16, 1.28, 0.02))
    elif kind == 'assist':
        if anim in ('idle', 'talk', 'turn', 'wave'): p = {'idle': A.idle_pose, 'talk': A.talk_pose, 'turn': A.turn_pose, 'wave': A.wave_pose}[anim](who, k)
        if anim in ('idle', 'talk', 'turn', 'wave', 'note', 'radio', 'walk'):
            if anim == 'walk': p = A.walk_pose(who, k)
            left = dict(tgt=(0.14, 1.02, 0.20))
            if anim == 'note':
                p = A.idle_pose(who, k); p['hpitch'] = 0.28; p['lean'] = 0.06; p['arm_r'] = dict(tgt=(-0.06 + 0.03 * (0, 1, 0, -1)[k], 1.04, 0.24 + 0.02 * (1, 0, -1, 0)[k]))
            elif anim == 'radio':
                p = A.idle_pose(who, k); p['arm_r'] = dict(tgt=(-0.10, 1.40 + 0.01 * (0, 1, 0, 0)[k], 0.20)); p['hroll'] = 0.05; p['mouth'] = (1, 2, 1, 0)[k]
            elif anim == 'walk': p['arm_r'] = dict(sw=0.30 * math.cos(2 * math.pi * k / 8), ab=0.10, ext=0.92)
            else: p['arm_r'] = p.get('arm_r', dict(tgt=(-0.17, 0.80, 0.10)))
            p['arm_l'] = left; p['yaw'] = yaw
    elif kind == 'carga':
        if anim in ('idle', 'carry'):
            p = A.idle_pose(who, k); p['arm_r'] = dict(tgt=(-0.19, 0.74 + 0.004 * (0, 1, 0, -1)[k], 0.02)); p['arm_l'] = dict(tgt=(0.17, 0.80, 0.10)); p['lean'] = -0.03; p['troll'] = 0.02; p['yaw'] = yaw
        elif anim in ('walk', 'carrywalk'):
            p = A.walk_pose(who, k); a = 2 * math.pi * k / 8
            p['arm_r'] = dict(tgt=(-0.19, 0.76 + 0.012 * math.cos(2 * a), 0.02 + 0.06 * math.sin(a))); p['arm_l'] = dict(sw=-0.22 * math.cos(a), ab=0.10, ext=0.92); p['troll'] = 0.025; p['yaw'] = yaw
    elif kind == 'diretor':
        if anim == 'watch':       # braço no cotovelo e mão no queixo, olhando a cena
            p = A.idle_pose(who, k); p['arm_l'] = dict(tgt=(0.06, 0.98, 0.16)); p['arm_r'] = dict(tgt=(-0.04, 1.30 + 0.01 * (0, 1, 0, 0)[k], 0.17)); p['hpitch'] = (0.04, 0.07, 0.04, 0.02)[k]; p['hyaw'] = (0.0, 0.10, 0.0, -0.10)[k]; p['lean'] = 0.03; p['yaw'] = yaw
        elif anim == 'point':     # orienta a posição dos participantes
            p = A.idle_pose(who, k); up = (0.4, 1.0, 1.0, 0.6)[k]
            p['arm_r'] = dict(tgt=(-0.24, 1.18 + 0.05 * up, 0.40 + 0.18 * up)); p['arm_l'] = dict(tgt=(0.15, 0.96, 0.18)); p['mouth'] = (1, 2, 1, 0)[k]; p['lean'] = 0.05; p['yaw'] = yaw
        elif anim == 'walk': p = A.walk_pose(who, k); p['script'] = True; p['arm_l'] = dict(tgt=(0.16, 1.00, 0.26)); p['yaw'] = yaw
        else:
            p = {'idle': A.idle_pose, 'talk': A.talk_pose, 'turn': A.turn_pose, 'wave': A.wave_pose}.get(anim, A.idle_pose)(who, k); p['yaw'] = yaw
    p['yaw'] = yaw
    return p

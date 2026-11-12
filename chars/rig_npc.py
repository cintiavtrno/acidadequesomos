"""Corpos dos clientes (Etapa 4): Seu Raimundo, Dandara e Lúcia — mesmo esqueleto/IK de Lia e Vó, com roupas e cabelos próprios."""
import math
import numpy as np
from render import *
import rig
from rig import R, ik2, tex_curl, tex_none

SKIN = lambda a, b, c, d: dict(ramp=R(a, b, c, d))
rig.MATS.update({
 'raimundo': {0: SKIN('#35201a', '#4d2f22', '#6a4130', '#87573e'), 1: SKIN('#6a6a68', '#8e8c88', '#b5b3ae', '#dad8d2'),
              2: SKIN('#8b94a0', '#b0b8c0', '#d2d8dc', '#eef1f2'), 3: SKIN('#4a4640', '#665f54', '#837a6a', '#a39a86'),
              4: SKIN('#24160e', '#3a2418', '#54362a', '#704a38'), 5: SKIN('#6a5a48', '#8a7a64', '#a89880', '#c8b8a0'),
              6: SKIN('#5a1c1c', '#7e2828', '#a63a36', '#c85c52'), 7: SKIN('#3a4452', '#4f5d70', '#6a7a90', '#8b9bb0'),
              8: SKIN('#b9b09c', '#d6cfbf', '#ece7da', '#faf6ec'), 9: SKIN('#101010', '#242020', '#3a3434', '#524a4a')},
 'dandara': {0: SKIN('#3b2318', '#5a3624', '#7a4b32', '#9a6444'), 1: SKIN('#141010', '#221916', '#352622', '#4c3830'),
             2: SKIN('#4a1c2a', '#6a2a3c', '#8e3d52', '#b4627a'), 3: SKIN('#2a2433', '#3c344a', '#554a66', '#75698a'),
             4: SKIN('#7a4a2a', '#a06838', '#c08a50', '#dcaa70'), 5: SKIN('#8a7e66', '#a89c82', '#c2b698', '#d8cdb0'),
             6: SKIN('#8a6a1e', '#c49a2a', '#ecc85a', '#f6e08a'), 7: SKIN('#8a6a1e', '#c49a2a', '#ecc85a', '#f6e08a'),
             8: SKIN('#101216', '#1e222a', '#2e343e', '#434b58'), 9: SKIN('#101010', '#242020', '#3a3434', '#524a4a')},
 'lucia': {0: SKIN('#5a3a28', '#7c5238', '#a07050', '#c09470'), 1: SKIN('#1e1410', '#30201a', '#46302a', '#644840'),
           2: SKIN('#8a95a8', '#b0bac8', '#d2d9e2', '#eef2f6'), 3: SKIN('#1c2236', '#2a3350', '#3c4a70', '#566690'),
           4: SKIN('#7a7a80', '#9a9aa2', '#c0c0c8', '#e4e4ea'), 5: SKIN('#a8a8a0', '#c8c8c0', '#e4e4dc', '#f8f8f2'),
           6: SKIN('#a04a10', '#d06a18', '#ec8c2c', '#fcb24c'), 7: SKIN('#8a6a1e', '#c49a2a', '#ecc85a', '#f6e08a'),
           8: SKIN('#8a6a44', '#a8865a', '#c8a678', '#e2c898'), 9: SKIN('#101010', '#242020', '#3a3434', '#524a4a')},
})
rig.SPEC.update({
 'raimundo': dict(hip_w=0.080, pelvis_h=0.775, ankle_h=0.063, thigh=0.335, shin=0.335, sh_w=0.135, sh_y=0.385, neck_y=0.425, head_dy=0.170,
                  head_r=(0.115, 0.140, 0.112), arm1=0.245, arm2=0.230, torso_len=0.40, stride=0.38),
 'dandara': dict(hip_w=0.085, pelvis_h=0.765, ankle_h=0.063, thigh=0.330, shin=0.330, sh_w=0.140, sh_y=0.375, neck_y=0.420, head_dy=0.175,
                 head_r=(0.116, 0.142, 0.114), arm1=0.240, arm2=0.220, torso_len=0.38, stride=0.46),
 'lucia': dict(hip_w=0.082, pelvis_h=0.780, ankle_h=0.063, thigh=0.335, shin=0.335, sh_w=0.138, sh_y=0.380, neck_y=0.420, head_dy=0.172,
               head_r=(0.114, 0.140, 0.112), arm1=0.245, arm2=0.225, torso_len=0.38, stride=0.48),
})
NPCS = ('raimundo', 'dandara', 'lucia')

def build_npc(who, pose, D):
    S = rig.SPEC[who]; p = dict(pose)
    yaw = p.get('yaw', 0.0); Rr = rotY(yaw)
    W = lambda v: Rr @ np.asarray(v, float)
    bob = p.get('bob', 0.0); sway = p.get('sway', 0.0)
    pel = np.array([sway, S['pelvis_h'] + bob, p.get('pz', 0.0)])
    Rt = rotY(p.get('twist', 0.0)) @ rotX(p.get('lean', 0.0)) @ rotZ(p.get('troll', 0.0))
    Rp = rotY(p.get('ptwist', 0.0)) @ rotZ(p.get('proll', 0.0))
    sh = {s_: pel + Rt @ np.array([s_ * S['sh_w'], S['sh_y'], 0.0]) for s_ in (+1, -1)}
    neck = pel + Rt @ np.array([0, S['neck_y'], 0.012])
    Rh = Rt @ rotY(p.get('hyaw', 0.0)) @ rotX(p.get('hpitch', 0.0)) @ rotZ(p.get('hroll', 0.0))
    head = neck + Rh @ np.array([0, S['head_dy'], 0.01])
    prims = []; O0 = np.zeros(3); I3 = np.eye(3)
    def wc(a, b, ra, rb, **kw): prims.append(cone(O0, I3, W(a), W(b), ra, rb, **kw))
    def we(c, r, Rl=None, **kw): prims.append(ell(W(c), Rr @ (Rl if Rl is not None else I3), (0, 0, 0), r, **kw))
    skirt = who == 'dandara'
    feet = {}
    for s_ in (+1, -1):
        f = p.get('foot_l' if s_ > 0 else 'foot_r', {})
        hip = pel + Rp @ np.array([s_ * S['hip_w'], -0.025, 0.0])
        ank = np.array([s_ * S['hip_w'] + f.get('x', 0.0), S['ankle_h'] + f.get('y', 0.0), f.get('z', 0.0)])
        knee, ank = ik2(hip, ank, S['thigh'], S['shin'], np.array([0.12 * s_, 0.0, 1.0]))
        feet[s_] = (hip, knee, ank, f.get('pitch', 0.0))
        if skirt:
            wc(hip, knee, 0.054, 0.045, mat=0, grp=f'leg{s_}'); wc(knee, ank, 0.042, 0.032, mat=0, grp=f'leg{s_}')
        else:
            wc(hip, knee, 0.060, 0.050, mat=3, grp=f'leg{s_}'); wc(knee, ank, 0.048, 0.040, mat=3, grp=f'leg{s_}')
        Rf = Rr @ rotX(-f.get('pitch', 0.0))
        def mf(q): return np.where(q[:, 1] < -0.0800, 5, 4)
        o = Rr @ ank
        pf = cone(o, Rf, (0, -0.0566, -0.030), (0, -0.0566, 0.095), 0.046, 0.040, mat=mf, grp=f'foot{s_}')
        pf.s = np.array([0.88, 0.66, 1.0]); prims.append(pf)
    Rtt = Rr @ Rt; o_t = pel
    if who == 'raimundo':
        def mt(q): return np.where((np.abs(q[:, 0]) > 0.048) & (np.abs(q[:, 0]) < 0.066) & (q[:, 2] > 0.0) & (q[:, 1] > 0.02), 6, np.where(q[:, 1] < 0.07, 3, 2))   # suspensórios
        prims.append(cone(Rr @ o_t, Rtt, (0, -0.02, 0), (0, 0.39, 0), 0.118, 0.128, scale=(1, 1, 0.84), mat=mt, grp='body'))
        prims.append(ell(Rr @ o_t, Rtt @ Rp, (0, -0.03, 0), (0.122, 0.092, 0.098), mat=3, grp='body'))
    elif who == 'lucia':
        def mt(q): return np.where(((q[:, 1] > 0.08) & (q[:, 1] < 0.105)) | ((q[:, 1] > 0.20) & (q[:, 1] < 0.225)), 5, np.where(q[:, 1] < 0.0, 3, 6))   # colete + faixas refletivas
        prims.append(cone(Rr @ o_t, Rtt, (0, -0.02, 0), (0, 0.39, 0), 0.114, 0.126, scale=(1, 1, 0.80), mat=mt, grp='body'))
        prims.append(ell(Rr @ o_t, Rtt @ Rp, (0, -0.03, 0), (0.118, 0.090, 0.094), mat=3, grp='body'))
    else:
        prims.append(cone(Rr @ o_t, Rtt, (0, -0.02, 0), (0, 0.39, 0), 0.118, 0.124, scale=(1, 1, 0.80), mat=2, grp='body'))
        def ms(q): return np.where((q[:, 1] < 0.215) & (q[:, 1] > 0.19), 5, 3)                       # barra da saia
        prims.append(cone(np.zeros(3), Rr, (0, S['pelvis_h'] + bob + 0.12, 0.0), (0, 0.285, 0.0), 0.136, 0.205, scale=(1, 1, 0.90), mat=ms, grp='body'))
    wc(neck - Rh @ np.array([0, 0.03, 0]), neck + Rh @ np.array([0, 0.09, 0.012]), 0.043, 0.039, mat=0, grp='head')
    rx, ry, rz = S['head_r']; Rhw = Rr @ Rh
    prims.append(ell(Rr @ head, Rhw, (0, 0, 0), (rx, ry, rz), mat=0, grp='head'))
    prims.append(ell(Rr @ head + Rhw @ np.array([0, -0.012, rz - 0.004]), Rhw, (0, 0, 0), (0.022, 0.025, 0.027), mat=0, grp='head'))
    for s_ in (+1, -1):
        prims.append(ell(Rr @ head + Rhw @ np.array([s_ * (rx - 0.004), -0.008, -0.012]), Rhw, (0, 0, 0), (0.020, 0.032, 0.026), mat=0, grp='head'))
    if who == 'raimundo':
        prims.append(ell(Rr @ head, Rhw, (0, 0.012, -0.030), (rx + 0.008, ry - 0.030, rz + 0.004), mat=1, grp='hair', cut=((0, -1, 0), 0.020)))        # cabelo grisalho curto
        prims.append(ell(Rr @ head, Rhw, (0, ry * 0.60, -0.012), (rx + 0.024, 0.050, rz + 0.022), mat=7, grp='hat'))                                        # boina
        prims.append(ell(Rr @ head, Rhw, (0, ry * 0.60 + 0.046, -0.012), (0.012, 0.010, 0.012), mat=7, grp='hat'))
        prims.append(ell(Rr @ head, Rhw, (0, ry * 0.44, rz * 0.78), (0.070, 0.016, 0.042), mat=7, grp='hat'))
    elif who == 'dandara':
        prims.append(ell(Rr @ head, Rhw, (0, 0.040, -0.034), (rx + 0.046, ry * 0.40, rz + 0.046), mat=6, grp='wrap'))                                         # turbante/faixa
        prims.append(ell(Rr @ head, Rhw, (0, 0.100, -0.034), (rx + 0.040, 0.078, rz + 0.044), mat=1, grp='hair', tex=lambda q, i, m: tex_curl(q, i, m, 0.05)))   # cabelo volumoso
        prims.append(ell(Rr @ head, Rhw, (0, 0.010, -0.040), (rx + 0.020, ry - 0.010, rz + 0.016), mat=1, grp='hair', cut=((0, -1, 0), 0.012), tex=lambda q, i, m: tex_curl(q, i, m, 0.05)))
        for s_ in (+1, -1): prims.append(ell(Rr @ head + Rhw @ np.array([s_ * (rx + 0.004), -0.058, -0.004]), Rhw, (0, 0, 0), (0.012, 0.020, 0.012), mat=6, grp='head'))
    else:
        prims.append(ell(Rr @ head, Rhw, (0, 0.016, -0.026), (rx + 0.010, ry - 0.008, rz + 0.010), mat=1, grp='hair', cut=((0, -1, 0), 0.006)))
        prims.append(ell(Rr @ head, Rhw, (0, ry * 0.55, -rz * 1.02), (0.055, 0.050, 0.055), mat=1, grp='hair'))                                              # coque baixo
    hands = {}
    for s_ in (+1, -1):
        a = p.get('arm_l' if s_ > 0 else 'arm_r', {}); shp = sh[s_]
        if 'tgt' in a: tgt = np.array(a['tgt'], float)
        else:
            sw, ab, ext = a.get('sw', 0.0), a.get('ab', 0.10), a.get('ext', 0.94)
            dirv = np.array([s_ * math.sin(ab), -math.cos(sw) * math.cos(ab), math.sin(sw) * math.cos(ab)])
            tgt = shp + (Rt @ dirv) * (S['arm1'] + S['arm2']) * ext
        pole = Rt @ np.array([s_ * 0.55, -0.9, -0.55])
        el, wr = ik2(shp, tgt, S['arm1'], S['arm2'], pole); hands[s_] = (shp, el, wr)
        sl = {'raimundo': 0.60, 'dandara': 0.72, 'lucia': 0.94}[who]
        wc(shp, el, 0.038, 0.033, mat=0, grp=f'arm{s_}')
        wc(shp, shp + (el - shp) * sl, 0.049, 0.045, mat=2, grp=f'arm{s_}')
        if who == 'lucia': wc(el, el + (wr - el) * 0.55, 0.040, 0.036, mat=2, grp=f'arm{s_}')
        wc(el, wr, 0.031, 0.027, mat=0, grp=f'arm{s_}')
        we(wr + (wr - el) / max(np.linalg.norm(wr - el), 1e-6) * 0.012, (0.034, 0.038, 0.034), mat=0, grp=f'arm{s_}')
    if who == 'dandara':        # caderno de capa dura junto ao quadril esquerdo
        prims.append(ell(Rr @ o_t, Rtt, (0.150, -0.050, 0.060), (0.020, 0.075, 0.056), mat=8, grp='book'))
    if who == 'lucia':          # trena no cinto e prancheta na mão esquerda
        prims.append(ell(Rr @ o_t, Rtt, (-0.120, -0.020, 0.040), (0.030, 0.030, 0.026), mat=7, grp='body'))
        shp, el, wr = hands[+1]
        def mb(q): return np.where(q[:, 2] > 0.006, 5, 8)
        prims.append(ell(Rr @ (wr + np.array([0.0, 0.05, 0.04])), Rr, (0, 0, 0), (0.080, 0.100, 0.010), mat=mb, grp='board'))
    info = dict(head=Rr @ head, Rhw=Rhw, rx=rx, ry=ry, rz=rz, who=who, feet=feet, hands=hands, pel=Rr @ pel)
    return prims, info

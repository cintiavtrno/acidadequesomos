"""Moradores da rua (Etapa 6): Seu Zé, Nonato, Dona Bela (dominó), Cícera, Júnior e Tonho (picolé).
Mesmo esqueleto/IK de Lia e Vó; construtor orientado por configuração (roupa, cabelo, chapéu, saia, adereço)."""
import math
import numpy as np
from render import *
import rig
from rig import R, ik2, tex_curl, tex_none

SK = lambda a, b, c, d: dict(ramp=R(a, b, c, d))
SHOE = ('#2a2018', '#3e3024', '#5a4634', '#7a6248'); SOLE = ('#8a8272', '#b0a894', '#d0c8b2', '#ece6d4'); DARK = ('#101010', '#242020', '#3a3434', '#524a4a')
def mats(skin, hair, top, pants, hat=None, acc=None, aux=None, shoe=SHOE):
    return {0: SK(*skin), 1: SK(*hair), 2: SK(*top), 3: SK(*pants), 4: SK(*shoe), 5: SK(*SOLE),
            6: SK(*(acc or top)), 7: SK(*(hat or hair)), 8: SK(*(aux or SOLE)), 9: SK(*DARK)}

rig.MATS.update({
 'ze':      mats(('#5a3a28', '#7c5238', '#a07050', '#c09470'), ('#8a8a88', '#b0b0ac', '#d2d2cc', '#eeeeea'), ('#6a8aa0', '#8aaac0', '#b0c8d8', '#d8e8f0'),
                 ('#3a3428', '#524a3a', '#6e6450', '#8c8068'), hat=('#8a6a2a', '#b08a3a', '#d4b058', '#ecd486'), acc=('#7a2a22', '#a43c30', '#c85c48', '#e08470')),
 'nonato':  mats(('#2c1810', '#442a1c', '#5e3c2a', '#7c5238'), ('#1c1210', '#2c1b14', '#43291e', '#5e3b2a'), ('#8a6a10', '#c4980e', '#e8c032', '#f6dc6a'),
                 ('#2a3c5e', '#3a5280', '#5470a4', '#7c98c8'), acc=('#1c4a2a', '#2a6a3c', '#3e8c52', '#62b076')),
 'bela':    mats(('#5a3826', '#7a4f36', '#9a6a4a', '#b88460'), ('#8a8a88', '#b4b4b0', '#d8d8d2', '#f2f2ee'), ('#7a2a46', '#a43e60', '#c85e80', '#e88ca4'),
                 ('#7a2a46', '#a43e60', '#c85e80', '#e88ca4'), acc=('#c8a040', '#e0bc54', '#f2d474', '#fae8a4'), aux=('#ece6d4', '#f6f2e4', '#fffcf0', '#ffffff')),
 'cicera':  mats(('#4a2c1e', '#6a4230', '#8a5a40', '#a87452'), ('#1c1210', '#2c1b14', '#43291e', '#5e3b2a'), ('#a8741c', '#d49a2c', '#f0be4c', '#fad884'),
                 ('#a8741c', '#d49a2c', '#f0be4c', '#fad884'), hat=('#2a6a6a', '#3a8a86', '#58aaa0', '#86cfc0'), acc=('#b9b09c', '#d6cfbf', '#ece7da', '#faf6ec')),
 'junior':  mats(('#4a2c1e', '#6a4230', '#8a5a40', '#a87452'), ('#100a08', '#1e1410', '#2e201a', '#42302a'), ('#8a2a22', '#b4382c', '#d85a46', '#ee8470'),
                 ('#24407a', '#3256a0', '#4a74c4', '#78a0e4'), acc=('#b9b09c', '#d6cfbf', '#ece7da', '#faf6ec'), shoe=('#2a4e8a', '#2f5fa8', '#4a7bc4', '#7aa2de')),
 'tonho':   mats(('#3a2216', '#58361f', '#7a4c30', '#9a6644'), ('#100a08', '#1e1410', '#2e201a', '#42302a'), ('#b9b09c', '#d6cfbf', '#ece7da', '#faf6ec'),
                 ('#4a5a3a', '#627850', '#809a6a', '#a0b888'), hat=('#2a4e8a', '#2f5fa8', '#4a7bc4', '#7aa2de'), acc=('#2a7ab0', '#3a96cc', '#5eb4e0', '#92d2f2'), aux=('#c8e4f0', '#e0f0f8', '#f4fafc', '#ffffff')),
})
_S = lambda **k: k
rig.SPEC.update({
 'ze':     _S(hip_w=0.074, pelvis_h=0.775, ankle_h=0.063, thigh=0.335, shin=0.335, sh_w=0.128, sh_y=0.385, neck_y=0.425, head_dy=0.170, head_r=(0.108, 0.136, 0.108), arm1=0.245, arm2=0.230, torso_len=0.40, stride=0.40),
 'nonato': _S(hip_w=0.092, pelvis_h=0.760, ankle_h=0.063, thigh=0.330, shin=0.330, sh_w=0.150, sh_y=0.380, neck_y=0.420, head_dy=0.168, head_r=(0.120, 0.140, 0.116), arm1=0.250, arm2=0.230, torso_len=0.38, stride=0.44),
 'bela':   _S(hip_w=0.088, pelvis_h=0.745, ankle_h=0.063, thigh=0.320, shin=0.320, sh_w=0.138, sh_y=0.372, neck_y=0.416, head_dy=0.172, head_r=(0.116, 0.140, 0.112), arm1=0.236, arm2=0.218, torso_len=0.37, stride=0.40),
 'cicera': _S(hip_w=0.086, pelvis_h=0.765, ankle_h=0.063, thigh=0.328, shin=0.328, sh_w=0.140, sh_y=0.376, neck_y=0.420, head_dy=0.172, head_r=(0.114, 0.140, 0.112), arm1=0.240, arm2=0.222, torso_len=0.38, stride=0.46),
 'junior': _S(hip_w=0.066, pelvis_h=0.580, ankle_h=0.063, thigh=0.240, shin=0.240, sh_w=0.112, sh_y=0.320, neck_y=0.364, head_dy=0.180, head_r=(0.122, 0.146, 0.118), arm1=0.180, arm2=0.168, torso_len=0.30, stride=0.50),
 'tonho':  _S(hip_w=0.082, pelvis_h=0.770, ankle_h=0.063, thigh=0.335, shin=0.335, sh_w=0.140, sh_y=0.382, neck_y=0.424, head_dy=0.170, head_r=(0.114, 0.140, 0.112), arm1=0.245, arm2=0.228, torso_len=0.39, stride=0.46),
})
NEW = ('ze', 'nonato', 'bela', 'cicera', 'junior', 'tonho')

# configuração visual: perna ('long' | 'bermuda'), saia (None | comprimento), mangas, barriga, cabelo, chapéu, adereço
CFG = {
 'ze':     dict(leg='long', sleeve=0.60, belly=0.0, hair='short', hat='palha', mustache=True),
 'nonato': dict(leg='bermuda', sleeve=0.55, belly=0.035, hair='bald', hat=None),
 'bela':   dict(leg='long', skirt=0.46, sleeve=0.62, belly=0.0, hair='curto_cacheado', hat=None, glasses=True),
 'cicera': dict(leg='long', skirt=0.40, sleeve=0.55, belly=0.0, hair='lenco', hat='lenco', apron=True),
 'junior': dict(leg='bermuda', sleeve=0.50, belly=0.0, hair='short', hat=None),
 'tonho':  dict(leg='bermuda', sleeve=0.58, belly=0.0, hair='short', hat='bone', box=True),
}

# ---- Etapa 8.6c: elenco do quintal (3/4) --------------------------------------------------------------------------------------------------------
def _rgb2hex(c): return '#%02x%02x%02x' % tuple(c)
def _ramp4(rows): return tuple(_rgb2hex(c) for c in reversed(rows))          # KIDS usa claro→escuro; as paletas daqui vão do escuro ao claro
SK_ = lambda *a: a
_SKINS = [('#4a2c1e', '#6a4230', '#8a5a40', '#a87452'), ('#5a3826', '#7a4f36', '#9a6a4a', '#b88460'), ('#2c1810', '#442a1c', '#5e3c2a', '#7c5238'),
          ('#3a2216', '#58361f', '#7a4c30', '#9a6644'), ('#6a4230', '#8a5a40', '#a87452', '#c48e68'), ('#4a2c1e', '#6a4230', '#8a5a40', '#a87452')]
_BLACK = ('#100a08', '#1e1410', '#2e201a', '#42302a'); _GRAY = ('#8a8a88', '#b4b4b0', '#d8d8d2', '#f2f2ee'); _CREAM = ('#b9b09c', '#d6cfbf', '#ece7da', '#faf6ec')
_KS = [(((246, 214, 120), (226, 178, 70), (186, 136, 44), (140, 98, 34)), ((96, 120, 90), (70, 92, 70), (48, 66, 52), (36, 50, 40))),
       (((150, 200, 150), (104, 160, 108), (70, 120, 80), (48, 88, 60)), ((170, 120, 80), (130, 88, 58), (92, 62, 42), (66, 44, 32))),
       (((240, 232, 214), (214, 204, 184), (176, 166, 148), (132, 124, 112)), ((74, 116, 196), (50, 86, 160), (36, 64, 122), (26, 46, 92))),
       (((240, 170, 110), (222, 128, 70), (184, 92, 48), (140, 66, 40)), ((96, 96, 112), (70, 70, 86), (50, 50, 64), (36, 36, 48))),
       (((190, 150, 210), (150, 108, 178), (112, 74, 142), (80, 52, 108)), ((200, 190, 160), (168, 156, 126), (130, 120, 96), (96, 88, 70))),
       (((120, 196, 200), (76, 152, 162), (50, 112, 126), (36, 82, 96)), ((150, 70, 64), (116, 50, 48), (84, 36, 38), (60, 26, 28)))]
_KH = ['short', 'bald', 'curto_cacheado', 'short', 'bald', 'curto_cacheado']; _KSC = [0.92, 1.0, 0.88, 0.96, 1.03, 0.90]
rig.MATS.update({
 'zefa': mats(_SKINS[0], _GRAY, ('#1f5a5a', '#2d7a78', '#4a9a94', '#7cc4b8'), ('#1f5a5a', '#2d7a78', '#4a9a94', '#7cc4b8'), hat=('#24407a', '#3256a0', '#4a74c4', '#78a0e4'), acc=_CREAM),
 'nena': mats(_SKINS[3], _GRAY, _CREAM, _CREAM, hat=_CREAM, acc=('#8a6a1e', '#c49a2a', '#ecc85a', '#f6e08a')),
 'davi': mats(_SKINS[0], _BLACK, ('#3a4a2a', '#52663a', '#74905a', '#9ab87e'), ('#1e2e4e', '#2c4474', '#42609a', '#6a88c0'), hat=('#1c1c22', '#2c2c34', '#44444e', '#62626e')),
 'rita': mats(_SKINS[1], _GRAY, ('#5a3a6a', '#7a5290', '#9c74b4', '#c2a0d4'), ('#3a3446', '#524a62', '#706684', '#948aa8'), acc=('#c8a040', '#e0bc54', '#f2d474', '#fae8a4')),
 'caio': mats(_SKINS[2], _BLACK, _CREAM, ('#6a5a3a', '#8a7a52', '#aa9a6c', '#cabc8c')),
 'bia':  mats(_SKINS[4], _BLACK, ('#8a2a5a', '#b43c78', '#d85e9a', '#ee8cba'), ('#2a3c5e', '#3a5280', '#5470a4', '#7c98c8'), acc=('#c8a040', '#e0bc54', '#f2d474', '#fae8a4')),
})
rig.SPEC.update({
 'zefa': _S(hip_w=0.086, pelvis_h=0.755, ankle_h=0.063, thigh=0.325, shin=0.325, sh_w=0.140, sh_y=0.375, neck_y=0.418, head_dy=0.172, head_r=(0.115, 0.140, 0.112), arm1=0.238, arm2=0.220, torso_len=0.38, stride=0.42),
 'nena': _S(hip_w=0.088, pelvis_h=0.750, ankle_h=0.063, thigh=0.322, shin=0.322, sh_w=0.140, sh_y=0.372, neck_y=0.416, head_dy=0.172, head_r=(0.116, 0.140, 0.112), arm1=0.236, arm2=0.218, torso_len=0.37, stride=0.38),
 'davi': _S(hip_w=0.082, pelvis_h=0.775, ankle_h=0.063, thigh=0.335, shin=0.335, sh_w=0.138, sh_y=0.385, neck_y=0.425, head_dy=0.170, head_r=(0.113, 0.140, 0.111), arm1=0.246, arm2=0.230, torso_len=0.40, stride=0.46),
 'rita': _S(hip_w=0.084, pelvis_h=0.755, ankle_h=0.063, thigh=0.325, shin=0.325, sh_w=0.136, sh_y=0.374, neck_y=0.418, head_dy=0.172, head_r=(0.114, 0.140, 0.111), arm1=0.238, arm2=0.220, torso_len=0.38, stride=0.40),
 'caio': _S(hip_w=0.078, pelvis_h=0.740, ankle_h=0.063, thigh=0.320, shin=0.320, sh_w=0.130, sh_y=0.372, neck_y=0.414, head_dy=0.172, head_r=(0.116, 0.142, 0.114), arm1=0.236, arm2=0.218, torso_len=0.37, stride=0.46),
 'bia':  _S(hip_w=0.076, pelvis_h=0.735, ankle_h=0.063, thigh=0.316, shin=0.316, sh_w=0.124, sh_y=0.368, neck_y=0.410, head_dy=0.174, head_r=(0.117, 0.143, 0.115), arm1=0.232, arm2=0.214, torso_len=0.36, stride=0.46),
})
rig.CFG_NEW = {
 'zefa': dict(leg='long', skirt=0.46, sleeve=0.55, belly=0.0, hair='curto_cacheado', hat='lenco', apron=True),
 'nena': dict(leg='long', skirt=0.52, sleeve=0.60, belly=0.0, hair='short', hat='lenco'),
 'davi': dict(leg='long', sleeve=0.50, belly=0.0, hair='curto_cacheado', hat='bone'),
 'rita': dict(leg='long', skirt=0.44, sleeve=0.60, belly=0.0, hair='curto_cacheado', hat=None, glasses=True),
 'caio': dict(leg='bermuda', sleeve=0.50, belly=0.0, hair='short', hat=None),
 'bia':  dict(leg='long', skirt=0.34, sleeve=0.48, belly=0.0, hair='curto_cacheado', hat=None),
}
for i in range(6):
    sh, pa = _KS[i]
    rig.MATS['m%d' % (i + 1)] = mats(_SKINS[i], _BLACK, _ramp4(sh), _ramp4(pa), shoe=('#2a2018', '#3e3024', '#5a4634', '#7a6248'))
    rig.SPEC['m%d' % (i + 1)] = dict(rig.SPEC['junior'], pelvis_h=0.57 + 0.008 * (i % 3), head_r=(0.120 + 0.002 * i, 0.146, 0.118))
    rig.CFG_NEW['m%d' % (i + 1)] = dict(leg='bermuda', sleeve=0.50, belly=0.0, hair=_KH[i], hat=None)
NEW2 = tuple(rig.CFG_NEW)
CFG.update(rig.CFG_NEW)

def build_npc2(who, pose, D):
    S = rig.SPEC[who]; C_ = CFG[who]; p = dict(pose)
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
    skirt = C_.get('skirt'); bermuda = C_['leg'] == 'bermuda'
    for s_ in (+1, -1):
        f = p.get('foot_l' if s_ > 0 else 'foot_r', {})
        hip = pel + Rp @ np.array([s_ * S['hip_w'], -0.025, 0.0])
        ank = np.array([s_ * S['hip_w'] + f.get('x', 0.0), S['ankle_h'] + f.get('y', 0.0), f.get('z', 0.0)])
        knee, ank = ik2(hip, ank, S['thigh'], S['shin'], np.array([0.12 * s_, 0.0, 1.0]))
        if skirt or bermuda:
            wc(hip, knee, 0.060, 0.050, mat=3 if bermuda else 0, grp=f'leg{s_}'); wc(knee, ank, 0.042, 0.032, mat=0, grp=f'leg{s_}')
        else:
            wc(hip, knee, 0.060, 0.050, mat=3, grp=f'leg{s_}'); wc(knee, ank, 0.048, 0.040, mat=3, grp=f'leg{s_}')
        Rf = Rr @ rotX(-f.get('pitch', 0.0)); o = Rr @ ank
        def mf(q): return np.where(q[:, 1] < -0.0800, 5, 4)
        pf = cone(o, Rf, (0, -0.0566, -0.030), (0, -0.0566, 0.095), 0.046, 0.040, mat=mf, grp=f'foot{s_}')
        pf.s = np.array([0.88, 0.66, 1.0]); prims.append(pf)
    Rtt = Rr @ Rt; o_t = pel; bl = C_.get('belly', 0.0)
    if C_.get('apron'):
        def mt(q): return np.where((q[:, 2] > 0.02) & (q[:, 1] > 0.02) & (q[:, 1] < 0.30), 6, 2)
    else:
        def mt(q): return np.where(q[:, 1] < 0.0, 3, 2) if not bermuda else 2
    prims.append(cone(Rr @ o_t, Rtt, (0, -0.02, 0), (0, 0.39, 0), 0.118 + bl, 0.126, scale=(1, 1, 0.82 + bl * 3), mat=mt, grp='body'))
    if not skirt:
        prims.append(ell(Rr @ o_t, Rtt @ Rp, (0, -0.03, 0), (0.122 + bl, 0.092, 0.098 + bl * 1.5), mat=3, grp='body'))
    else:
        L = skirt
        def ms(q): return np.where((q[:, 1] < 0.215 - (0.0 if L > 0.43 else 0.0)) & (q[:, 1] > 0.19), 7 if who == 'bela' else 6, 3)
        prims.append(cone(np.zeros(3), Rr, (0, S['pelvis_h'] + bob + 0.12, 0.0), (0, S['pelvis_h'] + bob + 0.12 - L * 0.62, 0.0), 0.130, 0.166, scale=(1, 1, 0.90), mat=ms, grp='body'))
    wc(neck - Rh @ np.array([0, 0.03, 0]), neck + Rh @ np.array([0, 0.09, 0.012]), 0.043, 0.039, mat=0, grp='head')
    rx, ry, rz = S['head_r']; Rhw = Rr @ Rh
    prims.append(ell(Rr @ head, Rhw, (0, 0, 0), (rx, ry, rz), mat=0, grp='head'))
    prims.append(ell(Rr @ head + Rhw @ np.array([0, -0.012, rz - 0.004]), Rhw, (0, 0, 0), (0.022, 0.025, 0.027), mat=0, grp='head'))
    for s_ in (+1, -1):
        prims.append(ell(Rr @ head + Rhw @ np.array([s_ * (rx - 0.004), -0.008, -0.012]), Rhw, (0, 0, 0), (0.020, 0.032, 0.026), mat=0, grp='head'))
    h = C_['hair']
    if h == 'short':
        prims.append(ell(Rr @ head, Rhw, (0, 0.014, -0.030), (rx + 0.008, ry - 0.028, rz + 0.004), mat=1, grp='hair', cut=((0, -1, 0), 0.020)))
    elif h == 'bald':      # coroa rala dos lados e atrás
        prims.append(ell(Rr @ head, Rhw, (0, -0.010, -0.040), (rx + 0.006, ry - 0.060, rz - 0.020), mat=1, grp='hair', cut=((0, -1, 0), 0.010)))
        prims.append(ell(Rr @ head, Rhw, (0, 0.050, -0.010), (rx - 0.004, 0.020, rz * 0.7), mat=0, grp='head'))
    elif h == 'curto_cacheado':
        prims.append(ell(Rr @ head, Rhw, (0, 0.022, -0.026), (rx + 0.016, ry - 0.002, rz + 0.012), mat=1, grp='hair', cut=((0, -1, 0), 0.005), tex=lambda q, i, m: tex_curl(q, i, m, 0.05)))
    elif h == 'lenco':
        prims.append(ell(Rr @ head, Rhw, (0, 0.012, -0.030), (rx + 0.010, ry - 0.020, rz + 0.006), mat=1, grp='hair', cut=((0, -1, 0), 0.016)))
    hat = C_.get('hat')
    if hat == 'palha':
        prims.append(ell(Rr @ head, Rhw, (0, ry * 0.52, -0.004), (rx + 0.030, 0.050, rz + 0.030), mat=7, grp='hat'))
        prims.append(ell(Rr @ head, Rhw, (0, ry * 0.52 - 0.012, 0.000), (rx + 0.100, 0.014, rz + 0.095), mat=7, grp='hat'))
    elif hat == 'bone':
        prims.append(ell(Rr @ head, Rhw, (0, ry * 0.58, -0.010), (rx + 0.016, 0.052, rz + 0.016), mat=7, grp='hat'))
        prims.append(ell(Rr @ head, Rhw, (0, ry * 0.40, rz * 0.82), (0.066, 0.014, 0.050), mat=7, grp='hat'))
    elif hat == 'lenco':
        prims.append(ell(Rr @ head, Rhw, (0, ry * 0.50, -0.020), (rx + 0.024, 0.046, rz + 0.022), mat=7, grp='hat'))
        prims.append(ell(Rr @ head, Rhw, (0, ry * 0.70, -rz * 0.9), (0.044, 0.040, 0.044), mat=7, grp='hat'))
    if C_.get('mustache'):
        prims.append(ell(Rr @ head, Rhw, (0, -0.040, rz - 0.016), (0.040, 0.010, 0.016), mat=1, grp='head'))
    if C_.get('glasses'):
        prims.append(ell(Rr @ head, Rhw, (0, 0.012, rz - 0.006), (rx - 0.006, 0.014, 0.012), mat=9, grp='head'))
    hands = {}
    sl = C_['sleeve']
    for s_ in (+1, -1):
        a = p.get('arm_l' if s_ > 0 else 'arm_r', {}); shp = sh[s_]
        if 'tgt' in a: tgt = np.array(a['tgt'], float)
        else:
            sw, ab, ext = a.get('sw', 0.0), a.get('ab', 0.10), a.get('ext', 0.94)
            dirv = np.array([s_ * math.sin(ab), -math.cos(sw) * math.cos(ab), math.sin(sw) * math.cos(ab)])
            tgt = shp + (Rt @ dirv) * (S['arm1'] + S['arm2']) * ext
        pole = Rt @ np.array([s_ * 0.55, -0.9, -0.55])
        el, wr = ik2(shp, tgt, S['arm1'], S['arm2'], pole); hands[s_] = (shp, el, wr)
        wc(shp, el, 0.038, 0.033, mat=0, grp=f'arm{s_}')
        wc(shp, shp + (el - shp) * sl, 0.049, 0.045, mat=2, grp=f'arm{s_}')
        wc(el, wr, 0.031, 0.027, mat=0, grp=f'arm{s_}')
        we(wr + (wr - el) / max(np.linalg.norm(wr - el), 1e-6) * 0.012, (0.034, 0.038, 0.034), mat=0, grp=f'arm{s_}')
    if C_.get('box'):       # caixa de isopor pendurada na frente (alça no ombro)
        def mb(q): return np.where(q[:, 1] > 0.045, 8, 6)
        prims.append(ell(Rr @ o_t, Rtt, (0.0, -0.030, 0.235), (0.170, 0.100, 0.120), mat=mb, grp='board'))
    info = dict(head=Rr @ head, Rhw=Rhw, rx=rx, ry=ry, rz=rz, who=who, feet={}, hands=hands, pel=Rr @ pel)
    return prims, info

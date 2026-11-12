"""Clipes de animação. pose_for(who, anim, k, yaw) -> dict de pose.  Passada ligada à velocidade do jogo (sem patinar)."""
import math

# jeito de andar de cada uma (m, s)
GAIT = {
 'raimundo': dict(T=1.10, step=0.36, lift=0.045, bob=0.010, arm=0.18, lean=0.14, sway=0.012, head=0.02, hand_out=0.10),
 'dandara':  dict(T=0.84, step=0.46, lift=0.060, bob=0.014, arm=0.40, lean=0.06, sway=0.010, head=0.03, hand_out=0.11),
 'lucia':    dict(T=0.80, step=0.48, lift=0.065, bob=0.014, arm=0.42, lean=0.05, sway=0.010, head=0.03, hand_out=0.11),
 'ze': dict(T=1.20, step=0.34, lift=0.040, bob=0.009, arm=0.16, lean=0.16, sway=0.012, head=0.02, hand_out=0.10),
 'nonato': dict(T=1.00, step=0.40, lift=0.050, bob=0.012, arm=0.26, lean=0.08, sway=0.016, head=0.02, hand_out=0.12),
 'bela': dict(T=1.04, step=0.36, lift=0.045, bob=0.010, arm=0.20, lean=0.10, sway=0.010, head=0.02, hand_out=0.10),
 'cicera': dict(T=0.88, step=0.44, lift=0.058, bob=0.013, arm=0.34, lean=0.06, sway=0.010, head=0.03, hand_out=0.11),
 'junior': dict(T=0.56, step=0.52, lift=0.090, bob=0.022, arm=0.70, lean=0.10, sway=0.014, head=0.03, hand_out=0.12),
 'tonho': dict(T=0.94, step=0.44, lift=0.055, bob=0.012, arm=0.12, lean=0.05, sway=0.010, head=0.02, hand_out=0.10),
 'lia':   dict(T=0.70, step=0.50, lift=0.085, bob=0.020, arm=0.62, lean=0.085, sway=0.014, head=0.03, hand_out=0.12),
 'aurea': dict(T=0.96, step=0.40, lift=0.050, bob=0.011, arm=0.20, lean=0.130, sway=0.010, head=0.02, hand_out=0.10),
}
GAIT.update({
 'zefa': dict(T=0.92, step=0.40, lift=0.050, bob=0.011, arm=0.22, lean=0.08, sway=0.010, head=0.02, hand_out=0.10),
 'nena': dict(T=1.00, step=0.36, lift=0.045, bob=0.010, arm=0.20, lean=0.08, sway=0.010, head=0.02, hand_out=0.10),
 'davi': dict(T=0.90, step=0.44, lift=0.055, bob=0.012, arm=0.30, lean=0.06, sway=0.012, head=0.02, hand_out=0.11),
 'rita': dict(T=0.98, step=0.38, lift=0.048, bob=0.010, arm=0.20, lean=0.09, sway=0.010, head=0.02, hand_out=0.10),
 'caio': dict(T=0.76, step=0.46, lift=0.065, bob=0.014, arm=0.40, lean=0.06, sway=0.012, head=0.03, hand_out=0.11),
 'bia':  dict(T=0.76, step=0.44, lift=0.062, bob=0.014, arm=0.40, lean=0.05, sway=0.010, head=0.03, hand_out=0.11),
})
for _i in range(6): GAIT['m%d' % (_i + 1)] = dict(GAIT['junior'], T=0.54 + 0.02 * (_i % 3), step=0.50)

def speed(who):                       # m/s para os pés não escorregarem: (2 passos por ciclo)
    g = GAIT[who]; return 2 * g['step'] / g['T']

ANIMS = {   # nome: (frames, fps, loop)
 'idle': (4, 2.0, True), 'walk': (8, None, True), 'turn': (2, 6.0, False), 'talk': (4, 6.0, True),
 'interact': (4, 7.0, False), 'interact_high': (4, 7.0, False),
 'sit': (4, 2.0, True), 'play': (4, 5.0, False), 'think': (4, 2.5, True), 'react': (4, 6.0, True), 'hang': (4, 4.0, True), 'wave': (4, 6.0, True), 'serve_idle': (4, 2.0, True), 'serve_wrap': (4, 5.0, True), 'serve_give': (4, 6.0, False),
 'serve_write': (4, 5.0, True), 'serve_greet': (4, 6.0, False),
}

def _foot(ph, g):
    ph %= 1.0; S = g['step']
    if ph < 0.5:                              # apoio: o pé anda para trás junto com o chão
        u = ph / 0.5; z = S / 2 - S * u; y = 0.0; pitch = 0.20 * (1 - u) - 0.42 * max(0, u - 0.62) / 0.38
    else:                                     # balanço: pé sobe e vai à frente
        u = (ph - 0.5) / 0.5; z = -S / 2 + S * u; y = g['lift'] * math.sin(math.pi * u) ** 0.8
        pitch = -0.42 + 0.62 * min(1, u * 1.25)
    y += 0.095 * max(0.0, -math.sin(pitch)) * (1.0 if ph < 0.5 else 0.5)      # toe-off: calcanhar sobe pivotando na ponta
    return dict(z=z, y=y, pitch=pitch)

def walk_pose(who, k, n=8):
    g = GAIT[who]; ph = k / float(n); a = 2 * math.pi * ph
    p = dict(bob=-g['bob'] * math.cos(2 * a) * 0.5 - g['bob'] * 0.5, sway=g['sway'] * math.sin(a), lean=g['lean'], proll=0.04 * math.sin(a) * (1 if who == 'lia' else 0.5),
             troll=-0.03 * math.sin(a), twist=0.10 * math.cos(a) * (1 if who == 'lia' else 0.4), ptwist=-0.08 * math.cos(a) * (1 if who == 'lia' else 0.4),
             hpitch=-g['lean'] * 0.6 + g['head'] * math.sin(2 * a), foot_l=_foot(ph, g), foot_r=_foot(ph + 0.5, g))
    if who == 'lia':
        p['arm_l'] = dict(sw=-g['arm'] * math.cos(a), ab=g['hand_out'], ext=0.90 + 0.06 * math.cos(a))
        p['arm_r'] = dict(sw=+g['arm'] * math.cos(a), ab=g['hand_out'], ext=0.90 - 0.06 * math.cos(a))
    else:                                                # Vó: braços perto do corpo, mãos junto ao avental
        p['arm_l'] = dict(sw=-g['arm'] * math.cos(a) + 0.22, ab=0.10, ext=0.78)
        p['arm_r'] = dict(sw=+g['arm'] * math.cos(a) + 0.22, ab=0.10, ext=0.78)
    return p

def _rest_arms(who, k=0):
    if who == 'lia': return dict(arm_l=dict(sw=0.02, ab=0.12, ext=0.93), arm_r=dict(sw=0.02, ab=0.12, ext=0.93))
    return dict(arm_l=dict(tgt=(0.17, 0.80, 0.10)), arm_r=dict(tgt=(-0.17, 0.80, 0.10)))

def idle_pose(who, k):
    br = (0.0, -0.014, -0.020, -0.008)[k]
    p = dict(bob=br, sway=(0, 0.004, 0.0, -0.006)[k] if who == 'lia' else 0.0, hpitch=(0, 0.02, 0.0, -0.015)[k],
             lean=0.02 if who == 'aurea' else 0.0, eyes=0 if k == 3 else 1)
    p.update(_rest_arms(who))
    if who == 'lia':
        p['arm_r'] = dict(sw=0.02 + (0.05, 0.0, -0.04, 0.0)[k], ab=0.12, ext=0.93)
        p['arm_l'] = dict(sw=0.02 - (0.05, 0.0, -0.04, 0.0)[k], ab=0.12, ext=0.93)
        p['foot_r'] = dict(x=-0.01, z=0.015 if k == 2 else 0.0)
    else:
        p['arm_l'] = dict(tgt=(0.17, 0.80 + (0, 0.008, 0, -0.005)[k], 0.10)); p['arm_r'] = dict(tgt=(-0.17, 0.80 + (0, 0.008, 0, -0.005)[k], 0.10))
    return p

def turn_pose(who, k):
    sgn = (+1, -1)[k]
    p = idle_pose(who, 0)
    p.update(hyaw=0.78 * sgn, twist=0.24 * sgn, ptwist=0.10 * sgn, hpitch=0.03, lean=0.03)
    return p

def talk_pose(who, k):
    mouth = (2, 1, 2, 0)[k] if who == 'lia' else (1, 2, 1, 0)[k]
    p = idle_pose(who, (0, 1, 0, 2)[k]); p['eyes'] = 1; p['mouth'] = mouth
    p['hpitch'] = (0.0, 0.05, 0.0, 0.04)[k]; p['hroll'] = (0.0, 0.05, 0.0, -0.05)[k]
    if who == 'lia':
        p['arm_r'] = dict(sw=(0.7, 1.0, 0.8, 0.5)[k], ab=0.30, ext=(0.80, 0.78, 0.82, 0.86)[k])
    else:
        p['arm_r'] = dict(tgt=(-0.20, (0.98, 1.04, 0.98, 0.90)[k], (0.20, 0.25, 0.22, 0.14)[k]))
    return p

def interact_pose(who, k, high=False):
    t = (0.35, 0.85, 1.0, 0.45)[k]
    p = idle_pose(who, 0)
    p.update(lean=0.06 + 0.10 * t, hpitch=0.10 * t if not high else -0.12 * t)
    y = 0.95 + (0.30 if high else 0.0) * t * 1.0
    if who == 'aurea': y += 0.12
    fz = 0.18 + 0.32 * t
    p['arm_r'] = dict(tgt=(-0.12, 0.80 + (y - 0.80) * t, fz))
    if k == 2: p['bob'] = -0.02
    return p

def serve_pose(who, anim, k):
    p = dict(bob=0.0, lean=0.05, eyes=1, mouth=0, hpitch=0.0)
    y = 1.00                                                         # tampo do balcão
    if anim == 'serve_idle':
        p['bob'] = (0, -0.01, -0.015, -0.006)[k]; p['eyes'] = 0 if k == 3 else 1
        p['arm_l'] = dict(tgt=(0.15, y, 0.30)); p['arm_r'] = dict(tgt=(-0.15, y, 0.30)); p['hpitch'] = (0.05, 0.07, 0.05, 0.08)[k]
    elif anim == 'serve_wrap':
        a = k / 4.0 * 2 * math.pi
        p['arm_l'] = dict(tgt=(0.08 + 0.04 * math.sin(a), y - 0.01, 0.24 + 0.03 * math.cos(a)))
        p['arm_r'] = dict(tgt=(-0.08 - 0.04 * math.sin(a), y + 0.015 * math.cos(a), 0.25 - 0.03 * math.cos(a)))
        p['hpitch'] = 0.30; p['lean'] = 0.09
    elif anim == 'serve_give':
        t = (0.2, 0.8, 1.0, 0.45)[k]
        p['arm_l'] = dict(tgt=(0.15, y, 0.28))
        p['arm_r'] = dict(tgt=(-0.12 + 0.04 * t, y + 0.06 * t, 0.28 + 0.30 * t)); p['lean'] = 0.07 + 0.08 * t
        p['mouth'] = 1 if k in (1, 2) else 0; p['hpitch'] = 0.04
    elif anim == 'serve_write':
        p['hpitch'] = 0.50; p['lean'] = 0.12
        p['arm_l'] = dict(tgt=(0.13, y, 0.24)); p['arm_r'] = dict(tgt=(-0.10 + 0.025 * (0, 1, 0, -1)[k], y, 0.25 + 0.02 * (1, 0, -1, 0)[k]))
    elif anim == 'serve_greet':
        up = (0.3, 1.0, 0.8, 0.5)[k]
        p['arm_l'] = dict(tgt=(0.15, y, 0.28))
        p['arm_r'] = dict(tgt=(-0.21 - 0.04 * math.sin(k * 1.6), y + 0.38 * up, 0.16))
        p['hpitch'] = -0.05; p['mouth'] = (1, 2, 1, 1)[k]; p['hroll'] = 0.05; p['lean'] = 0.03
    return p

def sit_pose(who, k):
    from rig import SPEC
    S = SPEC[who]; p = idle_pose(who, k)
    p['bob'] = (0.0, -0.006, -0.010, -0.004)[k] - (S['pelvis_h'] - 0.50)
    p['lean'] = 0.03; p['hpitch'] = (0.0, 0.02, 0.0, -0.02)[k]
    zf = S['thigh'] * 0.96
    p['foot_l'] = dict(x=0.02, z=zf, y=0.0, pitch=0.05); p['foot_r'] = dict(x=0.02, z=zf, y=0.0, pitch=0.05)
    if who == 'lia': p['arm_l'] = dict(tgt=(0.14, 0.50 + 0.02, 0.17)); p['arm_r'] = dict(tgt=(-0.14, 0.50 + 0.02, 0.17))
    else: p['arm_l'] = dict(tgt=(0.15, 0.56, 0.20)); p['arm_r'] = dict(tgt=(-0.15, 0.56, 0.20))
    return p


def _seated(who, k):
    p = sit_pose(who, 0); p['bob'] = p['bob']; return p

def play_pose(who, k):          # sentado: pega a pedra, estende o braço, bate na mesa, recolhe
    p = sit_pose(who, 0); t = (0.0, 0.7, 1.0, 0.35)[k]
    p['lean'] = 0.08 + 0.10 * t; p['hpitch'] = 0.18 + 0.10 * t
    p['arm_l'] = dict(tgt=(0.15, 0.76, 0.22))
    p['arm_r'] = dict(tgt=(-0.06 - 0.04 * t, 0.62 + 0.20 * t - (0.05 if k == 2 else 0.0), 0.16 + 0.30 * t))
    if k == 2: p['bob'] -= 0.012
    return p

def think_pose(who, k):         # sentado, mão no queixo, olhar para as próprias pedras
    p = sit_pose(who, k); p['lean'] = 0.05; p['hpitch'] = (0.22, 0.26, 0.22, 0.18)[k]; p['hroll'] = (0.0, 0.04, 0.0, -0.03)[k]
    p['arm_r'] = dict(tgt=(-0.04, 1.00 + 0.01 * (0, 1, 0, 0)[k] + 0.0, 0.14)); p['arm_l'] = dict(tgt=(0.15, 0.76, 0.24))
    p['eyes'] = 0 if k == 3 else 1
    return p

def react_pose(who, k):         # comemora/protesta: braço sobe, boca aberta, cabeça para trás
    p = sit_pose(who, k); up = (0.4, 1.0, 0.8, 1.0)[k]
    p['lean'] = -0.04; p['hpitch'] = -0.12 * up; p['mouth'] = (2, 1, 2, 1)[k]; p['hroll'] = (0.04, -0.04, 0.04, -0.04)[k]
    p['arm_r'] = dict(tgt=(-0.20 - 0.03 * (k % 2), 0.75 + 0.55 * up, 0.12 + 0.10 * up)); p['arm_l'] = dict(tgt=(0.15, 0.76, 0.24))
    return p

def hang_pose(who, k):          # em pé, mãos no alto (varal / janela / grade)
    p = idle_pose(who, 0); a = (0.0, 0.5, 1.0, 0.5)[k]
    p['hpitch'] = -0.14; p['lean'] = 0.0
    p['arm_l'] = dict(tgt=(0.14, 1.52 + 0.04 * a, 0.20)); p['arm_r'] = dict(tgt=(-0.14, 1.46 + 0.06 * (1 - a), 0.20))
    return p

def wave_pose(who, k):          # aceno
    p = idle_pose(who, 0); up = (0.6, 1.0, 0.6, 1.0)[k]
    p['mouth'] = 1 if k % 2 else 0; p['hroll'] = 0.05
    p['arm_r'] = dict(tgt=(-0.22 - 0.05 * (k % 2), 1.20 + 0.18 * up, 0.14))
    return p

def pose_for(who, anim, k, yaw):
    if anim == 'idle': p = idle_pose(who, k)
    elif anim == 'walk': p = walk_pose(who, k)
    elif anim == 'turn': p = turn_pose(who, k)
    elif anim == 'talk': p = talk_pose(who, k)
    elif anim == 'interact': p = interact_pose(who, k)
    elif anim == 'interact_high': p = interact_pose(who, k, True)
    elif anim == 'sit': p = sit_pose(who, k)
    elif anim == 'play': p = play_pose(who, k)
    elif anim == 'think': p = think_pose(who, k)
    elif anim == 'react': p = react_pose(who, k)
    elif anim == 'hang': p = hang_pose(who, k)
    elif anim == 'wave': p = wave_pose(who, k)
    elif anim.startswith('serve'): p = serve_pose(who, anim, k)
    else: raise KeyError(anim)
    p['yaw'] = yaw
    return p

"""Folhas de perfil (side-view) para o elenco da rua — Etapa 6."""
import json, math, os, sys
from multiprocessing import Pool
from PIL import Image
import rig_npc, rig_npc2
from pipeline import frame, CW, CH, SCALE
from anim import ANIMS, pose_for, GAIT, speed
OUT = '/home/claude/balcao/assets/chars'
D4 = {'down': 0, 'right': 90, 'up': 180, 'left': 270}
LR = {'right': 90, 'left': 270}
PAD = 2
def plan():
    rows = []
    for a in ('idle', 'walk', 'turn', 'talk', 'interact'):
        for dn, y in D4.items(): rows.append((a, dn, y))
    for a in ('sit', 'play', 'think', 'react'):
        for dn, y in D4.items(): rows.append((a, dn, y))
    for a in ('hang', 'wave'):
        for dn in ('down', 'up', 'right', 'left'): rows.append((a, dn, D4[dn]))
    return rows
def build(who):
    rows = plan(); cols = 8
    W = cols * (CW + PAD) + PAD; H = len(rows) * (CH + PAD) + PAD
    sh = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    atlas = dict(cell=[CW, CH], anchor=[20, 46], pad=PAD, cols=cols, persp='side', rows={}, speed_mps=speed(who) * SCALE[who], scale=SCALE[who], gait=GAIT[who])
    for r, (a, dn, y) in enumerate(rows):
        n = ANIMS[a][0]
        for k in range(n):
            im = frame(who, pose_for(who, a, k, math.radians(y)), 0)
            sh.alpha_composite(im, (PAD + k * (CW + PAD), PAD + r * (CH + PAD)))
        fps = ANIMS[a][1] or (8 / GAIT[who]['T'])
        atlas['rows'][f'{a}/{dn}'] = dict(row=r, n=n, fps=fps, loop=ANIMS[a][2])
    nm = 'lia_side6' if who == 'lia' else f'{who}_side'
    sh.save(f'{OUT}/{nm}.png'); json.dump(atlas, open(f'{OUT}/{nm}.json', 'w'), indent=1)
    return who, sh.size
if __name__ == '__main__':
    whos = sys.argv[1].split(',') if len(sys.argv) > 1 else ['raimundo', 'dandara', 'lucia', 'ze', 'nonato', 'bela', 'cicera', 'junior', 'tonho']
    with Pool(min(len(whos), os.cpu_count() or 2)) as p:
        for r in p.imap_unordered(build, whos): print(r, flush=True)

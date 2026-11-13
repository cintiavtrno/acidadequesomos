"""Folhas de perfil reduzidas para figurantes (moradores do quintal reaproveitados como público e moradores de 1996)."""
import json, math, os, sys
from multiprocessing import Pool
from PIL import Image
import build_side as BS
from pipeline import frame, CW, CH, SCALE
from anim import ANIMS, pose_for, GAIT, speed
OUT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'assets', 'chars'))
PAD = 2; D4 = BS.D4
PLAN = ['idle', 'walk', 'talk', 'wave', 'react', 'hang']
def build(who):
    rows = [(a, dn, y) for a in PLAN for dn, y in D4.items()]
    cols = 8; W = cols * (CW + PAD) + PAD; H = len(rows) * (CH + PAD) + PAD
    sh = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    atlas = dict(cell=[CW, CH], anchor=[20, 46], pad=PAD, cols=cols, persp='side', rows={}, speed_mps=speed(who) * SCALE[who], scale=SCALE[who], gait=GAIT[who])
    for r, (a, dn, y) in enumerate(rows):
        n = ANIMS[a][0]
        for k in range(n):
            sh.alpha_composite(frame(who, pose_for(who, a, k, math.radians(y)), 0), (PAD + k * (CW + PAD), PAD + r * (CH + PAD)))
        atlas['rows'][f'{a}/{dn}'] = dict(row=r, n=n, fps=ANIMS[a][1] or (8 / GAIT[who]['T']), loop=ANIMS[a][2])
    sh.save(f'{OUT}/{who}_side.png'); json.dump(atlas, open(f'{OUT}/{who}_side.json', 'w'), indent=1)
    return who, sh.size
if __name__ == '__main__':
    whos = sys.argv[1].split(',')
    with Pool(2) as p:
        for r in p.imap_unordered(build, whos): print(r, flush=True)

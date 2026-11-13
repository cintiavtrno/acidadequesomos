"""Folhas de perfil (side) dos personagens de 1996 no mesmo formato de build_side.py (linhas 'anim/dir', 8 colunas, célula 40x52, âncora 20,46)."""
import json, math, os, sys
from multiprocessing import Pool
from PIL import Image
import drv96, rig_96 as R96
from pipeline import CW, CH, SCALE
from anim import ANIMS, GAIT, speed
OUT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'assets', 'chars'))
D4 = {'down': 0, 'right': 90, 'up': 180, 'left': 270}
PAD = 2
BASE = ['idle', 'walk', 'talk', 'wave']
PLAN = {}
for n in R96.PERCS: PLAN[n] = BASE + ['drum', 'drumwalk']
PLAN['cantor'] = BASE + ['sway', 'pose']
PLAN['cam1'] = BASE + ['film', 'camwalk']
PLAN['cam2o'] = BASE + ['film']; PLAN['cam3o'] = PLAN['cam2o']; PLAN['assist2'] = BASE + ['note', 'radio']
PLAN['assist'] = BASE + ['note', 'radio']
PLAN['carga'] = BASE + ['carry', 'carrywalk']
PLAN['diretor'] = BASE + ['watch', 'point']
def build(who):
    rows = [(a, dn, y) for a in PLAN[who] for dn, y in D4.items()]
    cols = 8; W = cols * (CW + PAD) + PAD; H = len(rows) * (CH + PAD) + PAD
    sh = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    atlas = dict(cell=[CW, CH], anchor=[20, 46], pad=PAD, cols=cols, persp='side', rows={}, speed_mps=speed(who) * SCALE[who], scale=SCALE[who], gait=GAIT[who])
    for r, (a, dn, y) in enumerate(rows):
        n = ANIMS[a][0]
        for k in range(n):
            im = drv96.fr(who, a, k, y)
            sh.alpha_composite(im, (PAD + k * (CW + PAD), PAD + r * (CH + PAD)))
        fps = ANIMS[a][1] or (8 / GAIT[who]['T'])
        atlas['rows'][f'{a}/{dn}'] = dict(row=r, n=n, fps=fps, loop=ANIMS[a][2])
    sh.save(f'{OUT}/{who}_side.png'); json.dump(atlas, open(f'{OUT}/{who}_side.json', 'w'), indent=1)
    return who, sh.size
if __name__ == '__main__':
    whos = sys.argv[1].split(',') if len(sys.argv) > 1 else list(PLAN)
    with Pool(min(len(whos), os.cpu_count() or 2)) as p:
        for r in p.imap_unordered(build, whos): print(r, flush=True)

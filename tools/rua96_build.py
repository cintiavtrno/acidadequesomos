"""Monta world/front/far/scene do cenário-base de 1996 e as prévias de aprovação."""
import json, random, os
from PIL import Image
from pxl import *
import rua96_world as R
import rua6_props as RP
import far as FAR
from rua96_world import W, VH, yw, wy

OUT = '../assets/street96/'; os.makedirs(OUT, exist_ok=True)
INST = [dict(id='poste_1', sprite='poste', x=168, sy=24), dict(id='poste_2', sprite='poste', x=678, sy=24), dict(id='poste_3', sprite='poste', x=1150, sy=24)]

def front_layer(B):
    f = C(W, VH)
    def top_y(i): return yw(i['x']) + i['sy'] - 192 + 9
    def wire(x0, y0, x1, y1, sag, col=(30, 26, 36)):
        n = max(2, int(max(abs(x1 - x0), abs(y1 - y0) + sag * 2)) * 2)
        for k in range(n):
            t = k / (n - 1); f.pset(round(x0 + (x1 - x0) * t), round(y0 + (y1 - y0) * t + sag * 4 * t * (1 - t)), col)
    poles = INST
    for a, b in zip(poles, poles[1:]):
        for k, o in enumerate((-10, -4, 4, 10)):
            wire(a['x'] + o, top_y(a), b['x'] + o, top_y(b), 5 + (k % 2) * 2 + (b['x'] - a['x']) // 120, col=(30, 26, 36) if k % 3 else (54, 46, 58))
    def ramal(p, o, wx, wy_, sag=4):
        wire(p['x'] + o, top_y(p), wx, wy_, sag)
        f.rect(wx - 1, wy_ - 1, 3, 3, (96, 150, 150)); f.pset(wx - 1, wy_ - 1, (170, 214, 206)); f.pset(wx, wy_ + 2, (60, 56, 68))
    ramal(poles[0], 4, 160, wy(B['casa_salvia'], 98) + 6, 4); ramal(poles[0], -10, 30, wy(B['casa_salvia'], 98) + 4, 3)
    ramal(poles[1], -10, 596, wy(B['padaria'], 100) + 4, 4); ramal(poles[1], 4, 770, wy(B['azul'], 92) + 4, 3)
    ramal(poles[2], -4, 1060, wy(B['agua'], 92) + 4, 4); ramal(poles[2], 10, 1300, wy(B['rosa'], 92) + 2, 5)
    return f

def meta_scene(B):
    sol = []
    return dict(W=W, VH=VH, slope=dict(base=R.SLOPE_BASE, div=R.SLOPE_DIV), SW=22, walk=dict(top=8, bot=VH - 3), inst=[], solids=sol, ano=1996,
                buildings={n: dict(x0=b['x0'], w=b['w'], base=b['base'], door_x=b.get('door_x'), flat=b.get('flat')) for n, b in B.items()})

def far96():
    FAR.FAR_W = 900
    return FAR.far_layer()

def compose(world, front, far, sheet, meta, cam_far=True):
    bg = Image.new('RGBA', (W, VH))
    for k in range(0, W, far.im.width): pass
    # paralaxe 0.35: para a prévia inteira usa o céu esticado pelo mesmo critério
    fi = far.im.convert('RGBA')
    for k in range(0, W, fi.width): bg.paste(fi, (k, 0))
    bg.alpha_composite(world.im)
    m = meta['poste']
    for i in INST:
        fx, fy = m['frames'][0]; cr = sheet.crop((fx, fy, fx + m['w'], fy + m['h'])); by = yw(i['x']) + i['sy']
        bg.alpha_composite(cr, (i['x'] - m['ax'], by - m['ay']))
    bg.alpha_composite(front.im)
    return bg

if __name__ == '__main__':
    world, placed, B = R.build_world96()
    front = front_layer(B)
    far = far96()
    sheet, meta = RP.build_atlas(OUT + 'props.png', OUT + 'props.json')
    world.save(OUT + 'world.png'); front.save(OUT + 'front.png'); far.save(OUT + 'far.png')
    json.dump(meta_scene(B), open(OUT + 'scene_rua96.json', 'w'), indent=1, ensure_ascii=False)
    full = compose(world, front, far, sheet.im, meta)
    full.save('/home/claude/out96/rua96_base_full.png')
    for k, (a, b) in enumerate([(0, 520), (490, 1010), (980, 1500)]):
        full.crop((a, 0, b, VH)).resize(((b - a) * 3, VH * 3), Image.NEAREST).save(f'/home/claude/out96/rua96_base_p{k}.png')
    print('ok')

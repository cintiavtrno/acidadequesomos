"""Gera os assets da Etapa 6: mundo (fachadas+chão), camada da frente (fios), objetos, cena JSON e prévias estáticas."""
import json, math, random, sys
from PIL import Image
from pxl import *
import rua6_world as RW
import rua6_props as RP
from rua6_world import yw, W, VH, wy

OUT = '../assets/street6/'
# ---------------------------------------------------------------- instâncias (x = centro; sy = linha dos pés abaixo do encosto da parede: 0..21 calçada, 22+ meio-fio/rua)
INST = [
 # mobiliário urbano
 dict(id='poste_1', sprite='poste', x=114, sy=24), dict(id='poste_2', sprite='poste', x=395, sy=24), dict(id='poste_3', sprite='poste', x=868, sy=24),
 dict(id='orelhao_1', sprite='orelhao', x=600, sy=15),
 dict(id='cavalete_pao', sprite='cavalete_pao', x=525, sy=14),
 dict(id='lixeira_1', sprite='lixeira', x=294, sy=19), dict(id='lixeira_2', sprite='lixeira', x=786, sy=19),
 dict(id='banco_1', sprite='banco', x=562, sy=14),
 dict(id='bike_1', sprite='bicicleta', x=702, sy=11),
 dict(id='caixote_1', sprite='caixote_laranja', x=318, sy=15),
 dict(id='gato_1', sprite='gato', x=186, sy=10, anim='gato'),
 # (Etapa 6 rev.: sem árvores nem canteiros na calçada; só a vegetação das janelas e fachadas, que faz parte do mundo)
 # dominó (ancorado à fachada do sobrado)
 dict(id='mesa_domino', sprite='mesa_domino', x=240, sy=15),
 dict(id='cad_dom_E', sprite='cad_dir', x=212, sy=15), dict(id='cad_dom_D', sprite='cad_esq', x=268, sy=15),
 dict(id='cad_dom_F', sprite='cad_fundo', x=240, sy=8), dict(id='cad_dom_T', sprite='cad_fundo', x=240, sy=22),
 dict(id='cad_dom_T_enc', sprite='cad_costas', x=240, sy=22, layer='over'),
 dict(id='banquinho_1', sprite='banquinho', x=292, sy=12), dict(id='banquinho_2', sprite='banquinho', x=182, sy=21),
 dict(id='cad_calcada_1', sprite='cad_calcada', x=1088, sy=10),
 # parede
 dict(id='quadro_avisos', sprite='quadro_avisos', x=718, sy=0, layer='wall'),
]
INST = [i for i in INST if i]
SPR = RP.PRO

def solids():
    out = []
    for i in INST:
        m = SPR[i['sprite']]['meta']; c = m.get('collide')
        if not c or i.get('layer') in ('over', 'wall'): continue
        out.append(dict(id=i['id'], x0=i['x'] + c[0], x1=i['x'] + c[2], sy0=i['sy'] + c[1], sy1=i['sy'] + c[3]))
    return out

# ---------------------------------------------------------------- camada da frente (fios)
def front_layer(B):
    f = C(W, VH); rng = random.Random(7)
    def top_y(i):  # topo dos isoladores de um poste
        return yw(i['x']) + i['sy'] - 192 + 9
    poles = [i for i in INST if i['sprite'] == 'poste']
    def wire(x0, y0, x1, y1, sag, col=(30, 26, 36)):
        n = max(2, int(max(abs(x1 - x0), abs(y1 - y0) + sag * 2)) * 2)
        for k in range(n):
            t = k / (n - 1); x = x0 + (x1 - x0) * t; y = y0 + (y1 - y0) * t + sag * 4 * t * (1 - t)
            f.pset(round(x), round(y), col)
    offs = (-10, -4, 4, 10)
    for a, b in zip(poles, poles[1:]):
        for k, o in enumerate(offs):
            wire(a['x'] + o, top_y(a), b['x'] + o, top_y(b), 5 + (k % 2) * 2 + (b['x'] - a['x']) // 120, col=(30, 26, 36) if k % 3 else (54, 46, 58))
    # ramais para as casas (do poste para um isolador de parede)
    def ramal(p, o, wx, wy_, sag=4):
        wire(p['x'] + o, top_y(p), wx, wy_, sag)
        f.rect(wx - 1, wy_ - 1, 3, 3, (96, 150, 150)); f.pset(wx - 1, wy_ - 1, (170, 214, 206)); f.pset(wx, wy_ + 2, (60, 56, 68))
    ramal(poles[0], 4, 186, wy(B['sobrado'], 98) + 6, 4)
    ramal(poles[1], -10, 345, wy(B['padaria'], 84) + 4, 4)
    ramal(poles[1], 4, 616, wy(B['padaria'], 100) + 2, 5)
    ramal(poles[2], -4, 850, wy(B['verde'], 92) + 4, 3)
    ramal(poles[2], 10, 988, wy(B['b5'], 86) + 2, 5)
    return f

def meta_scene(B):
    spots = {}
    return dict(W=W, VH=VH, slope=dict(base=212, div=70), SW=22, walk=dict(top=8, bot=VH - 3 - 0),
                inst=[dict({**i, **{k: v for k, v in SPR[i['sprite']]['meta'].items() if k in ('nome', 'tipo', 'classe', 'desc', 'zoom', 'stand', 'collide')}, 'layer': i.get('layer', SPR[i['sprite']]['meta'].get('layer', 'sorted'))}) for i in INST],
                solids=solids(), buildings={n: dict(x0=b['x0'], w=b['w'], base=b['base'], door_x=b.get('door_x'), flat=b.get('flat')) for n, b in B.items()})

# ---------------------------------------------------------------- compositor estático (mesmo critério de ordenação do jogo)
def spr_img(sprite, f=0):
    return Image.open(OUT + 'props.png').convert('RGBA')

def compose_preview(world, front, atlas_meta, sheet, extra=None):
    v = Image.new('RGBA', (W, VH), (0, 0, 0, 0))
    far = Image.open('../assets/street_far.png').convert('RGBA')
    bg = Image.new('RGBA', (W, VH))
    # fundo distante: repete cobrindo o mundo (prévia; no jogo tem paralaxe)
    for k in range(0, W, far.width): bg.paste(far, (k, 0))
    bg.alpha_composite(world.im)
    ents = []
    for i in INST:
        m = atlas_meta[i['sprite']]; layer = i.get('layer', m.get('layer', 'sorted'))
        fx, fy = m['frames'][0]; cr = sheet.crop((fx, fy, fx + m['w'], fy + m['h']))
        bx = i['x']; by = yw(i['x']) + i['sy'] if layer != 'wall' else yw(i['x']) - 34
        ents.append((by + (0.5 if layer == 'over' else 0), layer, cr, bx - m['ax'], by - m['ay']))
    for (y, layer, im, x, yy) in sorted([e for e in ents if e[1] == 'wall'], key=lambda e: e[0]): bg.alpha_composite(im, (int(x), int(yy)))
    for (y, layer, im, x, yy) in sorted([e for e in ents if e[1] != 'wall'], key=lambda e: e[0]):
        bg.alpha_composite(im, (int(x), int(yy)))
    if extra: extra(bg)
    bg.alpha_composite(front.im)
    return bg

def run():
    world, placed, B = RW.build_world()
    front = front_layer(B)
    sheet, meta = RP.build_atlas(OUT + 'props.png', OUT + 'props.json')
    world.save(OUT + 'world.png'); front.save(OUT + 'front.png')
    scene = meta_scene(B); json.dump(scene, open(OUT + 'scene_rua.json', 'w'), indent=1, ensure_ascii=False)
    return world, front, meta, sheet, B

if __name__ == '__main__':
    world, front, meta, sheet, B = run()
    full = compose_preview(world, front, meta, sheet.im)
    full.save('/tmp/rua6_full.png')
    for k, (a, b) in enumerate([(0, 400), (370, 770), (730, 1130)]):
        full.crop((a, 0, b, VH)).resize(((b - a) * 3, VH * 3), Image.NEAREST).save(f'/tmp/rua6_p{k}.png')
    print('ok', len(INST))

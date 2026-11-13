"""Etapa C de 1996: posiciona os objetos na rua-base, valida contato/escala/colisão e gera as capturas.
sy = linha dos pés abaixo do encosto da parede (0..21 calçada · 22..27 meio-fio e sarjeta · 28+ rua de pedra)."""
import json, os
from PIL import Image
from pxl import *
import rua96_world as R
import rua96_props as P96
import rua6_props as RP
import rua96_build as B96
from rua96_world import W, VH, yw, wy

# espelho do cabo (descida do lado oposto)
@RP.prop('cabo_desce_e', 34, 18, 29, 16, nome='cabo com protetor de passagem (espelhado)', tipo='nenhum', classe='DECORATIVO', size_m=(1.4, 0.7, 0.2), collide=None)
def _desce_e(c):
    t = C(34, 18); RP.PRO['cabo_desce']['fn'](t)
    for y in range(18):
        for x in range(34): c.pset(33 - x, y, t.get(x, y))

I = lambda id, sprite, x, sy, **k: dict(id=id, sprite=sprite, x=x, sy=sy, **k)
INST = [
 # --- mobiliário urbano (mantido de 1991: mesmos objetos, novos pontos)
 I('poste_1', 'poste', 168, 24), I('poste_2', 'poste', 678, 24), I('poste_3', 'poste', 1166, 24),
 I('orelhao_1', 'orelhao', 412, 12), I('lixeira_1', 'lixeira', 612, 19), I('lixeira_2', 'lixeira', 1334, 19),
 I('banco_1', 'banco', 72, 14), I('cad_calcada_1', 'cad_calcada', 1470, 10),
 I('gato_1', 'gato', 150, 10, anim='gato'),
 I('cavalete_pao', 'cavalete_pao', 556, 14),
 # --- cotidiano
 I('vaso_palmeira_1', 'vaso_palmeira', 12, 13), I('vaso_latas_1', 'vaso_latas', 1308, 13), I('vaso_espada_1', 'vaso_espada', 1402, 14),
 I('caixote_1', 'caixote_laranja', 384, 16), I('banca_1', 'banca_tabuleiro', 344, 14),
 I('mesa_domino', 'mesa_domino', 278, 15), I('cad_dom_E', 'cad_dir', 252, 15), I('cad_dom_D', 'cad_esq', 306, 15), I('cad_dom_F', 'cad_fundo', 278, 8),
 I('cad_dom_T', 'cad_fundo', 278, 22), I('cad_dom_T_enc', 'cad_costas', 278, 22, layer='over'),
 I('quadro_avisos', 'quadro_avisos', 759, 0, layer='wall'),
 # --- produção: câmera A (esquerda), câmera B (direita), base na calçada, cases do lado da câmera B
 I('cam_A', 'tripe_cam_d', 702, 40), I('cam_B', 'tripe_cam_e', 1144, 40),
 I('mic_boom_1', 'mic_boom', 800, 26), I('mic_ped_1', 'mic_pedestal', 990, 26),
 I('base_cad_d', 'cad_dobravel_d', 834, 13), I('base_monitor', 'monitor_case', 872, 12), I('base_cad_e', 'cad_dobravel_e', 906, 13),
 I('cases_B1', 'case_pilha', 1200, 14), I('cases_B2', 'case_camera', 1234, 14),
 I('barr_A1', 'barreira', 746, 20), I('barr_B1', 'barreira', 1104, 20),
 # --- cabos: base -> câmera B (leste) e base -> câmera A (oeste), pela sarjeta
 I('cabo_E0', 'cabo_desce', 886, 28), I('cabo_E1', 'cabo_seg', 965, 27), I('cabo_E2', 'cabo_seg', 1065, 27), I('cabo_E3', 'cabo_desce', 1115, 41),
 I('cabo_O0', 'cabo_desce_e', 860, 28), I('cabo_O1', 'cabo_seg', 781, 27), I('cabo_O3', 'cabo_desce_e', 731, 41),
]

def sprites():
    sheet, meta = RP.build_atlas(B96.OUT + 'props.png', B96.OUT + 'props.json'); return sheet, meta

def bbox_alpha(sheet, m):
    fx, fy = m['frames'][0]; cr = sheet.im.crop((fx, fy, fx + m['w'], fy + m['h'])); b = cr.getchannel('A').point(lambda a: 255 if a > 60 else 0).getbbox()
    return b, cr

def entradas(meta, sheet):
    out = []
    for i in INST:
        m = meta[i['sprite']]; layer = i.get('layer', m.get('layer', 'sorted'))
        by = yw(i['x']) + i['sy'] if layer != 'wall' else yw(i['x']) - 34
        b, cr = bbox_alpha(sheet, m)
        out.append(dict(i=i, m=m, layer=layer, by=by, bx=i['x'] - m['ax'], oy=by - m['ay'], bb=(i['x'] - m['ax'] + b[0], by - m['ay'] + b[1], i['x'] - m['ax'] + b[2], by - m['ay'] + b[3]), cr=cr))
    return out

def validar(ents, B):
    erros = []
    doors = []
    for n, b in B.items():
        for fx in (b.get('flat') or []): doors.append((n, b['x0'] + fx - 18, b['x0'] + fx + 18, b['base']))
        if b.get('door_x') is not None: hw = 30 if n == 'padaria' else 22; doors.append((n, b['x0'] + b['door_x'] - hw, b['x0'] + b['door_x'] + hw, b['base']))
    for e in ents:
        i = e['i']; x0, y0, x1, y1 = e['bb']
        if e['layer'] == 'wall':
            continue
        # 1) contato: pé dentro da faixa jogável e sy coerente
        if not (0 <= i['sy'] <= (VH - 3 - yw(i['x']))): erros.append(f"{i['id']}: pé fora da faixa jogável (sy={i['sy']})")
        # 2) portas: objeto alto na calçada não pode tapar portas (cabos e peças baixas na sarjeta são livres)
        if i['sy'] <= 22 and (y1 - y0) > 12 and i['sprite'] not in ('poste', 'barreira'):
            for (n, a, b2, base) in doors:
                if x0 < b2 and x1 > a and abs(e['by'] - base) < 40: erros.append(f"{i['id']} cobre a porta de {n} ({x0}-{x1} × {a}-{b2})")
    # 3) sobreposição entre objetos (exceto pares intencionais)
    ok = {('mesa_domino', 'cad_dom_E'), ('mesa_domino', 'cad_dom_D'), ('mesa_domino', 'cad_dom_F'), ('mesa_domino', 'cad_dom_T'), ('mesa_domino', 'cad_dom_T_enc'), ('cad_dom_T', 'cad_dom_T_enc'), ('cad_dom_F', 'cad_dom_T'), ('cad_dom_F', 'cad_dom_T_enc')}
    for a in range(len(ents)):
        for b in range(a + 1, len(ents)):
            A, Bb = ents[a], ents[b]
            if 'wall' in (A['layer'], Bb['layer']): continue
            ida, idb = A['i']['id'], Bb['i']['id']
            if ida.startswith('cabo') or idb.startswith('cabo') or (ida, idb) in ok or (idb, ida) in ok: continue
            ax0, ay0, ax1, ay1 = A['bb']; bx0, by0, bx1, by1 = Bb['bb']
            if ax0 < bx1 and bx0 < ax1 and ay0 < by1 and by0 < ay1:
                ox0, ox1, oy0, oy1 = max(ax0, bx0), min(ax1, bx1), max(ay0, by0), min(ay1, by1)
                ma = A['cr'].getchannel('A').load(); mb = Bb['cr'].getchannel('A').load(); hit = 0
                for yy in range(oy0, oy1):
                    for xx in range(ox0, ox1):
                        pa = (xx - A['bx'], yy - A['oy']); pb = (xx - Bb['bx'], yy - Bb['oy'])
                        if 0 <= pa[0] < A['m']['w'] and 0 <= pa[1] < A['m']['h'] and 0 <= pb[0] < Bb['m']['w'] and 0 <= pb[1] < Bb['m']['h'] and ma[pa] > 60 and mb[pb] > 60: hit += 1
                if hit: erros.append(f"{ida} e {idb} se sobrepõem ({hit} px)")
    return erros

def compose(world, front, far, ents, only=None):
    bg = Image.new('RGBA', (W, VH)); fi = far.im.convert('RGBA')
    for k in range(0, W, fi.width): bg.paste(fi, (k, 0))
    bg.alpha_composite(world.im)
    es = [e for e in ents if (only is None or only(e))]
    for e in sorted([e for e in es if e['layer'] == 'wall'], key=lambda e: e['by']): bg.alpha_composite(e['cr'], (int(e['bx']), int(e['oy'])))
    for e in sorted([e for e in es if e['layer'] != 'wall'], key=lambda e: e['by'] + (0.5 if e['layer'] == 'over' else 0)): bg.alpha_composite(e['cr'], (int(e['bx']), int(e['oy'])))
    bg.alpha_composite(front.im)
    return bg

def meta_scene(B, meta):
    inst = [dict({**i, **{k: v for k, v in meta[i['sprite']].items() if k in ('nome', 'tipo', 'classe', 'desc', 'zoom', 'stand', 'collide')}, 'layer': i.get('layer', meta[i['sprite']].get('layer', 'sorted'))}) for i in INST]
    solids = []
    for i in inst:
        c = i.get('collide')
        if not c or i['layer'] in ('over', 'wall'): continue
        solids.append(dict(id=i['id'], x0=i['x'] + c[0], x1=i['x'] + c[2], sy0=i['sy'] + c[1], sy1=i['sy'] + c[3]))
    return dict(W=W, VH=VH, slope=dict(base=R.SLOPE_BASE, div=R.SLOPE_DIV), SW=22, walk=dict(top=8, bot=VH - 3), inst=inst, solids=solids, ano=1996,
                palco=dict(x0=720, x1=1124, sy0=28, sy1=45), buildings={n: dict(x0=b['x0'], w=b['w'], base=b['base'], door_x=b.get('door_x'), flat=b.get('flat')) for n, b in B.items()})

if __name__ == '__main__':
    world, placed, B = R.build_world96()
    B96.INST[:] = [dict(id=i['id'], sprite=i['sprite'], x=i['x'], sy=i['sy']) for i in INST if i['sprite'] == 'poste']
    front = B96.front_layer(B); far = B96.far96()
    sheet, meta = sprites(); ents = entradas(meta, sheet)
    erros = validar(ents, B)
    print('erros de validação:', len(erros)); [print(' -', e) for e in erros]
    sc = meta_scene(B, meta)
    # colisão no palco: nenhum sólido invade a faixa livre
    inv = [s['id'] for s in sc['solids'] if s['x1'] > sc['palco']['x0'] and s['x0'] < sc['palco']['x1'] and s['sy1'] > sc['palco']['sy0']]
    print('sólidos dentro do palco (sy>=28):', inv)
    json.dump(sc, open(B96.OUT + 'scene_rua96.json', 'w'), indent=1, ensure_ascii=False)
    world.save(B96.OUT + 'world.png'); front.save(B96.OUT + 'front.png'); far.save(B96.OUT + 'far.png')
    full = compose(world, front, far, ents); full.save('/home/claude/out96/rua96_c_full.png')
    for k, (a, b) in enumerate([(0, 520), (490, 1010), (980, 1500)]): full.crop((a, 0, b, VH)).resize(((b - a) * 3, VH * 3), Image.NEAREST).save(f'/home/claude/out96/rua96_c_p{k}.png')
    print('ok', len(INST), 'objetos')

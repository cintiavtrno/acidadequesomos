# Etapa 8.5 — imagens de posicionamento (planta + vista 3/4 + mapas) a partir de quintal_data.py + quintal_pos.py. Esquemas de projeto, não arte final.
import io, os, runpy, sys, math
from contextlib import redirect_stdout
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
with redirect_stdout(io.StringIO()):
    G = runpy.run_path(os.path.join(HERE, 'gerar_quintal.py'), run_name='lib')
    TP = runpy.run_path(os.path.join(HERE, 'teste_pos.py'), run_name='lib')
from PIL import Image, ImageDraw
import quintal_data as Q, quintal_pos as P
F_, where, CHX = TP['F'], TP['where'], TP['CHX']
Plan, F, FB, FS, hexrgb, COR, CC, INI, rect, OBJ = (G[k] for k in ('Plan', 'F', 'FB', 'FS', 'hexrgb', 'COR', 'CC', 'INI', 'rect', 'OBJ'))
CC = dict(CC); INI = dict(INI)
for i, m in enumerate(['m1', 'm2', 'm3', 'm4', 'm5', 'm6']): CC[m] = ['#f2c14e', '#7bc6a4', '#e68a7a', '#7aa7e0', '#c79bd8', '#f0a45a'][i]; INI[m] = m.upper()
COLZ = {'Z1': '#e9a15b', 'Z2': '#e8d36a', 'Z3': '#8fc47a', 'Z4': '#7aa9d8', 'Z5': '#b79ad8', 'ZE': '#e87fa0'}
SM = {s[0]: s for s in P.S}
def cor_item(i):
    if i.startswith('E'): return '#f2b8c8'
    z = SM[i][2]; return {'Z1': '#f0c48a', 'Z2': '#efe08c', 'Z3': '#b7dba6', 'Z4': '#a9c8ea', 'Z5': '#cdb8e8'}.get(z, '#ddd')
Tt = P.TOALHA; B = P.BANDEIRA
# ============================================================ planta
def planta():
    pc = Plan(30, ml=50, mt=44, mb=120); d = pc.d; Pp = pc.P
    pc.base()
    def zon(od):
        for z, (x0, y0, x1, y1) in P.ZONA_RECT.items(): od.rectangle([*Pp(x0, y0), *Pp(x1, y1)], fill=hexrgb(COLZ[z], 50), outline=hexrgb(COLZ[z], 200))
    pc.overlay(zon); d = pc.d
    for z, (x0, y0, x1, y1) in P.ZONA_RECT.items(): d.text((Pp(x0, y0)[0] + 3, Pp(x0, y0)[1] + 2), z, fill='#222', font=FB)
    # toalha e faixa de respeito
    def toa(od):
        od.rectangle([*Pp(Tt['x0'], Tt['y0']), *Pp(Tt['x1'], Tt['y1'])], fill=(240, 160, 190, 150), outline=(190, 60, 110, 255))
        od.rectangle([*Pp(Tt['x0'] - Tt['buffer'], Tt['y0'] - Tt['buffer']), *Pp(Tt['x1'] + Tt['buffer'], Tt['y1'] + Tt['buffer'])], outline=(190, 60, 110, 200), width=1)
    pc.overlay(toa); d = pc.d
    pc.objs()
    for s in P.S:
        i, nome, z, sup, x, y, w, dd, h = s[:9]
        if i == 'E01' or i == 'S22': continue
        d.rectangle([*Pp(x, y), *Pp(x + w, y + dd)], fill=cor_item(i), outline='#333')
        if i not in ('E11',) and w * 30 >= 12: d.text((Pp(x, y)[0] + 1, Pp(x, y)[1] + 1), i[1:], fill='#222', font=FS)
    # pessoas C1
    for k in F_:
        x, y, st = where(k); r = CHX[k][2] * 30 * (0.8 if st != 'pe' else 1.0)
        cx, cy = Pp(x, y); d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=CC[k], outline='#000'); d.text((cx - 7, cy - 5), INI[k], fill='#000', font=FS)
    # bandeira na parede (traço grosso) e área de olhar
    a, b = Pp(B['x0'], -0.15), Pp(B['x1'], -0.15); d.line([a, b], fill='#c0392b', width=6); d.text((a[0] - 10, a[1] - 18), 'B01 bandeira (parede)', fill='#c0392b', font=FB)
    v = P.BANNER_VIEW; d.rectangle([*Pp(v[0], v[1]), *Pp(v[2], v[3])], outline='#c0392b'); 
    # pontos de uso
    for k in ('F12a', 'F12b', 'banner', 'toalha_zefa', 'M27', 'M09', 'F09b'):
        x, y = P.STAND2[k][:2]; cx, cy = Pp(x, y); d.polygon([(cx, cy - 4), (cx + 4, cy + 4), (cx - 4, cy + 4)], fill='#222')
    # legenda
    yb = pc.mt + int(Q.D * 30) + 10
    L = ['PLANTA 8.5 · fase C1 (sete meninos comem) · 30 px/m · mesmos IDs e posições da vista 3/4 · fundo = zonas Z1–Z5 e ZE (nomes da etapa 8.5)',
         'Cinza/marrom = fixos F · amarelo-café = móveis M · verde = decorativo D · cores claras = objetos menores S/E (número = ID sem a letra) · rosa = toalha dos sete meninos + faixa de respeito (0,4 m) · ▲ = ponto de uso',
         f'Bandeira B01: {B["x1"]-B["x0"]:.2f} × {B["z1"]-B["z0"]:.2f} m = {B["area"]:.2f} m² = {B["area"]/P.PAREDE_LIVRE_M2:.0%} do pano de parede livre ({P.PAREDE_LIVRE_M2:.2f} m²) · X {B["x0"]}–{B["x1"]} m, Z {B["z0"]}–{B["z1"]} m',
         'Ajuste da planta aprovada: lavatório M22 de (9,2; 5,6) para (10,2; 6,0) para abrir a frente da toalha · ponto de uso F12a/F12b do aparador: (11,2; 1,32) e (12,3; 1,32)']
    import textwrap
    n = 0
    for t in L:
        for ln in textwrap.wrap(t, 150): d.text((12, yb + n * 13), ln, fill='#222', font=F); n += 1
    pc.im.convert('RGB').save('out/quintal_pos_planta.png'); return pc.im.size
def mapa():
    pc = Plan(30, ml=50, mt=44, mb=100); d = pc.d; Pp = pc.P; pc.base()
    def ov(od):
        for o in Q.OBJ:
            if o[0] in ('F01', 'F02', 'F03', 'F04') or not o[8]: continue
            x0, y0, x1, y1 = rect(o); od.rectangle([*Pp(x0, y0), *Pp(x1, y1)], fill=(200, 60, 50, 120), outline=(160, 30, 30, 255))
        od.rectangle([*Pp(Tt['x0'] - Tt['buffer'], Tt['y0'] - Tt['buffer']), *Pp(Tt['x1'] + Tt['buffer'], Tt['y1'] + Tt['buffer'])], fill=(190, 60, 110, 90), outline=(190, 60, 110, 255))
        r = 0.9 * 30
        for k, (x, y, f) in P.STAND2.items():
            if k in ('portao', 'telhado'): continue
            cx, cy = Pp(x, y); od.ellipse([cx - r, cy - r, cx + r, cy + r], outline=(40, 140, 70, 200), fill=(80, 190, 110, 28))
        v = P.BANNER_VIEW; od.rectangle([*Pp(v[0], v[1]), *Pp(v[2], v[3])], fill=(230, 190, 60, 90), outline=(190, 140, 20, 255))
    pc.overlay(ov); d = pc.d
    cols = ['#1f77b4', '#ff7f0e', '#2ca02c', '#9467bd', '#8c564b', '#e377c2', '#17becf', '#bcbd22', '#d62728']
    for n, (a, A, b, Bp) in enumerate(TP['rotasC1']):
        pth = TP['astar'](TP['wn2'], A, Bp, True)
        if pth: d.line([Pp((c[0] + .5) * 0.1, (c[1] + .5) * 0.1) for c in pth], fill=cols[n % 9], width=2)
    for z in ('F12a', 'F12b', 'banner', 'toalha_zefa', 'F09b', 'M27', 'M09'):
        x, y = P.STAND2[z][:2]; cx, cy = Pp(x, y); d.polygon([(cx, cy - 4), (cx + 4, cy + 4), (cx - 4, cy + 4)], fill='#222'); d.text((cx + 5, cy - 6), z, fill='#222', font=FS)
    yb = pc.mt + int(Q.D * 30) + 10
    import textwrap
    L = ['MAPA 8.5 · vermelho = colisão (objetos F/M/D, rosa = toalha + faixa de respeito 0,4 m, só na fase C1) · verde = área de interação (raio 0,9 m dos pontos de uso ▲) · amarelo = onde Lia olha a bandeira (B01) · linhas coloridas = rotas livres da fase C1 (A* com folga, não são trilhos)',
         'Objetos menores (S/E) sobre superfícies não têm colisão própria: herdam a do móvel que os apoia. S10 (bacia no chão) é zona de trabalho sentado, sem passagem.']
    n = 0
    for t in L:
        for ln in textwrap.wrap(t, 150): d.text((12, yb + n * 13), ln, fill='#222', font=F); n += 1
    pc.im.convert('RGB').save('out/quintal_pos_mapa.png'); return pc.im.size
# ============================================================ vista 3/4
src = open('/tmp/vista_src.py').read().replace('def vista(Z, anot=False):', 'def vista5(Z, anot=False):')
src = src.replace("    # piso\n", """    # bandeira de Cosme e Damião (pano pendurado na parede da casa)
    a, b = p(B['x0'], 0, B['z1']), p(B['x1'], 0, B['z0'])
    d.rectangle([a[0] - 1, a[1] - 3 * Z // 2, b[0] + 1, a[1]], fill='#6b4a35')                          # vareta superior
    d.rectangle([a[0], a[1], b[0], b[1]], fill='#2f7f6a', outline='#14463a')
    d.rectangle([a[0] + 3 * Z, a[1] + 3 * Z, b[0] - 3 * Z, b[1] - 3 * Z], outline='#e6c54a')
    cxm = (a[0] + b[0]) / 2; cym = (a[1] + b[1]) / 2
    d.ellipse([cxm - 14 * Z, cym - 20 * Z, cxm - 2 * Z, cym - 8 * Z], fill='#e8c9a0', outline='#7a5a3a'); d.ellipse([cxm + 2 * Z, cym - 20 * Z, cxm + 14 * Z, cym - 8 * Z], fill='#e8c9a0', outline='#7a5a3a')
    d.rectangle([cxm - 15 * Z, cym - 8 * Z, cxm - 1 * Z, cym + 14 * Z], fill='#c0392b'); d.rectangle([cxm + 1 * Z, cym - 8 * Z, cxm + 15 * Z, cym + 14 * Z], fill='#c0392b')
    if anot: d.text((a[0] + 4 * Z, b[1] + 2), 'B01 bandeira\\n(esquema: dois\\nsantos gêmeos;\\narte final a criar)', fill='#fff', font=FS)
    # piso
""", 1)
src = src.replace("    # beiral frontal do puxadinho", """    # toalha dos sete meninos (decalque no chão) e faixa de respeito
    q = [p(Tt['x0'], Tt['y0']), p(Tt['x1'], Tt['y0']), p(Tt['x1'], Tt['y1']), p(Tt['x0'], Tt['y1'])]
    d.polygon(q, fill='#e8a0b8', outline='#a43a63')
    for k in range(1, 6):
        d.line([p(Tt['x0'] + k * 0.366, Tt['y0']), p(Tt['x0'] + k * 0.366, Tt['y1'])], fill='#d98aa6'); d.line([p(Tt['x0'], Tt['y0'] + k * 0.366), p(Tt['x1'], Tt['y0'] + k * 0.366)], fill='#d98aa6')
    if anot:
        qb = [p(Tt['x0'] - .4, Tt['y0'] - .4), p(Tt['x1'] + .4, Tt['y0'] - .4), p(Tt['x1'] + .4, Tt['y1'] + .4), p(Tt['x0'] - .4, Tt['y1'] + .4)]
        d.line(qb + [qb[0]], fill='#a43a63', width=1)
    # beiral frontal do puxadinho""", 1)
src = src.replace("    for k in Q.FASE['C']:\n        x, y, st, sid = pos('C', k); itens.append((((OBJ[Q.SEATS[sid][2]][4] + OBJ[Q.SEATS[sid][2]][6] + 0.01) if st == 'sentado' else y), 1, (k, x, y, st, sid)))",
"""    for k in F_:
        x, y, st = where(k)
        if st == 'sentado': sid = F_[k][0]; ob = OBJ[Q.SEATS[sid][2]]; key = ob[4] + ob[6] + 0.01
        elif st == 'chao': key = y + 0.25
        else: key = y
        itens.append((key, 1, (k, x, y, st, None)))
    for s in P.S:
        if s[0] in ('E01', 'S22'): continue
        sup = s[3]
        key = (OBJ[sup][4] + OBJ[sup][6] + 0.002) if sup in OBJ else (s[5] + s[7] + 0.002)
        itens.append((key, 2, s))""")
src = src.replace("        else:\n            k, x, y, st, sid = o; h = Q.CH[k][1] * (0.72 if st == 'sentado' else 1.0)",
"""        elif kind == 2:
            i, nome, z, sup, x, y, w, dd, h, zb = o[:10]
            t0, t1 = p(x, y, zb + h), p(x + w, y + dd, zb + h); f0, f1 = p(x, y + dd, zb + h), p(x + w, y + dd, zb)
            c = hexrgb(cor_item(i)); dark = tuple(int(v * 0.8) for v in c[:3])
            d.rectangle([t0[0], t0[1], t1[0], f0[1]], fill=cor_item(i), outline='#444'); d.rectangle([f0[0], f0[1], f1[0], max(f1[1], f0[1] + 1)], fill=dark, outline='#444')
        else:
            k, x, y, st, sid = o; h = CHX[k][1] * (0.72 if st == 'sentado' else 0.62 if st == 'chao' else 1.0)""")
src = src.replace("w = Q.CH[k][2] * 24 * Z * 0.9", "w = CHX[k][2] * 24 * Z * 0.9")
import re
src = re.sub(r"    if anot:\n        d\.text\([^\n]*\n", "", src)
src = src.replace("    return im.convert('RGB')", "    if anot:\n        d.text((6, 6), 'VISTA 3/4 · fase C1 · mesmos IDs e posições da planta · B01 bandeira · E01 toalha (linha rosa = faixa de respeito) · sete meninos em roda aberta para a câmera', fill='#000', font=F)\n    return im.convert('RGB')")
ns = dict(G); ns.update(dict(CC=CC, INI=INI, F_=F_, where=where, CHX=CHX, P=P, Q=Q, Tt=Tt, B=B, cor_item=cor_item, hexrgb=hexrgb, Image=Image, ImageDraw=ImageDraw))
exec(src, ns)
if __name__ == '__main__':
    os.chdir(os.path.join(HERE, '..'))
    sz = planta(); mapa()
    v = ns['vista5']
    v(1).save('out/quintal_pos_vista34_720x270.png'); v(2).save('out/quintal_pos_vista34_1440x540.png'); v(2, True).save('out/quintal_pos_vista34_anotada_1440x540.png')
    print('planta', sz, 'vista', v(1).size)

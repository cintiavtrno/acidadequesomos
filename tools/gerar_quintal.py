# Gera as imagens revisadas do projeto do quintal (Etapa 8.3 revisada) a partir de quintal_data.py. Esquemas de projeto, não arte final.
import glob, io, math, os, runpy, sys, textwrap
from contextlib import redirect_stdout
from PIL import Image, ImageDraw, ImageFont
HERE = os.path.dirname(os.path.abspath(__file__)); os.chdir(os.path.join(HERE, '..'))
sys.path.insert(0, HERE)
import quintal_data as Q
with redirect_stdout(io.StringIO()): T = runpy.run_path(os.path.join(HERE, 'teste_quintal.py'), run_name='lib')   # reaproveita grade, A*, copa
DIST, BLK, REST, astar, walk, HULL, pos, R = T['DIST'], T['BLK'], T['REST'], T['astar'], T['walk'], T['HULL'], T['pos'], T['R']
_f = (glob.glob('/usr/share/fonts/**/DejaVuSans.ttf', recursive=True) or [None])[0]
F = ImageFont.truetype(_f, 10) if _f else ImageFont.load_default()
FB = ImageFont.truetype(_f.replace('DejaVuSans', 'DejaVuSans-Bold'), 11) if _f else F
FS = ImageFont.truetype(_f, 8) if _f else F
COR = {'F': '#9b8266', 'M': '#c79a63', 'D': '#6f9a5a'}
CC = {'lia': '#2aa198', 'zefa': '#d9534f', 'aurea': '#3b5ba5', 'raimundo': '#8a6d3b', 'dandara': '#8e44ad', 'ze': '#5b9bd5', 'nonato': '#e6b422', 'bela': '#e48ab0',
      'cicera': '#e6a817', 'junior': '#e0705a', 'tonho': '#2e8b8b', 'nena': '#d8d8d8', 'davi': '#444444', 'lucia': '#f08a24', 'rita': '#a3566b', 'caio': '#5a8f3d', 'bia': '#c0689a'}
INI = {'lia': 'Li', 'zefa': 'Ze', 'aurea': 'Áu', 'raimundo': 'Ra', 'dandara': 'Da', 'ze': 'Zé', 'nonato': 'No', 'bela': 'Be', 'cicera': 'Cí', 'junior': 'Jú', 'tonho': 'To', 'nena': 'Ne', 'davi': 'Dv', 'lucia': 'Lú', 'rita': 'Ri', 'caio': 'Ca', 'bia': 'Bi'}
def hexrgb(c, a=255): return tuple(int(c[i:i + 2], 16) for i in (1, 3, 5)) + (a,)
OBJ = {o[0]: o for o in Q.OBJ}
def rect(o): return o[3], o[4], o[3] + o[5], o[4] + o[6]

# =============================================================== planta (vista de cima verdadeira)
class Plan:
    def __init__(s, S, ml=50, mt=44, mb=118):
        s.S, s.ml, s.mt = S, ml, mt
        s.W = int(Q.W * S) + ml * 2; s.H = int(Q.D * S) + mt + mb
        s.im = Image.new('RGBA', (s.W, s.H), '#f4efe6'); s.d = ImageDraw.Draw(s.im)
    def P(s, x, y): return s.ml + x * s.S, s.mt + y * s.S
    def base(s):
        d, P = s.d, s.P
        d.rectangle([*P(0, 0), *P(Q.W, Q.D)], fill='#ead9bd', outline='#333')
        for i in range(0, 29):
            d.line([*P(i, 0), *P(i, Q.D)], fill='#e0cdac' if i % 2 else '#d3bf9b')
            if i % 2 == 0: d.text((P(i, 0)[0] - 7, s.mt - 16), f'{i} m', fill='#555', font=F)
        for j in range(0, 9):
            d.line([*P(0, j), *P(Q.W, j)], fill='#e0cdac' if j % 2 else '#d3bf9b')
            if j % 2 == 0: d.text((8, P(0, j)[1] - 5), f'{j} m', fill='#555', font=F)
    def overlay(s, fn):
        ov = Image.new('RGBA', s.im.size, (0, 0, 0, 0)); fn(ImageDraw.Draw(ov)); s.im = Image.alpha_composite(s.im, ov); s.d = ImageDraw.Draw(s.im)
    def zonas(s):
        def f(od):
            for n, x0, y0, x1, y1, c in Q.ZONAS: od.rectangle([*s.P(x0, y0), *s.P(x1, y1)], fill=hexrgb(c, 55), outline=hexrgb(c, 190))
        s.overlay(f)
        for n, x0, y0, x1, y1, c in Q.ZONAS: s.d.text((s.P(x0, y0)[0] + 3, s.P(x0, y0)[1] + 2), n, fill='#222', font=FB)
    def hatch(s, x0, y0, x1, y1, col, step=7):
        a, b = s.P(x0, y0), s.P(x1, y1)
        for k in range(int(a[0] - b[1] + a[1]), int(b[0]) + 1, step):
            xa, ya, xb, yb = k, a[1], k + (b[1] - a[1]), b[1]
            xa2, ya2 = max(a[0], min(b[0], xa)), a[1] + (max(a[0], min(b[0], xa)) - xa)
            xb2 = max(a[0], min(b[0], xb)); yb2 = b[1] - (xb - xb2)
            if ya2 <= b[1] and yb2 >= a[1] and xa2 < xb2: s.d.line([xa2, ya2, xb2, yb2], fill=col, width=1)
        s.d.rectangle([*a, *b], outline=col)
    def objs(s, ids=None, label=True):
        d = s.d
        for o in Q.OBJ:
            if o[0] in ('F01', 'F02', 'F03', 'F04') or (ids and o[0] not in ids): continue
            x0, y0, x1, y1 = rect(o)
            if o[0] == 'F14': cx, cy = s.P(22.6, 2.6); r = 0.4 * s.S; d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=COR['F'], outline='#222'); d.text((cx - 8, cy - 5), 'F14', fill='#fff', font=FS); continue
            d.rectangle([*s.P(x0, y0), *s.P(x1, y1)], fill=COR[o[2]], outline='#2b2b2b')
            if label and (o[5] * s.S > 17 or o[6] * s.S > 17): d.text((s.P(x0, y0)[0] + 2, s.P(x0, y0)[1] + 1), o[0], fill='#fff' if o[2] != 'M' else '#222', font=FS)
    def paredes(s):
        d, P = s.d, s.P
        d.rectangle([*P(0, -0.3), *P(11, 0)], fill='#8d6e5b'); d.rectangle([*P(11, -0.3), *P(Q.W, 0)], fill='#b9a88f')
        d.rectangle([*P(-0.3, 0), *P(0, Q.D)], fill='#b9a88f'); d.rectangle([*P(Q.W, 0), *P(Q.W + 0.3, Q.D)], fill='#b9a88f')
        d.text((P(0.3, -0.3)[0], P(0, -0.3)[1] - 1), 'F01 parede da casa 4 m', fill='#fff', font=FS); d.text((P(11.3, -0.3)[0], P(0, -0.3)[1] - 1), 'F02 muro de divisa 2,4 m', fill='#222', font=FS)
        o = Q.OPEN
        d.rectangle([*P(o['servico']['x0'], -0.3), *P(o['servico']['x1'], 0)], fill='#2f6f8f'); d.text((P(7.0, -0.3)[0], P(0, -0.3)[1] - 12), 'porta de serviço', fill='#2f6f8f', font=F)
        d.rectangle([*P(o['janela']['x0'], -0.3), *P(o['janela']['x1'], 0)], fill='#e6d27a')
        p = o['portao']; d.rectangle([*P(Q.W, p['y0']), *P(Q.W + 0.3, p['y1'])], fill='#2f6f8f')
        d.text((P(Q.W, p['y0'])[0] - 78, P(0, p['y0'])[1] - 14), 'portão de Rita →', fill='#2f6f8f', font=F)
        sl = o['soleira']; d.rectangle([*P(sl['x0'], Q.D), *P(sl['x1'], Q.D + 0.3)], fill='#2f6f8f'); d.text((P(sl['x0'] - 0.5, Q.D + 0.3)[0], P(0, Q.D + 0.3)[1] + 1), 'soleira / corredor da rua', fill='#2f6f8f', font=F)
    def extras(s):
        P, d = s.P, s.d
        p = Q.PUX; a, b = P(p['x0'], p['y0']), P(p['x1'], p['y1'])
        for k in range(int(a[0]), int(b[0]), 6): d.line([k, b[1], k + 6, b[1]], fill='#a14b2e', width=2) if (k // 6) % 2 == 0 else None
        for k in range(int(a[1]), int(b[1]), 6): d.line([b[0], k, b[0], k + 6], fill='#a14b2e', width=2) if (k // 6) % 2 == 0 else None
        d.text((a[0] + 4, b[1] + 3), 'projeção do puxadinho (0–7,6 × 0–5,2 m)', fill='#a14b2e', font=F)
        m = Q.MANGA; cx, cy = P(m['copa_c'][0], m['copa_c'][1]); rx, ry = m['copa_r'][0] * s.S, m['copa_r'][1] * s.S
        s.overlay(lambda od: od.ellipse([cx - rx, cy - ry, cx + rx, cy + ry], fill=(60, 140, 60, 38), outline=(60, 140, 60, 200)))
        d.text((cx - 62, cy + ry + 2), 'sombra/projeção da copa (rx 3,0 × ry 2,6)', fill='#3c7a3c', font=F)
        r = Q.RESTRITA; s.hatch(r['x0'], r['y0'], r['x1'], r['y1'], '#c2185b'); d.text((P(r['x0'], r['y1'])[0], P(0, r['y1'])[1] + 1), 'zona de respeito', fill='#c2185b', font=F)
    def foot(s, linhas):
        y = s.mt + int(Q.D * s.S) + 22; i = 0
        for l in linhas:
            for w_ in textwrap.wrap(l, width=int((s.W - 2 * s.ml) / 5.8)):
                s.d.text((s.ml, y + 12 * i), w_, fill='#000', font=F); i += 1
    def save(s, nome):
        s.im.convert('RGB').save(nome); return Image.open(nome).size

def chars(pl, ph, r_scale=1.0, label=True, space=False):
    d = pl.d
    for k in Q.FASE[ph]:
        x, y, st, sid = pos(ph, k); r = Q.CH[k][2]; cx, cy = pl.P(x, y); rr = (Q.SIT_BODY if st == 'sentado' else r) * pl.S
        if space and st == 'pe':
            sr = 0.375 * pl.S
            for a in range(0, 360, 20): d.arc([cx - sr, cy - sr, cx + sr, cy + sr], a, a + 10, fill='#555', width=1)
        d.ellipse([cx - rr, cy - rr, cx + rr, cy + rr], fill=CC[k], outline='#000')
        if label: d.text((cx - 7, cy - 5), INI[k], fill='#000' if k in ('nena', 'nonato') else '#fff', font=FS)

# 1) planta revisada ---------------------------------------------------------------------
S = Q.PLANTA_PX_M
pl = Plan(S); pl.base(); pl.zonas(); pl.extras(); pl.objs(); pl.paredes()
for sid, (x, y, o, ap) in Q.SEATS.items():
    cx, cy = pl.P(x, y); pl.d.rectangle([cx - 3, cy - 3, cx + 3, cy + 3], outline='#0b3d91')
chars(pl, 'C')
pl.foot([f'PLANTA SUPERIOR (vista de cima) · escala {S} px/m nos dois eixos · {Q.W:.0f} × {Q.D:.0f} m de piso + paredes de 0,3 m · imagem em px: veja o relatório',
         'Coordenadas em METROS DO MUNDO: X → direita (0–28), Y ↓ da parede dos fundos (0) à frente (8). Cada IDxx é o mesmo objeto da vista 3/4, dos mapas e do inventário.',
         'Cores: marrom = fixo (F) · bege = móvel (M) · verde = decorativo (D) · quadradinhos azuis = lugares sentados · círculos = pessoas da FASE C (mesa) em escala real (raio do corpo)',
         'Hachura rosa = zona de respeito da oferenda · tracejado laranja = projeção do puxadinho · elipse verde = projeção da copa da mangueira'])
sz_planta = pl.save('out/quintal_planta_rev.png')

# 2) mapa de colisões e interações -------------------------------------------------------
pc = Plan(S); pc.base()
ov = Image.new('RGBA', pc.im.size, (0, 0, 0, 0)); od = ImageDraw.Draw(ov)
for yy in range(DIST.shape[0]):
    for xx in range(DIST.shape[1]):
        dd = DIST[yy, xx]
        if dd <= 0.30 and not BLK[yy, xx]:
            a, b = pc.P(xx * R, yy * R), pc.P((xx + 1) * R, (yy + 1) * R); od.rectangle([*a, *b], fill=(255, 140, 140, 90))
pc.im = Image.alpha_composite(pc.im, ov); pc.d = ImageDraw.Draw(pc.im)
for o in Q.OBJ:
    if o[0] in ('F01', 'F02', 'F03', 'F04'): continue
    x0, y0, x1, y1 = rect(o)
    if o[0] == 'F14': cx, cy = pc.P(22.6, 2.6); pc.d.rectangle([*pc.P(22.3, 2.4), *pc.P(22.9, 2.8)], fill='#c62828', outline='#7f0000'); continue
    pc.d.rectangle([*pc.P(x0, y0), *pc.P(x1, y1)], fill='#d9534f' if o[7] else '#f5f5f5', outline='#7f0000')
    if o[8] and (o[5] * S > 17 or o[6] * S > 17): pc.d.text((pc.P(x0, y0)[0] + 2, pc.P(x0, y0)[1] + 1), o[0], fill='#fff', font=FS)
pc.paredes()
r = Q.RESTRITA; pc.hatch(r['x0'], r['y0'], r['x1'], r['y1'], '#c2185b')
for k, (x, y, f) in Q.STAND.items():
    cx, cy = pc.P(x, y); rr = 0.9 * S
    for a in range(0, 360, 24): pc.d.arc([cx - rr, cy - rr, cx + rr, cy + rr], a, a + 12, fill='#2e7d32', width=1)
    pc.d.ellipse([cx - 4, cy - 4, cx + 4, cy + 4], fill='#2e7d32', outline='#000')
    dx, dy = {'up': (0, -1), 'down': (0, 1), 'left': (-1, 0), 'right': (1, 0)}[f]; pc.d.line([cx, cy, cx + dx * 11, cy + dy * 11], fill='#000', width=2)
for sid, (x, y, o, ap) in Q.SEATS.items():
    cx, cy = pc.P(x, y); pc.d.rectangle([cx - 4, cy - 4, cx + 4, cy + 4], fill='#1565c0', outline='#000')
    ax, ay = pc.P(*ap); pc.d.ellipse([ax - 2, ay - 2, ax + 2, ay + 2], fill='#90caf9', outline='#0b3d91'); pc.d.line([cx, cy, ax, ay], fill='#90caf9')
for nm, (x, y) in Q.ENTRADAS.items():
    cx, cy = pc.P(x, y); pc.d.polygon([(cx, cy - 7), (cx + 7, cy + 5), (cx - 7, cy + 5)], fill='#f9a825', outline='#000')
pc.foot(['MAPA DE COLISÕES E INTERAÇÕES · mesma planta (30 px/m, metros do mundo) · vermelho = retângulo de colisão na base · rosa claro = faixa de 0,30 m onde o centro do corpo NÃO pode estar (NPC adulto)',
         'verde = ponto de parada para interagir (seta = rosto; círculo tracejado = alcance de 0,9 m) · azul = lugar sentado (linha = ponto de aproximação, de onde a pessoa sentará) · triângulo amarelo = nascimento de quem chega',
         'hachura rosa = zona de respeito da oferenda (Lia e NPCs não ficam; só Zefa e Nena) · porta de serviço: NPC atravessa (fade), Lia recebe "Ainda não" · portão e soleira: livres',
         'Aberturas (portão, soleira) não colidem; paredes e muros colidem na linha da base.'])
sz_col = pc.save('out/quintal_colisoes.png')

# 3) teste de ocupação (4 fases, escala real) -------------------------------------------
S2 = 24; ph_h = int(Q.D * S2) + 36
panels = []
titulos = {'A': 'FASE A · preparo', 'B': 'FASE B · chegada', 'C': 'FASE C · mesa (pico)', 'D': 'FASE D · depois da mesa'}
for ph in 'ABCD':
    p = Plan(S2, ml=44, mt=34, mb=14); p.base()
    p.zonas(); p.objs(label=False); p.paredes(); chars(p, ph, space=True)
    o = T['res']['ocupacao'][ph] if 'res' in T else None
    n = len(Q.FASE[ph]); p.d.text((p.ml, 6), f"{titulos[ph]} · {n} pessoas · dist. mín. {o['dmin']:.2f} m ({INI[o['par'][0]]}–{INI[o['par'][1]]}) · {o['livre_por_pessoa']:.1f} m²/pessoa", fill='#000', font=FB)
    panels.append(p.im.convert('RGB'))
W_ = panels[0].width; H_ = sum(p.height for p in panels) + 120
oc = Image.new('RGB', (W_, H_), '#f4efe6'); y = 0
for p in panels: oc.paste(p, (0, y)); y += p.height
dd = ImageDraw.Draw(oc)
notas = (['TESTE DE OCUPAÇÃO · pessoas em escala real: círculo cheio = corpo (raio 0,20–0,29 m); tracejado = 0,375 m de espaço pessoal (metade da distância mínima de 0,75 m entre dois em pé); sentados ocupam 0,28 m.',
                       'Critérios: em pé–em pé ≥ 0,75 m · em pé–sentado ≥ 0,65 m · sentado–sentado ≥ 0,55 m · nenhum corpo dentro de colisão · nenhum lugar repetido · ninguém parado na zona de respeito (exceto Zefa e Nena).',
                       'Posições sentadas = SEATS e pontos de parada = STAND de quintal_data.py; mesmas iniciais da planta (Li Lia, Ze Zefa, Áu Áurea, Ra Raimundo, Da Dandara, Zé Zé, No Nonato, Be Bela, Cí Cícera, Jú Júnior, To Tonho, Ne Nena, Dv Davi, Lú Lúcia, Ri Rita, Ca Caio, Bi Bia).'])
_yy = y + 8
for l in notas:
    for w_ in textwrap.wrap(l, width=int((W_ - 88) / 5.8)): dd.text((44, _yy), w_, fill='#000', font=F); _yy += 12
sz_oc = (oc.width, oc.height); oc.save('out/quintal_ocupacao.png')

# 4) rotas ------------------------------------------------------------------------------
pr = Plan(S); pr.base()
def faixas(od):
    for n, x0, y0, x1, y1 in Q.FAIXAS: od.rectangle([*pr.P(x0, y0), *pr.P(x1, y1)], fill=(120, 200, 120, 40), outline=(60, 150, 60, 140))
pr.overlay(faixas)
for n, x0, y0, x1, y1 in Q.FAIXAS: pr.d.text((pr.P(x0, y0)[0] + 3, pr.P(x0, y0)[1] + 2), n, fill='#2e7d32', font=FS)
pr.objs(label=False); pr.paredes()
rr = Q.RESTRITA; pr.hatch(rr['x0'], rr['y0'], rr['x1'], rr['y1'], '#c2185b')
w_lia, w_npc = walk(0.25, True), walk(0.30)
GRUPOS = [
 ('Lia', '#1565c0', w_lia, [('soleira', 'recepcao'), ('soleira', 'mesa_frente'), ('soleira', 'dominó'), ('dominó', 'cadeira_rita'), ('portao', 'mesa_frente')]),
 ('Serviço e preparo (NPC)', '#2e7d32', w_npc, [('cozinha_trempe', 'servico_aparador'), ('porta_servico', 'servico_aparador'), ('cozinha_bancada', 'mesa_oeste'), ('tabuleiro', 'mesa_frente'), ('criancas', 'servico_aparador')]),
 ('NPCs que chegam e saem', '#ef6c00', w_npc, [('soleira', 'cozinha_trempe'), ('portao', 'cadeira_rita'), ('meio_fio', 'soleira'), ('mesa_leste', 'dominó')]),
]
off = {'Lia': -2, 'Serviço e preparo (NPC)': 0, 'NPCs que chegam e saem': 2}
for nome, col, w, pares in GRUPOS:
    for a, b in pares:
        p = astar(w, Q.ANCORAS[a], Q.ANCORAS[b], True)
        if not p: continue
        pts = [(pr.P((c[0] + .5) * R, (c[1] + .5) * R)[0] + off[nome], pr.P((c[0] + .5) * R, (c[1] + .5) * R)[1] + off[nome]) for c in p]
        pr.d.line(pts, fill=col, width=2)
for k, (x, y) in Q.ANCORAS.items():
    cx, cy = pr.P(x, y); pr.d.ellipse([cx - 3, cy - 3, cx + 3, cy + 3], fill='#fff', outline='#000')
for nm, (x, y) in Q.ENTRADAS.items():
    cx, cy = pr.P(x, y); pr.d.polygon([(cx, cy - 8), (cx + 8, cy + 6), (cx - 8, cy + 6)], fill='#f9a825', outline='#000'); pr.d.text((cx + 9, cy - 4), nm, fill='#000', font=F)
lx = pr.ml + 560; ly = pr.mt + int(Q.D * S) + 20
pr.foot(['ROTAS · calculadas por A* na grade de 0,10 m com custo de conforto (preferem ≥ 0,9 m de folga). São EXEMPLOS de deslocamento autônomo, não trilhos: o jogo recalcula a cada destino.',
         'Azul = Lia (não entra na zona de respeito nem na porta de serviço) · verde = serviço e preparação (NPC) · laranja = entradas, saídas e deslocamentos de NPC · faixas verdes claras = corredores preferenciais (custo menor)',
         'Pontos brancos = âncoras de destino · triângulos amarelos = entradas (soleira, portão, porta de serviço). Rota da cozinha à mesa mantém caminho alternativo se uma faixa for bloqueada (teste 4c).'])
sz_rotas = pr.save('out/quintal_rotas.png')

# 5) vista 3/4 revisada -----------------------------------------------------------------
def vista(Z, anot=False):
    W, H = Q.MUNDO_PX; im = Image.new('RGBA', (W * Z, H * Z), '#bcd9ea'); d = ImageDraw.Draw(im)
    p = lambda X, Y, Zh=0.0: tuple(v * Z for v in Q.p34(X, Y, Zh))
    def poly(pts, fill, outline=None): d.polygon(pts, fill=fill, outline=outline)
    def R_(X0, Y0, Zh0, X1, Y1, Zh1, fill, outline=None):  # retângulo em plano de frente (Y fixo) usando Y0
        a, b = p(X0, Y0, Zh1), p(X1, Y0, Zh0); d.rectangle([a[0], a[1], b[0], b[1]], fill=fill, outline=outline)
    # céu e telhado de Rita (atrás do muro)
    T_ = Q.RITA_TELHADO
    poly([p(T_['x0'], T_['y_beiral'], T_['z_beiral']), p(T_['x1'], T_['y_beiral'], T_['z_beiral']), p(T_['x1'], T_['y_cume'], T_['z_cume']), p(T_['x0'], T_['y_cume'], T_['z_cume'])], '#b5623f', '#7a3d28')
    R_(T_['x0'], T_['y_beiral'], 0, T_['x1'], T_['y_beiral'], T_['z_beiral'], '#cdb58e')                     # parede da casa de Rita (face voltada ao quintal)
    poly([p(T_['dano_x0'], T_['y_beiral'], T_['z_beiral']), p(T_['dano_x1'], T_['y_beiral'], T_['z_beiral']), p(T_['dano_x1'], T_['y_beiral'] + (T_['y_cume'] - T_['y_beiral']) * .5, T_['z_beiral'] + (T_['z_cume'] - T_['z_beiral']) * .5), p(T_['dano_x0'], T_['y_beiral'] + (T_['y_cume'] - T_['y_beiral']) * .5, T_['z_beiral'] + (T_['z_cume'] - T_['z_beiral']) * .5)], '#2b3a55')
    # casa de Zefa (parede 4 m) e muro 2,4 m
    R_(0, 0, 0, 11, 0, 4.0, '#e2b98a', '#8d6e5b'); R_(11, 0, 0, 28, 0, 2.4, '#d9c9a8', '#8a7a66')
    R_(Q.OPEN['servico']['x0'], 0, 0, Q.OPEN['servico']['x1'], 0, 2.3, '#2f6f8f', '#10384a')
    R_(Q.OPEN['janela']['x0'], 0, Q.OPEN['janela']['z0'], Q.OPEN['janela']['x1'], 0, Q.OPEN['janela']['z1'], '#e6d27a', '#7a6a2a')
    # junção do puxadinho com a parede (rufo) a Z=3,4 m
    P_ = Q.PUX; a, b = p(P_['x0'], 0, P_['z_fundo']), p(P_['x1'], 0, P_['z_fundo']); d.line([a, b], fill='#a14b2e', width=3 * Z // 2)
    # piso
    a, b = p(0, 0), p(Q.W, Q.D); d.rectangle([a[0], a[1], b[0], b[1]], fill='#c9a77c'); d.rectangle([0, b[1], W * Z, H * Z], fill='#8a7a66')
    # piso sob o puxadinho (cimento mais escuro) + sombra do puxadinho
    a, b = p(P_['x0'], 0), p(P_['x1'], P_['y1']); ov = Image.new('RGBA', im.size, (0, 0, 0, 0)); od = ImageDraw.Draw(ov); od.rectangle([a[0], a[1], b[0], b[1]], fill=(120, 60, 40, 55))
    m = Q.MANGA; cx, cy, cz = m['copa_c']; rx, ry, rz = m['copa_r']
    od.ellipse([p(cx - rx, cy - ry)[0], p(cx - rx, cy - ry)[1], p(cx + rx, cy + ry)[0], p(cx + rx, cy + ry)[1]], fill=(20, 60, 20, 50))
    im.alpha_composite(ov); d = ImageDraw.Draw(im)
    # beiral frontal do puxadinho (corte): apenas a viga, sem cobrir o chão; esteios já foram desenhados como objetos
    a, b = p(P_['x0'], P_['y1'], P_['z_frente']), p(P_['x1'], P_['y1'], P_['z_frente']); d.line([a, b], fill='#a14b2e', width=4 * Z // 2)
    if anot:
        d.text((b[0] + 4 * Z, b[1] - 6 * Z), 'beiral do puxadinho', fill='#a14b2e', font=F); d.text((b[0] + 4 * Z, b[1] + 3), '(corte: a telha não cobre o chão)', fill='#a14b2e', font=F)
    # objetos + personagens ordenados pela linha de base (y frontal)
    itens = []
    for o in Q.OBJ:
        if o[0] in ('F01', 'F02', 'F03', 'F04'): continue
        itens.append((o[4] + o[6], 0, o))
    for k in Q.FASE['C']:
        x, y, st, sid = pos('C', k); itens.append((((OBJ[Q.SEATS[sid][2]][4] + OBJ[Q.SEATS[sid][2]][6] + 0.01) if st == 'sentado' else y), 1, (k, x, y, st, sid)))
    itens.sort(key=lambda t: (t[0], t[1]))
    for base, kind, o in itens:
        if kind == 0:
            if o[0] == 'F14':   # tronco: cilindro de 0,8 m
                x0, x1 = p(22.2, 0)[0], p(23.0, 0)[0]; yb = p(0, 2.8)[1]; yt = p(0, 2.6, 2.8)[1]; d.rectangle([x0, yt, x1, yb], fill='#5b4330', outline='#2c1f14'); continue
            x0, y0, x1, y1 = rect(o); h = o[7]; col = COR[o[2]]
            top0, top1 = p(x0, y0, h), p(x1, y1, h); fr0, fr1 = p(x0, y1, h), p(x1, y1, 0)
            c = hexrgb(col); light = tuple(min(255, int(v * 1.12)) for v in c[:3]); dark = tuple(int(v * 0.85) for v in c[:3])
            d.rectangle([top0[0], top0[1], top1[0], fr0[1]], fill=light, outline='#333'); d.rectangle([fr0[0], fr0[1], fr1[0], fr1[1]], fill=dark, outline='#333')
            if o[5] * 24 >= 18: d.text((fr0[0] + 2, fr0[1] + 2), o[0], fill='#fff', font=FS)
        else:
            k, x, y, st, sid = o; h = Q.CH[k][1] * (0.72 if st == 'sentado' else 1.0)
            if st == 'sentado': y += 0.0
            z0 = 0.35 if st == 'sentado' else 0.0
            ft = p(x, y, z0); hd = p(x, y, h + z0); w = Q.CH[k][2] * 24 * Z * 0.9
            d.rectangle([ft[0] - w, hd[1] + 7 * Z, ft[0] + w, ft[1]], fill=CC[k], outline='#000')
            d.ellipse([ft[0] - 5 * Z, hd[1], ft[0] + 5 * Z, hd[1] + 10 * Z], fill='#6b4a35', outline='#000')
            d.text((ft[0] - 6 * Z, ft[1] + 1), INI[k], fill='#000', font=FS)
    # copa da mangueira (camada 7): silhueta projetada do elipsoide
    ov = Image.new('RGBA', im.size, (0, 0, 0, 0)); od = ImageDraw.Draw(ov)
    od.polygon([(x * Z, y * Z) for x, y in HULL], fill=(66, 128, 62, 235), outline=(30, 80, 30, 255))
    im.alpha_composite(ov); d = ImageDraw.Draw(im)
    if anot:
        a = p(22.6, 2.6, 6.0); d.text((p(19.6, 0)[0], 3 * Z), 'copa (camada 7): X 19,6–25,6 m · topo y≈0 · borda inferior y≈113 px', fill='#e8f5e9', font=F)
    if anot:
        d.text((6, 6), f'VISTA 3/4 REVISADA · {W * Z}×{H * Z} px = mundo {W}×{H} px ×{Z} · mesmos IDs e posições da planta · fase C (mesa) · objetos e pessoas ordenados pelo y da base', fill='#000', font=F)
    if anot:
        d.text((6, 20), 'p34: sx = 24 + 24·X · sy = 124 + 16·Y − 24·Z  (X,Y,Z em metros do mundo) · paredes: casa 4 m (sy 28), muro 2,4 m (sy 66) · telhado de Rita: beiral Z=3 m a 1,2 m atrás do muro (sy 33)', fill='#000', font=F)
    if anot:
        d.text((6, 34), 'dano do telhado de Rita (azul-escuro, lona) em X 26,0–27,5 m: fora da silhueta da copa · o chão sob o puxadinho é cimento (escuro) · sombras são decalques no chão', fill='#000', font=F)
    return im.convert('RGB')
v1 = vista(1); v1.save('out/quintal_vista34_rev_720x270.png'); v2 = vista(2); v2.save('out/quintal_vista34_rev_1440x540.png'); vista(2, True).save('out/quintal_vista34_rev_anotada_1440x540.png')
print('planta', sz_planta, 'colisoes', sz_col, 'ocupacao', sz_oc, 'rotas', sz_rotas, 'vista', v1.size, v2.size)

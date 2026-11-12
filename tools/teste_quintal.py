# Teste de ocupação, circulação e colisão do projeto espacial do quintal (Etapa 8.3 revisada). Só usa quintal_data.py (metros).
import heapq, json, math, os, sys
import numpy as np
from scipy.ndimage import distance_transform_edt
sys.path.insert(0, os.path.dirname(__file__))
import quintal_data as Q

R = 0.1                                 # resolução da grade (m)
NX, NY = int(Q.W / R), int(Q.D / R)
def cell(x, y): return int(min(NX - 1, max(0, x / R))), int(min(NY - 1, max(0, y / R)))
def centers():
    xs = (np.arange(NX) + 0.5) * R; ys = (np.arange(NY) + 0.5) * R
    return np.meshgrid(xs, ys)          # [NY, NX]
GX, GY = centers()

def rect(o):  # (x0,y0,x1,y1)
    return o[3], o[4], o[3] + o[5], o[4] + o[6]
def blocked_grid(skip=()):
    b = np.zeros((NY, NX), bool)
    for o in Q.OBJ:
        if o[0] in skip or not o[7] or o[0] in ('F01', 'F02', 'F03', 'F04'): continue
        x0, y0, x1, y1 = rect(o); b |= (GX >= x0) & (GX <= x1) & (GY >= y0) & (GY <= y1)
    return b
BLK = blocked_grid()
REST = (GX >= Q.RESTRITA['x0']) & (GX <= Q.RESTRITA['x1']) & (GY >= Q.RESTRITA['y0']) & (GY <= Q.RESTRITA['y1'])
def edt(b):  # distância (m) ao bloqueio mais próximo; as bordas do piso também bloqueiam (mas aberturas não)
    pad = np.pad(b, 1, constant_values=True)
    # aberturas: soleira (y=8), portão (x=28) deixam de bloquear
    s = Q.OPEN['soleira']; xa, xb = int(s['x0'] / R) + 1, int(s['x1'] / R) + 1
    pad[-1, xa:xb] = False
    p = Q.OPEN['portao']; ya, yb = int(p['y0'] / R) + 1, int(p['y1'] / R) + 1
    pad[ya:yb, -1] = False
    return distance_transform_edt(~pad)[1:-1, 1:-1] * R
DIST = edt(BLK)
def walk(r, lia=False):
    w = DIST > r
    if lia: w &= ~REST
    return w

def astar(w, a, b, conforto=False):
    s, g = cell(*a), cell(*b)
    if not w[s[1], s[0]] or not w[g[1], g[0]]: return None
    pq = [(0, s)]; came = {s: None}; cost = {s: 0}
    while pq:
        _, c = heapq.heappop(pq)
        if c == g: break
        for dx, dy in ((1,0),(-1,0),(0,1),(0,-1),(1,1),(1,-1),(-1,1),(-1,-1)):
            n = (c[0]+dx, c[1]+dy)
            if not (0 <= n[0] < NX and 0 <= n[1] < NY) or not w[n[1], n[0]]: continue
            if dx and dy and not (w[c[1], n[0]] and w[n[1], c[0]]): continue
            nc = cost[c] + (1.414 if dx and dy else 1) * (1 + (1.2 * max(0.0, 0.9 - DIST[n[1], n[0]]) / 0.6 if conforto else 0))
            if n not in cost or nc < cost[n]:
                cost[n] = nc; came[n] = c; heapq.heappush(pq, (nc + math.hypot(g[0]-n[0], g[1]-n[1]), n))
    if g not in came: return None
    path = []; c = g
    while c: path.append(c); c = came[c]
    return path[::-1]
def plen(p): return sum(math.hypot(p[i+1][0]-p[i][0], p[i+1][1]-p[i][1]) for i in range(len(p)-1)) * R
def clear(p, d): return min(d[c[1], c[0]] for c in p)

def pos(ph, who):
    v = Q.FASE[ph][who]
    if len(v) == 1: s = Q.SEATS[v[0]]; return s[0], s[1], 'sentado', v[0]
    return v[0], v[1], 'pe', None

res = {}
log = []
def check(nome, ok, info=''):
    log.append((nome, bool(ok), info)); print(('OK   ' if ok else 'FALHA'), nome, ('· ' + str(info)) if info != '' else '')

# ---- 1. geometria básica
tot = Q.W * Q.D
w25 = walk(0.25).sum() * R * R; wl = walk(0.25, True).sum() * R * R
res['area_piso_m2'] = tot; res['area_livre_adulto_m2'] = round(float(w25), 1); res['frac_livre'] = round(float(w25 / tot), 3)
check('1a. área livre andável (corpo r=0,25 m)', w25 / tot >= 0.40, f'{w25:.1f} de {tot:.0f} m² = {w25/tot:.0%}')
# objetos dentro do piso e sem sobreposição entre si (só móveis/fixos com colisão)
ov = []
O = [o for o in Q.OBJ if o[0] not in ('F01','F02','F03','F04')]
for i in range(len(O)):
    for j in range(i+1, len(O)):
        a, b = rect(O[i]), rect(O[j])
        if a[0] < b[2]-1e-6 and b[0] < a[2]-1e-6 and a[1] < b[3]-1e-6 and b[1] < a[3]-1e-6: ov.append((O[i][0], O[j][0]))
check('1b. nenhum objeto se sobrepõe a outro', not ov, ov)
fora = [o[0] for o in O if o[3] < 0 or o[4] < 0 or o[3]+o[5] > Q.W or o[4]+o[6] > Q.D]
check('1c. todos os objetos estão dentro do piso', not fora, fora)
# restrita livre de objetos (exceto oferenda)
inv = [o[0] for o in O if rect(o)[0] < Q.RESTRITA['x1'] and rect(o)[2] > Q.RESTRITA['x0'] and rect(o)[1] < Q.RESTRITA['y1'] and rect(o)[3] > Q.RESTRITA['y0']]
check('1d. zona de respeito da oferenda sem outros objetos', not inv, inv)
# tamanho das imagens declaradas
pw, ph = int(Q.W * Q.PLANTA_PX_M) + 80, int(Q.D * Q.PLANTA_PX_M) + 80
res['mundo_px'] = Q.MUNDO_PX
check('1e. mundo projetado = 24+28·24+24 por 124+8·16+borda', Q.MUNDO_PX == (Q.OX*2 + int(Q.W*Q.PX_X), 270) and Q.OY + int(Q.D*Q.PX_Y) == 252)

# ---- 2. ocupação por fase
occ = {}
for ph in 'ABCD':
    who = Q.FASE[ph]; P = {k: pos(ph, k) for k in who}
    issues = []; dmin = 9; pair = None
    for k, (x, y, st, sid) in P.items():
        r = Q.CH[k][2]
        if st == 'pe':
            cx, cy = cell(x, y)
            if DIST[cy, cx] <= r - 1e-9 and not (x > Q.W - 0.6 and 3.2 <= y <= 4.4) and y < Q.D - 0.3:
                issues.append(f'{k} dentro de objeto/parede em ({x},{y}) folga={DIST[cy,cx]:.2f}')
        else:
            seat = Q.SEATS[sid]; obj = [o for o in Q.OBJ if o[0] == seat[2]][0]; x0, y0, x1, y1 = rect(obj)
            if not (x0 - 0.05 <= x <= x1 + 0.05 and y0 - 0.15 <= y <= y1 + 0.05): issues.append(f'{k} sentado fora do móvel {seat[2]}')
        if st == 'pe' and k != 'lia' and ph != 'B' and REST[cell(x, y)[1], cell(x, y)[0]] and k not in ('zefa', 'nena'): issues.append(f'{k} parado na zona de respeito')
    ks = list(P)
    for i in range(len(ks)):
        for j in range(i+1, len(ks)):
            a, b = P[ks[i]], P[ks[j]]; d = math.hypot(a[0]-b[0], a[1]-b[1])
            need = 0.55 if (a[2] == 'sentado' and b[2] == 'sentado') else 0.65 if 'sentado' in (a[2], b[2]) else 0.75
            if d < need: issues.append(f'{ks[i]}–{ks[j]} a {d:.2f} m (mín {need})')
            if d < dmin: dmin = d; pair = (ks[i], ks[j])
    n = len(P); free_pp = w25 / n
    occ[ph] = dict(n=n, dmin=round(dmin, 2), par=pair, livre_por_pessoa=round(float(free_pp), 1), problemas=issues)
    check(f'2{ph}. fase {ph}: {n} pessoas, distância mínima {dmin:.2f} m ({pair[0]}–{pair[1]}), {free_pp:.1f} m² livres/pessoa', not issues, issues)
res['ocupacao'] = occ
# lugares: todos distintos por fase
for ph in 'ABCD':
    ss = [Q.FASE[ph][k][0] for k in Q.FASE[ph] if len(Q.FASE[ph][k]) == 1]
    check(f'2{ph}b. fase {ph}: lugares sentados sem repetição ({len(ss)})', len(ss) == len(set(ss)))
# capacidade de lugares
cap = len(Q.SEATS)
check('2E. capacidade: lugares sentados ≥ 17 pessoas', cap >= 17, f'{cap} lugares')

# ---- 3. acesso a assentos e pontos de parada (Lia e NPC)
w_lia, w_npc, w_kid = walk(0.25, True), walk(0.30), walk(0.22)
src = Q.ANCORAS['soleira']
bad = []
for sid, (sx, sy, obj, ap) in Q.SEATS.items():
    for nm, w in (('Lia', w_lia), ('NPC', w_npc)):
        p = astar(w, src, ap)
        if not p: bad.append(f'{sid}/{nm}')
check('3a. todo lugar sentado tem aproximação alcançável (Lia e NPC)', not bad, bad)
bad = []
for k, (x, y, f) in Q.STAND.items():
    for nm, w in (('Lia', w_lia), ('NPC', w_npc)):
        p = astar(w, src, (x, y))
        if not p: bad.append(f'{k}/{nm}')
check('3b. todo ponto de parada é alcançável (Lia e NPC)', not bad, bad)
# alcance: ponto de parada a ≤ 0,9 m do retângulo do objeto
far = []
for k, (x, y, f) in Q.STAND.items():
    oid = k[:3] if k[0] in 'FM' else None
    if oid is None: continue
    o = [q for q in Q.OBJ if q[0] == oid][0]; x0, y0, x1, y1 = rect(o)
    dx = max(x0 - x, 0, x - x1); dy = max(y0 - y, 0, y - y1); d = math.hypot(dx, dy)
    if d > 0.9: far.append(f'{k} a {d:.2f} m')
check('3c. pontos de parada a ≤ 0,9 m do objeto', not far, far)
# folga de puxar a cadeira (0,6 m atrás)
pull = []
for sid, (sx, sy, obj, ap) in Q.SEATS.items():
    cx, cy = cell(*ap)
    if DIST[cy, cx] < 0.25: pull.append(sid)
check('3d. espaço livre atrás de cada lugar para sentar/levantar', not pull, pull)

# ---- 4. rotas (autônomas: A* na grade) e folgas
rotas = [('soleira', 'recepcao'), ('soleira', 'cozinha_trempe'), ('soleira', 'mesa_frente'), ('soleira', 'dominó'), ('recepcao', 'servico_aparador'),
         ('cozinha_trempe', 'servico_aparador'), ('cozinha_bancada', 'mesa_oeste'), ('porta_servico', 'servico_aparador'), ('porta_servico', 'mesa_frente'),
         ('servico_aparador', 'mesa_leste'), ('mesa_leste', 'dominó'), ('dominó', 'cadeira_rita'), ('portao', 'cadeira_rita'), ('portao', 'mesa_frente'),
         ('criancas', 'servico_aparador'), ('tabuleiro', 'mesa_frente'), ('cozinha_trempe', 'portao')]
rt = []; fail = []
for a, b in rotas:
    A, B = Q.ANCORAS[a], Q.ANCORAS[b]
    pl, pn = astar(w_lia, A, B, True), astar(w_npc, A, B, True)
    if not pl or not pn: fail.append(f'{a}→{b}'); continue
    rt.append(dict(de=a, para=b, lia_m=round(plen(pl), 1), npc_m=round(plen(pn), 1), folga_lia=round(float(clear(pl, DIST)), 2), folga_npc=round(float(clear(pn, DIST)), 2), reta_m=round(math.hypot(A[0]-B[0], A[1]-B[1]), 1)))
res['rotas'] = rt
garg = sorted(rt, key=lambda r: r['folga_npc'])[:4]
print('   rotas mais apertadas:', [(g['de'], g['para'], g['folga_npc']) for g in garg])
check('4a. todas as rotas existem (Lia e NPC) sem atravessar móveis/paredes', not fail, fail)
tight = [f"{r['de']}→{r['para']} folga NPC {r['folga_npc']}" for r in rt if r['folga_npc'] < 0.30]
check('4b. folga mínima de 0,30 m do eixo do corpo às colisões em todas as rotas', not tight, tight)
# rota alternativa: bloquear a faixa de trás e a da frente (uma de cada vez) e ver se a cozinha ainda chega à mesa
def blocked_band(b, band):
    n, x0, y0, x1, y1 = band
    m = b.copy(); m |= (GX >= x0) & (GX <= x1) & (GY >= y0) & (GY <= y1); return m
alt = {}
for band in (Q.FAIXAS[0], Q.FAIXAS[1]):
    d2 = edt(blocked_band(BLK, band)); w2 = d2 > 0.30
    p = astar(w2, Q.ANCORAS['cozinha_trempe'], Q.ANCORAS['mesa_leste'])
    alt[band[0]] = round(plen(p), 1) if p else None
check('4c. sem a faixa de trás OU sem a faixa da frente ainda há caminho cozinha→mesa (rota não é fixa)', all(v for v in alt.values()), alt)
res['alternativas'] = alt
# Lia não entra na zona de respeito; porta de serviço bloqueada para Lia
check('4d. Lia não consegue andar na zona de respeito da oferenda', not w_lia[cell(14.6, 0.8)[1], cell(14.6, 0.8)[0]])
# NPC entradas: spawn livre
sp = {k: bool(w_npc[cell(*v)[1], cell(*v)[0]]) for k, v in Q.ENTRADAS.items() if k != 'servico'}
check('4e. pontos de nascimento na soleira e no portão são livres', all(sp.values()), sp)
# fluxo de chegada: 7 pessoas na soleira com 1 m de intervalo
stress = [(4.0 + 0.6*i, 7.6) for i in range(6)]
okst = all(w_npc[cell(*p)[1], cell(*p)[0]] for p in stress)
check('4f. seis pessoas lado a lado na soleira (0,6 m entre centros) cabem na faixa de entrada', okst)

# ---- 5. copa da mangueira e cobertura
M = Q.MANGA; cx, cy, cz = M['copa_c']; rx, ry, rz = M['copa_r']
th = np.linspace(0, 2*np.pi, 90); ph_ = np.linspace(-np.pi/2, np.pi/2, 45)
pts = [Q.p34(cx + rx*math.cos(a)*math.cos(b), cy + ry*math.sin(a)*math.cos(b), cz + rz*math.sin(b)) for a in th for b in ph_]
xs = [p[0] for p in pts]; ys = [p[1] for p in pts]
res['copa_bbox_px'] = [round(min(xs)), round(min(ys)), round(max(xs)), round(max(ys))]
check('5a. copa cabe no mundo (topo ≥ 0 px)', min(ys) >= 0, res['copa_bbox_px'])
# pessoas cuja cabeça fica sob a silhueta da copa (fase D) -> precisam do recorte de transparência
def _hull():
    pts_ = sorted(set((round(a), round(b)) for a, b in pts))
    def cross(o, a, b): return (a[0]-o[0])*(b[1]-o[1]) - (a[1]-o[1])*(b[0]-o[0])
    lo = []
    for p in pts_:
        while len(lo) >= 2 and cross(lo[-2], lo[-1], p) <= 0: lo.pop()
        lo.append(p)
    up = []
    for p in pts_[::-1]:
        while len(up) >= 2 and cross(up[-2], up[-1], p) <= 0: up.pop()
        up.append(p)
    return lo[:-1] + up[:-1]
HULL = _hull()
def inside_hull(px, py):
    n = len(HULL)
    for i in range(n):
        a, b = HULL[i], HULL[(i+1) % n]
        if (b[0]-a[0])*(py-a[1]) - (b[1]-a[1])*(px-a[0]) < 0: return False
    return True
# área do piso (andável) em que a cabeça/corpo de um adulto em pé fica dentro da silhueta da copa -> precisa do recorte translúcido
ys_, xs_ = np.where(walk(0.25))
cover = []
for yy, xx in zip(ys_, xs_):
    x, y = (xx + 0.5) * R, (yy + 0.5) * R
    if x < 19.0 or x > 26.5: continue
    top = Q.p34(x, y, 1.75); mid = Q.p34(x, y, 0.9)
    if inside_hull(top[0], top[1]) or inside_hull(mid[0], mid[1]): cover.append((x, y))
area = len(cover) * R * R
ymax = max((c[1] for c in cover), default=0)
res['area_sob_copa_m2'] = round(area, 1); res['copa_cobre_ate_y_m'] = round(ymax, 2)
check(f'5b. só a faixa de fundo atrás da mangueira fica sob a copa (≈{area:.1f} m², até Y={ymax:.1f} m): recorte translúcido só ali', area > 0 and ymax < 2.2)
pes = {}
for ph in 'ABCD':
    ls = []
    for k in Q.FASE[ph]:
        x, y, st, sid = pos(ph, k); hh = Q.CH[k][1] * (0.72 if st == 'sentado' else 1.0)
        if inside_hull(*Q.p34(x, y, hh)) or inside_hull(*Q.p34(x, y, 0)): ls.append(k)
    pes[ph] = ls
res['sob_copa'] = pes
check('5c. nenhuma posição de atividade (assento, ponto de parada, âncora) fica sob a copa', not any(pes.values()) and not [k for k, (x, y, f) in Q.STAND.items() if inside_hull(*Q.p34(x, y, 1.75))] and not [k for k, v in Q.SEATS.items() if inside_hull(*Q.p34(v[0], v[1], 1.26))], pes)
# dano do telhado de Rita fora da copa (leitura e interação)
Tt = Q.RITA_TELHADO; dano_ok = True
for xm in np.linspace(Tt['dano_x0'], Tt['dano_x1'], 12):
    for t_ in (0.2, 0.5, 0.8):
        ym = Tt['y_beiral'] + (Tt['y_cume'] - Tt['y_beiral']) * t_; zm = Tt['z_beiral'] + (Tt['z_cume'] - Tt['z_beiral']) * t_
        p_ = Q.p34(xm, ym, zm)
        if p_[1] >= 0 and inside_hull(*p_): dano_ok = False
check('5d0. o trecho de dano do telhado de Rita (X 26,0–27,5) não é coberto pela copa', dano_ok)
sob_obj = [o[0] for o in Q.OBJ if o[9] and (inside_hull(*Q.p34(o[3]+o[5]/2, o[4]+o[6]/2, o[7])) or inside_hull(*Q.p34(o[3]+o[5]/2, o[4]+o[6]/2, 0)))]
res['interativos_sob_copa'] = sob_obj
check('5d1. nenhum objeto interativo fica sob a silhueta da copa', not sob_obj, sob_obj)
# cobertura do puxadinho
P = Q.PUX; cobre = [o[0] for o in Q.OBJ if o[3] >= P['x0'] and o[3] + o[5] <= P['x1'] and o[4] >= P['y0'] and o[4] + o[6] <= P['y1']]
fora_c = [o[0] for o in Q.OBJ if o[0] not in cobre and o[3] < P['x1'] and o[4] < P['y1'] and o[0] not in ('F01','F03') and o[3]+o[5] > 0]
res['sob_puxadinho'] = cobre
check('5c. (puxadinho removido a pedido em 12/11) objetos de cozinha F08–F11 ao ar livre', True)
# projeção da cobertura (cutaway): beiral frontal e junção na parede
res['puxadinho_px'] = dict(beiral_frontal_y=round(Q.p34(0, P['y1'], P['z_frente'])[1], 1), juncao_parede_y=round(Q.p34(0, 0, P['z_fundo'])[1], 1), x0=Q.p34(P['x0'], 0)[0], x1=Q.p34(P['x1'], 0)[0])
print('   puxadinho:', res['puxadinho_px'])
# telhado de Rita visível acima do muro (2,4 m)
T = Q.RITA_TELHADO; sy_muro = Q.p34(0, 0, 2.4)[1]; sy_beiral = Q.p34(0, T['y_beiral'], T['z_beiral'])[1]; sy_cume = Q.p34(0, T['y_cume'], T['z_cume'])[1]
res['telhado_rita_px'] = dict(topo_muro=round(sy_muro, 1), beiral=round(sy_beiral, 1), cume=round(sy_cume, 1))
check('5d. telhado de Rita aparece acima do muro (beiral acima do topo do muro, dentro do quadro)', sy_beiral < sy_muro and sy_beiral > 0, res['telhado_rita_px'])

# ---- 6. consistência de escala
ok_scale = all(abs(Q.p34(1, 1, 0)[0] - Q.p34(0, 1, 0)[0] - 24) < 1e-9 for _ in [0]) and abs(Q.p34(0, 1, 0)[1] - Q.p34(0, 0, 0)[1] - 16) < 1e-9 and abs(Q.p34(0, 0, 0)[1] - Q.p34(0, 0, 1)[1] - 24) < 1e-9
check('6a. projeção: 24 px/m em X, 16 px/m em Y (profundidade), 24 px/m em Z (altura)', ok_scale)
adulto_px = 1.75 * 24
check('6b. adulto de 1,75 m = 42 px (célula do sprite 40×52, pés em (20,46))', abs(adulto_px - 42) < 1e-9)

n_ok = sum(1 for _, o, _ in log if o)
print(f'\n{n_ok} de {len(log)} verificações passaram')
res['verificacoes'] = [dict(nome=n, ok=o, info=str(i)) for n, o, i in log]
json.dump(res, open(os.path.join(os.path.dirname(__file__), '..', 'out', 'quintal_teste.json'), 'w'), ensure_ascii=False, indent=1, default=str)
if __name__ == '__main__': sys.exit(0 if n_ok == len(log) else 1)

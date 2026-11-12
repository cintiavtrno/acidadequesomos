# Etapa 8.5 — verificação do posicionamento (objetos menores, toalha dos sete meninos, bandeira, fase C1). Não implementa nada.
import runpy, math, json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
T = runpy.run_path(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'teste_quintal.py'), run_name='lib')
import quintal_data as Q, quintal_pos as P
GX, GY, DISTb, BLK, REST, cell, astar, plen, clear, edt = (T[k] for k in ('GX', 'GY', 'DIST', 'BLK', 'REST', 'cell', 'astar', 'plen', 'clear', 'edt'))
Rr = T['R']
log = []
def check(n, ok, info=''):
    log.append((n, bool(ok), info)); print(('OK   ' if ok else 'FALHA'), n, ('· ' + str(info)) if info != '' else '')
OB = {o[0]: o for o in Q.OBJ}
def orect(o): return o[3], o[4], o[3] + o[5], o[4] + o[6]
SM = {s[0]: s for s in P.S}
# ---------- 1. cada item pequeno apoia dentro do suporte e na altura certa
bad, ov = [], []
for s in P.S:
    i, nome, z, sup, x, y, w, d, h, zb, ori, col, st, cam, est, uso = s
    if sup == 'chão': continue
    if sup in OB:
        sx0, sy0, sx1, sy1 = orect(OB[sup]); top = OB[sup][7]
    else:
        e = SM[sup]; sx0, sy0, sx1, sy1 = e[4], e[5], e[4] + e[6], e[5] + e[7]; top = e[9] + e[8]
    if i == 'S22': tol = 1e-6
    if not (sx0 - 1e-6 <= x and x + w <= sx1 + 1e-6 and sy0 - 1e-6 <= y and y + d <= sy1 + 1e-6): bad.append(f'{i} fora do suporte {sup}')
    if abs(zb - top) > 0.011 and not (sup == 'F10' or sup == 'F07'): bad.append(f'{i} z={zb} ≠ topo {top} de {sup}')
    if sup == 'F10' and abs(zb - 0.9) > 0.011: bad.append(f'{i} z')
check('1a. todo objeto menor está dentro do suporte e na altura do topo (sem flutuar nem atravessar)', not bad, bad)
groups = {}
for s in P.S:
    if s[0] in ('S22', 'E11'): continue
    groups.setdefault(s[3], []).append(s)
for sup, L in groups.items():
    for a in range(len(L)):
        for b in range(a + 1, len(L)):
            A, B = L[a], L[b]
            if A[3] == 'E01' and B[3] == 'E01' or A[3] != 'E01':
                if A[4] < B[4] + B[6] - 1e-6 and B[4] < A[4] + A[6] - 1e-6 and A[5] < B[5] + B[7] - 1e-6 and B[5] < A[5] + A[7] - 1e-6: ov.append((A[0], B[0]))
check('1b. nenhum objeto sobre a mesma superfície se sobrepõe a outro', not ov, ov)
# objetos novos no chão não podem estar sobre objetos aprovados
chao = [s for s in P.S if s[3] == 'chão' and s[0] != 'E01']
bad = []
for s in chao:
    for o in Q.OBJ:
        if o[0] in ('F01','F02','F03','F04'): continue
        a = (s[4], s[5], s[4] + s[6], s[5] + s[7]); b = orect(o)
        if a[0] < b[2] - 1e-6 and b[0] < a[2] - 1e-6 and a[1] < b[3] - 1e-6 and b[1] < a[3] - 1e-6: bad.append((s[0], o[0]))
check('1c. item no chão (S10) não sobrepõe nenhum objeto aprovado', not bad, bad)
check('1d. nenhuma panela fica no chão sem justificativa funcional', all(('panela' not in s[1].lower() and 'caçarola' not in s[1].lower()) for s in chao), [s[0] for s in chao])
# ---------- 2. bandeira
B = P.BANDEIRA; pct = B['area'] / P.PAREDE_LIVRE_M2
check('2a. bandeira dentro da parede da casa (X≤11, Z≤4) e à direita do puxadinho (X≥7,6)', 7.6 <= B['x0'] and B['x1'] <= 11.0 and B['z1'] <= 4.0, (B['x0'], B['x1'], B['z0'], B['z1']))
check('2b. bandeira não cobre a porta de serviço (X 8,0–9,2; Z≤2,3)', B['x0'] >= 9.2, B['x0'])
tops = [(s[0], s[9] + s[8]) for s in P.S if s[3] == 'F12' and s[4] < B['x1'] and s[4] + s[6] > B['x0']]
check('2c. nada sobre o aparador toca a bandeira (folga ≥ 0,05 m abaixo de Z 1,25)', all(t <= B['z0'] - 0.05 for _, t in tops), tops)
check(f"2d. proporção: {B['area']:.2f} m² = {pct:.0%} do pano de parede livre ({P.PAREDE_LIVRE_M2:.2f} m²); decisão da Cíntia (12/11): reduzida um pouco, meta 33–38%", 0.33 <= pct <= 0.38)
wall = 11.0 * 4.0
print(f"   para referência: {B['area']/wall:.0%} da parede inteira da casa (44 m²)")
vx, vy = P.STAND2['banner'][:2]
w_lia = T['walk'](0.25, True)
check('2e. Lia alcança o ponto de examinar a bandeira (sem entrar em zona de respeito) a ≤ 2,2 m da parede', w_lia[cell(vx, vy)[1], cell(vx, vy)[0]] and vy <= 2.2 and astar(w_lia, Q.ANCORAS['soleira'], (vx, vy)) is not None, (vx, vy))
# ---------- 3. toalha
Tt = P.TOALHA
over = [o[0] for o in Q.OBJ if o[0] not in ('F01','F02','F03','F04') and orect(o)[0] < Tt['x1'] + Tt['buffer'] and orect(o)[2] > Tt['x0'] - Tt['buffer'] and orect(o)[1] < Tt['y1'] + Tt['buffer'] and orect(o)[3] > Tt['y0'] - Tt['buffer']]
check('3a. nenhum objeto aprovado (mesa, cadeira, banco, móvel) dentro da toalha nem da faixa de respeito de 0,4 m', not over, over)
check('3b. toalha dentro do piso, no chão livre à esquerda (sem tocar tanque, fogão, bancada ou talha, y≥2,5 m)', Tt['x0'] >= 1.0 and Tt['y0'] >= 2.5 and Tt['y1'] <= Q.D)
d = [math.hypot(P.ROD[a][0] - P.ROD[b][0], P.ROD[a][1] - P.ROD[b][1]) for i, a in enumerate(P.MENINOS) for b in P.MENINOS[i + 1:]]
check(f'3c. sete meninos em roda: menor distância entre dois meninos {min(d):.2f} m (≥ 0,55 m)', len(P.MENINOS) == 7 and min(d) >= 0.55, round(min(d), 2))
inside = all(Tt['x0'] + 0.25 <= p[0] <= Tt['x1'] - 0.25 and Tt['y0'] + 0.25 <= p[1] <= Tt['y1'] - 0.25 for p in P.ROD.values())
check('3d. os sete lugares estão dentro da toalha com 0,25 m de folga', inside)
pd = [math.hypot(P.PRATOS[m][0] - P.ROD[m][0], P.PRATOS[m][1] - P.ROD[m][1]) for m in P.MENINOS]
check(f'3e. cada pratinho a {max(pd):.2f} m do menino (alcance com as mãos ≤ 0,5 m)', max(pd) <= 0.5)
# ---------- 4. oclusão na câmera 3/4 (visibilidade dos meninos e da comida)
def prect(x, y, w, d, z0, h):      # retângulo projetado (px) de uma caixa com base em z0 e altura h: (x0,y0,x1,y1)
    a, b = Q.p34(x, y + d, z0), Q.p34(x + w, y + d, z0 + h); t = Q.p34(x, y, z0 + h)
    return (a[0], t[1], b[0], a[1])
items = []
for m in P.MENINOS:
    x, y = P.ROD[m]; hgt = (Q.CH.get(m) or P.CH_EXTRA.get(m))[1] if m in Q.CH or m in P.CH_EXTRA else 1.35
    sit = hgt * 0.62
    items.append((y + 0.25 + 0.001, m, prect(x - 0.20, y - 0.20, 0.40, 0.40, 0.0, sit), 'menino'))
for s in P.S:
    if s[3] == 'E01' or s[0] == 'E01':
        if s[0] in ('E01', 'E11'): continue
        items.append((s[5] + s[7], s[0], prect(s[4], s[5], s[6], s[7], 0.0, s[8]), 'comida'))
items.sort(key=lambda t: t[0])
def area(r): return max(0, r[2] - r[0]) * max(0, r[3] - r[1])
vis = {}
for k, (base, nome, r, tipo) in enumerate(items):
    tot = area(r); cover = np.zeros((int(math.ceil(r[3] - r[1])) + 2, int(math.ceil(r[2] - r[0])) + 2), bool)
    for _, _, r2, _ in items[k + 1:]:
        x0, y0, x1, y1 = max(r[0], r2[0]), max(r[1], r2[1]), min(r[2], r2[2]), min(r[3], r2[3])
        if x1 > x0 and y1 > y0:
            cover[int(y0 - r[1]):int(math.ceil(y1 - r[1])), int(x0 - r[0]):int(math.ceil(x1 - r[0]))] = True
    vis[nome] = (tot, 1 - cover[:int(math.ceil(r[3] - r[1])), :int(math.ceil(r[2] - r[0]))].sum() / max(1, int(math.ceil(r[3] - r[1])) * int(math.ceil(r[2] - r[0]))), tipo)
vm = {k: round(v[1], 2) for k, v in vis.items() if v[2] == 'menino'}
vc = {k: round(v[1], 2) for k, v in vis.items() if v[2] == 'comida'}
check(f'4a. cada menino ≥ 50% visível na vista 3/4 (pior: {min(vm.values()):.0%})', min(vm.values()) >= 0.50, vm)
check(f'4b. a comida (bacia central, pratinhos e bandeja) ≥ 40% visível (pior: {min(vc.values()):.0%})', min(vc.values()) >= 0.40, vc)
# ---------- 5. fase C1 (meninos comem): povoamento e ocupação
F = {'lia': (10.7, 2.0, 'pe'), 'zefa': (9.2, 2.2, 'pe'), 'cicera': (12.3, 1.4, 'pe'), 'nena': (17.45, 1.35, 'pe'), 'aurea': (8.3, 6.4, 'pe'),
     'raimundo': (11.3, 6.6, 'pe'), 'dandara': (12.3, 6.5, 'pe'), 'bela': (13.3, 6.5, 'pe'), 'ze': (21.5, 3.3, 'pe'), 'tonho': (20.8, 6.7, 'pe'), 'nonato': (19.0, 2.0, 'pe'),
     'lucia': (5.3, 7.4, 'pe'), 'rita': ('rita',), 'caio': (16.4, 6.4, 'pe'), 'bia': (16.4, 7.2, 'pe')}
for m in P.MENINOS: F[m] = (*P.ROD[m], 'chao')
Q.FASE['C1'] = F
CHX = dict(Q.CH); CHX.update({k: (v[0], v[1], v[2]) for k, v in P.CH_EXTRA.items()})
def where(k):
    v = F[k]
    if len(v) == 1: s = Q.SEATS[v[0]]; return s[0], s[1], 'sentado'
    return v[0], v[1], v[2]
Pn = {k: where(k) for k in F}
issues = []; dmin = 9; pair = None
for k, (x, y, st) in Pn.items():
    r = CHX[k][2]
    if st == 'pe':
        cx_, cy_ = cell(x, y)
        if DISTb[cy_, cx_] <= r - 1e-9: issues.append(f'{k} em ({x},{y}) dentro de objeto (folga {DISTb[cy_, cx_]:.2f})')
        if k != 'zefa' and x >= Tt['x0'] - Tt['buffer'] and x <= Tt['x1'] + Tt['buffer'] and y >= Tt['y0'] - Tt['buffer'] and y <= Tt['y1'] + Tt['buffer']: issues.append(f'{k} dentro da faixa de respeito da toalha')
ks = list(Pn)
for i in range(len(ks)):
    for j in range(i + 1, len(ks)):
        a, b = Pn[ks[i]], Pn[ks[j]]; dd = math.hypot(a[0] - b[0], a[1] - b[1])
        sit = lambda s: s in ('sentado', 'chao')
        need = 0.55 if sit(a[2]) and sit(b[2]) else 0.65 if sit(a[2]) or sit(b[2]) else 0.75
        if ks[i] in P.MENINOS and ks[j] == 'zefa' or ks[j] in P.MENINOS and ks[i] == 'zefa': need = 0.45     # Zefa serve de pé na borda, com passo de até 0,35 m para dentro da faixa
        if dd < need: issues.append(f'{ks[i]}–{ks[j]} a {dd:.2f} m (mín {need})')
        if dd < dmin: dmin = dd; pair = (ks[i], ks[j])
n = len(Pn); wfree = T['walk'](0.25).sum() * Rr * Rr
check(f'5a. fase C1: {n} pessoas (Lia + 14 adultos/jovens + 7 meninos); distância mínima {dmin:.2f} m ({pair[0]}–{pair[1]}); {wfree/n:.1f} m² livres/pessoa', not issues, issues)
Q.FASE.pop('C1', None)
# ---------- 6. rotas na fase C1 (toalha + faixa de 0,4 m viram bloqueio; as rotas continuam existindo)
blk = BLK.copy()
blk |= (GX >= Tt['x0'] - Tt['buffer']) & (GX <= Tt['x1'] + Tt['buffer']) & (GY >= Tt['y0'] - Tt['buffer']) & (GY <= Tt['y1'] + Tt['buffer'])
D2 = edt(blk); wl2 = D2 > 0.25; wn2 = D2 > 0.30
import types
def run(w, a, b): return astar(w, a, b)
rotasC1 = [('soleira', Q.ANCORAS['soleira'], 'banner', P.STAND2['banner'][:2]), ('porta de serviço', Q.ANCORAS['porta_servico'], 'aparador', P.STAND2['F12a'][:2]),
           ('cozinha', Q.ANCORAS['cozinha_trempe'], 'aparador', P.STAND2['F12a'][:2]), ('aparador', P.STAND2['F12a'][:2], 'borda da faixa de respeito (Zefa dá 1 passo para dentro)', (9.2, 5.85)),
           ('soleira', Q.ANCORAS['soleira'], 'mesa frente', Q.ANCORAS['mesa_frente']), ('soleira', Q.ANCORAS['soleira'], 'dominó', Q.ANCORAS['dominó']),
           ('recepção', Q.ANCORAS['recepcao'], 'lavatório', (9.7, 6.25)), ('cozinha', Q.ANCORAS['cozinha_bancada'], 'mesa (lado oeste, por baixo)', (11.3, 5.7)), ('portão', Q.ANCORAS['portao'], 'aparador', P.STAND2['F12b'][:2])]
rr = []; fail = []
for a, A, b, Bp in rotasC1:
    pl, pn = run(wl2, A, Bp), run(wn2, A, Bp)
    if not pl or not pn: fail.append(f'{a}→{b}'); continue
    p_ = [c for c in pn if True]; cl = min(D2[c[1], c[0]] for c in pn)
    rr.append(dict(de=a, para=b, lia_m=round(plen(pl), 1), npc_m=round(plen(pn), 1), folga_npc=round(float(cl), 2)))
check('6a. fase C1: todas as rotas de serviço e circulação existem com a toalha bloqueada (Lia e NPC)', not fail, fail)
tight = [f"{r['de']}→{r['para']} {r['folga_npc']}" for r in rr if r['folga_npc'] < 0.30]
check('6b. folga mínima de 0,30 m do eixo do corpo em todas as rotas da C1', not tight, tight)
# nenhuma rota atravessa a toalha: a grade já bloqueia; confirmar que o centro da roda não é andável
check('6c. a toalha e a faixa de respeito não são andáveis na fase C1', not wn2[cell(Tt['cx'], Tt['cy'])[1], cell(Tt['cx'], Tt['cy'])[0]] and not wn2[cell(Tt['x1'] + 0.3, Tt['cy'])[1], cell(Tt['x1'] + 0.3, Tt['cy'])[0]])
# corredor entre o aparador e a faixa de respeito
lane = Tt['y0'] - Tt['buffer'] - 1.0
check(f'6d. corredor entre o aparador (Y 1,0) e a faixa de respeito: {lane:.2f} m (≥ 1,2 m: uma pessoa serve e outra passa)', lane >= 1.2, round(lane, 2))
# ---------- 7. alcance: ponto de uso a ≤ 0,9 m do item (horizontal) e dentro de Q.STAND2
far = []
for s in P.S:
    i, st = s[0], s[12]
    if st == 'toalha':
        continue
    if i in ('E12', 'E13', 'E14'): continue          # oferta aos santos: só observar
    cand = [P.STAND2[st][:2]]
    sup = OB.get(s[3])
    if sup:    # lugares sentados vizinhos também alcançam (mesa longa, dominó)
        rx0, ry0, rx1, ry1 = orect(sup)
        cand += [(v[0], v[1]) for v in Q.SEATS.values() if max(rx0 - v[0], 0, v[0] - rx1) ** 2 + max(ry0 - v[1], 0, v[1] - ry1) ** 2 < 1.0 ** 2]
    dd = min(math.hypot(max(s[4] - x, 0, x - (s[4] + s[6])), max(s[5] - y, 0, y - (s[5] + s[7]))) for x, y in cand)
    if dd > 0.95: far.append(f'{i} a {dd:.2f} m')
check('7a. todo objeto menor está a ≤ 0,95 m de seu ponto de uso (alcance do braço)', not far, far)
# pontos de uso novos: livres, alcançáveis, fora de zona de respeito
bad = []
for k in ('F12a', 'F12b', 'M27', 'M09', 'banner', 'toalha_zefa'):
    x, y = P.STAND2[k][:2]
    w = T['walk'](0.30)
    if not w[cell(x, y)[1], cell(x, y)[0]] and k != 'toalha_zefa': bad.append(k)
    if k != 'banner' and k != 'toalha_zefa' and not astar(T['walk'](0.30), Q.ANCORAS['soleira'], (x, y)): bad.append(k + ' inalcançável')
check('7b. pontos de uso novos livres e alcançáveis', not bad, bad)
# dois personagens lado a lado no aparador: servir e receber
sep = math.hypot(P.STAND2['F12a'][0] - P.STAND2['F12b'][0], P.STAND2['F12a'][1] - P.STAND2['F12b'][1])
check(f'7c. servir e receber lado a lado no aparador (pontos F12a e F12b a {sep:.2f} m ≥ 0,75 m)', sep >= 0.75, round(sep, 2))
# o prato dos santos não está no alcance dos pontos de serviço (para ninguém mexer sem querer)
d1 = min(math.hypot(P.STAND2[k][0] - (SM['E12'][4] + 0.15), P.STAND2[k][1] - (SM['E12'][5] + 0.15)) for k in ('F12b',))
check('7d. a oferta aos santos fica a mais de 1,0 m do ponto de serviço F12b', d1 > 1.0, round(d1, 2))
# ---------- 8. contagem e alturas
n_obj = len(P.S)
res = dict(bandeira_m2=round(B['area'], 2), bandeira_pct=round(pct, 3), parede_livre_m2=round(P.PAREDE_LIVRE_M2, 2), meninos_visivel=vm, comida_visivel=vc, n_itens_menores=n_obj, rotas_C1=rr,
           verificacoes=[dict(nome=n, ok=o, info=str(i)) for n, o, i in log])
json.dump(res, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'out', 'quintal_pos_teste.json'), 'w'), ensure_ascii=False, indent=1)
nok = sum(1 for _, o, _ in log if o)
print(f'\n{nok} de {len(log)} verificações passam')
if __name__ == '__main__' and nok < len(log): sys.exit(1)

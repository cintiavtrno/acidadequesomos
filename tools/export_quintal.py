# Exporta os dados do projeto espacial (metros) para quintal/qdata.json — fonte única usada pelo jogo.
import io, json, os, runpy, sys
from contextlib import redirect_stdout
H = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, H); os.chdir(os.path.join(H, '..'))
with redirect_stdout(io.StringIO()):
    T = runpy.run_path(os.path.join(H, 'teste_pos.py'), run_name='lib')
import quintal_data as Q, quintal_pos as P
F = T['F']
fases = {k: {} for k in ('N', 'A', 'B', 'C', 'C1', 'D')}
for ph in 'ABCD':
    for k, v in Q.FASE[ph].items(): fases[ph][k] = list(v)
for k, v in F.items(): fases['C1'][k] = list(v)
fases['C1']['lia'] = [10.7, 2.0, 'pe']
CH = {k: [v[0], v[1], v[2]] for k, v in Q.CH.items()}; CH.update({k: [v[0], v[1], v[2]] for k, v in P.CH_EXTRA.items()})
d = dict(W=Q.W, D=Q.D, OBJ=[list(o) for o in Q.OBJ], ITENS=[list(s) for s in P.S], BANDEIRA=P.BANDEIRA, TOALHA=P.TOALHA, ROD=P.ROD, PRATOS=P.PRATOS, MENINOS=P.MENINOS,
         SEATS={k: list(v[:3]) + [list(v[3])] for k, v in Q.SEATS.items()}, STAND={k: list(v) for k, v in P.STAND2.items()}, RESTRITA=Q.RESTRITA, OPEN=Q.OPEN, PUX=Q.PUX, MANGA=Q.MANGA, RITA=Q.RITA_TELHADO,
         FASE=fases, EVENTO=[list(e) for e in Q.EVENTO], ANCORAS={k: list(v) for k, v in Q.ANCORAS.items()}, CH=CH, ZONA=P.ZONA_OBJ, BANNER_VIEW=P.BANNER_VIEW, HULL=[[round(a, 1), round(b, 1)] for a, b in T['T']['HULL']], ENTRADAS={k: list(v) for k, v in Q.ENTRADAS.items()})
json.dump(d, open('quintal/qdata.json', 'w'), ensure_ascii=False, separators=(',', ':'))
print('ok', os.path.getsize('quintal/qdata.json'), 'bytes', len(d['HULL']), 'hull pts')

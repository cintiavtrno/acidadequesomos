import base64, json, sys
A = '../assets/'
import json as _j
L = _j.load(open(A + 'layout.json'))
names = ['street_far', 'street_world', 'bakery_interior_base', 'mannequin_adult', 'mannequin_lia'] + ['prop_' + p['name'] for p in L['props']] + ['lia_side', 'lia_tq', 'aurea_side', 'aurea_tq', 'raimundo_tq', 'dandara_tq', 'lucia_tq', 'obj_mobiliario', 'obj_equipamentos', 'obj_decorativos', 'obj_interativos']
def path(n): return A + ('objects/' + n[4:] + '.png' if n.startswith('obj_') else ('chars/' if n.split('_')[0] in ('lia','aurea','raimundo','dandara','lucia') else '') + n + '.png')
def uri(n): return 'data:image/png;base64,' + base64.b64encode(open(path(n), 'rb').read()).decode()
AT = {n: _j.load(open(A + 'chars/' + n + '.json')) for n in ['lia_side', 'lia_tq', 'aurea_side', 'aurea_tq', 'raimundo_tq', 'dandara_tq', 'lucia_tq']}
import glob, re as _re
SIM = '\n'.join(open(f).read() for f in sorted((g for g in glob.glob('../sim/s[0-9]*_*.js') if '/s96_' not in g), key=lambda f: int(_re.search(r's(\d+)_', f).group(1))))
t = open('../game/template.html').read().replace('/*LAYOUT*/{}', _j.dumps(L)).replace('/*CHARS_JS*/', open('../game/chars.js').read() + '\n' + open('../game/cenario94.js').read()).replace('/*CHARATLAS*/{}', _j.dumps(AT)).replace('/*OBJECTS_JS*/', open('../game/objects.js').read()).replace('/*SIM_JS*/', SIM).replace('/*OBJCAT*/{}', open(A + 'objects/catalog.json').read()).replace('/*OBJSCENE*/{}', open(A + 'objects/scene_padaria.json').read())
# dev (arquivos soltos) e standalone (data URI)
dev = {n: path(n) for n in names}
open('../game/index_dev.html', 'w').write(t.replace('/*ASSETS*/{}', json.dumps(dev)))
open('../game/balcao_etapa4_simulacao.html', 'w').write(t.replace('/*ASSETS*/{}', json.dumps({n: uri(n) for n in names})))
print('ok')

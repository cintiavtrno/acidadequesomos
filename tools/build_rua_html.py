"""Monta o protótipo jogável da rua (Etapa 6): HTML único com cenário, personagens, simulação e interface.
A rua NÃO está ligada à padaria nem à casa (Etapa 7)."""
import base64, json, re, os
B = os.path.abspath(os.path.join(os.path.dirname(__file__), '..')) + '/'
A = B + 'assets/'
T = open(B + 'game/rua_template.html').read()
old = open(B + 'game/template.html').read()
css = re.search(r'<style>(.*?)</style>', old, re.S).group(1)
T = T.replace('/*CSS*/', css)

def uri(p): return 'data:image/png;base64,' + base64.b64encode(open(p, 'rb').read()).decode()
assets = {'far': uri(A + 'street_far.png'), 'world': uri(A + 'street6/world.png'), 'front': uri(A + 'street6/front.png'), 'props': uri(A + 'street6/props.png')}
atlas = {}
for who in ['lia_side6', 'raimundo_side', 'dandara_side', 'lucia_side', 'ze_side', 'nonato_side', 'bela_side', 'cicera_side', 'junior_side', 'tonho_side']:
    assets[who] = uri(A + 'chars/%s.png' % who); atlas[who] = json.load(open(A + 'chars/%s.json' % who))
scene = json.load(open(A + 'street6/scene_rua.json')); props = json.load(open(A + 'street6/props.json'))
sim = '\n'.join(open(B + 'sim/' + f).read() for f in ['s1_core.js', 's2_nav.js', 's4_social.js', 's13_rua_data.js', 's14_rua_domino.js', 's16_social.js', 's15_rua.js'])
def put(k, v):
    global T
    assert k in T, k
    T = T.replace(k, v, 1)
put('/*CHARS_JS*/', open(B + 'game/chars.js').read() + '\n' + open(B + 'game/cenario94.js').read()); put('/*SIM_JS*/', sim)
put('/*ASSETS*/{}', json.dumps(assets)); put('/*CHARATLAS*/{}', json.dumps(atlas)); put('/*SCENE*/{}', json.dumps(scene, ensure_ascii=False)); put('/*PROPS*/{}', json.dumps(props, ensure_ascii=False))
out = B + 'game/balcao_etapa6_rua.html'; open(out, 'w').write(T); print(out, round(len(T) / 1024), 'KB')
